# -*- coding: utf-8 -*-
"""Open radar via cua background menu click (verified path). Zero mouse-stealing."""
import ctypes
import ctypes.wintypes as wt
import json
import subprocess
import time

u = ctypes.windll.user32
XQ_PID = 7924
CUA = r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe"

def call(tool, args, timeout=60):
    rr = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True, timeout=timeout)
    if not rr.stdout:
        return None
    return json.loads(rr.stdout.decode("utf-8", errors="replace"))

# find main window id
info = call("get_accessibility_tree", {}, 90)
wid = None
if info and "windows" in info:
    for w in info["windows"]:
        title = w.get("title", "")
        if title.startswith("XQ全球贏家(個人版)"):
            wid = w.get("window_id")
            print("main window_id:", wid)
            break
if not wid:
    print("main window not found"); raise SystemExit(1)

# get window state -> find 策略 menu -> 策略雷達 item -> background click
ws = call("get_window_state", {"pid": XQ_PID, "window_id": wid}, 90)
print("elements:", len(ws.get("elements", [])) if ws else "none")
if not ws or not ws.get("elements"):
    print("empty tree — trying markdown"); raise SystemExit(1)

# find menu path: 策略(D) -> 策略雷達
menu_el = None
radar_el = None
for e in ws["elements"]:
    name = e.get("name", "")
    if name == "策略" and e.get("role") in ("MenuItem", "Button"):
        menu_el = e
    if "策略雷達" in name:
        radar_el = e
print("menu 策略:", bool(menu_el), "| 策略雷達:", bool(radar_el))

if radar_el:
    # background click 策略雷達 directly (may auto-open menu)
    r = call("click", {"pid": XQ_PID, "window_id": wid,
                       "element_token": radar_el.get("element_token"),
                       "delivery_mode": "background"}, 60)
    print("click radar:", json.dumps(r, ensure_ascii=False)[:120] if r else "no response")
elif menu_el:
    r = call("click", {"pid": XQ_PID, "window_id": wid,
                       "element_token": menu_el.get("element_token"),
                       "delivery_mode": "background"}, 60)
    print("click 策略 menu:", json.dumps(r, ensure_ascii=False)[:120] if r else "no response")
    time.sleep(3)
    ws2 = call("get_window_state", {"pid": XQ_PID, "window_id": wid}, 90)
    for e in ws2.get("elements", []):
        if "策略雷達" in e.get("name", ""):
            r2 = call("click", {"pid": XQ_PID, "window_id": wid,
                                "element_token": e.get("element_token"),
                                "delivery_mode": "background"}, 60)
            print("click 策略雷達 (2nd):", json.dumps(r2, ensure_ascii=False)[:120] if r2 else "no response")
            break

time.sleep(5)
# verify radar window appeared
radar_found = False
for h, t in [(h, t) for h, t in _enum()] if False else []:
    pass
out = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(hwnd, lparam):
    pid = ctypes.c_ulong()
    u.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    if pid.value == XQ_PID:
        buf = ctypes.create_unicode_buffer(200)
        u.GetWindowTextW(hwnd, buf, 200)
        out.append((hex(hwnd), buf.value[:60]))
    return True
u.EnumWindows(cb, 0)
print("XQ windows now:")
for w in out:
    print("  ", w)
