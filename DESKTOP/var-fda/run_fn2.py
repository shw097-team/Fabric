# -*- coding: utf-8 -*-
"""FN01 + FN03 simplified: win32 main locate (10x) + uia read-only 新增 button locate."""
import ctypes
import ctypes.wintypes as wt
import json
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
from pywinauto import Desktop
import xq_native_adapter as na

results = {}
d32 = Desktop(backend="win32")

# FN01: locate main window via win32 — 10 runs
ok = 0
for _ in range(10):
    if na.find_main_window():
        ok += 1
    time.sleep(0.03)
results["FN01_locate_main_win32"] = {"pass": ok, "runs": 10, "wrong_action": 0, "silent_wrong_action": 0}
print("FN01:", ok, "/10")

# FN03: locate Afx 新增 button — uia read-only (no invoke = no deadlock)
du = Desktop(backend="uia")
try:
    editor = du.window(title_re=".*XScript 編輯器.*")
    if editor.exists(timeout=3):
        new_btn = [b for b in editor.descendants(control_type="Button")
                   if b.window_text().strip() == "新增" and b.is_visible()]
        results["FN03_editor_new_button_locate"] = {
            "pass": 1 if new_btn else 0, "runs": 1,
            "wrong_action": 0, "silent_wrong_action": 0,
            "note": "locate-only; UIA Invoke on Afx 新增 = known deadlock (R-FDA-011), invoke via win32 native pending",
        }
        print("FN03 新增 button located:", len(new_btn))
    else:
        results["FN03_editor_new_button_locate"] = {"pass": 0, "runs": 1, "note": "editor not open"}
        print("FN03: editor not open")
except Exception as e:
    results["FN03_editor_new_button_locate"] = {"pass": 0, "runs": 1, "note": f"uia err {str(e)[:80]}"}
    print("FN03 err:", str(e)[:80])

json.dump(results, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved")
