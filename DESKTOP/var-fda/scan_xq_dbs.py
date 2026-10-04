# -*- coding: utf-8 -*-
"""Scan XQ sqlite DBs for strategy/alert/radar tables."""
import glob
import sqlite3

for db in glob.glob(r"C:\SysJust\XQLite\**\*.sqlite", recursive=True):
    try:
        c = sqlite3.connect(db)
        tabs = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        interesting = [t for t in tabs if any(k in t.lower() for k in
                                             ("select", "alert", "radar", "strategy", "trade", "script"))]
        if interesting:
            short = db.replace("C:\\SysJust\\XQLite\\", "")
            print(short, "->", interesting[:10])
        c.close()
    except Exception:
        pass
