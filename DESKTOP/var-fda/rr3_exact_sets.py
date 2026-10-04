# -*- coding: utf-8 -*-
"""RR3 closure: compute exact sets — bundle files / manifest entries / payload / self-entry."""
import hashlib
import json
import os

BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")

# 1. bundle physical files (recursive)
bundle_files = []
for root, dirs, files in os.walk(BUNDLE):
    for f in files:
        p = os.path.join(root, f)
        rel = os.path.relpath(p, BUNDLE)
        bundle_files.append(rel)
bundle_files.sort()
print(f"bundle_files (physical, recursive): {len(bundle_files)}")

# 2. manifest entries
m = json.load(open(MAN, encoding="utf-8"))
manifest_paths = [a["path"] for a in m["artifacts"]]
print(f"manifest_entries: {len(manifest_paths)}")
print(f"  unique paths: {len(set(manifest_paths))}")
print(f"  duplicate paths: {len(manifest_paths) - len(set(manifest_paths))}")

# 3. does manifest self-include? (manifest file itself in entries?)
man_rel = os.path.relpath(MAN, BUNDLE)
self_included = any(a["path"] == man_rel or a["path"] == man_rel.replace("\\", "/") for a in m["artifacts"])
print(f"manifest self-entry: {self_included} (path {man_rel!r})")

# 4. payload = manifest entries that are NOT the manifest itself and NOT the evidence MD?
#    payload_entries = evidence payload files (all non-manifest, non-reducer entries)
payload = [p for p in manifest_paths if os.path.basename(p) != "FDA_EVIDENCE_MANIFEST.json"]
print(f"payload_entries (manifest minus self): {len(payload)}")

# 5. bundle files not in manifest (extras)
in_manifest = set(p.replace("\\", "/") for p in manifest_paths)
extras = [b for b in bundle_files if b.replace("\\", "/") not in in_manifest]
print(f"bundle files NOT in manifest: {len(extras)}")
for e in extras:
    print("  EXTRA:", e)

# 6. manifest rows whose file is missing in bundle
missing = [p for p in manifest_paths if not os.path.exists(os.path.join(BUNDLE, p.replace("/", os.sep)))]
print(f"manifest rows missing on disk: {len(missing)}")
for x in missing:
    print("  MISSING:", x)
