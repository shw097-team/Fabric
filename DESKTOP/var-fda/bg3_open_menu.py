# -*- coding: utf-8 -*-
"""bg v3: 檔案(F) menu -> 開啟(O) MenuItem (background clicks, proven pattern)."""
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


def ws(pid, wid, mx=400, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


# 1. 檔案(F) menu (background)
s0 = ws(PID, EWIN, 300)
fmenu = find(s0.get("elements", []), "檔案(F)", "MenuItem")
print("檔案(F):", fmenu.get("element_index") if fmenu else None)
if fmenu:
    r = cua("click", {"pid": PID, "element_token": fmenu.get("element_token"),
                      "snapshot_id": s0.get("snapshot_id")})
    print("click:", (r.get("effect") or "?"))
    time.sleep(3)

# 2. 開啟(O) MenuItem (background)
s1 = ws(PID, EWIN, 500)
op = find(s1.get("elements", []), "開啟(O)", "MenuItem")
print("開啟(O):", op.get("element_index") if op else None)
if op:
    r2 = cua("click", {"pid": PID, "element_token": op.get("element_token"),
                       "snapshot_id": s1.get("snapshot_id")})
    print("click:", (r2.get("effect") or "?"))
    time.sleep(4)

# 3. find 開啟 dialog via Win32
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == PID and t.value.strip() == "開啟":
        out.append((hwnd, t.value))
    return True
user32.EnumWindows(cb, 0)
print("開啟 dialogs:", [hex(h) for h, t in out])
