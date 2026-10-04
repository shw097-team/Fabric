# -*- coding: utf-8 -*-
"""Explicit SensorList Name query — find FDAPaperClosure row."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
# schema
cols = c.execute("PRAGMA table_info(SensorList)").fetchall()
print("columns:", [(col[1], col[2]) for col in cols])

c.text_factory = bytes
rows = c.execute("SELECT rowid, * FROM SensorList").fetchall()
print("rows:", len(rows))
for r in rows:
    # find Name column index
    name_idx = None
    for i, col in enumerate(cols):
        if col[1] == "Name":
            name_idx = i + 1  # +1 for rowid
            break
    raw = r[name_idx] if name_idx else None
    if raw:
        try:
            nm = raw.decode("cp950")
        except Exception:
            nm = repr(raw)[:60]
    else:
        nm = repr(raw)
    print(f"row {r[0]}: Name={nm!r} type={type(raw).__name__}")
c.close()
