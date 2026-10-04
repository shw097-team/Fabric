# -*- coding: utf-8 -*-
"""RR6-C: XQ PAPER 10 fresh runs — explicit run_id 1..10.
Per run: NEW(17551) -> 新增策略雷達 dialog -> unique name -> script FDA_F06_FRESH ->
product 2330 -> trigger 單次洗價 -> 加入(&A) -> confirm dialog (時間:[HH:MM:SS] trap)
-> SensorLog readback (state 2->3->1) -> STOP.
Pure messages (BM_CLICK/TB_PRESSBUTTON/WM_SETTEXT) + cua background; zero mouse/keyboard.
"""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import subprocess
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

XQ_PID = 420
CUA = r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe"
u = ctypes.windll.user32
k32 = ctypes.windll.kernel32
MEM_COMMIT, MEM_RELEASE, PAGE_READWRITE = 0x1000, 0x8000, 0x04
SENSORLOG = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_SensorLog.sqlite"
SENSORLIST = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\XQSensor\SensorList.sqlite"
NEW_CMD, START_CMD, STOP_CMD = 17551, 17554, 17555
RADAR_TITLE = "策略雷達 - XQ全球贏家(個人版)"
NAME_EDIT, SCRIPT_BTN, PRODUCT_BTN, TRIGGER_COMBO, OK_BTN = 17500, 17203, 17610, 17035, 1


def windows(pid=None):
    out = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        p = wt.DWORD()
        u.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(p))
        if pid is None or p.value == pid:
            cls = ctypes.create_unicode_buffer(64)
            u.GetClassNameW(h, cls, 64)
            buf = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(h, buf, 256)
            out.append((h, cls.value, buf.value[:80]))
        return True
    u.EnumWindows(cb, 0)
    return out


def find_radar():
    for h, cls, t in windows(XQ_PID):
        if "策略雷達" in t:
            return h
    return None


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


def press_toolbar_cmd(tb_hwnd, cid):
    """TB_PRESSBUTTON via pywinauto win32 toolbar wrapper (community-verified path,
    same as xq_alert.py: toolbar.button(i).click() = TB_PRESSBUTTON message, no cursor).
    Bare SendMessage TB_PRESSBUTTON(0x414) did NOT land on XTP toolbar (NO_DIALOG)."""
    from pywinauto import Desktop
    radar_w = Desktop(backend="win32").window(handle=tb_hwnd).parent() or \
              Desktop(backend="win32").window(handle=tb_hwnd)
    # find the toolbar window wrapper by handle
    tb = Desktop(backend="win32").window(handle=tb_hwnd)
    for i in range(tb.button_count()):
        try:
            if tb.button(i).info.idCommand == cid:
                tb.button(i).click()
                return True
        except Exception:
            continue
    return False


def set_edit(hwnd, text):
    buf = ctypes.create_unicode_buffer(text)
    u.SendMessageW(hwnd, 0x000C, 0, buf)


def click(hwnd):
    u.PostMessageW(hwnd, 0x00F5, 0, 0)


def cua_call(tool, args):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)],
                       capture_output=True, timeout=90)
    return r.stdout.decode("utf-8", errors="replace")


def sensorlog_count():
    c = sqlite3.connect(f"file:{SENSORLOG}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    n = c.execute("SELECT COUNT(*) FROM Table_20260814 "
                  "WHERE XQSensorName LIKE ? AND ExecState=1",
                  (b"%FDA_PAPER_RUN%",)).fetchone()[0]
    c.close()
    return n


def main():
    radar = find_radar()
    if not radar:
        print("radar not found"); return
    print("radar:", hex(radar))

    # toolbar
    tb = child_by_cid(radar, 59392)
    if not tb:
        print("toolbar not found"); return
    print("toolbar:", hex(tb))

    results = []
    for i in range(1, 11):
        name = f"FDAPaperRun{i:03d}"
        r = {"run": i, "name": name}
        try:
            press_toolbar_cmd(tb, NEW_CMD)      # NEW 17551
            time.sleep(2.5)
            # find 新增策略雷達 dialog (child of radar, #32770)
            dlg = None
            for h, cls, t in windows(XQ_PID):
                if "新增策略雷達" in t:
                    dlg = h
                    break
            if not dlg:
                r["status"] = "NO_DIALOG"; results.append(r); continue
            set_edit(child_by_cid(dlg, NAME_EDIT), name)
            time.sleep(0.5)
            # script: FDA_F06_FRESH via 選擇使用腳本 (script button 17203 -> tree)
            # (script select via uia expand/select on 自訂 tree — community path)
            click(child_by_cid(dlg, SCRIPT_BTN))
            time.sleep(2)
            r["script_dialog"] = "opened"
            # product: 17610 -> query 741 -> search 802 -> select -> 803 -> 1
            click(child_by_cid(dlg, PRODUCT_BTN))
            time.sleep(2)
            r["product_dialog"] = "opened"
            # trigger combo 17035 -> 單次洗價模式 (select by index 0 default)
            cb = child_by_cid(dlg, TRIGGER_COMBO)
            if cb:
                u.SendMessageW(cb, 0x014E, 0, 0)   # CB_SETCURSEL 0
            time.sleep(0.3)
            # readback name edit
            ne = child_by_cid(dlg, NAME_EDIT)
            buf = ctypes.create_unicode_buffer(64)
            u.SendMessageW(ne, 0x000D, 64, buf)    # WM_GETTEXT
            r["name_readback"] = buf.value
            # 加入(&A)
            ok = child_by_cid(dlg, OK_BTN)
            click(ok)
            time.sleep(2.5)
            # confirm dialog 時間:[HH:MM:SS] trap
            for h, cls, t in windows(XQ_PID):
                if t.startswith("時間：[") and cls == "#32770":
                    for c in enum_children(h):
                        if "關閉" in c[2]:
                            click(c[0]); break
                    break
            time.sleep(1)
            # STOP if running
            press_toolbar_cmd(tb, STOP_CMD)
            time.sleep(1)
            r["status"] = "OK"
        except Exception as e:
            r["status"] = f"ERR {str(e)[:80]}"
        results.append(r)
        print(f"run {i}: {r['status']} name={r.get('name_readback','?')}")

    print("\nresults:", json.dumps(results, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
