# -*- coding: utf-8 -*-
"""DoD-17 S1c: Enter to dismiss 開放體驗說明 (proven pattern), then verify radar window."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
dlg = d32.window(handle=0x3512aa)
dlg.wait("visible", timeout=5)
dlg.set_focus()
time.sleep(0.3)
dlg.send_keystrokes("{ENTER}")
print("sent Enter")
time.sleep(4)

# verify: dialog gone? radar window present?
u = ctypes.windll.user32
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    u.GetWindowTextW(hwnd, t, 256)
    if "策略雷達" in t.value:
        print("WIN:", hex(hwnd), "|", t.value[:50])
    return True
u.EnumWindows(cb, 0)
