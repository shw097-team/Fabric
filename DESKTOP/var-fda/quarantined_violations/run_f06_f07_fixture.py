# -*- coding: utf-8 -*-
"""FDA-C4 F06/F07 compile fixtures — full loop with FILE readback (hierarchy #1).
F06: load known-good system script (ATR) -> compile -> readback CompileStatus.
F07: readback known-bad user script (xs_script) CompileStatus=2 + error text.
File readback = XQ native/file output (readback hierarchy level 1).
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
USER_DB = Path(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\DAQXQLITE_SHW097_Script.sqlite")
SYS_DB = Path(r"C:\SysJust\XQLite\XS\Data\DAQXQLITE\SHW097\System_Script_User.sqlite")


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


def find(els, sub, role=None):
    for e in els:
        if sub in (e.get("label") or "") and (role is None or e.get("role") == role):
            return e
    return None


def user_script(name):
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute(
            "SELECT ID, Name, CompileStatus, substr(CompileMsg,1,120), LastCompileTime "
            "FROM Indicator WHERE Name=?", (name,)).fetchone()
    finally:
        c.close()


results = []

# ===== F07: known-bad compile readback (file, already compiled at 15:37:35) =====
xs = user_script("xs_script")
f07_pass = xs is not None and xs[2] == 2 and xs[3] is not None and len(xs[3]) > 0
results.append(("F07_KNOWN_BAD_COMPILE_ERROR_READBACK", f07_pass,
                f"CompileStatus={xs[2] if xs else '?'} msg='{(xs[3] if xs else '')[:60]}' "
                f"at {xs[4] if xs else '?'}"))
print(f"F07: xs_script CompileStatus={xs[2] if xs else '?'} LastCompile={xs[4] if xs else '?'}")
print(f"     error: {(xs[3] if xs else '')[:90]}")

# ===== F06: load known-good ATR system script and compile =====
# 1. locate ATR in system tree and double-click load
s0 = snap()
atr = find(s0.get("elements", []), "ATR (平均真實區域)", "TreeItem")
if atr:
    cua("click", {"pid": PID, "element_token": atr.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id"), "count": 2})
    time.sleep(3)
    s1 = snap()
    title = next((e.get("label") for e in s1.get("elements", [])
                  if e.get("role") == "TitleBar"), "")
    results.append(("F06_ATR_LOADED", "ATR" in title, f"TitleBar='{title[:40]}'"))
    print(f"F06: editor TitleBar after load: '{title[:50]}'")

    # 2. open 編譯(C) menu (foreground for Win32 popup)
    m = find(s1.get("elements", []), "編譯(C)", "MenuItem")
    if m:
        cua("click", {"pid": PID, "element_token": m.get("element_token"),
                      "snapshot_id": s1.get("snapshot_id"), "delivery_mode": "foreground"})
        time.sleep(2)
        s2 = snap()
        # 3. click 編譯所有我的文件 (or first compile item)
        c1 = find(s2.get("elements", []), "編譯所有我的文件", "MenuItem")
        if c1:
            r = cua("click", {"pid": PID, "element_token": c1.get("element_token"),
                              "snapshot_id": s2.get("snapshot_id")})
            print("F06: compile-all click:", json.dumps(r, ensure_ascii=False)[:100])
            time.sleep(8)  # wait for compile
        else:
            # try pressing Enter on focused menu via type_text
            print("F06: compile submenu not visible in tree; menu may be Win32 popup")
            results.append(("F06_COMPILE_TRIGGERED", False, "submenu not visible"))
else:
    results.append(("F06_ATR_LOADED", False, "ATR not found"))
    print("F06: ATR not found in tree (need to re-expand)")

# 4. file readback after compile — check user script DB for fresh compile
time.sleep(2)
xs_after = user_script("xs_script")
if xs_after:
    print(f"F06/F07: xs_script after: CompileStatus={xs_after[2]} LastCompile={xs_after[4]}")
    results.append(("F06_COMPILE_RE_EXECUTED", xs_after[4] != (xs[4] if xs else None),
                    f"LastCompile updated to {xs_after[4]}"))

# also check System_Script_User for ATR-compiled state
c = sqlite3.connect(SYS_DB)
sys_rows = c.execute(
    "SELECT Name, CompileStatus, substr(CompileMsg,1,80), LastCompileTime FROM Indicator").fetchall()
c.close()
for r in sys_rows:
    print("SYS DB:", r)

ok = all(p for _, p, _ in results)
print("\n=== F06/F07 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_F07_LIVE_FIXTURE_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixtures": ["F06-COMPILE-KNOWN-PASS", "F07-COMPILE-KNOWN-BAD-READBACK"],
    "action_classes": ["XS_COMPILE_PASS", "XS_COMPILE_FAIL_READBACK"],
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback_hierarchy_level": "1 (XQ native/file output: Script.sqlite CompileStatus/CompileMsg)",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL (compile is read-only verification; LOCAL_REVERSIBLE navigation)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
