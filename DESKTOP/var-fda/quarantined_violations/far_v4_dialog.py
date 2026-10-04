# -*- coding: utf-8 -*-
"""FAR v4: click 新增 (toolbar), handle 新增腳本 dialog: 警示 type + name + confirm."""
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
import time
from pywinauto import Desktop

desktop = Desktop(backend="uia")
editor = desktop.window(title_re=".*XScript 編輯器.*")
editor.wait("exists visible", timeout=5)

# 1. click 新增 toolbar button
add_btn = [b for b in editor.descendants(control_type="Button")
           if b.window_text().strip() == "新增" and b.is_visible()]
if not add_btn:
    raise RuntimeError("新增 button not found")
add_btn[0].click_input()
print("clicked 新增")
time.sleep(2)

# 2. find 新增腳本 dialog
d32 = Desktop(backend="win32")
dlg = None
for w in d32.windows(class_name="#32770"):
    try:
        if "新增腳本" in w.window_text():
            dlg = w
            break
    except Exception:
        continue
if dlg is None:
    print("no dialog; listing #32770:")
    for w in d32.windows(class_name="#32770"):
        print("  ", w.window_text()[:40])
    raise SystemExit(2)
print("dialog:", dlg.window_text())

# 3. via uia on dialog: click 警示 button, set name edit, confirm
du = Desktop(backend="uia")
dlg_uia = du.window(handle=dlg.handle)
# list all buttons + edits with text
for b in dlg_uia.descendants(control_type="Button"):
    t = b.window_text().strip()
    if t:
        print("  btn:", repr(t[:15]))
for e in dlg_uia.descendants(control_type="Edit"):
    print("  edit:", e.element_info.control_id())

# click 警示
warn = [b for b in dlg_uia.descendants(control_type="Button")
        if b.window_text().strip() == "警示"]
if warn:
    warn[0].click_input()
    print("clicked 警示")
    time.sleep(0.8)

# set name: find the edit labeled 名稱： (first edit after Static 名稱：)
# use win32: edits with control ids
edits = dlg.children(class_name="Edit")
print("edits win32:", [(e.element_info.control_id(), e.window_text()[:20]) for e in edits])
