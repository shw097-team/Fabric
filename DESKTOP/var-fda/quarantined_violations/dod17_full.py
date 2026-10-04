# -*- coding: utf-8 -*-
"""DoD-17 FULL CLOSURE: XQ_RADAR_OPEN -> PAPER_CONFIG -> START -> STATUS -> STOP -> PERSISTENCE.
All message-only (zero mouse). Uses community xq_alert.py semantics.
"""
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
PID = 23456
u = ctypes.windll.user32
log = []
receipt = {"stages": {}}


def logm(s):
    log.append(s)
    print(s)


# ---------- S1: RADAR OPEN (cua background menu) ----------
r = subprocess.run([CUA, "get_accessibility_tree"], capture_output=True, timeout=40, env=ENV)
d = json.loads(r.stdout.decode("utf-8", errors="replace")) if r.stdout else {}
main_wid = next((w["window_id"] for w in d.get("windows", [])
                 if w.get("pid") == PID and (w.get("title") or "").startswith("XQ全球贏家(個人版)")), None)
logm(f"S1 main_wid={main_wid}")
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
        radar = next((e for e in s1.get("elements", []) if "策略雷達" in (e.get("label") or "")), None)
        if radar:
            cua("click", {"pid": PID, "element_token": radar.get("element_token"), "snapshot_id": s1.get("snapshot_id")})
            logm("S1 clicked 策略雷達")
            time.sleep(6)

# find radar + 說明 dialog
radar_hwnd = None
dlg_hwnd = None
for w in Desktop(backend="win32").windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if "策略雷達" in t and "說明" not in t:
                radar_hwnd = w.handle
            elif "開放體驗說明" in t:
                dlg_hwnd = w.handle
    except Exception:
        pass
logm(f"S1 radar={hex(radar_hwnd) if radar_hwnd else None} helpdlg={hex(dlg_hwnd) if dlg_hwnd else None}")

# dismiss 說明 dialog (Enter — proven safe pattern)
if dlg_hwnd:
    dlg = Desktop(backend="win32").window(handle=dlg_hwnd)
    try:
        dlg.set_focus()
        dlg.send_keystrokes("{ENTER}")
        logm("S1 dismissed help dialog (Enter)")
        time.sleep(3)
    except Exception as e:
        logm(f"S1 dismiss err: {str(e)[:60]}")
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
def cmd_en(cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return bool(tb.button(i).info.fsState & 4)
    return None

# ---------- S2: PAPER CONFIG ----------
tb.button(cmd_index(17551)).click()  # NEW
time.sleep(4)
DLG = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "新增策略雷達" in w.window_text():
            DLG = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if DLG is None:
    logm("FAIL: 新增策略雷達 dialog not found")
    receipt["stages"]["config"] = False
    json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    raise SystemExit(2)

NAME = "FDAPaperClosure" + time.strftime("%H%M%S")
DLG.child_window(control_id=17500, class_name="Edit").set_edit_text(NAME)
time.sleep(0.4)
DLG.child_window(control_id=17203, class_name="Button").click()
time.sleep(3.5)
chooser = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇使用腳本" in w.window_text():
            chooser = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if chooser:
    du = Desktop(backend="uia")
    cu = du.window(handle=chooser.handle)
    tv = cu.descendants(control_type="Tree")[0]
    custom = [i for i in tv.descendants(control_type="TreeItem") if i.window_text().startswith("自訂")]
    if custom:
        custom[0].expand()
        time.sleep(1)
    target = [i for i in tv.descendants(control_type="TreeItem") if i.window_text() == "FDA_PAPER_ALERT"]
    logm(f"S2 FDA_PAPER_ALERT nodes: {len(target)}")
    if target:
        target[0].select()
        time.sleep(0.4)
        ok = [b for b in cu.descendants(control_type="Button") if "確定" in b.window_text()]
        if ok:
            ok[0].click()
            time.sleep(2.5)

DLG = d32.window(handle=DLG.handle)
DLG.child_window(control_id=17610, class_name="Button").click()
time.sleep(3.5)
PROD = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇商品" in w.window_text():
            PROD = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if PROD:
    PROD.child_window(control_id=741, class_name="Edit").set_edit_text("2330")
    time.sleep(0.3)
    PROD.child_window(control_id=802, class_name="Button").click()
    time.sleep(2)
    pu = Desktop(backend="uia").window(handle=PROD.handle)
    items = [i for i in pu.descendants(control_type="ListItem") if i.window_text() == "2330"]
    if items:
        items[0].select()
        time.sleep(0.4)
        PROD.child_window(control_id=803, class_name="Button").click()
        time.sleep(0.5)
        PROD.child_window(control_id=1, class_name="Button").click()
        time.sleep(2)

DLG.child_window(control_id=17035, class_name="ComboBox").select("單次洗價模式")
time.sleep(0.4)
config_rb = {
    "name": DLG.child_window(control_id=17500, class_name="Edit").window_text(),
    "script": DLG.child_window(control_id=17202, class_name="Edit").window_text(),
    "product": DLG.child_window(control_id=17107, class_name="Static").window_text(),
    "trigger": DLG.child_window(control_id=17035, class_name="ComboBox").window_text(),
}
logm(f"S2 CONFIG READBACK: {json.dumps(config_rb, ensure_ascii=False)}")
receipt["stages"]["config"] = config_rb
receipt["strategy_name"] = NAME

# ---------- S3: START (加入) ----------
DLG.child_window(control_id=1, class_name="Button").click()
logm("S3 clicked 加入")
time.sleep(2)
for attempt in range(8):
    time.sleep(1)
    notices = []
    for w in d32.windows(class_name="#32770"):
        try:
            if w.is_visible() and w.handle not in (radar_hwnd, DLG.handle):
                t = w.window_text()
                if t.strip() and "新增策略" not in t:
                    notices.append((w.handle, t))
        except Exception:
            pass
    if notices:
        for h, t in notices:
            logm(f"S3 notice: '{t[:30]}'")
            nw = d32.window(handle=h)
            btns = nw.children(class_name="Button")
            if btns:
                btns[0].click()
                logm(f"S3 dismissed ({btns[0].window_text()[:10]})")
                time.sleep(1.5)
        break
time.sleep(2)

# verify running: START disabled/STOP enabled (community: running = STOP enabled)
start_en = cmd_en(17554)
stop_en = cmd_en(17555)
logm(f"S3 after 加入: START en={start_en} STOP en={stop_en}")
running = bool(stop_en) or not bool(start_en)
logm(f"S3 running={running}")
receipt["stages"]["start"] = {"start_enabled": start_en, "stop_enabled": stop_en, "running": running}

# ---------- S4: STATUS (wait wash / verify persisted) ----------
time.sleep(8)  # allow wash cycle
start_en = cmd_en(17554)
stop_en = cmd_en(17555)
logm(f"S4 status: START en={start_en} STOP en={stop_en}")

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
persisted = []
for r in rows:
    d = dict(zip(cols, r))
    nm = dec(d.get("Name"))
    if NAME in nm:
        persisted.append({k: dec(v)[:40] for k, v in d.items() if k in ("Name", "ScriptName", "Symbol", "Freq", "TriggerSetting", "Enable")})
c.close()
logm(f"S4 persisted: {json.dumps(persisted, ensure_ascii=False)}")
receipt["stages"]["status"] = {"start_enabled": start_en, "stop_enabled": stop_en, "persisted": persisted}

# ---------- S5: STOP ----------
if stop_en or not start_en:  # running
    tb.button(cmd_index(17555)).click()
    logm("S5 pressed STOP")
    time.sleep(4)
start_en2 = cmd_en(17554)
stop_en2 = cmd_en(17555)
logm(f"S5 post-stop: START en={start_en2} STOP en={stop_en2}")
loop_closed = bool(persisted) and (not bool(stop_en2))
receipt["stages"]["stop"] = {"start_enabled": start_en2, "stop_enabled": stop_en2}
receipt["loop_closed"] = loop_closed
receipt["broker_write"] = 0
receipt["environment"] = "PAPER"
receipt["surface"] = "XQ 策略雷達 PAPER runtime (build 260811, 盤中量化交易模組 subscribed)"
receipt["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
logm(f"LOOP CLOSED: {loop_closed}")
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
logm("receipt saved")
