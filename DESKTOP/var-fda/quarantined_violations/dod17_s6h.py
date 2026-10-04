# -*- coding: utf-8 -*-
"""DoD-17 S6h: click_input 自訂 (community pattern) + verify grid + read SensorList again."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and w.window_text().startswith("策略雷達"):
            radar_hwnd = w.handle
            break
    except Exception:
        pass
ru = du.window(handle=radar_hwnd)

# click_input 自訂 (community-validated)
customs = [e for e in ru.descendants(control_type="TreeItem") if (e.window_text() or "").strip() == "自訂"]
print("自訂:", len(customs))
if customs:
    customs[0].click_input()
    print("click_input 自訂")
    time.sleep(3)

# read grid via uia (try 17001 + all text)
for cid in (17001, 17002):
    try:
        grid = ru.child_window(control_id=cid, class_name="MFCGridCtrl")
        if grid.exists(timeout=2):
            texts = [el.window_text().strip() for el in grid.descendants()
                     if el.window_text().strip() and len(el.window_text().strip()) < 50]
            fda = [t for t in texts if "FDA" in t or "FDAPaper" in t]
            print(f"grid {cid}: {texts[:12]}")
            print(f"  FDA: {fda[:5]}")
    except Exception as e:
        print(f"grid {cid} err: {str(e)[:50]}")

# SensorList re-read
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=5)
c.text_factory = bytes
cols = [col[1] for col in c.execute("PRAGMA table_info(SensorList)").fetchall()]
rows = c.execute("SELECT * FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
names = []
for r in rows:
    d = dict(zip(cols, r))
    nm = dec(d.get("Name"))
    if nm:
        names.append(nm[:40])
print("SensorList names:", names)
c.close()
