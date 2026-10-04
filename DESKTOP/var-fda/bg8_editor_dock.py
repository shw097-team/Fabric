# -*- coding: utf-8 -*-
"""bg v8: open editor (background), inspect 45001/45002 type-filter buttons."""
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
MAIN = 983362


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


# open editor
s0 = ws(PID, MAIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if menu:
    cua("click", {"pid": PID, "element_token": menu.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
    time.sleep(3)
s1 = ws(PID, MAIN, 400)
ed = find(s1.get("elements", []), "XScript 編輯器", "MenuItem")
if ed:
    cua("click", {"pid": PID, "element_token": ed.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id")})
    time.sleep(6)

ewin = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID and "XScript 編輯器" in (w.get("title") or ""):
        ewin = w
        break
print("editor:", ewin.get("window_id") if ewin else None)
EWID = ewin["window_id"]

# inspect dock buttons 45001/45002 + tree area
s2 = ws(PID, EWID, 800, 40)
els = s2.get("elements", [])
for e in els:
    if e.get("id") in (45001, 45002, 45041):
        print("id", e.get("id"), "| role", e.get("role"), "| label", repr((e.get("label") or "")[:20]),
              "| frame", (e.get("frame") or {}))
# full tree lines 36-50
md = s2.get("tree_markdown") or ""
lines = md.splitlines()
for i, l in enumerate(lines[36:52], 36):
    print(i, l[:100])
