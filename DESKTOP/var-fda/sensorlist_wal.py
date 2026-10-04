# -*- coding: utf-8 -*-
"""SensorList read with WAL handling + full row dump."""
import sqlite3
import time

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
for attempt in range(3):
    time.sleep(3)
    try:
        c = sqlite3.connect(db, timeout=8)
        c.text_factory = bytes
        cols = [col[1] for col in c.execute("PRAGMA table_info(SensorList)").fetchall()]
        rows = c.execute("SELECT * FROM SensorList").fetchall()
        def dec(b):
            return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
        print(f"attempt {attempt+1} rows: {len(rows)}")
        for r in rows:
            d = dict(zip(cols, r))
            print("  -", repr(dec(d.get("Name"))[:40]), "| Create:", repr(dec(d.get("CreateTime"))),
                  "| Script:", repr(dec(d.get("ScriptName"))[:30]), "| Symbol:", repr(dec(d.get("Symbol"))[:20]))
        c.close()
        if any(dec(dict(zip(cols, r)).get("Name")) for r in rows):
            break
    except Exception as e:
        print(f"attempt {attempt+1} err: {str(e)[:60]}")
