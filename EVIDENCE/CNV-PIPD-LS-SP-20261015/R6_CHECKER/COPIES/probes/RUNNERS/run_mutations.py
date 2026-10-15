"""Drive the locally constructible MUTATIONS_18 cases through probe_lib.capture."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_lib import capture  # noqa: E402

ROOT = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
R = str(ROOT / "RUNNERS")

# M02 (plugin helper body tamper) and the bridge/RQ-case mutations (M07..M10, M13, M15, M17)
# require the frozen R5 corpus package whose physical bytes are not reachable on this host, so
# they are recorded NOT_RUN by the artifact writer rather than probed here.
CONSTRUCTIBLE = ["m01", "m03", "m04", "m05", "m06", "m11", "m12", "m14", "m16", "m18"]


def main() -> int:
    records = []
    for mode in CONSTRUCTIBLE:
        pid = f"mut_{mode}"
        rec = capture(pid, [PY, f"{R}/probe_mutations.py", mode], cwd=str(ROOT))
        records.append(rec)
        print(f"{pid}: exit={rec['exit_code']}")
    out = ROOT / "RUNNERS" / "mutation_records.json"
    out.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out} ({len(records)} cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
