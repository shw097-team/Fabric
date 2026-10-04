# -*- coding: utf-8 -*-
"""bg v11: 新增腳本 dialog (3211854) -> PostMessage 警示 + name + 確認.
Verified pattern (created FDA_PAPER_ALERT earlier).
"""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32
DLG = 3211854


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


kids = enum_children(DLG)
alert_btn = next((c for c in kids if c["text"] == "警示" and c["class"] == "Button"), None)
confirm_btn = next((c for c in kids if c["text"] == "確認" and c["class"] == "Button"), None)
edits = [c for c in kids if c["class"] == "Edit"]
print("警示:", hex(alert_btn["hwnd"]) if alert_btn else None)
print("確認:", hex(confirm_btn["hwnd"]) if confirm_btn else None)
print("edits:", [(hex(c["hwnd"]), c["text"]) for c in edits])

if not alert_btn or not confirm_btn:
    print("FAIL controls")
    raise SystemExit(2)

# 1. click 警示
user32.PostMessageW(alert_btn["hwnd"], 0x00F5, 0, 0)
print("post 警示")
time.sleep(1)

# 2. set name (PostMessage WM_SETTEXT)
NAME = "FDA_PAPER_ALERT2"
if edits:
    buf = ctypes.create_unicode_buffer(NAME)
    r = user32.PostMessageW(edits[0]["hwnd"], 0x000C, 0, ctypes.cast(buf, ctypes.c_void_p))
    print("post name:", r)
    time.sleep(1)
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(edits[0]["hwnd"], t, 128)
    print("name now:", repr(t.value[:40]))

# 3. click 確認
user32.PostMessageW(confirm_btn["hwnd"], 0x00F5, 0, 0)
print("post 確認")
time.sleep(5)

# 4. check editor title
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(hwnd, lparam):
    t2 = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t2, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == 8100 and "XScript" in t2.value:
        out.append((hex(hwnd), t2.value[:70]))
    return True
user32.EnumWindows(cb2, 0)
print("editor:", out)
