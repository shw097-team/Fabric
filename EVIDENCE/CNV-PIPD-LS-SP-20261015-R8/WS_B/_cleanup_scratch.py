"""Remove only WS_B-local scratch dirs. Scoped: refuses to touch anything outside WS_B."""
import os
import stat
import shutil
from pathlib import Path

WSB = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B").resolve()

def onerror(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


for name in ("_verify_apply", "_verify_rebased", "tmp_rebase"):
    t = (WSB / name).resolve()
    if WSB not in t.parents:
        raise SystemExit(f"refusing to delete outside WS_B: {t}")
    if t.exists():
        shutil.rmtree(t, onerror=onerror)
        print(f"removed {t}")
    else:
        print(f"absent  {t}")
