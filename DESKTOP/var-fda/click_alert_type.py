# -*- coding: utf-8 -*-
"""Click 警示 type button via native BM_CLICK + fill name via WM_SETTEXT."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32

BM_CLICK = 0x00F5
WM_SETTEXT = 0x000C

# button handles from prior enumeration (verified)
BTN_ALERT = 0x30c20      # 警示
EDIT_NAME = 0x3093e      # 名稱

# 1. click 警示 type
r = user32.SendMessageW(BTN_ALERT, BM_CLICK, 0, 0)
print("警示 click sent:", r)
time.sleep(1)

# 2. set name
name = "FDA_PAPER_ALERT"
buf = ctypes.create_unicode_buffer(name)
user32.SendMessageW(EDIT_NAME, WM_SETTEXT, 0, ctypes.cast(buf, ctypes.c_void_p))
print("name set:", name)
time.sleep(1)

# 3. verify: find OK button and remaining buttons
MAXT = 128

def enum_children(hwnd):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(ch, lparam):
        t = ctypes.create_unicode_buffer(MAXT)
        user32.GetWindowTextW(ch, t, MAXT)
        cls = ctypes.create_unicode_buffer(MAXT)
        user32.GetClassNameW(ch, cls, MAXT)
        out.append({"hwnd": ch, "text": t.value[:60], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out

# dialog hwnd 0x210850
for c in enum_children(0x210850):
    if c["text"] in ("確定", "取消", "確認", "OK", "Cancel") or "確定" in c["text"] or "取消" in c["text"]:
        print("ACTION BTN:", hex(c["hwnd"]), c["text"], c["class"])
    if "Edit" in c["class"]:
        # read back name edit text
        t = ctypes.create_unicode_buffer(MAXT)
        user32.GetWindowTextW(c["hwnd"], t, MAXT)
        print("Edit:", repr(t.value[:40]))
