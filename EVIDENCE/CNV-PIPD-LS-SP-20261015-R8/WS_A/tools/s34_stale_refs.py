"""WS-A steps 3+4: handle stale absorbed references by carrying the CURRENT live file.

Step 3: references/verifier-lane-handover.md is STALE (stub recorded aebb35ea.., live is
        2126b82e..). Do NOT absorb it; copy the current live file verbatim.
Step 4: re-verify every remaining stub against the CURRENT live bytes; any further mismatch
        is handled the same way and recorded.

Reads the frozen candidate stubs (source of the recorded sha) and the live tree; writes into
WS_A/repaired_candidate/references/. Records WS_A/s34_stale_refs_result.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A")
SRC = W / "repaired_candidate"
LIVE = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
            "/skills/software-development/adversarial-verification-rounds")
STUB_RE = re.compile(r"absorbed -> (?P<topic>[^\s]+) :: topic_byte_offset=(?P<off>\d+) :: sha256=(?P<sha>[0-9a-f]{64})")
STUB_MAX = 600


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    rows: list[dict] = []
    carried: list[dict] = []
    for p in sorted((SRC / "references").glob("*.md")):
        b = p.read_bytes()
        m = STUB_RE.search(b.decode("utf-8", "replace"))
        if m is None:
            continue
        live_ref = LIVE / "references" / p.name
        recorded = m.group("sha")
        if not live_ref.is_file():
            rows.append({"ref": p.name, "status": "NO_LIVE_COUNTERPART", "recorded_sha": recorded})
            continue
        lb = live_ref.read_bytes()
        live_sha = sha(lb)
        match = live_sha == recorded
        rows.append({"ref": p.name, "recorded_sha256": recorded, "live_sha256": live_sha,
                     "live_bytes": len(lb), "sha_match": match,
                     "status": "VERIFIED" if match else "STALE_MISMATCH"})
        if not match:
            p.write_bytes(lb)
            carried.append({"ref": p.name, "path": str(p.relative_to(W)),
                            "action": "EXCLUDED_STALE_ABSORPTION",
                            "stub_recorded_sha256": recorded, "carried_live_sha256": live_sha,
                            "carried_live_bytes": len(lb)})

    out = {"step": "s34_stale_refs", "stubs_examined": len(rows),
           "verified": [r["ref"] for r in rows if r.get("status") == "VERIFIED"],
           "mismatches_handled": carried, "rows": rows}
    (W / "s34_stale_refs_result.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
