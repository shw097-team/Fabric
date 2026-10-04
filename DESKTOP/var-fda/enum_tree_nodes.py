# -*- coding: utf-8 -*-
"""Enumerate all SysTreeView32 nodes via TVM_GETNEXTITEM to find FDA_PAPER_ALERT."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
comctl32 = ctypes.windll.comctl32

EDITOR = 0x4903c4  # cua window_id 4788292 -> hex? compute below

# window_id 4788292 = 0x4903C4
print("editor hwnd guess:", hex(EDITOR))


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


def tree_items(tree_hwnd, root=0):
    items = []
    def walk(parent):
        h = user32.SendMessageW(tree_hwnd, TVM_GETNEXTITEM, TVGN_CHILD, parent)
        while h:
            buf = ctypes.create_unicode_buffer(256)
            item = TVITEM(TVIF_TEXT, h, 0, 0, buf, 256, 0, 0, 0, 0)
            user32.SendMessageW(tree_hwnd, TVM_GETITEMTEXT, 0, ctypes.byref(item))
            text = buf.value
            items.append((h, text))
            walk(h)
            h = user32.SendMessageW(tree_hwnd, TVM_GETNEXTITEM, TVGN_NEXT, h)
    walk(root)
    return items


trees = [c for c in enum_children(EDITOR) if "TreeView" in c["class"]]
print("tree views:", [(hex(c["hwnd"]), c["class"]) for c in trees])
for tv in trees:
    items = tree_items(tv["hwnd"])
    print(f"--- tree {hex(tv['hwnd'])} ({len(items)} items) ---")
    for h, t in items[:40]:
        print("   ", t[:60])
