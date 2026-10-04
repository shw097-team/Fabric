# -*- coding: utf-8 -*-
"""Open radar via 警示提示 dialog 策略雷達(&A) button (direct path). Zero mouse."""
import ctypes
import ctypes.wintypes as wt
import time

u = ctypes.windll.user32
XQ_PID = 7924

def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        buf = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(h, buf, 128)
        out.append((h, buf.value[:60]))
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out

# find 警示提示 dialog with 策略雷達 button
target = None
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, lparam):
    global target
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        buf = ctypes.create_unicode_buffer(100)
        u.GetWindowTextW(hwnd, buf, 100)
        if "警示提示" in buf.value:
            for ch, t in enum_children(hwnd):
                if "策略雷達" in t:
                    target = ch
                    return False
    return True
u.EnumWindows(cb, 0)

if target:
    print("found 策略雷達 button:", hex(target))
    u.PostMessageW(target, 0x00F5, 0, 0)
    print("clicked (PostMessage BM_CLICK)")
else:
    print("策略雷達 button not found")

time.sleep(5)
# verify radar window
out = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb2(hwnd, lparam):
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        buf = ctypes.create_unicode_buffer(200)
        u.GetWindowTextW(hwnd, buf, 200)
        if "策略雷達" in buf.value:
            out.append((hex(hwnd), buf.value[:50]))
    return True
u.EnumWindows(cb2, 0)
print("radar windows:", out if out else "none yet")
