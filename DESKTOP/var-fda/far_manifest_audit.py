# -*- coding: utf-8 -*-
"""FAR source-1: audit current manifest for the exact stale metadata the external reviewer flagged:
- '54' vs actual artifact count mismatch
- old checker history 'current' flags
- multiple different serialization SHAs"""
import hashlib
import json
from pathlib import Path

MAN = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE\FDA_EVIDENCE_MANIFEST.json")
m = json.load(open(MAN, encoding="utf-8"))
raw = MAN.read_bytes()

print("=== CURRENT MANIFEST AUDIT ===")
print(f"file sha256: {hashlib.sha256(raw).hexdigest()}")
print(f"artifact_count field: {m.get('artifact_count')}")
print(f"actual len(artifacts[]): {len(m.get('artifacts', []))}")
print(f"subject_root: {m.get('subject_root')}")

# 1. 54 mismatch — search all '54' references in manifest
txt = json.dumps(m, ensure_ascii=False)
import re
for pat in ["54", "b07d5d81", "reducer", "manifest_self", "checker_history"]:
    hits = [ln.strip()[:90] for ln in txt.splitlines() if pat in ln]
    if hits:
        print(f"\n--- '{pat}' occurrences ({len(hits)}) ---")
        for h in hits[:5]:
            print("  ", h)

# 2. old checker history current flags
print("\n=== checker-related keys ===")
for k, v in m.items():
    if "checker" in str(k).lower():
        print(f"  {k}: {str(v)[:120]}")

# 3. multiple serialization SHAs — look for any sha fields in the body
print("\n=== embedded sha-like fields ===")
shas = re.findall(r'[0-9a-f]{64}', txt)
from collections import Counter
cnt = Counter(shas)
print(f"total 64-hex strings: {len(shas)} | unique: {len(cnt)}")
for s, n in cnt.most_common(6):
    print(f"  {s[:16]}... x{n}")
