# -*- coding: utf-8 -*-
"""bg v12: open 新增腳本 dialog via menu (background), PostMessage 警示,
then cua type_text (background, px) into name field, PostMessage 確認.
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


# 1. 檔案(F) menu -> 新增(N)
s0 = ws(PID, EWIN, 300)
fmenu = find(s0.get("elements", []), "檔案(F)", "MenuItem")
if fmenu:
    cua("click", {"pid": PID, "element_token": fmenu.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
    time.sleep(3)
s1 = ws(PID, EWIN, 500)
new_item = find(s1.get("elements", []), "新增(N)", "MenuItem")
if new_item:
    cua("click", {"pid": PID, "element_token": new_item.get("element_token"),
                  "snapshot_id": s1.get("snapshot_id")})
    time.sleep(4)

dls = [h for h, t, p in enum_windows(pid=PID, title_sub="新增腳本")]
print("新增腳本 dialogs:", [hex(h) for h in dls])
if not dls:
    raise SystemExit(2)
DLG = dls[0]

# 2. PostMessage 警示
kids = enum_children(DLG)
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
confirm_btn = next((c for c in kids if c["text"] == "確認" and c["class"] == "Button"), None)
edits = [c for c in kids if c["class"] == "Edit"]
print("警示:", hex(alert_btn["hwnd"]) if alert_btn else None)
print("確認:", hex(confirm_btn["hwnd"]) if confirm_btn else None)
if alert_btn:
    user32.PostMessageW(alert_btn["hwnd"], 0x00F5, 0, 0)
    print("post 警示")
    time.sleep(1)

# 3. type name via cua type_text (background, px) into FIRST edit (名稱欄)
if edits:
    edit = edits[0]["hwnd"]
    er = wt.RECT()
    user32.GetWindowRect(edit, ctypes.byref(er))
    # convert screen coords to window-local (dialog is the target window)
    # cua px is window-local to the window_id; use dialog's client origin
    dlg_rect = wt.RECT()
    user32.GetWindowRect(DLG, ctypes.byref(dlg_rect))
    lx = er.left - dlg_rect.left
    ty = er.top - dlg_rect.top
    cx = lx + (er.right - er.left) // 2
    cy = ty + (er.bottom - er.top) // 2
    print("name edit window-local:", cx, cy)
    r = cua("type_text", {"pid": PID, "window_id": DLG, "x": cx, "y": cy,
                          "text": "FDA_PAPER_ALERT2", "delivery_mode": "background"})
    print("type_text:", (r.get("delivery") or {}).get("mode", "?"), (r.get("effect") or "?"))
    time.sleep(2)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edit, t, 128)
    print("name now:", repr(t.value[:40]))

# 4. PostMessage 確認
if confirm_btn:
    user32.PostMessageW(confirm_btn["hwnd"], 0x00F5, 0, 0)
    print("post 確認")
    time.sleep(5)

for h, t, p in enum_windows(pid=PID, title_sub="XScript"):
    print("editor:", repr(t[:70]), hex(h))
