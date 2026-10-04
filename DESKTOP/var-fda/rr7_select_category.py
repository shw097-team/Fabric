# -*- coding: utf-8 -*-
"""RR7-A v3: select 執行中/自訂 category (uia pattern) then cua bg click first row, STOP, readback.
Debug single run first."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
CUA = r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe"
XQ_PID = 21500

def cua(tool, args, timeout=60):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else None

def main():
    from pywinauto import Desktop
    d32 = Desktop(backend="uia")
    radar = d32.window(title="策略雷達 - XQ全球贏家(個人版)")
    radar.wait("exists", timeout=15)
    # find 執行中 TreeItem and select (pattern, no mouse)
    items = radar.descendants(control_type="TreeItem")
    print("tree items:", len(items))
    for it in items:
        t = it.window_text()
        if "執行中" in t:
            print("found 執行中, select...")
            try:
                it.select()
                print("selected OK")
            except Exception as e:
                print("select err:", str(e)[:60])
            break
    time.sleep(2)
    # toolbar state after category select
    d32w = Desktop(backend="win32")
    rw = d32w.window(title="策略雷達 - XQ全球贏家(個人版)")
    tb = rw.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
    st = {}
    for i in range(tb.button_count()):
        b = tb.button(i); cid = b.info.idCommand
        if cid in (17551,17554,17555): st[{17551:'NEW',17554:'START',17555:'STOP'}[cid]] = bool(b.state()&4)
    print("toolbar after category:", st)

if __name__ == "__main__":
    main()
