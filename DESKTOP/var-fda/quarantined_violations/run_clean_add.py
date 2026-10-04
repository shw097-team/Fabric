# -*- coding: utf-8 -*-
"""Clean restart path: open editor, load FDA_PAPER_ALERT, click 加入雷達 (UIA pixel)."""
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
PID = 12260
MAIN = 331604


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


# 1. 策略(D) menu
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
print("editor:", ewin.get("window_id") if ewin else None)
if not ewin:
    raise SystemExit(2)
EWID = ewin.get("window_id")
EHWND = ewin.get("window_id")  # cua window_id == hwnd for XQ

# 2. load FDA_PAPER_ALERT — check tree; if not visible, use 開啟 dialog? 
# Try: click 加入雷達 directly (active script may auto-load on open)
s2 = ws(PID, EWID, 600, 35)
add_btn = find(s2.get("elements", []), "加入雷達", "Button")
print("加入雷達 btn frame:", add_btn.get("frame") if add_btn else None)
f = add_btn.get("frame") or {}
x = f.get("x", 0) + f.get("w", 0) // 2
y = f.get("y", 0) + f.get("h", 0) // 2
print("click at:", x, y)
cua("click", {"pid": PID, "x": x, "y": y, "delivery_mode": "foreground"})
time.sleep(5)

dls = find_dialog()
print("dialog:", [hex(d) for d in dls])
if dls:
    DLG = dls[0]
    kids = win32_children(DLG)
    edits = [c for c in kids if c["class"] == "Edit"]
    print("edits:", [hex(c["hwnd"]) for c in edits])
    # try WM_SETTEXT via SendMessageW (may work now)
    if edits:
        name = "FDA_PAPER_ALERT"
        buf = ctypes.create_unicode_buffer(name)
        r = user32.SendMessageW(edits[0]["hwnd"], 0x000C, 0, ctypes.cast(buf, ctypes.c_void_p))
        print("sendmsg settext:", r)
        time.sleep(1)
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(edits[0]["hwnd"], t, 128)
        print("name now:", repr(t.value[:40]))
