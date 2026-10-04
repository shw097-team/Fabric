# -*- coding: utf-8 -*-
"""FINAL P12 (MOUSE-FREE): product chooser — query 2330, select 台積電, confirm."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
PROD = d32.window(handle=0xa0f34)
PROD.wait("visible", timeout=5)
print("product chooser ok")

# query edit (741)
q = PROD.child_window(control_id=741, class_name="Edit")
print("query edit:", q.exists(timeout=2))
q.set_edit_text("2330")
time.sleep(0.3)

# 搜尋 button (802)
sbtn = PROD.child_window(control_id=802, class_name="Button")
sbtn.click()
time.sleep(2)

# list items via uia — select 台積電(2330)
du = Desktop(backend="uia")
pu = du.window(handle=0xa0f34)
items = [i for i in pu.descendants(control_type="ListItem")
         if "2330" in i.window_text()]
print("matches:", [i.window_text()[:40] for i in items[:3]])
if items:
    items[0].select()
    print("selected:", items[0].window_text()[:30])
    time.sleep(0.5)
    # 確定 (803) then (1)
    b803 = PROD.child_window(control_id=803, class_name="Button")
    b803.click()
    time.sleep(0.5)
    b1 = PROD.child_window(control_id=1, class_name="Button")
    b1.click()
    print("confirmed product")
    time.sleep(2)

# readback product static (17107) in main dialog
DLG = d32.window(handle=0xd1168)
pr = DLG.child_window(control_id=17107, class_name="Static")
print("product readback:", repr(pr.window_text()[:40]))

# trigger mode combobox (17035) — set 單次洗價模式
cb = DLG.child_window(control_id=17035, class_name="ComboBox")
print("trigger cb exists:", cb.exists(timeout=2))
cb.select("單次洗價模式")
time.sleep(0.5)
print("trigger mode:", repr(cb.window_text()[:20]))
