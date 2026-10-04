# -*- coding: utf-8 -*-
"""DoD-17 S4b: verify strategy exists — radar left tree 自訂 + SensorList delayed re-read."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x80fc8
radar = d32.window(handle=RADAR)

# 1. radar left tree — 自訂 category via uia (read-only, expand)
ru = du.window(handle=RADAR)
try:
    trees = ru.descendants(control_type="Tree")
    print("trees:", len(trees))
    for tv in trees:
        items = tv.descendants(control_type="TreeItem")
        for it in items:
            t = it.window_text()
            if t.strip():
                print("  TI:", t[:40])
        break
except Exception as e:
    print("tree err:", str(e)[:80])

# 2. SensorList delayed re-read (3 attempts)
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
for attempt in range(3):
    time.sleep(2)
    c = sqlite3.connect(db)
    c.text_factory = bytes
    cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
    rows = c.execute("SELECT * FROM SensorList").fetchall()
    def dec(b):
        return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
    names = [dec(dict(zip(cols, r)).get("Name"))[:40] for r in rows]
    print(f"attempt {attempt+1}: {names}")
    if any("FDAPaperClosure" in n for n in names):
        print("FOUND FDAPaperClosure in SensorList!")
        break
    c.close()
