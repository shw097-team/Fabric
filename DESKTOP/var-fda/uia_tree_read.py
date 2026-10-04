# -*- coding: utf-8 -*-
"""uia READ-ONLY: full radar tree walk — find strategy nodes under 自訂."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
ru = du.window(handle=0x80fc8)

try:
    items = ru.descendants(control_type="TreeItem")
    print("tree items:", len(items))
    for it in items:
        t = (it.window_text() or "").strip()
        if t:
            print("  TI:", t[:45])
except Exception as e:
    print("err:", str(e)[:80])
