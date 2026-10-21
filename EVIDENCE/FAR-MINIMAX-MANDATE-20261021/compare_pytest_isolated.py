#!/usr/bin/env python
"""Compare the pytest failure set with and without this round's config change -- ISOLATED.

WHY A WORKTREE
  The first version of this comparison restored the pre-round bytes IN THE WORKING TREE and
  re-ran the suite. That is unsafe: a parallel lane dispatch or a research subagent reading the
  same files sees a half-restored tree. It also left the tree in a mixed state when the
  process was killed (the `finally` block never ran) -- an actual incident this round.

  This version instead:
    1. creates a DETACHED git worktree at HEAD (the pre-round committed state),
    2. copies the CURRENT (post-change) config bytes over it,
    3. runs the suite there  -> AFTER,
    4. restores the pre-round bytes in that worktree,
    5. runs the suite there  -> BEFORE,
    6. removes the worktree.

  The main working tree is NEVER modified by this script.

WHAT IT CANNOT DO
  The worktree runs the suite against COMMITTED code plus the three changed config files. It
  does not include the round's untracked outputs, which is correct: they are evidence, not
  code. Tests that depend on untracked files will fail in BOTH runs and therefore cancel out
  of the difference.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HG = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
OUT = HG / "var" / "FAR-MINIMAX-MANDATE-20261021"
FILES = [
    "config/lane-route-slots.candidate.json",
    "config/lane-routing-registry.yaml",
    "config/model-lane-assignment.json",
]
BACKUP = {
    "config/lane-route-slots.candidate.json": "backup-pool.json",
    "config/lane-routing-registry.yaml": "backup-registry.yaml",
    "config/model-lane-assignment.json": "backup-assignment.json",
}


def git(*args, cwd=HG) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout


def run_suite(cwd: Path) -> tuple[set[str], str]:
    env = dict(os.environ, PYTHONPATH="src", PYTHONDONTWRITEBYTECODE="1",
               TMPDIR=os.environ.get("LOCALAPPDATA", "") + r"\Temp",
               TEMP=os.environ.get("LOCALAPPDATA", "") + r"\Temp",
               TMP=os.environ.get("LOCALAPPDATA", "") + r"\Temp")
    py = HG / ".venv" / "Scripts" / "python.exe"
    r = subprocess.run([str(py), "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider"],
                       cwd=cwd, capture_output=True, text=True, env=env)
    fails = set()
    for ln in r.stdout.splitlines():
        ln = ln.strip()
        if ln.startswith("FAILED "):
            name = ln[7:].split(" - ")[0].strip()
            if name and name != "FAILED":
                fails.add(name)
    tail = [l for l in r.stdout.splitlines() if (" passed" in l or " failed" in l)]
    return fails, (tail[-1] if tail else r.stdout[-300:])


def main() -> None:
    wt = Path(tempfile.mkdtemp(prefix="hgk-cmp-"))
    # a worktree must be created OUTSIDE the repo root's own tree
    shutil.rmtree(wt, ignore_errors=True)
    wt = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / "HG-KSEOS" / "cmp-wt-20261021"
    shutil.rmtree(wt, ignore_errors=True)
    wt.parent.mkdir(parents=True, exist_ok=True)

    print("creating worktree ...", flush=True)
    git("worktree", "add", "--detach", str(wt), "HEAD")
    try:
        # AFTER: current bytes over the committed tree
        for f in FILES:
            shutil.copy2(HG / f, wt / f)
        after_fails, after_tail = run_suite(wt)
        print(f"AFTER  : {after_tail}", flush=True)

        # BEFORE: the pre-round bytes
        for f, bname in BACKUP.items():
            shutil.copy2(OUT / bname, wt / f)
        before_fails, before_tail = run_suite(wt)
        print(f"BEFORE : {before_tail}", flush=True)
    finally:
        git("worktree", "remove", "--force", str(wt))
        git("worktree", "prune")

    new = sorted(after_fails - before_fails)
    gone = sorted(before_fails - after_fails)
    both = sorted(before_fails & after_fails)
    result = {
        "method": "isolated detached worktree; the main working tree was never modified",
        "before_tail": before_tail, "after_tail": after_tail,
        "before_count": len(before_fails), "after_count": len(after_fails),
        "new_failures": new, "fixed": gone, "unchanged": both,
    }
    (OUT / "pytest_diff.json").write_text(json.dumps(result, ensure_ascii=False, indent=2),
                                          encoding="utf-8")
    print("\n=== NEW failures introduced by this round (%d) ===" % len(new))
    for f in new:
        print("  ", f)
    print("\n=== unchanged pre-existing failures (%d) ===" % len(both))
    for f in both:
        print("  ", f)
    print("\n=== fixed by this round (%d) ===" % len(gone))
    for f in gone:
        print("  ", f)


if __name__ == "__main__":
    main()
