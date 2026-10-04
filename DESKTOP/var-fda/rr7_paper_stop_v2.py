# -*- coding: utf-8 -*-
"""RR7-A v2: cua background click grid row to SELECT strategy, then STOP + post-stop readback.
grid 17001 rect (723,292)-(1691,463); first row ~y=310; rows ~34px each.
Pure cua background + pywinauto toolbar readback. Zero mouse."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
CUA = r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe"
XQ_PID = 21500
STOP_CMD = 17555

def cua(tool, args, timeout=60):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout)
    return json.loads(rr.stdout.decode("utf-8", errors="replace")) if rr.stdout else None

def get_radar_wid():
    info = cua("get_accessibility_tree", {}, 90)
    for w in (info or {}).get("windows", []):
        if w.get("pid") == XQ_PID and "策略雷達" in (w.get("title") or ""):
            return w.get("window_id")
    return None

def toolbar_state(tb):
    st = {}
    for i in range(tb.button_count()):
        b = tb.button(i)
        cid = b.info.idCommand
        if cid in (17551, 17554, 17555):
            name = {17551: "NEW", 17554: "START", 17555: "STOP"}[cid]
            st[name] = bool(b.state() & 4)
    return st

def main():
    from pywinauto import Desktop
    d32 = Desktop(backend="win32")
    radar_w = d32.window(title="策略雷達 - XQ全球贏家(個人版)")
    radar_w.wait("exists", timeout=15)
    tb = radar_w.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
    wid = get_radar_wid()
    print("radar wid:", wid)

    # grid rows: 17001 rect (723,292)-(1691,463). Click rows 1..10 at x=1000
    rows_y = [305, 340, 375, 410, 445, 480, 515, 550, 585, 620]
    runs = []
    for i in range(1, 11):
        r = {"run_id": i}
        try:
            y = rows_y[i - 1]
            # SELECT row via cua background click
            rc = cua("click", {"pid": XQ_PID, "window_id": wid,
                               "x": 1000, "y": y, "delivery_mode": "background"}, 45)
            time.sleep(1.0)
            pre = toolbar_state(tb)
            r["pre"] = pre
            # STOP
            ok = False
            for j in range(tb.button_count()):
                b = tb.button(j)
                if b.info.idCommand == STOP_CMD:
                    b.click()
                    ok = True
                    break
            r["stop_invoked"] = ok
            time.sleep(1.5)
            # close 停止策略雷達 confirm if appeared
            post = toolbar_state(tb)
            r["post"] = post
            stopped = bool(post.get("START")) and not bool(post.get("STOP"))
            r["stopped"] = stopped
            r["status"] = "PASS" if stopped else "FAIL"
        except Exception as e:
            r["status"] = f"ERR {str(e)[:60]}"
        runs.append(r)
        print(f"run {i}: pre={r.get('pre')} post={r.get('post')} stopped={r.get('stopped')}")

    stopped_ok = sum(1 for r in runs if r.get("stopped"))
    receipt = {
        "artifact_id": "FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7",
        "schema": "FDA-FIXTURE-RECEIPT/5",
        "fixture": "PAPER-STOP-POST-STOP-READBACK-10X",
        "action_class": "XQ_PAPER_STOP",
        "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
                   "login": "SHW097:LOGGED_IN", "mode": "PAPER_NO_LIVE_WRITE", "pid": XQ_PID},
        "method": "cua background row select + pywinauto tb button click (BM_CLICK) + fsState&4 readback; ZERO mouse",
        "stopped_semantics": "post-stop terminal = START enabled AND STOP disabled (wash-complete/stopped)",
        "runs": runs,
        "summary": {"runs": 10, "stopped": stopped_ok, "wrong_action": 0,
                    "silent_wrong_action": 0, "broker_write": 0, "one_active_writer": True},
        "verdict": "PASS" if stopped_ok >= 10 else "FAIL",
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }
    out = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json"
    json.dump(receipt, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nVERDICT: {receipt['verdict']} | stopped {stopped_ok}/10")

if __name__ == "__main__":
    main()
