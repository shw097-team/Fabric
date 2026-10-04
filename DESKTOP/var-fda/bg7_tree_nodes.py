# -*- coding: utf-8 -*-
"""bg v7: enumerate SysTreeView32 nodes of 開啟 dialog (Win32 read-only).
Find 自訂 node -> select it (TVM_SELECTITEM) -> then read list.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
DLG = 0x100f76

TVM_GETNEXTITEM = 0x110C
TVGN_CHILD = 0x0004
TVGN_NEXT = 0x0001
TVM_GETITEMTEXT = 0x110E
TVIF_TEXT = 0x0001
TVM_SELECTITEM = 0x110B
TVGN_CARET = 0x0009
TVM_EXPAND = 0x1102
TVE_EXPAND = 0x0002


class TVITEM(ctypes.Structure):
    _fields_ = [("mask", wt.UINT), ("hItem", wt.LPVOID), ("state", wt.UINT),
                ("stateMask", wt.UINT), ("pszText", wt.LPWSTR), ("cchTextMax", ctypes.c_int),
                ("iImage", ctypes.c_int), ("iSelectedImage", ctypes.c_int),
                ("cChildren", ctypes.c_int), ("lParam", wt.LPARAM)]


def tree_items(tree_hwnd, maxn=60):
    items = []
    def walk(parent, depth=0):
        h = user32.SendMessageW(tree_hwnd, TVM_GETNEXTITEM, TVGN_CHILD, parent)
        while h and len(items) < maxn:
            buf = ctypes.create_unicode_buffer(256)
            item = TVITEM(TVIF_TEXT, h, 0, 0, ctypes.cast(buf, ctypes.c_wchar_p), 256, 0, 0, 0, 0)
            user32.SendMessageW(tree_hwnd, TVM_GETITEMTEXT, 0, ctypes.byref(item))
            items.append(("  " * depth + (buf.value or "")[:50], h))
            walk(h, depth + 1)
            h = user32.SendMessageW(tree_hwnd, TVM_GETNEXTITEM, TVGN_NEXT, h)
    walk(0)
    return items


trees = [0x241108, 0x2b024e, 0x2505e6, 0x80efc]
for tv in trees:
    items = tree_items(tv)
    print(f"--- tree {hex(tv)} ({len(items)}) ---")
    for t, h in items[:25]:
        print("   ", t, hex(h))
