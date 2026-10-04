# -*- coding: utf-8 -*-
"""DoD-17 S17: cua background click 內容 tab (from uia tab rect) -> verify strategy list tab."""
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
PID = 23408
d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x32112a
ru = du.window(handle=RADAR)

# 1. get 內容 tab rect via uia (read-only)
try:
    tabs = ru.descendants(control_type="TabItem")
    print("tabs:", [t.window_text().strip() for t in tabs if t.window_text().strip()])
    content = next((t for t in tabs if t.window_text().strip() == "內容"), None)
    if content:
        r = content.rectangle()
        print("內容 tab rect:", r)
        cx, cy = r.left + (r.width() // 2), r.top + (r.height() // 2)
        print("click:", cx, cy)
        # cua background click
        rr = subprocess.run([CUA, "call", "click", json.dumps({"pid": PID, "coordinate": [cx, cy], "delivery_mode": "background"})],
                            capture_output=True, timeout=40, env=ENV)
        print("cua click:", rr.stdout.decode("utf-8", "replace")[:120] if rr.stdout else "(empty)")
        time.sleep(3)
except Exception as e:
    print("tab err:", str(e)[:70])

# 2. verify — radar texts now show strategy list?
u = ctypes.windll.user32
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cid = u.GetDlgCtrlID(ch)
    if t.value.strip() and cid in (33041, 17629):
        out.append((hex(ch), cid, t.value[:45]))
    return True
u.EnumChildWindows(RADAR, cb, 0)
print("=== after 內容 click ===")
for h, cid, t in out:
    print(f"  {h} cid={cid} '{t}'")
