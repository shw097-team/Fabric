"""Emit R7_WRITER_RECEIPT.json — what was run, exit codes, exact commands, honest gaps."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

R7 = Path(__file__).resolve().parent.parent
RAW = R7 / "RAW"
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


commands = [
    {"purpose": "hash-rule probe (pre-change, confirms content_hash == body hash)",
     "command": f"{PY} RAW/probe_hashcheck.py",
     "raw": "RAW/probe_hashcheck.stdout.txt"},
    {"purpose": "direct probe: three blind spots + positives + fail-closed",
     "command": f"{PY} RAW/probe_r7_validator.py",
     "raw": "RAW/probe_r7_validator.stdout.txt"},
    {"purpose": "strong attacker probe (re-issued identity; frozen-reference layer)",
     "command": f"{PY} RAW/probe_r7_strong.py",
     "raw": "RAW/probe_r7_strong.stdout.txt"},
    {"purpose": "targeted regression tests (positive slices + typed errors)",
     "command": (f"{PY} -m pytest tests/test_s1_lite_slice.py tests/test_negative_and_rollback.py "
                 "tests/test_technology_admission.py tests/test_tqaep_design_positive.py "
                 "tests/test_cli_typed_errors.py -q"),
     "raw": "RAW/r7_pytest_targeted.stdout.txt"},
    {"purpose": "full test suite (regression sweep)",
     "command": f"{PY} -m pytest tests -q",
     "raw": "RAW/r7_pytest_full.stdout.txt"},
    {"purpose": "R7 re-run of the existing MUTATIONS_18 driver (RAW redirected to R7/RAW)",
     "command": f"{PY} run_r7_mutations.py",
     "raw": "RAW/r7_run_mutations.stdout.txt"},
    {"purpose": "checker write-root isolation proof (denial fixture + copy-based review)",
     "command": f"{PY} run_r7_isolation.py",
     "raw": "RAW/r7_isolation.stdout.txt"},
    {"purpose": "unified diff generation (git diff --no-index)",
     "command": f"{PY} RAW/_make_diff.py",
     "raw": "RAW/r7_make_diff.stdout.txt"},
]

pytest_targeted = (RAW / "r7_pytest_targeted.stdout.txt")
pytest_full = (RAW / "r7_pytest_full.stdout.txt")

receipt = {
    "schema": "CNV-PIPD-LS-SP-20261015-R7/WRITER-RECEIPT/1",
    "changeset": "R7-0-VALIDATOR-AND-CHECKER-ISOLATION",
    "produced_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"),
    "lane": "EXECUTE",
    "host": {"shell": "PowerShell", "python": PY, "elevated": False},
    "model_provider_actually_served": {
        "lane_brief_declared": "Codex CLI, provider/model opencode-go/deepseek-v4.1-flash",
        "self_identification": "deepseek-v4.1-flash",
        "note": ("Declared by the lane brief and the R7 admission record; the serving host routes "
                 "the model. This writer does not independently observe the upstream provider "
                 "attestation, so the value is reported, not re-proved, here."),
    },
    "claim_ceiling": "LOCAL / candidate-only",
    "commands_run": commands,
    "exit_codes": {
        "probe_hashcheck": 0,
        "probe_r7_validator": 0,
        "probe_r7_strong": 0,
        "pytest_targeted": "0 (44 passed, 3 subtests passed)",
        "pytest_full": "1 (7 failed, 319 passed, 2 skipped, 34 subtests passed)",
        "run_r7_mutations": 0,
        "run_r7_isolation": 0,
        "make_diff": 0,
        "pytest_targeted_sha256": sha(pytest_targeted) if pytest_targeted.exists() else None,
        "pytest_full_sha256": sha(pytest_full) if pytest_full.exists() else None,
    },
    "results": {
        "mutations_executed": 10,
        "mutations_detected_reject": 10,
        "mutations_not_run": 8,
        "flipped_to_reject": ["M04", "M06", "M16"],
        "previously_detected_still_reject": ["M01", "M03", "M05", "M11", "M12", "M14", "M18"],
        "isolation_denial_fixture": "ENFORCED / DENIED (append + new-file refused, read preserved)",
        "isolation_copy_based_review": "ENFORCED / DENIED (write into review copy refused, scratch writable)",
    },
    "pytest_full_failures_assessment": {
        "ids": ["tests/test_publication_projection.py::CliSmoke::test_write_then_check_exits_zero",
                "tests/test_publication_projection.py::CurrentTreeCoverage::test_attestation_build_then_verify_exits_zero",
                "tests/test_publication_projection.py::CurrentTreeCoverage::test_check_always_prints_current_tree_coverage",
                "tests/test_publication_projection.py::CurrentTreeCoverage::test_current_check_fails_while_any_current_product_path_is_uncovered",
                "tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs",
                "tests/test_tooling_executes.py::TestToolingExecutes::test_export_manifest_has_no_vcs_paths",
                "tests/test_tooling_executes.py::TestToolingExecutes::test_tracked_file_metric_excludes_vcs_internals"],
        "cause": ("pre-existing and environmental: shutil.copytree over the dirty tree hits Windows "
                  "venv junction/symlink entries ([Errno 22]/[WinError 1920]) before any PIPD code "
                  "runs, plus dirty-tree tracked-file counts"),
        "proof": ("the SAME 7 failures reproduce with the pre-change sources restored from "
                  "RAW/pre_change; RAW/r7_pytest_full.stdout.txt (hardened) == those failures"),
        "impact_on_this_changeset": "none — none of the 7 imports the changed validation path",
    },
    "not_done_or_limited": [
        "Could not observe the upstream provider attestation for the served model; the declared "
        "provider/model is reported from the brief/admission, not re-proved.",
        "The 8 NOT_RUN mutations (M02, M07..M10, M13, M15, M17) remain NOT_RUN: their frozen source "
        "bytes are not reachable on this host. Not fabricated.",
        "The full test suite has 7 pre-existing environmental failures (see above); the targeted "
        "validation/positive tests are green.",
        "OS test of ACL enforcement was performed on this (non-elevated) account only; a different "
        "account/host could yield ACL_UNENFORCEABLE, in which case the wrapper records it verbatim.",
        "No git write was issued; R6_DELIVERY/RAW and RUNNERS/mutation_records.json were left "
        "untouched (the R7 rerun redirects captures to R7/RAW).",
    ],
}
(R7 / "R7_WRITER_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1),
                                           encoding="utf-8")
print("wrote R7_WRITER_RECEIPT.json")
