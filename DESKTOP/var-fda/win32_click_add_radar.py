# -*- coding: utf-8 -*-
"""Win32-native: find '加入雷達' button hwnd under editor window, PostMessage BM_CLICK.
Then watch for 新增策略雷達 dialog via EnumWindows.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
BM_CLICK = 0x00F5
WM_CLOSE = 0x0010

EDITOR = 0x2210b8e


def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        out.append({"hwnd": ch, "text": t.value[:40], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


# find button with text containing 加入雷達
target = None
for c in enum_children(EDITOR):
    if "雷達" in c["text"] and "加入" in c["text"]:
        target = c
        break
    if "加入雷達" in c["text"]:
        target = c
        break
print("加入雷達 btn:", hex(target["hwnd"]) if target else None, target["text"] if target else "")
if target:
    r = user32.PostMessageW(target["hwnd"], BM_CLICK, 0, 0)
    print("post click:", r)
    time.sleep(5)

# find any top-level dialog for pid
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 20252 and t.value.strip() and "XQ全球" not in t.value and "XScript" not in t.value:
        out.append((hex(hwnd), t.value[:60]))
    return True
user32.EnumWindows(cb2, 0)
for h, t in out:
    print("WIN:", h, "|", t)
