# -*- coding: utf-8 -*-
"""DoD-17 S11: read radar window geometry — 自訂 tree item rect + grid rect (uia read-only)."""
import ctypes
import ctypes.wintypes as wt
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x80fc8
ru = du.window(handle=RADAR)

# radar window rect
r32 = d32.window(handle=RADAR)
rect = r32.rectangle()
print("radar rect:", rect)

# 自訂 tree item rect
try:
    items = ru.descendants(control_type="TreeItem")
    custom = next((i for i in items if (i.window_text() or "").strip() == "自訂"), None)
    if custom:
        c_rect = custom.rectangle()
        print("自訂 rect:", c_rect)
        # 全部 rect (top of list) + 執行中 rect
        for name in ("全部", "執行中"):
            it = next((i for i in items if (i.window_text() or "").strip() == name), None)
            if it:
                print(f"{name} rect:", it.rectangle())
except Exception as e:
    print("tree rect err:", str(e)[:80])

# grid 17001 rect
try:
    g = ru.child_window(control_id=17001, class_name="MFCGridCtrl")
    if g.exists(timeout=2):
        print("grid 17001 rect:", g.rectangle())
except Exception as e:
    print("grid rect err:", str(e)[:60])
