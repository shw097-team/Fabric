# -*- coding: utf-8 -*-
"""DoD-17 S6b: full radar left tree — find 自訂 category + FDAPaperClosure."""
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
        if w.is_visible() and "策略雷達" in w.window_text() and "說明" not in w.window_text():
            radar_hwnd = w.handle
            break
    except Exception:
        pass

ru = du.window(handle=radar_hwnd)
try:
    trees = ru.descendants(control_type="Tree")
    print("trees:", len(trees))
    for ti, tv in enumerate(trees):
        items = tv.descendants(control_type="TreeItem")
        vis = [i.window_text().strip() for i in items if i.window_text().strip()]
        print(f"tree {ti}: {len(vis)} items")
        for v in vis[:25]:
            print("   ", v[:40])
        # find 自訂 and expand
        for it in items:
            if it.window_text().strip().startswith("自訂"):
                try:
                    it.expand()
                    time.sleep(1)
                    print("expanded 自訂:")
                    for sub in it.descendants(control_type="TreeItem"):
                        t = sub.window_text().strip()
                        if t:
                            print("     ", t[:45])
                except Exception as e:
                    print("expand err:", str(e)[:50])
except Exception as e:
    print("tree err:", str(e)[:80])
