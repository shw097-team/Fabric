# -*- coding: utf-8 -*-
"""Read list contents of 開啟 dialog 0xf0d58 — check if FDA_PAPER_ALERT visible."""
import ctypes
import ctypes.wintypes as wt

user32 = ctypes.windll.user32
DLG = 0xf0d58

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


def lv_items(hwnd, maxn=100):
    n = user32.SendMessageW(hwnd, LVM_GETITEMCOUNT, 0, 0)
    out = []
    for i in range(min(n, maxn)):
        buf = ctypes.create_unicode_buffer(128)
        item = LVITEM(LVIF_TEXT, i, 0, 0, 0, ctypes.cast(buf, ctypes.c_wchar_p), 128, 0, 0, 0, 0, 0, None, None, 0)
        user32.SendMessageW(hwnd, LVM_GETITEMTEXT, i, ctypes.byref(item))
        if buf.value.strip():
            out.append((i, buf.value))
    return out


def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        out.append({"hwnd": ch, "text": t.value[:50], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


kids = enum_children(DLG)
lvs = [c for c in kids if "SysListView32" in c["class"]]
print("lists:", [hex(c["hwnd"]) for c in lvs])
for lv in lvs:
    items = lv_items(lv["hwnd"])
    print(f"--- {hex(lv['hwnd'])} ({len(items)}) ---")
    for i, t in items[:40]:
        print("   ", i, t[:70])
