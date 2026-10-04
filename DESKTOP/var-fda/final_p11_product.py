# -*- coding: utf-8 -*-
"""FINAL P11 (MOUSE-FREE): verify chooser applied, then product (17610) + trigger (17035) + readback."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
DLG = d32.window(handle=0xd1168)
DLG.wait("visible", timeout=5)

# --- verify script readback (edit 17202) ---
script_edit = DLG.child_window(control_id=17202, class_name="Edit")
print("script readback:", repr(script_edit.window_text()[:40]))

# --- product button (17610) ---
pb = DLG.child_window(control_id=17610, class_name="Button")
print("product btn exists:", pb.exists(timeout=2))
pb.click()
time.sleep(4)

# --- 選擇商品 dialog ---
prod = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇商品" in w.window_text():
            prod = w
            break
    except Exception:
        continue
if prod is None:
    print("FAIL product chooser")
    raise SystemExit(2)
print("product chooser:", hex(prod.handle))

# search edit (741) + 搜尋 button (802) + result list + 確定 (803 then 1)
q = prod.child_window(control_id=741, class_name="Edit")
print("query edit exists:", q.exists(timeout=2))
q.set_edit_text("2330")
time.sleep(0.3)
# click 搜尋 (802)
sbtn = prod.child_window(control_id=802, class_name="Button")
sbtn.click()
time.sleep(1.5)

# read list items (uia ListItem) to verify 台積電 present
du = Desktop(backend="uia")
pu = du.window(handle=prod.handle)
items = [i for i in pu.descendants(control_type="ListItem")
         if "2330" in i.window_text()]
print("product matches:", [i.window_text()[:30] for i in items[:3]])
