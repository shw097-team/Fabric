# -*- coding: utf-8 -*-
"""FINAL P17 (MOUSE-FREE): full create flow + IMMEDIATE notice handling after 加入."""
import ctypes
import ctypes.wintypes as wt
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
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

# dialog
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

# --- 2. name ---
DLG.child_window(control_id=17500, class_name="Edit").set_edit_text("FDAPaperProbe")
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
if chooser is None:
    print("FAIL chooser")
    raise SystemExit(2)
du = Desktop(backend="uia")
cu = du.window(handle=chooser.handle)
trees = cu.descendants(control_type="Tree")
tv = trees[0]
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

# --- 4. product ---
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

# --- 6. 加入 + IMMEDIATE notice scan ---
DLG.child_window(control_id=1, class_name="Button").click()
print("clicked 加入; scanning for notice...")
for attempt in range(6):
    time.sleep(1)
    notices = []
    for w in d32.windows(class_name="#32770"):
        try:
            if w.is_visible() and w.handle != RADAR_HANDLE:
                t = w.window_text()
                if t.strip():
                    notices.append((w.handle, t))
        except Exception:
            pass
    if notices:
        print(f"  t+{attempt+1}s notices:", [(hex(h), t[:40]) for h, t in notices])
        for h, t in notices:
            # click first button in notice (usually 我知道了/確定)
            nw = d32.window(handle=h)
            btns = nw.children(class_name="Button")
            if btns:
                btns[0].click()
                print("   dismissed:", t[:30], "via", btns[0].window_text()[:15])
        time.sleep(2)
        break
    else:
        print(f"  t+{attempt+1}s no notice")
time.sleep(4)

# --- 7. verify ---
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XSStrategyCenter.sqlite")
rows = c.execute("SELECT Name, Enable, LastExecuteTime, ScriptID FROM XSTradeStrategyDTO WHERE Name LIKE 'FDAPaper%'").fetchall()
c.close()
print("DB:", rows)
