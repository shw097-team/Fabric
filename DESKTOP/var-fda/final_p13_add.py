# -*- coding: utf-8 -*-
"""FINAL P13 (MOUSE-FREE): click 加入 (id=1) -> strategy auto-starts -> verify wash + trigger."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

d32 = Desktop(backend="win32")
DLG = d32.window(handle=0xd1168)
DLG.wait("visible", timeout=5)

# click 加入 (control_id=1)
add_btn = DLG.child_window(control_id=1, class_name="Button")
print("加入 btn:", add_btn.window_text()[:15])
add_btn.click()
print("clicked 加入")
time.sleep(6)

# --- check: dialog closed? notice dialog? radar toolbar state ---
for w in d32.windows(class_name="#32770"):
    try:
        if w.is_visible():
            t = w.window_text()
            if t.strip() and "策略" in t:
                print("DLG:", hex(w.handle), "|", t[:40])
    except Exception:
        pass

# radar toolbar START/STOP state (fsState via pywinauto — read-only, no input)
RADAR = 0x110d96
radar = d32.window(handle=RADAR)
tb = radar.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()

def cmd_state(cmd_id):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cmd_id:
            return bool(b.info.fsState & 4), bool(b.info.fsState & 2)
    return None

start_en, start_pressed = cmd_state(17554)
stop_en, stop_pressed = cmd_state(17555)
print(f"START enabled={start_en} pressed={start_pressed}")
print(f"STOP  enabled={stop_en} pressed={stop_pressed}")

# --- trigger readback: 觸發商品 tab tree (33035) ---
du = Desktop(backend="uia")
ru = du.window(handle=RADAR)
# switch to 觸發商品 tab (SysTabControl32 17003) via uia select
try:
    tabs = ru.descendants(control_type="TabItem")
    for t in tabs:
        if "觸發" in t.window_text():
            t.select()
            print("switched to 觸發商品 tab")
            time.sleep(1.5)
            break
except Exception as e:
    print("tab err:", str(e)[:80])

# read tree 33035 (uia Tree) — HH:MM:SS(N) nodes
try:
    tree = ru.child_window(control_id=33035, class_name="SysTreeView32")
    print("trigger tree exists:", tree.exists(timeout=2))
    if tree.exists(timeout=1):
        du2 = Desktop(backend="uia")
        tw = du2.window(handle=RADAR)
        trees = [t for t in tw.descendants(control_type="Tree")]
        for t in trees:
            for item in t.descendants(control_type="TreeItem"):
                txt = item.window_text()
                if txt.strip():
                    print("  TREE:", repr(txt[:40]))
except Exception as e:
    print("tree err:", str(e)[:100])
