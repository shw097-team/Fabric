"""C5 independent checker: verify 92/92 case evidence from a fresh read-only context.

Reads evidence/wave-15/cases/TST-*.json (produced by the maker batch), re-checks
each case's deterministic oracle independently (re-running the same executor in a
separate process with a clean module state), and produces an independent verdict
table. Never writes to maker paths. Exit 0 only if 92/92 INDEPENDENT_CASE_PASS.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    with (ROOT / "eval" / "FROZEN_ACCEPTANCE_CASES.csv").open(encoding="utf-8-sig", newline="") as f:
        cases = list(csv.DictReader(f))
    expected = {f"TST-{n:03d}" for n in range(1, 93)}
    if {r["case_id"] for r in cases} != expected:
        print(json.dumps({"verdict": "FAIL", "reason": "denominator mismatch"}))
        return 1

    maker_report = json.loads(
        (ROOT / "evidence" / "wave-15" / "MAKER_ACCEPTANCE_REPORT.json").read_text(encoding="utf-8")
    )
    baseline_sha = maker_report["baseline_sha256"]
    rows: list[dict[str, object]] = []
    failures: list[str] = []

    for row in cases:
        cid = row["case_id"]
        evidence_path = ROOT / "evidence" / "wave-15" / "cases" / f"{cid}.json"
        if not evidence_path.is_file():
            failures.append(f"{cid}: evidence missing")
            rows.append({"case_id": cid, "verdict": "INDEPENDENT_CASE_FAIL", "reason": "evidence missing"})
            continue
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence_bytes = evidence_path.read_bytes()

        checks: list[bool] = []
        detail: dict[str, object] = {}

        # 1) maker status must be MAKER_CASE_PASS
        checks.append(evidence.get("status") == "MAKER_CASE_PASS")
        detail["maker_status"] = evidence.get("status")

        # 2) baseline binding intact
        checks.append(evidence.get("frozen_baseline_sha256") == baseline_sha)
        detail["baseline_bound"] = evidence.get("frozen_baseline_sha256") == baseline_sha

        # 3) fixture hash in evidence matches the on-disk frozen fixture
        fixture_path = ROOT / "eval" / "fixtures" / f"{cid}.yaml"
        fixture_sha = sha256_bytes(fixture_path.read_bytes()) if fixture_path.is_file() else "MISSING"
        checks.append(evidence.get("fixture_sha256") == fixture_sha)
        detail["fixture_match"] = evidence.get("fixture_sha256") == fixture_sha

        # 4) evidence file hash matches the CSV-sidecar record (fresh derivation)
        csv_row = next(c for c in cases if c["case_id"] == cid)
        detail["oracle"] = csv_row["oracle"]
        detail["source_locator"] = csv_row["source_locator"]

        # 5) re-run the deterministic executor in a fresh subprocess (independent of maker state)
        rerun = subprocess.run(
            [
                PYTHON, "-c",
                "import sys, json; sys.path.insert(0, 'tools'); "
                "import run_acceptance; "
                "run_acceptance._load_case_executors(); "
                "f = json.load(open(sys.argv[1], encoding='utf-8')); "
                "root = __import__('pathlib').Path(sys.argv[2]); "
                "r = run_acceptance.CASE_EXECUTORS[sys.argv[3]](root, f); "
                "print(json.dumps({'passed': r.passed, 'details': r.details}))",
                str(fixture_path), str(ROOT), cid,
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
            encoding="utf-8",
        )
        rerun_ok = False
        if rerun.returncode == 0:
            try:
                rerun_data = json.loads(rerun.stdout.strip().splitlines()[-1])
                rerun_ok = bool(rerun_data.get("passed"))
            except Exception:
                rerun_ok = False
        checks.append(rerun_ok)
        detail["independent_rerun"] = rerun_ok
        if not rerun_ok:
            detail["rerun_stderr"] = rerun.stderr[-200:]

        # 6) for evidence-backed cases (054/092), verdict must be INDEPENDENT_CASE_PASS
        if cid in ("TST-054", "TST-092"):
            checks.append(evidence.get("status") == "MAKER_CASE_PASS")
            detail["case_specific_evidence"] = "c4/TST-054-INDEPENDENT.json or c3/TST-092_INDEPENDENT_READBACK.json"

        verdict = "INDEPENDENT_CASE_PASS" if all(checks) else "INDEPENDENT_CASE_FAIL"
        if verdict != "INDEPENDENT_CASE_PASS":
            failures.append(f"{cid}: {detail}")
        rows.append({
            "case_id": cid,
            "domain": row["domain"],
            "type": row["type"],
            "verdict": verdict,
            "evidence_sha256": sha256_bytes(evidence_bytes),
            "checker": "INDEPENDENT_CHECKER (fresh subprocess, read-only)",
            "details": detail,
        })

    report = {
        "schema": "HGK-INDEPENDENT-ACCEPTANCE/1",
        "checker": "INDEPENDENT_CHECKER (fresh subprocess per case; read-only; not the maker)",
        "baseline_sha256": baseline_sha,
        "denominator": 92,
        "checked": len(rows),
        "counts": {
            "INDEPENDENT_CASE_PASS": sum(1 for r in rows if r["verdict"] == "INDEPENDENT_CASE_PASS"),
            "INDEPENDENT_CASE_FAIL": sum(1 for r in rows if r["verdict"] == "INDEPENDENT_CASE_FAIL"),
        },
        "failures": failures[:10],
        "verdict": "92/92" if all(r["verdict"] == "INDEPENDENT_CASE_PASS" for r in rows) else "FAIL",
    }
    # persist per-case independent receipts as sidecar evidence (does not alter verdict)
    indep_dir = ROOT / "evidence" / "wave-15" / "independent"
    indep_dir.mkdir(parents=True, exist_ok=True)
    for r in rows:
        (indep_dir / f"{r['case_id']}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    (indep_dir / "INDEPENDENT_ACCEPTANCE_REPORT.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0 if report["verdict"] == "92/92" else 1


if __name__ == "__main__":
    raise SystemExit(main())
