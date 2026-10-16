"""Record the pre-image manifest (path, bytes, sha256) for WS_B/preimage."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def main() -> int:
    pre = Path(sys.argv[1])
    rows = []
    for p in sorted(pre.rglob("*")):
        if p.is_file():
            b = p.read_bytes()
            rows.append({"path": p.relative_to(pre).as_posix(),
                         "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    out = {"schema": "WS_R9B/PREIMAGE-MANIFEST/1", "preimage_root": str(pre),
           "count": len(rows), "entries": rows}
    (pre / "PREIMAGE_MANIFEST.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({"preimage_root": str(pre), "count": len(rows)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
