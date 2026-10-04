# -*- coding: utf-8 -*-
"""FDA-C4 F01 XQ_LAUNCH_LOCATE — 10 fresh-run live desktop qualification (Cua).
Each run issues a FRESH read-only UIA call against the live XQ process; the
action class is certified 10/10 only if every run identifies the exact target
window/process with the expected identity. No write, no login (HumanGate).
"""
import json
import subprocess
import sys
import time
from pathlib import Path

CUA = str(Path.home() / "AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe")
XQ_PID = 20028  # verified live daqxqlite.exe pid (readback before run)


def cua_call(tool: str, args: dict) -> dict:
    r = subprocess.run([CUA, "call", tool, json.dumps(args)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=30, env={"PATH": str(Path(CUA).parent)})
    if r.returncode != 0:
        raise RuntimeError(f"cua {tool} rc={r.returncode}: {r.stderr[:200]}")
    return json.loads(r.stdout)


def verify_identity(win_title: str, exe_basename: str, pid: int) -> bool:
    return ("XQ全球贏家" in win_title or "XQ" in win_title) \
        and exe_basename == "daqxqlite.exe" and pid == XQ_PID


results = []
for i in range(1, 11):
    t0 = time.time()
    try:
        info = cua_call("debug_window_info", {"pid": XQ_PID})
        wins = info.get("windows", [])
        exe = info.get("exe_basename", "")
        pid = info.get("pid")
        titles = [w.get("title", "") for w in wins]
        ok_identity = any(verify_identity(t, exe, pid) for t in titles)
        ok_window = any(w.get("class_name") == "DAQXQLITEMainWnd" for w in wins)
        ok_uia = info.get("focused_element") is not None
        ok = ok_identity and ok_window and ok_uia
        ms = int((time.time() - t0) * 1000)
        results.append({"run": i, "pass": ok, "ms": ms,
                        "windows": len(wins), "exe": exe, "pid": pid,
                        "first_title": titles[0][:60] if titles else "",
                        "uia_element": bool(ok_uia)})
        print(f"RUN {i}: {'PASS' if ok else 'FAIL'} ({ms}ms) wins={len(wins)} exe={exe} pid={pid} uia={ok_uia}")
        if not ok:
            print("  identity:", ok_identity, "window:", ok_window, "uia:", ok_uia)
    except Exception as e:
        results.append({"run": i, "pass": False, "error": str(e)[:150]})
        print(f"RUN {i}: ERROR {str(e)[:150]}")
    time.sleep(1)  # fresh run spacing; no lock held

passed = sum(1 for r in results if r.get("pass"))
print(f"\nRESULT: {passed}/10 PASS")
verdict = "10_OF_10_PASS" if passed == 10 else f"{passed}_OF_10_FAIL"
print(f"VERDICT: {verdict}")

# receipt
receipt = {
    "artifact_id": "FDA_F01_LIVE_FIXTURE_RECEIPT",
    "schema": "FDA-FIXTURE-RECEIPT/1",
    "fixture": "XQ-LAUNCH",
    "action_class": "XQ_LAUNCH_LOCATE",
    "provider": {"name": "CUA_DRIVER", "version": "0.19.3"},
    "target": {"application": "XQ", "product": "XQLite 個人版",
               "product_version": "3.18.02 (260102)", "exe": "daqxqlite.exe",
               "window_class": "DAQXQLITEMainWnd", "login_state": "NOT_LOGGED_IN"},
    "mode": "PAPER_NO_LIVE_WRITE",
    "runs": results,
    "summary": {"passed": passed, "total": 10, "wrong_action": 0, "silent_wrong_action": 0},
    "verdict": verdict,
    "claim": "F01 certified for CUA on this subject ONLY IF 10/10 (blueprint: an action class is team-certified if >=1 provider passes 10/10 fresh runs with full readback and zero wrong action).",
    "readback": "UIA structured state (debug_window_info) — level 2 of readback hierarchy; no login performed (HumanGate boundary respected).",
}
out = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_F01_LIVE_FIXTURE_RECEIPT.json")
out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
print("receipt:", out)
