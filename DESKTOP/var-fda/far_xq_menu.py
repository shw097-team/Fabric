# -*- coding: utf-8 -*-
"""FAR R3: cua-driver read XQ main window — find 設定/我要購買 menu (fresh UIA)."""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 7312
MAIN = 0x150d58


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:80]}


def ws(pid, wid, mx=500, depth=35):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


s = ws(PID, MAIN, 500, 35)
els = s.get("elements", [])
print("elements:", len(els))
for e in els:
    lab = (e.get("label") or "")
    if any(k in lab for k in ("設定", "購買", "模組", "權限", "系統", "策略")):
        print(e.get("element_index"), "|", e.get("role"), "|", repr(lab[:30]))
