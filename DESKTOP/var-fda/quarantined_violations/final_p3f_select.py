# -*- coding: utf-8 -*-
"""FINAL P3f: select FDA_PAPER_ALERT in chooser, confirm; then handle 新增策略雷達 dialog."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

du = Desktop(backend="uia")
d32 = Desktop(backend="win32")

# 1. select FDA_PAPER_ALERT in chooser
dlg = du.window(handle=0x11354)
matches = [i for i in dlg.descendants(control_type="TreeItem")
           if i.window_text() == "FDA_PAPER_ALERT"]
print("FDA_PAPER_ALERT nodes:", len(matches))
if matches:
    matches[0].click_input()
    print("selected FDA_PAPER_ALERT")
    time.sleep(1)
    # click 確定(K)
    ok = [b for b in dlg.descendants(control_type="Button")
          if "確定" in b.window_text()]
    if ok:
        ok[0].click_input()
        print("clicked 確定")
        time.sleep(3)

# 2. find 新增策略雷達 dialog
nw = d32.window(title="新增策略雷達")
print("新增策略雷達 exists:", nw.exists(timeout=3))
if nw.exists(timeout=1):
    nw.wait("visible", timeout=8)
    print("NEW DIALOG:", hex(nw.handle))
    # enumerate edit/combobox/static controls (win32 control ids)
    for c in nw.children():
        try:
            ci = c.element_info.control_id() if hasattr(c.element_info, "control_id") else "?"
            cls = c.class_name()
            txt = c.window_text()[:30]
            print(f"  id={ci} {cls[:20]} '{txt}'")
        except Exception:
            pass
