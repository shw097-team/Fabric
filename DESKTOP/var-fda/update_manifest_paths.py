# -*- coding: utf-8 -*-
"""Update EvidenceManifest artifact paths for reorganized FDA folder + rehash."""
import hashlib
import json
import os

BUNDLE = r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE"
FDA = r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation"
MAN = os.path.join(BUNDLE, "FDA_EVIDENCE_MANIFEST.json")

# move receipts/governance rows in the bundle too (bundle mirrors fabric-desktop-automation/)
for sub in ("evidence/receipts", "governance"):
    src_dir = os.path.join(BUNDLE, "Fabric", "fabric-desktop-automation", sub)
    os.makedirs(src_dir, exist_ok=True)
    for f in os.listdir(os.path.join(FDA, sub)):
        s = os.path.join(FDA, sub, f)
        d = os.path.join(src_dir, f)
        if not os.path.exists(d):
            import shutil
            shutil.copy2(s, d)
        # remove stale root copy in bundle if present
        root_copy = os.path.join(BUNDLE, "Fabric", "fabric-desktop-automation", f)
        if os.path.exists(root_copy):
            os.remove(root_copy)

m = json.load(open(MAN, encoding="utf-8"))
GOV = {"FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml", "FDA_INTEROP_DISPOSITION.yaml",
       "FDA_ROUTE_CHECK.yaml", "FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml"}
REC = {  # receipt set
    "FDA_C0_READBACK_RECEIPT.json", "FDA_C2_CUA_QUALIFICATION_RECEIPT.json",
    "FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json", "FDA_C3_UFO2_QUALIFICATION_RECEIPT.json",
    "FDA_C4_XQ_QUALIFICATION_RECEIPT.json", "FDA_C5_LEASE_CONCURRENCY_RECEIPT.json",
    "FDA_F01_LIVE_FIXTURE_RECEIPT.json", "FDA_F03_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F04_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F06_CLOSURE_V3_RECEIPT.json", "FDA_F06_CLOSURE_V4_RECEIPT.json",
    "FDA_F06_CLOSURE_V5_RECEIPT.json", "FDA_F06_CLOSURE_V6_RECEIPT.json",
    "FDA_F06_CLOSURE_V7_RECEIPT.json", "FDA_F06_CLOSURE_V8_RECEIPT.json",
    "FDA_F06_COMPILE_RECEIPT.json", "FDA_F06_COMPILE_TOOLBAR_RECEIPT.json",
    "FDA_F06_EXPORT_RECEIPT.json", "FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json",
    "FDA_F06_LIVE_FIXTURE_RECEIPT.json", "FDA_F06_SYSTEM_PATH_RECEIPT.json",
    "FDA_F06_TEN_RUN_RECEIPT.json", "FDA_F09_RADAR_RECEIPT.json",
    "FDA_F09B_PAPER_RUNTIME_RECEIPT.json", "FDA_F10_F11_READBACK_RECEIPT.json",
    "FDA_BOUNDED_CONTROL_LIVE_PROBE.json",
    "FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json", "FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
    "FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
}

changed = 0
for a in m["artifacts"]:
    base = os.path.basename(a["path"])
    if base in REC and "/evidence/receipts/" not in a["path"]:
        a["path"] = "Fabric/fabric-desktop-automation/evidence/receipts/" + base
        changed += 1
    elif base in GOV and "/governance/" not in a["path"]:
        a["path"] = "Fabric/fabric-desktop-automation/governance/" + base
        changed += 1

# rehash all from bundle bytes
for a in m["artifacts"]:
    p = os.path.join(BUNDLE, a["path"])
    if os.path.exists(p):
        data = open(p, "rb").read()
        a["sha256"] = hashlib.sha256(data).hexdigest()
        a["size"] = len(data)
    else:
        print("MISSING:", a["path"])

json.dump(m, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
mh = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
print(f"manifest paths updated: {changed} | entries: {m['artifact_count']} | sha: {mh}")

# verify all rows resolve
missing = [a["path"] for a in m["artifacts"] if not os.path.exists(os.path.join(BUNDLE, a["path"]))]
print("missing rows:", missing if missing else "(none)")
