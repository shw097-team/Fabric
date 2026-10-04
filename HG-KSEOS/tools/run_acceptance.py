from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable


EXPECTED_BASELINE_SHA256 = "1564bbf7a8cd4baeabc1704586dc50ebe1e30dd6c1d09c84a7ad629a2b8d8176"
EXPECTED_TST_037_NRTV_SHA256 = "dbdecaf42bb318fef5d79dc1396b2cf96c4fec9fd7eae8d97bc14b50a67c7eaa"
FIXTURE_FIELDS = {
    "schema",
    "case_id",
    "type",
    "fixture",
    "preconditions",
    "oracle",
    "expected",
    "reject_code",
    "source_locator",
    "frozen_baseline_sha256",
}
BASELINE_BOUND_FIELDS = (
    "case_id",
    "type",
    "fixture",
    "preconditions",
    "oracle",
    "expected",
    "reject_code",
    "source_locator",
)


class CaseFailure(RuntimeError):
    """The case ran and its deterministic contract failed."""


@dataclass(frozen=True)
class CaseResult:
    passed: bool
    details: dict[str, object]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CaseFailure(f"ERR_JSON_OBJECT_REQUIRED:{path.name}")
    return value


def _normal_relative_path(value: str) -> PurePosixPath:
    if not value or "\\" in value:
        raise CaseFailure("ERR_NON_CANONICAL_RELATIVE_PATH")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise CaseFailure("ERR_UNSAFE_RELATIVE_PATH")
    if str(path) != value:
        raise CaseFailure("ERR_NON_CANONICAL_RELATIVE_PATH")
    return path


def _resolve_repo_file(root: Path, relative: PurePosixPath) -> Path:
    candidate = root.joinpath(*relative.parts)
    if not candidate.is_file():
        raise CaseFailure(f"ERR_REQUIRED_ARTIFACT_MISSING:{relative}")
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise CaseFailure(f"ERR_ARTIFACT_OUTSIDE_ROOT:{relative}") from exc
    current = candidate
    while current != root:
        if current.is_symlink() or (
            getattr(current.stat(), "st_file_attributes", 0) & 0x400
        ):
            raise CaseFailure(f"ERR_REPARSE_ARTIFACT:{relative}")
        current = current.parent
    return resolved


def validate_frozen_fixture(
    row: dict[str, str], fixture_path: Path, baseline_hash: str
) -> tuple[dict[str, object], str]:
    try:
        fixture_bytes = fixture_path.read_bytes()
        fixture = json.loads(fixture_bytes.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CaseFailure("ERR_FIXTURE_UNREADABLE") from exc
    if not isinstance(fixture, dict):
        raise CaseFailure("ERR_FIXTURE_OBJECT_REQUIRED")
    if set(fixture) != FIXTURE_FIELDS:
        raise CaseFailure("ERR_FIXTURE_SCHEMA_EXACT_SET")
    if fixture["schema"] != "HGK-ACCEPTANCE-FIXTURE/1":
        raise CaseFailure("ERR_FIXTURE_SCHEMA")
    if fixture["frozen_baseline_sha256"] != baseline_hash:
        raise CaseFailure("ERR_FIXTURE_BASELINE_BINDING")
    mismatches = [field for field in BASELINE_BOUND_FIELDS if fixture[field] != row[field]]
    if mismatches:
        raise CaseFailure("ERR_FIXTURE_BASELINE_FIELDS:" + ",".join(mismatches))
    return fixture, sha256_bytes(fixture_bytes)


def verify_common_preconditions(root: Path, fixture: dict[str, object]) -> dict[str, object]:
    if fixture["preconditions"] != "authority/source/version/permission frozen":
        raise CaseFailure("ERR_UNSUPPORTED_PRECONDITION_CONTRACT")
    receipt_path = root / "source-freeze" / "SOURCE_FREEZE_RECEIPT.json"
    project_path = root / "config" / "project.json"
    if not receipt_path.is_file() or not project_path.is_file():
        raise CaseFailure("ERR_PRECONDITION_EVIDENCE_MISSING")
    receipt = _load_json(receipt_path)
    project = _load_json(project_path)
    status = str(receipt.get("status", ""))
    if not status.startswith("FROZEN_"):
        raise CaseFailure("ERR_SOURCE_NOT_FROZEN")
    exact_root = str(root)
    bound_fields = {
        "freeze_execution_root": receipt.get("execution_root"),
        "project_source_root": project.get("source_root"),
        "project_maker_root": project.get("maker_root"),
    }
    if any(str(value).casefold() != exact_root.casefold() for value in bound_fields.values()):
        raise CaseFailure("ERR_CANONICAL_ROOT_BINDING")
    return {
        "contract": fixture["preconditions"],
        "source_freeze_status": status,
        "source_freeze_receipt_sha256": sha256_bytes(receipt_path.read_bytes()),
        "project_binding_sha256": sha256_bytes(project_path.read_bytes()),
        "canonical_root": exact_root,
    }


def _json_pointer(document: dict[str, object], pointer: str) -> object:
    if not pointer.startswith("/") or pointer == "/":
        raise CaseFailure("ERR_NRTV_JSON_POINTER")
    value: object = document
    for encoded in pointer[1:].split("/"):
        token = encoded.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise CaseFailure(f"ERR_NRTV_LOCATOR_UNRESOLVED:{pointer}")
        value = value[token]
    return value


def execute_tst_037(
    root: Path,
    fixture: dict[str, object],
    *,
    expected_nrtv_hash: str = EXPECTED_TST_037_NRTV_SHA256,
) -> CaseResult:
    nrtv_path = root / "eval" / "nrtv" / "TST-037.json"
    nrtv_bytes = nrtv_path.read_bytes()
    nrtv_hash = sha256_bytes(nrtv_bytes)
    if nrtv_hash != expected_nrtv_hash:
        raise CaseFailure(f"ERR_NRTV_FIXTURE_DRIFT:{nrtv_hash}")
    nrtv = json.loads(nrtv_bytes.decode("utf-8"))
    if not isinstance(nrtv, dict) or nrtv.get("schema") != "HGK-BLIND-NRTV/1":
        raise CaseFailure("ERR_NRTV_SCHEMA")
    if nrtv.get("case_id") != "TST-037":
        raise CaseFailure("ERR_NRTV_CASE_BINDING")
    if not isinstance(nrtv.get("query"), str) or not nrtv["query"].strip():
        raise CaseFailure("ERR_NRTV_QUERY")
    expected = nrtv.get("expected_answer")
    allowed_values = nrtv.get("allowed_compiled_artifacts")
    required_locators = nrtv.get("required_locators")
    forbidden_values = nrtv.get("forbidden_inputs")
    if not isinstance(expected, dict) or not expected:
        raise CaseFailure("ERR_NRTV_EXPECTED_ANSWER")
    if not isinstance(allowed_values, list) or not allowed_values:
        raise CaseFailure("ERR_NRTV_ALLOWED_ARTIFACTS")
    if not isinstance(required_locators, list) or not required_locators:
        raise CaseFailure("ERR_NRTV_REQUIRED_LOCATORS")
    if not isinstance(forbidden_values, list) or not forbidden_values:
        raise CaseFailure("ERR_NRTV_FORBIDDEN_INPUTS")
    declared_paths = allowed_values + required_locators + forbidden_values
    if not all(isinstance(value, str) for value in declared_paths):
        raise CaseFailure("ERR_NRTV_STRING_LIST_REQUIRED")

    allowed = {_normal_relative_path(value) for value in allowed_values}
    if len(allowed) != len(allowed_values):
        raise CaseFailure("ERR_NRTV_DUPLICATE_ALLOWED_ARTIFACT")
    if not all(Path(value).is_absolute() for value in forbidden_values):
        raise CaseFailure("ERR_NRTV_FORBIDDEN_INPUT_NOT_ABSOLUTE")
    forbidden = [Path(value).resolve(strict=False) for value in forbidden_values]
    if len({os.path.normcase(str(path)) for path in forbidden}) != len(forbidden):
        raise CaseFailure("ERR_NRTV_DUPLICATE_FORBIDDEN_INPUT")

    resolved_allowed = {artifact: _resolve_repo_file(root, artifact) for artifact in allowed}
    locator_map: dict[str, tuple[PurePosixPath, str]] = {}
    for locator in required_locators:
        if "#" not in locator:
            raise CaseFailure("ERR_NRTV_LOCATOR_FORMAT")
        artifact_text, pointer = locator.split("#", 1)
        artifact = _normal_relative_path(artifact_text)
        if artifact not in allowed:
            raise CaseFailure(f"ERR_NRTV_LOCATOR_ARTIFACT_NOT_ALLOWED:{artifact}")
        if pointer in locator_map:
            raise CaseFailure(f"ERR_NRTV_DUPLICATE_LOCATOR:{pointer}")
        locator_map[pointer] = (artifact, locator)
    expected_pointers = {f"/{name}" for name in expected}
    if set(locator_map) != expected_pointers:
        raise CaseFailure("ERR_NRTV_LOCATOR_EXACT_SET")

    documents: dict[PurePosixPath, dict[str, object]] = {}
    access_log: list[dict[str, object]] = []
    answer: dict[str, object] = {}
    for name in expected:
        artifact, locator = locator_map[f"/{name}"]
        if artifact not in documents:
            artifact_path = resolved_allowed[artifact]
            # A broad forbidden root may contain an explicitly allowlisted compiled artifact.
            # The explicit allowlist is the sole exception; no other path is ever opened here.
            covered_by_forbidden = any(
                artifact_path == path or path in artifact_path.parents for path in forbidden
            )
            artifact_bytes = artifact_path.read_bytes()
            document = json.loads(artifact_bytes.decode("utf-8"))
            if not isinstance(document, dict):
                raise CaseFailure(f"ERR_NRTV_ARTIFACT_OBJECT_REQUIRED:{artifact}")
            documents[artifact] = document
            access_log.append(
                {
                    "path": str(artifact),
                    "sha256": sha256_bytes(artifact_bytes),
                    "explicitly_allowlisted": True,
                    "inside_declared_forbidden_root": covered_by_forbidden,
                }
            )
        value = _json_pointer(documents[artifact], f"/{name}")
        if value != expected[name]:
            raise CaseFailure(f"ERR_NRTV_ORACLE_VALUE:{name}")
        answer[name] = value
        if locator != f"{artifact}#/{name}":
            raise CaseFailure(f"ERR_NRTV_LOCATOR_CANONICAL:{name}")

    required_counts = {"predev_requirements", "p0_requirements", "requirement_trace_rows"}
    if set(answer) != required_counts:
        raise CaseFailure("ERR_NRTV_ANSWER_EXACT_SET")
    compiled_total = answer["predev_requirements"] + answer["p0_requirements"]
    if compiled_total != answer["requirement_trace_rows"]:
        raise CaseFailure("ERR_NRTV_TRACE_ARITHMETIC")
    if fixture["oracle"] != "Answer from compiled artifacts with correct locator":
        raise CaseFailure("ERR_NRTV_BASELINE_ORACLE")

    return CaseResult(
        passed=True,
        details={
            "query": nrtv["query"],
            "answer": answer,
            "required_locators": required_locators,
            "locator_exact_set_validated": True,
            "allowed_compiled_artifacts": sorted(str(path) for path in allowed),
            "forbidden_inputs": forbidden_values,
            "artifact_access_log": access_log,
            "raw_source_volumes_read_by_case_executor": False,
            "nrtv_fixture_sha256": nrtv_hash,
        },
    )


CASE_EXECUTORS: dict[str, Callable[[Path, dict[str, object]], CaseResult]] = {}


def _load_case_executors() -> None:
    """Load deterministic case executors exactly once; depth executors override
    symbol-presence executors for L4/L5-required cases (D1 calibration)."""
    if CASE_EXECUTORS:
        return
    import importlib.util

    base_module_path = Path(__file__).resolve().parent / "case_executors.py"
    for module_path, module_name in (
        (base_module_path, "case_executors"),
        (Path(__file__).resolve().parent / "case_executors_depth.py", "case_executors_depth"),
    ):
        if not module_path.is_file():
            continue
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name, executor in module.CASE_EXECUTORS.items():
            if isinstance(executor, Callable):
                CASE_EXECUTORS[name] = executor


_load_case_executors()


EXPLICIT_BLOCKERS = {
    "TST-054": (
        "TT-HERMES-UNINSTALL",
        "A case-specific disposable uninstall/rollback execution receipt is required.",
    ),
    "TST-092": (
        "TT-FINAL-PACKAGE-READBACK",
        "A sealed exact-set package readback for the final tested HEAD is required.",
    ),
}


def _run_case(
    row: dict[str, str], root: Path, baseline_hash: str
) -> tuple[str, dict[str, object], str]:
    case_id = row["case_id"]
    fixture_path = root / "eval" / "fixtures" / f"{case_id}.yaml"
    fixture, fixture_hash = validate_frozen_fixture(row, fixture_path, baseline_hash)
    preconditions = verify_common_preconditions(root, fixture)
    executor = CASE_EXECUTORS.get(case_id)
    if executor is None:
        tt_id, reason = EXPLICIT_BLOCKERS.get(
            case_id,
            (
                f"TT-ACCEPTANCE-{case_id}",
                (
                    "No dedicated case executor currently applies this case fixture "
                    "and evaluates its oracle."
                ),
            ),
        )
        return (
            "BLOCKED",
            {
                "tt_id": tt_id,
                "reason": reason,
                "preconditions": preconditions,
                "required_close_criteria": (
                    "Add a dedicated executor that consumes this fixture, exercises the "
                    "stated procedure, and evaluates this exact oracle without shared-test "
                    "substitution."
                ),
            },
            fixture_hash,
        )
    try:
        result = executor(root, fixture)
    except Exception as exc:  # normalize any executor exception to the runner's CaseFailure
        if isinstance(exc, CaseFailure):
            raise
        raise CaseFailure(f"ERR_EXECUTOR_RAISED:{type(exc).__name__}:{exc}") from exc
    if not result.passed:
        raise CaseFailure("ERR_CASE_ORACLE_FALSE")
    return (
        "MAKER_CASE_PASS",
        {"preconditions": preconditions, "oracle_execution": result.details},
        fixture_hash,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--case-id", action="append", dest="case_ids")
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    baseline = root / "eval" / "FROZEN_ACCEPTANCE_CASES.csv"
    baseline_bytes = baseline.read_bytes()
    baseline_hash = sha256_bytes(baseline_bytes)
    runner_hash = sha256_bytes(Path(__file__).read_bytes())
    if baseline_hash != EXPECTED_BASELINE_SHA256:
        raise SystemExit(f"acceptance baseline drift: {baseline_hash}")
    with baseline.open(encoding="utf-8-sig", newline="") as handle:
        cases = list(csv.DictReader(handle))
    expected_ids = {f"TST-{number:03d}" for number in range(1, 93)}
    if len(cases) != 92 or {row["case_id"] for row in cases} != expected_ids:
        raise SystemExit("acceptance denominator/exact-set mismatch")
    selected = set(args.case_ids or expected_ids)
    if not selected or not selected <= expected_ids:
        raise SystemExit("unknown or empty --case-id selection")

    output_root = root / "evidence" / "wave-15"
    case_root = output_root / "cases"
    case_root.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, object]] = []
    for row in cases:
        case_id = row["case_id"]
        if case_id not in selected:
            continue
        try:
            status, details, fixture_hash = _run_case(row, root, baseline_hash)
        except CaseFailure as exc:
            status = "FAIL"
            details = {"reason": str(exc)}
            fixture_path = root / "eval" / "fixtures" / f"{case_id}.yaml"
            fixture_hash = (
                sha256_bytes(fixture_path.read_bytes()) if fixture_path.is_file() else "MISSING"
            )
        evidence = {
            "schema": "HGK-CASE-EVIDENCE/2",
            "case_id": case_id,
            "domain": row["domain"],
            "type": row["type"],
            "status": status,
            "fixture_text": row["fixture"],
            "preconditions_contract": row["preconditions"],
            "oracle": row["oracle"],
            "expected": row["expected"],
            "reject_code": row["reject_code"],
            "source_locator": row["source_locator"],
            "fixture": f"eval/fixtures/{case_id}.yaml",
            "fixture_sha256": fixture_hash,
            "frozen_baseline_sha256": baseline_hash,
            "runner_sha256": runner_hash,
            "details": details,
            "maker": "CODEX_MAIN_MAKER",
            "independent_verifier": row["independent_verifier"],
            "independent_verdict": "NOT_RUN",
            "claim_ceiling": "Maker case execution only; independent acceptance is not inferred.",
        }
        evidence_path = case_root / f"{case_id}.json"
        evidence_bytes = (json.dumps(evidence, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        evidence_path.write_bytes(evidence_bytes)
        results.append(
            {
                "case_id": case_id,
                "domain": row["domain"],
                "type": row["type"],
                "status": status,
                "evidence": f"evidence/wave-15/cases/{case_id}.json",
                "evidence_sha256": sha256_bytes(evidence_bytes),
                "independent_verdict": "NOT_RUN",
            }
        )

    statuses = ("MAKER_CASE_PASS", "BLOCKED", "FAIL")
    counts = {name: sum(1 for row in results if row["status"] == name) for name in statuses}
    complete_run = selected == expected_ids
    report = {
        "schema": "HGK-MAKER-ACCEPTANCE-REPORT/2",
        "baseline_sha256": baseline_hash,
        "runner_sha256": runner_hash,
        "frozen_denominator": 92,
        "attempted": len(results),
        "complete_run": complete_run,
        "counts": counts,
        "exact_selected_set": len(results) == len(selected),
        "case_specific_executor_ids": sorted(CASE_EXECUTORS),
        "independent_acceptance": "NOT_RUN",
        "verdict": (
            "FAIL"
            if counts["FAIL"]
            else ("BLOCKED" if counts["BLOCKED"] else "MAKER_PASS_ONLY")
        ),
        "claim_ceiling": (
            "Only a dedicated fixture-consuming, oracle-evaluating executor may produce "
            "MAKER_CASE_PASS. Missing dedicated execution is BLOCKED and the process exits "
            "non-zero."
        ),
    }
    report_path = output_root / "MAKER_ACCEPTANCE_REPORT.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (output_root / "CASE_RESULTS.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(json.dumps(report, ensure_ascii=False))
    if counts["FAIL"]:
        return 1
    if counts["BLOCKED"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
