# -*- coding: utf-8 -*-
"""DoD-17 S8b: post-user-confirm — verify dialog closed, strategy in list, toolbar state."""
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

# all visible dialogs
print("=== visible windows ===")
for w in d32.windows():
    try:
        if w.is_visible():
            t = w.window_text()
            if t.strip():
                print(" ", hex(w.handle), "|", t[:55])
    except Exception:
        pass

# radar toolbar state
radar_hwnd = None
for w in d32.windows():
    try:
        if w.is_visible() and w.window_text().startswith("策略雷達"):
            radar_hwnd = w.handle
            break
    except Exception:
        pass
if radar_hwnd:
    radar = d32.window(handle=radar_hwnd)
    tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
    def cmd_state(cid):
        for i in range(tb.button_count()):
            b = tb.button(i)
            if b.info.idCommand == cid:
                return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
        return None, None
    st = cmd_state(17554); sp = cmd_state(17555)
    print(f"toolbar: START en={st[0]} pr={st[1]} | STOP en={sp[0]} pr={sp[1]}")
    # NEW enabled? COPY enabled?
    for cid, nm in ((17551, "NEW"), (17627, "COPY"), (17553, "DEL")):
        s = cmd_state(cid)
        print(f"  {nm}: en={s[0]}")
else:
    print("radar not found")

# SensorList re-read
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
for n, s, y, ct in rows:
    print("DB:", dec(n)[:35], "|", dec(s)[:25], "|", dec(y)[:15], "|", dec(ct))
c.close()
