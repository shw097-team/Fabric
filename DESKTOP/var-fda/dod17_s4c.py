# -*- coding: utf-8 -*-
"""DoD-17 S4c: full row of FDAPaperClosure011939 + sensor logs + radar 執行紀錄."""
import ctypes
import ctypes.wintypes as wt
import glob
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

# 1. full row
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [col[1] for col in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
for r in rows:
    d = dict(zip(cols, r))
    if "FDAPaperClosure" in dec(d.get("Name")):
        for k in ("Name", "SensorType", "ScriptType", "ScriptName", "Symbol", "Freq",
                  "TriggerSetting", "CreateTime", "ScriptVersion", "LastUpdateTime"):
            print(f"  {k}: {dec(d.get(k))!r}")
c.close()

# 2. sensor logs (recent activity = execution evidence)
print("\n=== sensor logs (today) ===")
for lg in sorted(glob.glob(r"C:\SysJust\XQLite\Log\XSSensor*20260814*")):
    import os
    print(f"  {lg.split(chr(92))[-1]} ({os.path.getsize(lg)} bytes)")

# 3. radar 執行紀錄 tab via uia (read-only)
d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
radar = d32.window(handle=0x80fc8)
ru = du.window(handle=0x80fc8)
try:
    tabs = ru.descendants(control_type="TabItem")
    print("\ntabs:", [t.window_text() for t in tabs if t.window_text().strip()][:8])
except Exception as e:
    print("tabs err:", str(e)[:60])
