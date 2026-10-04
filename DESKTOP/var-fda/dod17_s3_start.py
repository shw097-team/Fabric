# -*- coding: utf-8 -*-
"""DoD-17 S3: XQ_PAPER_START — 加入(1) -> auto-start -> notice handling -> toolbar state."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

u = ctypes.windll.user32
d32 = Desktop(backend="win32")
RADAR = 0x3612aa
DLG_HWND = 0x29092a

# 1. click 加入 (control_id=1) via pywinauto .click() (BM_CLICK message)
DLG = d32.window(handle=DLG_HWND)
add_btn = DLG.child_window(control_id=1, class_name="Button")
print("加入 btn:", add_btn.window_text()[:15])
add_btn.click()
print("clicked 加入")
time.sleep(2)

# 2. IMMEDIATE notice scan — handle any new #32770 dialog (開放體驗警示 etc.)
for attempt in range(8):
    time.sleep(1)
    notices = []
    for w in d32.windows(class_name="#32770"):
        try:
            if w.is_visible() and w.handle != RADAR and w.handle != DLG_HWND:
                t = w.window_text()
                if t.strip():
                    notices.append((w.handle, t))
        except Exception:
            pass
    if notices:
        for h, t in notices:
            print(f"notice: {hex(h)} '{t[:40]}'")
            nw = d32.window(handle=h)
            btns = nw.children(class_name="Button")
            if btns:
                btns[0].click()
                print(f"  dismissed via '{btns[0].window_text()[:15]}'")
                time.sleep(1.5)
        break
    else:
        if attempt >= 3:
            break

# 3. check dialog closed + toolbar state
time.sleep(2)
dlg_alive = any(w.handle == DLG_HWND and w.is_visible() for w in d32.windows(class_name="#32770"))
print("dialog closed:", not dlg_alive)

radar = d32.window(handle=RADAR)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def st(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return f"en={bool(b.info.fsState & 4)} pr={bool(b.info.fsState & 2)}"
    return None
start_state = st(17554)
stop_state = st(17555)
print("START:", start_state)
print("STOP :", stop_state)

# 4. DB check (XQSensor SensorList — big5)
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db)
c.text_factory = bytes
rows = c.execute("SELECT * FROM SensorList").fetchall()
cols = [r[1] for r in c.execute("PRAGMA table_info(SensorList)").fetchall()]
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
for r in rows:
    d = dict(zip(cols, r))
    if "FDAPaperProbe" in dec(d.get("Name")):
        print("DB HIT:", dec(d.get("Name")), "| Script:", dec(d.get("ScriptName")),
              "| Symbol:", dec(d.get("Symbol"))[:30])
c.close()

json.dump({"stage": "start", "start_state": start_state, "stop_state": stop_state,
           "dialog_closed": not dlg_alive},
          open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("receipt updated (start stage)")
