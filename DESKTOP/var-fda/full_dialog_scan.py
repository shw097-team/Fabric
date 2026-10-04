# -*- coding: utf-8 -*-
"""FULL dialog scan: enumerate ALL XQ-related top-level windows incl Afx classes + child buttons.
Pure read-only (EnumWindows/EnumChildWindows), zero mouse."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
PID = 23456
out = []

@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value != PID:
        return True
    t = ctypes.create_unicode_buffer(256)
    u.GetWindowTextW(hwnd, t, 256)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(hwnd, cls, 64)
    if u.IsWindowVisible(hwnd):
        out.append((hwnd, cls.value, t.value))
    return True

u.EnumWindows(cb, 0)
print(f"=== XQ visible top-level windows ({len(out)}) ===")
for h, c, t in out:
    print(f"  {hex(h)} | {c[:35]} | '{t[:60]}'")
    # enumerate child buttons
    btns = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb2(ch, lp):
        tc = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(ch, tc, 128)
        cc = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(ch, cc, 64)
        if "Button" in cc.value and tc.value.strip():
            btns.append((hex(ch), tc.value[:25]))
        return True
    u.EnumChildWindows(h, cb2, 0)
    if btns:
        for bh, bt in btns[:8]:
            print(f"      btn {bh} '{bt}'")
