# -*- coding: utf-8 -*-
"""FAR v20: open radar via cua-driver background menu clicks (proven pattern)."""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 8100
MAIN = 983362


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:120]}


def ws(pid, wid, mx=300, depth=25):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


# 策略(D) menu -> 策略雷達
s0 = ws(PID, MAIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
print("策略(D):", menu.get("element_index") if menu else None)
if not menu:
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN, 400)
radar_item = find(s1.get("elements", []), "策略雷達", "MenuItem")
print("策略雷達:", radar_item.get("element_index") if radar_item else None)
if radar_item:
    cua("click", {"pid": PID, "element_token": radar_item.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id")})
    print("clicked 策略雷達")
    time.sleep(6)
else:
    # try 開放體驗 variant
    radar_item2 = find(s1.get("elements", []), "開放體驗", "MenuItem")
    print("開放體驗:", radar_item2.get("element_index") if radar_item2 else None)
    if radar_item2:
        cua("click", {"pid": PID, "element_token": radar_item2.get("element_token"),
                      "snapshot_id": s1.get("snapshot_id")})
        time.sleep(6)

# check radar window via cua
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if w.get("pid") == PID:
        print("WIN:", repr((w.get("title") or "")[:50]), "| wid:", w.get("window_id"))
