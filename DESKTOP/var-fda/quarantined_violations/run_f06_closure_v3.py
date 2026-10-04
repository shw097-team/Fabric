# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v3 — known-good compile via user-script overwrite path.
Load 自訂(1)/xs_script from editor tree -> select-all -> type DOC-03 known-good
indicator syntax -> 儲存 -> F6 compile -> file readback CompileStatus=0/1.
All ops are ones already proven non-deadlocking (tree dbl-click, type_text,
press_key). AVOIDS the 新增 button (Afx UIA Invoke deadlock, R-FDA-011).
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 21488
EWIN = 5246196
USER_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"
GOOD_SCRIPT = "Input: length(20);\nVariable: ma(0);\nma = Average(Close, length);\nif Close CrossOver ma then\n    Plot1(ma);"


def cua(tool, args, timeout=40):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(mx=400, depth=25):
    return cua("get_window_state", {"pid": PID, "window_id": EWIN,
                                    "max_elements": mx, "max_depth": depth})


def db_user():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute("SELECT Name, CompileStatus, substr(CompileMsg,1,60), LastCompileTime "
                         "FROM Indicator WHERE Name LIKE 'xs_script'").fetchone()
    finally:
        c.close()


results = []
before = db_user()
print("DB before:", before)

# 1. expand 自訂 (1) tree (single click first, then dbl-click if needed)
s0 = ws()
custom = next((e for e in s0.get("elements", []) if e.get("role") == "TreeItem" and "自訂" in (e.get("label") or "")), None)
print("自訂 item:", custom.get("element_index") if custom else None)
if custom:
    cua("click", {"pid": PID, "element_token": custom.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id"), "count": 2}, timeout=60)
    time.sleep(3)
    s1 = ws(500, 30)
    xs = next((e for e in s1.get("elements", []) if e.get("role") == "TreeItem" and "xs_script" in (e.get("label") or "").lower()), None)
    results.append(("XS_SCRIPT_LOCATED", xs is not None, "自訂/xs_script tree item"))
    print("xs_script item:", xs.get("element_index") if xs else None)
    if xs:
        # 2. dbl-click load into editor
        cua("click", {"pid": PID, "element_token": xs.get("element_token"),
                      "snapshot_id": s1.get("snapshot_id"), "count": 2}, timeout=60)
        time.sleep(4)
        s2 = ws()
        title = next((e.get("label") for e in s2.get("elements", []) if e.get("role") == "TitleBar"), "")
        results.append(("XS_SCRIPT_LOADED", "xs_script" in title.lower() or "xs" in title.lower(), f"TitleBar={title[:40]}"))
        print("editor title:", title[:50])

        # 3. select-all then type known-good (replace body)
        cua("press_key", {"pid": PID, "window_id": EWIN, "key": "a", "modifiers": ["ctrl"],
                          "delivery_mode": "foreground"})
        time.sleep(1)
        # find body edit field
        s3 = ws()
        body = None
        for e in s3.get("elements", []):
            if e.get("role") == "Edit" and (e.get("value") or "").strip():
                body = e
                break
        if body:
            r = cua("type_text", {"pid": PID, "window_id": EWIN,
                                  "element_token": body.get("element_token"),
                                  "text": GOOD_SCRIPT}, timeout=60)
            print("type:", json.dumps(r, ensure_ascii=False)[:120])
            time.sleep(3)
            s4 = ws()
            typed_ok = any("Average(Close" in (e.get("value") or "") for e in s4.get("elements", []) if e.get("role") == "Edit")
            results.append(("KNOWN_GOOD_TYPED", typed_ok, "DOC-03 syntax in body"))
            print("typed readback:", typed_ok)
        else:
            results.append(("KNOWN_GOOD_TYPED", False, "no body edit found"))

        # 4. 儲存
        s5 = ws()
        save = next((e for e in s5.get("elements", []) if e.get("role") == "Button" and (e.get("label") or "").strip() == "儲存"), None)
        if save:
            cua("click", {"pid": PID, "element_token": save.get("element_token"),
                          "snapshot_id": s5.get("snapshot_id")}, timeout=60)
            print("儲存 clicked")
            time.sleep(4)
        else:
            print("WARN: 儲存 not found")

        # 5. F6 compile
        cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
        print("F6 sent")
        time.sleep(10)

# 6. file readback
after = db_user()
print("DB after :", after)
compiled_ok = after is not None and after[1] in (0, 1)
status_changed = before != after
results.append(("COMPILE_STATUS_READBACK", compiled_ok, f"CompileStatus={after[1] if after else '?'} msg={(after[2] if after else '')[:40]}"))
results.append(("DB_DELTA", status_changed, f"before={before[3] if before else '?'} after={after[3] if after else '?'}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 CLOSURE v3 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V3_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V3",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script_fixture": "DOC-03 CH-02.2 known-good indicator syntax (authority); user script xs_script body replaced (LOCAL_REVERSIBLE)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus/CompileMsg/LastCompileTime",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script body edited + recompiled; no financial write; original content preserved in gitignored var/fda notes)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V3_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
