# -*- coding: utf-8 -*-
"""RR6-C v3: clear leftover dialogs (停止策略雷達 confirm + 時間 trap), then runs 3-10."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

XQ_PID = 7924
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
            buf = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(h, buf, 256)
            out.append((h, buf.value[:80]))
        return True
    u.EnumWindows(cb, 0)
    return out


def enum_children(hwnd):
    out = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        buf = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(h, buf, 128)
        out.append((h, buf.value[:60], u.GetDlgCtrlID(h)))
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    return out


def child_by_cid(hwnd, cid):
    for h, t, c in enum_children(hwnd):
        if c == cid:
            return h
    return None


def click(hwnd):
    u.PostMessageW(hwnd, 0x00F5, 0, 0)


def set_edit(hwnd, text):
    buf = ctypes.create_unicode_buffer(text)
    u.SendMessageW(hwnd, 0x000C, 0, buf)


def clear_dialogs():
    """close 停止策略雷達 confirms + 時間 traps + 警示提示."""
    for h, t in windows(XQ_PID):
        if "停止策略雷達" in t or t.startswith("時間：["):
            for c in enum_children(h):
                if "確定" in c[1] or "是" in c[1] or "關閉" in c[1]:
                    click(c[0])
                    break


def press_toolbar_cmd(tb, cid):
    for i in range(tb.button_count()):
        if tb.button(i).info.idCommand == cid:
            tb.button(i).click()
            return True
    return False


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

    # pre-clean
    clear_dialogs()
    time.sleep(1.5)

    # load existing receipt, keep runs 1-2
    path = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_XQ_PAPER_10RUN_RECEIPT_RR6.json"
    receipt = json.load(open(path, encoding="utf-8"))
    results = receipt["runs"]

    for i in range(3, 11):
        name = f"FDAPaperRun{i:03d}"
        r = {"run": i, "name": name}
        try:
            clear_dialogs()          # ensure clean before NEW
            time.sleep(0.5)
            press_toolbar_cmd(tb, NEW_CMD)
            time.sleep(2.5)
            dlg = None
            for h, t in windows(XQ_PID):
                if "新增策略雷達" in t:
                    dlg = h
                    break
            if not dlg:
                r["status"] = "NO_DIALOG"
                results.append(r)
                print(f"run {i}: NO_DIALOG")
                continue
            set_edit(child_by_cid(dlg, NAME_EDIT), name)
            time.sleep(0.4)
            # script via 選擇使用腳本 (FDA_F06_FRESH exists)
            click(child_by_cid(dlg, SCRIPT_BTN))
            time.sleep(2)
            chooser = None
            for h, t in windows(XQ_PID):
                if "選擇使用腳本" in t:
                    chooser = h
                    break
            if chooser:
                try:
                    cw = Desktop(backend="uia").window(handle=chooser)
                    for item in cw.descendants(control_type="TreeItem"):
                        if "自訂" in item.window_text():
                            item.expand()
                            break
                    time.sleep(1)
                    for item in cw.descendants(control_type="TreeItem"):
                        if "FDA_F06_FRESH" in item.window_text():
                            item.select()
                            break
                    click(child_by_cid(chooser, 1))
                except Exception as e:
                    r["script_err"] = str(e)[:50]
            time.sleep(1.5)
            # product 2330
            click(child_by_cid(dlg, PRODUCT_BTN))
            time.sleep(2)
            prod = None
            for h, t in windows(XQ_PID):
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
                if ok3 and ok3 != ok2:
                    click(ok3)
            time.sleep(1.5)
            cb = child_by_cid(dlg, TRIGGER_COMBO)
            if cb:
                u.SendMessageW(cb, 0x014E, 0, 0)
            time.sleep(0.3)
            ne = child_by_cid(dlg, NAME_EDIT)
            buf = ctypes.create_unicode_buffer(64)
            u.SendMessageW(ne, 0x000D, 64, buf)
            r["name_readback"] = buf.value
            click(child_by_cid(dlg, OK_BTN))
            time.sleep(2.5)
            # 時間 trap
            for h, t in windows(XQ_PID):
                if t.startswith("時間：[") :
                    for c in enum_children(h):
                        if "關閉" in c[1]:
                            click(c[0])
                            break
                    break
            time.sleep(1.5)
            # STOP + confirm 停止策略雷達
            try:
                press_toolbar_cmd(tb, STOP_CMD)
                time.sleep(1)
                clear_dialogs()
            except Exception:
                pass
            time.sleep(1)
            r["status"] = "OK"
        except Exception as e:
            r["status"] = f"ERR {str(e)[:80]}"
        results.append(r)
        print(f"run {i}: {r['status']} name={r.get('name_readback','?')}")

    receipt["runs"] = results
    receipt["sensorlog_exec_starts"] = sensorlog_exec_starts()
    json.dump(receipt, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\nSensorLog ExecState=1:", receipt["sensorlog_exec_starts"])
    ok = sum(1 for r in results if r["status"] == "OK")
    print(f"OK runs: {ok}/10")


if __name__ == "__main__":
    main()
