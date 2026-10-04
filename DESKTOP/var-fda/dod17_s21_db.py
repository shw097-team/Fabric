# -*- coding: utf-8 -*-
"""DoD-17 S21: SensorList full row for FDAPaperFinal020037 — LastUpdateTime/Enable/execution traces."""
import sqlite3
import time

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
cols = [col[1] for col in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)

for r in rows:
    d = dict(zip(cols, r))
    nm = dec(d.get("Name"))
    if "FDAPaperFinal" in nm:
        print(f"=== {nm} ===")
        for k in ("Name", "ScriptName", "Symbol", "Freq", "TriggerSetting", "CreateTime",
                  "LastUpdateTime", "ScriptVersion", "TotalBar", "MaxBarBack", "CalcType",
                  "Comment", "PushCheck", "ForceCalcMode"):
            print(f"  {k}: {dec(d.get(k))!r}")

# also check Sensor DB for execution log tables
import glob
print("\n=== sensor-related DBs ===")
for db2 in glob.glob(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\**\*.sqlite", recursive=True):
    try:
        c2 = sqlite3.connect(db2, timeout=4)
        tabs = [t[0] for t in c2.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        if any("log" in t.lower() or "run" in t.lower() or "exec" in t.lower() for t in tabs):
            print(f"  {db2.split(chr(92))[-1]}: {tabs[:8]}")
        c2.close()
    except Exception:
        pass
c.close()
print("\nnow:", time.strftime("%Y-%m-%d %H:%M:%S"))
