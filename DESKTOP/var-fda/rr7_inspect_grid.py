# -*- coding: utf-8 -*-
"""Inspect radar grid 17001 current selection via uia (read-only) + cua AX tree."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
CUA = r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe"
u = ctypes.windll.user32
XQ_PID = 21500

def cua(tool, args, timeout=60):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else None

# cua AX tree of radar
info = cua("get_accessibility_tree", {}, 90)
wid = None
for w in (info or {}).get("windows", []):
    if w.get("pid") == XQ_PID and "策略雷達" in (w.get("title") or ""):
        wid = w.get("window_id")
        print("radar wid:", wid)
        break

if wid:
    ws = cua("get_window_state", {"pid": XQ_PID, "window_id": wid}, 90)
    els = (ws or {}).get("elements", [])
    print("radar elements:", len(els))
    # find grid/strategy items
    for e in els[:60]:
        name = e.get("name", "")
        role = e.get("role", "")
        if name or role in ("DataItem", "ListItem", "TreeItem"):
            print(f"  [{role}] {name[:40]}")
