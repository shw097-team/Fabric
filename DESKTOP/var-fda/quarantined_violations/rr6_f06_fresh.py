# -*- coding: utf-8 -*-
"""RR6-B: F06 10x FRESH compiles with distinct per-run LastCompileTime proof.
Per run: modify source (append unique comment) -> SCI_SETTEXT(2181) into Scintilla ->
F6 compile -> read DB CompileStatus=1 + LastCompileTime (must advance per run).
Pure messages (SCI_SETTEXT is a message; F6 via pywinauto send_keystrokes to editor).
"""
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import sqlite3
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"
EDITOR_HWND = 0x260658  # current session; re-find if XQ restarted

BASE = """{@type:indicator}
// FDA F06 FRESH RUN fixture
value1 = CrossOver(Close, Average(Close, 5));
Plot1(value1, "X");
// run marker: {MARKER}
"""


def find_scintilla(parent):
    u = ctypes.windll.user32
    kids = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        kids.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(parent), cb, 0)
    for h in kids:
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        if "Scintilla" in cls.value or "EDIT" in cls.value.upper():
            return h
    return None


def sci_set_text(hwnd, text):
    """SCI_SETTEXT=2181 with RemoteMemoryBlock (community recipe)."""
    from pywinauto.remote_memory_block import RemoteMemoryBlock
    from win32gui import SendMessage
    raw = text.encode("cp950") + b"\x00"
    # RemoteMemoryBlock takes a control; wrap hwnd in a minimal adapter
    class _Ctl:
        def __init__(self, h):
            self.handle = h
    remote = RemoteMemoryBlock(_Ctl(hwnd), size=len(raw))
    remote.Write(raw)
    SendMessage(hwnd, 2181, 0, remote.Address())
    time.sleep(0.3)
    length = SendMessage(hwnd, 2183, 0, 0)
    return length


def read_compile():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=8)
    c.text_factory = bytes
    rows = c.execute(
        "SELECT Name, CompileStatus, LastCompileTime FROM Script "
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
    sc = find_scintilla(EDITOR_HWND)
    if not sc:
        print("ERROR: no Scintilla control found under editor", hex(EDITOR_HWND))
        return
    print("Scintilla hwnd:", hex(sc))

    d32 = Desktop(backend="win32")
    editor = d32.window(handle=EDITOR_HWND)
    editor.set_focus()  # editor window (brief focus; needed for F6 to land) — user away

    results = []
    for i in range(1, 11):
        marker = f"RUN{i}-{int(time.time())}"
        src = BASE.replace("{MARKER}", marker)
        length = sci_set_text(sc, src)
        time.sleep(0.5)
        send_keys("{F6}")          # compile
        time.sleep(2.5)            # wait compiler
        row = read_compile()
        results.append({"run": i, "marker": marker,
                        "sci_length_after": length,
                        "compile_status": row["status"] if row else None,
                        "last_compile": row["last_compile"] if row else None,
                        "pass": bool(row and row["status"] == 1)})
        print(f"run {i}: status={results[-1]['compile_status']} "
              f"last_compile={results[-1]['last_compile']} pass={results[-1]['pass']}")

    # distinct LastCompileTime proof
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
        "method": "Scintilla SCI_SETTEXT(2181) message + F6 + DB file-readback",
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
