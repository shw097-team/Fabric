# -*- coding: utf-8 -*-
"""DoD-17 S4: XQ_PAPER_STATUS_READBACK — wait wash complete, read 執行紀錄/觸發 + DB."""
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

# 1. poll toolbar until START enabled and STOP not pressed (wash complete)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def st(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None, None

wash_done = False
for i in range(60):  # up to 60s
    se, sp = st(17554)
    ste, stp = st(17555)
    if se and not stp:  # START enabled AND STOP not pressed = wash complete
        wash_done = True
        print(f"WASH COMPLETE at t+{i}s (START en={se} STOP pr={stp})")
        break
    time.sleep(1)
if not wash_done:
    print(f"wash timeout: START en={se} pr={sp} | STOP en={ste} pr={stp}")

# 2. read 執行紀錄 tab (17002 MFCGridCtrl) via uia — rows with timestamps
du = Desktop(backend="uia")
ru = du.window(handle=RADAR)
try:
    tabs = ru.descendants(control_type="TabItem")
    for t in tabs:
        if "執行紀錄" in t.window_text():
            t.select()
            time.sleep(1.5)
            break
    grid = ru.child_window(control_id=17002, class_name="MFCGridCtrl")
    print("grid 17002 exists:", grid.exists(timeout=2))
    if grid.exists(timeout=1):
        texts = []
        for row in grid.descendants():
            try:
                tx = row.window_text()
                if tx.strip():
                    texts.append(tx.strip()[:60])
            except Exception:
                pass
        print("執行紀錄 rows:", texts[:10])
except Exception as e:
    print("record tab err:", str(e)[:80])

# 3. DB: SensorList FDAPaperProbe state + any sensor log
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
for r in rows:
    d = dict(zip(cols, r))
    if "FDAPaperProbe" in dec(d.get("Name")):
        print("DB:", dec(d.get("Name")), "| Script:", dec(d.get("ScriptName")),
              "| Freq:", dec(d.get("Freq")), "| Trigger:", dec(d.get("TriggerSetting")),
              "| CreateTime:", dec(d.get("CreateTime")))
c.close()

# 4. check XSSensorProxyClient / XQSensorSvc logs for run evidence
import glob
for lg in glob.glob(r"C:\SysJust\XQLite\Log\XQSensor*.log.enc") + glob.glob(r"C:\SysJust\XQLite\Log\XSSensor*.log.enc"):
    print("sensor log:", lg.split("\\")[-1])

json.dump({"stage": "status_readback", "wash_done": wash_done,
           "start_state": st(17554), "stop_state": st(17555)},
          open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("receipt updated (status stage)")
