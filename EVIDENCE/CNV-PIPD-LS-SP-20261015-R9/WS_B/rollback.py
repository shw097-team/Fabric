"""WS-A rollback: restore every pre-image byte-for-byte and delete every added file.

Reads WS_A/apply/APPLY_RECEIPT.json (sibling) and WS_A/apply/preimage/ (sibling).
For each path:
  action == "replaced"          -> write preimage/<path> bytes back over dst/<path>
  action == "added"             -> delete dst/<path>
  action == "retained_untouched"-> leave untouched
Verifies each restored file's sha256 equals the recorded before_sha256.

  python rollback.py            # perform rollback
  python rollback.py --check    # verify current dst matches the pre-turn state, no writes
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_RECEIPT = HERE / "APPLY_RECEIPT.json"
DEFAULT_PREIMAGE = HERE / "preimage"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--receipt", default=str(DEFAULT_RECEIPT),
                    help="APPLY_RECEIPT.json to act on (default: sibling)")
    ap.add_argument("--preimage", default=str(DEFAULT_PREIMAGE),
                    help="pre-image directory (default: sibling)")
    a = ap.parse_args()
    receipt = Path(a.receipt)
    preimage = Path(a.preimage)
    rec = json.loads(receipt.read_text(encoding="utf-8"))
    dst = Path(rec["dst"])
    problems: list[str] = []
    for row in rec["paths"]:
        rel = row["path"]
        target = dst / rel
        act = row["action"]
        if act == "replaced":
            pre = preimage / rel
            pb = pre.read_bytes()
            if sha(pb) != row["before_sha256"]:
                problems.append(f"preimage sha mismatch: {rel}")
                continue
            if a.check:
                cur = target.read_bytes() if target.is_file() else b""
                if sha(cur) != row["before_sha256"]:
                    problems.append(f"NOT yet restored: {rel}")
            else:
                target.write_bytes(pb)
        elif act == "added":
            if a.check:
                if target.exists():
                    problems.append(f"added file still present: {rel}")
            else:
                if target.exists():
                    target.unlink()
        # retained_untouched: nothing to do
    if problems:
        print(json.dumps({"rollback": "FAIL", "problems": problems}, indent=1))
        return 1
    print(json.dumps({"rollback": "OK" if not a.check else "CLEAN",
                      "mode": "check" if a.check else "apply",
                      "paths_total": len(rec["paths"])}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
