# -*- coding: utf-8 -*-
"""PostMessage-based dialog interaction (cross-process safe)."""
import ctypes
import ctypes.wintypes as wt
import time

user32 = ctypes.windll.user32

BM_CLICK = 0x00F5
WM_SETTEXT = 0x000C
WM_COMMAND = 0x0111

BTN_ALERT = 0x30c20      # 警示
EDIT_NAME = 0x3093e      # 名稱
BTN_CONFIRM = 0x30c12    # 確認
DLG = 0x210850

# 1. PostMessage click 警示
r = user32.PostMessageW(BTN_ALERT, BM_CLICK, 0, 0)
print("post 警示:", r)
time.sleep(1)

# 2. set name
name = "FDA_PAPER_ALERT"
buf = ctypes.create_unicode_buffer(name)
r2 = user32.PostMessageW(EDIT_NAME, WM_SETTEXT, 0, ctypes.cast(buf, ctypes.c_void_p))
print("post name:", r2)
time.sleep(1)

# verify name edit content via GetWindowText
t = ctypes.create_unicode_buffer(256)
user32.GetWindowTextW(EDIT_NAME, t, 256)
print("name edit now:", repr(t.value[:40]))

# 3. post click 確認
r3 = user32.PostMessageW(BTN_CONFIRM, BM_CLICK, 0, 0)
print("post 確認:", r3)
time.sleep(4)

# 4. check windows — did a new script tab open? DB row?
def find_windows(pid=None, title_sub=None):
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

for h, t, p in find_windows(title_sub="FDA_PAPER")[:5]:
    print("WIN:", repr(t[:60]), hex(h), p)
