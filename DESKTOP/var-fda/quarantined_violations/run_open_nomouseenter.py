# -*- coding: utf-8 -*-
"""Open dialog via real-mouse clicks only (NO Enter key - crash trigger).
1. editor open (UIA menu)
2. Ctrl+O -> dialog
3. SendInput click 警示 tab
4. SendInput click list, type FDA_PAPER_ALERT
5. SendInput click 確認 button (not Enter!)
"""
import ctypes
import ctypes.wintypes as wt
import json
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
    time.sleep(0.3)
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
        time.sleep(0.05)


# ===== 1. open editor =====
s0 = ws(PID, MAIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN, 400)
ed = find(s1.get("elements", []), "XScript 編輯器", "MenuItem")
cua("click", {"pid": PID, "element_token": ed.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)
ewin = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID and "XScript 編輯器" in (w.get("title") or ""):
        ewin = w
        break
print("editor:", hex(ewin["window_id"]) if ewin else None)
EWID = ewin["window_id"]

# ===== 2. Ctrl+O =====
cua("hotkey", {"pid": PID, "window_id": EWID, "keys": ["ctrl", "o"], "delivery_mode": "foreground"})
time.sleep(4)
dls = find_dialog("開啟")
print("開啟 dialog:", [hex(d) for d in dls])
if not dls:
    raise SystemExit(2)
DLG = dls[0]

# ===== 3. enumerate + click 警示 tab with real mouse =====
kids = win32_children(DLG)
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
confirm_btn = next((c for c in kids if c["text"] == "確認" and c["class"] == "Button"), None)
lvs = [c for c in kids if "SysListView32" in c["class"]]
print("警示 tab:", hex(alert_btn["hwnd"]) if alert_btn else None)
print("確認:", hex(confirm_btn["hwnd"]) if confirm_btn else None)
print("lists:", [hex(c["hwnd"]) for c in lvs])

user32.SetForegroundWindow(DLG)
time.sleep(0.6)

# click 警示 tab (real mouse)
ar = wt.RECT()
user32.GetWindowRect(alert_btn["hwnd"], ctypes.byref(ar))
sendinput_click((ar.left + ar.right) // 2, (ar.top + ar.bottom) // 2)
print("clicked 警示 tab at", (ar.left + ar.right) // 2, (ar.top + ar.bottom) // 2)
time.sleep(2)

# click into list (last list view)
if lvs:
    lv = lvs[-1]
    lr = wt.RECT()
    user32.GetWindowRect(lv["hwnd"], ctypes.byref(lr))
    sendinput_click((lr.left + lr.right) // 2, (lr.top + lr.bottom) // 2)
    time.sleep(0.6)
    # type name (list jump search)
    sendinput_type("FDA_PAPER_ALERT")
    print("typed FDA_PAPER_ALERT")
    time.sleep(1.5)

# ===== 4. click 確認 (real mouse, NO Enter) =====
if confirm_btn:
    cr = wt.RECT()
    user32.GetWindowRect(confirm_btn["hwnd"], ctypes.byref(cr))
    sendinput_click((cr.left + cr.right) // 2, (cr.top + cr.bottom) // 2)
    print("clicked 確認")
    time.sleep(6)

# ===== 5. check editor title =====
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
