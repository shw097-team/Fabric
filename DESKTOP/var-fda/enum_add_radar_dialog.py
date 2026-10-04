# -*- coding: utf-8 -*-
"""Enumerate 新增策略雷達 dialog (0x30f88) controls via Win32."""
import ctypes
import ctypes.wintypes as wt

user32 = ctypes.windll.user32
DLG = 0x30f88


def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        out.append({"hwnd": ch, "text": t.value[:60], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


for c in enum_children(DLG):
    print(f"hwnd={hex(c['hwnd'])} class={c['class']!r} text={c['text']!r}")
