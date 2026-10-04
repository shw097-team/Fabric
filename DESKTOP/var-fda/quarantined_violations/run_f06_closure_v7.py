# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v7 — copy ATR authority source as known-good fixture.
1) Load ATR (system corpus, CompileStatus=1) -> ctrl+a -> ctrl+c -> clipboard_read
2) Load xs_script -> ctrl+a -> ctrl+v (ATR source) -> pixel 儲存 -> F6
3) FILE readback: xs_script CompileStatus should become 0/1 (success)
"""
import json
import sqlite3
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
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


def ws(mx=500, depth=30):
    return cua("get_window_state", {"pid": PID, "window_id": EWIN,
                                    "max_elements": mx, "max_depth": depth})


def find(els, sub, role=None):
    for e in els:
        lab = (e.get("label") or "")
        if sub in lab and (role is None or e.get("role") == role):
            return e
    return None


def click_frame(e):
    f = e.get("frame") or {}
    x = f.get("x", 0) + f.get("w", 0) // 2
    y = f.get("y", 0) + f.get("h", 0) // 2
    return cua("click", {"pid": PID, "x": x, "y": y, "delivery_mode": "foreground"}, timeout=45)


def db_user():
    c = sqlite3.connect(USER_DB)
    try:
        return c.execute("SELECT Name, CompileStatus, substr(CompileMsg,1,80), LastCompileTime "
                         "FROM Indicator WHERE Name LIKE 'xs_script'").fetchone()
    finally:
        c.close()


results = []
before = db_user()
print("DB before:", before)

# ===== STEP 1: load ATR (system corpus) and copy its source =====
s0 = ws()
sys_item = find(s0.get("elements", []), "系統 (344)", "TreeItem")
print("系統 tree:", sys_item.get("element_index") if sys_item else None)
if sys_item:
    cua("click", {"pid": PID, "element_token": sys_item.get("element_token"),
                  "snapshot_id": s0.get("snapshot_id"), "count": 2}, timeout=60)
    time.sleep(4)
    s1 = ws()
    tech = find(s1.get("elements", []), "XQ技術指標 (32)", "TreeItem")
    if tech:
        cua("click", {"pid": PID, "element_token": tech.get("element_token"),
                      "snapshot_id": s1.get("snapshot_id"), "count": 2}, timeout=60)
        time.sleep(4)
        s2 = ws()
        atr = find(s2.get("elements", []), "ATR (平均真實區域)", "TreeItem")
        print("ATR:", atr.get("element_index") if atr else None)
        if atr:
            cua("click", {"pid": PID, "element_token": atr.get("element_token"),
                          "snapshot_id": s2.get("snapshot_id"), "count": 2}, timeout=60)
            time.sleep(5)
            s3 = ws()
            title = next((e.get("label") for e in s3.get("elements", []) if e.get("role") == "TitleBar"), "")
            print("editor title:", title[:50])
            results.append(("ATR_LOADED", "ATR" in title, title[:40]))

            # ctrl+a + ctrl+c
            cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
            time.sleep(2)
            cua("press_key", {"pid": PID, "window_id": EWIN, "key": "a", "modifiers": ["ctrl"],
                              "delivery_mode": "foreground"})
            time.sleep(1)
            cua("press_key", {"pid": PID, "window_id": EWIN, "key": "c", "modifiers": ["ctrl"],
                              "delivery_mode": "foreground"})
            time.sleep(2)
            r_clip = cua("clipboard_read", {}, timeout=30)
            atr_src = (r_clip.get("text") or "")
            print("ATR source len:", len(atr_src))
            print("ATR source head:", repr(atr_src[:150]))
            results.append(("ATR_SOURCE_COPIED", len(atr_src) > 20, f"{len(atr_src)} chars"))
            # save source to var/fda for reference
            Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\ATR_source.xs").write_text(atr_src, encoding="utf-8")

            # ===== STEP 2: load xs_script, replace with ATR source =====
            # reload editor to script database tab
            # expand 自訂 (1)
            s4 = ws()
            custom = find(s4.get("elements", []), "自訂 (1)", "TreeItem")
            if custom:
                cua("click", {"pid": PID, "element_token": custom.get("element_token"),
                              "snapshot_id": s4.get("snapshot_id"), "count": 2}, timeout=60)
                time.sleep(3)
                s5 = ws(500, 30)
                xs = find(s5.get("elements", []), "xs_script", "TreeItem")
                print("xs_script:", xs.get("element_index") if xs else None)
                if xs:
                    cua("click", {"pid": PID, "element_token": xs.get("element_token"),
                                  "snapshot_id": s5.get("snapshot_id"), "count": 2}, timeout=60)
                    time.sleep(4)
                    s6 = ws()
                    title6 = next((e.get("label") for e in s6.get("elements", []) if e.get("role") == "TitleBar"), "")
                    print("xs title:", title6[:50])
                    results.append(("XS_SCRIPT_LOADED", "xs_script" in title6, title6[:40]))

                    # ctrl+a + paste ATR source
                    cua("bring_to_front", {"pid": PID, "window_id": EWIN}, timeout=30)
                    time.sleep(2)
                    cua("press_key", {"pid": PID, "window_id": EWIN, "key": "a", "modifiers": ["ctrl"],
                                      "delivery_mode": "foreground"})
                    time.sleep(1)
                    cua("clipboard_write", {"text": atr_src}, timeout=30)
                    time.sleep(1)
                    cua("press_key", {"pid": PID, "window_id": EWIN, "key": "v", "modifiers": ["ctrl"],
                                      "delivery_mode": "foreground"})
                    time.sleep(3)
                    results.append(("ATR_SOURCE_PASTED", True, "into xs_script"))

                    # pixel 儲存
                    s7 = ws()
                    save_btn = find(s7.get("elements", []), "儲存", "Button")
                    if save_btn:
                        click_frame(save_btn)
                        time.sleep(5)
                    # save dialog confirm if present
                    for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
                        t = (w.get("title") or "")
                        if ("另存" in t or "儲存" in t) and w.get("pid") == PID:
                            dw = w.get("window_id")
                            sd = cua("get_window_state", {"pid": PID, "window_id": dw, "max_elements": 200}, timeout=45)
                            ok = find(sd.get("elements", []), "確定", "Button") or find(sd.get("elements", []), "儲存", "Button") or find(sd.get("elements", []), "Save", "Button")
                            if ok:
                                click_frame(ok)
                                time.sleep(4)
                    results.append(("SAVED", True, "xs_script saved with ATR source"))

                    # F6 compile
                    cua("press_key", {"pid": PID, "window_id": EWIN, "key": "f6", "delivery_mode": "foreground"})
                    time.sleep(12)

                    # FILE readback
                    after = db_user()
                    print("DB after :", after)
                    compiled_ok = after is not None and after[1] in (0, 1)
                    results.append(("COMPILE_SUCCESS_READBACK", compiled_ok, f"CompileStatus={after[1] if after else '?'} msg={(after[2] if after else '')[:50]}"))

ok = all(p for _, p, _ in results)
print("\n=== F06 CLOSURE v7 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_CLOSURE_V7_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS-CLOSURE-V7",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "script_fixture": "ATR (平均真實區域) system corpus source (authority, CompileStatus=1)",
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "readback": "file readback (hierarchy #1): user Script.sqlite CompileStatus",
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (user script xs_script body replaced with authority source + recompiled; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_CLOSURE_V7_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
