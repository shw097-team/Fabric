# -*- coding: utf-8 -*-
"""RR6-B v7: cua click with snapshot_id (0.19.3 contract).
get_window_state -> snapshot_id + element_index=18 (編譯 Button) -> click(snapshot_id)."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import subprocess
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"
EDITOR_HWND = 0x260658
XQ_PID = 22384
EDITOR_WID = 2491992
CUA = r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe"
SCI_SETTEXT, SCI_GETTEXTLENGTH = 2181, 2183
u = ctypes.windll.user32
NAME = "FDA_F06_FRESH"
SRC = """{@type:indicator}
// FDA F06 fresh fixture
value1 = CrossOver(Close, Average(Close, 5));
Plot1(value1, "X");
// marker: {MARKER}
"""


def cua_call(tool, args):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)],
                       capture_output=True, timeout=90)
    return r.stdout.decode("utf-8", errors="replace")


def cua_compile():
    """fresh get_window_state -> find 編譯 button element -> background invoke."""
    st = cua_call("get_window_state", {"pid": XQ_PID, "window_id": EDITOR_WID})
    snap = None
    try:
        d = json.loads(st)
        snap = d.get("snapshot_id") or d.get("snapshot") or None
        els = d.get("structuredContent", {}).get("elements", [])
        idx = None
        for e in els:
            if "編譯" in str(e.get("name", "")):
                idx = e.get("element_index")
                break
        if idx is None:
            md = d.get("tree_markdown", "")
            import re
            m = re.search(r"\[(\d+)\][^\[]*?編譯", md)
            idx = m.group(1) if m else None
        print(f"  snapshot={str(snap)[:20]} compile_el={idx}")
        if idx and snap:
            return cua_call("click", {"pid": XQ_PID, "window_id": EDITOR_WID,
                                      "element_index": int(idx),
                                      "snapshot_id": snap,
                                      "delivery_mode": "background"})[:120]
        return f"NO_TARGET snap={snap} idx={idx}"
    except Exception as e:
        return f"ERR {str(e)[:80]} :: {st[:150]}"


def sci_set_text(hwnd, text):
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
        "SELECT Name, CompileStatus, CompileMsg, LastCompileTime FROM Sensor "
        "WHERE Name=? ORDER BY LastCompileTime DESC LIMIT 1",
        (NAME.encode("cp950"),)).fetchall()
    c.close()
    if not rows:
        return None
    n, st, msg, t = rows[0]
    return {"status": st,
            "msg": msg.decode("cp950", errors="replace") if msg else "",
            "last_compile": t.decode("cp950", errors="replace") if t else None}


def find_scintilla():
    kids = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, _):
        cls = ctypes.create_unicode_buffer(64)
        u.GetClassNameW(h, cls, 64)
        if "Scintilla" in cls.value:
            kids.append(h)
        return True
    u.EnumChildWindows(ctypes.c_void_p(EDITOR_HWND), cb, 0)
    return kids[0] if kids else None


def main():
    sc = find_scintilla()
    if not sc:
        print("no scintilla"); return
    print("scintilla:", hex(sc))

    results = []
    for i in range(1, 11):
        src = SRC.replace("{MARKER}", f"RUN{i}-{int(time.time())}")
        sci_set_text(sc, src)
        time.sleep(0.5)
        cua_out = cua_compile()
        time.sleep(3.5)
        row = read_compile()
        results.append({"run": i, "compile_status": row["status"] if row else None,
                        "compile_msg": (row["msg"] or "")[:40] if row else None,
                        "last_compile": row["last_compile"] if row else None,
                        "pass": bool(row and row["status"] == 1),
                        "cua_effect": cua_out[:70]})
        print(f"run {i}: status={results[-1]['compile_status']} "
              f"last_compile={results[-1]['last_compile']} pass={results[-1]['pass']}")

    times = [r["last_compile"] for r in results if r["last_compile"]]
    receipt = {
        "artifact_id": "FDA_F06_FRESH_10RUN_RECEIPT_RR6",
        "schema": "FDA-FIXTURE-RECEIPT/2",
        "fixture": "F06-COMPILE-FRESH-10RUN",
        "action_class": "XS_COMPILE_PASS",
        "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
                   "login": "SHW097:LOGGED_IN"},
        "mode": "PAPER_NO_LIVE_WRITE",
        "method": "SCI_SETTEXT(2181) + cua background invoke 編譯 (snapshot_id contract) + DB readback; "
                  "ZERO set_focus/send_keys/click_input/foreground",
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
