# -*- coding: utf-8 -*-
"""Step 2: Ctrl+O, Win32 警示 tab click, keyboard-navigate to FDA_PAPER_ALERT, Enter."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import time
from pathlib import Path

user32 = ctypes.windll.user32
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 14200
EWID = 0xa0a64


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


def find_dialog(title):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, t, 256)
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if p.value == PID and title in t.value:
            out.append(hwnd)
        return True
    user32.EnumWindows(cb, 0)
    return out


# 1. Ctrl+O on editor
r = subprocess.run([CUA, "call", "hotkey", json.dumps(
    {"pid": PID, "window_id": EWID, "keys": ["ctrl", "o"], "delivery_mode": "foreground"})],
    capture_output=True, timeout=40, env=ENV)
print("ctrl+o:", r.stdout.decode("utf-8", errors="replace")[:40])
time.sleep(4)

dls = find_dialog("開啟")
print("開啟 dialog:", [hex(d) for d in dls])
if not dls:
    raise SystemExit(2)
DLG = dls[0]

# 2. click 警示 tab
kids = enum_children(DLG)
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
print("警示 tab:", hex(alert_btn["hwnd"]) if alert_btn else None)
if alert_btn:
    user32.PostMessageW(alert_btn["hwnd"], 0x00F5, 0, 0)
    time.sleep(2)

# 3. keyboard navigation: click into list area then type FDA_PAPER_ALERT
# Find the list view (largest SysListView32)
lvs = [c for c in kids if "SysListView32" in c["class"]]
print("list views:", [hex(c["hwnd"]) for c in lvs])
if lvs:
    lv = lvs[-1]
    er = wt.RECT()
    user32.GetWindowRect(lv["hwnd"], ctypes.byref(er))
    cx = (er.left + er.right) // 2
    cy = (er.top + er.bottom) // 2
    print("list center:", cx, cy)

    # foreground dialog, click into list
    user32.SetForegroundWindow(DLG)
    time.sleep(0.5)

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

    # type FDA_PAPER_ALERT (list jump-search)
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
    time.sleep(1)

    # Enter to open
    key_event(0x0D, True)
    key_event(0x0D, False)
    print("Enter sent")
    time.sleep(5)

# 4. check editor title
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == PID and "XScript" in t.value:
        out.append((hex(hwnd), t.value[:70]))
    return True
user32.EnumWindows(cb2, 0)
print("editor:", out)
