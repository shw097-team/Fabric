# -*- coding: utf-8 -*-
"""FINAL P26: raw dump of SensorList rows — find where FDAPaperProbe lives."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
print("cols:", cols)

rows = c.execute("SELECT * FROM SensorList").fetchall()
for ri, r in enumerate(rows):
    print(f"=== row {ri} ({len(r)} vals) ===")
    for i, v in enumerate(r):
        if v is not None:
            b = v if isinstance(v, bytes) else str(v).encode()
            try:
                t = b.decode("cp950", errors="replace")
            except Exception:
                t = repr(b)
            if t.strip():
                print(f"  [{i}] {cols[i]}: {t[:70]}")
c.close()
