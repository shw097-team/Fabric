# -*- coding: utf-8 -*-
"""bg v15: scan ALL pid-8100 top windows; find the one with 名稱/腳本類型 children."""
import ctypes
import ctypes.wintypes as wt

user32 = ctypes.windll.user32
PID = 8100

# close known error dialogs
for h in (0x3a0898, 0x100ba0):
    user32.PostMessageW(h, 0x0010, 0, 0)

wins = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(hwnd, lparam):
    t = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, t, 256)
    p = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
    if p.value == PID:
        wins.append((hwnd, t.value))
    return True
user32.EnumWindows(cb, 0)
print("all pid windows:", [(hex(h), t[:40]) for h, t in wins])

# for each non-XQ window, check children for 名稱/腳本類型/警示
for hwnd, title in wins:
    if "XQ全球" in title:
        continue
    kids = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb2(ch, lparam):
        t = ctypes.create_unicode_buffer(128)
        user32.GetWindowTextW(ch, t, 128)
        cls = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ch, cls, 64)
        kids.append((t.value[:30], cls.value[:20]))
        return True
    user32.EnumChildWindows(hwnd, cb2, 0)
    labels = [t for t, c in kids if t.strip()]
    print(f"--- {hex(hwnd)} '{title[:40]}' labels={labels[:8]}")
