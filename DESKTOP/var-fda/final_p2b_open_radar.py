# -*- coding: utf-8 -*-
"""FINAL P2b: open radar via cua-driver background menu clicks (proven on this XQ)."""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 25256

# find main window id via cua
r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
d = json.loads(r.stdout.decode("utf-8", errors="replace"))
MAIN = None
for w in d.get("windows", []):
    if w.get("pid") == PID:
        MAIN = w.get("window_id")
        print("main wid:", MAIN)
        break
if not MAIN:
    print("FAIL: main not found via cua")
    raise SystemExit(2)


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:100]}


def ws(pid, wid, mx=300, depth=25):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


s0 = ws(PID, MAIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
print("策略(D):", menu.get("element_index") if menu else None)
if not menu:
    print("no 策略(D); sample labels:")
    for e in s0.get("elements", [])[:30]:
        print("  ", e.get("role"), repr((e.get("label") or "")[:20]))
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN, 500)
radar = find(s1.get("elements", []), "策略雷達", "MenuItem")
print("策略雷達:", radar.get("element_index") if radar else None)
if radar:
    cua("click", {"pid": PID, "element_token": radar.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id")})
    print("clicked 策略雷達")
    time.sleep(6)
    # verify radar window via win32
    from pywinauto import Desktop
    d32 = Desktop(backend="win32")
    rw = d32.window(title_re="策略雷達.*")
    print("radar exists:", rw.exists(timeout=3))
    if rw.exists(timeout=1):
        rw.wait("visible enabled", timeout=10)
        print("RADAR:", rw.window_text()[:50], hex(rw.handle))
