# -*- coding: utf-8 -*-
"""Enumerate tree nodes on all 5 SysTreeView32 under editor 0x491044."""
import ctypes
import ctypes.wintypes as wt

user32 = ctypes.windll.user32
EDITOR = 0x491044

TVM_GETNEXTITEM = 0x110C
TVGN_CHILD = 0x0004
TVGN_NEXT = 0x0001
TVM_GETITEMTEXT = 0x110E
TVIF_TEXT = 0x0001


class TVITEM(ctypes.Structure):
    _fields_ = [("mask", wt.UINT), ("hItem", wt.LPVOID), ("state", wt.UINT),
                ("stateMask", wt.UINT), ("pszText", wt.LPWSTR), ("cchTextMax", ctypes.c_int),
                ("iImage", ctypes.c_int), ("iSelectedImage", ctypes.c_int),
                ("cChildren", ctypes.c_int), ("lParam", wt.LPARAM)]


def tree_items(tree_hwnd, maxn=80):
    items = []
    def walk(parent, depth=0):
        h = user32.SendMessageW(tree_hwnd, TVM_GETNEXTITEM, TVGN_CHILD, parent)
        while h and len(items) < maxn:
            buf = ctypes.create_unicode_buffer(256)
            item = TVITEM(TVIF_TEXT, h, 0, 0, buf, 256, 0, 0, 0, 0)
            user32.SendMessageW(tree_hwnd, TVM_GETITEMTEXT, 0, ctypes.byref(item))
            items.append(("  " * depth + (buf.value or "")[:60], h))
            walk(h, depth + 1)
            h = user32.SendMessageW(tree_hwnd, TVM_GETNEXTITEM, TVGN_NEXT, h)
    walk(0)
    return items


trees = [0x50e6e, 0xa08f4, 0x40c6c, 0x40bc0, 0x40cec]
for tv in trees:
    items = tree_items(tv)
    print(f"--- tree {hex(tv)} ({len(items)}) ---")
    for t, h in items[:50]:
        print("   ", t)
