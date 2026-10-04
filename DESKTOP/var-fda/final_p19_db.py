# -*- coding: utf-8 -*-
"""FINAL P19: close error dialog; check DB for FDAPaperProbe (full query)."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32
# close error dialog 0x5f11f0 (WM_CLOSE)
user32.PostMessageW(0x5f11f0, 0x0010, 0, 0)
print("closed error dialog")
time.sleep(1)

db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"
c = sqlite3.connect(db)
tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("tables:", tables)
for t in tables:
    try:
        n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {n} rows")
        if n and n < 100:
            cols = [r[1] for r in c.execute(f"PRAGMA table_info({t})").fetchall()]
            rows = c.execute(f"SELECT * FROM {t}").fetchall()
            for r in rows:
                print("   ", [str(x)[:28] for x in r][:10])
    except Exception as e:
        print(f"  {t}: err {str(e)[:40]}")
c.close()
