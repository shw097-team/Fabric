"""Local dry-run of the remote readback check: every file the index lists must match on disk,
and the only payload file NOT listed must be PACK_INDEX.json itself."""
import hashlib
import json
from pathlib import Path

PAY = Path(__file__).resolve().parent / "publish" / "payload"
idx = json.loads((PAY / "PACK_INDEX.json").read_text(encoding="utf-8"))
bad = []
for f in idx["files"]:
    p = PAY / f["path"]
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    if h != f["sha256"] or p.stat().st_size != f["bytes"]:
        bad.append(f["path"])
actual = {str(p.relative_to(PAY)).replace("\\", "/") for p in PAY.rglob("*") if p.is_file()}
notlisted = sorted(actual - {f["path"] for f in idx["files"]})
print("listed", len(idx["files"]), "| actual payload files", len(actual), "| mismatches", len(bad), bad[:3])
print("files not listed (must be exactly the index):", notlisted)
print("declared self_excluded:", idx.get("self_excluded", {}).get("path"),
      "| payload_files_total:", idx.get("payload_files_total"))
print("LOCAL_DRYRUN=" + ("PASS" if not bad and notlisted == ["PACK_INDEX.json"] else "FAIL"))
