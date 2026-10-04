# -*- coding: utf-8 -*-
"""Paste alert XS into FDA_PAPER_ALERT editor, save, F6 compile, DB readback."""
import ctypes
import ctypes.wintypes as wt
import json
import sqlite3
import subprocess
import time
from pathlib import Path

user32 = ctypes.windll.user32
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 20252
EWIN = 0x2210b8e
DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"

# Win32: find Edit child of editor window (the script content editor)
def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(ch, t, 256)
        cls = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(ch, cls, 128)
        out.append({"hwnd": ch, "text": t.value[:80], "class": cls.value[:40]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out

children = enum_children(EWIN)
edits = [c for c in children if "Edit" in c["class"]]
print("editor edits:", [(hex(c['hwnd']), c['class']) for c in edits])

# XQ XS editor content control is a syntax editor (likely class 'XTPEdit' or RichEdit)
# The content edit is usually the LARGEST edit control. Use cua to type instead:
# (UIA worked for type/clipboard in F06). Reuse clipboard paste path:
def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:120]}

# set clipboard via PowerShell
xs = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\FDA_PAPER_ALERT.xs").read_text(encoding="utf-8")
Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\clip_tmp.xs").write_text(xs, encoding="utf-8")
subprocess.run(["powershell", "-NoProfile", "-Command",
                "Get-Content -Raw -Encoding UTF8 'C:\\Projects\\Agent_Workspace\\HG-KSEOS\\var\\fda\\clip_tmp.xs' | Set-Clipboard"],
               capture_output=True, timeout=30)
print("clipboard set")

# focus editor window then ctrl+a / ctrl+v
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "a"], "delivery_mode": "foreground"})
time.sleep(1)
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "v"], "delivery_mode": "foreground"})
time.sleep(2)
print("pasted")

# save Ctrl+S
cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "s"], "delivery_mode": "foreground"})
time.sleep(3)

# compile F6
cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
time.sleep(8)

# DB readback
c = sqlite3.connect(DB)
rows = c.execute("SELECT Name, ExecType, CompileStatus, CompileMsg, LastCompileTime FROM Indicator WHERE Name='FDA_PAPER_ALERT'").fetchall()
c.close()
print("DB:", rows)
