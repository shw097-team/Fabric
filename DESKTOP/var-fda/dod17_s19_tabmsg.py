# -*- coding: utf-8 -*-
"""DoD-17 S19: TCM_SETCURSEL to tab 0 (內容) — then verify strategy list appears."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

u = ctypes.windll.user32
d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x32112a

# find SysTabControl32 (cid=17003) — enumerate children for class
TAB = None
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    global TAB
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cls, 64)
    if cls.value == "SysTabControl32":
        TAB = ch
        return False
    return True
u.EnumChildWindows(RADAR, cb, 0)
print("tab ctrl:", hex(TAB) if TAB else None)
if TAB:
    # TCM_SETCURSEL = 0x130B (TCM_SETCURSELW)
    r = u.SendMessageW(TAB, 0x130B, 0, 0)  # tab 0 = 內容
    print("TCM_SETCURSEL(0) rc:", r)
    time.sleep(3)

# verify: read radar texts — 內容 tab shows strategy list (grid 17001 area)
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cls, 64)
    cid = u.GetDlgCtrlID(ch)
    if t.value.strip() and (cls.value in ("MFCGridCtrl", "Static") or cid in (33041, 17629, 17001, 17002)):
        out.append((hex(ch), cls.value[:16], cid, t.value[:42]))
    return True
u.EnumChildWindows(RADAR, cb2, 0)
print("=== after tab switch ===")
for h, c, cid, t in out[:20]:
    print(f"  {h} {c} cid={cid} '{t}'")
