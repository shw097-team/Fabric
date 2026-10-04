# -*- coding: utf-8 -*-
"""Inspect XSStrategyCenter.sqlite — radar strategy storage."""
import sqlite3

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"
c = sqlite3.connect(db)
for t in ("XSTradeStrategyDTO", "StrategyTreeItemSource", "StrategyScheduleSetting"):
    cols = [r[1] for r in c.execute(f"PRAGMA table_info({t})")]
    print(f"=== {t} cols ===")
    print("  ", cols)
    n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print("  rows:", n)
    if n:
        row = c.execute(f"SELECT * FROM {t} LIMIT 1").fetchone()
        for col, val in zip(cols, row):
            v = str(val)
            print(f"    {col}: {v[:60]}")
c.close()
