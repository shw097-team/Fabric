# -*- coding: utf-8 -*-
"""Open XScript editor via uia menu: 策略(D) -> XScript 編輯器 (community click pattern)."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

du = Desktop(backend="uia")
main = du.window(class_name="DAQXQLITEMainWnd")

# 1. 策略(D)
items = [i for i in main.descendants(control_type="MenuItem") if i.window_text() == "策略(D)" and i.is_visible()]
print("策略(D):", len(items))
if not items:
    raise SystemExit(2)
items[0].click_input()
time.sleep(1.5)

# 2. XScript 編輯器 in submenu
items2 = [i for i in main.descendants(control_type="MenuItem") if "XScript 編輯器" in i.window_text() and i.is_visible()]
print("XScript 編輯器:", len(items2))
if items2:
    items2[0].click_input()
    print("clicked editor")
    time.sleep(6)
    # verify
    d32 = Desktop(backend="win32")
    eds = [w for w in d32.windows() if "XScript 編輯器" in w.window_text()]
    print("editor visible:", len(eds))
