# -*- coding: utf-8 -*-
"""FAR v6: try UIA Invoke (no mouse) on 新增 button."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

desktop = Desktop(backend="uia")
editor = desktop.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

add_btn = [b for b in editor.descendants(control_type="Button")
           if b.window_text().strip() == "新增" and b.is_visible()]
print("新增 buttons:", len(add_btn))
if not add_btn:
    raise SystemExit(2)
btn = add_btn[0]
# try invoke via wrapper
try:
    btn.invoke()
    print("invoke() ok")
except Exception as e:
    print("invoke err:", str(e)[:80])
    try:
        btn.click()  # uia click (not click_input) - may still work
        print("click() ok")
    except Exception as e2:
        print("click err:", str(e2)[:80])
time.sleep(2)

# check dialog
d32 = Desktop(backend="win32")
for w in d32.windows(class_name="#32770"):
    try:
        t = w.window_text()
        if t.strip() and "新增" in t:
            print("DIALOG:", repr(t[:40]))
    except Exception:
        pass
