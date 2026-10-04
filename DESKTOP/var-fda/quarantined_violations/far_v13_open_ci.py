# -*- coding: utf-8 -*-
"""FAR v13: click_input on 開啟 toolbar button (community-validated), then dialog."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

du = Desktop(backend="uia")
editor = du.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

open_btn = [b for b in editor.descendants(control_type="Button")
            if b.window_text().strip() == "開啟" and b.is_visible()]
print("開啟 buttons:", len(open_btn))
if not open_btn:
    raise SystemExit(2)
open_btn[0].click_input()
print("click_input 開啟")
time.sleep(3)

d32 = Desktop(backend="win32")
dlg = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.window_text().strip() == "開啟":
            dlg = w
            break
    except Exception:
        continue
if dlg is None:
    print("no dialog")
    raise SystemExit(2)
print("開啟 dialog:", hex(dlg.handle))

# enumerate buttons
dlg_uia = Desktop(backend="uia").window(handle=dlg.handle)
for b in dlg_uia.descendants(control_type="Button"):
    t = b.window_text().strip()
    if t:
        print("  btn:", repr(t[:12]))
