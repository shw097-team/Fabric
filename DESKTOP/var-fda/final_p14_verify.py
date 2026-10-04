# -*- coding: utf-8 -*-
"""FINAL P14: check 執行中 tree node children + DB state + toolbar after settle."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
RADAR = 0x110d96

# 1. expand 執行中 in tree, list children
du = Desktop(backend="uia")
ru = du.window(handle=RADAR)
trees = ru.descendants(control_type="Tree")
print("trees:", len(trees))
for tv in trees:
    for item in tv.descendants(control_type="TreeItem"):
        if item.window_text().strip() == "執行中":
            print("found 執行中; expanding...")
            try:
                item.expand()
                time.sleep(1)
            except Exception as e:
                print("expand err:", str(e)[:60])
            for child in item.descendants(control_type="TreeItem"):
                txt = child.window_text().strip()
                if txt:
                    print("   CHILD:", repr(txt[:50]))
            break

# 2. DB check
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"
c = sqlite3.connect(db)
rows = c.execute("SELECT Name, Enable, LastExecuteTime, ScriptType, ScriptID FROM XSTradeStrategyDTO WHERE Name LIKE 'FDAPaper%'").fetchall()
print("DB FDAPaper:", rows)
c.close()

# 3. toolbar state after settle (read-only)
radar = d32.window(handle=RADAR)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_state(cmd_id):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cmd_id:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None
print("START:", cmd_state(17554))
print("STOP :", cmd_state(17555))
