# -*- coding: utf-8 -*-
"""DoD-17 S1: XQ_RADAR_OPEN — open 策略雷達 (cua background menu) + dismiss 說明 dialog (message)."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 2416

# 1. open radar via cua background menu clicks (proven pattern, zero mouse)
r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
d = json.loads(r.stdout.decode("utf-8", errors="replace")) if r.stdout else {}
main_wid = next((w["window_id"] for w in d.get("windows", []) if w.get("pid") == PID and (w.get("title") or "").startswith("XQ全球贏家(個人版)")), None)
print("main wid:", main_wid)
if not main_wid:
    print("FAIL: main window not found")
    raise SystemExit(2)

def cua(tool, args, timeout=40):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}

s0 = cua("get_window_state", {"pid": PID, "window_id": main_wid, "max_elements": 300, "max_depth": 25})
menu = next((e for e in s0.get("elements", []) if "策略(D)" in (e.get("label") or "")), None)
print("策略(D):", menu.get("element_index") if menu else None)
if not menu:
    print("FAIL: 策略 menu")
    raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"), "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = cua("get_window_state", {"pid": PID, "window_id": main_wid, "max_elements": 500, "max_depth": 25})
radar = next((e for e in s1.get("elements", []) if "策略雷達" in (e.get("label") or "")), None)
print("策略雷達:", radar.get("element_index") if radar else None)
if radar:
    cua("click", {"pid": PID, "element_token": radar.get("element_token"), "snapshot_id": s1.get("snapshot_id")})
    print("clicked 策略雷達")
    time.sleep(6)

# 2. dismiss 開放體驗說明 dialog (win32, message only) + find radar window
d32_win = ctypes.windll.user32
radar_hwnd = None
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    d32_win.GetWindowTextW(hwnd, t, 256)
    if "策略雷達" in t.value:
        radar_hwnd = hwnd
        return False
    return True
d32_win.EnumWindows(cb, 0)
print("radar hwnd:", hex(radar_hwnd) if radar_hwnd else None)

# 3. dismiss any 開放體驗說明 dialog (Enter via message? use 我知道了 button if found)
# scan for #32770 dialogs with 策略雷達 in title
dialogs = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    d32_win.GetWindowTextW(hwnd, t, 256)
    cls = ctypes.create_unicode_buffer(64)
    d32_win.GetClassNameW(hwnd, cls, 64)
    if "策略雷達" in t.value and cls.value == "#32770":
        dialogs.append(hwnd)
    return True
d32_win.EnumWindows(cb2, 0)
print("radar dialogs:", [hex(h) for h in dialogs])
