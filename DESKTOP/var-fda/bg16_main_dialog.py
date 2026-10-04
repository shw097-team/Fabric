# -*- coding: utf-8 -*-
"""bg v16: REAL main dialog 0x100ba0 — full children with labels+rects."""
import ctypes
import ctypes.wintypes as wt

user32 = ctypes.windll.user32
DLG = 0x100ba0

kids = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    r = wt.RECT()
    user32.GetWindowRect(ch, ctypes.byref(r))
    dr = wt.RECT()
    user32.GetWindowRect(DLG, ctypes.byref(dr))
    kids.append({"hwnd": ch, "class": cls.value, "text": t.value[:40],
                 "lx": r.left - dr.left, "ly": r.top - dr.top,
                 "w": r.right - r.left, "h": r.bottom - r.top})
    return True
user32.EnumChildWindows(DLG, cb, 0)

for c in kids:
    print(f"{hex(c['hwnd'])} {c['class']!r} {c['text']!r} local=({c['lx']},{c['ly']},{c['w']}x{c['h']})")
