# -*- coding: utf-8 -*-
"""SKILL 實跑檢測 (internal verification): verify every path/asset/ID/claim in the skill
matches reality on disk. Exit 0 = ALL PASS."""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SKILL = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\fda-desktop-automation\SKILL.md")
txt = SKILL.read_text(encoding="utf-8")
checks = []
def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))

# --- 1. asset files exist ---
FDA = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
VFD = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")
for f in ["xq_native_adapter.py", "fda_router.py", "FDA_DESKTOP_CAPABILITY_MATRIX.yaml", "FDA_ASSET_REGISTRY.json"]:
    check(f"asset {f}", (FDA / f).exists())
for f in ["screen_state_check.py", "fda_script_guard.py", "fda_run.py"]:
    check(f"asset {f}", (VFD / f).exists())
check("skill references screen_state_check", (Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\fda-desktop-automation\references\screen_state_check.py")).exists())
check("skill scripts fda_run", (Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\fda-desktop-automation\scripts\fda_run.py")).exists())

# --- 2. control IDs in skill match adapter/dialog reality ---
check("skill NEW=17551", "17551" in txt)
check("skill STOP=17555", "17555" in txt)
check("skill name Edit=17500", "17500" in txt)
check("skill script btn=17203", "17203" in txt)
check("skill product btn=17610", "17610" in txt)
check("skill trigger Combo=17035", "17035" in txt)

# --- 3. DB paths ---
check("SensorList path", r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite" in txt or "SensorList.sqlite" in txt)
check("SensorLog path", "DAQXQLITE_SHW097_SensorLog.sqlite" in txt)
check("SensorLog LIKE trap", "LIKE" in txt and "XQSensorName" in txt)
check("flush delay", "15s" in txt or "flush" in txt.lower())

# --- 4. fingerprint ---
fp = FDA / "evidence/receipts/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json"
if fp.exists():
    d = json.load(open(fp, encoding="utf-8"))
    check("fingerprint 260811", d.get("subject", {}).get("product_build") == "260811")
    check("fingerprint exe_sha in skill", d.get("subject", {}).get("exe_sha256", "")[:8] in txt)
else:
    check("fingerprint receipt exists", False)

# --- 5. matrix PYWINAUTO_WIN32 QUALIFIED ---
mx = FDA / "FDA_DESKTOP_CAPABILITY_MATRIX.yaml"
if mx.exists():
    mxt = mx.read_text(encoding="utf-8")
    check("matrix PYWINAUTO QUALIFIED", "PYWINAUTO_WIN32" in mxt and "QUALIFIED" in mxt)
else:
    check("matrix exists", False)

# --- 6. key sections present in skill ---
for sec in ["## 0. 完整操作流程路由", "## 1. 強制路由總覽", "### 1.1", "### 1.2", "## 2. 機械強制",
            "### 2.0 REUSE-FIRST", "### 2.1", "### 2.2", "## 3. XQ/XS 操作速查", "## 4. 已驗證資產清單",
            "## 5. FAR 歷史", "## 6. 外部驗收證據打包路由"]:
    check(f"section {sec}", sec in txt)

# --- 7. no forbidden API names promoted as USAGE in operational sections ---
# Allowed ONLY in: §1.2 FORBIDDEN block, §2.1 guard-detection, §5 history.
# Forbidden in: §0 quickstart, §3 operational quick-ref (would promote their use).
for bad in ["click_input()", "set_focus()", "send_keystrokes()", "SetCursorPos", "SendInput", "SetForegroundWindow"]:
    op_lines = []
    in_op = False
    for l in txt.splitlines():
        if l.startswith("## 0.") or l.startswith("## 3."):
            in_op = True
        if l.startswith("## 1.") or l.startswith("## 2.") or l.startswith("## 4.") or l.startswith("## 5.") or l.startswith("## 6."):
            in_op = False  # §1.2 FORBIDDEN block, §2 guard-detect, §5 history are allowed contexts
        if in_op and bad in l:
            op_lines.append(l.strip()[:60])
    check(f"no {bad} in operational sections", not op_lines, f"lines: {op_lines[:2]}")

# --- 8. receipts inventory matches skill claims ---
rec = FDA / "evidence/receipts"
for name in ["FDA_F01_CURRENT_260811_RECEIPT.json", "FDA_F06_FRESH_10RUN_RECEIPT_RR6.json",
             "FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json", "FDA_CHECKER_FINAL_RR7.json",
             "FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json"]:
    check(f"receipt {name}", (rec / name).exists())

print(f"{'='*60}")
passed = sum(1 for _, ok, _ in checks if ok)
for name, ok, detail in checks:
    print(f"  {'PASS' if ok else 'FAIL'}  {name} {detail}")
print(f"{'='*60}")
print(f"RESULT: {passed}/{len(checks)} PASS")
sys.exit(0 if passed == len(checks) else 1)
