from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path


FIELDS = (
    "case_id",
    "domain",
    "type",
    "fixture",
    "environment",
    "preconditions",
    "procedure",
    "oracle",
    "expected",
    "reject_code",
    "evidence",
    "rollback",
    "owner",
    "independent_verifier",
    "rerun_command",
    "source_locator",
    "source_status",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("project_root", type=Path)
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    project = args.project_root.resolve(strict=True)
    rows: list[dict[str, str]] = []
    for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not re.match(r"^\|TST-\d{3}\|", line):
            continue
        values = line.strip("|").split("|")
        case_number = int(values[0].split("-")[1])
        if case_number <= 68:
            if len(values) != 15:
                raise SystemExit(f"ERR_CASE_FIELD_COUNT:{values[0]}:{len(values)}")
            row = dict(zip(
                ("case_id", "domain", "type", "fixture", "environment", "preconditions", "procedure", "oracle", "expected", "reject_code", "evidence", "owner", "independent_verifier", "rerun_command", "source_status"),
                values,
                strict=True,
            ))
            row["rollback"] = "restore prior accepted generation / reopen mapped TT"
        else:
            if len(values) != 13:
                raise SystemExit(f"ERR_CASE_FIELD_COUNT:{values[0]}:{len(values)}")
            row = dict(zip(
                ("case_id", "domain", "type", "fixture", "preconditions", "procedure", "oracle", "reject_code", "evidence", "rollback", "owner", "independent_verifier", "source_status"),
                values,
                strict=True,
            ))
            row["environment"] = "isolated local fixture / pinned design inputs"
            row["expected"] = row["oracle"]
            row["rerun_command"] = f"case.run --id {row['case_id']}"
        row["source_locator"] = f"{source.name}#L{line_number}"
        rows.append({field: row[field] for field in FIELDS})
    expected_ids = [f"TST-{index:03d}" for index in range(1, 93)]
    if [row["case_id"] for row in rows] != expected_ids:
        raise SystemExit("ERR_ACCEPTANCE_CASE_DENOMINATOR_OR_ORDER")
    output = project / "eval" / "FROZEN_ACCEPTANCE_CASES.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    receipt = {
        "captured_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "source": str(source),
        "source_sha256": digest(source),
        "case_count": len(rows),
        "case_ids": {"first": rows[0]["case_id"], "last": rows[-1]["case_id"], "unique": len({row["case_id"] for row in rows})},
        "frozen_baseline": str(output),
        "frozen_baseline_sha256": digest(output),
        "verdict": "FROZEN_CASE_BASELINE_PASS",
    }
    receipt_path = project / "evidence" / "wave-15" / "EVAL_BASELINE_RECEIPT.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
