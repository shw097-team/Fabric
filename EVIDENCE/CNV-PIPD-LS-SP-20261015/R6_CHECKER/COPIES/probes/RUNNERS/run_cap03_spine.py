"""Drive probe_spine_lifecycle.py in each mode through probe_lib.capture.

Writes RAW/cap03_spine_<mode>.{stdout,stderr,json}. The probe itself only touches
the scratch sqlite under RAW/. No canonical mutation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_lib import capture  # noqa: E402

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
PROBE = str(ROOT / "RUNNERS" / "probe_spine_lifecycle.py")


def main() -> int:
    records = []
    for mode, pid in (
        ("positive", "cap03_spine_positive"),
        ("negative", "cap03_spine_negative"),
        ("acceptance", "cap03_spine_acceptance"),
        ("teardown", "cap03_spine_teardown"),
    ):
        rec = capture(pid, [PY, PROBE, mode], cwd=str(ROOT))
        records.append(rec)
    (ROOT / "RUNNERS" / "cap03_records.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps([{"probe_id": r["probe_id"], "exit_code": r["exit_code"]}
                      for r in records], ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
