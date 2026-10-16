"""Assemble R8_MUTATIONS_18_ON_MAIN.json from raw captures + the R6 baseline.

Reads only RAW/mut_m*.stdout.txt (verbatim probe rows) and the R6 MUTATIONS_18.json
baseline (for the NOT_RUN rows). Never invents output.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

WSB = Path(__file__).resolve().parent
RAW = WSB / "RAW"
BASE = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/MUTATIONS_18.json")
DRIVER_DIFF = WSB / "R8_0_DRIVER_DIFF.patch"
PRODUCT = "C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt"

ORDER = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09",
         "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18"]
NOT_RUN_IDS = {"M02", "M07", "M08", "M09", "M10", "M13", "M15", "M17"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    base_rows = {r["id"]: r for r in base["rows"]}
    rows = []
    for mid in ORDER:
        if mid in NOT_RUN_IDS:
            br = base_rows[mid]
            rows.append({
                "id": mid, "mutation": br["mutation"], "expected": "REJECT",
                "observed": "NOT_RUN", "validator_verdict": "",
                "first_fail": "", "raw_receipt": "",
                "rejudgement": "NOT_CONSTRUCTIBLE_FROZEN_BYTES_ABSENT",
                "not_run_reason": br["not_run_reason"],
            })
            continue
        stub = mid.lower()  # M01 -> m01
        f = RAW / f"mut_{stub}.stdout.txt"
        row = json.loads(f.read_text(encoding="utf-8"))
        row["raw_receipt"] = f"RAW/mut_{stub}.stdout.txt"
        row["raw_receipt_sha256"] = sha256_file(f)
        rows.append(row)
    detected = [r["id"] for r in rows if r.get("observed") == "REJECT"]
    not_detected = [r["id"] for r in rows if r.get("observed") == "ACCEPT"]
    not_run = [r["id"] for r in rows if r.get("observed") == "NOT_RUN"]
    out = {
        "schema": "PIPD-R8-MUTATIONS-18-ON-MAIN/1",
        "producer": "WS-B (R8-0 rebase on main)",
        "produced_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f+00:00"),
        "base_commit": "dba4b19456777d3b597fdf71480f6423dd974243",
        "product_tree": PRODUCT,
        "driver_diff": str(DRIVER_DIFF.name),
        "driver_diff_sha256": sha256_file(DRIVER_DIFF),
        "driver_note": ("R6/R7 mutation driver reused verbatim; only PIPD_SRC / SCHEMAS / "
                        "RAW / ROOT constants redirected (no logic change). See driver_diff."),
        "totals": {"executed": len(detected) + len(not_detected),
                   "detected": len(detected), "not_detected": len(not_detected),
                   "not_run": len(not_run), "total": len(rows)},
        "rows": rows,
        "detected_ids": detected,
        "not_detected_ids": not_detected,
        "not_run_ids": not_run,
        "claim_level": "LOCAL / candidate-only; a green local run is not an acceptance and not a Gate PASS",
    }
    dst = WSB / "R8_MUTATIONS_18_ON_MAIN.json"
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {dst}: executed={len(detected)+len(not_detected)} detected={len(detected)} "
          f"not_detected={len(not_detected)} not_run={len(not_run)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
