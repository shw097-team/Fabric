"""Confirm R8_0_REBASED.patch (a) matches the r8-wt working tree diff vs main and
(b) applies cleanly to a fresh main checkout, yielding WS_B/post byte-for-byte."""
import hashlib
import shutil
import subprocess
from pathlib import Path

WSB = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B")
WT = Path("C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt")


def norm(text):
    out = []
    for ln in text.splitlines():
        if ln.startswith("index ") or ln.startswith("diff --git"):
            continue
        if ln.startswith("--- "):
            ln = "--- a"
        if ln.startswith("+++ "):
            ln = "+++ b"
        out.append(ln.rstrip("\r"))
    return "\n".join(out)


# (a) live worktree diff vs main HEAD
r = subprocess.run(["git", "-C", str(WT), "diff", "--no-color", "--",
                    "src/pipd_ls_sp/validate.py", "src/pipd_ls_sp/pipeline.py",
                    "src/pipd_ls_sp/cli.py"], capture_output=True, text=True)
live = r.stdout
rebased = WSB.joinpath("R8_0_REBASED.patch").read_text(encoding="utf-8")
print("worktree live diff == rebased patch:", norm(live) == norm(rebased))
print("sha norm(live)   :", hashlib.sha256(norm(live).encode()).hexdigest()[:32])
print("sha norm(rebased):", hashlib.sha256(norm(rebased).encode()).hexdigest()[:32])

# (b) apply rebased patch to a clean main checkout
scratch = WSB / "_verify_rebased"
if scratch.exists():
    shutil.rmtree(scratch)
subprocess.run(["git", "-C", str(WT), "worktree", "list"], capture_output=True)
subprocess.run(["git", "clone", "-q", "--no-local", "--shared", str(WT), str(scratch)],
               capture_output=True, text=True)
# detach to main commit already (worktree HEAD is dba4b19); reset any worktree-local edits
subprocess.run(["git", "-C", str(scratch), "checkout", "-q", "--detach", "dba4b19"],
               capture_output=True, text=True)
chk = subprocess.run(["git", "-C", str(scratch), "apply", "--check",
                      str(WSB / "R8_0_REBASED.patch")], capture_output=True, text=True)
print("apply --check on fresh main exit:", chk.returncode, chk.stderr.strip())
app = subprocess.run(["git", "-C", str(scratch), "apply",
                      str(WSB / "R8_0_REBASED.patch")], capture_output=True, text=True)
print("apply exit:", app.returncode, app.stderr.strip())


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


for f in ("validate.py", "pipeline.py", "cli.py"):
    got = sha16(scratch / "src/pipd_ls_sp" / f)
    want = sha16(WSB / "post" / f)
    print(f"{f}: applied={got} post={want} match={got == want}")
