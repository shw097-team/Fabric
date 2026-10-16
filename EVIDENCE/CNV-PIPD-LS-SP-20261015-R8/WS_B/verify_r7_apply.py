"""Independent check: does R7_VALIDATOR_DIFF.patch reproduce the R7 target files when applied to
the R7 pre_change originals? Confirms R8_0_DERIVED_FROM_R7.patch is the true delta (same as R7's
own archive) and that WS_B/post is the R7 target semantics re-expressed on main."""
import hashlib
import shutil
import subprocess
from pathlib import Path

R7 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7")
WSB = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B")
SCRATCH = WSB / "_verify_apply"
TARGET = R7 / "R7_CHECKER_ATTEMPT3/a3_driver/product_changed/src/pipd_ls_sp"


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


if SCRATCH.exists():
    shutil.rmtree(SCRATCH)
(SCRATCH / "src/pipd_ls_sp").mkdir(parents=True)
for f in ("validate.py", "pipeline.py", "cli.py"):
    shutil.copy2(R7 / "RAW/pre_change" / f, SCRATCH / "src/pipd_ls_sp" / f)


def run(*args):
    return subprocess.run(args, cwd=str(SCRATCH), capture_output=True, text=True)


run("git", "init", "-q")
run("git", "add", "-A")
run("git", "-c", "user.email=a@b", "-c", "user.name=x", "commit", "-qm", "base")
chk = run("git", "apply", "--check", str(R7 / "R7_VALIDATOR_DIFF.patch"))
print("git apply --check exit:", chk.returncode, chk.stderr.strip())
app = run("git", "apply", str(R7 / "R7_VALIDATOR_DIFF.patch"))
print("git apply exit:", app.returncode, app.stderr.strip())
for f in ("validate.py", "pipeline.py", "cli.py"):
    print(f"{f}: applied={sha16(SCRATCH / 'src/pipd_ls_sp' / f)} target={sha16(TARGET / f)}")
