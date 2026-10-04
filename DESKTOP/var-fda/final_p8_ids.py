# -*- coding: utf-8 -*-
"""FINAL P8: scan radar window for community-known control ids (17001/17002/17003/17202/33035/45243/45041/17107/17035/59392)."""
import ctypes
import ctypes.wintypes as wt
import sys

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
user32 = ctypes.windll.user32

RADAR = 0x110d96
WANT = {17001, 17002, 17003, 17107, 17035, 17202, 45243, 45041, 33035, 33555, 59392, 17500, 17501, 17502}

out = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(ch, lparam):
    t = ctypes.create_unicode_buffer(128)
    user32.GetWindowTextW(ch, t, 128)
    cls = ctypes.create_unicode_buffer(64)
    user32.GetClassNameW(ch, cls, 64)
    cid = user32.GetDlgCtrlID(ch)
    r = wt.RECT()
    user32.GetWindowRect(ch, ctypes.byref(r))
    out.append({"hwnd": ch, "text": t.value[:35], "class": cls.value[:22], "cid": cid,
                "x": r.left, "y": r.top, "w": r.right - r.left, "h": r.bottom - r.top})
    return True
user32.EnumChildWindows(RADAR, cb, 0)

print(f"total children: {len(out)}")
hits = [c for c in out if c["cid"] in WANT]
print(f"=== wanted ids found: {len(hits)} ===")
for c in hits:
    print(f"  {hex(c['hwnd'])} id={c['cid']} {c['class']!r} '{c['text']}' ({c['x']},{c['y']},{c['w']}x{c['h']})")

# also list tab-like controls (SysTabControl32, XTPReport, MFCGridCtrl-ish)
print("=== tab/report/grid controls ===")
for c in out:
    if any(k in c["class"] for k in ("Tab", "Report", "Grid", "Tree", "List")):
        print(f"  {hex(c['hwnd'])} id={c['cid']} {c['class']!r} '{c['text']}' ({c['x']},{c['y']},{c['w']}x{c['h']})")
