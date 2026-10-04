# -*- coding: utf-8 -*-
"""FINAL P4 (MOUSE-FREE): all interactions via PostMessage/SendMessage ONLY.
Zero SetCursorPos, zero click_input, zero set_focus, zero send_keystrokes.
Step 1: close leftover 選擇使用腳本 dialog; check radar toolbar state via messages.
"""
import ctypes
import ctypes.wintypes as wt
import sys
import time

user32 = ctypes.windll.user32
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
WM_SETTEXT = 0x000C
WM_GETTEXT = 0x000D
TB_PRESSBUTTON = 0x0408
TB_BUTTONCOUNT = 0x0418
TB_GETBUTTON = 0x0417
TB_ISBUTTONENABLED = 0x041D

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


# 1. close any 選擇使用腳本 / 新增策略雷達 dialogs (message only)
for h, t in enum_windows():
    if "選擇使用腳本" in t or "新增策略雷達" in t:
        user32.PostMessageW(h, WM_CLOSE, 0, 0)
        print("closed:", t[:30], hex(h))
time.sleep(2)

# 2. radar window still alive?
radar_ok = any(h == RADAR for h, t in enum_windows())
print("radar alive:", radar_ok)

# 3. find radar toolbar (class ToolbarWindow32) via EnumChildWindows
kids = enum_children(RADAR)
toolbars = [c for c in kids if c["class"] == "ToolbarWindow32"]
print("toolbars:", [hex(c["hwnd"]) for c in toolbars])
for tb in toolbars:
    n = user32.SendMessageW(tb["hwnd"], TB_BUTTONCOUNT, 0, 0)
    print(f"  toolbar {hex(tb['hwnd'])} buttons={n}")
