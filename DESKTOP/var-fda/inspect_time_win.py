# -*- coding: utf-8 -*-
"""Inspect 時間 window (0xe1014): class, owner, children — decide close or ignore."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
H = 0xe1014
cls = ctypes.create_unicode_buffer(64)
u.GetClassNameW(H, cls, 64)
t = ctypes.create_unicode_buffer(128)
u.GetWindowTextW(H, t, 128)
owner = u.GetWindow(H, 4)  # GW_OWNER
style = u.GetWindowLongW(H, -16)  # GWL_STYLE
exstyle = u.GetWindowLongW(H, -20)  # GWL_EXSTYLE
print(f"hwnd={hex(H)} class={cls.value} text='{t.value}' owner={hex(owner)}")
print(f"style=0x{style:08X} exstyle=0x{exstyle:08X}")
print(f"  WS_VISIBLE={bool(style & 0x10000000)} WS_CAPTION={bool(style & 0x00C00000)} WS_POPUP={bool(style & 0x80000000)}")
print(f"  WS_EX_TOOLWINDOW={bool(exstyle & 0x80)} WS_EX_TOPMOST={bool(exstyle & 0x8)}")

# children
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lp):
    tc = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, tc, 128)
    cc = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cc, 64)
    out.append((hex(ch), cc.value, tc.value[:30]))
    return True
u.EnumChildWindows(H, cb, 0)
print("children:", out[:6] if out else "(none)")
