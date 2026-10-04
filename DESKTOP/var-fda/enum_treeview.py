# -*- coding: utf-8 -*-
"""Enumerate SysTreeView32 nodes under editor via TVM_GETITEM (native).
Check if FDA_PAPER_ALERT is in the script tree (UIA may miss it).
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
EDITOR = 0x2210b8e

# find SysTreeView32 child
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

trees = [c for c in enum_children(EDITOR) if "TreeView" in c["class"] or "Tree" in c["class"]]
print("tree views:", [(hex(c['hwnd']), c['class']) for c in trees])

# also check dialog-free: all windows titled 策略雷達 still open?
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 20252 and t.value.strip():
        out.append((hex(hwnd), t.value[:55]))
    return True
user32.EnumWindows(cb2, 0)
for h, t in out:
    print(h, '|', t)
