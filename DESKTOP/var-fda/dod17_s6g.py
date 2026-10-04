# -*- coding: utf-8 -*-
"""DoD-17 S6g: get 自訂 screen coords via uia bounding_rect -> cua background click at point."""
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

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and w.window_text().startswith("策略雷達"):
            radar_hwnd = w.handle
            break
    except Exception:
        pass
ru = du.window(handle=radar_hwnd)
customs = [e for e in ru.descendants(control_type="TreeItem") if (e.window_text() or "").strip() == "自訂"]
print("自訂:", len(customs))
if customs:
    rect = customs[0].rectangle()
    print("rect:", rect)
    cx = rect.left + (rect.width() // 2)
    cy = rect.top + (rect.height() // 2)
    print("click point:", cx, cy)
    # cua background click at coordinate
    def cua(tool, args, timeout=40):
        rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
        return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}
    res = cua("click", {"pid": PID, "coordinate": [cx, cy], "delivery_mode": "background"})
    print("cua click:", json.dumps(res, ensure_ascii=False)[:120])
    time.sleep(3)

# verify — read grid cell texts via uia (data grid cells may be in 17002 or custom)
try:
    grid = ru.child_window(control_id=17001, class_name="MFCGridCtrl")
    texts = [el.window_text().strip() for el in grid.descendants() if el.window_text().strip() and len(el.window_text().strip()) < 50]
    fda = [t for t in texts if "FDA" in t or "FDAPaper" in t]
    print("grid all:", texts[:20])
    print("FDA in grid:", fda)
except Exception as e:
    print("grid err:", str(e)[:60])
