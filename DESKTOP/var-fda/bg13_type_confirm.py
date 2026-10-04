# -*- coding: utf-8 -*-
"""bg v13: dialog 0x100ba0 -> PostMessage 警示 -> cua type_text bg px name -> PostMessage 確認."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import time
from pathlib import Path

user32 = ctypes.windll.user32
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 8100
DLG = 0x100ba0


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:120]}


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
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
confirm_btn = next((c for c in kids if c["text"] == "確認" and c["class"] == "Button"), None)
edits = [c for c in kids if c["class"] == "Edit"]
print("警示:", hex(alert_btn["hwnd"]) if alert_btn else None)
print("確認:", hex(confirm_btn["hwnd"]) if confirm_btn else None)
print("edits:", [hex(c["hwnd"]) for c in edits])

if alert_btn:
    user32.PostMessageW(alert_btn["hwnd"], 0x00F5, 0, 0)
    print("post 警示")
    time.sleep(1)

# type name via cua type_text background px
if edits:
    edit = edits[0]["hwnd"]
    er = wt.RECT()
    user32.GetWindowRect(edit, ctypes.byref(er))
    dr = wt.RECT()
    user32.GetWindowRect(DLG, ctypes.byref(dr))
    cx = (er.left - dr.left) + (er.right - er.left) // 2
    cy = (er.top - dr.top) + (er.bottom - er.top) // 2
    print("name edit local:", cx, cy)
    r = cua("type_text", {"pid": PID, "window_id": DLG, "x": cx, "y": cy,
                          "text": "FDA_PAPER_ALERT2", "delivery_mode": "background"})
    print("type_text:", (r.get("delivery") or {}).get("mode", "?"), (r.get("effect") or "?"))
    time.sleep(2)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edit, t, 128)
    print("name now:", repr(t.value[:40]))

if confirm_btn:
    user32.PostMessageW(confirm_btn["hwnd"], 0x00F5, 0, 0)
    print("post 確認")
    time.sleep(5)

# check editor title + DB
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t2 = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t2, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == PID and "XScript" in t2.value:
        out.append((hex(hwnd), t2.value[:70]))
    return True
user32.EnumWindows(cb2, 0)
print("editor:", out)

import sqlite3
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite")
rows = c.execute("SELECT Name, CompileStatus FROM Sensor WHERE Name LIKE 'FDA%'").fetchall()
c.close()
print("DB:", rows)
