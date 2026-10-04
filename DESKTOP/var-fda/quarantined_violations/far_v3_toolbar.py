# -*- coding: utf-8 -*-
"""FAR v3: enumerate editor toolbar buttons (find 新增/新增腳本 entry), click it."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

desktop = Desktop(backend="uia")
editor = desktop.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

# enumerate toolbar buttons
toolbar = None
for ctrl in editor.descendants(control_type="ToolBar"):
    tb = ctrl
    print("toolbar:", tb.window_text()[:30])
    for btn in tb.descendants(control_type="Button"):
        t = btn.window_text().strip()
        if t:
            print("  btn:", repr(t[:20]))
    break

# try 新增 button via uia
add_btn = [b for b in editor.descendants(control_type="Button")
           if b.window_text().strip() == "新增"]
print("新增 buttons:", len(add_btn))
if add_btn:
    add_btn[0].click_input()
    print("clicked 新增")
    time.sleep(2)
    # check dialog
    d32 = Desktop(backend="win32")
    for w in d32.windows(class_name="#32770"):
        try:
            t = w.window_text()
            if "新增腳本" in t:
                print("DIALOG:", t)
        except Exception:
            pass
