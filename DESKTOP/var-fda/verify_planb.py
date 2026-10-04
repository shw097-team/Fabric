# -*- coding: utf-8 -*-
"""Post-sync verification (Plan B): G1 resolved + all refs consistent."""
from pathlib import Path

VFD = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")
FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
SKF = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\fda-desktop-automation")
SKH = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution")

ok = True
def chk(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    ok &= bool(cond)

print("=== PLAN B SYNC VERIFICATION ===")
# 1. G1: fda_script_guard.py exists at all 3 canonical locations
chk("var/fda/fda_script_guard.py", (VFD / "fda_script_guard.py").exists())
chk("fda skill refs/fda_script_guard.py", (SKF / "references" / "fda_script_guard.py").exists())
chk("hgk skill refs/fda_script_guard.py", (SKH / "references" / "fda_script_guard.py").exists())
chk("OLD name gone from fda skill refs", not (SKF / "references" / "FDA_PREFLIGHT_GUARD.py").exists())
# 2. content identical (canonical)
import hashlib
h1 = hashlib.sha256((VFD / "fda_script_guard.py").read_bytes()).hexdigest()
h2 = hashlib.sha256((SKF / "references" / "fda_script_guard.py").read_bytes()).hexdigest()
h3 = hashlib.sha256((SKH / "references" / "fda_script_guard.py").read_bytes()).hexdigest()
chk("3 copies identical sha", h1 == h2 == h3, f"({h1[:10]})")
# 3. docs reference new name (with formerly note ok)
ag = (FDA / "AGENTS.md").read_text(encoding="utf-8")
chk("AGENTS references fda_script_guard", "fda_script_guard" in ag)
sk = (SKF / "SKILL.md").read_text(encoding="utf-8")
chk("fda skill §2.1 new name", "fda_script_guard.py <script.py>" in sk or "fda_script_guard.py" in sk)
# 4. run the guard itself (functional test)
import subprocess, sys
PY = r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe"
r = subprocess.run([PY, str(VFD / "fda_script_guard.py"), str(FDA / "xq_native_adapter.py")], capture_output=True, text=True, timeout=60)
chk("guard functional (clean script exit 0)", r.returncode == 0, f"(exit {r.returncode}: {r.stdout.strip()[:50]})")
print("=" * 40)
print(f"VERIFICATION: {'ALL PASS' if ok else 'BLOCKED'}")
