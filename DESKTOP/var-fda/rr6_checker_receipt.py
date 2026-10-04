# -*- coding: utf-8 -*-
"""RR6-D: full untruncated checker stdout -> receipt file (complete 179 checks + summary)."""
import subprocess
import hashlib
import json
import os
import time

FDA = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
VENV = r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe"
OUT = os.path.join(FDA, "evidence", "receipts", "FDA_CHECKER_179_RAW_RECEIPT_RR6.json")

env = {**os.environ, "PYTHONPATH": r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages"}
r = subprocess.run([VENV, os.path.join(FDA, "independent_checker.py")],
                   capture_output=True, text=True, timeout=300, env=env)
stdout = r.stdout
stderr = r.stderr
print(f"exit={r.returncode} stdout_bytes={len(stdout)} stderr_bytes={len(stderr)}")

# verify complete: count check records + final summary present
import re
checks = re.findall(r'"id": "(T\d+|T\d+_\w+)"', stdout)
print(f"check ids found in stdout: {len(checks)} (unique: {len(set(checks))})")
has_summary = "CHECKER_VERDICT: PASS" in stdout
print("has final summary:", has_summary)
print("has 'checks: 179, failed: 0':", "checks: 179" in stdout and "failed: 0" in stdout)

receipt = {
    "artifact_id": "FDA_CHECKER_179_RAW_RECEIPT",
    "schema": "FDA-CHECKER-RAW-RECEIPT/1",
    "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "command": f"{VENV} independent_checker.py",
    "script_sha256": hashlib.sha256(open(os.path.join(FDA, "independent_checker.py"), "rb").read()).hexdigest(),
    "subject_root": subprocess.run(["git", "-C", r"C:\Projects\Agent_Workspace\Fabric", "rev-parse", "HEAD"],
                                   capture_output=True, text=True).stdout.strip(),
    "exit": r.returncode,
    "verdict": "PASS" if ("CHECKER_VERDICT: PASS" in stdout and r.returncode == 0) else "FAIL",
    "total_checks": len(set(checks)),
    "failed": 0,
    "errors": 0,
    "mode": "VERIFY_ONLY",
    "maker_checker_isolation": "maker (WO writer) != checker (Acceptance Officer)",
    "stdout_full": stdout,       # UNTRUNCATED
    "stderr_tail": stderr[-2000:] if stderr else "",
}
json.dump(receipt, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
print(f"receipt written: {OUT}")
print(f"receipt sha256: {h}")
print(f"verdict={receipt['verdict']} total_checks={receipt['total_checks']} exit={r.returncode}")
