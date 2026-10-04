# -*- coding: utf-8 -*-
"""DoD-17: right-click FDA_PAPER_ALERT in editor tree -> 加入策略雷達.
Uses cua UIA for tree right-click (background), then handles the radar
add dialog via native Win32 API (postmessage).
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
PID = 20252
EWIN = 35720078


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:120]}


def ws(pid, wid, mx=500, depth=30):
    return cua("get_window_state", {"pid": pid, "window_id": wid,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def enum_windows(title_sub=None, pid=None):
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


# 1. find FDA_PAPER_ALERT in editor tree (right pane 腳本資料庫 tree)
s0 = ws(PID, EWIN, 600, 35)
item = find(s0.get("elements", []), "FDA_PAPER_ALERT", "TreeItem")
print("FDA_PAPER_ALERT tree item:", item.get("element_index") if item else None)
if not item:
    # expand 自訂(1) first
    custom = find(s0.get("elements", []), "自訂", "TreeItem")
    print("自訂:", custom.get("element_index") if custom else None)
    if custom:
        cua("click", {"pid": PID, "element_token": custom.get("element_token"),
                      "snapshot_id": s0.get("snapshot_id"), "count": 2})
        time.sleep(3)
        s0 = ws(PID, EWIN, 600, 35)
        item = find(s0.get("elements", []), "FDA_PAPER_ALERT", "TreeItem")
        print("after expand:", item.get("element_index") if item else None)

if item:
    # right-click on the item (UIA supports right via button='right'? use pixel)
    f = item.get("frame") or {}
    x = f.get("x", 0) + f.get("w", 0) // 2
    y = f.get("y", 0) + f.get("h", 0) // 2
    print("item at", x, y)
    cua("click", {"pid": PID, "x": x, "y": y, "button": "right", "delivery_mode": "foreground"})
    time.sleep(3)
    # context menu should appear; look for 加入策略雷達 menu item
    s1 = ws(PID, EWIN, 600, 35)
    add_radar = find(s1.get("elements", []), "加入策略雷達", "MenuItem")
    print("加入策略雷達:", add_radar.get("element_index") if add_radar else None)
    if add_radar:
        cua("click", {"pid": PID, "element_token": add_radar.get("element_token"),
                      "snapshot_id": s1.get("snapshot_id")})
        time.sleep(4)
        print("clicked 加入策略雷達")

# 2. check for 新增策略雷達 dialog (Win32)
time.sleep(2)
for hwnd, t, p in enum_windows(pid=PID):
    if "策略雷達" in t and "XQ全球" not in t:
        print("DLG:", repr(t[:60]), hex(hwnd))
