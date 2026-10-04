# -*- coding: utf-8 -*-
"""FINAL P6 (MOUSE-FREE): dump radar toolbar button enabled states + grid content."""
import ctypes
import ctypes.wintypes as wt
import sys

user32 = ctypes.windll.user32
sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")

TB = 0xb08fa
RADAR = 0x110d96
TB_ISBUTTONENABLED = 0x041D
TB_BUTTONCOUNT = 0x0418

n = user32.SendMessageW(TB, TB_BUTTONCOUNT, 0, 0)
cmds = [17550, 17551, 17553, 17627, 33011, 33012, 33059, 33062, 17554, 17555, 17556, 17557, 33051, 33052, 33053]
print(f"toolbar buttons={n}")
for cid in cmds:
    en = user32.SendMessageW(TB, TB_ISBUTTONENABLED, cid, 0)
    print(f"  id={cid} enabled={bool(en)}")

# enumerate radar children — find grid (MFCGridCtrl 17001) + tabs (SysTabControl32 17003)
out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    cid = user32.GetDlgCtrlID(ch)
    out.append({"hwnd": ch, "text": t.value[:30], "class": cls.value[:25], "cid": cid})
    return True
user32.EnumChildWindows(RADAR, cb, 0)
print("=== radar children (non-empty) ===")
for c in out:
    if c["cid"] in (17001, 17002, 17003, 17035, 17107, 17202, 45243, 45041, 33035, 33555, 59392) or c["text"]:
        print(f"  {hex(c['hwnd'])} id={c['cid']} {c['class']!r} '{c['text']}'")
