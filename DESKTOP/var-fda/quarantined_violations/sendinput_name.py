# -*- coding: utf-8 -*-
"""Close error dialog; focus name edit in 0x30f88; SendInput type name; click 加入."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
WM_SETTEXT = 0x000C

# 1. close error dialog
user32.PostMessageW(0x5110e, WM_CLOSE, 0, 0)
time.sleep(1)

DLG = 0x30f88


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


kids = enum_children(DLG)
edits = [c for c in kids if c["class"] == "Edit"]
add_btn = next((c for c in kids if "加入" in c["text"]), None)
print("edits:", [hex(c["hwnd"]) for c in edits])
print("加入 btn:", hex(add_btn["hwnd"]) if add_btn else None)

if edits:
    edit = edits[0]["hwnd"]
    # try WM_SETTEXT first (may work on this dialog)
    name = "FDA_PAPER_ALERT"
    buf = ctypes.create_unicode_buffer(name)
    user32.PostMessageW(edit, WM_SETTEXT, 0, ctypes.cast(buf, ctypes.c_void_p))
    time.sleep(1)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edit, t, 128)
    print("after WM_SETTEXT:", repr(t.value[:40]))
    if not t.value:
        # SendInput real keyboard: click edit then type
        er = wt.RECT()
        user32.GetWindowRect(edit, ctypes.byref(er))
        cx = (er.left + er.right) // 2
        cy = (er.top + er.bottom) // 2
        print("edit center:", cx, cy)
        # set foreground + click
        user32.SetForegroundWindow(DLG)
        time.sleep(0.5)

        # SendInput mouse click
        INPUT_MOUSE = 0
        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [("dx", wt.DWORD), ("dy", wt.DWORD), ("mouseData", wt.DWORD),
                        ("dwFlags", wt.DWORD), ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]

        class INPUT(ctypes.Structure):
            _fields_ = [("type", wt.DWORD), ("mi", MOUSEINPUT)]

        def mouse_event(flags, x, y):
            extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
            mi = MOUSEINPUT(x, y, 0, flags, 0, extra)
            inp = INPUT(INPUT_MOUSE, mi)
            user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

        # absolute coords need normalized; use relative moves instead
        # simpler: SetCursorPos + mouse_event
        user32.SetCursorPos(cx, cy)
        time.sleep(0.3)
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.5)

        # SendInput keyboard for name
        KEYEVENTF_KEYUP = 0x0002
        INPUT_KEYBOARD = 1

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [("wVk", wt.WORD), ("wScan", wt.WORD), ("dwFlags", wt.DWORD),
                        ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]

        class INPUT2(ctypes.Structure):
            _fields_ = [("type", wt.DWORD), ("ki", KEYBDINPUT)]

        def key_event(vk, down):
            extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
            ki = KEYBDINPUT(vk, 0, 0 if down else KEYEVENTF_KEYUP, 0, extra)
            inp = INPUT2(INPUT_KEYBOARD, ki)
            user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT2))

        # type each char via VK codes (ASCII)
        for ch in name:
            vk = ord(ch.upper())
            key_event(vk, True)
            key_event(vk, False)
            time.sleep(0.05)
        time.sleep(0.5)
        t2 = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(edit, t2, 128)
        print("after SendInput:", repr(t2.value[:40]))

if add_btn:
    user32.PostMessageW(add_btn["hwnd"], BM_CLICK, 0, 0)
    print("clicked 加入")
    time.sleep(5)

# verify
import sqlite3
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite")
rows = c.execute("SELECT Name, Enable, LastExecuteTime, ScriptType FROM XSTradeStrategyDTO WHERE Name LIKE '%FDA%'").fetchall()
print("DB:", rows)
c.close()
