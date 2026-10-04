# -*- coding: utf-8 -*-
"""FDA-C4 F06 compile readback — execute 編譯所有我的文件 then dump 訊息 tab fully.
"""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 2904
WIN = 527196


def cua(tool, args):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=40, env=ENV)
    return json.loads(r.stdout.decode("utf-8", errors="replace"))


def snap():
    return cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 400})


def find(els, sub, role=None):
    for e in els:
        if sub in (e.get("label") or "") and (role is None or e.get("role") == role):
            return e
    return None


# 1. open compile menu
s0 = snap()
m = find(s0.get("elements", []), "編譯(C)", "MenuItem")
if m:
    cua("click", {"pid": PID, "element_token": m.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
    time.sleep(2)

# 2. click 編譯所有我的文件 (first submenu item)
s1 = snap()
c1 = find(s1.get("elements", []), "編譯所有我的文件", "MenuItem")
print("compile-all entry:", c1.get("element_index") if c1 else None)
if c1:
    r = cua("click", {"pid": PID, "element_token": c1.get("element_token"),
                      "snapshot_id": s1.get("snapshot_id")})
    print("compile-all click:", json.dumps(r, ensure_ascii=False)[:100])
    time.sleep(6)  # allow compile to finish

# 3. switch to 訊息 tab and dump
s2 = snap()
msg_tab = find(s2.get("elements", []), "訊息", "TabItem")
print("訊息 tab:", msg_tab.get("element_index") if msg_tab else None)
if msg_tab:
    cua("click", {"pid": PID, "element_token": msg_tab.get("element_token"),
                  "snapshot_id": s2.get("snapshot_id")})
    time.sleep(2)

# 4. full dump of 訊息 tab content
s3 = snap()
els3 = s3.get("elements", [])
print("=== post-compile snapshot (total", s3.get("total_element_count"), ") ===")
for e in els3:
    lab = (e.get("label") or "")
    val = (e.get("value") or "")
    txt = (lab + " " + val).strip()
    if txt and e.get("role") in ("Text", "Edit", "ListItem", "DataItem", "Document"):
        print(f"[{e.get('role')}] {txt[:110]}")
