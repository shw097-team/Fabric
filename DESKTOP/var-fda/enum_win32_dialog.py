# -*- coding: utf-8 -*-
"""Root-cause fix: enumerate Win32 dialog controls via native API (no UIA).
Lists child controls of the 新增腳本 dialog (hwnd by title) with text + class.
"""
import ctypes
import ctypes.wintypes as wt
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

GW_CHILD = 5
MAXT = 256


def find_windows(pid=None, title_sub=None):
    out = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(MAXT)
        user32.GetWindowTextW(hwnd, t, MAXT)
        title = t.value
        p = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if (pid is None or p.value == pid) and (title_sub is None or title_sub in title):
            out.append((hwnd, title, p.value))
        return True

    user32.EnumWindows(cb, 0)
    return out


def enum_children(hwnd):
    out = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(MAXT)
        user32.GetWindowTextW(ch, t, MAXT)
        cls = ctypes.create_unicode_buffer(MAXT)
        user32.GetClassNameW(ch, cls, MAXT)
        out.append({"hwnd": ch, "text": t.value[:60], "class": cls.value[:40]})
        return True

    user32.EnumChildWindows(hwnd, cb, 0)
    return out


# find the 新增腳本 dialog (any pid, title match)
dls = find_windows(title_sub="新增腳本")
print("dialogs:", [(hex(h), t, p) for h, t, p in dls])
for hwnd, title, p in dls:
    print(f"=== {title} (hwnd {hex(hwnd)}, pid {p}) children ===")
    for c in enum_children(hwnd):
        print(f"  hwnd={hex(c['hwnd'])} class={c['class']!r} text={c['text']!r}")
