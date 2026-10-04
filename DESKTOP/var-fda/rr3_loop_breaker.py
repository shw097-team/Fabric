# -*- coding: utf-8 -*-
"""RR3 loop-breaker: manifest MUST NOT include the evidence reducer MD.
Single-direction binding: evidence MD embeds manifest sha; manifest excludes MD.
Sets become:
  payload_entries = manifest rows (evidence payload, EXCLUDES evidence MD + manifest itself)
  manifest_entries = payload + 1 (manifest file physically present, not self-listed)
  bundle_files = physical count (incl. MD, manifest, index, readbacks...)
  reducer_self_entry_policy = evidence MD is NOT a manifest row (loop breaker);
                              MD references manifest by sha (single direction)
"""
import hashlib
import json
import os
import shutil

BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
FDA = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")

# sync MD into bundle first (its final bytes)
md_src = os.path.join(FDA, "FDA_IMPLEMENTATION_EVIDENCE.md")
md_dst = os.path.join(BUNDLE, "Fabric", "fabric-desktop-automation", "FDA_IMPLEMENTATION_EVIDENCE.md")
shutil.copy2(md_src, md_dst)
md_sha = hashlib.sha256(open(md_src, "rb").read()).hexdigest()
print("evidence MD sha256:", md_sha)

m = json.load(open(MAN, encoding="utf-8"))

# remove evidence MD from artifacts (reducer self-exclusion)
before = m["artifact_count"]
m["artifacts"] = [a for a in m["artifacts"]
                  if os.path.basename(a["path"]) != "FDA_IMPLEMENTATION_EVIDENCE.md"]
m["artifact_count"] = len(m["artifacts"])
print(f"payload rows: {before} -> {m['artifact_count']} (evidence MD excluded)")

# rehash all rows from bundle bytes
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"].replace("/", os.sep))
    if os.path.exists(p):
        data = open(p, "rb").read()
        a["sha256"] = hashlib.sha256(data).hexdigest()
        a["size"] = len(data)
    else:
        print("MISSING:", a["path"])

# update exact_sets with reducer self-exclusion policy
m["exact_sets"].update({
    "reducer_self_entry_policy": "evidence MD (FDA_IMPLEMENTATION_EVIDENCE.md) is NOT a manifest row "
        "(loop breaker: MD embeds manifest sha single-direction; manifest excludes MD). "
        "The MD is delivered alongside the bundle as the review entry artifact.",
    "evidence_reducer_sha256": md_sha,
    "bundle_files": None,
})
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# physical bundle count
bundle_files = []
for root, dirs, files in os.walk(BUNDLE):
    for f in files:
        bundle_files.append(os.path.relpath(os.path.join(root, f), BUNDLE))
m["exact_sets"]["bundle_files"] = len(bundle_files)
json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print(f"payload={m['artifact_count']} | manifest_entries={m['artifact_count']+1} | bundle_files={len(bundle_files)}")
print(f"manifest sha256 (final, loop-free): {mh}")

# verify
bad = 0
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"].replace("/", os.sep))
    if not os.path.exists(p):
        print("MISSING:", a["path"]); bad += 1
    elif hashlib.sha256(open(p, "rb").read()).hexdigest() != a["sha256"]:
        print("HASH MISMATCH:", a["path"]); bad += 1
print("verify:", "ALL OK" if bad == 0 else f"{bad} bad")
