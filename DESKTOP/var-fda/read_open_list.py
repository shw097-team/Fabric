# -*- coding: utf-8 -*-
"""Read list view contents of 開啟 dialog after 警示 tab click."""
import ctypes
import ctypes.wintypes as wt

user32 = ctypes.windll.user32
DLG = 0x90a02

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


lvs = [0x100d90, 0x50bae, 0x151130, 0x320cb4, 0x80d40]
for lv in lvs:
    items = lv_items(lv)
    print(f"--- {hex(lv)} ({len(items)}) ---")
    for i, t in items[:30]:
        print("   ", i, t[:70])
