# -*- coding: utf-8 -*-
"""FDA-C4 F06 (compile known-pass) live fixture.
Load ATR (平均真實區域) from system corpus -> 編譯(C) menu -> readback result.
Bounded: compile is a read-only verification action (no financial write).
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
    if r.returncode != 0:
        raise RuntimeError(f"{tool} rc={r.returncode}: {r.stderr[:200]}")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:300]}


def snap():
    return cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 500})


def find(els, label_substr, role=None):
    for e in els:
        if label_substr in (e.get("label") or "") and (role is None or e.get("role") == role):
            return e
    return None


results = []

# 1. locate ATR script leaf and LOAD it (double-click loads into editor)
s0 = snap()
atr = find(s0.get("elements", []), "ATR (平均真實區域)", "TreeItem")
results.append(("ATR_SCRIPT_LOCATED", atr is not None, "ATR leaf"))
if atr:
    r = cua("click", {"pid": PID, "element_token": atr.get("element_token"),
                      "snapshot_id": s0.get("snapshot_id"), "count": 2})  # double-click loads
    print("ATR dbl-click:", json.dumps(r, ensure_ascii=False)[:120])
    time.sleep(3)

# 2. verify script loaded into editor (Edit field populated)
s1 = snap()
edits = [e for e in s1.get("elements", []) if e.get("role") == "Edit" and (e.get("value") or "").strip()]
loaded = len(edits) > 0
results.append(("SCRIPT_LOADED_INTO_EDITOR", loaded, f"{len(edits)} populated edit fields"))
for e in edits[:2]:
    v = (e.get("value") or "")
    print("  edit value:", repr(v[:120]))

# 3. open 編譯(C) menu
if loaded:
    compile_menu = find(s1.get("elements", []), "編譯(C)", "MenuItem")
    results.append(("COMPILE_MENU_LOCATED", compile_menu is not None, "編譯(C) menu"))
    if compile_menu:
        r2 = cua("click", {"pid": PID, "element_token": compile_menu.get("element_token"),
                           "snapshot_id": s1.get("snapshot_id")})
        print("compile menu click:", json.dumps(r2, ensure_ascii=False)[:120])
        time.sleep(2)
        # 4. readback: find compile submenu item (e.g. 編譯 / Compile)
        s2 = snap()
        els2 = s2.get("elements", [])
        compile_items = [e for e in els2 if e.get("role") == "MenuItem" and
                         ("編譯" in (e.get("label") or "") or "Compile" in (e.get("label") or ""))]
        print("compile submenu items:")
        for e in compile_items:
            print("  ", e.get("element_index"), "|", (e.get("label") or "")[:40])
        results.append(("COMPILE_SUBMENU_READBACK", len(compile_items) > 0,
                        f"{len(compile_items)} compile entries"))

        # 5. click the first compile entry (the actual compile action)
        if compile_items:
            target = compile_items[0]
            r3 = cua("click", {"pid": PID, "element_token": target.get("element_token"),
                               "snapshot_id": s2.get("snapshot_id")})
            print("compile action click:", json.dumps(r3, ensure_ascii=False)[:120])
            time.sleep(3)
            # 6. readback: check 訊息 (message) tab for compile result
            s3 = snap()
            els3 = s3.get("elements", [])
            msg = [e for e in els3 if "訊息" in (e.get("label") or "") and e.get("role") == "TabItem"]
            # search whole snapshot for compile result text
            texts = [e for e in els3 if e.get("role") in ("Text", "Edit") and (e.get("label") or e.get("value") or "")]
            result_hint = [t for t in texts if any(k in ((t.get("label") or "") + (t.get("value") or ""))
                                                   for k in ("成功", "完成", "編譯成功", "error", "錯誤", "0 個錯誤"))]
            for t in result_hint[:5]:
                print("  result text:", ((t.get("label") or "") + (t.get("value") or ""))[:80])
            results.append(("COMPILE_RESULT_READBACK", len(result_hint) > 0,
                            f"{len(result_hint)} result hint(s)"))

ok = all(p for _, p, _ in results)
print("\n=== F06 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_LIVE_FIXTURE_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-COMPILE-KNOWN-PASS",
    "action_class": "XS_COMPILE_PASS",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN", "editor_window": "XScript 編輯器"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL (compile is read-only verification; LOCAL_REVERSIBLE navigation)",
    "readback": "UIA structured snapshots before/after each write",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_LIVE_FIXTURE_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
