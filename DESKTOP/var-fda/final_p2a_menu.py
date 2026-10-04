# -*- coding: utf-8 -*-
"""FINAL P2a: read XQ main menu via win32 GetMenu/GetMenuString (no UIA).
If menu bar readable, we can send WM_COMMAND with menu item IDs directly.
"""
import ctypes
import ctypes.wintypes as wt
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32
d32 = Desktop(backend="win32")

MAIN = None
for w in d32.windows():
    try:
        if w.is_visible() and "XQ全球" in w.window_text():
            MAIN = w
            break
    except Exception:
        pass
if MAIN is None:
    print("main not found")
    raise SystemExit(2)
print("main:", hex(MAIN.handle))

# GetMenu (top-level menu bar)
hmenu = user32.GetMenu(MAIN.handle)
if not hmenu:
    print("no menu bar (GetMenu = 0)")
    raise SystemExit(2)
n = user32.GetMenuItemCount(hmenu)
print("menu items:", n)
for i in range(n):
    buf = ctypes.create_unicode_buffer(128)
    user32.GetMenuStringW(hmenu, i, buf, 128, 0x0400)  # MF_BYPOSITION
    mid = user32.GetMenuItemID(hmenu, i)
    print(f"  [{i}] id={mid} '{buf.value}'")

# submenu of 策略(D) — find by position
for i in range(n):
    buf = ctypes.create_unicode_buffer(128)
    user32.GetMenuStringW(hmenu, i, buf, 128, 0x0400)
    if "策略" in buf.value:
        sub = user32.GetSubMenu(hmenu, i)
        if sub:
            sn = user32.GetMenuItemCount(sub)
            print(f"=== 策略 submenu ({sn} items) ===")
            for j in range(sn):
                sbuf = ctypes.create_unicode_buffer(128)
                user32.GetMenuStringW(sub, j, sbuf, 128, 0x0400)
                smid = user32.GetMenuItemID(sub, j)
                print(f"  [{j}] id={smid} '{sbuf.value}'")
        break
