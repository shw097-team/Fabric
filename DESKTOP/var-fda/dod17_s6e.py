# -*- coding: utf-8 -*-
"""DoD-17 S6e: cua-driver click 自訂 in radar (deeper depth, background) then verify grid."""
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
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}

# deeper scan
s = cua("get_window_state", {"pid": PID, "window_id": RADAR_WID, "max_elements": 800, "max_depth": 40})
els = s.get("elements", [])
print("elements:", len(els))
for e in els:
    lab = (e.get("label") or "").strip()
    if lab in ("自訂", "系統", "全部", "執行中") or "FDAPaper" in lab:
        print(e.get("element_index"), "|", e.get("role"), "|", repr(lab[:30]))
