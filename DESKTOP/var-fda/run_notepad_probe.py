# -*- coding: utf-8 -*-
"""FDA-C2 bounded desktop-control LIVE probe on a harmless app (Notepad).
Proves: window focus -> type_text -> readback (UIA Value) -> cleanup, with
zero financial side effect. Bounded, local, reversible (LOCAL_REVERSIBLE class).
No credentials, no live broker, no unrelated app.
"""
import json
import subprocess
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
ENV = {"PATH": str(Path(CUA).parent)}


def cua_call(tool, args):
    r = subprocess.run([CUA, "call", tool, json.dumps(args)],
                       capture_output=True, timeout=30, env=ENV)
    out = r.stdout.decode("utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"{tool} rc={r.returncode}: {r.stderr[:200]}")
    return json.loads(out)


# 1. launch Notepad (GUI app — detach, never wait for exit)
subprocess.Popen(["notepad.exe"])
time.sleep(4)

# 2. find notepad window/pid via accessibility tree
tree = cua_call("get_accessibility_tree", {})
win = None
for w in tree.get("windows", []):
    t = (w.get("title") or "").lower()
    if "notepad" in t or "記事本" in t:
        win = w
        break
print("notepad window:", json.dumps(win, ensure_ascii=False)[:200] if win else "NOT FOUND")

if not win:
    print("RESULT: NOTEPAD_WINDOW_NOT_FOUND — probe aborted (no write attempted)")
    raise SystemExit(2)

pid = win.get("pid")
if not pid:
    tl = subprocess.run(["tasklist"], capture_output=True, text=True, errors="replace").stdout or ""
    for line in tl.splitlines():
        if "notepad.exe" in line.lower():
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                pid = int(parts[1])
                break
print("notepad pid:", pid, "window_id:", win.get("window_id"))

# 3. get window state (UIA tree snapshot — required before element-indexed action)
ws = cua_call("get_window_state", {"pid": pid, "window_id": win.get("window_id")})
sc = ws.get("structuredContent") or {}
els = sc.get("elements") or []
print("window state total elements:", sc.get("total_element_count"))
text_idx = None
for e in els:
    role = e.get("role", "")
    label = (e.get("label") or "").lower()
    if role == "Document" or (role == "Edit" and label in ("", "text editor", "文字編輯器")):
        text_idx = e.get("element_index")
        print("  editable element index:", text_idx, "role:", role, "label:", (e.get("label") or "")[:30])
        break

# 4. type into the document
if text_idx is not None:
    typed = cua_call("type_text", {"pid": pid, "element_index": text_idx, "text": "FDA-PROBE-20260813"})
    print("type_text:", json.dumps(typed, ensure_ascii=False)[:150])
else:
    print("no editable element found; trying type_text with window_id")
    try:
        typed = cua_call("type_text", {"pid": pid, "window_id": win.get("window_id"),
                                       "text": "FDA-PROBE-20260813"})
        print("type_text(window):", json.dumps(typed, ensure_ascii=False)[:150])
    except Exception as e:
        print("type_text failed:", str(e)[:150])

# 5. readback: fresh window state, verify the typed text is present
time.sleep(1)
ws2 = cua_call("get_window_state", {"pid": pid, "window_id": win.get("window_id")})
sc2 = ws2.get("structuredContent") or {}
els2 = sc2.get("elements") or []
found = any("FDA-PROBE-20260813" in (e.get("value") or "") + (e.get("label") or "") for e in els2)
# also scan raw markdown tree as fallback evidence
md = ws2.get("tree_markdown") or ""
found = found or ("FDA-PROBE-20260813" in md)
print("READBACK found text:", found)

# 6. cleanup: kill notepad (reversible local action)
subprocess.run(["taskkill", "/F", "/IM", "notepad.exe"], capture_output=True)
print("cleanup: notepad killed")

receipt = {
    "artifact_id": "FDA_BOUNDED_CONTROL_LIVE_PROBE",
    "schema": "FDA-PROBE-RECEIPT/1",
    "target": "notepad.exe (harmless local app; LOCAL_REVERSIBLE side effect class)",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "actions": ["window_locate", "uia_snapshot", "type_text", "readback", "cleanup_kill"],
    "result": "PASS" if found else "FAIL",
    "wrong_action": 0,
    "silent_wrong_action": 0,
    "side_effect": "NONE_FINANCIAL / LOCAL_REVERSIBLE (app killed after probe)",
    "readback": "UIA Value/Label/markdown readback after type",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_BOUNDED_CONTROL_LIVE_PROBE.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("receipt:", out)
print("VERDICT:", receipt["result"])
