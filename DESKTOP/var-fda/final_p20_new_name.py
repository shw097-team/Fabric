# -*- coding: utf-8 -*-
"""FINAL P20: close leftover dialog (0x100f34), use NEW name, add, verify ALL surfaces."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32
d32 = Desktop(backend="win32")

# close leftover 新增策略雷達 dialog
user32.PostMessageW(0x100f34, 0x0010, 0, 0)
time.sleep(1)

RADAR_HANDLE = 0x110d96
radar = d32.window(handle=RADAR_HANDLE)
radar.wait("visible enabled", timeout=5)

# --- 1. NEW ---
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_index(cmd_id):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cmd_id:
            return i
    return None
tb.button(cmd_index(17551)).click()
time.sleep(4)

DLG = None
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible() and "新增策略雷達" in w.window_text():
            DLG = d32.window(handle=w.handle)
            break
    except Exception:
        continue
if DLG is None:
    print("FAIL dialog")
    raise SystemExit(2)
print("dialog:", hex(DLG.handle))

# --- 2. unique name ---
NAME = "FDAPaperProbe" + time.strftime("%H%M%S")
DLG.child_window(control_id=17500, class_name="Edit").set_edit_text(NAME)
print("name:", NAME)
time.sleep(0.4)

# --- 3. script ---
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
    custom = [i for i in tv.descendants(control_type="TreeItem")
              if i.window_text().startswith("自訂")]
    if custom:
        custom[0].expand()
        time.sleep(1)
    target = [i for i in tv.descendants(control_type="TreeItem")
              if i.window_text() == "FDA_PAPER_ALERT"]
    if target:
        target[0].select()
        time.sleep(0.4)
        ok = [b for b in cu.descendants(control_type="Button") if "確定" in b.window_text()]
        if ok:
            ok[0].click()
            time.sleep(2.5)
print("script chosen")

# --- 4. product 2330 ---
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

# --- 5. trigger mode ---
DLG.child_window(control_id=17035, class_name="ComboBox").select("單次洗價模式")
time.sleep(0.4)
print("trigger:", repr(DLG.child_window(control_id=17035, class_name="ComboBox").window_text()[:15]))

# --- 6. 加入 ---
DLG.child_window(control_id=1, class_name="Button").click()
print("clicked 加入")
time.sleep(3)

# --- 7. VERIFY: dialogs + toolbar + DB + 執行中 tree ---
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible():
            t = w.window_text()
            if t.strip():
                print("DLG:", hex(w.handle), "|", t[:45])
    except Exception:
        pass

tb2 = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def st(cid):
    for i in range(tb2.button_count()):
        b = tb2.button(i)
        if b.info.idCommand == cid:
            return f"en={bool(b.info.fsState & 4)} pr={bool(b.info.fsState & 2)}"
print("START:", st(17554), "| STOP:", st(17555))

# DB full scan for NAME
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite"
c = sqlite3.connect(db)
rows = c.execute(f"SELECT Name, Enable, LastExecuteTime FROM XSTradeStrategyDTO WHERE Name LIKE '%{NAME}%'").fetchall()
c.close()
print("DB:", rows)
