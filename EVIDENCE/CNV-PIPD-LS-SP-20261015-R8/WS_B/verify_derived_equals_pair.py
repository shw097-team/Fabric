"""Confirm WS_B/R8_0_DERIVED_FROM_R7.patch is the real diff RAW/pre_change -> R7 post-change,
and that (normalized) it equals the archived R7_VALIDATOR_DIFF.patch."""
import hashlib
import subprocess
from pathlib import Path

R7 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7")
WSB = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B")
TARGET = R7 / "R7_CHECKER_ATTEMPT3/a3_driver/product_changed/src/pipd_ls_sp"


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


def sha(t):
    return hashlib.sha256(t.encode()).hexdigest()


# real diff pre_change -> target, per file, combined
chunks = []
for f in ("cli.py", "pipeline.py", "validate.py"):
    r = subprocess.run(
        ["git", "diff", "--no-index", "--no-color", "--",
         str(R7 / "RAW/pre_change" / f), str(TARGET / f)],
        capture_output=True, text=True)
    chunks.append(r.stdout)
combined = "".join(chunks)

derived = WSB.joinpath("R8_0_DERIVED_FROM_R7.patch").read_text(encoding="utf-8")
archived = (R7 / "R7_VALIDATOR_DIFF.patch").read_text(encoding="utf-8")

print("sha norm(real pair diff) :", sha(norm(combined))[:32])
print("sha norm(WSB derived)    :", sha(norm(derived))[:32])
print("sha norm(R7 archived)    :", sha(norm(archived))[:32])
print("derived == real pair diff:", norm(derived) == norm(combined))
