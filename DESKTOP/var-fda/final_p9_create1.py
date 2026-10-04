# -*- coding: utf-8 -*-
"""FINAL P9 (MOUSE-FREE FULL): create radar strategy via pure window messages.
tb.click() = TB_PRESSBUTTON, btn.click() = BM_CLICK, edit.set_edit_text() = WM_SETTEXT,
tree expand/select = TVM. NO click_input anywhere.
"""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
RADAR_HANDLE = 0x110d96
radar = d32.window(handle=RADAR_HANDLE)
radar.wait("visible enabled", timeout=5)

# --- 1. toolbar: press NEW (17551) via pywinauto win32 .click() = TB_PRESSBUTTON ---
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
print("toolbar ok")
# find index of 17551
def cmd_index(cmd_id):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cmd_id:
            return i
    raise RuntimeError(f"cmd {cmd_id} not found")
ni = cmd_index(17551)
tb.button(ni).click()
print("pressed NEW(17551) idx", ni)
time.sleep(4)

# --- 2. find 新增策略雷達 dialog ---
dlg = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "新增策略雷達" in w.window_text():
            dlg = w
            break
    except Exception:
        continue
if dlg is None:
    print("FAIL: 新增策略雷達 dialog not found")
    raise SystemExit(2)
print("dialog:", dlg.window_text(), hex(dlg.handle))

# --- 3. set strategy name (edit 17500) via pywinauto set_edit_text (WM_SETTEXT) ---
name_edit = dlg.child_window(control_id=17500, class_name="Edit")
name_edit.set_edit_text("FDAPaperProbe")
time.sleep(0.5)
print("name set:", repr(name_edit.window_text()[:30]))

# --- 4. click 腳本選擇 button (17203) via .click() (BM_CLICK) ---
script_btn = dlg.child_window(control_id=17203, class_name="Button")
print("script btn exists:", script_btn.exists(timeout=2))
script_btn.click()
time.sleep(3)

# --- 5. 選擇使用腳本 dialog: expand 自訂, select FDA_PAPER_ALERT ---
chooser = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇使用腳本" in w.window_text():
            chooser = w
            break
    except Exception:
        continue
if chooser is None:
    print("FAIL: chooser not found")
    raise SystemExit(2)
print("chooser:", hex(chooser.handle))
