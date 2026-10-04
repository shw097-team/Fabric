# -*- coding: utf-8 -*-
"""DoD-17: open XS editor, load xs_script, rewrite as ret/RetVal ALERT-type
strategy (DOC-10 CH-13.05 authority syntax + DOC-04 CrossOver function form),
save, F6 compile, file readback.
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 23488
MAIN_WIN = 199968
DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"

# DOC-10 CH-13.05 ret/RetVal alert syntax (authority) + DOC-04 function form
ALERT_XS = (
    "// FDA DoD-17 PAPER radar fixture (DOC-10 CH-13.05 ret/RetVal contract)\n"
    "if CrossOver(Close, Average(Close, 20)) and Volume > Volume[1] then begin\n"
    "    ret = 1;\n"
    "    RetMsg = \"FDA-PAPER-ALERT\";\n"
    "end;\n"
)


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(pid, wid, mx=400, depth=25):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def db_read():
    c = sqlite3.connect(DB)
    row = c.execute("SELECT Name, Type, CompileStatus, CompileMsg FROM Indicator WHERE Name='xs_script'").fetchone()
    c.close()
    return row


# 1. open 策略(D) -> XScript 編輯器(E)
s0 = ws(PID, MAIN_WIN, 300)
menu = find(s0.get("elements", []), "策略(D)", "MenuItem")
if not menu:
    print("FAIL: 策略 menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": menu.get("element_token"),
              "snapshot_id": s0.get("snapshot_id")})
time.sleep(3)
s1 = ws(PID, MAIN_WIN, 400)
ed = find(s1.get("elements", []), "XScript 編輯器", "MenuItem")
if not ed:
    print("FAIL: XScript 編輯器 menu"); raise SystemExit(2)
cua("click", {"pid": PID, "element_token": ed.get("element_token"),
              "snapshot_id": s1.get("snapshot_id")})
time.sleep(6)

# find editor window
ed_win = None
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    if "XScript 編輯器" in (w.get("title") or ""):
        ed_win = w
        break
print("editor win:", ed_win.get("window_id") if ed_win else None)
if not ed_win:
    raise SystemExit(2)
EWIN = ed_win.get("window_id")

# 2. load xs_script tab (Ctrl+Tab until active)
s2 = ws(PID, EWIN, 200, 15)
print("editor title:", (s2.get("tree_markdown") or "").splitlines()[0][:70] if s2.get("tree_markdown") else "?")
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "tab"], "delivery_mode": "foreground"})
time.sleep(2)
s2b = ws(PID, EWIN, 200, 15)
md = s2b.get("tree_markdown") or ""
active = [l for l in md.splitlines() if "xs_script" in l or "TitleBar" in l]
print("active tab:", active[:2])

# 3. ctrl+a then paste alert XS via clipboard
import ctypes
def set_clip(text):
    import ctypes.wintypes as wt
    CF_UNICODETEXT = 13
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    user32.OpenClipboard(0)
    user32.EmptyClipboard()
    data = (text + "\0").encode("utf-16-le")
    h = kernel32.GlobalAlloc(0x0042, len(data))
    p = kernel32.GlobalLock(h)
    ctypes.memmove(p, data, len(data))
    kernel32.GlobalUnlock(h)
    user32.SetClipboardData(CF_UNICODETEXT, h)
    user32.CloseClipboard()

set_clip(ALERT_XS)
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "a"], "delivery_mode": "foreground"})
time.sleep(1)
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "v"], "delivery_mode": "foreground"})
time.sleep(2)
print("pasted alert XS")

# 4. save (Ctrl+S)
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "s"], "delivery_mode": "foreground"})
time.sleep(3)

# 5. F6 compile
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
time.sleep(6)

# 6. file readback
row = db_read()
print("DB after:", row)
print("ALERT_COMPILE_PASS" if row and row[2] == 1 else "ALERT_COMPILE_FAIL")
