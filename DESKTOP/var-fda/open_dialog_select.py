# -*- coding: utf-8 -*-
"""Open dialog: click 警示 type, then find FDA_PAPER_ALERT in list, select, confirm."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
BM_CLICK = 0x00F5
WM_SETTEXT = 0x000C

DLG = 0x4d05f8
BTN_ALERT = 0xe0d92
BTN_CONFIRM = 0xf0d90
# list views for script list
LV_0 = 0x8097a  # first SysListView32 (type tree list?)
LV_1 = 0x70e90  # second SysListView32 (script list?)

# 1. click 警示 type
user32.PostMessageW(BTN_ALERT, BM_CLICK, 0, 0)
print("clicked 警示 type")
time.sleep(2)

# 2. enumerate list view items (LVM_GETITEMCOUNT / LVM_GETITEMTEXT)
LVM_GETITEMCOUNT = 0x1004
LVM_GETITEMTEXT = 0x1073
LVIF_TEXT = 0x0001


class LVITEM(ctypes.Structure):
    _fields_ = [("mask", wt.UINT), ("iItem", ctypes.c_int), ("iSubItem", ctypes.c_int),
                ("state", wt.UINT), ("stateMask", wt.UINT),
                ("pszText", wt.LPWSTR), ("cchTextMax", ctypes.c_int),
                ("iImage", ctypes.c_int), ("lParam", wt.LPARAM),
                ("iIndent", ctypes.c_int), ("iGroupId", ctypes.c_int),
                ("cColumns", wt.UINT), ("puColumns", wt.LPVOID),
                ("piColFmt", wt.LPVOID), ("iGroup", ctypes.c_int)]


def lv_items(hwnd, maxn=60):
    n = user32.SendMessageW(hwnd, LVM_GETITEMCOUNT, 0, 0)
    out = []
    for i in range(min(n, maxn)):
        buf = ctypes.create_unicode_buffer(128)
        item = LVITEM(LVIF_TEXT, i, 0, 0, 0, ctypes.cast(buf, ctypes.c_wchar_p), 128, 0, 0, 0, 0, 0, None, None, 0)
        user32.SendMessageW(hwnd, LVM_GETITEMTEXT, i, ctypes.byref(item))
        out.append((i, buf.value))
    return out


for lvname, lv in (("LV_A", LV_0), ("LV_B", LV_1)):
    items = lv_items(lv)
    print(f"--- {lvname} ({len(items)}) ---")
    for i, t in items[:40]:
        print("   ", i, t[:60])
