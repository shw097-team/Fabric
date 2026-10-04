# -*- coding: utf-8 -*-
"""FAR v8: pywinauto uia .click() (non-input) on 新增; poll for dialog."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

desktop = Desktop(backend="uia")
editor = desktop.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

add_btn = [b for b in editor.descendants(control_type="Button")
           if b.window_text().strip() == "新增" and b.is_visible()]
print("新增:", len(add_btn))
if add_btn:
    try:
        add_btn[0].click()  # uia click via invoke pattern (no mouse move)
        print("uia click() ok")
    except Exception as e:
        print("click err:", str(e)[:80])
time.sleep(2)

d32 = Desktop(backend="win32")
for w in d32.windows(class_name="#32770"):
    try:
        t = w.window_text()
        if t.strip():
            print("DLG:", repr(t[:40]))
    except Exception:
        pass
