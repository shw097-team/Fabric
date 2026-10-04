# -*- coding: utf-8 -*-
"""FINAL P10 (MOUSE-FREE): continue — name, script chooser, product, trigger mode, add."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
DLG = d32.window(handle=0xd1168)
DLG.wait("visible", timeout=5)
print("dialog ok:", DLG.window_text())

# --- 1. name (edit 17500) ---
name_edit = DLG.child_window(control_id=17500, class_name="Edit")
print("name edit exists:", name_edit.exists(timeout=2))
name_edit.set_edit_text("FDAPaperProbe")
time.sleep(0.5)
print("name:", repr(name_edit.window_text()[:30]))

# --- 2. script button (17203) ---
sb = DLG.child_window(control_id=17203, class_name="Button")
print("script btn exists:", sb.exists(timeout=2))
sb.click()
time.sleep(4)

# --- 3. chooser dialog ---
chooser = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇使用腳本" in w.window_text():
            chooser = w
            break
    except Exception:
        continue
if chooser is None:
    print("FAIL chooser")
    raise SystemExit(2)
print("chooser:", hex(chooser.handle))

# expand 自訂 in chooser tree via uia (expand = pattern, no mouse)
du = Desktop(backend="uia")
ch_uia = du.window(handle=chooser.handle)
trees = ch_uia.descendants(control_type="Tree")
print("chooser trees:", len(trees))
tv = trees[0]
custom = [i for i in tv.descendants(control_type="TreeItem")
          if i.window_text().startswith("自訂")]
print("custom:", len(custom))
if custom:
    custom[0].expand()
    time.sleep(1)
    # find FDA_PAPER_ALERT and select (SelectionItemPattern — no mouse)
    target = [i for i in tv.descendants(control_type="TreeItem")
              if i.window_text() == "FDA_PAPER_ALERT"]
    print("FDA_PAPER_ALERT nodes:", len(target))
    if target:
        target[0].select()
        print("selected FDA_PAPER_ALERT")
        time.sleep(0.5)
        # confirm (確定 button — uia click = Invoke, no mouse)
        ok = [b for b in ch_uia.descendants(control_type="Button")
              if "確定" in b.window_text()]
        if ok:
            ok[0].click()
            print("confirmed chooser")
            time.sleep(3)
