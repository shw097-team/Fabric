# -*- coding: utf-8 -*-
"""FINAL P24: dump XQSensor/SensorList.sqlite fully — FDAPaper strategies + state."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
print("cols:", cols)
rows = c.execute("SELECT * FROM SensorList").fetchall()
print(f"rows: {len(rows)}")
for r in rows:
    d = dict(zip(cols, r))
    print("---")
    for k in ("Name", "ScriptName", "ScriptID", "Enable", "SymbolGroupType", "SymbolName",
              "Symbols", "Freq", "LastExecuteTime", "TriggerCount", "Status", "ModifiedTime",
              "ScriptType", "TriggerMode", "Product", "SourceType"):
        if k in d:
            print(f"  {k}: {str(d[k])[:60]}")
c.close()
