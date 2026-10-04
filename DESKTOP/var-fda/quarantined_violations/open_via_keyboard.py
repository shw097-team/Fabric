# -*- coding: utf-8 -*-
"""Open dialog via keyboard: foreground, focus name Edit, type FDA_PAPER_ALERT, Enter."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
DLG = 0x4d05f8

# foreground dialog
user32.SetForegroundWindow(DLG)
time.sleep(0.8)

# Enumerate edits + their rects
def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        out.append({"hwnd": ch, "text": t.value[:50], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out

edits = [c for c in enum_children(DLG) if c["class"] == "Edit"]
print("edits:", [(hex(c["hwnd"]), c["text"]) for c in edits])

# focus first visible edit via click
for edit in edits:
    er = wt.RECT()
    user32.GetWindowRect(edit["hwnd"], ctypes.byref(er))
    w = er.right - er.left
    h = er.bottom - er.top
    if w > 60 and h > 15:  # skip tiny invisible ones
        cx = (er.left + er.right) // 2
        cy = (er.top + er.bottom) // 2
        print("edit rect:", er.left, er.top, w, h, "center:", cx, cy)

        # click into it
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

        user32.SetCursorPos(cx, cy)
        time.sleep(0.2)
        mouse_event(0x0002)
        mouse_event(0x0004)
        time.sleep(0.4)

        # type name
        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [("wVk", wt.WORD), ("wScan", wt.WORD), ("dwFlags", wt.DWORD),
                        ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]
        class INPUT2(ctypes.Structure):
            _fields_ = [("type", wt.DWORD), ("ki", KEYBDINPUT)]

        def key_event(vk, down):
            extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
            ki = KEYBDINPUT(vk, 0, 0 if down else 0x0002, 0, extra)
            inp = INPUT2(1, ki)
            user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT2))

        name = "FDA_PAPER_ALERT"
        for ch in name:
            vk = ord(ch.upper())
            key_event(vk, True)
            key_event(vk, False)
            time.sleep(0.04)
        time.sleep(0.5)
        # read back
        t2 = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(edit["hwnd"], t2, 128)
        print("after type:", repr(t2.value[:40]))
        break

# press Enter (default confirm)
time.sleep(0.5)
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wt.WORD), ("wScan", wt.WORD), ("dwFlags", wt.DWORD),
                ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]
class INPUT2(ctypes.Structure):
    _fields_ = [("type", wt.DWORD), ("ki", KEYBDINPUT)]
def key_event(vk, down):
    extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
    ki = KEYBDINPUT(vk, 0, 0 if down else 0x0002, 0, extra)
    inp = INPUT2(1, ki)
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT2))
key_event(0x0D, True)  # Enter
key_event(0x0D, False)
print("Enter pressed")
time.sleep(4)

# check editor title change
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 12260 and "XScript" in t.value:
        out.append((hex(hwnd), t.value[:70]))
    return True
user32.EnumWindows(cb2, 0)
print("editor:", out)
