# -*- coding: utf-8 -*-
"""FINAL P21: read radar LEFT tree via win32 TVM — find 自訂 children (FDAPaperProbe234930)."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32
RADAR = 0x110d96

TVM_GETNEXTITEM = 0x110C
TVGN_CHILD = 0x0004
TVGN_NEXT = 0x0001
TVM_GETITEMTEXT = 0x110E
TVIF_TEXT = 0x0001
TVM_EXPAND = 0x1102
TVE_EXPAND = 0x0002
TVM_SELECTITEM = 0x110B
TVGN_CARET = 0x0009

class TVITEM(ctypes.Structure):
    _fields_ = [("mask", wt.UINT), ("hItem", wt.LPVOID), ("state", wt.UINT),
                ("stateMask", wt.UINT), ("pszText", wt.LPWSTR), ("cchTextMax", ctypes.c_int),
                ("iImage", ctypes.c_int), ("iSelectedImage", ctypes.c_int),
                ("cChildren", ctypes.c_int), ("lParam", wt.LPARAM)]

# find all SysTreeView32 under radar
trees = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    if cls.value == "SysTreeView32":
        cid = user32.GetDlgCtrlID(ch)
        trees.append((ch, cid))
    return True
user32.EnumChildWindows(RADAR, cb, 0)
print("trees:", [(hex(h), cid) for h, cid in trees])

def node_text(hwnd, hitem):
    buf = ctypes.create_unicode_buffer(256)
    item = TVITEM(TVIF_TEXT, hitem, 0, 0, ctypes.cast(buf, ctypes.c_wchar_p), 256, 0, 0, 0, 0)
    user32.SendMessageW(hwnd, TVM_GETITEMTEXT, 0, ctypes.byref(item))
    return buf.value

def walk(hwnd, parent, depth=0, maxn=120):
    out = []
    h = user32.SendMessageW(hwnd, TVM_GETNEXTITEM, TVGN_CHILD, parent)
    while h and len(out) < maxn:
        txt = node_text(hwnd, h)
        out.append((h, "  " * depth + txt[:50]))
        out.extend(walk(hwnd, h, depth + 1, maxn - len(out)))
        h = user32.SendMessageW(hwnd, TVM_GETNEXTITEM, TVGN_NEXT, h)
    return out

for h, cid in trees:
    items = walk(h, 0)
    print(f"--- tree {hex(h)} id={cid} ({len(items)} nodes) ---")
    for hi, t in items[:35]:
        print("   ", t, hex(hi))
