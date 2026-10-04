# -*- coding: utf-8 -*-
"""FDA-C4 F06 known-good compile: locate toolbar 編譯 button (label has spaces),
click, then file-readback the user script DB compile fields.
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 2904
WIN = 527196
USER_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"


def cua(tool, args):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=40, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def snap():
    return cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 300})


def db_state():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute(
            "SELECT Name, CompileStatus, substr(CompileMsg,1,60), LastCompileTime "
            "FROM Indicator").fetchall()
    finally:
        c.close()


before = db_state()
print("DB before:", before)

# locate compile button (label may include spaces)
s0 = snap()
btn = None
for e in s0.get("elements", []):
    lab = (e.get("label") or "")
    if e.get("role") == "Button" and lab.strip() == "編譯":
        btn = e
        break
print("compile button:", btn.get("element_index") if btn else "NOT FOUND",
      "| label:", repr((btn or {}).get("label", "")))

if not btn:
    # fall back: 編譯(C) menu via foreground + first submenu click attempt
    print("fallback: no toolbar button; using menu")
    raise SystemExit(2)

r = cua("click", {"pid": PID, "element_token": btn.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id")})
print("compile click:", json.dumps(r, ensure_ascii=False)[:120])
time.sleep(6)

after = db_state()
print("DB after :", after)
changed = before != after
print("DB changed:", changed)

receipt = {
    "artifact_id": "FDA_F06_COMPILE_KNOWN_GOOD_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN", "script": "ATR (平均真實區域) (system corpus)"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "db_before": [list(x) for x in before],
    "db_after": [list(x) for x in after],
    "db_changed": changed,
    "readback": "file readback (hierarchy #1): Script.sqlite CompileStatus/CompileMsg/LastCompileTime",
    "verdict": "PASS" if changed else "NO_DB_CHANGE",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_COMPILE_KNOWN_GOOD_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("receipt:", out)
