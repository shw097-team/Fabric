# -*- coding: utf-8 -*-
"""Read 觸發商品 tree (33035) + 執行紀錄 grid (17002) via uia — read-only, no expand/click."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
ru = du.window(handle=0x80fc8)

# 1. 觸發商品 tree (33035)
try:
    t = ru.child_window(control_id=33035, class_name="SysTreeView32")
    print("33035 exists:", t.exists(timeout=2))
    if t.exists(timeout=1):
        items = t.descendants(control_type="TreeItem")
        texts = [(i.window_text() or "").strip() for i in items if (i.window_text() or "").strip()]
        print("33035 nodes:", texts[:15])
except Exception as e:
    print("33035 err:", str(e)[:70])

# 2. 執行紀錄 grid (17002)
try:
    g = ru.child_window(control_id=17002, class_name="MFCGridCtrl")
    print("17002 exists:", g.exists(timeout=2))
    if g.exists(timeout=1):
        txts = [el.window_text().strip() for el in g.descendants() if el.window_text().strip()]
        print("17002 texts:", txts[:15])
except Exception as e:
    print("17002 err:", str(e)[:70])

# 3. 內容 tab 的 grid (17001) — 策略清單
try:
    g1 = ru.child_window(control_id=17001, class_name="MFCGridCtrl")
    print("17001 exists:", g1.exists(timeout=2))
except Exception as e:
    print("17001 err:", str(e)[:70])
