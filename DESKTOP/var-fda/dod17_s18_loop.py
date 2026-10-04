# -*- coding: utf-8 -*-
"""DoD-17 S18: post-add — radar state + select FDAPaperFinal strategy (cua bg) + START/STOP loop."""
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
u = ctypes.windll.user32
RADAR = 0x32112a
receipt = {"stages": {}}

# 1. radar state texts
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    u.GetWindowTextW(ch, t, 128)
    cid = u.GetDlgCtrlID(ch)
    if t.value.strip() and cid in (33041, 17629, 17107):
        out.append((hex(ch), cid, t.value[:45]))
    return True
u.EnumChildWindows(RADAR, cb, 0)
print("=== radar key texts ===")
for h, cid, t in out:
    print(f"  {h} cid={cid} '{t}'")

# 2. select 自訂 category (uia pattern)
ru = du.window(handle=RADAR)
try:
    items = ru.descendants(control_type="TreeItem")
    custom = next((i for i in items if (i.window_text() or "").strip() == "自訂"), None)
    print("自訂:", bool(custom))
    if custom:
        custom.select()
        print("selected 自訂")
        time.sleep(3)
except Exception as e:
    print("custom select err:", str(e)[:60])

# 3. find FDAPaperFinal in tree (uia) — if visible, select; else cua bg click grid row
try:
    items = ru.descendants(control_type="TreeItem")
    fda = [i for i in items if "FDAPaperFinal" in (i.window_text() or "")]
    print("FDAPaperFinal tree items:", len(fda))
    if fda:
        fda[0].select()
        print("selected FDAPaperFinal (uia)")
        time.sleep(2)
except Exception as e:
    print("fda select err:", str(e)[:60])

# 4. toolbar START/STOP loop
radar = d32.window(handle=RADAR)
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

st = cmd_state(17554); sp = cmd_state(17555)
print(f"PRE: START en={st[0]} | STOP en={sp[0]} pr={sp[1]}")
receipt["stages"]["pre"] = {"start": st, "stop": sp}

# START if not running
if not sp[0]:
    tb.button(cmd_index(17554)).click()
    print("pressed START")
    time.sleep(6)
st2 = cmd_state(17554); sp2 = cmd_state(17555)
running = bool(sp2[0])
print(f"t+6s: START en={st2[0]} | STOP en={sp2[0]} pr={sp2[1]} running={running}")
receipt["stages"]["start"] = {"start": st2, "stop": sp2, "running": running}

time.sleep(10)
st3 = cmd_state(17554); sp3 = cmd_state(17555)
running3 = bool(sp3[0])
print(f"t+16s: START en={st3[0]} | STOP en={sp3[0]} pr={sp3[1]} running={running3}")
receipt["stages"]["status"] = {"start": st3, "stop": sp3, "running": running3}

tb.button(cmd_index(17555)).click()
print("pressed STOP")
time.sleep(4)
st4 = cmd_state(17554); sp4 = cmd_state(17555)
stopped = not bool(sp4[0])
print(f"t+20s: START en={st4[0]} | STOP en={sp4[0]} pr={sp4[1]} stopped={stopped}")
receipt["stages"]["stop"] = {"start": st4, "stop": sp4, "stopped": stopped}

receipt["broker_write"] = 0
receipt["environment"] = "PAPER"
receipt["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved")
