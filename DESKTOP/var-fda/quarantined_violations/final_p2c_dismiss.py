# -*- coding: utf-8 -*-
"""FINAL P2c: dismiss 策略雷達開放體驗說明 dialog, then find radar window."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32
d32 = Desktop(backend="win32")

# find the 說明 dialog
dlg = d32.window(title_re="策略雷達開放體驗說明.*")
print("說明 dialog exists:", dlg.exists(timeout=2))
if dlg.exists(timeout=1):
    dlg.wait("visible", timeout=5)
    print("dialog:", dlg.window_text()[:40], hex(dlg.handle))
    # enumerate buttons
    for b in dlg.children(class_name="Button"):
        print("  btn:", repr(b.window_text()[:20]))
    # click first button (通常為 我知道了/確定)
    btns = dlg.children(class_name="Button")
    if btns:
        btns[0].click_input()
        print("clicked:", repr(btns[0].window_text()[:20]))
        time.sleep(3)

# find radar window now
rw = d32.window(title_re="策略雷達.*")
print("radar exists:", rw.exists(timeout=2))
if rw.exists(timeout=1):
    rw.wait("visible enabled", timeout=8)
    print("RADAR:", rw.window_text()[:50], hex(rw.handle))
