# -*- coding: utf-8 -*-
"""FINAL P2e: Enter to dismiss 說明 dialog (community pattern), verify radar opens."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
dlg = d32.window(handle=0x100d96)
dlg.wait("visible", timeout=5)
dlg.set_focus()
time.sleep(0.3)
dlg.send_keystrokes("{ENTER}")
print("sent Enter")
time.sleep(4)

# check: dialog gone? radar window present?
for w in d32.windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if "策略雷達" in t:
                print("WIN:", hex(w.handle), "|", t[:50])
    except Exception:
        pass
