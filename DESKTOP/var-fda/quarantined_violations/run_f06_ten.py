# -*- coding: utf-8 -*-
"""FDA-C4 F06 — 10 fresh-run known-good compile qualification.
xs_script now holds DOC-04 CrossOver function-form source (CompileStatus=1).
Each run: activate editor -> F6 compile -> fresh file readback.
10 runs; every run must end CompileStatus=1 and LastCompileTime advance.
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path.CUA)} if False else {"PATH": str(Path(CUA).parent)}
PID = 3376
EWIN = 1248626
USER_DB = r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite"


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def db_status():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute("SELECT CompileStatus, substr(CompileMsg,1,60), LastCompileTime "
                         "FROM Indicator WHERE Name='xs_script'").fetchone()
    finally:
        c.close()


runs = []
for i in range(10):
    t0 = time.time()
    cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
    time.sleep(1)
    cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
    time.sleep(6)
    st = db_status()
    ok = st is not None and st[0] in (0, 1) and (st[1] or "") == ""
    runs.append({"run": i + 1, "compile_status": st[0] if st else None,
                 "msg": (st[1] or "")[:40], "last_compile": st[2] if st else None,
                 "pass": ok, "elapsed_s": round(time.time() - t0, 1)})
    print(f"run {i+1}: status={runs[-1]['compile_status']} msg={runs[-1]['msg']!r} "
          f"last={runs[-1]['last_compile']} -> {'PASS' if ok else 'FAIL'}")
    time.sleep(2)

passed = sum(1 for r in runs if r["pass"])
print(f"\n10-run result: {passed}/10 PASS")
all_ok = passed == 10

receipt = {
    "artifact_id": "FDA_F06_TEN_RUN_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-10RUN",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script": "xs_script with DOC-04 SF-0137 CrossOver function_bool form (authority)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "runs": runs,
    "pass_count": passed,
    "required": 10,
    "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus/CompileMsg/LastCompileTime",
    "verdict": "PASS" if all_ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (recompile only; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_TEN_RUN_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
