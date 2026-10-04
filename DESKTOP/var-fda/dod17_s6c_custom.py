# -*- coding: utf-8 -*-
"""DoD-17 S6c: click 自訂 category via cua background -> read strategy grid via uia."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 23456

# find radar wid in cua tree
r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
d = json.loads(r.stdout.decode("utf-8", errors="replace")) if r.stdout else {}
radar_wid = None
for w in d.get("windows", []):
    t = w.get("title") or ""
    if w.get("pid") == PID and t.startswith("策略雷達"):
        radar_wid = w["window_id"]
        break
print("radar wid:", radar_wid)
if not radar_wid:
    raise SystemExit(2)

def cua(tool, args, timeout=40):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}

# read radar state -> find 自訂 tree item -> click
s = cua("get_window_state", {"pid": PID, "window_id": radar_wid, "max_elements": 600, "max_depth": 30})
els = s.get("elements", [])
print("elements:", len(els))
custom = next((e for e in els if (e.get("label") or "").strip() == "自訂"), None)
print("自訂:", custom.get("element_index") if custom else None)
if custom:
    cua("click", {"pid": PID, "element_token": custom.get("element_token"), "snapshot_id": s.get("snapshot_id")})
    print("clicked 自訂")
    time.sleep(3)

# read radar state again -> strategy grid texts
s2 = cua("get_window_state", {"pid": PID, "window_id": radar_wid, "max_elements": 600, "max_depth": 30})
labels = [e.get("label") or "" for e in s2.get("elements", [])]
hits = [l for l in labels if "FDAPaper" in l or "FDA" in l]
print("FDA hits:", hits[:10])
# also print grid area labels (strategy names)
grid_hits = [l.strip() for l in labels if l.strip() and len(l.strip()) < 40 and any(k in l for k in ("FDAPaper", "複製", "台積電", "2330"))]
print("grid:", grid_hits[:10])
