# -*- coding: utf-8 -*-
"""DoD-17 FINAL (fixed-route, crash-recovered): open radar -> START -> running? -> STOP -> stopped?
Pure messages only. cua background for radar open."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 23408
u = ctypes.windll.user32
receipt = {"stages": {}}

def logm(s):
    print(s)

# ---------- 1. open radar (cua background menu) ----------
r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
d = json.loads(r.stdout.decode("utf-8", errors="replace")) if r.stdout else {}
main_wid = next((w["window_id"] for w in d.get("windows", [])
                 if w.get("pid") == PID and (w.get("title") or "").startswith("XQ全球贏家(個人版)")), None)
logm(f"main_wid={main_wid}")
def cua(tool, args, timeout=40):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
    if not rr.stdout:
        time.sleep(2)
        rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout, env=ENV)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else {}

if main_wid:
    s0 = cua("get_window_state", {"pid": PID, "window_id": main_wid, "max_elements": 300, "max_depth": 25})
    menu = next((e for e in s0.get("elements", []) if "策略(D)" in (e.get("label") or "")), None)
    if menu:
        cua("click", {"pid": PID, "element_token": menu.get("element_token"), "snapshot_id": s0.get("snapshot_id")})
        time.sleep(3)
        s1 = cua("get_window_state", {"pid": PID, "window_id": main_wid, "max_elements": 500, "max_depth": 25})
        radar_m = next((e for e in s1.get("elements", []) if "策略雷達" in (e.get("label") or "")), None)
        if radar_m:
            cua("click", {"pid": PID, "element_token": radar_m.get("element_token"), "snapshot_id": s1.get("snapshot_id")})
            logm("clicked 策略雷達")
            time.sleep(6)

# find radar hwnd (win32)
radar_hwnd = None
help_hwnd = None
for w in Desktop(backend="win32").windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if t.startswith("策略雷達") and "說明" not in t:
                radar_hwnd = w.handle
            elif "開放體驗說明" in t:
                help_hwnd = w.handle
    except Exception:
        pass
logm(f"radar={hex(radar_hwnd) if radar_hwnd else None} help={hex(help_hwnd) if help_hwnd else None}")

# dismiss help dialog — find its button via EnumChildWindows (any class), PostMessage BM_CLICK
if help_hwnd:
    btns = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb2(ch, lp):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(ch, cls, 64)
        if "Button" in cls.value:
            btns.append(ch)
        return True
    u.EnumChildWindows(help_hwnd, cb2, 0)
    logm(f"help dialog buttons: {len(btns)}")
    if btns:
        u.PostMessageW(btns[0], 0x00F5, 0, 0)  # BM_CLICK
        logm("dismissed help (BM_CLICK)")
        time.sleep(3)
    else:
        # CEF dialog — click 我知道了 via uia (pattern, no mouse)
        try:
            du = Desktop(backend="uia")
            hw = du.window(handle=help_hwnd)
            btns_u = [b for b in hw.descendants(control_type="Button") if "知道" in (b.window_text() or "")]
            logm(f"uia 我知道了: {len(btns_u)}")
            if btns_u:
                btns_u[0].click()
                logm("clicked 我知道了 (uia)")
                time.sleep(3)
        except Exception as e:
            logm(f"uia dismiss err: {str(e)[:60]}")

receipt["stages"]["radar_open"] = bool(radar_hwnd)
if not radar_hwnd:
    logm("FAIL: radar not open")
    json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    raise SystemExit(2)

d32 = Desktop(backend="win32")
radar = d32.window(handle=radar_hwnd)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_index(cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return i
    return None
def cmd_state(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None, None

# ---------- 2. START / running / STOP loop ----------
st = cmd_state(17554); sp = cmd_state(17555)
logm(f"PRE: START en={st[0]} | STOP en={sp[0]} pr={sp[1]}")
receipt["stages"]["pre"] = {"start": st, "stop": sp}

tb.button(cmd_index(17554)).click()
logm("pressed START")
time.sleep(6)
st2 = cmd_state(17554); sp2 = cmd_state(17555)
running = bool(sp2[0])
logm(f"t+6s: START en={st2[0]} | STOP en={sp2[0]} pr={sp2[1]} running={running}")
receipt["stages"]["start"] = {"start": st2, "stop": sp2, "running": running}

time.sleep(10)
st3 = cmd_state(17554); sp3 = cmd_state(17555)
running3 = bool(sp3[0])
logm(f"t+16s: START en={st3[0]} | STOP en={sp3[0]} pr={sp3[1]} running={running3}")
receipt["stages"]["status"] = {"start": st3, "stop": sp3, "running": running3}

tb.button(cmd_index(17555)).click()
logm("pressed STOP")
time.sleep(4)
st4 = cmd_state(17554); sp4 = cmd_state(17555)
stopped = not bool(sp4[0])
logm(f"t+20s: START en={st4[0]} | STOP en={sp4[0]} pr={sp4[1]} stopped={stopped}")
receipt["stages"]["stop"] = {"start": st4, "stop": sp4, "stopped": stopped}

# persistence
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
persist = [dec(r[0]) for r in rows if b"FDAPaperClosure" in r[0]]
c.close()
logm(f"persisted: {persist}")
receipt["stages"]["persistence"] = persist

receipt["broker_write"] = 0
receipt["environment"] = "PAPER"
receipt["subscribed_module"] = "盤中量化交易模組"
receipt["crash_recovered"] = True
receipt["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
logm("receipt saved")
