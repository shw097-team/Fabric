# -*- coding: utf-8 -*-
"""DoD-17 S16: check leftover dialogs; uia select 自訂 (pattern); re-read grid empty-state."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
u = ctypes.windll.user32

# 1. any #32770 dialogs besides radar/main?
print("=== #32770 dialogs ===")
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible():
            print(" ", hex(w.handle), "|", w.window_text()[:45])
    except Exception:
        pass

# 2. select 自訂 in radar tree (uia pattern)
RADAR = 0x32112a
ru = du.window(handle=RADAR)
try:
    items = ru.descendants(control_type="TreeItem")
    custom = next((i for i in items if (i.window_text() or "").strip() == "自訂"), None)
    print("自訂:", bool(custom))
    if custom:
        custom.select()
        print("selected 自訂")
        time.sleep(3)
except Exception as e:
    print("select err:", str(e)[:70])

# 3. re-read radar text (empty-state msg gone?)
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cid = u.GetDlgCtrlID(ch)
    if t.value.strip() and cid in (33041, 17629, 17107, 33530):
        out.append((hex(ch), cid, t.value[:45]))
    return True
u.EnumChildWindows(RADAR, cb, 0)
print("=== key radar texts ===")
for h, cid, t in out:
    print(f"  {h} cid={cid} '{t}'")
