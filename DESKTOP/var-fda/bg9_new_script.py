# -*- coding: utf-8 -*-
"""bg v9: Ctrl+N -> 新增腳本 dialog -> PostMessage 警示 + name + 確認.
Verified pattern from earlier (created FDA_PAPER_ALERT successfully).
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
PID = 8100
EWIN = 2425730


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


# 1. Ctrl+N background hotkey
r = cua("hotkey", {"pid": PID, "window_id": EWIN, "keys": ["ctrl", "n"]})
print("ctrl+n:", (r.get("delivery") or {}).get("mode", "?"), (r.get("effect") or "?"))
time.sleep(4)

# 2. find 新增腳本 dialog
dls = [h for h, t, p in enum_windows(pid=PID, title_sub="新增腳本")]
print("新增腳本 dialogs:", [hex(h) for h in dls])
if not dls:
    raise SystemExit(2)
DLG = dls[0]

# 3. enumerate children -> find 警示 Button, 名稱 Edit, 確認 Button
kids = enum_children(DLG)
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
confirm_btn = next((c for c in kids if c["text"] == "確認" and c["class"] == "Button"), None)
edits = [c for c in kids if c["class"] == "Edit"]
print("警示:", hex(alert_btn["hwnd"]) if alert_btn else None)
print("確認:", hex(confirm_btn["hwnd"]) if confirm_btn else None)
print("edits:", [(hex(c["hwnd"]), c["text"]) for c in edits])

if not alert_btn or not confirm_btn:
    print("FAIL: missing controls")
    raise SystemExit(2)

# 4. PostMessage click 警示
user32.PostMessageW(alert_btn["hwnd"], 0x00F5, 0, 0)
print("post 警示")
time.sleep(1)

# 5. set name via PostMessage WM_SETTEXT on FIRST edit (名稱)
NAME = "FDA_PAPER_ALERT2"
if edits:
    buf = ctypes.create_unicode_buffer(NAME)
    r2 = user32.PostMessageW(edits[0]["hwnd"], 0x000C, 0, ctypes.cast(buf, ctypes.c_void_p))
    print("post name:", r2)
    time.sleep(1)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edits[0]["hwnd"], t, 128)
    print("name edit now:", repr(t.value[:40]))

# 6. PostMessage click 確認
user32.PostMessageW(confirm_btn["hwnd"], 0x00F5, 0, 0)
print("post 確認")
time.sleep(5)

# 7. check editor title
for h, t, p in enum_windows(pid=PID, title_sub="XScript"):
    print("editor:", repr(t[:70]), hex(h))
