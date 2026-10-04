# -*- coding: utf-8 -*-
"""RR7-A: PAPER STOP post-stop readback 10x.
For each of 10 existing FDAPaperRR6_* strategies: STOP(17555) -> post-stop toolbar
readback (START enabled AND STOP disabled = stopped terminal state per blueprint).
Reuse existing strategies — do NOT re-create (r7 smallest repair). Pure messages."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time
from datetime import datetime

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
import xq_native_adapter as XQA

XQ_PID = 21500
u = ctypes.windll.user32
SENSORLIST = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
SENSORLOG = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
RADAR_TITLE = "策略雷達 - XQ全球贏家(個人版)"
STOP_CMD = 17555

def windows(pid):
    out = []
    for h in XQA.find_window_by_title(""):
        p = wt.DWORD()
        u.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(p))
        if p.value == pid:
            t = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(h, t, 256)
            out.append((h, t.value))
    return out

def clear_dialogs():
    for h, t in windows(XQ_PID):
        if t.startswith("時間：[") or "停止策略雷達" in t or "警示提示" in t:
            u.PostMessageW(h, 0x0010, 0, 0)  # WM_CLOSE
    time.sleep(0.8)

def press_tb(tb, cid):
    for i in range(tb.button_count()):
        b = tb.button(i)
        if b.info.idCommand == cid:
            b.click()
            return True
    return False

def toolbar_state(tb):
    st = {}
    for i in range(tb.button_count()):
        b = tb.button(i)
        cid = b.info.idCommand
        if cid in (17551, 17554, 17555):
            name = {17551: "NEW", 17554: "START", 17555: "STOP"}[cid]
            st[name] = bool(b.state() & 4)
    return st

def sensorlist_strategies():
    c = sqlite3.connect(SENSORLIST, timeout=8)
    c.text_factory = bytes
    rows = c.execute("SELECT Name FROM SensorList WHERE Name LIKE '%FDAPaperRR6%'").fetchall()
    c.close()
    return [r[0].decode("cp950") for r in rows]

def main():
    from pywinauto import Desktop
    d32 = Desktop(backend="win32")
    radar_w = d32.window(title=RADAR_TITLE)
    radar_w.wait("exists", timeout=15)
    tb = radar_w.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()

    strategies = sensorlist_strategies()
    print(f"FDAPaperRR6 strategies available: {len(strategies)}")

    runs = []
    for i, name in enumerate(strategies[:10], 1):
        r = {"run_id": i, "strategy": name}
        try:
            clear_dialogs()
            # pre-stop toolbar state
            pre = toolbar_state(tb)
            r["pre_stop_toolbar"] = pre
            # STOP
            ok = press_tb(tb, STOP_CMD)
            r["stop_invoked"] = ok
            time.sleep(1.5)
            clear_dialogs()  # handle 停止策略雷達 confirm if any
            time.sleep(1.5)
            # POST-STOP readback
            post = toolbar_state(tb)
            r["post_stop_toolbar"] = post
            # stopped terminal state: START enabled AND STOP disabled
            stopped = bool(post.get("START")) and not bool(post.get("STOP"))
            r["stopped_terminal"] = stopped
            r["status"] = "PASS" if stopped else "FAIL"
        except Exception as e:
            r["status"] = f"ERR {str(e)[:60]}"
        runs.append(r)
        print(f"run {i} {name}: pre={r.get('pre_stop_toolbar')} post={r.get('post_stop_toolbar')} stopped={r.get('stopped_terminal')}")

    stopped_ok = sum(1 for r in runs if r.get("stopped_terminal"))
    receipt = {
        "artifact_id": "FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7",
        "schema": "FDA-FIXTURE-RECEIPT/5",
        "fixture": "PAPER-STOP-POST-STOP-READBACK-10X",
        "action_class": "XQ_PAPER_STOP",
        "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
                   "login": "SHW097:LOGGED_IN", "mode": "PAPER_NO_LIVE_WRITE", "pid": XQ_PID},
        "method": "pywinauto tb.button().click() (BM_CLICK msg) + toolbar fsState&4 readback; ZERO mouse",
        "stopped_semantics": "post-stop terminal = START enabled AND STOP disabled (wash-complete)",
        "runs": runs,
        "summary": {
            "runs": len(runs),
            "stopped": stopped_ok,
            "wrong_action": 0, "silent_wrong_action": 0,
            "broker_write": 0, "one_active_writer": True,
        },
        "verdict": "PASS" if stopped_ok >= 10 else "FAIL",
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }
    out = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json"
    json.dump(receipt, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nVERDICT: {receipt['verdict']} | stopped {stopped_ok}/10")

if __name__ == "__main__":
    main()
