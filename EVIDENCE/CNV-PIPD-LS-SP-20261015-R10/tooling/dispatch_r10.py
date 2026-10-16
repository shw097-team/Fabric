"""Dispatch one HG-KSEOS lane turn for mission CNV-PIPD-LS-SP-20261015 (R10) - successor to dispatch_r9.py.

TWO MEASURED DEFECTS REPAIRED HERE (see R10/tooling/README_R10_TOOLING.md for the evidence):

1. PER-ROLE RECEIPT COLLISION. dispatch_r9.py named the receipt
   `<lane>_dispatch_receipt_attempt<attempt>.json`; a round dispatches every turn with attempt=1, so a SECOND
   turn of the same lane overwrote the first turn's receipt. MEASURED: after the R9 EXECUTE turns, the single
   file EXECUTE_dispatch_receipt_attempt1.json held the LATER turn's content and the earlier turn's provenance
   survived only because it had been snapshotted by hand. Repair: receipt and attempt-log paths carry a TURN
   label plus a UTC stamp, and both files are SNAPSHOTTED into the round root the moment the turn returns.

2. NONCE PRESENT BUT REPORTED ABSENT. The dispatcher scans only the transcript's
   `item.completed/agent_message` events (`nonce_source` in its receipt). MEASURED: for the R9 VERIFY turn the
   receipt said `code: ERR_NO_ARM_EMITTED_NONCE`, `nonce_present: false`, `used_rank/served_arm: null` while the
   SAME receipt's own recorded `stdout_tail` ended with the nonce the brief had asked for, and its recorded
   `stdout_path` (429,783 bytes) contained it as well. Repair: this wrapper derives the expected nonce from the
   BRIEF it is about to dispatch, and after the turn it ADDITIONALLY reads the surfaces the dispatcher already
   recorded (each attempt's stdout/stderr path) plus any caller-declared artifact root. The dispatcher's own
   receipt is never rewritten - the finding goes into a SIBLING attestation record, and the served arm is read
   from `attempts[]` because the dispatcher's `used_*` fields stay null on that code path.

Usage:
  python dispatch_r10.py <EXECUTE|VERIFY_SECURITY> <brief-path> [turn] [timeout_s] [--artifacts <dir>] [--round-root <dir>]

argv-safety: the lane flags are a list, never a shell string; no credential is read or printed.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PY = "C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe"
ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
DISP = ROOT + "/scripts/hgk-lane-dispatch.py"
HANDOVER = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
LANE_RUNS = HANDOVER + "/lane_runs"
LIVE_CODEX = "C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe"
ROUND_NAME = "CNV-PIPD-LS-SP-20261015-R10"
DEFAULT_ROUND_ROOT = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10"

# The R10-0 mandate (2026-10-16, later turn) names: EXECUTE = opencode-go/deepseek-v4.1-flash and
# VERIFY_SECURITY = opencode-go/deepseek-v4.1-flash. NOTE THE RESIDUAL this creates: writer and checker are
# the SAME ARM, so model-axis independence between maker and checker is ABSENT (process/lane separation only).
LANE_CONF = {
    "EXECUTE": ("--force-rank", "1", "--require-arm", "opencode-go/deepseek-v4.1-flash"),
    "VERIFY_SECURITY": ("--force-rank", "1", "--require-arm", "opencode-go/deepseek-v4.1-flash"),
}
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
    "VERIFY_SECURITY": [HANDOVER + "/R6_DELIVERY"],
}

# a round nonce looks like <ROUND>-<ROLE>-NONCE-<hex>; keep the pattern permissive about the dashes and
# require a plausible length so the bare word NONCE in prose is never mistaken for a token.
NONCE_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*NONCE[A-Za-z0-9-]*")


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def receipt_paths(lane: str, turn: str, stamp: str, lane_runs: str = LANE_RUNS) -> dict:
    """IMMUTABLE per-turn paths (defect 1). Two turns of one lane can never collide."""
    base = lane_runs.rstrip("/") + "/" + lane + "_turn" + str(turn) + "_" + stamp
    return {"receipt": base + "_dispatch_receipt.json",
            "attempt_log_dir": base + "_logs",
            "attestation": base + "_nonce_attestation.json"}


def extract_expected_nonce(brief_text: str) -> str | None:
    """The round's brief states the nonce it will ask the lane to echo; that is the expected value."""
    hits = NONCE_RE.findall(brief_text or "")
    if not hits:
        return None
    return max(hits, key=len)


def sha256_file(p: str) -> str | None:
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def _search(paths, needle: str, limit_bytes: int = 8_000_000):
    """Return the paths whose bytes contain needle, with their digests."""
    found = []
    for p in paths:
        try:
            b = Path(p).read_bytes()[:limit_bytes]
        except OSError:
            continue
        if needle.encode("utf-8") in b:
            found.append({"path": p, "bytes": len(b), "sha256": sha256_file(p)})
    return found


def attest(receipt: dict, brief_text: str, artifact_roots=None, lane_runs: str = LANE_RUNS) -> dict:
    """Build the sibling attestation for a receipt that reports the nonce absent.

    Reads ONLY surfaces the dispatcher itself already recorded (attempts[].stdout_path / stderr_path)
    plus caller-declared artifact roots. Never mutates the receipt.
    """
    artifact_roots = [r for r in (artifact_roots or []) if r]
    expected = extract_expected_nonce(brief_text or "")
    attempts = receipt.get("attempts") or []
    surfaces, arms = [], []
    for a in attempts:
        arms.append({"rank": a.get("rank"), "provider": a.get("provider"), "model": a.get("model"),
                     "exit": a.get("exit"), "seconds": a.get("seconds"),
                     "nonce_present_as_reported": a.get("nonce_present"),
                     "nonce_source_as_reported": a.get("nonce_source"),
                     "timed_out": a.get("timed_out"), "stdout_bytes": a.get("stdout_bytes")})
        for key in ("stdout_path", "stderr_path"):
            if a.get(key):
                surfaces.append(a[key])
    # caller-declared artifact roots: every regular file under them, bounded
    extra = []
    for r in artifact_roots:
        rp = Path(r)
        if rp.is_dir():
            extra += [str(p) for p in sorted(rp.rglob("*")) if p.is_file()]
        elif rp.is_file():
            extra.append(str(rp))
    out = {
        "schema": "HGK-LANE-NONCE-ATTESTATION/1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "lane": receipt.get("lane"),
        "dispatcher_code": receipt.get("code"),
        "dispatcher_claim": {"code": receipt.get("code"),
                             "used_rank": receipt.get("used_rank"),
                             "used_transport_model": receipt.get("used_transport_model"),
                             "nonce_absent_arms": receipt.get("nonce_absent_arms")},
        "expected_nonce_derived_from": "the dispatched brief text",
        "expected_nonce_present_in_brief": bool(expected),
        "expected_nonce_sha256_prefix": hashlib.sha256(expected.encode()).hexdigest()[:16] if expected else None,
        "arms_from_attempts": arms,
        "surfaces_scanned_from_receipt": surfaces,
        "artifact_roots_declared": artifact_roots,
        "artifact_root_files": len(extra),
        "nonce_found_in": [],
        "verdict": "NOT_EVALUATED",
        "claim_ceiling": ("an attestation here corrects the RECORD of whether the lane emitted the nonce; it is "
                          "not an acceptance, not a model attestation by the provider, and it does not upgrade "
                          "any round claim"),
    }
    if not expected:
        out["verdict"] = "NO_EXPECTED_NONCE_IN_BRIEF"
        return out
    found = _search(surfaces + extra, expected)
    out["nonce_found_in"] = found
    if found:
        out["verdict"] = "NONCE_PRESENT_DESPITE_DISPATCHER_CODE"
    elif not attempts:
        out["verdict"] = "NO_ATTEMPTS_RECORDED"
    else:
        out["verdict"] = "NONCE_NOT_FOUND_IN_ANY_RECORDED_SURFACE"
    return out


def snapshot(receipt_path: str, attempt_log_dir: str, round_root: str, lane: str, turn: str, stamp: str) -> dict:
    """Copy the receipt and its attempt log into the round root (defect 1)."""
    dest_dir = Path(round_root) / "lane_receipts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    srcs = [receipt_path]
    ald = Path(attempt_log_dir) if attempt_log_dir else None
    if ald and ald.is_dir():
        srcs += [str(p) for p in sorted(ald.glob("*.ndjson"))]
        srcs += [str(p) for p in sorted(ald.glob("*.json"))]
    for s in srcs:
        sp = Path(s)
        if not sp.is_file():
            continue
        dp = dest_dir / (lane + "_turn" + str(turn) + "_" + stamp + "_" + sp.name)
        dp.write_bytes(sp.read_bytes())
        copied.append({"from": s, "to": str(dp), "bytes": dp.stat().st_size, "sha256": sha256_file(str(dp))})
    return {"snapshot_dir": str(dest_dir), "copied": copied}


def main() -> int:
    args = [a for a in sys.argv[1:]]
    artifacts, round_root = [], DEFAULT_ROUND_ROOT
    if "--artifacts" in args:
        i = args.index("--artifacts")
        artifacts = [args[i + 1]]
        del args[i:i + 2]
    if "--round-root" in args:
        i = args.index("--round-root")
        round_root = args[i + 1]
        del args[i:i + 2]
    lane = args[0]
    brief_path = Path(args[1])
    turn = args[2] if len(args) > 2 else "1"
    timeout_s = args[3] if len(args) > 3 else "2700"
    brief = brief_path.read_text(encoding="utf-8")
    stamp = utc_stamp()
    Path(LANE_RUNS).mkdir(parents=True, exist_ok=True)
    paths = receipt_paths(lane, turn, stamp)
    cmd = [PY, DISP, "--lane", lane, "--prompt", brief, "--brief", str(brief_path),
           *LANE_CONF[lane], *LANE_EXTRA[lane], "--max-candidates", "1",
           "--round", ROUND_NAME, "--attempt", str(turn),
           "--output-root", LANE_RUNS,
           "--json-out", paths["receipt"],
           "--attempt-log-dir", paths["attempt_log_dir"],
           "--cwd", HANDOVER, "--codex-executable", LIVE_CODEX,
           "--timeout", timeout_s, "--no-authorization-claim"]
    for g in GUARDS[lane]:
        cmd += ["--guard-subject", g]
    print("DISPATCH_CMD=" + json.dumps(cmd[:8], ensure_ascii=False), flush=True)
    print("RECEIPT_PATH=" + paths["receipt"], flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=int(timeout_s) + 300)
    print("=== DISPATCHER STDOUT (tail) ===")
    print(r.stdout[-6000:])
    print("=== DISPATCHER STDERR (tail) ===")
    print(r.stderr[-3000:])
    print(f"=== DISPATCHER EXIT {r.returncode} ===")

    # post-turn: snapshot provenance, then attest the nonce against surfaces the dispatcher recorded
    if Path(paths["receipt"]).is_file():
        receipt = json.loads(Path(paths["receipt"]).read_text(encoding="utf-8"))
        snap = snapshot(paths["receipt"], paths["attempt_log_dir"], round_root, lane, turn, stamp)
        att = attest(receipt, brief, artifacts, LANE_RUNS)
        att["snapshot"] = snap
        att["receipt_path"] = paths["receipt"]
        Path(paths["attestation"]).write_text(json.dumps(att, ensure_ascii=False, indent=1), encoding="utf-8")
        copy_in = Path(round_root) / "lane_receipts" / Path(paths["attestation"]).name
        copy_in.parent.mkdir(parents=True, exist_ok=True)
        copy_in.write_text(json.dumps(att, ensure_ascii=False, indent=1), encoding="utf-8")
        print("=== NONCE ATTESTATION ===")
        print(json.dumps({"dispatcher_code": att["dispatcher_code"], "verdict": att["verdict"],
                          "nonce_found_in": [f["path"] for f in att["nonce_found_in"]],
                          "arms_from_attempts": att["arms_from_attempts"],
                          "snapshot_copied": len(snap["copied"])}, ensure_ascii=False, indent=1))
    else:
        print("=== NO RECEIPT AT THE PER-TURN PATH (a turn killed before completion leaves only the attempt log) ===")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
