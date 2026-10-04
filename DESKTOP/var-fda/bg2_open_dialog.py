# -*- coding: utf-8 -*-
"""bg v2: Ctrl+O (background) -> enumerate 開啟 dialog via Win32 (read-only).
NO foreground, NO SendInput, NO SetCursorPos. Win32 = observation + PostMessage.
"""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import time
from pathlib import Path

user32 = ctypes.windll.user32
CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 21964
EWIN = 593114


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:120]}


def enum_windows(pid=None, title_sub=None):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, t, 256)
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if (pid is None or p.value == pid) and (title_sub is None or title_sub in t.value):
            out.append((hwnd, t.value, p.value))
        return True
    user32.EnumWindows(cb, 0)
    return out


def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        out.append({"hwnd": ch, "text": t.value[:50], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


# 1. Ctrl+O via background hotkey
r = cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "o"]})
print("ctrl+o:", (r.get("delivery") or {}).get("mode", "?"), (r.get("effect") or "?"))
time.sleep(4)

# 2. find 開啟 dialog
dls = [h for h, t, p in enum_windows(pid=PID, title_sub="開啟") if t.strip() == "開啟" or "開啟" in t]
print("開啟 dialogs:", [hex(h) for h in dls[:3]])
if not dls:
    raise SystemExit(2)
DLG = dls[0]

# 3. enumerate children — find 警示 tab button + list views + 確認 button
kids = enum_children(DLG)
print("=== children (first 25) ===")
for c in kids[:25]:
    print(f"  {hex(c['hwnd'])} {c['class']!r} {c['text']!r}")
