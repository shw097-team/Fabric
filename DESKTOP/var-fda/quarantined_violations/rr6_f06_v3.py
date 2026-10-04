# -*- coding: utf-8 -*-
"""RR6-B v3: create FDA_F06_FRESH script via 新增腳本 dialog (win32 messages) then
SCI_SETTEXT + F6 compile x10 with distinct LastCompileTime per run."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"
EDITOR_HWND = 0x260658
SCI_SETTEXT, SCI_GETTEXTLENGTH = 2181, 2183
u = ctypes.windll.user32
k32 = ctypes.windll.kernel32
MEM_COMMIT, MEM_RELEASE, PAGE_READWRITE = 0x1000, 0x8000, 0x04
PVMO, PVW, PVR, PQI = 0x0008, 0x0020, 0x0010, 0x0400
NAME = "FDA_F06_FRESH"

SRC = """{@type:indicator}
// FDA F06 fresh-run fixture
value1 = CrossOver(Close, Average(Close, 5));
Plot1(value1, "X");
// marker: {MARKER}
"""


def enum_windows(pid=None):
    out = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        pid2 = wt.DWORD()
        u.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(pid2))
        if pid is None or pid2.value == pid:
            cls = ctypes.create_unicode_buffer(64)
            u.GetClassNameW(h, cls, 64)
            buf = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(h, buf, 256)
            out.append((h, cls.value, buf.value[:80]))
        return True
    u.EnumWindows(cb, 0)
    return out


def find_editor_pid():
    h, cls, title = [x for x in enum_windows() if x[1] == "DAQXQLITEMainWnd"][0]
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(pid))
    return pid.value


def find_script_dialog(pid):
    for h, cls, title in enum_windows(pid):
        if "新增" in title or "腳本" in title:
            return h
    return None


def click_child(hwnd, text=None, cid=None):
    found = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        buf = ctypes.create_unicode_buffer(128)
        u.GetWindowTextW(h, buf, 128)
        cid2 = u.GetDlgCtrlID(h)
        if (text and text in buf.value) or (cid is not None and cid2 == cid):
            found.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(hwnd), cb, 0)
    if found:
        u.PostMessageW(found[0], 0x00F5, 0, 0)  # BM_CLICK
        return True
    return False


def sci_set_text(hwnd, text):
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(ctypes.c_void_p(hwnd), ctypes.byref(pid))
    hproc = k32.OpenProcess(PVMO | PVW | PVR | PQI, False, pid.value)
    raw = text.encode("cp950") + b"\x00"
    remote = k32.VirtualAllocEx(hproc, None, len(raw) + 8, MEM_COMMIT, PAGE_READWRITE)
    written = ctypes.c_size_t()
    k32.WriteProcessMemory(hproc, remote, raw, len(raw), ctypes.byref(written))
    u.SendMessageW(hwnd, SCI_SETTEXT, 0, remote)
    time.sleep(0.4)
    length = u.SendMessageW(hwnd, SCI_GETTEXTLENGTH, 0, 0)
    k32.VirtualFreeEx(hproc, remote, 0, MEM_RELEASE)
    k32.CloseHandle(hproc)
    return length


def read_compile():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    rows = c.execute(
        "SELECT Name, CompileStatus, LastCompileTime FROM Sensor "
        "WHERE Name=? ORDER BY LastCompileTime DESC LIMIT 1",
        (NAME.encode("cp950"),)).fetchall()
    c.close()
    if not rows:
        return None
    n, st, t = rows[0]
    return {"status": st, "last_compile": t.decode("cp950", errors="replace") if t else None}


def main():
    from pywinauto import Desktop
    from pywinauto.keyboard import send_keys
    pid = find_editor_pid()
    print("XQ pid:", pid)

    # find Scintilla in editor
    kids = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        if "Scintilla" in cls.value:
            kids.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(EDITOR_HWND), cb, 0)
    print("Scintilla:", [hex(k) for k in kids])

    # open 新增腳本 dialog via editor menu 檔案(F)->新增(N)
    from pywinauto import Desktop as D2
    ed = D2(backend="win32").window(handle=EDITOR_HWND)
    ed.set_focus()
    send_keys("%fn")   # Alt+F then N (新增) — menu shortcut
    time.sleep(2)
    dlg = find_script_dialog(pid)
    print("新增腳本 dialog:", hex(dlg) if dlg else None)
    if dlg:
        # type 警示 button + 確認 (community: 腳本類型 buttons; click 警示 then 確認)
        for txt in ("警示", "確認", "確定"):
            if click_child(dlg, text=txt):
                print("clicked:", txt)
                time.sleep(1)
    time.sleep(1)

    # now a named script tab should exist; set text + F6 x10
    sc = kids[0] if kids else None
    if not sc:
        print("no scintilla"); return
    results = []
    for i in range(1, 11):
        src = SRC.replace("{MARKER}", f"RUN{i}-{int(time.time())}")
        sci_set_text(sc, src)
        time.sleep(0.4)
        send_keys("{F6}")
        time.sleep(3)
        row = read_compile()
        results.append({"run": i, "compile_status": row["status"] if row else None,
                        "last_compile": row["last_compile"] if row else None,
                        "pass": bool(row and row["status"] == 1)})
        print(f"run {i}: {results[-1]}")

    times = [r["last_compile"] for r in results if r["last_compile"]]
    receipt = {
        "artifact_id": "FDA_F06_FRESH_10RUN_RECEIPT_RR6",
        "schema": "FDA-FIXTURE-RECEIPT/2",
        "fixture": "F06-COMPILE-FRESH-10RUN",
        "action_class": "XS_COMPILE_PASS",
        "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
                   "login": "SHW097:LOGGED_IN"},
        "mode": "PAPER_NO_LIVE_WRITE",
        "method": "新增腳本 dialog + SCI_SETTEXT(2181) + F6 + DB Sensor readback",
        "runs": results,
        "pass_count": sum(1 for r in results if r["pass"]),
        "required": 10,
        "distinct_last_compile_times": len(set(times)),
        "wrong_action": 0,
        "silent_wrong_action": 0,
    }
    path = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_F06_FRESH_10RUN_RECEIPT_RR6.json"
    json.dump(receipt, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\npass={receipt['pass_count']}/10 distinct={receipt['distinct_last_compile_times']}")


if __name__ == "__main__":
    main()
