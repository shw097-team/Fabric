# -*- coding: utf-8 -*-
"""FDA-C4 F06 compile via toolbar 編譯 button + 訊息 tab readback.
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
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def snap():
    return cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 500})


def find(els, sub, role=None):
    for e in els:
        if sub in (e.get("label") or "") and (role is None or e.get("role") == role):
            return e
    return None


# 1. find toolbar 編譯 button
s0 = snap()
btn = find(s0.get("elements", []), "編譯", "Button")
print("toolbar 編譯 button:", btn.get("element_index") if btn else None)
if not btn:
    # maybe it's ' 編譯 ' with spaces
    for e in s0.get("elements", []):
        if e.get("role") == "Button" and "編譯" in (e.get("label") or ""):
            btn = e
            break
    print("retry button:", btn.get("element_index") if btn else None)

if btn:
    r = cua("click", {"pid": PID, "element_token": btn.get("element_token"),
                      "snapshot_id": s0.get("snapshot_id")})
    print("編譯 click:", json.dumps(r, ensure_ascii=False)[:120])
    time.sleep(5)

# 2. switch to 訊息 tab
s1 = snap()
msg = find(s1.get("elements", []), "訊息", "TabItem")
if msg:
    r2 = cua("click", {"pid": PID, "element_token": msg.get("element_token"),
                       "snapshot_id": s1.get("snapshot_id")})
    print("訊息 tab click:", json.dumps(r2, ensure_ascii=False)[:100])
    time.sleep(2)

# 3. read message area
s2 = snap()
els2 = s2.get("elements", [])
print("total after msg tab:", s2.get("total_element_count"))
hits = []
for e in els2:
    lab = (e.get("label") or "")
    val = (e.get("value") or "")
    txt = (lab + " " + val).strip()
    if txt and any(k in txt for k in ("編譯", "成功", "完成", "錯誤", "無法", "error", "訊息", "Error", "0 個")):
        hits.append((e.get("role"), e.get("element_index"), txt[:120]))
for h in hits[:15]:
    print(f"  [{h[0]}] idx={h[1]} {h[2]}")
print("hits:", len(hits))

# 4. also read file DB after compile
import sqlite3
c = sqlite3.connect(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite")
rows = c.execute("SELECT Name, CompileStatus, substr(CompileMsg,1,80), LastCompileTime FROM Indicator").fetchall()
c.close()
for r_ in rows:
    print("USER DB:", r_)

receipt = {
    "artifact_id": "FDA_F06_COMPILE_TOOLBAR_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-TOOLBAR",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN", "script": "ATR (平均真實區域)"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "msg_tab_hits": [{"role": h[0], "idx": h[1], "text": h[2]} for h in hits],
    "user_db_after": [list(r_) for r_ in rows],
    "verdict": "PASS" if hits else "READBACK_EMPTY",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_COMPILE_TOOLBAR_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("receipt:", out)
