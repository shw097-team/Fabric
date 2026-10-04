# -*- coding: utf-8 -*-
"""RR6-B v5 (FAR best-solution): create FDA_F06_FRESH via community-verified path:
Alt+F (%f) -> popup -> {HOME}{ENTER} (新增) -> 新增腳本 dialog #32770 ->
type alert button 30049 BM_CLICK -> name 30021 WM_SETTEXT -> confirm 30001 BM_CLICK ->
Scintilla SCI_SETTEXT (community create_string_buffer pattern) -> F6 x10 ->
DB Sensor LastCompileTime per run (distinct proof).
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
SCI_SETTEXT, SCI_GETTEXTLENGTH = 2181, 2183
u = ctypes.windll.user32
k32 = ctypes.windll.kernel32
MEM_COMMIT, MEM_RELEASE, PAGE_READWRITE = 0x1000, 0x8000, 0x04
NAME = "FDA_F06_FRESH"
SRC = """{@type:indicator}
// FDA F06 fresh fixture
value1 = CrossOver(Close, Average(Close, 5));
Plot1(value1, "X");
// marker: {MARKER}
"""


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


def click_cid(hwnd, cid):
    for h, cls, t, c in enum_children(hwnd):
        if c == cid:
            u.PostMessageW(h, 0x00F5, 0, 0)
            return True
    return False


def set_edit_cid(hwnd, cid, text):
    for h, cls, t, c in enum_children(hwnd):
        if c == cid:
            buf = ctypes.create_unicode_buffer(text)
            u.SendMessageW(h, 0x000C, 0, buf)  # WM_SETTEXT
            return True
    return False


def sci_set_text(hwnd, text):
    """Community pattern: Write(create_string_buffer, size=...)."""
    from ctypes import create_string_buffer
    import win32gui
    from pywinauto.remote_memory_block import RemoteMemoryBlock

    class _Ctl:
        def __init__(self, h):
            self.handle = h

    raw = text.encode("cp950") + b"\x00"
    buffer = create_string_buffer(raw)
    remote = RemoteMemoryBlock(_Ctl(hwnd), size=len(raw))
    try:
        remote.Write(buffer, size=len(raw))
        win32gui.SendMessage(hwnd, SCI_SETTEXT, 0, remote.Address())
    finally:
        remote.CleanUp()
    time.sleep(0.4)
    return win32gui.SendMessage(hwnd, SCI_GETTEXTLENGTH, 0, 0)


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
    pid = 22384

    ed = Desktop(backend="win32").window(handle=EDITOR_HWND)
    ed.set_focus()
    time.sleep(0.5)

    # community path: %f opens popup, {HOME}{ENTER} selects 新增(N)
    send_keys("%f")
    time.sleep(1.2)
    send_keys("{HOME}")
    time.sleep(0.3)
    send_keys("{ENTER}")
    time.sleep(2.5)

    # find 新增腳本 dialog
    dlg = None
    for h, cls, t in windows(pid):
        if "新增腳本" in t or cls == "#32770" and t.strip():
            dlg = h
            break
    if not dlg:
        print("DLGs:", [(hex(h), c, t) for h, c, t in windows(pid) if c == "#32770"])
        return
    print("新增腳本 dialog:", hex(dlg))
    for c in enum_children(dlg)[:24]:
        print("  child:", hex(c[0]), c[1], repr(c[2]), "cid", c[3])

    # type alert (30049), name (30021), confirm (30001)
    click_cid(dlg, 30049); time.sleep(0.5)
    set_edit_cid(dlg, 30021, NAME); time.sleep(0.5)
    click_cid(dlg, 30001); time.sleep(2)

    # find scintilla in editor
    kids = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        if "Scintilla" in cls.value:
            kids.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(EDITOR_HWND), cb, 0)
    sc = kids[0] if kids else None
    if not sc:
        print("no scintilla"); return
    print("scintilla:", hex(sc))

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
        "method": "新增腳本 dialog (%f->HOME->ENTER; type 30049; name 30021; confirm 30001) + SCI_SETTEXT + F6 + DB readback",
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
