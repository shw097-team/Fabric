"""Produce R7_VALIDATOR_DIFF.patch: a clean unified diff of the changed PIPD source files.

Builds two parallel `src/pipd_ls_sp/` trees (old = pre-change snapshots, new = current product),
then runs `git diff --no-index` so the patch paths read `a/src/pipd_ls_sp/<file>` /
`b/src/pipd_ls_sp/<file>`. The PIPD tree itself is not a git repo, so this is the documented
`git diff --no-index` route the brief allows.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

R7 = Path(__file__).resolve().parent.parent
PRE = R7 / "RAW" / "pre_change"
PROD = Path("C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp")
FILES = ("validate.py", "pipeline.py", "cli.py")


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="r7-diff-"))
    try:
        old = tmp / "old" / "src" / "pipd_ls_sp"
        new = tmp / "new" / "src" / "pipd_ls_sp"
        old.mkdir(parents=True)
        new.mkdir(parents=True)
        for name in FILES:
            shutil.copy(PRE / name, old / name)
            shutil.copy(PROD / name, new / name)
        proc = subprocess.run(
            ["git", "diff", "--no-index", "--no-color",
             "--src-prefix=a/", "--dst-prefix=b/", "old", "new"],
            cwd=str(tmp), capture_output=True, text=True)
        patch = proc.stdout
        # Normalize the temp-tree prefixes so the patch reads a/src/pipd_ls_sp/<f>.
        patch = (patch.replace("a/old/", "a/").replace("b/new/", "b/")
                 .replace("a/new/", "a/").replace("b/old/", "b/"))
        out = R7 / "R7_VALIDATOR_DIFF.patch"
        out.write_text(patch, encoding="utf-8")
        print(f"git diff exit={proc.returncode} (1 == differences, expected)")
        print(f"wrote {out} ({len(patch)} chars)")
        if proc.stderr.strip():
            print("stderr:", proc.stderr.strip())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
