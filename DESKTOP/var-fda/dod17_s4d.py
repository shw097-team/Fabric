# -*- coding: utf-8 -*-
"""DoD-17 S4d: FDAPaperClosure full row + 執行紀錄 tab content."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

# 1. full row
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
cols = [col[1] for col in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
for r in rows:
    d = dict(zip(cols, r))
    if "FDAPaperClosure" in dec(d.get("Name")):
        print("=== FDAPaperClosure row ===")
        for k in ("Name", "SensorType", "ScriptType", "ScriptName", "Symbol", "Freq",
                  "TriggerSetting", "CreateTime", "ScriptVersion", "LastUpdateTime", "Comment"):
            print(f"  {k}: {dec(d.get(k))!r}")
c.close()

# 2. 執行紀錄 tab content
d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
ru = du.window(handle=0x80fc8)
try:
    tabs = ru.descendants(control_type="TabItem")
    for t in tabs:
        if t.window_text().strip() == "執行紀錄":
            t.select()
            time.sleep(2)
            print("\n=== 執行紀錄 tab ===")
            break
    # grid 17002 content
    grid = ru.child_window(control_id=17002, class_name="MFCGridCtrl")
    if grid.exists(timeout=2):
        texts = [x.window_text().strip() for x in grid.descendants() if x.window_text().strip()]
        print("grid rows:", len(texts))
        for x in texts[:12]:
            print("  ", x[:60])
    else:
        print("grid 17002 not found")
except Exception as e:
    print("tab err:", str(e)[:80])
