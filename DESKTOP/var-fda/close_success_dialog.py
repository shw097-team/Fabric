# -*- coding: utf-8 -*-
"""Close 新增成功 dialog (關閉 button) + verify radar now shows FDAPaperFinal strategy."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

u = ctypes.windll.user32
DLG = 0xe1014

# 1. click 關閉 button (BM_CLICK message)
u.PostMessageW(0x220b6a, 0x00F5, 0, 0)
print("clicked 關閉")
time.sleep(2)

# verify dialog gone
still = u.IsWindow(DLG)
print("dialog still exists:", bool(still))

# 2. verify strategy in DB (FDAPaperFinal020037)
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
print("=== SensorList ===")
for n, s, y, ct in rows:
    print(f"  {dec(n)[:38]} | {dec(s)[:25]} | {dec(y)[:15]} | {dec(ct)}")
c.close()
