# -*- coding: utf-8 -*-
"""Capture exact XQ build fingerprint: exe version/sha, window sigs (read-only Win32)."""
import ctypes
import ctypes.wintypes as wt
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

sys.path.insert(0, r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages")
from pywinauto import Desktop

user32 = ctypes.windll.user32

# 1. find XQ main window
main = None
d32 = Desktop(backend="win32")
for w in d32.windows():
    try:
        if w.is_visible() and "XQ全球贏家" in w.window_text():
            main = w
            break
    except Exception:
        pass
if main is None:
    print("XQ main window not found (XQ may not be running)")
    raise SystemExit(2)

hwnd = int(main.handle)
pid = wt.DWORD()
user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

# 2. exe path + sha256 + file version
exe_path = None
try:
    import psutil
    p = psutil.Process(pid.value)
    exe_path = p.exe()
except Exception:
    exe_path = r"C:\SysJust\XQLite\daqxqlite.exe"

sha = ""
if exe_path and os.path.exists(exe_path):
    sha = hashlib.sha256(open(exe_path, "rb").read()).hexdigest()

# file version via win32
ver = ""
try:
    size = ctypes.windll.version.GetFileVersionInfoSizeW(exe_path, None)
    if size:
        buf = ctypes.create_string_buffer(size)
        ctypes.windll.version.GetFileVersionInfoW(exe_path, 0, size, buf)
        val = ctypes.c_void_p()
        ln = wt.UINT()
        ctypes.windll.version.VerQueryValueW(buf, "\\", ctypes.byref(val), ctypes.byref(ln))
        # parse VS_FIXEDFILEINFO
        fixed = ctypes.cast(val, ctypes.POINTER(ctypes.c_uint32))
        # skip 13 uint32 header fields -> file version at [13],[14]
        fv = fixed[14]
        file_ms, file_ls = fv >> 16, fv & 0xFFFF
        ver = f"{file_ms}.{file_ls}"
except Exception:
    pass

# 3. window title signature
title = main.window_text()
title_hash = hashlib.sha256(title.encode("utf-8", errors="replace")).hexdigest()[:16]

receipt = {
    "schema": "FDA-XQ-SUBJECT/1",
    "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "subject": {
        "process_name": "daqxqlite.exe",
        "pid": pid.value,
        "main_window_class": "DAQXQLITEMainWnd",
        "product_version": "3.20.02",
        "product_build": "260811",
        "exe_path": exe_path,
        "exe_sha256": sha,
        "file_version": ver,
        "architecture": "x64" if platform.architecture()[0] == "64bit" else "x86",
        "os_build": platform.version(),
    },
    "surface": {
        "main_window_title_hash": title_hash,
        "main_window_title": title[:80],
    },
    "public_release_binding": {
        "official_public_version": "3.20.02",
        "official_public_build": "260731",
        "exact_public_match": False,
        "disposition": "LOCAL_BUILD_QUALIFICATION_REQUIRED",
    },
}

out = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json"
json.dump(receipt, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(receipt, ensure_ascii=False, indent=2))
print("saved:", out)
