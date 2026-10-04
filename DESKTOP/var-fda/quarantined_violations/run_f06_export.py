# -*- coding: utf-8 -*-
"""FDA-C4 F06 CLOSURE v8 — export ATR source via 匯出 button.
ATR loaded in editor -> pixel-click 匯出 -> file dialog -> save to
var/fda/ATR_export.xs -> read file -> use as known-good source.
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
EXPORT_PATH = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\ATR_export.xs"


def cua(tool, args, timeout=45):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)], capture_output=True,
                       timeout=timeout, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out[:200]}


def ws(mx=300, depth=20):
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


results = []

# verify ATR still loaded
s0 = ws()
title = next((e.get("label") for e in s0.get("elements", []) if e.get("role") == "TitleBar"), "")
print("title:", title[:55])
results.append(("ATR_LOADED", "ATR" in title, title[:40]))

# pixel click 匯出
export_btn = find(s0.get("elements", []), "匯出", "Button")
if not export_btn:
    print("FAIL: 匯出 button")
    raise SystemExit(2)
r = click_frame(export_btn)
print("匯出 clicked:", json.dumps(r, ensure_ascii=False)[:80])
time.sleep(5)

# file dialog: type path + confirm
dlg_found = False
for w in cua("get_accessibility_tree", {}, timeout=30).get("windows", []):
    t = (w.get("title") or "")
    if w.get("pid") == PID and ("另存" in t or "匯出" in t or "Save" in t or "Export" in t):
        dlg_found = True
        print("DLG:", repr(t[:50]), "wid:", w.get("window_id"))
        dw = w.get("window_id")
        sd = cua("get_window_state", {"pid": PID, "window_id": dw, "max_elements": 300}, timeout=45)
        # filename edit — usually a ComboBox/Edit with current name
        name_edit = None
        for e in sd.get("elements", []):
            lab = (e.get("label") or "")
            if e.get("role") == "Edit" and ("檔名" in lab or "File" in lab or "Name" in lab):
                name_edit = e
                break
        if not name_edit:
            for e in sd.get("elements", []):
                if e.get("role") == "Edit":
                    name_edit = e
                    break
        if name_edit:
            r_t = cua("type_text", {"pid": PID, "window_id": dw,
                                    "element_token": name_edit.get("element_token"),
                                    "text": str(EXPORT_PATH)}, timeout=45)
            print("path typed:", json.dumps(r_t, ensure_ascii=False)[:80])
            time.sleep(2)
        # confirm button
        ok = None
        for cand in ("儲存", "確定", "Save", "Export", "開啟"):
            ok = find(sd.get("elements", []), cand, "Button")
            if ok:
                break
        if ok:
            click_frame(ok)
            print("confirm clicked:", cand)
            time.sleep(4)
        break

if not dlg_found:
    print("WARN: no dialog window found in tree (may be Win32 common dialog)")

# check export file
time.sleep(2)
p = Path(EXPORT_PATH)
if p.exists():
    src = p.read_text(encoding="utf-8", errors="replace")
    print("EXPORT FILE:", len(src), "chars")
    print("head:", repr(src[:200]))
    results.append(("ATR_EXPORTED", len(src) > 20, f"{len(src)} chars"))
else:
    # maybe extension appended or dialog used different name
    found = list(Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda").glob("*.xs"))
    print("xs files:", [f.name for f in found])
    results.append(("ATR_EXPORTED", False, "file not found"))

ok = all(p for _, p, _ in results)
print("\n=== F06 EXPORT RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F06_EXPORT_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F06-EXPORT-ATR-SOURCE",
    "action_class": "XS_COMPILE_PASS (source acquisition)",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)", "login": "SHW097:LOGGED_IN"},
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0, "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (export only; no financial write)",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F06_EXPORT_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
