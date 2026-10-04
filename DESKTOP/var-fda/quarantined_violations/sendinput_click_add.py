# -*- coding: utf-8 -*-
"""Win32 SendInput real mouse click on 加入雷達 button.
Button window-local center (2023, 611) in editor window 0x2210b8e.
ClientToScreen converts to screen coords; SetCursorPos + SendInput click.
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
EDITOR = 0x2210b8e

# client-to-screen
pt = wt.POINT(2023, 611)
user32.ClientToScreen(EDITOR, ctypes.byref(pt))
sx, sy = pt.x, pt.y
print("screen coords:", sx, sy)

# foreground editor
user32.SetForegroundWindow(EDITOR)
time.sleep(0.5)

# move cursor + click via SendInput
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wt.DWORD), ("dy", wt.DWORD), ("mouseData", wt.DWORD),
                ("dwFlags", wt.DWORD), ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]

class INPUT(ctypes.Structure):
    _fields_ = [("type", wt.DWORD), ("mi", MOUSEINPUT)]

def mouse_event(flags):
    extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
    mi = MOUSEINPUT(0, 0, 0, flags, 0, extra)
    inp = INPUT(0, mi)
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

user32.SetCursorPos(sx, sy)
time.sleep(0.3)
mouse_event(0x0002)  # LEFTDOWN
time.sleep(0.1)
mouse_event(0x0004)  # LEFTUP
print("click sent")
time.sleep(4)

# find 新增策略雷達 dialog
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 20252 and "新增策略雷達" in t.value:
        out.append((hex(hwnd), t.value[:50]))
    return True
user32.EnumWindows(cb, 0)
print("dialogs:", out)
