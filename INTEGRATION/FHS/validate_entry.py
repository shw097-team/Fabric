#!/usr/bin/env python3
"""FHS-NAV/v1 r2: strict local navigation, never grants permission or writes a repo."""
import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

EXPECTED_REPOS = {
    "sbl": ("shw097-team/SBL", "PRODUCT_TPM"),
    "fabric": ("shw097-team/Fabric", "POLICY_FAR"),
    "hgk": ("shw097-team/HG-KSEOS", "NATIVE_CONTROL_SOURCE_EXPORT"),
    "pipd": ("shw097-team/PIPD-LS-SP", "CANONICAL_COMPILER_PRE_CUTOVER"),
}
# Exact r1 public route semantics preserved; any change needs formal ABI+Owner review.
EXPECTED_ROUTE_DETAILS = {
    "sbl_product": ("sbl", ("pipd",), "NAVIGATION_ONLY"),
    "fabric_policy": ("fabric", ("hgk",), "NAVIGATION_ONLY"),
    "hgk_admission": ("hgk", ("fabric", "sbl"), "NAVIGATION_ONLY"),
    "pipd_canonical": ("pipd", ("sbl",), "NAVIGATION_ONLY"),
    "cross_repo": (None, ("sbl", "fabric", "hgk", "pipd"), "SPLIT_PR_BY_ORIGINAL_DOMAIN"),
    "hermes_runtime": (None, ("hgk", "fabric"), "HOST_SOURCE_READER_REQUIRED"),
}
# Verified public source pointers, NOT canonical host readers or proof of native load.
NAV_READERS = {
    "sbl_product": {"url": "https://github.com/shw097-team/SBL/blob/main/sbl_sp/plugins/tpm_sp/SKILL.md", "reader": "SBL_PRODUCT_SOURCE_READER", "next": "SBL_PRODUCT_OWNER_AND_PIPD_COMPILER_RECHECK", "host_required": False},
    "fabric_policy": {"url": "https://github.com/shw097-team/Fabric/blob/main/INTEGRATION/SOURCE-PROJECTION.md", "reader": "FABRIC_MIRROR_TO_ORIGINAL_POLICY_SOURCE_READER", "next": "ORIGINAL_FABRIC_POLICY_OWNER_SOURCE_READ", "host_required": True},
    "hgk_admission": {"url": "https://github.com/shw097-team/HG-KSEOS/blob/main/README.md", "reader": "HGK_SOURCE_EXPORT_TO_NATIVE_ISSUER_READER", "next": "HGK_ORIGINAL_OWNER_AND_ISSUER_READBACK", "host_required": True},
    "pipd_canonical": {"url": "https://github.com/shw097-team/PIPD-LS-SP/blob/main/src/pipd_ls_sp/pipeline.py", "reader": "PIPD_ORIGINAL_COMPILER_SOURCE_READER", "next": "PIPD_OWNER_COMPILER_ABI_AND_U04_CHECK", "host_required": False},
    "cross_repo": {"url": None, "reader": "EACH_AFFECTED_REPOSITORY_SOURCE_READER", "next": "PER_DOMAIN_SOURCE_READ_AND_SPLIT_CANDIDATE_PRS", "host_required": True},
    "hermes_runtime": {"url": None, "reader": "ORIGINAL_HERMES_HOST_PROFILE_PID_LOADER_READER", "next": "FRESH_HOST_SOURCE_LOADED_INVOKED_READBACK", "host_required": True},
}
MAP_KEYS = {"schema_version", "identity", "effect_permission", "unknown_route", "source_state", "repositories", "routes"}
ROUTE_KEYS = {"task_class", "primary_repo", "affected_repos", "claim"}
MAX_BYTES = 262144
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")

def no_duplicate_keys(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError("DUPLICATE_JSON_KEY")
        d[k] = v
    return d

def read_json(path):
    p = Path(path)
    if not p.is_file() or p.is_symlink() or p.stat().st_size > MAX_BYTES:
        raise ValueError("MAP_PATH_OR_SIZE_UNSAFE")
    return json.loads(p.read_text("utf-8"), object_pairs_hook=no_duplicate_keys)

def validate(d):
    errors = []
    if type(d) is not dict:
        return ["MAP_NOT_OBJECT"]
    if set(d) != MAP_KEYS:
        errors.append("TOP_LEVEL_FIELDS")
    for k, v in {"schema_version": "FHS-NAV/v1", "identity": "FABRIC_HOSTED_NON_AUTHORITATIVE_INDEX", "effect_permission": "NONE", "unknown_route": "HOLD_AFFECTED_WRITE_ONLY", "source_state": "PROPOSED_NOT_OWNER_RATIFIED"}.items():
        if type(d.get(k)) is not str or d.get(k) != v:
            errors.append("FIELD_" + k)
    repos = d.get("repositories")
    if type(repos) is not dict or set(repos) != set(EXPECTED_REPOS):
        errors.append("REPO_SET")
        repos = {}
    for key, (name, domain) in EXPECTED_REPOS.items():
        item = repos.get(key)
        if type(item) is not dict or set(item) != {"full_name", "default_branch", "domain"}:
            errors.append("REPO_FIELDS_" + key)
            continue
        if any(type(item.get(k)) is not str for k in item):
            errors.append("REPO_TYPES_" + key)
        if (item.get("full_name"), item.get("default_branch"), item.get("domain")) != (name, "main", domain):
            errors.append("REPO_SEMANTICS_" + key)
    routes = d.get("routes")
    if type(routes) is not list or len(routes) != len(EXPECTED_ROUTE_DETAILS):
        errors.append("ROUTE_COUNT")
        routes = routes if type(routes) is list else []
    seen = set()
    for item in routes:
        if type(item) is not dict or set(item) != ROUTE_KEYS:
            errors.append("ROUTE_FIELDS_OR_TYPE")
            continue
        task = item.get("task_class")
        if type(task) is not str or not re.fullmatch(r"[a-z_]{3,32}", task):
            errors.append("ROUTE_TASK_TYPE")
            continue
        if task in seen:
            errors.append("ROUTE_DUPLICATE_" + task)
        seen.add(task)
        if task not in EXPECTED_ROUTE_DETAILS:
            errors.append("ROUTE_UNKNOWN_" + task)
            continue
        primary, affected, claim = EXPECTED_ROUTE_DETAILS[task]
        actual = (item.get("primary_repo"), item.get("affected_repos"), item.get("claim"))
        if type(actual[1]) is not list or any(type(x) is not str for x in actual[1]) or type(actual[2]) is not str:
            errors.append("ROUTE_TYPES_" + task)
        if actual != (primary, list(affected), claim) or (primary is not None and type(actual[0]) is not str):
            errors.append("ROUTE_SEMANTIC_DRIFT_" + task)
    if seen != set(EXPECTED_ROUTE_DETAILS):
        errors.append("ROUTE_COVERAGE")
    return errors

def fetch_main(name, timeout=8):
    if name not in {name for name, _ in EXPECTED_REPOS.values()}:
        raise ValueError("REPO_NOT_ALLOWLISTED")
    r = urllib.request.Request("https://api.github.com/repos/" + name + "/branches/main", headers={"User-Agent": "FHS-NAV-READ-ONLY/2", "Accept": "application/vnd.github+json"}, method="GET")
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        data = json.loads(resp.read(MAX_BYTES + 1))
    sha = data.get("commit", {}).get("sha")
    if type(sha) is not str or not SHA_RE.fullmatch(sha):
        raise ValueError("INVALID_GITHUB_SHA")
    return sha

def validate_expected_snapshot(doc, now=None):
    if type(doc) is not dict or set(doc) != {"schema_version", "observed_at_utc", "source_scope", "expected_heads"}:
        raise ValueError("EXPECTED_SNAPSHOT_SCHEMA")
    if doc["schema_version"] != "FHS-HEAD-EXPECTATION/v1" or doc["source_scope"] != "GITHUB_MAIN_ONLY":
        raise ValueError("EXPECTED_SNAPSHOT_SCOPE")
    if type(doc["expected_heads"]) is not dict or set(doc["expected_heads"]) != set(EXPECTED_REPOS):
        raise ValueError("EXPECTED_SNAPSHOT_REPOS")
    if any(type(s) is not str or not SHA_RE.fullmatch(s) for s in doc["expected_heads"].values()):
        raise ValueError("EXPECTED_SNAPSHOT_SHA")
    try:
        stamp = dt.datetime.fromisoformat(doc["observed_at_utc"].replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError):
        raise ValueError("EXPECTED_SNAPSHOT_TIME") from None
    if stamp.tzinfo is None:
        raise ValueError("EXPECTED_SNAPSHOT_TIMEZONE")
    now = now or dt.datetime.now(dt.timezone.utc)
    age = (now - stamp).total_seconds()
    if age < -120 or age > 900:
        raise ValueError("EXPECTED_SNAPSHOT_STALE")
    return doc["expected_heads"]

def compare_heads(expected, fetched):
    if set(expected) != set(EXPECTED_REPOS) or set(fetched) != set(EXPECTED_REPOS):
        return ["HEAD_SET_MISMATCH"]
    return ["SOURCE_DRIFT_" + k for k in EXPECTED_REPOS if fetched[k] != expected[k]]

def route_result(doc, task):
    if task not in EXPECTED_ROUTE_DETAILS:
        return {"status": "HOLD_AFFECTED_WRITE", "reason": "UNKNOWN_TASK", "claim_ceiling": "NAVIGATION_ONLY"}, 3
    rule = next(r for r in doc["routes"] if r["task_class"] == task)
    info = NAV_READERS[task]
    return {"status": "NAVIGATION_CANDIDATE_ONLY", "route": rule,
            "original_reader_kind": info["reader"], "public_source_pointer": info["url"],
            "original_reader_verified": False, "owner_ratification_verified": False,
            "native_host_required": info["host_required"], "next_action": info["next"],
            "handoff_ref": "REQUIRE_ORIGINAL_ABI_SOURCE_REF", "claim_ceiling": "NAVIGATION_ONLY",
            "effect_permission": "NONE"}, 0

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", default=str(Path(__file__).with_name("repository-map.json")))
    parser.add_argument("--route")
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--expected-heads", help="operator-supplied fresh SHA snapshot; required with --online")
    args = parser.parse_args(argv)
    try:
        if args.map != str(Path(__file__).with_name("repository-map.json")) and not Path(args.map).resolve().is_relative_to(Path.cwd().resolve()):
            raise ValueError("CUSTOM_MAP_OUTSIDE_WORKTREE")
        doc = read_json(args.map)
        problems = validate(doc)
        if problems:
            print(json.dumps({"status": "FAIL_CLOSED", "errors": problems}))
            return 2
        result, status = route_result(doc, args.route) if args.route is not None else ({"status": "STATIC_VALID_ONLY", "claim_ceiling": "NAVIGATION_ONLY"}, 0)
        if status:
            print(json.dumps(result, ensure_ascii=False))
            return status
        if args.online:
            if not args.expected_heads:
                print(json.dumps({"status": "HOLD_AFFECTED_WRITE", "reason": "EXPECTED_HEADS_MISSING"}))
                return 4
            expectation = validate_expected_snapshot(read_json(args.expected_heads))
            observed = {k: fetch_main(name) for k, (name, _) in EXPECTED_REPOS.items()}
            diffs = compare_heads(expectation, observed)
            if diffs:
                print(json.dumps({"status": "HOLD_AFFECTED_WRITE", "reason": "SOURCE_RECHECK", "errors": diffs}))
                return 5
            result["source_state"] = "HEAD_SHA_MATCHED_AT_READ_TIME_GITHUB_ONLY"
            result["observed_heads"] = observed
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError, urllib.error.URLError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "error_class": type(exc).__name__, "reason": str(exc)[:96]}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    sys.exit(main())
