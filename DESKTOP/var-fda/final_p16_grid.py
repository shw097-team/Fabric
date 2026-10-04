# -*- coding: utf-8 -*-
"""FINAL P16: expand 自訂 in radar left tree; read strategy grid (17001/17002)."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
RADAR = 0x110d96
du = Desktop(backend="uia")
ru = du.window(handle=RADAR)

# find the left category tree (first Tree) — expand 自訂
trees = ru.descendants(control_type="Tree")
print("trees:", len(trees))
for idx, tv in enumerate(trees):
    for item in tv.descendants(control_type="TreeItem"):
        t = item.window_text().strip()
        if t == "自訂":
            print(f"tree[{idx}] 自訂 found; expand...")
            try:
                item.expand()
                time.sleep(1.2)
            except Exception as e:
                print("  expand err:", str(e)[:50])
            children = [c.window_text().strip() for c in item.descendants(control_type="TreeItem")
                        if c.window_text().strip()]
            print("  自訂 children:", children[:10])
            break

# read strategy grid 17001 (win32 MFCGridCtrl) via uia — list rows
try:
    grid = ru.child_window(control_id=17001, class_name="MFCGridCtrl")
    print("grid17001 exists:", grid.exists(timeout=2))
    if grid.exists(timeout=1):
        for row in grid.descendants(control_type="DataItem"):
            try:
                txt = row.window_text()
                if txt.strip():
                    print("  ROW:", repr(txt[:60]))
            except Exception:
                pass
except Exception as e:
    print("grid err:", str(e)[:80])
