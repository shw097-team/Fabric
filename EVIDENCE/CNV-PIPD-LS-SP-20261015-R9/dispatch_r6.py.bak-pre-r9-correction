"""Dispatch one HG-KSEOS lane turn for mission CNV-PIPD-LS-SP-20261015 (R6).

Wraps scripts/hgk-lane-dispatch.py with the round's pinned flags (argv-safe: no shell quoting).
Usage: python dispatch_r6.py <EXECUTE|VERIFY_SECURITY> <brief-path> <attempt> [timeout_s]
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PY = "C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe"
ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
DISP = ROOT + "/scripts/hgk-lane-dispatch.py"
HANDOVER = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
LANE_RUNS = HANDOVER + "/lane_runs"
LIVE_CODEX = "C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe"

LANE_CONF = {
    "EXECUTE": ("--force-rank", "1", "--require-arm", "opencode-go/deepseek-v4.1-flash"),
    "VERIFY_SECURITY": ("--force-rank", "2", "--require-arm", "opencode-go/glm-5.3-flash"),
}
# VERIFY_SECURITY defaults to a read-only sandbox, which cannot persist a file-backed verdict or
# reproduce probes that write; escalation is explicit, recorded by the dispatcher receipt, and paired
# with the frozen-copy guard subject below.
LANE_EXTRA = {
    "EXECUTE": [],
    "VERIFY_SECURITY": ["--sandbox", "danger-full-access", "--allow-sandbox-escalation"],
}

GUARDS = {
    "EXECUTE": [
        HANDOVER + "/C0_C9_CONTRACT_R5.json",
        HANDOVER + "/compiler_native_output_R5/thin-prompt.md",
        HANDOVER + "/OWNER_TRUST_LOCK.json",
    ],
    # the checker must not be able to change the writer's candidate set
    "VERIFY_SECURITY": [HANDOVER + "/R6_DELIVERY"],
}


def main() -> int:
    lane = sys.argv[1]
    brief_path = Path(sys.argv[2])
    attempt = sys.argv[3] if len(sys.argv) > 3 else "1"
    timeout_s = sys.argv[4] if len(sys.argv) > 4 else "2700"
    brief = brief_path.read_text(encoding="utf-8")
    round_name = "CNV-PIPD-LS-SP-20261015-R6"
    Path(LANE_RUNS).mkdir(parents=True, exist_ok=True)
    cmd = [PY, DISP, "--lane", lane, "--prompt", brief, "--brief", str(brief_path),
           *LANE_CONF[lane], *LANE_EXTRA[lane],
           "--max-candidates", "1",
           "--round", round_name, "--attempt", attempt,
           "--output-root", LANE_RUNS,
           "--json-out", f"{LANE_RUNS}/{lane}_dispatch_receipt_attempt{attempt}.json",
           "--attempt-log-dir", f"{LANE_RUNS}/{lane}_logs_attempt{attempt}",
           "--cwd", HANDOVER,
           "--codex-executable", LIVE_CODEX,
           "--timeout", timeout_s,
           "--no-authorization-claim"]
    for g in GUARDS[lane]:
        cmd += ["--guard-subject", g]
    print("DISPATCH_CMD=" + json.dumps(cmd[:8], ensure_ascii=False), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=int(timeout_s) + 300)
    print("=== DISPATCHER STDOUT (tail) ===")
    print(r.stdout[-6000:])
    print("=== DISPATCHER STDERR (tail) ===")
    print(r.stderr[-3000:])
    print(f"=== DISPATCHER EXIT {r.returncode} ===")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
