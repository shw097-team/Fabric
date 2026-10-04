# -*- coding: utf-8 -*-
"""SCREEN-STATE CHECK V2 (SSC-V2) — fixed route, user-mandated upgrade 2026-08-14.
Fixes vs V1 (FAR root-cause):
1. DYNAMIC XQ pid: find via DAQXQLITEMainWnd class (no hardcoded pid — V1 bug 23456/22384)
2. FULL window scan: ALL XQ top-level incl HIDDEN + title-less + popup (V1 visible-only)
3. NEEDS_CONFIRM marking: dialogs with 確定/關閉/是/加入 buttons flagged prominently
4. Buttons listed for EVERY XQ window (V1 pid-mismatch made the button section always empty)
Read-only; zero mouse/focus. Run FIRST on ANY anomaly; never retry blind."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import os
os.add_dll_directory(r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages\pywin32_system32")

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
u = ctypes.windll.user32

# ---- 1. DYNAMIC XQ pid via main window class ----
def find_xq_pid():
    pids = set()
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        cls = ctypes.create_unicode_buffer(128)
        u.GetClassNameW(hwnd, cls, 128)
        if "DAQXQLITEMainWnd" in cls.value:
            pid = wt.DWORD()
            u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            pids.add(pid.value)
        return True
    u.EnumWindows(cb, 0)
    return sorted(pids)

XQ_PIDS = find_xq_pid()
XQ_PID = XQ_PIDS[0] if XQ_PIDS else None
stamp = time.strftime("%H%M%S")
print(f"=== SCREEN-STATE CHECK V2 {stamp} (XQ pid={XQ_PID} {'DYNAMIC' if XQ_PID else 'NOT_RUNNING'}) ===")
if not XQ_PID:
    print("XQ NOT RUNNING — restart XQ first; automation state unknown. STOP.")
    sys.exit(1)

# ---- 2. ALL top-level windows (any process, visible only w/ titles) ----
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

# ---- 3. ALL XQ windows (INCL HIDDEN + title-less) with buttons + NEEDS_CONFIRM ----
print(f"\n=== XQ windows detail (pid={XQ_PID}, incl HIDDEN) ===")
CONFIRM_WORDS = ("確定", "關閉", "是", "加入", "OK", "取消")
xq_wins = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb3(hwnd, lparam):
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        xq_wins.append(hwnd)
    return True
u.EnumWindows(cb3, 0)

needs_confirm = []
for h in xq_wins:
    vis = u.IsWindowVisible(h)
    t = ctypes.create_unicode_buffer(150)
    u.GetWindowTextW(h, t, 150)
    cls = ctypes.create_unicode_buffer(60)
    u.GetClassNameW(h, cls, 60)
    r = wt.RECT()
    u.GetWindowRect(h, ctypes.byref(r))
    w, hh = r.right - r.left, r.bottom - r.top
    # buttons
    btns = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb4(ch, lp):
        tc = ctypes.create_unicode_buffer(100)
        u.GetWindowTextW(ch, tc, 100)
        cc = ctypes.create_unicode_buffer(50)
        u.GetClassNameW(ch, cc, 50)
        if "Button" in cc.value:
            btns.append(tc.value)
        return True
    u.EnumChildWindows(h, cb4, 0)
    btns = [b for b in btns if b.strip()]
    flag = "VIS" if vis else "hid"
    marker = ""
    if btns and any(w_ in "".join(btns) for w_ in CONFIRM_WORDS):
        marker = "  ⚠️ NEEDS_CONFIRM"
        needs_confirm.append((h, t.value[:40], btns))
    line = f"  {flag} {hex(h)} [{cls.value[:26]}] '{t.value[:42]}' {w}x{hh}"
    if btns:
        line += f" | buttons: {btns[:6]}"
    line += marker
    print(line)

print(f"\n=== NEEDS_CONFIRM dialogs: {len(needs_confirm)} ===")
for h, t, btns in needs_confirm:
    print(f"  ⚠️ {hex(h)} '{t}' → 應 PostMessage BM_CLICK: {btns[:4]}")

# ---- 4. AX tree (cua) ----
try:
    r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
    d = json.loads(r.stdout.decode("utf-8", errors="replace")) if r.stdout else {}
    print("\n=== AX windows (cua) ===")
    for w in d.get("windows", []):
        if w.get("pid") == XQ_PID:
            print(f"  wid={w.get('window_id')} '{ (w.get('title') or '')[:45]}'")
except Exception as e:
    print("\nAX tree err:", str(e)[:60])

# ---- 5. screenshot for record ----
try:
    shot = Path.home() / "AppData/Local/hermes/attachments" / f"screen_state_v2_{stamp}.png"
    r = subprocess.run([CUA, "call", "capture", json.dumps({"pid": XQ_PID})], capture_output=True, timeout=30, env=ENV)
    print("\ncapture rc:", r.returncode, "out:", r.stdout.decode("utf-8", "replace")[:100] if r.stdout else "(none)")
except Exception as e:
    print("\ncapture err:", str(e)[:60])

print("\nGUIDANCE: anomaly → check NEEDS_CONFIRM first; if any, BM_CLICK its buttons, then re-run the op. XQ is rarely frozen — usually an unseen popup.")
