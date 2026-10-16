"""Publication packet builder for ChangeSet R8-0 under mission CNV-PIPD-LS-SP-20261015.

Reuses the proven R7 publication machinery (publish_r7.py) with R8 constants and one improvement:
every path excluded from the packet is recorded with a reason in the manifest, so nothing is dropped
silently.

Publishes a NEW evidence prefix (EVIDENCE/CNV-PIPD-LS-SP-20261015-R8/) on a NEW branch, so the already
merged R6R7 archive (main b8ff8104, 581 blobs) and the R7 packet (04a1e118, 306 blobs) stay byte-stable.

Usage:
  python publish_r8.py prepare   # create/refresh the worktree branch, stage the packet, commit (no remote write)
  python publish_r8.py m2        # trusted scope+secret scan of the staged commit (writes M2 result)
  python publish_r8.py status    # worktree/branch state
  python publish_r8.py push      # push with an inline credential helper (never on argv)
  python publish_r8.py readback  # read the remote ref/tree back and compare with the local commit
  python publish_r8.py pr        # open a DRAFT pull request
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("C:/Projects/Agent_Workspace/Fabric")
HANDOVER = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8")
R6_HANDOVER = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015")
PKT = "EVIDENCE/CNV-PIPD-LS-SP-20261015-R8"
BRANCH = "evidence/cnv-pipd-ls-sp-20261015-r8"
BASE = "origin/main"
TOKEN_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
WT = Path("C:/Projects/wt-cnv-r8")

# existing single-file includes (transferable artifacts the packet must carry verbatim)
EXTRA_INCLUDE = [
    (R6_HANDOVER / "R6R7_POST_COMMIT_READBACK.json", "PREVIOUS_ROUNDS/R6R7_POST_COMMIT_READBACK.json"),
    (R6_HANDOVER / "R6R7_M2_SCAN_AT_FINAL_HEAD.json", "PREVIOUS_ROUNDS/R6R7_M2_SCAN_AT_FINAL_HEAD.json"),
    (R6_HANDOVER / "M3_MAINTAINER_APPROVAL.json", "PREVIOUS_ROUNDS/M3_MAINTAINER_APPROVAL.json"),
    (R6_HANDOVER / "R6R7_MERGE_AND_CLOSURE.json", "PREVIOUS_ROUNDS/R6R7_MERGE_AND_CLOSURE.json"),
    (R6_HANDOVER / "CONVERGENCE_RETURN_PACK_R6R7.json", "PREVIOUS_ROUNDS/CONVERGENCE_RETURN_PACK_R6R7.json"),
    (R6_HANDOVER / "m2_scan.py", "m2_scan.py"),
]

# directory names anywhere under the handover root that are lane scratch, not evidence
EXCLUDE_DIR_PREFIXES = ("pipd-clone", "pipd_wt_", "scratch-clone-", "tmp_verify", "rebase_scratch",
                        "r8-wt", "clone", "logs")
EXCLUDE_DIR_EXACT = {"__pycache__", ".git"}


def _skip_scratch(dirpath, names):
    return [n for n in names if n in EXCLUDE_DIR_EXACT or n.startswith(EXCLUDE_DIR_PREFIXES)]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str, cwd: Path = WT) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def ensure_worktree() -> int:
    if WT.exists():
        return 0
    r = git("worktree", "add", str(WT), "-b", BRANCH, BASE, cwd=REPO)
    print("WORKTREE_ADD", r.returncode, r.stdout[-300:], r.stderr[-300:])
    if r.returncode != 0:
        r = git("worktree", "add", str(WT), BRANCH, cwd=REPO)
        print("WORKTREE_ADD_EXISTING_BRANCH", r.returncode, r.stderr[-200:])
    return r.returncode


def excluded_paths() -> list[dict]:
    """Every path under HANDOVER that this packet deliberately does not carry, with its reason."""
    out = []
    for p in sorted(HANDOVER.rglob("*")):
        rel = p.relative_to(HANDOVER).as_posix()
        if any(part in EXCLUDE_DIR_EXACT or part.startswith(EXCLUDE_DIR_PREFIXES) for part in rel.split("/")):
            reason = ("__pycache__" if "__pycache__" in rel else
                      "lane scratch / log directory excluded from publication (reason recorded, not silently dropped)")
            out.append({"path": rel, "kind": "dir" if p.is_dir() else "file",
                        "bytes": p.stat().st_size if p.is_file() else None, "reason": reason})
    return out


def write_packet_manifest(dst: Path, excluded: list[dict]) -> tuple[int, int]:
    files = [f for f in sorted(dst.rglob("*")) if f.is_file()]
    rels = [str(f.relative_to(WT)).replace("\\", "/") for f in files]
    ign = subprocess.run(["git", "check-ignore", "--stdin", "-z"], cwd=str(WT),
                         input=b"\0".join(r.encode() for r in rels) + b"\0", capture_output=True)
    ignored = {x.decode() for x in ign.stdout.split(b"\0") if x}
    tracked = {r for r in rels if r not in ignored}
    manifest, local_only = [], []
    for f, rel in zip(files, rels):
        row = {"path": rel, "bytes": f.stat().st_size, "sha256": sha256_file(f), "tracked": rel in tracked}
        manifest.append(row)
        if not row["tracked"]:
            gi = subprocess.run(["git", "check-ignore", "-v", rel], cwd=str(WT),
                                capture_output=True, text=True).stdout.strip()
            local_only.append({"path": rel, "bytes": row["bytes"], "sha256": row["sha256"],
                               "reason": "ignored by the repository's own rules; never added to git",
                               "check_ignore": gi.split("\t")[0]})
    tracked_inventory = sorted(r["path"] for r in manifest if r["tracked"])
    doc = {"schema": "CNV-PIPD-LS-SP-20261015-R8/PACKET-MANIFEST/1",
           "publish_claim": ("the DELIVERED set is tracked_inventory (%d paths); the local inventory is %d paths, "
                             "of which %d are excluded by the repository's own ignore rules and are NOT published; "
                             "%d further paths under the round root are excluded as lane scratch and are listed here"
                             % (len(tracked_inventory), len(manifest), len(local_only), len(excluded))),
           "files": manifest, "file_count": len(manifest), "tracked_file_count": len(tracked_inventory),
           "local_inventory_count": len(manifest), "tracked_inventory": tracked_inventory,
           "local_only_excluded": local_only, "excluded_scratch": excluded, "branch": BRANCH,
           "base_origin_main_expected": "b8ff81043e47e4b652522be34444bf52fcf4d65e",
           "note": ("the merged R6R7 archive under EVIDENCE/CNV-PIPD-LS-SP-20261015/ and the R7 packet under "
                    "EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/ are NOT part of this packet and are not rewritten")}
    (dst / "PACKET_MANIFEST.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    (dst / ".gitattributes").write_text("# Published evidence packet: store bytes EXACTLY as produced.\n* -text\n",
                                        encoding="utf-8")
    return len(manifest), len(tracked_inventory)


def prepare() -> int:
    if ensure_worktree() != 0:
        return 2
    git("config", "core.autocrlf", "false")
    dst = WT / PKT
    dst.mkdir(parents=True, exist_ok=True)
    missing = []
    # the whole round root (minus scratch), then the transferable extras
    if HANDOVER.exists():
        shutil.copytree(HANDOVER, dst, dirs_exist_ok=True, ignore=_skip_scratch)
        # copytree would have copied a nested packet dir if one existed; keep the destination clean
        for stray in (dst / "RS8_TMP",):
            if stray.exists():
                shutil.rmtree(stray, ignore_errors=True)
    else:
        missing.append(str(HANDOVER))
    for src, rel in EXTRA_INCLUDE:
        if not src.exists():
            missing.append(str(src))
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    excluded = excluded_paths()
    local_n, tracked_n = write_packet_manifest(dst, excluded)
    print("PACKET_MISSING", len(missing))
    for m in missing:
        print("  missing:", m)
    print("MANIFEST local=%d tracked=%d excluded_scratch=%d" % (local_n, tracked_n, len(excluded)))
    git("add", "-A", PKT)
    staged = git("diff", "--cached", "--name-only").stdout.strip().splitlines()
    print("STAGED_DELTA", len(staged))
    if not staged:
        print("NOTHING_TO_COMMIT")
        return 0
    git("commit", "-m",
        "evidence(CNV-PIPD-LS-SP-20261015-R8): skill-slim regression+apply, R8-0 rebase on main, checker-isolation evidence, EIA closure\n\n"
        "ChangeSet R8-0-SKILL-SLIM-REGRESSION-AND-EIA-CLOSURE, admitted as HGK project CNV-R8-SKILL-SLIM-EIA-CLOSURE.\n"
        "Contents: the skill-slim regression harness and its per-candidate verdicts, the guarded apply record,\n"
        "the R8-0 rebase of the validator hardening onto main with the 18-mutation re-measurement, the\n"
        "checker write-root isolation evidence-of-absence plus the proven deny-ACE mechanism, the\n"
        "finding-by-finding EIA-R6-01..09 reconciliation, and the guarded-subject byte-exactness proof.\n\n"
        "Published under a NEW prefix so the merged R6 archive and the R7 packet stay byte-stable.\n"
        "Candidate-only, claim ceiling LOCAL: no acceptance, no approval, no Gate PASS, no production effect.\n"
        "Archived scripts are evidence copies and must not be executed.\n")
    print("HEAD", git("rev-parse", "HEAD").stdout.strip())
    return 0


def m2() -> int:
    rev = git("rev-parse", "HEAD").stdout.strip()
    out = HANDOVER / "M2_TRUSTED_SCOPE_SECRETS_R8.json"
    r = subprocess.run([sys.executable, str(R6_HANDOVER / "m2_scan.py"), "--rev", rev,
                        "--worktree", str(WT), "--out", str(out), "--prefix", PKT + "/"],
                       capture_output=True, text=True)
    print(r.stdout.strip()[-600:], r.stderr.strip()[-300:])
    return r.returncode


def status() -> int:
    print("WT exists:", WT.exists(), "| branch:", git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip())
    print("HEAD:", git("rev-parse", "HEAD").stdout.strip())
    print("porcelain:", git("status", "--porcelain").stdout.strip()[:400])
    return 0


def push() -> int:
    tk = TOKEN_FILE.read_text(encoding="utf-8").strip()
    helper = ("!f() { test \"$1\" = get && printf 'username=%s\\npassword=%s\\n' x \"$GITHUB_PACKET_TOKEN\"; }; f")
    env = dict(os.environ, GITHUB_PACKET_TOKEN=tk)
    r = subprocess.run(["git", "-c", "credential.helper=", "-c", f"credential.helper={helper}",
                        "push", "origin", f"HEAD:refs/heads/{BRANCH}"],
                       cwd=str(WT), capture_output=True, text=True, env=env)
    print("PUSH_EXIT", r.returncode)
    print(r.stdout[-800:])
    print(r.stderr[-800:])
    return r.returncode


def readback() -> int:
    tk = TOKEN_FILE.read_text(encoding="utf-8").strip()
    from urllib.request import Request, urlopen

    def api(path: str):
        req = Request("https://api.github.com" + path,
                      headers={"Authorization": "Bearer " + tk, "Accept": "application/vnd.github+json",
                               "User-Agent": "hgk-r8"})
        with urlopen(req, timeout=60) as r:
            return json.loads(r.read())

    local = git("rev-parse", "HEAD").stdout.strip()
    br = api(f"/repos/shw097-team/Fabric/branches/{BRANCH}")
    remote = br["commit"]["sha"]
    tree = api(f"/repos/shw097-team/Fabric/git/trees/{remote}?recursive=1")
    rpaths = {e["path"]: e["sha"] for e in tree["tree"] if e["type"] == "blob" and e["path"].startswith(PKT + "/")}
    bad = []
    for rel, sha in rpaths.items():
        lp = WT / rel
        if not lp.exists():
            bad.append((rel, "local absent"))
            continue
        b = lp.read_bytes()
        if hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest() != sha:
            bad.append((rel, "blob mismatch"))
    print(json.dumps({"local_head": local, "remote_head": remote, "match": local == remote,
                      "remote_blobs": len(rpaths), "blob_mismatches": len(bad), "sample": bad[:3]}, indent=1))
    return 0 if local == remote and not bad else 1


def pr() -> int:
    tk = TOKEN_FILE.read_text(encoding="utf-8").strip()
    body = ("Candidate-only evidence packet for the R8-0 ChangeSet of mission CNV-PIPD-LS-SP-20261015.\n\n"
            "- Scope: `EVIDENCE/CNV-PIPD-LS-SP-20261015-R8/**` only. The merged R6 archive "
            "(`EVIDENCE/CNV-PIPD-LS-SP-20261015/**`) and the R7 packet (`…-R7/**`) are untouched.\n"
            "- Admitted as HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE` (4 WorkOrders).\n"
            "- Contents: skill-slim regression harness + per-candidate verdicts + guarded apply record; R8-0 rebase "
            "of the validator hardening onto `main` with all 18 mutations re-measured; checker write-root isolation "
            "evidence (absence + proven deny-ACE mechanism + proposal only); EIA-R6-01..09 reconciliation; "
            "guarded-subject byte-exactness proof against the merged packet.\n"
            "- Claim ceiling LOCAL / candidate-only: no acceptance, no approval, no Gate PASS, no production effect; "
            "archived scripts are evidence copies and must not be executed.\n"
            "- Rollback: drop the branch or `git revert` the merge commit; never force-push main.")
    payload = {"title": "evidence(CNV-PIPD-LS-SP-20261015-R8): skill-slim regression+apply, R8-0 rebase on main, checker isolation, EIA closure",
               "head": BRANCH, "base": "main", "draft": True, "body": body}
    with tempfile.NamedTemporaryFile("w", suffix=".curlrc", delete=False, encoding="utf-8") as fh:
        fh.write('header = "Authorization: Bearer ***"\nheader = "Accept: application/vnd.github+json"\n'
                 'header = "X-GitHub-Api-Version: 2022-11-28"\n')
        cfg = fh.name
    pj = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    pj.write(json.dumps(payload))
    pj.close()
    try:
        r = subprocess.run(["curl", "-s", "-K", cfg, "-X", "POST", "-d", "@" + pj.name,
                            "https://api.github.com/repos/shw097-team/Fabric/pulls"],
                           capture_output=True, text=True)
    finally:
        for f in (cfg, pj.name):
            try:
                os.unlink(f)
            except OSError:
                pass
    try:
        d = json.loads(r.stdout)
        print(json.dumps({"number": d.get("number"), "url": d.get("html_url"), "draft": d.get("draft"),
                          "error": d.get("errors") or d.get("message")}, ensure_ascii=False))
    except Exception:
        print(r.stdout[:600])
    return 0


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    raise SystemExit({"prepare": prepare, "m2": m2, "status": status, "push": push,
                      "readback": readback, "pr": pr}[action]())
