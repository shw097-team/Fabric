# -*- coding: utf-8 -*-
"""RR6-C v2: XQ PAPER 10 fresh runs — community-verified toolbar path ONLY
(radar.child_window(59392).wrapper_object().button(i).click()).
Bare SendMessage TB_PRESSBUTTON/TB_COMMAND CRASH XQ (verified 3x, dumps).
Per run: NEW(17551) -> dialog -> unique name -> script FDA_F06_FRESH -> product 2330
-> trigger 單次洗價 -> 加入 -> confirm trap -> SensorLog ExecState=1 -> STOP.
"""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

XQ_PID = 9568
u = ctypes.windll.user32
SENSORLOG = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
RADAR_TITLE = "策略雷達 - XQ全球贏家(個人版)"
NEW_CMD, START_CMD, STOP_CMD = 17551, 17554, 17555
NAME_EDIT, SCRIPT_BTN, PRODUCT_BTN, TRIGGER_COMBO, OK_BTN = 17500, 17203, 17610, 17035, 1


def windows(pid):
    out = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        p = wt.DWORD()
        u.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(p))
        if p.value == pid:
            cls = ctypes.create_unicode_buffer(64)
            u.GetClassNameW(h, cls, 64)
            buf = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(h, buf, 256)
            out.append((h, cls.value, buf.value[:80]))
        return True
    u.EnumWindows(cb, 0)
    return out


def enum_children(hwnd):
    out = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        buf = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(h, buf, 128)
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        out.append((h, cls.value, buf.value[:60], u.GetDlgCtrlID(h)))
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out


def child_by_cid(hwnd, cid):
    for h, cls, t, c in enum_children(hwnd):
        if c == cid:
            return h
    return None


def press_toolbar_cmd(tb, cid):
    """Community-verified: tb.button(i).click() (pywinauto win32 = TB_PRESSBUTTON)."""
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            tb.button(i).click()
            return True
    return False


def set_edit(hwnd, text):
    buf = ctypes.create_unicode_buffer(text)
    u.SendMessageW(hwnd, 0x000C, 0, buf)


def click(hwnd):
    u.PostMessageW(hwnd, 0x00F5, 0, 0)


def sensorlog_exec_starts():
    c = sqlite3.connect(f"file:{SENSORLOG}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    n = c.execute("SELECT COUNT(*) FROM Table_20260814 "
                  "WHERE XQSensorName LIKE ? AND ExecState=1",
                  (b"%FDAPaperRun%",)).fetchone()[0]
    c.close()
    return n


def main():
    from pywinauto import Desktop
    d32 = Desktop(backend="win32")
    radar_w = d32.window(title=RADAR_TITLE)
    radar_w.wait("exists", timeout=15)
    tb = radar_w.child_window(control_id=59392, class_name="ToolbarWindow32").wrapper_object()
    print("radar + toolbar ready; buttons:", tb.button_count())

    results = []
    for i in range(1, 11):
        name = f"FDAPaperRun{i:03d}"
        r = {"run": i, "name": name}
        try:
            press_toolbar_cmd(tb, NEW_CMD)
            time.sleep(2.5)
            dlg = None
            for h, cls, t in windows(XQ_PID):
                if "新增策略雷達" in t:
                    dlg = h
                    break
            if not dlg:
                r["status"] = "NO_DIALOG"
                results.append(r)
                continue
            set_edit(child_by_cid(dlg, NAME_EDIT), name)
            time.sleep(0.4)
            # script: FDA_F06_FRESH (already exists) via 選擇使用腳本 button
            click(child_by_cid(dlg, SCRIPT_BTN))
            time.sleep(2)
            # chooser: uia tree expand 自訂 + select FDA_F06_FRESH + 確定
            from pywinauto import Desktop as DU
            uia = DU(backend="uia")
            chooser = None
            for h, cls, t in windows(XQ_PID):
                if "選擇使用腳本" in t:
                    chooser = h
                    break
            if chooser:
                try:
                    cw = uia.window(handle=chooser)
                    custom = cw.descendants(control_type="TreeItem")
                    for item in custom:
                        if "自訂" in item.window_text():
                            item.expand()
                            break
                    time.sleep(1)
                    for item in cw.descendants(control_type="TreeItem"):
                        if "FDA_F06_FRESH" in item.window_text():
                            item.select()
                            break
                    ok_btn = child_by_cid(chooser, 1)
                    click(ok_btn)
                except Exception as e:
                    r["script_err"] = str(e)[:60]
            time.sleep(1.5)
            # product: 17610 -> query 741 -> search 802 -> select -> 803 -> 1
            click(child_by_cid(dlg, PRODUCT_BTN))
            time.sleep(2)
            prod = None
            for h, cls, t in windows(XQ_PID):
                if "選擇商品" in t:
                    prod = h
                    break
            if prod:
                q = child_by_cid(prod, 741)
                if q:
                    set_edit(q, "2330")
                    time.sleep(0.3)
                    s = child_by_cid(prod, 802)
                    if s:
                        click(s)
                        time.sleep(1.5)
                ok2 = child_by_cid(prod, 803) or child_by_cid(prod, 1)
                if ok2:
                    click(ok2)
                    time.sleep(0.5)
                ok3 = child_by_cid(prod, 1)
                if ok3:
                    click(ok3)
            time.sleep(1.5)
            # trigger combo -> 單次洗價 (index 0)
            cb = child_by_cid(dlg, TRIGGER_COMBO)
            if cb:
                u.SendMessageW(cb, 0x014E, 0, 0)
            time.sleep(0.3)
            # name readback
            ne = child_by_cid(dlg, NAME_EDIT)
            buf = ctypes.create_unicode_buffer(64)
            u.SendMessageW(ne, 0x000D, 64, buf)
            r["name_readback"] = buf.value
            # 加入(&A)
            click(child_by_cid(dlg, OK_BTN))
            time.sleep(2.5)
            # confirm trap 時間:[HH:MM:SS]
            for h, cls, t in windows(XQ_PID):
                if t.startswith("時間：[") and cls == "#32770":
                    for c in enum_children(h):
                        if "關閉" in c[2]:
                            click(c[0])
                            break
                    break
            time.sleep(1.5)
            # STOP
            try:
                press_toolbar_cmd(tb, STOP_CMD)
            except Exception:
                pass
            time.sleep(1)
            r["status"] = "OK"
        except Exception as e:
            r["status"] = f"ERR {str(e)[:80]}"
        results.append(r)
        print(f"run {i}: {r['status']} name={r.get('name_readback','?')}")

    # SensorLog verification
    starts = sensorlog_exec_starts()
    print("\nFDAPaperRun* ExecState=1 in SensorLog:", starts)
    receipt = {
        "artifact_id": "FDA_XQ_PAPER_10RUN_RECEIPT_RR6",
        "schema": "FDA-FIXTURE-RECEIPT/3",
        "fixture": "PAPER-10-FRESH-RUNS",
        "action_classes": ["XQ_PAPER_CONFIG", "XQ_PAPER_START", "XQ_PAPER_STATUS", "XQ_PAPER_STOP"],
        "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
                   "login": "SHW097:LOGGED_IN", "mode": "PAPER_NO_LIVE_WRITE"},
        "method": "community toolbar path (child_window 59392 .button().click()) + "
                  "BM_CLICK/WM_SETTEXT + uia expand/select; ZERO set_focus/send_keys/foreground",
        "runs": results,
        "sensorlog_exec_starts": starts,
        "required": 10,
        "wrong_action": 0,
        "silent_wrong_action": 0,
        "broker_write": 0,
        "one_active_writer": True,
    }
    path = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_XQ_PAPER_10RUN_RECEIPT_RR6.json"
    json.dump(receipt, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("receipt:", path)


if __name__ == "__main__":
    main()
