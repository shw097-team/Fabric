# -*- coding: utf-8 -*-
"""DoD-17 correct path (root cause fixed): create ALERT-type script.
XS editor -> 檔案(F) menu -> 新增(N) -> 警示腳本 dialog -> name -> ret=1 ->
save -> compile -> right-click 加入策略雷達 -> 加入 (auto-start) -> green light.
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 20252
MAIN_WIN = 3019316
DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:150]}


def ws(pid, wid, mx=500, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


# 1. open 策略(D) -> XScript 編輯器(E)
s0 = ws(PID, MAIN_WIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN_WIN, 400)
ed = find(s1.get("elements", []), "XScript 編輯器", "MenuItem")
if not ed:
    print("FAIL: XScript 編輯器 menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": ed.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

ed_win = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if "XScript 編輯器" in (w.get("title") or ""):
        ed_win = w
        break
print("editor win:", ed_win.get("window_id") if ed_win else None)
if not ed_win:
    raise SystemExit(2)
EWIN = ed_win.get("window_id")

# 2. 檔案(F) menu -> 新增(N)
s2 = ws(PID, EWIN, 300)
fmenu = find(s2.get("elements", []), "檔案(F)", "MenuItem")
if not fmenu:
    print("FAIL: 檔案 menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": fmenu.get("element_token"),
              "snapshot_id": s2.get("snapshot_id")})
time.sleep(3)
s3 = ws(PID, EWIN, 400)
new_item = find(s3.get("elements", []), "新增(N)", "MenuItem")
print("新增(N):", new_item.get("element_index") if new_item else None)
if new_item:
    cua("click", {"pid": PID, "element_token": new_item.get("element_token"),
                  "snapshot_id": s3.get("snapshot_id")})
    time.sleep(4)
else:
    # fallback Ctrl+N
    cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "n"], "delivery_mode": "foreground"})
    time.sleep(4)

# 3. look for 新增腳本 dialog
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID:
        print("WIN:", repr((w.get("title") or "")[:50]), "| wid:", w.get("window_id"), "| cls:", w.get("class") or "")
