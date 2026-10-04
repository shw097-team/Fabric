# -*- coding: utf-8 -*-
"""bg v4: enumerate 開啟 dialog (wid 1052534) — find 警示 tab, list, 確認.
Win32 READ-ONLY + PostMessage BM_CLICK only.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
DLG = 1052534


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
for c in kids:
    print(f"{hex(c['hwnd'])} {c['class']!r} {c['text']!r}")
