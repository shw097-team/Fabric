# -*- coding: utf-8 -*-
"""Check XQ window state: main / editor / radar (win32 read-only)."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
titles = []

@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, _):
    buf = ctypes.create_unicode_buffer(512)
    u.GetWindowTextW(hwnd, buf, 512)
    t = buf.value
    if "XQ" in t or "XScript" in t or "策略" in t or "雷達" in t:
        titles.append((hwnd, t[:80]))
    return True

u.EnumWindows(cb, 0)
for h, t in titles:
    print(f"0x{h:x} | {t}")
