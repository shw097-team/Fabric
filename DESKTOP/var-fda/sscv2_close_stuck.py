# -*- coding: utf-8 -*-
"""SSC-V2 disposition: close stuck dialogs — error dialog 確定 + main dialog 取消.
PostMessage BM_CLICK only; zero mouse."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
XQ_PID = 7924

def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        b = ctypes.create_unicode_buffer(100)
        u.GetWindowTextW(h, b, 100)
        c = ctypes.create_unicode_buffer(50)
        u.GetClassNameW(h, c, 50)
        out.append((h, c.value, b.value[:40]))
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out

dlgs = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb2(hwnd, lparam):
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        b = ctypes.create_unicode_buffer(120)
        u.GetWindowTextW(hwnd, b, 120)
        if "新增策略雷達" in b.value:
            kids = enum_children(hwnd)
            is_err = any("名稱已被使用" in k[2] for k in kids)
            is_main = any("加入" in k[2] for k in kids)
            dlgs.append((hwnd, is_err, is_main, kids))
    return True
u.EnumWindows(cb2, 0)

for h, is_err, is_main, kids in dlgs:
    print(f"dialog {hex(h)} err={is_err} main={is_main}")
    for ch, cls, txt in kids:
        if is_err and txt == "確定":
            u.PostMessageW(ch, 0x00F5, 0, 0)
            print(f"  clicked 確定 {hex(ch)}")
        elif is_main and txt == "取消(&C)":
            u.PostMessageW(ch, 0x00F5, 0, 0)
            print(f"  clicked 取消 {hex(ch)}")

print("done")
