# -*- coding: utf-8 -*-
"""FINAL P5 (MOUSE-FREE): TB_PRESSBUTTON NEW(17551) -> find 新增策略雷達 dialog -> enumerate."""
import ctypes
import ctypes.wintypes as wt
import sys
import time

user32 = ctypes.windll.user32
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
TB_PRESSBUTTON = 0x0408
TB_BUTTONCOUNT = 0x0418
TB_GETBUTTON = 0x0417
TB_ISBUTTONENABLED = 0x041D

TB = 0xb08fa
RADAR = 0x110d96


def enum_windows(pid=None, title_sub=None):
    out = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(hwnd, lparam):
        t = ctypes.create_unicode_buffer(256)
        user32.GetWindowTextW(hwnd, t, 256)
        p = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(p))
        if (pid is None or p.value == pid) and (title_sub is None or title_sub in t.value):
            out.append((hwnd, t.value))
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
        out.append({"hwnd": ch, "text": t.value[:40], "class": cls.value[:30]})
        return True
    user32.EnumChildWindows(hwnd, cb, 0)
    return out


# 1. press NEW (17551) via TB_PRESSBUTTON
enabled = user32.SendMessageW(TB, TB_ISBUTTONENABLED, 17551, 0)
print("NEW enabled:", bool(enabled))
user32.SendMessageW(TB, TB_PRESSBUTTON, 17551, 1)
print("pressed NEW")
time.sleep(3)

# 2. find 新增策略雷達 dialog
dlgs = [(h, t) for h, t in enum_windows() if "新增策略雷達" in t]
print("新增策略雷達 dialogs:", [hex(h) for h, t in dlgs])
if not dlgs:
    raise SystemExit(2)
DLG = dlgs[0][0]

# 3. enumerate dialog children (classes + control ids + text)
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb2(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    cid = user32.GetDlgCtrlID(ch)
    r = wt.RECT()
    user32.GetWindowRect(ch, ctypes.byref(r))
    dr = wt.RECT()
    user32.GetWindowRect(DLG, ctypes.byref(dr))
    out.append({"hwnd": ch, "text": t.value[:35], "class": cls.value[:25],
                "cid": cid, "lx": r.left - dr.left, "ly": r.top - dr.top})
    return True
user32.EnumChildWindows(DLG, cb2, 0)
for c in out:
    print(f"  {hex(c['hwnd'])} id={c['cid']} {c['class']!r} '{c['text']}' @({c['lx']},{c['ly']})")
