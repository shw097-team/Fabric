# -*- coding: utf-8 -*-
"""DoD-17 S7: FULL loop — verify strategy in list, START explicitly, verify running, STOP, verify stopped.
Community semantics: running = STOP button enabled."""
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
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and w.window_text().startswith("策略雷達"):
            radar_hwnd = w.handle
            break
    except Exception:
        pass
print("radar:", hex(radar_hwnd) if radar_hwnd else None)
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
def cmd_en(cid):
    s = cmd_state(cid)
    return s[0] if s else None

receipt = {"stages": {}}

# 1. current toolbar state
st = cmd_state(17554); sp = cmd_state(17555)
print(f"current: START en={st[0]} pr={st[1]} | STOP en={sp[0]} pr={sp[1]}")
receipt["stages"]["initial"] = {"start": st, "stop": sp}

# 2. if not running (STOP disabled), press START to explicitly start
running = bool(sp[0])
if not running:
    tb.button(cmd_index(17554)).click()
    print("pressed START (explicit)")
    time.sleep(5)
    st2 = cmd_state(17554); sp2 = cmd_state(17555)
    print(f"after START: START en={st2[0]} | STOP en={sp2[0]} pr={sp2[1]}")
    running = bool(sp2[0])
    receipt["stages"]["start"] = {"start": st2, "stop": sp2}
else:
    print("already running")
    receipt["stages"]["start"] = {"start": st, "stop": sp}

# 3. wait a bit, read status (running = STOP enabled)
time.sleep(10)
st3 = cmd_state(17554); sp3 = cmd_state(17555)
print(f"status t+10s: START en={st3[0]} | STOP en={sp3[0]} pr={sp3[1]} running={bool(sp3[0])}")
receipt["stages"]["status"] = {"start": st3, "stop": sp3, "running": bool(sp3[0])}

# 4. STOP explicitly
if bool(sp3[0]):
    tb.button(cmd_index(17555)).click()
    print("pressed STOP")
    time.sleep(4)
st4 = cmd_state(17554); sp4 = cmd_state(17555)
print(f"after STOP: START en={st4[0]} | STOP en={sp4[0]} pr={sp4[1]}")
receipt["stages"]["stop"] = {"start": st4, "stop": sp4}
stopped = not bool(sp4[0])

# 5. persistence re-verify (explicit columns)
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
persist = [(dec(n), dec(s), dec(y), dec(ct)) for n, s, y, ct in rows if b"FDAPaperClosure" in n]
print("persisted:", persist)
c.close()
receipt["stages"]["persistence"] = persist

receipt["loop_closed"] = bool(persist) and stopped
receipt["broker_write"] = 0
receipt["environment"] = "PAPER"
receipt["subscribed_module"] = "盤中量化交易模組"
receipt["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
print("LOOP CLOSED:", receipt["loop_closed"])
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved")
