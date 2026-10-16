"""WS-A rollback drill: prove rollback.py restores the live tree byte-for-byte.

Builds a throwaway reconstruction of the true pre-turn live state from the captured
pre-image, re-applies the candidate onto it, then rolls back and asserts every byte
matches the pre-turn state (and that added files are gone). No writes to the live dir.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A")
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
APPLY = W / "apply"
DRILL = W / "sim/drill"


def sha(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def tree(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): sha(p)
            for p in root.rglob("*") if p.is_file()}


def main() -> int:
    preimage = APPLY / "preimage"
    pre_turn = {k: v for k, v in tree(preimage).items()
                if k != "PREIMAGE_MANIFEST.json"}

    # rebuild chance: fresh drill = pre-turn copy
    if DRILL.exists():
        shutil.rmtree(DRILL)
    shutil.copytree(preimage, DRILL)
    (DRILL / "PREIMAGE_MANIFEST.json").unlink(missing_ok=True)
    assert tree(DRILL) == pre_turn, "drill pre-state != preimage"

    # land candidate onto the drill
    subprocess.run([PY, str(W / "tools/landing.py"), "--src", str(W / "repaired_candidate"),
                    "--dst", str(DRILL), "--preimage", str(W / "sim/drill_pre2"),
                    "--receipt", str(W / "sim/drill_receipt.json")], check=True)
    landed = tree(DRILL)
    assert landed != pre_turn, "landing changed nothing (drill vacuous)"

    # point a receipt at the drill and roll back
    rec = json.loads((W / "sim/drill_receipt.json").read_text(encoding="utf-8"))
    rec["dst"] = str(DRILL)
    drill_receipt = W / "sim/drill_receipt_used.json"
    drill_receipt.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    subprocess.run([PY, str(APPLY / "rollback.py"),
                    "--receipt", str(drill_receipt),
                    "--preimage", str(W / "sim/drill_pre2")], check=True)

    after = tree(DRILL)
    restored = after == pre_turn
    out = {"step": "rollback_drill", "pre_turn_files": len(pre_turn),
           "landed_files": len(landed), "restored_files": len(after),
           "byte_for_byte_restored": restored,
           "verdict": "PASS" if restored else "FAIL",
           "mismatches": [k for k in set(pre_turn) | set(after)
                          if pre_turn.get(k) != after.get(k)]}
    print(json.dumps(out, indent=1))
    (W / "rollback_drill_result.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    return 0 if restored else 1


if __name__ == "__main__":
    sys.exit(main())
