# -*- coding: utf-8 -*-
"""Post-reseal verification (external-recompute-equivalent)."""
import hashlib
import json
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
m = json.load(open(MAN, encoding="utf-8"))
sha = hashlib.sha256(open(MAN, "rb").read()).hexdigest()
ok = True

print("=== POST-RESEAL VERIFICATION ===")
print(f"manifest SHA: {sha}")

# 1. derived count invariant
c1 = m.get("artifact_count"); c2 = len(m["artifacts"])
print(f"count derived: field={c1} actual={c2} -> {'PASS' if c1 == c2 else 'FAIL'}")
ok &= c1 == c2

# 2. all artifacts exist + hash match
missing = [a["path"] for a in m["artifacts"] if not (BUNDLE / a["path"]).exists()]
mismatch = []
for a in m["artifacts"]:
    p = BUNDLE / a["path"]
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() != a["sha256"]:
        mismatch.append(a["path"])
print(f"missing: {len(missing)} | mismatch: {len(mismatch)} -> {'PASS' if not missing and not mismatch else 'FAIL'}")
ok &= not missing and not mismatch

# 3. checker single current 194
cur = [c for c in m.get("checker_history", []) if c["status"] == "CURRENT"]
ck = m.get("checker", {})
print(f"history CURRENT entries: {len(cur)} (expect 0) | checker total: {ck.get('total_checks')} (expect 194) -> {'PASS' if not cur and ck.get('total_checks') == 194 else 'FAIL'}")
ok &= not cur and ck.get("total_checks") == 194

# 4. no stale RR4 version remnant / no e7b2894 in CURRENT identity fields (history subjects may cite old HEADs legitimately)
txt = json.dumps(m, ensure_ascii=False)
stale_version = "FINAL_RR4" in txt
current_identity = json.dumps({"sr": m.get("subject_root"), "ck": m.get("checker")}, ensure_ascii=False)
stale_subject = "e7b2894" in current_identity
print(f"stale RR4 version: {'FOUND -> FAIL' if stale_version else 'none -> PASS'}")
print(f"e7b2894 in current identity: {'FOUND -> FAIL' if stale_subject else 'none (history-only) -> PASS'}")
ok &= not stale_version and not stale_subject

# 5. subject binding
sb = m["subject_root"]["git_head"]
print(f"subject: {sb[:12]} (expect be576be) -> {'PASS' if sb.startswith('be576be') else 'FAIL'}")
ok &= sb.startswith("be576be")

# 6. unique paths
paths = [a["path"] for a in m["artifacts"]]
dups = len(paths) - len(set(paths))
print(f"unique paths: {len(set(paths))}/{len(paths)} dups={dups} -> {'PASS' if dups == 0 else 'FAIL'}")
ok &= dups == 0

print("=" * 40)
print(f"RESEAL VERIFICATION: {'ALL PASS' if ok else 'BLOCKED'}")
