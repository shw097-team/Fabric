#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabric governance-mirror admission validator — fail-closed reader for
``INTEGRATION/MANIFEST.json``'s ``subject_admissions[]`` (EC-R26-013 / R26-09).

Why this file exists
--------------------
PR #49 merged the r26 FHS W0 mirror into this repository, but a merged file is not
an admission: the mirror stayed ``candidate / not policy loaded`` because nothing in
``INTEGRATION/MANIFEST.json`` named it, and nothing re-derived its digest from the
bytes actually present here.  This validator is the reader that makes the admission
checkable instead of asserted:

* every ``subject_admissions[]`` entry must be bound to a file that exists inside
  this worktree, whose ``sha256`` and ``bytes`` are recomputed **from that file**;
* an entry may never claim more effect than the navigation surface
  (``INTEGRATION/FHS/repository-map.json``, ``FHS-NAV/v2``) actually holds;
* an admission state and a claim ceiling may never name a tier the effect
  permission denies;
* with ``--baseline``, every pre-existing manifest entry must survive byte-for-byte
  (additions only) — an admission may not be paid for by rewriting an older record.

Refusal codes (exit 2, fail-closed)
-----------------------------------
MANIFEST_UNREADABLE, MANIFEST_UNPARSEABLE, MANIFEST_DUPLICATE_KEY,
MANIFEST_NOT_OBJECT, MANIFEST_SCHEMA_UNSUPPORTED, ADMISSION_SET_MISSING,
ADMISSION_ENTRY_NOT_OBJECT, ADMISSION_FIELDS_MISSING, ADMISSION_FIELD_UNKNOWN,
ADMISSION_FIELD_TYPE, ADMISSION_ID_DUPLICATE, MIRROR_PATH_MISSING,
MIRROR_PATH_OUTSIDE_REPO, MIRROR_DIGEST_MISMATCH, MIRROR_SIZE_MISMATCH,
EFFECT_PERMISSION_UNKNOWN, EFFECT_PERMISSION_ESCALATION,
ADMISSION_STATE_UNKNOWN, ADMISSION_STATE_PERMISSION_MISMATCH,
CLAIM_CEILING_ESCALATION, SOURCE_COMMIT_INVALID, SOURCE_REPOSITORY_UNKNOWN,
ADMITTED_AT_INVALID, ADMITTED_BY_EMPTY, NAV_MAP_UNREADABLE,
ADDITIVE_ONLY_VIOLATION.

Test seam, not a bypass
-----------------------
``--candidate-entry <file>`` validates one candidate entry (a JSON object) in place
of the entries recorded in the manifest.  It is used by the negative tests to feed a
tampered admission to the same code path.  It is validation-only: it never writes,
never admits, and every check still runs — a tampered candidate still exits non-zero
with a named code.  There is no flag that turns a check off.

Stdlib only.  Read-only: this script never writes to the repository.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_ID = "FABRIC-INTEGRATION-MIRROR/3"
NAV_MAP_REL = Path("INTEGRATION") / "FHS" / "repository-map.json"
MANIFEST_REL = Path("INTEGRATION") / "MANIFEST.json"

REQUIRED_FIELDS = (
    "admission_id",
    "subject_id",
    "mirror_path",
    "bytes",
    "sha256",
    "source_repository",
    "source_commit",
    "effect_permission",
    "admission_state",
    "admitted_by",
    "admitted_at",
    "claim_ceiling",
)
# Recorded context that is allowed beside the required fields.  Anything else is
# refused: an admission record is a contract, not a notebook.
OPTIONAL_FIELDS = ("mirror_dir", "digest_verified_from", "not_claims")

ADMISSION_STATES = ("ADMITTED_FOR_NAVIGATION_ONLY", "ADMITTED_FOR_CONSUMPTION")
# States that assert consumption (i.e. the mirror is policy the surface serves)
# need more than navigation permission to be honest.
CONSUMPTION_STATES = ("ADMITTED_FOR_CONSUMPTION",)
CLAIM_CEILINGS = ("MIRROR_ADMITTED_FOR_NAVIGATION_WITH_BOUND_DIGEST_ONLY",)
SOURCE_REPOSITORIES = ("shw097-team/SBL", "shw097-team/Fabric", "shw097-team/HG-KSEOS")

# Effect ordering, low to high.  An admission may not outrank the surface that
# consumes it.  "NONE" is what FHS-NAV/v2 declares today.
EFFECT_RANK = {"NONE": 0, "READ_ONLY": 1, "NAVIGATION_ONLY": 1, "WRITE": 2, "ADMIN": 3}

SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
MAX_BYTES = 262144


class Refusal(Exception):
    """A named, typed refusal.  Carries the code the log will show."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code)
        self.code = code
        self.detail = detail


def _no_duplicate_keys(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise Refusal("MANIFEST_DUPLICATE_KEY", key)
        seen[key] = value
    return seen


def read_json(path: Path):
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise Refusal("MANIFEST_UNREADABLE", f"{path}: {exc}") from None
    if len(raw) > MAX_BYTES:
        raise Refusal("MANIFEST_UNREADABLE", f"{path}: larger than {MAX_BYTES} bytes")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
    except Refusal:
        raise
    except (ValueError, UnicodeError) as exc:
        raise Refusal("MANIFEST_UNPARSEABLE", f"{path}: {exc}") from None


def sha256_of(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def _parse_iso(value: str) -> dt.datetime:
    try:
        stamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError):
        raise Refusal("ADMITTED_AT_INVALID", repr(value)) from None
    if stamp.tzinfo is None:
        raise Refusal("ADMITTED_AT_INVALID", "no timezone offset")
    return stamp


def check_entry(entry, repo_root: Path, nav_effect: str, *, verify_digest: bool = True) -> list[str]:
    """Return the list of refusal codes for one admission entry (empty == admitted)."""
    errors: list[str] = []
    if type(entry) is not dict:
        return ["ADMISSION_ENTRY_NOT_OBJECT"]

    missing = [f for f in REQUIRED_FIELDS if f not in entry]
    if missing:
        errors.append("ADMISSION_FIELDS_MISSING")
    unknown = [f for f in entry if f not in REQUIRED_FIELDS + OPTIONAL_FIELDS]
    if unknown:
        errors.append("ADMISSION_FIELD_UNKNOWN")

    for field in ("admission_id", "subject_id", "mirror_path", "sha256",
                  "source_repository", "source_commit", "effect_permission",
                  "admission_state", "admitted_by", "admitted_at", "claim_ceiling"):
        if field in entry and type(entry[field]) is not str:
            errors.append("ADMISSION_FIELD_TYPE")
            break
    if "bytes" in entry and (type(entry["bytes"]) is not int or entry["bytes"] <= 0):
        errors.append("ADMISSION_FIELD_TYPE")

    # -- identity of the source ------------------------------------------------
    repo = entry.get("source_repository")
    if type(repo) is str and repo not in SOURCE_REPOSITORIES:
        errors.append("SOURCE_REPOSITORY_UNKNOWN")
    commit = entry.get("source_commit")
    if type(commit) is str and not COMMIT_RE.fullmatch(commit):
        errors.append("SOURCE_COMMIT_INVALID")

    # -- effect permission may not outrank the consuming surface ---------------
    effect = entry.get("effect_permission")
    if type(effect) is not str or effect not in EFFECT_RANK:
        errors.append("EFFECT_PERMISSION_UNKNOWN")
    elif nav_effect not in EFFECT_RANK:
        errors.append("EFFECT_PERMISSION_UNKNOWN")
    elif EFFECT_RANK[effect] > EFFECT_RANK[nav_effect]:
        errors.append("EFFECT_PERMISSION_ESCALATION")
    elif nav_effect == "NONE" and effect != "NONE":
        errors.append("EFFECT_PERMISSION_ESCALATION")

    # -- admission state and claim ceiling must agree with the permission ------
    state = entry.get("admission_state")
    if type(state) is not str or state not in ADMISSION_STATES:
        errors.append("ADMISSION_STATE_UNKNOWN")
    elif state in CONSUMPTION_STATES and effect != "WRITE":
        # Consumption means the surface serves this as loaded policy; claiming it
        # while holding NONE (or READ) is the escalation EC-R26-013 is about.
        errors.append("ADMISSION_STATE_PERMISSION_MISMATCH")

    ceiling = entry.get("claim_ceiling")
    if type(ceiling) is str:
        upper = ceiling.upper()
        if ceiling not in CLAIM_CEILINGS:
            errors.append("CLAIM_CEILING_ESCALATION")
        elif any(word in upper for word in ("ACCEPTED", "RELEASED", "PRODUCTION", "LIVE")):
            errors.append("CLAIM_CEILING_ESCALATION")

    admitted_by = entry.get("admitted_by")
    if type(admitted_by) is str and not admitted_by.strip():
        errors.append("ADMITTED_BY_EMPTY")
    admitted_at = entry.get("admitted_at")
    if type(admitted_at) is str:
        try:
            _parse_iso(admitted_at)
        except Refusal:
            errors.append("ADMITTED_AT_INVALID")

    # -- the digest is re-derived from the mirrored file, never trusted --------
    if verify_digest and type(entry.get("mirror_path")) is str:
        root = repo_root.resolve()
        target = (root / entry["mirror_path"]).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            errors.append("MIRROR_PATH_OUTSIDE_REPO")
        else:
            if not target.is_file():
                errors.append("MIRROR_PATH_MISSING")
            else:
                measured_sha, measured_bytes = sha256_of(target)
                if type(entry.get("sha256")) is str and entry["sha256"] != measured_sha:
                    errors.append("MIRROR_DIGEST_MISMATCH")
                if type(entry.get("bytes")) is int and entry["bytes"] != measured_bytes:
                    errors.append("MIRROR_SIZE_MISMATCH")
    return errors


def check_additive_only(manifest: dict, baseline: dict) -> list[str]:
    """Every baseline key must survive unchanged; additions are the only change."""
    errors: list[str] = []
    for key, value in baseline.items():
        if key not in manifest:
            errors.append("ADDITIVE_ONLY_VIOLATION")
            break
        if manifest[key] != value:
            errors.append("ADDITIVE_ONLY_VIOLATION")
            break
    return errors


def validate(manifest, repo_root: Path, nav_map, *, baseline=None, candidate_entry=None) -> dict:
    """Run every static check and return a result dict (``status`` PASS or REFUSED)."""
    errors: list[str] = []
    if type(manifest) is not dict:
        return {"status": "REFUSED", "errors": ["MANIFEST_NOT_OBJECT"]}
    if manifest.get("schema") != SCHEMA_ID:
        errors.append("MANIFEST_SCHEMA_UNSUPPORTED")
    if type(nav_map) is not dict or type(nav_map.get("effect_permission")) is not str:
        errors.append("NAV_MAP_UNREADABLE")
        nav_effect = "NONE"
    else:
        nav_effect = nav_map["effect_permission"]

    entries = [candidate_entry] if candidate_entry is not None else manifest.get("subject_admissions")
    if type(entries) is not list or not entries:
        errors.append("ADMISSION_SET_MISSING")
        entries = []

    seen_ids = set()
    checked = []
    for entry in entries:
        entry_errors = check_entry(entry, repo_root, nav_effect)
        errors.extend(entry_errors)
        if type(entry) is dict:
            admission_id = entry.get("admission_id")
            if type(admission_id) is str:
                if admission_id in seen_ids:
                    errors.append("ADMISSION_ID_DUPLICATE")
                seen_ids.add(admission_id)

    if baseline is not None:
        errors.extend(check_additive_only(manifest, baseline))

    # de-duplicate while keeping first-seen order: a log should read like a list
    # of distinct reasons, not like a counter.
    ordered = list(dict.fromkeys(errors))
    return {
        "status": "REFUSED" if ordered else "PASS",
        "code": ordered[0] if ordered else "OK",
        "errors": ordered,
        "schema": manifest.get("schema"),
        "nav_effect_permission": nav_effect,
        "admissions_checked": len(entries),
        "entries": [
            {
                "admission_id": e.get("admission_id"),
                "mirror_path": e.get("mirror_path"),
                "sha256": e.get("sha256"),
                "bytes": e.get("bytes"),
                "admission_state": e.get("admission_state"),
                "effect_permission": e.get("effect_permission"),
            }
            for e in entries
            if type(e) is dict
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Fabric governance-mirror admission validator (fail-closed).")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--manifest", default=None, help="defaults to <repo-root>/INTEGRATION/MANIFEST.json")
    parser.add_argument("--nav-map", default=None, help="defaults to <repo-root>/INTEGRATION/FHS/repository-map.json")
    parser.add_argument("--baseline", default=None, help="pre-change manifest JSON; enforces additions only")
    parser.add_argument("--candidate-entry", default=None, help="validate one candidate entry (JSON object) instead of the recorded set")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root)
    manifest_path = Path(args.manifest) if args.manifest else repo_root / MANIFEST_REL
    nav_path = Path(args.nav_map) if args.nav_map else repo_root / NAV_MAP_REL

    try:
        manifest = read_json(manifest_path)
        nav_map = read_json(nav_path)
        baseline = read_json(Path(args.baseline)) if args.baseline else None
        candidate = read_json(Path(args.candidate_entry)) if args.candidate_entry else None
    except Refusal as refusal:
        print(json.dumps({"status": "REFUSED", "code": refusal.code, "errors": [refusal.code],
                          "detail": refusal.detail}, ensure_ascii=False, sort_keys=True))
        return 2

    result = validate(manifest, repo_root, nav_map, baseline=baseline, candidate_entry=candidate)
    result["manifest"] = str(manifest_path)
    result["candidate_entry_supplied"] = candidate is not None
    result["baseline_compared"] = bool(args.baseline)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
