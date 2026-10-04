# -*- coding: utf-8 -*-
"""Full pipeline: UIA pixel click 加入雷達 -> Win32 dialog -> SendInput name -> click 加入."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import time
from pathlib import Path

user32 = ctypes.windll.user32
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 20252
EDITOR = 0x2210b8e


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


def find_dialog():
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, t, 256)
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == PID and "新增策略雷達" in t.value:
            out.append(hwnd)
        return True
    user32.EnumWindows(cb, 0)
    return out


# 1. UIA pixel click on 加入雷達 (2023, 611 client coords of editor window 35720078)
r = subprocess.run([CUA, "call", "click", json.dumps(
    {"pid": PID, "x": 2023, "y": 611, "delivery_mode": "foreground"})],
    capture_output=True, timeout=40, env=ENV)
print("click:", r.stdout.decode("utf-8", errors="replace")[:50])
time.sleep(4)

dls = find_dialog()
print("dialog:", [hex(d) for d in dls])
if not dls:
    raise SystemExit(2)
DLG = dls[0]

# 2. enumerate dialog
kids = enum_children(DLG)
edits = [c for c in kids if c["class"] == "Edit"]
add_btn = next((c for c in kids if "加入" in c["text"]), None)
print("edits:", [hex(c["hwnd"]) for c in edits])
print("加入 btn:", hex(add_btn["hwnd"]) if add_btn else None)

# 3. SendInput: foreground dialog, click name edit, type name
if edits:
    edit = edits[0]["hwnd"]
    user32.SetForegroundWindow(DLG)
    time.sleep(0.5)
    er = wt.RECT()
    user32.GetWindowRect(edit, ctypes.byref(er))
    cx = (er.left + er.right) // 2
    cy = (er.top + er.bottom) // 2

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
    time.sleep(0.3)
    mouse_event(0x0002)
    mouse_event(0x0004)
    time.sleep(0.5)

    # type name via SendInput keyboard (VK codes)
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
        time.sleep(0.05)
    time.sleep(0.5)

    t2 = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edit, t2, 128)
    print("name edit now:", repr(t2.value[:40]))

# 4. click 加入
if add_btn:
    user32.PostMessageW(add_btn["hwnd"], 0x00F5, 0, 0)
    print("clicked 加入")
    time.sleep(6)

# 5. verify DB
import sqlite3
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite")
rows = c.execute("SELECT Name, Enable, LastExecuteTime, ScriptType FROM XSTradeStrategyDTO WHERE Name LIKE '%FDA%'").fetchall()
print("DB:", rows)
c.close()
