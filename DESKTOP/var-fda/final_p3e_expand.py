# -*- coding: utf-8 -*-
"""FINAL P3e: expand 自訂 tree, look for alert-script subnode / type tabs."""
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

du = Desktop(backend="uia")
dlg = du.window(handle=0x11354)

trees = dlg.descendants(control_type="Tree")
tv = trees[0]
custom = [i for i in tv.descendants(control_type="TreeItem")
          if i.window_text().startswith("自訂")]
print("custom nodes:", len(custom))
if custom:
    try:
        custom[0].expand()
        print("expanded 自訂")
        time.sleep(1)
    except Exception as e:
        print("expand err:", str(e)[:80])
    # list all visible tree items after expand
    for item in tv.descendants(control_type="TreeItem"):
        try:
            t = item.window_text()[:50]
            if t:
                print("  TI:", repr(t))
        except Exception:
            pass

# also check for tabs/type buttons in the dialog
print("=== buttons ===")
for b in dlg.descendants(control_type="Button"):
    try:
        t = b.window_text().strip()
        if t:
            print("  btn:", repr(t[:15]))
    except Exception:
        pass
