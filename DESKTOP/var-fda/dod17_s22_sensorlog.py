# -*- coding: utf-8 -*-
"""DoD-17 S22: read SensorLog Table_20260814 — execution records for FDAPaperFinal."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes

# schema
cols = [col[1] for col in c.execute("PRAGMA table_info(Table_20260814)").fetchall()]
print("Table_20260814 cols:", cols[:15])

rows = c.execute("SELECT * FROM Table_20260814").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
print(f"rows: {len(rows)}")
for r in rows:
    d = dict(zip(cols, r))
    line = " | ".join(f"{k}={dec(v)[:25]}" for k, v in list(d.items())[:10])
    print(" ", line)

# exec times table
print("\nCustomFieldStrategyExecTimes:")
try:
    rows2 = c.execute("SELECT * FROM CustomFieldStrategyExecTimes").fetchall()
    cols2 = [col[1] for col in c.execute("PRAGMA table_info(CustomFieldStrategyExecTimes)").fetchall()]
    for r in rows2:
        d = dict(zip(cols2, r))
        print("  ", " | ".join(f"{k}={dec(v)[:30]}" for k, v in d.items()))
except Exception as e:
    print("  err:", str(e)[:60])
c.close()
