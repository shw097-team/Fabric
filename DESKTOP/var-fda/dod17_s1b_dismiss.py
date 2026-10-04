# -*- coding: utf-8 -*-
"""DoD-17 S1b: dismiss 開放體驗說明 via 我知道了 button (win32 message), verify radar."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
u = ctypes.windll.user32
DLG = 0x3512aa

# enumerate dialog children to find 我知道了 button
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(ch, cls, 64)
    out.append((ch, cls.value, t.value[:30]))
    return True
u.EnumChildWindows(DLG, cb, 0)
for h, c, t in out:
    print(hex(h), c, repr(t))

# click 我知道了 button (BM_CLICK)
target = next((h for h, c, t in out if "我知道了" in t or "知道" in t), None)
if not target:
    # fallback: first Button
    target = next((h for h, c, t in out if c == "Button"), None)
if target:
    u.PostMessageW(target, 0x00F5, 0, 0)  # BM_CLICK
    print("clicked:", hex(target))
    time.sleep(3)

# verify radar window
radar = None
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    u.GetWindowTextW(hwnd, t, 256)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(hwnd, cls, 64)
    if "策略雷達" in t.value and "說明" not in t.value:
        radar = hwnd
        return False
    return True
u.EnumWindows(cb2, 0)
print("radar hwnd:", hex(radar) if radar else None)
