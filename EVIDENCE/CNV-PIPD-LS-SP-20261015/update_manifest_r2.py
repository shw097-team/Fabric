"""把掃描到的 5 份回收筒還原之證據登記進 manifest 更新版；另補 6 號缺失指定 STATE。"""
import os, json, hashlib

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
rb_dir = os.path.join(ROOT, "physical_source_readback")

man_path = os.path.join(ROOT, "PHYSICAL_SOURCE_READBACK_MANIFEST.json")
with open(man_path, encoding="utf-8") as f:
    manifest = json.load(f)

# 5 份回收筒已回復檔案；登記它們
recycled = [
    "AUDIT_Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG_v1.0.0_FULL_DESTRUCTIVE_2026-10-15(1).md",
    "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG_Blueprint_v1.0.0_2026-10-15.md",
    "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG_Blueprint_v1.0.0_FULL_DESTRUCTIVE_AUDIT_2026-10-15(1).md",
    "Fabric_Hermes_HGK_Convergence_Blueprint_Full_Destructive_Audit_2026-10-14(1).md",
    "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_2026-10-14.md",
]
rows_manifest = {}
for row in manifest["rows"]:
    rows_manifest[row["path"].split("physical_source_readback")[-1].lstrip("\\")] = row

new_rows = []
for row in manifest["rows"]:
    new_rows.append(row)

added = 0
for fn in recycled:
    p = os.path.join(rb_dir, fn)
    if os.path.isfile(p):
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        prev = rows_manifest.get(fn)
        expected = None
        for m in manifest["missing"]:
            if m["sha256"] == h:
                expected = m
        if expected:
            new_rows.append({
                "path": p,
                "bytes": expected["bytes"],
                "sha256": expected["sha256"],
                "origin": "C:\\$Recycle.Bin byte-identical recovery",
                "origin_kind": "RECYCLE_BIN_BYTE_RECOVERY",
            })
            added += 1
print("ADDED_TO_MANIFEST", added)

six = [m for m in manifest["missing"] if m["filename"] == "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v1.1.0_PATCHED_2026-10-15.md"]
print("STILL_MISSING_COUNT", len(manifest["missing"]) - added)
print("STILL_MISSING", [m["filename"] for m in manifest["missing"] if m["sha256"] not in {r["sha256"] for r in new_rows}])

# 寫入 updated manifest v2
with open(os.path.join(ROOT, "PHYSICAL_SOURCE_READBACK_MANIFEST_R2.json"), "w", encoding="utf-8") as f:
    json.dump({
        "claim": "byte copies + verified appendix recovery + recycle bin byte-identical recovery; not canonical source freeze",
        "expected": 21,
        "materialized": added + 15,
        "rows": new_rows,
        "missing": [m for m in manifest["missing"] if m["sha256"] not in {r["sha256"] for r in new_rows}],
    }, f, ensure_ascii=False, indent=2)
print("manifest_v2_written")
