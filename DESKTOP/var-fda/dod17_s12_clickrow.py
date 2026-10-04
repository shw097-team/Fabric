# -*- coding: utf-8 -*-
"""DoD-17 S12 (fixed-route): cua background click 自訂 tree node -> cua background click grid row 1.
Read grid state after each step (uia read-only). Zero mouse-stealing."""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 23456
RADAR_WID = 528328

def cua(tool, args, timeout=40):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
    if not rr.stdout:
        time.sleep(2)
        rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}

# 1. get radar state — find 自訂 element
s = cua("get_window_state", {"pid": PID, "window_id": RADAR_WID, "max_elements": 200, "max_depth": 30})
els = s.get("elements", [])
print("radar elements:", len(els))
custom = next((e for e in els if (e.get("label") or "").strip() == "自訂"), None)
print("自訂 element:", custom.get("element_index") if custom else None)
if custom:
    r = cua("click", {"pid": PID, "element_token": custom.get("element_token"), "snapshot_id": s.get("snapshot_id")})
    print("cua click 自訂:", json.dumps(r, ensure_ascii=False)[:150])
    time.sleep(3)

# 2. click grid first row (pixel from geometry: grid L1265 T511 -> row1 ~T525)
# cua background click at coordinate (window-relative? use screen absolute via element or coordinate)
r2 = cua("click", {"pid": PID, "coordinate": [1800, 530], "delivery_mode": "background"})
print("cua click grid row:", json.dumps(r2, ensure_ascii=False)[:150])
time.sleep(3)

# 3. read radar state again — any strategy labels?
s2 = cua("get_window_state", {"pid": PID, "window_id": RADAR_WID, "max_elements": 300, "max_depth": 30})
labels = [(e.get("label") or "") for e in s2.get("elements", [])]
fda = [l for l in labels if "FDAPaper" in l or "FDA" in l]
print("FDA labels:", fda[:8])
print("all labels sample:", [l for l in labels if l.strip()][:15])
