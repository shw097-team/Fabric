# -*- coding: utf-8 -*-
"""bg v5: PostMessage 警示 tab -> read list views (LVM) for FDA_PAPER_ALERT."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
DLG = 1052534
BTN_ALERT = 0x80f72  # 警示 tab

# click 警示 tab (PostMessage BM_CLICK — focus-safe)
r = user32.PostMessageW(BTN_ALERT, 0x00F5, 0, 0)
print("post 警示:", r)
time.sleep(2)

# read list views
LVM_GETITEMCOUNT = 0x1004
LVM_GETITEMTEXT = 0x1073
LVIF_TEXT = 0x0001


class LVITEM(ctypes.Structure):
    _fields_ = [("mask", wt.UINT), ("iItem", ctypes.c_int), ("iSubItem", ctypes.c_int),
                ("state", wt.UINT), ("stateMask", wt.UINT),
                ("pszText", ctypes.c_wchar_p), ("cchTextMax", ctypes.c_int),
                ("iImage", ctypes.c_int), ("lParam", wt.LPARAM),
                ("iIndent", ctypes.c_int), ("iGroupId", ctypes.c_int),
                ("cColumns", wt.UINT), ("puColumns", wt.LPVOID),
                ("piColFmt", wt.LPVOID), ("iGroup", ctypes.c_int)]


def lv_items(hwnd, maxn=80):
    n = user32.SendMessageW(hwnd, LVM_GETITEMCOUNT, 0, 0)
    out = []
    for i in range(min(n, maxn)):
        buf = ctypes.create_unicode_buffer(128)
        item = LVITEM(LVIF_TEXT, i, 0, 0, 0, ctypes.cast(buf, ctypes.c_wchar_p), 128, 0, 0, 0, 0, 0, None, None, 0)
        user32.SendMessageW(hwnd, LVM_GETITEMTEXT, i, ctypes.byref(item))
        if buf.value.strip():
            out.append((i, buf.value))
    return out


lvs = [0x171130, 0x2d125c, 0x1c094e]
for lv in lvs:
    items = lv_items(lv)
    print(f"--- {hex(lv)} ({len(items)}) ---")
    for i, t in items[:40]:
        print("   ", i, t[:70])
