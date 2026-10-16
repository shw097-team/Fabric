import hashlib
import json
from pathlib import Path

work = Path(__file__).resolve().parents[1]
root = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
round_dir = root / "var/FAR-REMEDIATION-AND-CLOSURE-20261016"
manifest = json.loads((round_dir / "FROZEN_MANIFEST.json").read_text(encoding="utf-8-sig"))
rows = []
aggregate = hashlib.sha256()
for item in manifest["items"]:
    relative = Path(item["path"]).relative_to(root)
    local = work / "subject" / relative
    actual = hashlib.sha256(local.read_bytes()).hexdigest() if local.is_file() else None
    canonical = Path(item["path"])
    canonical_digest = hashlib.sha256(canonical.read_bytes()).hexdigest() if canonical.is_file() else None
    aggregate.update(("%s|%s|%s\n" % (item["label"], item["path"], canonical_digest)).encode())
    rows.append({"path": str(relative), "expected": item["sha256"], "copy_present": local.is_file(), "copy_digest": actual, "canonical_digest": canonical_digest, "canonical_matches": canonical_digest == item["sha256"]})
copy_files = {path.relative_to(work / "subject").as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted((work / "subject").rglob("*")) if path.is_file()}
frozen = round_dir / "subject"
frozen_files = {path.relative_to(frozen).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(frozen.rglob("*")) if path.is_file()}
result = {"manifest_declared": manifest["aggregate_sha256"], "manifest_recomputed_over_original_paths": aggregate.hexdigest(), "manifest_rows": rows, "copy_count": len(copy_files), "frozen_count": len(frozen_files), "copy_equals_frozen": copy_files == frozen_files, "copy_relative_map_sha256": hashlib.sha256(json.dumps(sorted(copy_files.items()), sort_keys=True).encode()).hexdigest(), "instructions": {str(path): path.read_text(encoding="utf-8-sig") for path in work.rglob("AGENTS.md")}}
(work / "TEST_RESULTS/digest_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in result.items() if key not in ("manifest_rows", "instructions")}, indent=2))
print("Manifest mismatches:", json.dumps([row for row in rows if not row["canonical_matches"]], indent=2))
print("Copy covered:", sum(row["copy_present"] for row in rows), "/", len(rows))
print("Nested instructions:", json.dumps(result["instructions"], indent=2))
