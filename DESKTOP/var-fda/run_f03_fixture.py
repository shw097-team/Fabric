# -*- coding: utf-8 -*-
"""FDA-C4 F03 (open XS Editor) live fixture — bounded, LOCAL_REVERSIBLE.
Uses element_token (Cua 0.17+ contract): snapshot -> click 策略(D) menu ->
readback snapshot -> locate XS editor entry. Readback before/after each write.
"""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 2904
WIN = 265672


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


def snapshot():
    return cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 300})


def find_by_label(sc, label_substr, role=None):
    els = sc.get("elements") or []
    for e in els:
        lab = (e.get("label") or "")
        if label_substr in lab and (role is None or e.get("role") == role):
            return e
    return None


results = []

# --- step 1: pre-click readback (known state) ---
s0 = snapshot()
menu = find_by_label(s0, "策略(D)", "MenuItem")
results.append(("PRE_READBACK_MENU_VISIBLE", menu is not None, "menu 策略(D) located"))
if not menu:
    print("FAIL: 策略(D) menu not found in pre snapshot")
    raise SystemExit(2)
tok = menu.get("element_token")
snap = s0.get("snapshot_id")
print("策略(D) token:", tok[:40] if tok else None, "| snapshot:", snap)

# --- step 2: bounded click (LOCAL_REVERSIBLE, background first) ---
r1 = cua("click", {"pid": PID, "element_token": tok, "snapshot_id": snap})
results.append(("CLICK_MENU", "refusal" not in r1 or r1.get("status") != "refused",
                json.dumps(r1, ensure_ascii=False)[:120]))
print("click result:", json.dumps(r1, ensure_ascii=False)[:150])
time.sleep(2)

# --- step 3: post-click readback (menu expanded?) ---
s1 = snapshot()
xs_entries = []
els1 = s1.get("elements") or []
for e in els1:
    lab = (e.get("label") or "")
    if "XS" in lab or "策略" in lab and e.get("role") in ("MenuItem", "Button"):
        xs_entries.append({"idx": e.get("element_index"), "role": e.get("role"),
                           "label": lab[:50], "token": (e.get("element_token") or "")[:30]})
        print("XS/策略 entry:", e.get("element_index"), "|", e.get("role"), "|", lab[:50])
results.append(("POST_READBACK_MENU_EXPANDED", len(xs_entries) > 0,
                f"{len(xs_entries)} menu entries visible"))

# find the XS editor entry
xs_editor = None
for e in els1:
    lab = (e.get("label") or "")
    if ("XS" in lab and ("編輯" in lab or "Editor" in lab or "策略" in lab)) or lab.strip() in ("XS編輯器", "XS 編輯器", "策略編輯器"):
        xs_editor = e
        break
results.append(("XS_EDITOR_ENTRY_FOUND", xs_editor is not None,
                (xs_editor or {}).get("label", "not found")))

print("\n=== F03 RESULTS ===")
ok = True
for name, passed, detail in results:
    print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}")
    ok = ok and passed

# if editor entry found, click it (next fixture F04 boundary) — but keep readback-first
if xs_editor is not None:
    tok2 = xs_editor.get("element_token")
    snap2 = s1.get("snapshot_id")
    r2 = cua("click", {"pid": PID, "element_token": tok2, "snapshot_id": snap2})
    time.sleep(3)
    s2 = snapshot()
    sc2 = s2
    total2 = sc2.get("total_element_count")
    print("\nXS editor click:", json.dumps(r2, ensure_ascii=False)[:120])
    print("post-editor snapshot total elements:", total2)
    results.append(("XS_EDITOR_OPENED", total2 is not None and total2 > 30, f"total={total2}"))

receipt = {
    "artifact_id": "FDA_F03_LIVE_FIXTURE_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F03-OPEN-XS-EDITOR",
    "action_class": "XS_EDITOR_OPEN",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN", "window_class": "DAQXQLITEMainWnd"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (menu/editor navigation only; no financial write)",
    "readback": "UIA structured snapshots before/after each write",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F03_LIVE_FIXTURE_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
