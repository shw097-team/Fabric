# -*- coding: utf-8 -*-
"""Zero-UIA path: open editor via menu, Ctrl+O, Win32 警示 tab, keyboard select FDA_PAPER_ALERT.
Step 1: open XScript editor via 策略(D) menu (UIA menu click - proven ok on fresh daemon).
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
PID = 14200
MAIN = 1247428


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


# 1. 策略(D) -> XScript 編輯器
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
