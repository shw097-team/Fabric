# -*- coding: utf-8 -*-
"""DoD-17 S6: read radar strategy grid (17001) — find FDAPaperClosure in UI (truth surface)."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")

# find radar window
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and "策略雷達" in w.window_text() and "說明" not in w.window_text():
            radar_hwnd = w.handle
            break
    except Exception:
        pass
print("radar:", hex(radar_hwnd) if radar_hwnd else None)
if not radar_hwnd:
    raise SystemExit(2)

# uia read grid 17001 (strategy list) — read-only, small scope
ru = du.window(handle=radar_hwnd)
try:
    grid = ru.child_window(control_id=17001, class_name="MFCGridCtrl")
    print("grid 17001 exists:", grid.exists(timeout=3))
    if grid.exists(timeout=2):
        texts = []
        for el in grid.descendants():
            try:
                t = el.window_text().strip()
                if t and len(t) < 60:
                    texts.append(t)
            except Exception:
                pass
        print("grid texts:", texts[:15])
except Exception as e:
    print("grid err:", str(e)[:80])

# also try win32 direct child text
print("\n=== win32 children of radar ===")
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    ctypes.windll.user32.GetWindowTextW(ch, t, 128)
    if t.value.strip():
        cls = ctypes.create_unicode_buffer(64)
        ctypes.windll.user32.GetClassNameW(ch, cls, 64)
        print(f"  {hex(ch)} {cls.value[:20]} '{t.value[:35]}'")
    return True
ctypes.windll.user32.EnumChildWindows(radar_hwnd, cb, 0)
