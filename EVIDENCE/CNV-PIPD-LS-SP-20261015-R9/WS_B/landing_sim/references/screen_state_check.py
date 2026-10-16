# -*- coding: utf-8 -*-
"""screen_state_check.py — FIXED ROUTE on ANY automation anomaly (user-mandated 2026-08-14).
Read-only: dumps visible windows (all classes), per-XQ-window child button labels,
cua AX tree, screenshot attempt. Zero mouse, zero focus change.
Run FIRST whenever an operation shows anomaly — do NOT retry before checking."""
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
u = ctypes.windll.user32
XQ_PID = None
stamp = time.strftime("%H%M%S")
print(f"=== SCREEN-STATE CHECK {stamp} ===")

# detect XQ pid from any visible DAQXQLITEMainWnd
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def find_xq(hwnd, lparam):
    global XQ_PID
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(hwnd, cls, 64)
    if cls.value == "DAQXQLITEMainWnd":
        pid = wt.DWORD()
        u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        XQ_PID = pid.value
        return False
    return True
u.EnumWindows(find_xq, 0)
print(f"XQ pid: {XQ_PID}")

# 1. ALL visible top-level windows (flag XQ)
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    t = ctypes.create_unicode_buffer(256)
    u.GetWindowTextW(hwnd, t, 256)
    cls = ctypes.create_unicode_buffer(64)
    u.GetClassNameW(hwnd, cls, 64)
    if u.IsWindowVisible(hwnd) and t.value.strip():
        out.append((hwnd, pid.value, cls.value, t.value))
    return True
u.EnumWindows(cb, 0)
print(f"visible windows: {len(out)}")
for h, p, c, t in out:
    tag = "XQ" if p == XQ_PID else "  "
    print(f"  [{tag}] {hex(h)} pid={p} | {c[:28]} | '{t[:48]}'")

# 2. per-XQ-window child button labels (catches 確定/關閉/加入 confirms of ANY class)
print("\n=== XQ windows with buttons ===")
for h, p, c, t in out:
    if p != XQ_PID:
        continue
    btns = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb2(ch, lp):
        tc = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(ch, tc, 128)
        cc = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(ch, cc, 64)
        if "Button" in cc.value and tc.value.strip():
            btns.append((hex(ch), tc.value[:22]))
        return True
    u.EnumChildWindows(h, cb2, 0)
    print(f"  {hex(h)} '{t[:40]}' buttons: {btns[:8]}")

# 3. cua AX tree (fresh window ids)
try:
    r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
    d = json.loads(r.stdout.decode("utf-8", errors="replace")) if r.stdout else {}
    print("\n=== AX windows (cua) ===")
    for w in d.get("windows", []):
        if XQ_PID and w.get("pid") == XQ_PID:
            print(f"  wid={w.get('window_id')} '{ (w.get('title') or '')[:45]}'")
except Exception as e:
    print("\nAX tree err:", str(e)[:60])

# 4. screenshot attempt (record only)
try:
    shot = Path.home() / "AppData/Local/hermes/attachments" / f"screen_state_{stamp}.png"
    r = subprocess.run([CUA, "call", "capture", json.dumps({"pid": XQ_PID})], capture_output=True, timeout=30, env=ENV)
    print("\ncapture rc:", r.returncode)
except Exception as e:
    print("\ncapture err:", str(e)[:60])
