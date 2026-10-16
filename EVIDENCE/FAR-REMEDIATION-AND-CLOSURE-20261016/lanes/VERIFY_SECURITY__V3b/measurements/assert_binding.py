import hashlib
import json
from pathlib import Path

work = Path(__file__).resolve().parents[1]
report = json.loads((work / "TEST_RESULTS/digest_check.json").read_text(encoding="utf-8"))
root = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
manifest_path = root / "var/FAR-REMEDIATION-AND-CLOSURE-20261016/FROZEN_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
aggregate = hashlib.sha256()
missing = []
for item in manifest["items"]:
    local = work / "subject" / Path(item["path"]).relative_to(root)
    digest = hashlib.sha256(local.read_bytes()).hexdigest() if local.is_file() else None
    if item["exists"] and not local.is_file():
        missing.append(item["path"])
    aggregate.update(("%s|%s|%s\n" % (item["label"], item["path"], digest)).encode())
result = {"declared": manifest["aggregate_sha256"], "copy_aggregate_using_manifest_order": aggregate.hexdigest(), "missing_required_items": missing, "copy_equals_frozen_tree": report["copy_equals_frozen"], "status": "INCONCLUSIVE", "assertion": "not evaluated"}
try:
    assert not missing, "copy lacks %d required manifest files" % len(missing)
    assert aggregate.hexdigest() == manifest["aggregate_sha256"], "copy aggregate disagrees with declared digest"
    assert report["manifest_recomputed_over_original_paths"] == manifest["aggregate_sha256"], "original subject manifest drift"
except AssertionError as error:
    result["assertion"] = "FAILED: " + str(error)
    (work / "TEST_RESULTS/binding_gate.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(1)
raise SystemExit("Unexpected successful binding; inspect report before adjudication")
