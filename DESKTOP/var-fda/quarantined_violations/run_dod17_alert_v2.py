# -*- coding: utf-8 -*-
"""DoD-17 alert script: 檔案(F) -> 新增(N) -> dialog. Background clicks only."""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 20252
EWIN = 35720078


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:150]}


def ws(pid, wid, mx=400, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


# 檔案(F) menu (background click — proven to work on this editor)
s0 = ws(PID, EWIN, 300)
fmenu = find(s0.get("elements", []), "檔案(F)", "MenuItem")
print("檔案(F):", fmenu.get("element_index") if fmenu else None)
if not fmenu:
    print("FAIL: no 檔案 menu")
    raise SystemExit(2)
r = cua("click", {"pid": PID, "element_token": fmenu.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
print("檔案 click:", (r.get("delivery") or r.get("effect") or "?")[:40])
time.sleep(3)

s1 = ws(PID, EWIN, 500)
new_item = find(s1.get("elements", []), "新增(N)", "MenuItem")
print("新增(N):", new_item.get("element_index") if new_item else None)
if new_item:
    r2 = cua("click", {"pid": PID, "element_token": new_item.get("element_token"),
                       "snapshot_id": s1.get("snapshot_id")})
    print("新增 click:", (r2.get("delivery") or r2.get("effect") or "?")[:40])
    time.sleep(4)
else:
    print("新增(N) not in tree; trying Ctrl+N")
    cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "n"], "delivery_mode": "foreground"})
    time.sleep(4)

# list all windows after
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID:
        print("WIN:", repr((w.get("title") or "")[:50]), "| wid:", w.get("window_id"), "| cls:", w.get("class") or "")
