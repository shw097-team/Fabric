from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


PREDEV_HEADER_PREFIX = "|REQ|direct_source_locator|"
P0_HEADER_PREFIX = "|p0_req|family|"
PREDEV_ID = re.compile(r"^REQ-\d{3}$")
P0_ID = re.compile(r"^(?:COV-\d{2}-\d{2}|SQS-REQ-\d{3})$")


def split_markdown_row(line: str) -> list[str]:
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError("not a complete Markdown table row")
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line[1:-1]:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
            current.append(char)
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def extract_table(lines: list[str], header_prefix: str, id_pattern: re.Pattern[str]) -> list[dict[str, str]]:
    header_index = next(i for i, line in enumerate(lines) if line.startswith(header_prefix))
    header = split_markdown_row(lines[header_index])
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        cells = split_markdown_row(line)
        if len(cells) != len(header):
            raise ValueError(f"column mismatch at row {line[:80]!r}: {len(cells)} != {len(header)}")
        if not id_pattern.fullmatch(cells[0].strip("`")):
            break
        rows.append(dict(zip(header, cells, strict=True)))
    return rows


def extract_all_tables(
    lines: list[str], header_prefix: str, id_pattern: re.Pattern[str]
) -> list[dict[str, str]]:
    combined: list[dict[str, str]] = []
    for header_index, line in enumerate(lines):
        if not line.startswith(header_prefix):
            continue
        header = split_markdown_row(line)
        for row_line in lines[header_index + 2 :]:
            if not row_line.startswith("|"):
                break
            cells = split_markdown_row(row_line)
            if len(cells) != len(header):
                raise ValueError(
                    f"column mismatch at row {row_line[:80]!r}: {len(cells)} != {len(header)}"
                )
            if not id_pattern.fullmatch(cells[0].strip("`")):
                break
            combined.append(dict(zip(header, cells, strict=True)))
    return combined


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def p0_children(row: dict[str, str]) -> list[str]:
    raw = row["child_requirements"]
    children = [item.strip() for item in raw.split(";") if item.strip()]
    return children or [f"{row['p0_req']}-C1: {row['original_wording']}"]


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: compile_requirements.py GROUP01_MD OUTPUT_DIR", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    lines = source.read_text(encoding="utf-8").splitlines()
    predev = extract_table(lines, PREDEV_HEADER_PREFIX, PREDEV_ID)
    p0 = extract_all_tables(lines, P0_HEADER_PREFIX, P0_ID)
    if len(predev) != 240:
        raise SystemExit(f"ERR_PREDEV_DENOMINATOR: expected 240, observed {len(predev)}")
    if len(p0) != 259:
        raise SystemExit(f"ERR_P0_DENOMINATOR: expected 259, observed {len(p0)}")
    if len({r['REQ'] for r in predev}) != 240:
        raise SystemExit("ERR_PREDEV_DUPLICATE_ID")
    if len({r['p0_req'] for r in p0}) != 259:
        raise SystemExit("ERR_P0_DUPLICATE_ID")

    write_csv(output / "PREDEV_REQUIREMENTS.csv", list(predev[0]), predev)
    write_csv(output / "P0_REQUIREMENTS.csv", list(p0[0]), p0)

    atomic: list[dict[str, str]] = []
    trace: list[dict[str, str]] = []
    acceptance: list[dict[str, str]] = []
    for row in predev:
        atomic.append(
            {
                "parent_requirement": row["REQ"],
                "atomic_requirement": row["REQ"] + "-C1",
                "wording": row["requirement"],
                "source": "PREDEV",
                "source_locator": row["direct_source_locator"],
            }
        )
        trace.append(
            {
                "requirement_id": row["REQ"],
                "source": "PREDEV",
                "source_locator": row["direct_source_locator"],
                "architecture": f"{row['target_doc']}#{row['target_h1']}",
                "wp": row["WP"],
                "rbwi": row["RBWI"],
                "contract_artifact": row["CA"],
                "spec": row["SPEC"],
                "acceptance": row["ACC"],
                "implementation_locator": "UNBOUND_PENDING_WAVE_03_PLUS",
                "test_locator": row["fixture"],
                "evidence_plan": row["evidence"],
                "status": "COMPILED_NOT_IMPLEMENTED",
            }
        )
        acceptance.append(
            {
                "requirement_id": row["REQ"],
                "acceptance_id": row["ACC"],
                "oracle": row["oracle"],
                "threshold": row["threshold"],
                "negative_fixture": row["rejected_interpretation"],
                "test_locator": row["fixture"],
                "gate": row["Gate"],
                "evidence_plan": row["evidence"],
                "verdict": "NOT_RUN",
            }
        )
    for row in p0:
        for index, child in enumerate(p0_children(row), start=1):
            child_id, sep, wording = child.partition(":")
            atomic.append(
                {
                    "parent_requirement": row["p0_req"],
                    "atomic_requirement": child_id.strip() if sep else f"{row['p0_req']}-C{index}",
                    "wording": wording.strip() if sep else child,
                    "source": "P0",
                    "source_locator": row["original_source_locator"],
                }
            )
        trace.append(
            {
                "requirement_id": row["p0_req"],
                "source": "P0",
                "source_locator": row["original_source_locator"],
                "architecture": f"{row['new_DOC']}#{row['new_H1']}",
                "wp": row["new_WP"],
                "rbwi": row["new_RBWI"],
                "contract_artifact": row["new_CA"],
                "spec": row["new_SPEC"],
                "acceptance": row["new_ACC"],
                "implementation_locator": "UNBOUND_PENDING_WAVE_03_PLUS",
                "test_locator": row["original_test_gate"],
                "evidence_plan": "EvidenceEnvelope + source-bound positive/negative/boundary/adversarial receipts",
                "status": "COMPILED_NOT_IMPLEMENTED",
            }
        )
        acceptance.append(
            {
                "requirement_id": row["p0_req"],
                "acceptance_id": row["new_ACC"],
                "oracle": row["original_oracle"],
                "threshold": row["original_test_gate"],
                "negative_fixture": row["original_rejected_interpretation"],
                "test_locator": row["original_test_gate"],
                "gate": row["original_test_gate"],
                "evidence_plan": "EvidenceEnvelope + checker receipt + rollback receipt",
                "verdict": "NOT_RUN",
            }
        )

    write_csv(output / "ATOMIC_CHILD_REQUIREMENTS.csv", list(atomic[0]), atomic)
    write_csv(output / "REQUIREMENT_TRACEABILITY.csv", list(trace[0]), trace)
    write_csv(output / "ACCEPTANCE_EVIDENCE_PLAN.csv", list(acceptance[0]), acceptance)
    summary = {
        "source": str(source),
        "predev_requirements": len(predev),
        "p0_requirements": len(p0),
        "requirement_trace_rows": len(trace),
        "atomic_child_rows": len(atomic),
        "acceptance_plan_rows": len(acceptance),
        "status": "COMPILED_NOT_IMPLEMENTED",
    }
    (output / "REQUIREMENT_COMPILATION_RECEIPT.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
