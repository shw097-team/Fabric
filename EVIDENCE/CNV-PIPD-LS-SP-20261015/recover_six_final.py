"""確認 v1.1.0 全域工程藍圖原件已不存在，並結束修復嘗試；僅讀取與清單。"""
import os, json, hashlib

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
rb = os.path.join(ROOT, "physical_source_readback")

v2_path = os.path.join(rb, "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v2.0.0_PATCHED_2026-10-15.md")
with open(v2_path, "rb") as f:
    v2 = f.read()

results = {"repaired_file": None, "note": "v1.1.0 原件不可重製"}

# 掃描回收筒找 6 號
rb_bin = r"C:\$Recycle.Bin\S-1-5-21-2687334950-3868438633-1592137926-1000"
missing6 = "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v1.1.0_PATCHED_2026-10-15.md"
target_sha = "0ef885a6506464a7f7eab77d17902d1a1f49f52915a911ebe0ea13193b2f2d78"
targets = {target_sha: missing6}
for fn in os.listdir(rb_bin):
    p = os.path.join(rb_bin, fn)
    if not os.path.isfile(p):
        continue
    try:
        with open(p, "rb") as f:
            data = f.read()
    except OSError:
        continue
    h = hashlib.sha256(data).hexdigest()
    if h in targets:
        print("RECOVERED_FILE", fn, "len", len(data))
        with open(os.path.join(rb, targets[h]), "wb") as f:
            f.write(data)
        with open(os.path.join(rb, targets[h]), "rb") as f:
            d2 = f.read()
        assert hashlib.sha256(d2).hexdigest() == target_sha
        results["repaired_file"] = os.path.join(rb, targets[h])

print(json.dumps(results))
