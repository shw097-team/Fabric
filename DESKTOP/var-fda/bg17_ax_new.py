# -*- coding: utf-8 -*-
"""bg v17: ax-rung click on 新增 button (element_index, background).
Then find main 新增腳本 dialog, PostMessage 警示, fill name via cua type_text px, confirm.
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
        r = wt.RECT()
        user32.GetWindowRect(ch, ctypes.byref(r))
        dr = wt.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(dr))
        out.append({"hwnd": ch, "class": cls.value, "text": t.value[:40],
                    "lx": r.left - dr.left, "ly": r.top - dr.top,
                    "w": r.right - r.left, "h": r.bottom - r.top})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


# 1. ax click 新增 (element_index 0)
s0 = ws(PID, EWIN, 300)
btn0 = next((e for e in s0.get("elements", []) if e.get("element_index") == 0), None)
print("新增 btn:", btn0.get("label") if btn0 else None)
if btn0:
    r = cua("click", {"pid": PID, "element_token": btn0.get("element_token"),
                      "snapshot_id": s0.get("snapshot_id")})
    print("ax click:", (r.get("delivery") or {}).get("mode", "?"), (r.get("effect") or "?"))
    time.sleep(4)

# 2. find main dialog (with 腳本類型 labels)
main_dlg = None
for hwnd, t, p in enum_windows(pid=PID):
    if "新增腳本" not in t:
        continue
    kids = enum_children(hwnd)
    labels = [c["text"] for c in kids if c["text"].strip()]
    if "腳本類型" in labels:
        main_dlg = hwnd
        print("MAIN dialog:", hex(hwnd))
        break
if not main_dlg:
    print("no main dialog; windows:", [hex(h) for h, t, p in enum_windows(pid=PID, title_sub="新增腳本")])
    raise SystemExit(2)

# 3. PostMessage 警示
kids = enum_children(main_dlg)
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
confirm_btn = next((c for c in kids if c["text"] == "確認" and c["class"] == "Button"), None)
name_edit = None
# find Edit right after 名稱： Static
for i, c in enumerate(kids):
    if c["text"] == "名稱：" and i + 1 < len(kids) and kids[i + 1]["class"] == "Edit":
        name_edit = kids[i + 1]
        break
print("警示:", hex(alert_btn["hwnd"]) if alert_btn else None)
print("確認:", hex(confirm_btn["hwnd"]) if confirm_btn else None)
print("名稱 Edit:", hex(name_edit["hwnd"]) if name_edit else None, (name_edit or {}).get("lx"))

if alert_btn:
    user32.PostMessageW(alert_btn["hwnd"], 0x00F5, 0, 0)
    print("post 警示")
    time.sleep(1)

# 4. type name via cua type_text px (background)
if name_edit:
    cx = name_edit["lx"] + name_edit["w"] // 2
    cy = name_edit["ly"] + name_edit["h"] // 2
    print("name edit local:", cx, cy)
    r2 = cua("type_text", {"pid": PID, "window_id": main_dlg, "x": cx, "y": cy,
                           "text": "FDA_PAPER_ALERT2", "delivery_mode": "background"})
    print("type_text:", (r2.get("delivery") or {}).get("mode", "?"), (r2.get("effect") or "?"))
    time.sleep(2)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(name_edit["hwnd"], t, 128)
    print("name now:", repr(t.value[:40]))

# 5. confirm
if confirm_btn:
    user32.PostMessageW(confirm_btn["hwnd"], 0x00F5, 0, 0)
    print("post 確認")
    time.sleep(5)

for h, t, p in enum_windows(pid=PID, title_sub="XScript"):
    print("editor:", repr(t[:70]), hex(h))
