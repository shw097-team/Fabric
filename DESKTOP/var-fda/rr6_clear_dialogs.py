# -*- coding: utf-8 -*-
"""Close leftover XQ notification dialogs (read-only enumerate + PostMessage BM_CLICK).
Screen-state-first: show buttons before closing. Zero mouse."""
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
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        out.append((h, cls.value, buf.value[:60]))
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out

# enumerate all XQ dialogs with class #32770 / Afx 警示
dlgs = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, lparam):
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        buf = ctypes.create_unicode_buffer(200)
        u.GetWindowTextW(hwnd, buf, 200)
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(hwnd, cls, 64)
        if cls.value.startswith("#32770") or "Afx" in cls.value:
            dlgs.append((hwnd, cls.value, buf.value[:50]))
    return True
u.EnumWindows(cb, 0)

print(f"found {len(dlgs)} dialogs:")
for h, c, t in dlgs:
    children = enum_children(h)
    btns = [(ch, ct, ct2) for ch, ct, ct2 in children if ct == "Button"]
    print(f"  {hex(h)} [{c}] '{t}' buttons: {[(ct2 or hex(ch)) for ch, ct, ct2 in btns][:4]}")

# close 警示提示 + 交易訊息中心 + XQ 交易資訊 (notification dialogs)
closed = 0
for h, c, t in dlgs:
    if "警示提示" in t or "交易訊息" in t or "交易資訊" in t:
        children = enum_children(h)
        for ch, ct, ct2 in children:
            if ct == "Button" and ("關閉" in ct2 or "確定" in ct2 or "OK" in ct2):
                u.PostMessageW(ch, 0x00F5, 0, 0)
                closed += 1
                print(f"  clicked: {hex(ch)} '{ct2}' in '{t}'")
                break
print(f"closed {closed} notification buttons")
