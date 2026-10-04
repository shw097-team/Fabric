# -*- coding: utf-8 -*-
"""DoD-17 S20: read 執行中 category children (uia tree) — evidence of auto-execution."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x32112a
ru = du.window(handle=RADAR)

# read full tree (categories + children if expanded)
try:
    items = ru.descendants(control_type="TreeItem")
    print("tree items:", len(items))
    for it in items:
        t = (it.window_text() or "").strip()
        if t:
            print("  TI:", t[:45])
except Exception as e:
    print("tree err:", str(e)[:70])
