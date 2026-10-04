# -*- coding: utf-8 -*-
"""FAR v12: Ctrl+O (send_keys), dialog: 警示 tab -> select FDA_PAPER_ALERT -> confirm."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
editor = d32.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

# bring editor to front briefly for hotkey (pywinauto manages this)
editor.set_focus()
time.sleep(0.5)
editor.send_keystrokes("^o")
print("sent ctrl+o")
time.sleep(3)

# find 開啟 dialog
dlg = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.window_text().strip() == "開啟":
            dlg = w
            break
    except Exception:
        continue
if dlg is None:
    print("no 開啟 dialog")
    raise SystemExit(2)
print("開啟 dialog:", hex(dlg.handle))

# uia on dialog: find 警示 tab button + tree
du = Desktop(backend="uia")
dlg_uia = du.window(handle=dlg.handle)
for b in dlg_uia.descendants(control_type="Button"):
    t = b.window_text().strip()
    if t:
        print("  btn:", repr(t[:12]))
