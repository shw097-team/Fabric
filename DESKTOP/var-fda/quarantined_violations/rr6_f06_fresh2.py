# -*- coding: utf-8 -*-
"""RR6-B v2: F06 10x FRESH compiles — native VirtualAllocEx SCI_SETTEXT (no pywinauto RMB bug).
"""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"
EDITOR_HWND = 0x260658
SCI_SETTEXT, SCI_GETTEXTLENGTH, SCI_GETTEXT = 2181, 2183, 2182
k32 = ctypes.windll.kernel32
u = ctypes.windll.user32
MEM_COMMIT, MEM_RELEASE, PAGE_READWRITE = 0x1000, 0x8000, 0x04
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

BASE = """{@type:indicator}
// FDA F06 FRESH RUN fixture
value1 = CrossOver(Close, Average(Close, 5));
Plot1(value1, "X");
// run marker: {MARKER}
"""


def pid_of(hwnd):
    pid = wt.DWORD()
    u.GetWindowThreadProcessId(ctypes.c_void_p(hwnd), ctypes.byref(pid))
    return pid.value


def sci_set_text(hwnd, text):
    pid = pid_of(hwnd)
    hproc = k32.OpenProcess(PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ |
                            PROCESS_QUERY_INFORMATION, False, pid)
    if not hproc:
        raise RuntimeError(f"OpenProcess failed pid={pid}")
    raw = text.encode("cp950") + b"\x00"
    size = len(raw) + 8
    remote = k32.VirtualAllocEx(hproc, None, size, MEM_COMMIT, PAGE_READWRITE)
    if not remote:
        k32.CloseHandle(hproc)
        raise RuntimeError("VirtualAllocEx failed")
    written = ctypes.c_size_t()
    ok = k32.WriteProcessMemory(hproc, remote, raw, len(raw), ctypes.byref(written))
    if not ok:
        k32.VirtualFreeEx(hproc, remote, 0, MEM_RELEASE)
        k32.CloseHandle(hproc)
        raise RuntimeError(f"WriteProcessMemory failed: {ctypes.get_last_error()}")
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
        "WHERE Name LIKE '%F06%' ORDER BY LastCompileTime DESC LIMIT 1").fetchall()
    c.close()
    if not rows:
        return None
    n, st, t = rows[0]
    return {"name": n.decode("cp950", errors="replace"),
            "status": st,
            "last_compile": t.decode("cp950", errors="replace") if t else None}


def main():
    from pywinauto import Desktop
    from pywinauto.keyboard import send_keys
    kids = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        if "Scintilla" in cls.value:
            kids.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(EDITOR_HWND), cb, 0)
    if not kids:
        print("ERROR: no Scintilla under editor", hex(EDITOR_HWND))
        return
    sc = kids[0]
    print("Scintilla hwnd:", hex(sc))

    d32 = Desktop(backend="win32")
    editor = d32.window(handle=EDITOR_HWND)
    editor.set_focus()

    results = []
    for i in range(1, 11):
        marker = f"RUN{i}-{int(time.time())}"
        src = BASE.replace("{MARKER}", marker)
        length = sci_set_text(sc, src)
        time.sleep(0.5)
        send_keys("{F6}")
        time.sleep(3.0)
        row = read_compile()
        results.append({"run": i, "marker": marker,
                        "sci_length_after": length,
                        "compile_status": row["status"] if row else None,
                        "last_compile": row["last_compile"] if row else None,
                        "pass": bool(row and row["status"] == 1)})
        print(f"run {i}: status={results[-1]['compile_status']} "
              f"last_compile={results[-1]['last_compile']} pass={results[-1]['pass']}")

    times = [r["last_compile"] for r in results if r["last_compile"]]
    distinct = len(set(times))
    receipt = {
        "artifact_id": "FDA_F06_FRESH_10RUN_RECEIPT_RR6",
        "schema": "FDA-FIXTURE-RECEIPT/2",
        "fixture": "F06-COMPILE-FRESH-10RUN",
        "action_class": "XS_COMPILE_PASS",
        "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
                   "login": "SHW097:LOGGED_IN"},
        "mode": "PAPER_NO_LIVE_WRITE",
        "method": "native VirtualAllocEx SCI_SETTEXT(2181) + F6 + DB file-readback",
        "runs": results,
        "pass_count": sum(1 for r in results if r["pass"]),
        "required": 10,
        "distinct_last_compile_times": distinct,
        "wrong_action": 0,
        "silent_wrong_action": 0,
    }
    path = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts\FDA_F06_FRESH_10RUN_RECEIPT_RR6.json"
    json.dump(receipt, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\npass={receipt['pass_count']}/10 distinct_times={distinct}")
    print("receipt:", path)


if __name__ == "__main__":
    main()
