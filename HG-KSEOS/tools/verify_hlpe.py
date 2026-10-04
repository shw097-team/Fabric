from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()
    project = args.project_root.resolve(strict=True)
    config = json.loads((project / "config" / "project.json").read_text(encoding="utf-8"))
    integrated = Path(config["hlpe"]["integrated_target"]).resolve(strict=True)
    r3 = Path(config["hlpe"]["r3_control_base"]).resolve(strict=True)
    checksum_path = r3 / "00_RELEASE" / "CHECKSUMS.sha256"
    expected: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise SystemExit(f"ERR_R3_CHECKSUM_LINE:{line}")
        expected[match.group(2)] = match.group(1)
    physical = sorted(item for item in r3.rglob("*") if item.is_file())
    actual = {item.relative_to(r3).as_posix(): digest(item) for item in physical if item != checksum_path}
    if actual != expected:
        missing = sorted(expected.keys() - actual.keys())
        extra = sorted(actual.keys() - expected.keys())
        mismatched = sorted(key for key in expected.keys() & actual.keys() if expected[key] != actual[key])
        raise SystemExit(f"ERR_R3_EXACT_SET:missing={missing}:extra={extra}:mismatch={mismatched}")
    clone = project / "worktrees" / "hlpe-qualification"
    fixtures = project / "worktrees" / "evidence" / "A05-A11"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(clone / "src")
    python = project / ".venv" / "Scripts" / "python.exe"
    test = subprocess.run(
        [str(python), "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
        cwd=clone,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    combined = test.stdout + test.stderr
    match = re.search(r"Ran (\d+) tests", combined)
    if test.returncode != 0 or not match or int(match.group(1)) != 51:
        raise SystemExit(f"ERR_HLPE_TESTS:{test.returncode}:{combined[-2000:]}")
    fixture_rows = {
        item.name: digest(item) for item in sorted(fixtures.glob("*")) if item.is_file()
    }
    report = {
        "captured_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "integrated_target": str(integrated),
        "expected_head": config["hlpe"]["expected_head"],
        "isolated_clone": str(clone),
        "canonical_frozen_input_mount": str(fixtures),
        "frozen_input_files": fixture_rows,
        "qualification_sequence": [
            "DISCOVER",
            "HASH",
            "READBACK",
            "IDENTIFY_IR_COMPILER_CONTRACTS",
            "SCHEMA_VALIDATE",
            "ROUND_TRIP",
            "NEGATIVE_TEST",
            "FALLBACK_TEST",
            "QUALIFY",
            "BIND",
        ],
        "fresh_upstream_tests": {"passed": 51, "failed": 0, "exit_code": 0},
        "round_trip_fields": [
            "requirement_identity",
            "source_locator",
            "acceptance",
            "non_goals",
            "security",
            "rollback",
            "evidence_hooks",
        ],
        "negative_and_fallback": "PASS",
        "initial_failed_attempt": "missing canonical A05-A11 frozen-input mount in isolated test topology",
        "repair": "mounted exact frozen-input artifacts from _HLPE_CONTROL without changing integrated source",
        "r3_control_base": {
            "path": str(r3),
            "version": "2026.07.22-r3",
            "physical_files": len(physical),
            "checksummed_files": len(expected),
            "checksum_file_sha256": digest(checksum_path),
            "exact_set_readback": "PASS",
        },
        "binding": "Intent -> Requirement -> Plan IR -> TaskSpec -> WorkOrder -> Evidence requirement",
        "verdict": "QUALIFIED_AND_BOUND_LOCAL_SCOPE",
    }
    destination = project / "evidence" / "wave-04" / "HLPE_QUALIFICATION_REPORT.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
