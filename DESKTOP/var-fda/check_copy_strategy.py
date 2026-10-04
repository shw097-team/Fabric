# -*- coding: utf-8 -*-
"""Check all XQ strategy DBs for the copied strategy record."""
import sqlite3

for db in (
    r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite",
    r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite",
):
    c = sqlite3.connect(db)
    tabs = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    for t in tabs:
        try:
            rows = c.execute(f"SELECT * FROM {t}").fetchall()
            if rows:
                for row in rows:
                    s = str(row)
                    if "暴量" in s or "複製" in s:
                        print(db.split("\\")[-1], t, "->", s[:150])
        except Exception:
            pass
    c.close()
print("done")
