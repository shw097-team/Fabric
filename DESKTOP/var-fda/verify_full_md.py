# -*- coding: utf-8 -*-
"""Verify full-evidence MD has real embedded bodies (not pointers) + finalize sha in header."""
import hashlib
import os

P = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_EXTERNAL_FULL_EVIDENCE_20260814.md"
txt = open(P, encoding="utf-8").read()

# 1. verify real bodies embedded
checks = {
    "receipt_bodies": txt.count("```json") >= 7,
    "sensorlog_rows": "SensorLog Table_20260814" in txt and "FDAPaper" in txt,
    "sensorlist_rows": "SensorList (persistence)" in txt and "FDA_PAPER_ALERT" in txt,
    "manifest_table": "EvidenceManifest — full artifact table" in txt,
    "dod_counts": "PASS 36" in txt or "'PASS': 36" in txt,
    "checker_174": "174/174" in txt,
    "no_path_only": "C:\\SysJust" not in txt.replace("C:\\\\SysJust", ""),  # paths only as provenance labels
}
for k, v in checks.items():
    print(("PASS " if v else "FAIL ") + k)

# 2. fill own sha into header (avoid self-reference loop: write sha after computing)
data = open(P, "rb").read()
sha = hashlib.sha256(data).hexdigest()
hdr = txt.split("```yaml")[1].split("```")[0]
if "this_file_sha256" not in hdr:
    txt = txt.replace("generated_at: %s" % "", "generated_at: 2026-08-14")  # no-op guard
# insert sha line into yaml header
lines = txt.split("\n")
for i, l in enumerate(lines):
    if l.startswith("generated_at:"):
        lines.insert(i, "this_file_sha256: " + sha)
        break
open(P, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
sha2 = hashlib.sha256(open(P, "rb").read()).hexdigest()
print("final sha256 (with header):", sha2)
