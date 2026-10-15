"""Find the icacls deny spec that denies WRITE but still permits READ for the checker."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

USER = os.environ["USERNAME"]


def fresh():
    d = Path(tempfile.mkdtemp(prefix="aclw-"))
    (d / "subject.txt").write_text("frozen-content", encoding="utf-8")
    (d / "sub").mkdir()
    (d / "sub" / "nested.txt").write_text("nested", encoding="utf-8")
    return d


def attempt(p: Path):
    out = {}
    try:
        out["read"] = len(p.read_bytes())
    except Exception as e:  # noqa: BLE001
        out["read"] = f"DENIED {type(e).__name__}"
    try:
        p.open("ab").write(b"x")
        out["append"] = "OK"
    except Exception as e:  # noqa: BLE001
        out["append"] = f"DENIED {type(e).__name__}"
    return out


def run_spec(spec: str):
    d = fresh()
    for f in sorted(d.rglob("*"), key=lambda x: len(str(x)), reverse=True):
        subprocess.run(["icacls", str(f), "/deny", f"{USER}:{spec}"],
                       capture_output=True, text=True)
    subprocess.run(["icacls", str(d), "/deny", f"{USER}:{spec}"], capture_output=True, text=True)
    res_file = attempt(d / "subject.txt")
    try:
        listing = len(os.listdir(d))
    except Exception as e:  # noqa: BLE001
        listing = f"DENIED {type(e).__name__}"
    try:
        (d / "new.tmp").write_text("x")
        new = "OK"
    except Exception as e:  # noqa: BLE001
        new = f"DENIED {type(e).__name__}"
    subprocess.run(["icacls", str(d), "/remove:d", USER], capture_output=True, text=True)
    for f in sorted(d.rglob("*"), key=lambda x: len(str(x))):
        subprocess.run(["icacls", str(f), "/remove:d", USER], capture_output=True, text=True)
    shutil.rmtree(d, ignore_errors=True)
    return {"spec": spec, "subject": res_file, "dir_listing": listing, "new_file": new}


for spec in ["(W)", "(WD,AD)", "(WD,AD,WEA,WA)", "(WD,AD,DC)", "(M)"]:
    print(run_spec(spec))
