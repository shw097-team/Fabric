# -*- coding: utf-8 -*-
"""DoD-17 FINAL v2: NEW(17551) -> dialog -> 加入 = AUTO-START (community flow) -> wash-complete verify.
Community: 加入 = auto-execute (綠燈); single-wash complete = START en AND STOP dis."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
du = Desktop(backend="uia")
u = ctypes.windll.user32
RADAR = 0x32112a
receipt = {"stages": {}}

radar = d32.window(handle=RADAR)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
def cmd_index(cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            return i
    return None
def cmd_state(cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None, None

# 1. NEW
tb.button(cmd_index(17551)).click()
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

# 3. name (unique)
NAME = "FDAPaperFinal" + time.strftime("%H%M%S")
DLG.child_window(control_id=17500, class_name="Edit").set_edit_text(NAME)
time.sleep(0.4)
print("name:", NAME)

# 4. script FDA_PAPER_ALERT
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
    cu = du.window(handle=chooser.handle)
    tv = cu.descendants(control_type="Tree")[0]
    custom = [i for i in tv.descendants(control_type="TreeItem") if i.window_text().startswith("自訂")]
    if custom:
        custom[0].expand()
        time.sleep(1)
    target = [i for i in tv.descendants(control_type="TreeItem") if i.window_text() == "FDA_PAPER_ALERT"]
    print("FDA_PAPER_ALERT:", len(target))
    if target:
        target[0].select()
        time.sleep(0.4)
        ok = [b for b in cu.descendants(control_type="Button") if "確定" in b.window_text()]
        if ok:
            ok[0].click()
            time.sleep(2.5)

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
    pu = du.window(handle=PROD.handle)
    items = [i for i in pu.descendants(control_type="ListItem") if i.window_text() == "2330"]
    if items:
        items[0].select()
        time.sleep(0.4)
        PROD.child_window(control_id=803, class_name="Button").click()
        time.sleep(0.5)
        PROD.child_window(control_id=1, class_name="Button").click()
        time.sleep(2)

# 6. trigger mode
DLG.child_window(control_id=17035, class_name="ComboBox").select("單次洗價模式")
time.sleep(0.4)
rb = {
    "name": DLG.child_window(control_id=17500, class_name="Edit").window_text(),
    "script": DLG.child_window(control_id=17202, class_name="Edit").window_text(),
    "product": DLG.child_window(control_id=17107, class_name="Static").window_text(),
    "trigger": DLG.child_window(control_id=17035, class_name="ComboBox").window_text(),
}
print("CONFIG:", json.dumps(rb, ensure_ascii=False))
receipt["stages"]["config"] = rb
receipt["strategy_name"] = NAME

# 7. 加入 = AUTO-START
DLG.child_window(control_id=1, class_name="Button").click()
print("clicked 加入 (auto-start)")
time.sleep(2)

# 8. notice handling — poll ALL-class dialogs (fixed route: not just #32770)
for attempt in range(8):
    time.sleep(1)
    notices = []
    for w in d32.windows():
        try:
            if w.is_visible() and w.handle not in (RADAR, DLG.handle):
                t = w.window_text()
                if t.strip() and "新增策略" not in t:
                    notices.append((w.handle, t))
        except Exception:
            pass
    if notices:
        for h, t in notices:
            print(f"notice: '{t[:30]}'")
            btns = []
            @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
            def cb(ch, lp):
                cls = ctypes.create_unicode_buffer(64)
                u.GetClassNameW(ch, cls, 64)
                if "Button" in cls.value:
                    btns.append(ch)
                return True
            u.EnumChildWindows(h, cb, 0)
            print(f"  buttons: {len(btns)}")
            if btns:
                u.PostMessageW(btns[0], 0x00F5, 0, 0)
                print("  dismissed (BM_CLICK)")
                time.sleep(1.5)
        break
    if attempt >= 4:
        break

# 9. AUTO-START verify — poll toolbar for wash-complete (START en AND STOP dis) up to 60s
wash = False
for i in range(60):
    time.sleep(1)
    st = cmd_state(17554); sp = cmd_state(17555)
    if st[0] and not sp[0]:
        wash = True
        print(f"WASH COMPLETE t+{i}s: START en={st[0]} STOP en={sp[0]}")
        break
    if sp[0]:
        print(f"t+{i}s RUNNING: STOP en={sp[0]} pr={sp[1]}")
        running_observed = True
print("wash complete:", wash)
receipt["stages"]["wash"] = {"complete": wash,
                             "start": cmd_state(17554), "stop": cmd_state(17555)}

# 10. persistence
db = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
c = sqlite3.connect(db, timeout=8)
c.text_factory = bytes
rows = c.execute("SELECT Name, ScriptName, Symbol, CreateTime FROM SensorList").fetchall()
def dec(b):
    return b.decode("cp950", errors="replace") if isinstance(b, bytes) else str(b)
persist = [(dec(n), dec(s), dec(y)) for n, s, y, ct in rows if NAME in dec(n)]
print("persisted:", persist)
receipt["stages"]["persistence"] = persist

receipt["broker_write"] = 0
receipt["environment"] = "PAPER"
receipt["subscribed_module"] = "盤中量化交易模組"
receipt["fixed_route"] = "pure messages + cua background; no mouse steal"
receipt["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
json.dump(receipt, open(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_PAPER_RUNTIME_RECEIPT.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("receipt saved")
