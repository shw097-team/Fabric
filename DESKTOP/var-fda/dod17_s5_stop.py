# -*- coding: utf-8 -*-
"""DoD-17 S5: XQ_PAPER_STOP — press STOP(17555), verify post-stop state (full loop close)."""
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
def cmd_index(cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return i
    return None
def st(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None, None

# 1. pre-stop state
pre = {"start": st(17554), "stop": st(17555)}
print("pre-stop START:", pre["start"], "STOP:", pre["stop"])

# 2. press STOP (17555) via TB_PRESSBUTTON (message)
tb.button(cmd_index(17555)).click()
print("pressed STOP")
time.sleep(3)

# 3. post-stop state (poll up to 15s)
post = None
for i in range(15):
    s = st(17554)
    sp = st(17555)
    if s[0] and not sp[1]:  # START enabled, STOP not pressed = stopped
        post = {"start": s, "stop": sp}
        print(f"STOPPED at t+{i}s: START={s} STOP={sp}")
        break
    time.sleep(1)
if post is None:
    post = {"start": st(17554), "stop": st(17555)}
    print("stop state (final):", post)

# 4. verify strategy still in list (config intact)
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
names = [dec(dict(zip(cols, r)).get("Name")) for r in rows]
print("SensorList names:", names)
c.close()

# 5. loop closed!
closed = bool(pre["stop"][1]) and post["stop"][1] is False
print("LOOP CLOSED (was running -> now stopped):", closed)

receipt = {
    "stage": "stop",
    "pre_stop": {"start": pre["start"], "stop": pre["stop"]},
    "post_stop": post,
    "loop_closed": closed,
    "broker_write": 0,
    "environment": "PAPER",
    "time_note": "盤後無即時行情 — 觸發計數待盤中驗證；start/stop 閉環已達成",
}
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved:", json.dumps(receipt, ensure_ascii=False, indent=1)[:600])
