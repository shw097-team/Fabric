# -*- coding: utf-8 -*-
"""PURE-MESSAGE TVM: read radar left tree (SysTreeView32 32926) — find 自訂 + strategy nodes.
TVM_GETNEXTITEM / TVM_GETITEM with TVITEM struct. Zero mouse, zero UIA."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
RADAR = 0x80fc8
TREE = 0x90fd6  # SysTreeView32 cid=32926

# TVM constants
TVM_GETNEXTITEM = 0x110C
TVM_GETITEM = 0x110C + 1  # TVM_GETITEMW = 0x110E actually
TVM_GETITEMW = 0x110E
TVM_EXPAND = 0x1102
TVM_SELECTITEM = 0x110B
TVGN_ROOT = 0
TVGN_NEXT = 1
TVGN_CHILD = 4
TVGN_CARET = 9
TVE_EXPAND = 2
TVIF_TEXT = 1

class TVITEMW(ctypes.Structure):
    _fields_ = [
        ("mask", ctypes.c_uint),
        ("hItem", ctypes.c_void_p),
        ("state", ctypes.c_uint),
        ("stateMask", ctypes.c_uint),
        ("pszText", ctypes.c_wchar_p),
        ("cchTextMax", ctypes.c_int),
        ("iImage", ctypes.c_int),
        ("iSelectedImage", ctypes.c_int),
        ("cChildren", ctypes.c_int),
        ("lParam", ctypes.c_void_p),
    ]

def get_text(hItem):
    buf = ctypes.create_unicode_buffer(256)
    item = TVITEMW()
    item.mask = TVIF_TEXT
    item.hItem = hItem
    item.pszText = buf
    item.cchTextMax = 256
    r = u.SendMessageW(TREE, TVM_GETITEMW, 0, ctypes.byref(item))
    return buf.value

def get_child(parent):
    return u.SendMessageW(TREE, TVM_GETNEXTITEM, TVGN_CHILD, parent)

def get_next(hItem):
    return u.SendMessageW(TREE, TVM_GETNEXTITEM, TVGN_NEXT, hItem)

def expand(hItem):
    u.SendMessageW(TREE, TVM_EXPAND, TVE_EXPAND, hItem)

def walk_tree(root, depth=0, max_nodes=200):
    """BFS walk of tree, printing text."""
    nodes = []
    h = get_child(root)
    count = 0
    while h and count < max_nodes:
        t = get_text(h)
        nodes.append((h, t, depth))
        h = get_next(h)
        count += 1
    # expand each and recurse
    for h, t, d in list(nodes):
        if d < 4:
            expand(h)
            nodes.extend(walk_tree(h, d + 1, max_nodes))
    return nodes

root = u.SendMessageW(TREE, TVM_GETNEXTITEM, TVGN_ROOT, 0)
print("root:", hex(root) if root else None)
if root:
    nodes = walk_tree(root)
    print(f"tree nodes: {len(nodes)}")
    for h, t, d in nodes:
        print("  " * d + f"| {t[:40]} (h={hex(h)})")
