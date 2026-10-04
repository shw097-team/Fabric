# -*- coding: utf-8 -*-
"""FAR v19: check if radar window exists (win32), enumerate its toolbar via win32."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

d32 = Desktop(backend="win32")
radar = d32.window(title_re="策略雷達.*")
print("radar exists:", radar.exists(timeout=2))
if radar.exists(timeout=1):
    radar.wait("visible enabled", timeout=8)
    print("radar:", radar.window_text()[:50], hex(radar.handle))
    # find ToolbarWindow32 (standard class per xq_alert.py: control_id 59392)
    try:
        tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32")
        print("toolbar 59392 exists:", tb.exists(timeout=2))
        if tb.exists(timeout=1):
            print("button count:", tb.button_count())
            for i in range(min(tb.button_count(), 20)):
                try:
                    b = tb.button(i)
                    print(f"  [{i}] id={b.info.idCommand} state={b.info.fsState}")
                except Exception as e:
                    print(f"  [{i}] err {str(e)[:40]}")
    except Exception as e:
        print("toolbar err:", str(e)[:100])
