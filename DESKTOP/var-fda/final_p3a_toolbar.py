# -*- coding: utf-8 -*-
"""FINAL P3a: verify radar toolbar 59392 + button command ids (win32)."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
radar = d32.window(handle=0x110d96)
radar.wait("visible enabled", timeout=8)
print("radar:", radar.window_text()[:40])

# toolbar control_id 59392, class ToolbarWindow32 (per xq_alert.py)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32")
print("toolbar 59392 exists:", tb.exists(timeout=3))
if tb.exists(timeout=1):
    try:
        print("button count:", tb.button_count())
        for i in range(min(tb.button_count(), 30)):
            try:
                b = tb.button(i)
                print(f"  [{i}] id={b.info.idCommand} state={b.info.fsState} enabled={bool(b.info.fsState & 4)}")
            except Exception as e:
                print(f"  [{i}] err {str(e)[:40]}")
    except Exception as e:
        print("button_count err:", str(e)[:80])
