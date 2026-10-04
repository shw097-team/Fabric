# -*- coding: utf-8 -*-
"""DoD-17 bg v1: open editor (background only), verify FDA_PAPER_ALERT in DB.
NO foreground, NO SendInput, NO SetCursorPos.
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
PID = 21964
MAIN = 657684


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


# verify FDA_PAPER_ALERT in DB first (Sensor table)
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite")
rows = c.execute("SELECT Name, CompileStatus, CompileMsg, LastCompileTime FROM Sensor WHERE Name='FDA_PAPER_ALERT'").fetchall()
c.close()
print("DB FDA_PAPER_ALERT:", rows)

# 1. 策略(D) menu -> XScript 編輯器 (background clicks)
s0 = ws(PID, MAIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu")
    raise SystemExit(2)
r = cua("click", {"pid": PID, "element_token": menu.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
print("策略(D) click:", (r.get("delivery") or {}).get("mode", "?"), (r.get("effect") or "?"))
time.sleep(3)
s1 = ws(PID, MAIN, 400)
ed = find(s1.get("elements", []), "XScript 編輯器", "MenuItem")
if not ed:
    print("FAIL: XScript 編輯器 menu")
    raise SystemExit(2)
r2 = cua("click", {"pid": PID, "element_token": ed.get("element_token"),
                   "snapshot_id": s1.get("snapshot_id")})
print("XScript 編輯器 click:", (r2.get("delivery") or {}).get("mode", "?"), (r2.get("effect") or "?"))
time.sleep(6)

ewin = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID and "XScript 編輯器" in (w.get("title") or ""):
        ewin = w
        break
print("editor:", hex(ewin["window_id"]) if ewin else None)
