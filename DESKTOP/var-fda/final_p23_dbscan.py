# -*- coding: utf-8 -*-
"""FINAL P23: scan ALL XQ sqlite DBs for FDAPaperProbe / recent sensor runs."""
import glob
import sqlite3
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

dbs = glob.glob(r"C:\SysJust\XQLite\**\*.sqlite", recursive=True) + \
      glob.glob(r"C:\SysJust\XQLite\**\*.db", recursive=True)
print("found DBs:", len(dbs))
for db in dbs:
    try:
        c = sqlite3.connect(db)
        tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        for t in tables:
            try:
                cols = [r[1] for r in c.execute(f"PRAGMA table_info({t})").fetchall()]
                # search tables with name-ish columns for FDAPaper
                if any("Name" in col or "name" in col for col in cols):
                    name_col = next((col for col in cols if "Name" in col or "name" in col), cols[0])
                    try:
                        rows = c.execute(f"SELECT {name_col} FROM {t} WHERE {name_col} LIKE '%FDAPaper%' OR {name_col} LIKE '%Probe%'").fetchall()
                        if rows:
                            print(f"  HIT {db}\n    {t}.{name_col}: {rows[:5]}")
                    except Exception:
                        pass
                # also look for sensor/trigger tables
                if any(k in t.lower() for k in ("sensor", "log", "trigger", "execut", "run")):
                    n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                    if n:
                        print(f"  {db} :: {t} ({n} rows)")
            except Exception:
                pass
        c.close()
    except Exception:
        pass
