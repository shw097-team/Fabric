# -*- coding: utf-8 -*-
"""FN03 final: locate Afx 新增 button in editor (uia read-only) + FN01 re-run."""
import json
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
from pywinauto import Desktop
import xq_native_adapter as na

results = {}
d32 = Desktop(backend="win32")

# FN01 re-run (10x)
ok = 0
for _ in range(10):
    if na.find_main_window():
        ok += 1
    time.sleep(0.03)
results["FN01_locate_main_win32"] = {"pass": ok, "runs": 10, "wrong_action": 0, "silent_wrong_action": 0}
print("FN01:", ok, "/10")

# FN03: locate 新增 in editor (uia read-only)
du = Desktop(backend="uia")
editor = du.window(title_re=".*XScript 編輯器.*")
if editor.exists(timeout=3):
    new_btn = [b for b in editor.descendants(control_type="Button")
               if b.window_text().strip() == "新增" and b.is_visible()]
    print("FN03 新增 buttons:", len(new_btn))
    results["FN03_editor_new_button_locate"] = {
        "pass": 1 if new_btn else 0, "runs": 1,
        "wrong_action": 0, "silent_wrong_action": 0,
        "note": "locate-only PASS; UIA Invoke on this Afx button = known deadlock (R-FDA-011); "
                "canonical invoke path = pywinauto Win32 native (pending FN03-challenge)",
    }
else:
    results["FN03_editor_new_button_locate"] = {"pass": 0, "runs": 1, "note": "editor not visible"}
    print("FN03: editor not visible")

# FN02: editor window locate via win32 (10x)
ed_ok = 0
for _ in range(10):
    eds = [w for w in d32.windows() if "XScript 編輯器" in w.window_text()]
    if eds:
        ed_ok += 1
    time.sleep(0.03)
results["FN02_editor_locate_win32"] = {"pass": ed_ok, "runs": 10, "wrong_action": 0, "silent_wrong_action": 0}
print("FN02:", ed_ok, "/10")

json.dump(results, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved")
