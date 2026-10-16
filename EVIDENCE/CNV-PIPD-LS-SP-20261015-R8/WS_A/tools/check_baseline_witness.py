"""Verify the frozen baseline holds the ORIGINAL bytes for the 6 absorbed stubs.

The stubs' recorded sha256 must equal sha256(baseline/references/<name>) for each
still-absorbed reference, so the baseline is a valid 'originals' witness for the
harness --live argument after the live tree is overwritten with stubs.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A")
SRC = W / "repaired_candidate"
BASE = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014"
            "/baseline/adversarial-verification-rounds")
STUB_RE = re.compile(r"absorbed -> [^\s]+ :: topic_byte_offset=\d+ :: sha256=(?P<sha>[0-9a-f]{64})")


def main() -> int:
    rows = []
    ok = True
    for p in sorted((SRC / "references").glob("*.md")):
        b = p.read_bytes()
        m = STUB_RE.search(b.decode("utf-8", "replace"))
        if m is None:
            continue
        bf = BASE / "references" / p.name
        if not bf.is_file():
            rows.append({"ref": p.name, "baseline_present": False, "match": False})
            ok = False
            continue
        bb = bf.read_bytes()
        bs = hashlib.sha256(bb).hexdigest()
        match = bs == m.group("sha")
        ok = ok and match
        rows.append({"ref": p.name, "baseline_bytes": len(bb), "baseline_sha256": bs,
                     "recorded_sha256": m.group("sha"), "match": match})
    out = {"step": "baseline_witness", "verdict": "PASS" if ok else "FAIL", "rows": rows}
    (W / "baseline_witness.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
