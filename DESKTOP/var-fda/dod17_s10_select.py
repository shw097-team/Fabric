# -*- coding: utf-8 -*-
"""DoD-17 S10 (fixed-route): uia select 自訂 category (pattern, no mouse) -> verify radar state."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
RADAR = 0x80fc8
ru = du.window(handle=RADAR)

# 1. find 自訂 TreeItem and select via pattern (NOT click_input)
try:
    items = ru.descendants(control_type="TreeItem")
    custom = next((i for i in items if (i.window_text() or "").strip() == "自訂"), None)
    print("自訂 found:", bool(custom))
    if custom:
        custom.select()
        print("selected 自訂 (pattern)")
        time.sleep(3)
except Exception as e:
    print("select err:", str(e)[:80])

# 2. verify radar state changed — dump tree + any strategy-ish text via uia read
try:
    items2 = ru.descendants(control_type="TreeItem")
    vis = [i.window_text().strip() for i in items2 if i.window_text().strip()]
    print("tree items:", vis[:20])
except Exception as e:
    print("tree read err:", str(e)[:60])

# 3. toolbar state (message read)
radar = d32.window(handle=RADAR)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_state(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None, None
print("START:", cmd_state(17554), "STOP:", cmd_state(17555))
