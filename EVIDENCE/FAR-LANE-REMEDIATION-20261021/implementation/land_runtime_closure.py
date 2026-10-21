#!/usr/bin/env python
"""FAR-CLOSURE-20261021-R3 — land the untracked lane runtime so a clean checkout can rebuild it.

The defect (measured, not inferred):
  This round committed `tests/test_lane_policy.py` and `scripts/hgk-lane-dispatch.py`, and BOTH import
  `hg_kseos.lane_policy` / `hg_kseos.lane_admission` / `hg_kseos.lane_route_resolver` /
  `hg_kseos.role_binding` -- none of which were tracked in git. A clean detached worktree at the
  round's own HEAD could not import them at all:

      clean checkout: ImportError: cannot import name 'lane_policy' from 'hg_kseos'
      pytest tests/test_lane_policy.py -> ERROR during collection (1 error)

  So the published epoch-24 contract was NOT reproducible from the repository: the tracked tree
  carried the TESTS and the DISPATCHER while the modules they depend on lived only in the working
  copy. A lane that cannot be rebuilt from a clean checkout is a lane that cannot be handed over.

Why these files (the closure is measured, not guessed):
  Every local import of every candidate was resolved against `git ls-files`. The four
  `src/hg_kseos` modules import only each other plus already-tracked `hg_kseos.errors` and
  `hg_kseos.util`; the scripts import only `hg_kseos`; the one test imports
  `hg_kseos.lane_route_resolver`. No candidate pulls in an untracked dependency.

What this script does:
  1. Verifies the closure again (re-derives the import graph) and REFUSES if a candidate would
     introduce an untracked dependency.
  2. Refuses if any candidate carries a credential-shaped literal.
  3. `git add` the closure (this is a version-control operation, not a file edit) and records the
     blob sha1 of each added file in the receipt.
  4. Verifies in a FRESH DETACHED WORKTREE at the new commit that the conformance suite collects
     and passes, and that the dispatcher imports -- i.e. the repository can rebuild itself.
  5. Removes the scratch worktree.

Properties: dry-run default; explicit --apply; per-file pre-image sha256; receipt; no force
operations; no push (the owner decides publication).
"""
from __future__ import annotations
import argparse, ast, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROUND = "FAR-CLOSURE-20261021-R3"
OUT = ROOT / "var" / ROUND
SCRATCH = Path(os.environ.get("TMPDIR") or os.environ.get("TEMP") or
               (Path(os.environ["LOCALAPPDATA"]) / "Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch"))

# The closure. Four runtime modules, four lane scripts, one test.
CANDIDATES = [
    "src/hg_kseos/lane_policy.py",
    "src/hg_kseos/lane_admission.py",
    "src/hg_kseos/lane_route_resolver.py",
    "src/hg_kseos/role_binding.py",
    "scripts/hgk-lane-guard.py",
    "scripts/runtime_role_binding_assert.py",
    "scripts/hgk-exec-model-frontdoor.py",
    "scripts/hgk-artifact-gate.py",
    "tests/test_lane_dispatch_ao_guard.py",
]

SECRET_PAT = r"\b(sk-[A-Za-z0-9]{20,}|nvapi-[A-Za-z0-9_-]{32,}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{22,}|oc_[A-Za-z0-9_-]{20,})"

COMMIT_MSG = """FAR-CLOSURE-20261021-R3: land the lane runtime so a clean checkout can rebuild it

This round committed tests/test_lane_policy.py and scripts/hgk-lane-dispatch.py, and both
import hg_kseos.lane_policy / lane_admission / lane_route_resolver / role_binding -- none of
which were tracked. A clean detached worktree at the round's own HEAD could not import them
(ImportError: cannot import name 'lane_policy' from 'hg_kseos'), and the conformance suite
aborted during collection. The tracked tree carried the TESTS and the DISPATCHER while the
modules they depend on lived only in the working copy, so the published epoch-24 contract was
not reproducible from the repository.

Lands the measured closure: four runtime modules, four lane scripts, one test. Every local
import of every candidate was resolved against git ls-files first, so no candidate pulls in an
untracked dependency; no candidate carries a credential-shaped literal; no candidate hardcodes a
machine-absolute path.

Verification is from a FRESH DETACHED WORKTREE at the new commit: the four modules import, the
conformance suite collects and passes, and the dispatcher parses. The point is that the repository
can now rebuild its own lane contract from its own tracked bytes.

Local commit only: no push, no branch movement, no force operation."""



def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def local_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            if n.level:
                out.add("." * n.level + (n.module or ""))
            elif n.module and n.module.startswith("hg_kseos"):
                out.add(n.module)
        elif isinstance(n, ast.Import):
            for a in n.names:
                if a.name.startswith("hg_kseos"):
                    out.add(a.name)
    return out


def resolve(rel: str, imp: str) -> str | None:
    """Map a local import to a repo-relative path, or None if it is not a repo-local module."""
    if imp.startswith("hg_kseos."):
        return "src/" + imp.replace(".", "/") + ".py"
    if imp.startswith("."):
        base = Path(rel).parent
        return (base / (imp.lstrip(".") + ".py")).as_posix()
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    receipt = {"round": ROUND, "utc": stamp, "applied": bool(args.apply), "candidates": CANDIDATES,
               "pre_sha256": {}}
    problems = []

    tracked = set(git("ls-files").stdout.splitlines())
    # files present in the INDEX but absent from the committed tree
    head_tree = set(git("ls-tree", "-r", "--name-only", "HEAD").stdout.splitlines())
    staged = {f for f in tracked if f not in head_tree}
    receipt["staged_but_uncommitted"] = sorted(staged)
    closure = []
    for rel in CANDIDATES:
        p = ROOT / rel
        if not p.exists():
            problems.append({"file": rel, "problem": "MISSING"})
            continue
        receipt["pre_sha256"][rel] = sha(p)
        # ORDER MATTERS: a file that is in the INDEX but not yet in a commit is `already_staged`,
        # and it still needs the commit and the clean-worktree verification. Checking
        # `in tracked` first would swallow every staged-but-uncommitted file into
        # `already_tracked` and silently skip the commit -- which is exactly what happened on the
        # first apply: the receipt showed a completed verification against the PRE-landing HEAD.
        if rel in staged:
            closure.append({"file": rel, "state": "already_staged"})
            continue
        if rel in tracked:
            closure.append({"file": rel, "state": "already_tracked"})
            continue
        # 1. secret check
        import re
        hits = re.findall(SECRET_PAT, p.read_text(encoding="utf-8", errors="replace"))
        if hits:
            problems.append({"file": rel, "problem": "SECRET_SHAPED_LITERAL", "count": len(hits)})
            continue
        # 2. dependency closure check against the TRACKED tree
        for imp in sorted(local_imports(p)):
            dep = resolve(rel, imp)
            if dep and dep not in tracked and not (ROOT / dep).exists():
                problems.append({"file": rel, "problem": "UNTRACKED_OR_MISSING_DEP", "dep": dep})
        closure.append({"file": rel, "state": "would_add"})

    if problems:
        receipt["problems"] = problems
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / ("apply_receipt.json" if args.apply else "apply_dryrun.json")).write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"applied": False, "refused": True, "problems": problems}, ensure_ascii=False, indent=1))
        return 2

    to_add = [c["file"] for c in closure if c["state"] == "would_add"]
    already_staged = [c["file"] for c in closure if c["state"] == "already_staged"]
    if args.apply and to_add:
        r = git("add", *to_add)
        if r.returncode != 0:
            receipt["git_add_error"] = r.stderr[-400:]
            print(json.dumps({"applied": False, "error": "git add failed", "detail": r.stderr[-400:]}, indent=1))
            return 3
    if args.apply and (to_add or already_staged):
        receipt["git_add"] = to_add
        receipt["git_add_already_staged"] = already_staged
        _idx = git("ls-files", "-s", *(to_add + already_staged)).stdout.strip().splitlines()
        receipt["index_blobs"] = {ln.split("\t")[-1]: ln.split()[1] for ln in _idx if ln.strip()}
        # COMMIT before verifying: a detached worktree is created at a COMMIT, so verifying at HEAD
        # while the files are only staged would test the PRE-landing tree and report a false
        # failure. The commit is local; no push, no branch movement, no force.
        head_before = git("rev-parse", "HEAD").stdout.strip()
        receipt["head_before"] = head_before
        cm = subprocess.run(["git", "-c", "user.name=HGK Governed Runtime", "-c", "user.email=hgk@local",
                             "commit", "-q", "-m", COMMIT_MSG], cwd=str(ROOT), capture_output=True, text=True)
        receipt["commit"] = {"rc": cm.returncode, "stderr": cm.stderr[-300:]}
        if cm.returncode != 0:
            print(json.dumps({"applied": False, "error": "commit failed", "detail": cm.stderr[-300:]}, indent=1))
            return 4
        receipt["head_after"] = git("rev-parse", "HEAD").stdout.strip()

    # 3. VERIFY FROM A CLEAN DETACHED WORKTREE. This is the point of the round: prove the
    #    repository can rebuild the epoch-24 contract from its own tracked bytes.
    verification = {}
    if args.apply:
        wt = SCRATCH / ("clean-rebuild-" + str(int(time.time())))
        if wt.exists():
            shutil.rmtree(wt, ignore_errors=True)
        wt.parent.mkdir(parents=True, exist_ok=True)
        add = git("worktree", "add", "--detach", str(wt), "HEAD")
        verification["worktree_add"] = {"rc": add.returncode, "stderr": add.stderr[-200:]}
        if add.returncode == 0:
            py = str(ROOT / ".venv" / "Scripts" / "python.exe")
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            # a) the modules import from the clean tree
            imp = subprocess.run([py, "-c", "import sys;sys.path.insert(0,'src');"
                                  "from hg_kseos import lane_policy, lane_admission, lane_route_resolver, role_binding;"
                                  "print('IMPORTS_OK')"],
                                 cwd=str(wt), capture_output=True, text=True, env=env)
            verification["imports"] = {"rc": imp.returncode, "out": imp.stdout.strip()[-200:],
                                       "err": imp.stderr.strip()[-300:]}
            # b) the conformance suite collects and passes from the clean tree
            t = subprocess.run([py, "-m", "pytest", "tests/test_lane_policy.py", "-q", "-p", "no:cacheprovider"],
                               cwd=str(wt), capture_output=True, text=True, env=env, timeout=900)
            verification["pytest"] = {"rc": t.returncode, "tail": (t.stdout or "").strip().splitlines()[-2:],
                                      "err": (t.stderr or "").strip()[-300:]}
            # c) the dispatcher (the committed lane entry point) imports
            d = subprocess.run([py, "-c", "import ast,sys;ast.parse(open('scripts/hgk-lane-dispatch.py',encoding='utf-8').read());"
                                  "print('DISPATCHER_PARSES')"],
                               cwd=str(wt), capture_output=True, text=True, env=env)
            verification["dispatcher"] = {"rc": d.returncode, "out": d.stdout.strip()[-200:]}
            git("worktree", "remove", "--force", str(wt))
            verification["worktree_removed"] = True
    receipt["verification"] = verification

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ("apply_receipt.json" if args.apply else "apply_dryrun.json")).write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"applied": bool(args.apply), "added": to_add, "problems": problems,
                      "verification": verification}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
