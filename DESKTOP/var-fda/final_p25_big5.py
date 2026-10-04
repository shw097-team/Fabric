# -*- coding: utf-8 -*-
"""FINAL P25: read SensorList with big5 text decoding — FDAPaper strategies."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes  # raw bytes, decode manually

cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
def dec(b):
    if isinstance(b, bytes):
        try:
            return b.decode("cp950", errors="replace")
        except Exception:
            return repr(b)
    return str(b)

rows = c.execute("SELECT * FROM SensorList").fetchall()
print(f"rows: {len(rows)}")
for r in rows:
    d = dict(zip(cols, r))
    name = dec(d.get("Name"))
    if "FDAPaper" in name:
        print("=== FOUND:", name)
        for k in ("ID", "Name", "SensorType", "SourceType", "ScriptType", "ScriptName",
                  "Symbol", "Freq", "TriggerSetting", "Script_ID", "CreateTime", "LastUpdateTime"):
            if k in d:
                print(f"  {k}: {dec(d[k])[:80]}")
print("--- all names:")
for r in rows:
    d = dict(zip(cols, r))
    print("  ", dec(d.get("Name"))[:50])
c.close()
