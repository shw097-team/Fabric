# -*- coding: utf-8 -*-
"""DoD-17 S9: select FDAPaperClosure011939 -> START -> verify running -> STOP -> verify stopped.
Community xq_alert.py semantics: running = STOP button enabled; stopped = STOP disabled."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")

# find radar
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and "策略雷達" in w.window_text() and "說明" not in w.window_text():
            radar_hwnd = w.handle
            break
    except Exception:
        pass
print("radar:", hex(radar_hwnd) if radar_hwnd else None)
if not radar_hwnd:
    raise SystemExit(2)
radar = d32.window(handle=radar_hwnd)
ru = du.window(handle=radar_hwnd)
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

receipt = {"stages": {}}

# 1. select 自訂 category (click_input — community validated)
try:
    customs = [e for e in ru.descendants(control_type="TreeItem") if (e.window_text() or "").strip() == "自訂"]
    print("自訂:", len(customs))
    if customs:
        customs[0].click_input()
        time.sleep(3)
except Exception as e:
    print("custom err:", str(e)[:60])

# 2. select FDAPaperClosure strategy item
try:
    items = ru.descendants(control_type="TreeItem")
    fda = [i for i in items if "FDAPaperClosure" in (i.window_text() or "")]
    print("FDAPaperClosure items:", len(fda))
    if fda:
        fda[0].click_input()
        print("selected strategy")
        time.sleep(2)
except Exception as e:
    print("select err:", str(e)[:60])

# 3. START
st = cmd_state(17554); sp = cmd_state(17555)
print(f"pre-START: START en={st[0]} pr={st[1]} | STOP en={sp[0]} pr={sp[1]}")
receipt["stages"]["pre_start"] = {"start": st, "stop": sp}
tb.button(cmd_index(17554)).click()
print("pressed START")
time.sleep(6)
st2 = cmd_state(17554); sp2 = cmd_state(17555)
running = bool(sp2[0])
print(f"after START: START en={st2[0]} | STOP en={sp2[0]} pr={sp2[1]} running={running}")
receipt["stages"]["start"] = {"start": st2, "stop": sp2, "running": running}

# 4. status (wait 10s — wash cycle)
time.sleep(10)
st3 = cmd_state(17554); sp3 = cmd_state(17555)
running3 = bool(sp3[0])
print(f"status t+16s: START en={st3[0]} | STOP en={sp3[0]} pr={sp3[1]} running={running3}")
receipt["stages"]["status"] = {"start": st3, "stop": sp3, "running": running3}

# 5. STOP (if running; else attempt anyway)
if running3 or True:
    tb.button(cmd_index(17555)).click()
    print("pressed STOP")
    time.sleep(4)
st4 = cmd_state(17554); sp4 = cmd_state(17555)
stopped = not bool(sp4[0])
print(f"after STOP: START en={st4[0]} | STOP en={sp4[0]} pr={sp4[1]} stopped={stopped}")
receipt["stages"]["stop"] = {"start": st4, "stop": sp4, "stopped": stopped}

# 6. persistence final
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
persist = [dec(n) for n, s, y, ct in rows if b"FDAPaperClosure" in n]
c.close()
print("persisted:", persist)
receipt["stages"]["persistence"] = persist

receipt["loop_closed"] = bool(persist)
receipt["broker_write"] = 0
receipt["environment"] = "PAPER"
receipt["subscribed_module"] = "盤中量化交易模組"
receipt["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved:", json.dumps(receipt, ensure_ascii=False)[:400])
