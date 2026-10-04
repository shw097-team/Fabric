from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


SECRET_ENV_NAMES = {
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "OPENROUTER_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "XAI_API_KEY",
    "DEEPSEEK_API_KEY",
    "GITHUB_TOKEN",
    "GH_TOKEN",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(
    argv: list[str], home: Path, timeout: int = 150, cwd: Path | None = None
) -> dict[str, object]:
    environment = os.environ.copy()
    environment["HERMES_HOME"] = str(home)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    for name in SECRET_ENV_NAMES:
        environment.pop(name, None)
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    return {"returncode": completed.returncode, "output": output}


def junit_summary(path: Path) -> dict[str, object]:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    total = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) for suite in suites)
    errors = sum(int(suite.attrib.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
    failure_rows: list[dict[str, str]] = []
    for case in root.iter("testcase"):
        failure = case.find("failure")
        error = case.find("error")
        node = failure if failure is not None else error
        if node is not None:
            text = node.text or ""
            message = node.attrib.get("message", "")
            captured = "\n".join(
                value for value in (case.findtext("system-out"), case.findtext("system-err")) if value
            )
            diagnostic = f"{message}\n{text}\n{captured}"
            failure_rows.append(
                {
                    "classname": case.attrib.get("classname", ""),
                    "name": case.attrib.get("name", ""),
                    "message": message,
                    "windows_symlink_privilege_block": "WinError 1314" in diagnostic
                    or (
                        case.attrib.get("name", "") == "test_allows_valid_directory_include"
                        and "falling back to copytree on Windows" in diagnostic
                    ),
                }
            )
    return {
        "tests": total,
        "passed": total - failures - errors - skipped,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "all_observed_failures_are_windows_symlink_privilege_blocks": bool(failure_rows)
        and all(row["windows_symlink_privilege_block"] for row in failure_rows),
        "failure_details": failure_rows,
        "junit_sha256": sha256(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hermes", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--pytest-python", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.work_root.mkdir(parents=True, exist_ok=True)
    version = invoke([str(args.hermes), "--version"], args.work_root / "version")
    status = invoke([str(args.hermes), "status"], args.work_root / "status")
    negative = invoke(
        [
            str(args.hermes),
            "--safe-mode",
            "--provider",
            "openrouter",
            "--model",
            "openrouter/auto",
            "-z",
            "HGK local negative provider pilot",
        ],
        args.work_root / "negative",
    )
    rollback = invoke(
        [str(args.hermes), "uninstall", "--full", "--yes", "--dry-run"],
        args.work_root / "rollback",
    )
    doctor = invoke([str(args.hermes), "--safe-mode", "doctor"], args.work_root / "doctor")
    fallback_probe = invoke(
        [
            str(args.pytest_python),
            "-m",
            "pytest",
            "-q",
            "-s",
            "-p",
            "no:cacheprovider",
            "tests/cli/test_worktree_security.py::TestWorktreeIncludeSecurity::test_allows_valid_directory_include",
        ],
        args.work_root / "fallback-probe",
        cwd=args.repo,
    )
    test_summary = junit_summary(args.junit)
    fallback_observed = "falling back to copytree on Windows" in str(fallback_probe["output"])
    if fallback_observed:
        for row in test_summary["failure_details"]:
            if row["name"] == "test_allows_valid_directory_include":
                row["windows_symlink_privilege_block"] = True
        test_summary["all_observed_failures_are_windows_symlink_privilege_blocks"] = all(
            row["windows_symlink_privilege_block"] for row in test_summary["failure_details"]
        )

    report = {
        "schema": "HGK-HERMES-RUNTIME-VALIDATION/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_ceiling": "Local no-credential validation only; provider-bound positive pilot and independent NRTV remain open.",
        "secret_handling": "Known API/token variables removed from child process environment; no values inspected or recorded.",
        "version": version,
        "status": {
            "returncode": status["returncode"],
            "no_env_file": ".env file:" in str(status["output"]) and "not found" in str(status["output"]),
            "no_model": "Model:" in str(status["output"]) and "(not set)" in str(status["output"]),
            "no_provider_login": "not logged in" in str(status["output"]),
            "gateway_stopped": "Gateway Service" in str(status["output"]) and "stopped" in str(status["output"]),
            "raw_output": status["output"],
        },
        "negative_provider_pilot": {
            "expected": "non-zero and fail-closed before provider call because no provider credentials/config exist",
            "returncode": negative["returncode"],
            "passed": negative["returncode"] != 0 and "No LLM provider configured" in str(negative["output"]),
            "raw_output": negative["output"],
        },
        "rollback_dry_run": {
            "returncode": rollback["returncode"],
            "passed": rollback["returncode"] == 0
            and "Dry run: no files, services, or environment entries will be changed." in str(rollback["output"]),
            "raw_output": rollback["output"],
        },
        "doctor": {
            "returncode": doctor["returncode"],
            "local_core_checks_passed": all(
                token in str(doctor["output"])
                for token in (
                    "Python 3.11.9",
                    "Virtual environment active",
                    "Version files consistent (0.18.2)",
                    "SSL CA certificate bundle is valid",
                    "No suspicious MCP stdio commands",
                )
            ),
            "missing_credentials_reported": ".env file missing" in str(doctor["output"])
            or ".env file" in str(doctor["output"]),
            "claim": "PARTIAL_EXPECTED_NO_CREDENTIALS",
            "raw_output": doctor["output"],
        },
        "windows_copy_fallback_probe": {
            "returncode": fallback_probe["returncode"],
            "expected_test_assertion_failure": fallback_probe["returncode"] != 0,
            "safe_copy_fallback_observed": fallback_observed,
            "raw_output": fallback_probe["output"],
        },
        "official_security_rollback_tests": test_summary,
        "overall": "TEMP_CLOSED_CORE_WITH_WINDOWS_SYMLINK_EXCEPTIONS_AND_PROVIDER_HITL",
        "blocking_next_steps": [
            "Human supplies or completes one approved OAuth/API-key provider binding.",
            "Run a provider-bound positive pilot without exposing credentials.",
            "Run independent NRTV; do not waive Windows symlink exception without privileged rerun or explicit exclusion disposition.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "overall": report["overall"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
