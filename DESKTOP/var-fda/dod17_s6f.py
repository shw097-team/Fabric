# -*- coding: utf-8 -*-
"""DoD-17 S6f: uia select 自訂 category (SelectionItemPattern) -> read strategy grid."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")

radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and w.window_text().startswith("策略雷達"):
            radar_hwnd = w.handle
            break
    except Exception:
        pass
ru = du.window(handle=radar_hwnd)

# find 自訂 and select via pattern (no mouse)
try:
    customs = [e for e in ru.descendants(control_type="TreeItem") if (e.window_text() or "").strip() == "自訂"]
    print("自訂:", len(customs))
    if customs:
        customs[0].select()
        print("selected 自訂")
        time.sleep(2.5)
except Exception as e:
    print("select err:", str(e)[:80])

# read grid now — strategy list should show FDAPaperClosure
try:
    grid = ru.child_window(control_id=17001, class_name="MFCGridCtrl")
    print("grid 17001:", grid.exists(timeout=3))
    if grid.exists(timeout=2):
        texts = [el.window_text().strip() for el in grid.descendants() if el.window_text().strip()]
        print("grid texts:", texts[:15])
except Exception as e:
    print("grid err:", str(e)[:80])
