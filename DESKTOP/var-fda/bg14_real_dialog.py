# -*- coding: utf-8 -*-
"""bg v14: close error dialog; enumerate REAL 新增腳本 dialog 0x3a0898;
find 名稱 label + its Edit precisely."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32

# close error dialog 0x100ba0
user32.PostMessageW(0x100ba0, 0x0010, 0, 0)
print("closed error dialog")
time.sleep(1)

DLG = 0x3a0898
kids = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    r = wt.RECT()
    user32.GetWindowRect(ch, ctypes.byref(r))
    kids.append({"hwnd": ch, "class": cls.value, "text": t.value[:40],
                 "x": r.left, "y": r.top, "w": r.right - r.left, "h": r.bottom - r.top})
    return True
user32.EnumChildWindows(DLG, cb, 0)

for c in kids:
    print(f"{hex(c['hwnd'])} {c['class']!r} {c['text']!r} rect=({c['x']},{c['y']},{c['w']}x{c['h']})")
