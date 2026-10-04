# -*- coding: utf-8 -*-
"""Count SensorLog Table_20260814 execution starts (ExecState=1) across all FDA strategies."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
c = sqlite3.connect(db, timeout=10)
c.text_factory = bytes
cols = [r[1].decode("cp950", errors="replace") if isinstance(r[1], bytes) else r[1]
        for r in c.execute("PRAGMA table_info(Table_20260814)")]
print("cols:", cols[:20])

# try to find ExecState + XQSensorName columns
rows = list(c.execute("SELECT * FROM Table_20260814"))
print("total rows:", len(rows))

# decode with explicit column mapping
def dec(x):
    if isinstance(x, bytes):
        return x.decode("cp950", errors="replace")
    return str(x)

# find column indexes
name_idx = None
state_idx = None
for i, col in enumerate(cols):
    cl = col.lower()
    if "name" in cl:
        name_idx = i
    if "exec" in cl and "state" in cl:
        state_idx = i
print("name_idx:", name_idx, "state_idx:", state_idx)

# per-strategy ExecState=1 count (execution starts)
from collections import Counter
starts = Counter()
for r in rows:
    name = dec(r[name_idx]) if name_idx is not None else "?"
    st = dec(r[state_idx]) if state_idx is not None else "?"
    if st == "1":
        starts[name] += 1
print("ExecState=1 starts per strategy:", dict(starts))
print("total starts:", sum(starts.values()))
