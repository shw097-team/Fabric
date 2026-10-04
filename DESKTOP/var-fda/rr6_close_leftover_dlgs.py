# -*- coding: utf-8 -*-
"""Close leftover 新增策略雷達 dialogs (error 確定 + main 取消). Zero mouse."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
XQ_PID = 7924

def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        buf = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(h, buf, 128)
        out.append((h, buf.value[:50]))
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out

dlgs = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, lparam):
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        buf = ctypes.create_unicode_buffer(100)
        u.GetWindowTextW(hwnd, buf, 100)
        t = buf.value
        if "新增策略雷達" in t:
            dlgs.append(hwnd)
    return True
u.EnumWindows(cb, 0)

for d in dlgs:
    kids = enum_children(d)
    err = any("該名稱已被使用" in k[1] for k in kids)
    print(f"dialog {hex(d)} err={'該名稱已被使用' if err else ''}")
    for ch, t in kids:
        if err and "確定" in t:
            u.PostMessageW(ch, 0x00F5, 0, 0)
            print(f"  clicked 確定 {hex(ch)}")
        elif (not err) and "取消" in t:
            u.PostMessageW(ch, 0x00F5, 0, 0)
            print(f"  clicked 取消 {hex(ch)}")

print("done; dialogs:", len(dlgs))
