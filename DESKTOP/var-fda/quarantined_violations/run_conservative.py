# -*- coding: utf-8 -*-
"""Conservative path: open editor (UIA menu), click 加入雷達 (pixel), 
SendInput name into dialog, click 加入. DB readback at end.
"""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import subprocess
import time
from pathlib import Path

user32 = ctypes.windll.user32
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 7580
MAIN = 13764744


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:120]}


def ws(pid, wid, mx=400, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def win32_children(hwnd):
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


def sendinput_click(x, y):
    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [("dx", wt.DWORD), ("dy", wt.DWORD), ("mouseData", wt.DWORD),
                    ("dwFlags", wt.DWORD), ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]
    class INPUT(ctypes.Structure):
        _fields_ = [("type", wt.DWORD), ("mi", MOUSEINPUT)]
    def me(flags):
        extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
        mi = MOUSEINPUT(0, 0, 0, flags, 0, extra)
        inp = INPUT(0, mi)
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    user32.SetCursorPos(x, y)
    time.sleep(0.2)
    me(0x0002)
    me(0x0004)


def sendinput_type(text):
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", wt.WORD), ("wScan", wt.WORD), ("dwFlags", wt.DWORD),
                    ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]
    class INPUT2(ctypes.Structure):
        _fields_ = [("type", wt.DWORD), ("ki", KEYBDINPUT)]
    def ke(vk, down):
        extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
        ki = KEYBDINPUT(vk, 0, 0 if down else 0x0002, 0, extra)
        inp = INPUT2(1, ki)
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT2))
    for ch in text:
        vk = ord(ch.upper())
        ke(vk, True)
        ke(vk, False)
        time.sleep(0.04)


def sendinput_enter():
    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [("wVk", wt.WORD), ("wScan", wt.WORD), ("dwFlags", wt.DWORD),
                    ("time", wt.DWORD), ("dwExtraInfo", ctypes.POINTER(wt.ULONG))]
    class INPUT2(ctypes.Structure):
        _fields_ = [("type", wt.DWORD), ("ki", KEYBDINPUT)]
    def ke(vk, down):
        extra = ctypes.cast(ctypes.pointer(ctypes.c_ulong(0)), ctypes.POINTER(wt.ULONG))
        ki = KEYBDINPUT(vk, 0, 0 if down else 0x0002, 0, extra)
        inp = INPUT2(1, ki)
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT2))
    ke(0x0D, True)
    ke(0x0D, False)


# ============ 1. open editor ============
s0 = ws(PID, MAIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN, 400)
ed = find(s1.get("elements", []), "XScript 編輯器", "MenuItem")
if not ed:
    print("FAIL: XScript 編輯器 menu")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": ed.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

ewin = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID and "XScript 編輯器" in (w.get("title") or ""):
        ewin = w
        break
print("editor:", hex(ewin["window_id"]) if ewin else None)
if not ewin:
    raise SystemExit(2)
EWID = ewin["window_id"]

# ============ 2. click 加入雷達 (UIA pixel) ============
s2 = ws(PID, EWID, 600, 35)
add_btn = find(s2.get("elements", []), "加入雷達", "Button")
if not add_btn:
    # fallback: 策略雷達 button
    add_btn = find(s2.get("elements", []), "策略雷達", "Button")
print("add btn label:", repr((add_btn.get("label") or "")[:12]) if add_btn else None)
if add_btn:
    f = add_btn.get("frame") or {}
    x = f.get("x", 0) + f.get("w", 0) // 2
    y = f.get("y", 0) + f.get("h", 0) // 2
    print("click at:", x, y)
    cua("click", {"pid": PID, "x": x, "y": y, "delivery_mode": "foreground"})
    time.sleep(5)

# ============ 3. dialog handling ============
dls = find_dialog("新增策略雷達")
print("dialog:", [hex(d) for d in dls])
if not dls:
    print("no dialog; dump windows")
    raise SystemExit(2)
DLG = dls[0]

kids = win32_children(DLG)
edits = [c for c in kids if c["class"] == "Edit"]
add_btn2 = next((c for c in kids if "加入" in c["text"]), None)
print("edits:", [hex(c["hwnd"]) for c in edits])
print("加入:", hex(add_btn2["hwnd"]) if add_btn2 else None)

if edits:
    edit = edits[0]["hwnd"]
    user32.SetForegroundWindow(DLG)
    time.sleep(0.8)
    er = wt.RECT()
    user32.GetWindowRect(edit, ctypes.byref(er))
    cx = (er.left + er.right) // 2
    cy = (er.top + er.bottom) // 2
    print("edit center:", cx, cy)
    sendinput_click(cx, cy)
    time.sleep(0.6)
    sendinput_type("FDA_PAPER_ALERT")
    time.sleep(0.8)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edit, t, 128)
    print("name now:", repr(t.value[:40]))

if add_btn2:
    user32.PostMessageW(add_btn2["hwnd"], 0x00F5, 0, 0)
    print("clicked 加入")
    time.sleep(6)

# ============ 4. DB readback ============
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite")
rows = c.execute("SELECT Name, Enable, LastExecuteTime, ScriptType FROM XSTradeStrategyDTO WHERE Name LIKE '%FDA%'").fetchall()
print("DB:", rows)
c.close()
