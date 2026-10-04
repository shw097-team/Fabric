# -*- coding: utf-8 -*-
"""bg v10: 檔案(F) menu -> 新增(N) MenuItem (background clicks) -> dialog -> PostMessage."""
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


def ws(pid, wid, mx=400, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


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


# 1. 檔案(F) menu
s0 = ws(PID, EWIN, 300)
fmenu = find(s0.get("elements", []), "檔案(F)", "MenuItem")
print("檔案(F):", fmenu.get("element_index") if fmenu else None)
if fmenu:
    cua("click", {"pid": PID, "element_token": fmenu.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
    time.sleep(3)

# 2. 新增(N) MenuItem
s1 = ws(PID, EWIN, 500)
new_item = find(s1.get("elements", []), "新增(N)", "MenuItem")
print("新增(N):", new_item.get("element_index") if new_item else None)
if new_item:
    cua("click", {"pid": PID, "element_token": new_item.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id")})
    time.sleep(4)

# 3. find 新增腳本 dialog
dls = [h for h, t, p in enum_windows(pid=PID, title_sub="新增腳本")]
print("新增腳本 dialogs:", [hex(h) for h in dls])
