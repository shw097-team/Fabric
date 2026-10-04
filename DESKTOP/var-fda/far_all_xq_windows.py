# -*- coding: utf-8 -*-
"""FAR source-1: enumerate ALL XQ windows INCLUDING title-less, popup, owner-linked.
The hypothesis: FDA's screen_state_check misses small popups (no title / Afx class /
owner != top-level) — the root of 'XQ seems frozen' false positives."""
import ctypes
import ctypes.wintypes as wt

u = ctypes.windll.user32
XQ_PID = 7924

def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        out.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out

print("=== ALL XQ top-level windows (any class, any title) ===")
toplevels = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, lparam):
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        buf = ctypes.create_unicode_buffer(200)
        u.GetWindowTextW(hwnd, buf, 200)
        cls = ctypes.create_unicode_buffer(80)
        u.GetClassNameW(hwnd, cls, 80)
        # visible state
        vis = u.IsWindowVisible(hwnd)
        owner = u.GetWindow(hwnd, 4)  # GW_OWNER
        toplevels.append((hwnd, cls.value, buf.value[:55], vis, hex(owner)))
    return True
u.EnumWindows(cb, 0)

for h, c, t, vis, owner in toplevels:
    flag = "VIS" if vis else "hid"
    print(f"  {flag} {hex(h)} [{c[:28]}] '{t}' owner={owner}")

print(f"\ntotal XQ top-level: {len(toplevels)}")

print("\n=== Top-level with child windows (popup candidates) ===")
for h, c, t, vis, owner in toplevels:
    kids = enum_children(h)
    if kids and vis:
        print(f"  {hex(h)} '{t[:40]}' has {len(kids)} children")
