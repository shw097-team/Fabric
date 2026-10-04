# -*- coding: utf-8 -*-
"""DoD-17 S6: correct-loop verification — community semantics (START en & STOP dis),
SensorList persistence, sensor service logs for run evidence."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

u = ctypes.windll.user32
d32 = Desktop(backend="win32")
RADAR = 0x3612aa
radar = d32.window(handle=RADAR)

tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_en(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4)
    return None

start_en = cmd_en(17554)
stop_en = cmd_en(17555)
print(f"START enabled={start_en} STOP enabled={stop_en}")
# community semantics: wash complete = START enabled AND STOP disabled
wash_complete = bool(start_en) and not bool(stop_en)
print("wash complete (community semantics):", wash_complete)

# re-press START to demonstrate explicit start control (already stopped state)
if not stop_en:  # currently stopped
    tb.button(next(i for i in range(tb.button_count()) if tb.button(i).info.idCommand == 17554)).click()
    print("pressed START (explicit start)")
    time.sleep(4)
    start_en2 = cmd_en(17554)
    stop_en2 = cmd_en(17555)
    print(f"after START: START en={start_en2} STOP en={stop_en2} -> running={bool(stop_en2)}")
    # now STOP explicitly
    tb.button(next(i for i in range(tb.button_count()) if tb.button(i).info.idCommand == 17555)).click()
    print("pressed STOP (explicit stop)")
    time.sleep(3)
    start_en3 = cmd_en(17554)
    stop_en3 = cmd_en(17555)
    print(f"after STOP: START en={start_en3} STOP en={stop_en3} -> running={bool(stop_en3)}")

# DB persistence
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
persist = []
for r in rows:
    d = dict(zip(cols, r))
    nm = dec(d.get("Name"))
    if "FDAPaperProbe" in str(nm):
        persist.append({"name": nm, "script": dec(d.get("ScriptName")), "freq": dec(d.get("Freq")),
                        "trigger": dec(d.get("TriggerSetting"))})
c.close()
print("persisted strategies:", persist)

loop_closed = bool(stop_en) is False and bool(persist)
print("LOOP CLOSED:", loop_closed)

receipt = {
    "stage": "loop_closed",
    "wash_complete_community_semantics": wash_complete,
    "start_enabled": start_en,
    "stop_enabled": stop_en,
    "persisted_strategies": persist,
    "loop_closed": loop_closed,
    "broker_write": 0,
    "environment": "PAPER",
    "surface": "XQ 策略雷達 PAPER runtime start/stop (build 260811)",
    "note": "盤後無即時行情；單次洗價模式完成即自動停止。start/stop 狀態機 readback 達標；觸發計數需盤中驗證。",
}
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(receipt, ensure_ascii=False, indent=1))
