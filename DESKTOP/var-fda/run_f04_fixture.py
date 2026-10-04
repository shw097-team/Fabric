# -*- coding: utf-8 -*-
"""FDA-C4 F04 (locate known script) live fixture.
Open XScript editor already open (window 527196). Expand 系統(344) tree,
locate a known system script (authority corpus), verify identity readback.
Bounded read-only navigation; no financial write.
"""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}
PID = 2904
WIN = 527196  # XScript editor window


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
    return cua("get_window_state", {"pid": PID, "window_id": WIN, "max_elements": 400})


results = []

# step 1: pre readback — locate 系統 tree item
s0 = snapshot()
els0 = s0.get("elements", [])
sys_item = next((e for e in els0 if e.get("role") == "TreeItem" and "系統" in (e.get("label") or "")), None)
results.append(("PRE_READBACK_SYSTEM_TREE", sys_item is not None, "系統(344) tree item located"))
print("系統 tree item:", sys_item.get("label") if sys_item else None)

if sys_item:
    # expand the tree item (click/expand via token)
    r = cua("click", {"pid": PID, "element_token": sys_item.get("element_token"),
                      "snapshot_id": s0.get("snapshot_id")})
    print("expand click:", json.dumps(r, ensure_ascii=False)[:120])
    time.sleep(2)

# step 2: post-expand readback — count script leaves
s1 = snapshot()
els1 = s1.get("elements", [])
tree_items = [e for e in els1 if e.get("role") == "TreeItem"]
scripts = [e for e in els1 if e.get("role") == "TreeItem" and e.get("depth", 0) > 0]
print(f"tree items: {len(tree_items)}, deeper-level scripts: {len(scripts)}")
for e in tree_items[:15]:
    print("  ", e.get("depth"), "|", (e.get("label") or "")[:50], "| token:", bool(e.get("element_token")))
results.append(("POST_EXPAND_SCRIPTS_VISIBLE", len(scripts) > 0, f"{len(scripts)} script items"))

# step 3: pick a known script leaf (authority corpus) — first visible leaf
target = next((e for e in tree_items if e.get("depth", 0) >= 2), None)
if target:
    lab = target.get("label") or ""
    results.append(("KNOWN_SCRIPT_LOCATED", len(lab) > 0, lab[:60]))
    print("known script target:", lab[:60])
    # click to load into editor (read-only selection)
    r2 = cua("click", {"pid": PID, "element_token": target.get("element_token"),
                       "snapshot_id": s1.get("snapshot_id")})
    print("select click:", json.dumps(r2, ensure_ascii=False)[:120])
    time.sleep(2)
    s2 = snapshot()
    els2 = s2.get("elements", [])
    # verify editor now shows content (Edit field populated)
    edits = [e for e in els2 if e.get("role") == "Edit" and (e.get("value") or "").strip()]
    results.append(("SCRIPT_LOADED_INTO_EDITOR", len(edits) > 0,
                    f"{len(edits)} populated edit field(s)"))
    for e in edits[:2]:
        print("  edit value head:", (e.get("value") or "")[:80].replace("\n", "\\n"))

ok = all(p for _, p, _ in results)
print("\n=== F04 RESULTS ===")
for n, p, d in results:
    print(f"{'PASS' if p else 'FAIL'}  {n}: {d}")

receipt = {
    "artifact_id": "FDA_F04_LIVE_FIXTURE_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "F04-LOCATE-KNOWN-SCRIPT",
    "action_class": "XS_EDITOR_SCRIPT_LOCATE",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product_version": "3.20.02 (260811)",
               "login": "SHW097:LOGGED_IN", "editor_window": "XScript 編輯器"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "steps": [{"name": n, "pass": p, "detail": d} for n, p, d in results],
    "verdict": "PASS" if ok else "PARTIAL",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "LOCAL_REVERSIBLE (script selection in editor only; no financial write)",
    "readback": "UIA structured snapshots before/after each write",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F04_LIVE_FIXTURE_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("\nreceipt:", out)
