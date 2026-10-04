#!/usr/bin/env python3
"""Deterministic structural validator for the external challenge review skill.

This script does not inspect or mutate product code. It validates review intake/report
structure and can run a local self-test for the packaged skill.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

REQUIRED_INTAKE_KEYS = {
    "review_id", "project_id", "task_id", "gate_ids", "candidate",
    "evidence_manifest_sha256", "oracle", "authority_locators",
    "raw_evidence", "claim_ceiling", "requested_review_scope",
}
REQUIRED_CANDIDATE_KEYS = {"commit", "package_sha256", "distribution_digest"}
REQUIRED_ORACLE_KEYS = {"identity", "package_digest"}
REQUIRED_REPORT_HEADINGS = [
    "## 1. Review identity",
    "## 2. Authority/source inventory",
    "## 3. Evidence inventory",
    "## 4. Challenge matrix",
    "## 5. Findings",
    "## 6. Missing / quarantined evidence",
    "## 7. Internal Oracle disagreement",
    "## 8. Gate calibration defense",
    "## 9. Verdict",
    "## 10. Claim ceiling",
    "## 11. Recommended next route",
    "## 12. External inspection list",
    "## 13. Readback",
]
ALLOWED_VERDICTS = {
    "PASS_CHALLENGE", "PARTIAL_CHALLENGE", "FAIL_CHALLENGE", "TEMP_CLOSED_CHALLENGE"
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_intake(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid_json: {exc}"]
    missing = REQUIRED_INTAKE_KEYS - set(data)
    if missing:
        errors.append(f"missing_top_keys: {sorted(missing)}")
    candidate = data.get("candidate", {})
    if not isinstance(candidate, dict):
        errors.append("candidate_not_object")
    else:
        m = REQUIRED_CANDIDATE_KEYS - set(candidate)
        if m:
            errors.append(f"missing_candidate_keys: {sorted(m)}")
    oracle = data.get("oracle", {})
    if not isinstance(oracle, dict):
        errors.append("oracle_not_object")
    else:
        m = REQUIRED_ORACLE_KEYS - set(oracle)
        if m:
            errors.append(f"missing_oracle_keys: {sorted(m)}")
    if not isinstance(data.get("gate_ids", []), list):
        errors.append("gate_ids_not_list")
    if not isinstance(data.get("authority_locators", []), list):
        errors.append("authority_locators_not_list")
    if not isinstance(data.get("raw_evidence", []), list):
        errors.append("raw_evidence_not_list")
    return errors


def validate_report(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"read_error: {exc}"]
    for heading in REQUIRED_REPORT_HEADINGS:
        if heading not in text:
            errors.append(f"missing_heading: {heading}")
    if not any(v in text for v in ALLOWED_VERDICTS):
        errors.append("missing_allowed_verdict")
    forbidden_mutation_phrases = [
        "I patched the candidate", "I merged the candidate", "I deployed the candidate"
    ]
    for phrase in forbidden_mutation_phrases:
        if phrase in text:
            errors.append(f"forbidden_mutation_claim: {phrase}")
    return errors


def self_test() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    required = [
        skill_root / "SKILL.md",
        skill_root / "agents" / "openai.yaml",
        skill_root / "references" / "evidence-intake.md",
        skill_root / "references" / "finding-contract.md",
        skill_root / "references" / "gate-calibration.md",
        skill_root / "references" / "security-permissions.md",
        skill_root / "references" / "adjudication-resume.md",
        skill_root / "references" / "rp002-profile.md",
        skill_root / "references" / "report-contract.md",
        skill_root / "assets" / "EXTERNAL_CHALLENGE_REPORT.template.md",
        skill_root / "assets" / "EXTERNAL_CHALLENGE_INTAKE.template.json",
        skill_root / "evals" / "trigger_prompts.csv",
    ]
    missing = [str(p) for p in required if not p.is_file()]
    if missing:
        print(json.dumps({"status": "FAIL", "missing": missing}, ensure_ascii=False, indent=2))
        return 1
    intake_errors = validate_intake(skill_root / "assets" / "EXTERNAL_CHALLENGE_INTAKE.template.json")
    report_text = (skill_root / "assets" / "EXTERNAL_CHALLENGE_REPORT.template.md").read_text(encoding="utf-8")
    report_errors = [h for h in REQUIRED_REPORT_HEADINGS if h not in report_text]
    result = {
        "status": "PASS" if not intake_errors and not report_errors else "FAIL",
        "skill_sha256": sha256_file(skill_root / "SKILL.md"),
        "intake_errors": intake_errors,
        "report_errors": report_errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--intake", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    errors: list[str] = []
    if args.intake:
        errors.extend(validate_intake(args.intake))
    if args.report:
        errors.extend(validate_report(args.report))
    if not args.intake and not args.report:
        ap.error("provide --self-test, --intake, or --report")
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
