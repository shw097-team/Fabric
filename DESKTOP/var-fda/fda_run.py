# -*- coding: utf-8 -*-
"""fda_run.py — FDA 統一執行器：preflight guard → 執行 → 異常自動 screen_state_check。
所有 FDA 自動化腳本必須經此執行（禁止直接 python <script>）。"""
import subprocess
import sys
import time
from pathlib import Path

FAR = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda")
PY = r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe"

def main():
    if len(sys.argv) < 2:
        print("usage: fda_run.py <script.py> [args...]")
        sys.exit(2)
    script = Path(sys.argv[1])
    if not script.is_absolute():
        script = FAR / script
    if not script.exists():
        print(f"fda_run: script not found: {script}")
        sys.exit(2)

    # 0. REUSE-FIRST check: query FDA_ASSET_REGISTRY for the operation's asset mapping
    try:
        REG = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_ASSET_REGISTRY.json")
        if REG.exists():
            import json as _json
            reg = _json.load(open(REG, encoding="utf-8"))
            adapter_fns = list(reg.get("assets", {}).get("adapter", {}).get("functions", {}).keys())
            print(f"fda_run: registry loaded ({len(adapter_fns)} adapter functions available)")
            print(f"fda_run: REUSE-FIRST — check registry before implementing new logic; "
                  f"adapter fns: {adapter_fns[:8]}...")
    except Exception as e:
        print(f"fda_run: registry check skipped ({str(e)[:40]})")

    # 1. preflight guard
    guard = FAR / "fda_script_guard.py"
    g = subprocess.run([PY, str(guard), str(script)], capture_output=True, text=True, timeout=60)
    if g.returncode != 0:
        print("=" * 60)
        print("fda_run: PREFLIGHT BLOCKED — script violates hard no-mouse route:")
        print(g.stdout)
        print("Execution FORBIDDEN. Rewrite pure-message or fix, then re-run guard.")
        print("=" * 60)
        sys.exit(1)
    print(f"fda_run: preflight PASS — {script.name}")

    # 2. execute
    t0 = time.time()
    args = [PY, str(script)] + sys.argv[2:]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        print("fda_run: script TIMEOUT (>900s)")
        sys.exit(3)
    dt = time.time() - t0
    if r.stdout:
        print(r.stdout[-4000:])
    if r.stderr:
        print("STDERR:", r.stderr[-2000:])

    # 3. anomaly -> auto screen_state_check
    if r.returncode != 0:
        print("=" * 60)
        print(f"fda_run: exit={r.returncode} — FIXED ROUTE: auto screen_state_check (anomaly → check screen)")
        print("=" * 60)
        ssc = FAR / "screen_state_check.py"
        if ssc.exists():
            s = subprocess.run([PY, str(ssc)], capture_output=True, text=True, timeout=120)
            print(s.stdout[-3000:])
        else:
            print("screen_state_check.py missing!")
        sys.exit(r.returncode)

    print(f"fda_run: OK ({dt:.0f}s, exit 0)")
    sys.exit(0)

if __name__ == "__main__":
    main()
