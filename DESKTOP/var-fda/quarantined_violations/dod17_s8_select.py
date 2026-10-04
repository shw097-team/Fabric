# -*- coding: utf-8 -*-
"""DoD-17 S8: select FDAPaperClosure011939 in 自訂 category, then START, verify running, STOP."""
import ctypes
import ctypes.wintypes as wt
import json
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
radar = d32.window(handle=radar_hwnd)
ru = du.window(handle=radar_hwnd)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_index(cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return i
    return None
def cmd_state(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None, None

receipt = {}

# 1. click 自訂 (community click_input) then find FDAPaperClosure tree item
customs = [e for e in ru.descendants(control_type="TreeItem") if (e.window_text() or "").strip() == "自訂"]
print("自訂:", len(customs))
if customs:
    customs[0].click_input()
    time.sleep(3)
    print("clicked 自訂")

# find strategy item under tree (uia read)
target = None
try:
    items = ru.descendants(control_type="TreeItem")
    fda = [i for i in items if "FDAPaperClosure" in (i.window_text() or "")]
    print("FDAPaperClosure items:", len(fda))
    if fda:
        target = fda[0]
except Exception as e:
    print("find err:", str(e)[:60])

if target:
    target.click_input()
    print("selected FDAPaperClosure")
    time.sleep(2)

# 2. START
st = cmd_state(17554); sp = cmd_state(17555)
print(f"pre-START: START en={st[0]} | STOP en={sp[0]} pr={sp[1]}")
tb.button(cmd_index(17554)).click()
print("pressed START")
time.sleep(6)
st2 = cmd_state(17554); sp2 = cmd_state(17555)
print(f"after START t+6s: START en={st2[0]} | STOP en={sp2[0]} pr={sp2[1]} running={bool(sp2[0])}")
receipt["start"] = {"start_en": st2[0], "stop_en": sp2[0], "running": bool(sp2[0])}

# 3. wait + status
time.sleep(8)
st3 = cmd_state(17554); sp3 = cmd_state(17555)
print(f"status t+14s: START en={st3[0]} | STOP en={sp3[0]} pr={sp3[1]} running={bool(sp3[0])}")
receipt["status"] = {"start_en": st3[0], "stop_en": sp3[0], "running": bool(sp3[0])}

# 4. STOP
if bool(sp3[0]):
    tb.button(cmd_index(17555)).click()
    print("pressed STOP")
    time.sleep(4)
st4 = cmd_state(17554); sp4 = cmd_state(17555)
print(f"after STOP: START en={st4[0]} | STOP en={sp4[0]} pr={sp4[1]}")
receipt["stop"] = {"start_en": st4[0], "stop_en": sp4[0]}

json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved")
