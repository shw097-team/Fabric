# -*- coding: utf-8 -*-
"""DoD-17: reopen radar, load strategy list (28 built-in strategies exist),
locate 均線黃金交叉, verify UI shows it, then prepare start.
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 23488
MAIN_WIN = 199968
STRAT_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(pid, wid, mx=500, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


# 1. open 策略(D) -> 策略雷達(開放體驗)(L)
s0 = ws(PID, MAIN_WIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN_WIN, 400)
radar = find(s1.get("elements", []), "策略雷達", "MenuItem")
if not radar:
    print("FAIL: radar menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": radar.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

rw = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if "策略雷達" in (w.get("title") or ""):
        rw = w
        break
print("radar win:", rw.get("window_id") if rw else None, "|", repr((rw.get("title") or "")[:40]) if rw else "")
if not rw:
    raise SystemExit(2)
RWID = rw.get("window_id")

# 2. dump radar tree — look for strategy list
s2 = ws(PID, RWID, 800, 40)
md = s2.get("tree_markdown") or ""
print("radar tree lines:", len(md.splitlines()))
# print whole tree (compact)
for l in md.splitlines():
    print(l[:105])
