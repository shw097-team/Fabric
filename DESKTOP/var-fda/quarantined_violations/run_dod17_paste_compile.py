# -*- coding: utf-8 -*-
"""DoD-17 part 2: paste alert XS (already in clipboard) into active editor tab,
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


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(pid, wid, mx=200, depth=15):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


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

# Ctrl+Tab to xs_script tab
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "tab"], "delivery_mode": "foreground"})
time.sleep(2)
s = ws(PID, EWIN)
md = s.get("tree_markdown") or ""
print("title line:", [l for l in md.splitlines() if 'Window "' in l][:1])

# select all + paste
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "a"], "delivery_mode": "foreground"})
time.sleep(1)
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "v"], "delivery_mode": "foreground"})
time.sleep(2)
print("pasted")

# save
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "s"], "delivery_mode": "foreground"})
time.sleep(3)

# F6 compile
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
time.sleep(8)

# file readback
c = sqlite3.connect(DB)
rows = c.execute("SELECT Name, Type, CompileStatus, CompileMsg, LastCompileTime FROM Indicator").fetchall()
c.close()
for r in rows:
    print("DB:", r)
