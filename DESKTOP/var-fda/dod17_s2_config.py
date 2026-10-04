# -*- coding: utf-8 -*-
"""DoD-17 S2: XQ_PAPER_CONFIG — NEW(17551) -> dialog: name/script/product/trigger (pure messages)."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
from pywinauto import Desktop
import xq_native_adapter as na

u = ctypes.windll.user32
RADAR = 0x3612aa
d32 = Desktop(backend="win32")

# 1. find toolbar 59392 + press NEW (17551) via TB_PRESSBUTTON (message)
radar = d32.window(handle=RADAR)
radar.wait("visible enabled", timeout=5)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_index(cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return i
    return None
tb.button(cmd_index(17551)).click()  # win32 .click() = TB_PRESSBUTTON message
print("pressed NEW")
time.sleep(4)

# 2. find 新增策略雷達 dialog
DLG = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "新增策略雷達" in w.window_text():
            DLG = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if DLG is None:
    print("FAIL: dialog not found")
    raise SystemExit(2)
print("dialog:", hex(DLG.handle))

# 3. name (edit 17500) — unique
NAME = "FDAPaperProbe" + time.strftime("%H%M%S")
DLG.child_window(control_id=17500, class_name="Edit").set_edit_text(NAME)
time.sleep(0.4)
print("name:", NAME)

# 4. script button (17203) -> chooser -> select FDA_PAPER_ALERT
DLG.child_window(control_id=17203, class_name="Button").click()
time.sleep(3.5)
chooser = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇使用腳本" in w.window_text():
            chooser = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if chooser:
    du = Desktop(backend="uia")
    cu = du.window(handle=chooser.handle)
    tv = cu.descendants(control_type="Tree")[0]
    custom = [i for i in tv.descendants(control_type="TreeItem") if i.window_text().startswith("自訂")]
    if custom:
        custom[0].expand()
        time.sleep(1)
    target = [i for i in tv.descendants(control_type="TreeItem") if i.window_text() == "FDA_PAPER_ALERT"]
    print("FDA_PAPER_ALERT nodes:", len(target))
    if target:
        target[0].select()
        time.sleep(0.4)
        ok = [b for b in cu.descendants(control_type="Button") if "確定" in b.window_text()]
        if ok:
            ok[0].click()
            time.sleep(2.5)
print("script chosen")

# 5. product 2330
DLG = d32.window(handle=DLG.handle)
DLG.child_window(control_id=17610, class_name="Button").click()
time.sleep(3.5)
PROD = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "選擇商品" in w.window_text():
            PROD = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if PROD:
    PROD.child_window(control_id=741, class_name="Edit").set_edit_text("2330")
    time.sleep(0.3)
    PROD.child_window(control_id=802, class_name="Button").click()
    time.sleep(2)
    pu = Desktop(backend="uia").window(handle=PROD.handle)
    items = [i for i in pu.descendants(control_type="ListItem") if i.window_text() == "2330"]
    if items:
        items[0].select()
        time.sleep(0.4)
        PROD.child_window(control_id=803, class_name="Button").click()
        time.sleep(0.5)
        PROD.child_window(control_id=1, class_name="Button").click()
        time.sleep(2)
print("product:", repr(DLG.child_window(control_id=17107, class_name="Static").window_text()[:30]))

# 6. trigger mode 單次洗價模式 (17035)
DLG.child_window(control_id=17035, class_name="ComboBox").select("單次洗價模式")
time.sleep(0.4)
print("trigger:", repr(DLG.child_window(control_id=17035, class_name="ComboBox").window_text()[:15]))

# 7. readback
rb = {
    "name": DLG.child_window(control_id=17500, class_name="Edit").window_text(),
    "script": DLG.child_window(control_id=17202, class_name="Edit").window_text(),
    "product": DLG.child_window(control_id=17107, class_name="Static").window_text(),
    "trigger": DLG.child_window(control_id=17035, class_name="ComboBox").window_text(),
}
print("READBACK:", json.dumps(rb, ensure_ascii=False))
json.dump({"stage": "config", "name": NAME, "readback": rb, "dialog_hwnd": DLG.handle},
          open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("receipt partial saved (config stage)")
