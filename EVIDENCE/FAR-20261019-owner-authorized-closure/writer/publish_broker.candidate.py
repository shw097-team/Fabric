#!/usr/bin/env python
"""Trusted local publishing broker for round FAR-20261016-018-r7r11-residual-closure-and-handover.

Credential discipline (command-sheet section 3): the token file is READ BY THIS PROCESS ONLY.
The value is never printed, logged, echoed into a receipt, committed, or returned to the caller.
Only a non-reversible scope probe (an authenticated GET) and the resulting counts are surfaced.

Publication method: GitHub git-data API (blobs -> tree -> commit -> ref) so the whole packet lands as
ONE commit on a NEW branch off the current origin tip. Never a force update, never a write to main.
Every created path is checked against the round's single allowed prefix before any API call.
"""
import base64, hashlib, json, os, sys, urllib.request, urllib.error, datetime
from pathlib import Path

TOKEN_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
REPO = "shw097-team/Fabric"
ROUND = "FAR-20261016-018-r7r11-residual-closure-and-handover"
PREFIX = f"EVIDENCE/{ROUND}/"
BRANCH = "evidence/far-018-r7r11-residual-closure"
ROOT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
PUB = ROOT / "publish"
API = "https://api.github.com"


def parse_args(argv):
    """FAR018-BROKER-ARGUMENT-SAFETY: parse BEFORE any credential read or API call.

    The archived broker had no argument parser, so a `--help` probe took the
    publishing main path and actually published. This guard makes the broker fail
    closed on an unknown flag and treats `--help` as a pure probe, in BOTH cases
    without reaching the network. The documented invocation is NO ARGUMENTS (the
    payload is pinned by PUBLISH_MANIFEST.json); that invocation is unchanged.
    """
    import argparse
    ap = argparse.ArgumentParser(
        prog="publish_broker.py",
        description=("Trusted local publishing broker. The documented invocation takes "
                     "NO arguments: it publishes the payload pinned by PUBLISH_MANIFEST.json "
                     "as one commit on a new branch. --help is a probe and never publishes."))
    ap.add_argument("--dry-run", action="store_true",
                    help="validate the manifest and prefix check, then exit without any "
                         "credential read or network call")
    return ap.parse_args(argv)


def token():
    """Read the PAT. Never returns it to any caller that prints; used only inside _req."""
    t = TOKEN_FILE.read_text(encoding="utf-8", errors="replace").strip()
    for line in t.splitlines():
        line = line.strip()
        if line.startswith(("ghp_", "github_pat_", "gho_", "ghs_")):
            return line
    return t.split()[0]


def _req(method, path, body=None, raw=False):
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(API + path, data=data, method=method)
    r.add_header("Authorization", f"Bearer {token()}")
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("X-GitHub-Api-Version", "2022-11-28")
    r.add_header("User-Agent", "hgk-governed-publisher")
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            raw_b = resp.read()
            return resp.status, (raw_b if raw else json.loads(raw_b or b"{}"))
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:400]}


def main(argv=None):
    manifest_path = PUB / "PUBLISH_MANIFEST.json"
    files = json.loads(manifest_path.read_text(encoding="utf-8"))["files"]
    receipt = {"round": ROUND, "repo": REPO, "branch": BRANCH, "generated_utc":
               datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "token_value_exported": False, "force_update": False, "targets_main": False}

    # --- every target path must sit under the round's single evidence prefix (fail closed) --------
    # The manifest lists paths RELATIVE to the payload; the prefix is applied below, so the check is on
    # the FINAL path, plus a traversal/absolute-path guard on the relative part.
    targets = [PREFIX + f for f in files]
    bad = [t for t in targets if not t.startswith(PREFIX) or "/../" in t or t.startswith("/")]
    unsafe = [f for f in files if f.startswith(("/", "\\")) or ".." in f.split("/")]
    if bad or unsafe:
        print(json.dumps({"first_fail": "PREFIX_ESCAPE", "paths": (bad + unsafe)[:5]}))
        return 2

    # A `--dry-run` probe stops here: the manifest and prefix check are validated, but no
    # credential is read and no request is made. This is the safe way to probe the broker.
    if getattr(main, "_dry_run", False):
        print(json.dumps({"first_fail": None, "dry_run": True, "targets_checked": len(targets)}))
        return 0

    # --- scope probe: prove the credential only reaches the named repo, and record NOTHING secret --
    st, repo = _req("GET", f"/repos/{REPO}")
    if st != 200:
        print(json.dumps({"first_fail": "TOKEN_BROKER_UNAVAILABLE", "status": st,
                          "detail": str(repo)[:200]}))
        return 3
    st, perms = _req("GET", f"/repos/{REPO}")
    receipt["scope_probe"] = {"get_repo_status": st, "full_name": repo.get("full_name"),
                              "private": repo.get("private"), "default_branch": repo.get("default_branch")}

    st, ref = _req("GET", f"/repos/{REPO}/git/ref/heads/{repo['default_branch']}")
    if st != 200:
        print(json.dumps({"first_fail": "REPOCONTEXT_STALE", "status": st}))
        return 4
    base_sha = ref["object"]["sha"]
    receipt["base_branch"] = repo["default_branch"]
    receipt["base_sha"] = base_sha

    # --- create blobs (one per file) --------------------------------------------------------------
    tree = []
    file_rows = []
    for rel in files:
        src = PUB / "payload" / rel
        data = src.read_bytes()
        blob_sha = hashlib.sha256(data).hexdigest()
        st, blob = _req("POST", f"/repos/{REPO}/git/blobs",
                        {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        if st not in (200, 201):
            print(json.dumps({"first_fail": "BLOB_CREATE_FAILED", "path": rel, "status": st,
                              "detail": str(blob)[:200]}))
            return 5
        tree.append({"path": PREFIX + rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        file_rows.append({"path": PREFIX + rel, "bytes": len(data), "content_sha256": blob_sha,
                          "blob_sha": blob["sha"]})

    st, base_tree = _req("GET", f"/repos/{REPO}/git/trees/{base_sha}")
    if st != 200:
        print(json.dumps({"first_fail": "BASE_TREE_UNREADABLE", "status": st}))
        return 6
    st, t = _req("POST", f"/repos/{REPO}/git/trees",
                 {"base_tree": base_tree["sha"], "tree": tree})
    if st not in (200, 201):
        print(json.dumps({"first_fail": "TREE_CREATE_FAILED", "status": st, "detail": str(t)[:300]}))
        return 6
    receipt["base_tree_sha"] = base_tree["sha"]
    receipt["tree_sha"] = t["sha"]

    msg = (f"evidence-archive {ROUND}: candidate evidence packet\n\n"
           f"Contract {ROUND}; EIA-FABRIC-CNV-R7-R11-20261016 routes ARCHIVE-PR4-TO-11.\n"
           "candidate-only, not AO/Production. No archived helper is executed by this commit.\n"
           "Rollback: delete this branch (its commit is unreachable from main).")
    st, c = _req("POST", f"/repos/{REPO}/git/commits",
                 {"message": msg, "tree": t["sha"], "parents": [base_sha]})
    if st not in (200, 201):
        print(json.dumps({"first_fail": "COMMIT_CREATE_FAILED", "status": st, "detail": str(c)[:300]}))
        return 7
    receipt["commit_sha"] = c["sha"]

    st, r = _req("POST", f"/repos/{REPO}/git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": c["sha"]})
    if st not in (200, 201):
        print(json.dumps({"first_fail": "REF_CREATE_FAILED", "status": st, "detail": str(r)[:300]}))
        return 8
    receipt["ref_created"] = r.get("ref")

    st, pr = _req("POST", f"/repos/{REPO}/pulls",
                  {"title": f"[{ROUND}] candidate evidence archive (candidate-only, not AO/Production)",
                   "head": BRANCH, "base": repo["default_branch"], "draft": True,
                   "body": (f"Contract `{ROUND}`. Candidate evidence packet for the R7-R11 archive route.\n\n"
                            "- claim ceiling: `CANDIDATE_EVIDENCE_ARCHIVED_ONLY`\n"
                            "- every changed path is under `" + PREFIX + "`\n"
                            "- no archived `.py`/`.ps1` helper is executed\n"
                            "- not an acceptance of the validator, the checker isolation, the runtime or production\n"
                            "- rollback: delete the branch; `main` is untouched\n")})
    receipt["pr_number"] = pr.get("number") if isinstance(pr, dict) else None
    receipt["pr_url"] = pr.get("html_url") if isinstance(pr, dict) else None
    if st not in (200, 201):
        receipt["pr_error"] = {"status": st, "detail": str(pr)[:300]}

    # --- remote readback (the claim is bound to what the remote actually serves) -------------------
    st, rb = _req("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    receipt["readback"] = {"status": st, "ref": rb.get("ref"),
                           "sha": rb.get("object", {}).get("sha") if isinstance(rb, dict) else None}
    receipt["files"] = file_rows
    receipt["file_count"] = len(file_rows)
    (ROOT / "PUBLISH_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("base_sha", "commit_sha", "ref_created", "pr_number",
                                              "pr_url", "file_count", "readback")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    _ns = parse_args(sys.argv[1:])
    main._dry_run = _ns.dry_run
    sys.exit(main())
