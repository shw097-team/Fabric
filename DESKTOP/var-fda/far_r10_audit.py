# -*- coding: utf-8 -*-
"""FAR source: current manifest exact_set + all bound evidence timestamps (for chronology fix)."""
import json
import re
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
m = json.load(open(MAN, encoding="utf-8"))

print("=== current manifest ===")
print(f"artifact_count: {m.get('artifact_count')}")
print(f"len(artifacts): {len(m.get('artifacts', []))}")
print(f"exact_set: {json.dumps(m.get('exact_set'), ensure_ascii=False) if m.get('exact_set') else 'MISSING'}")
print(f"generated_at_utc: {m.get('generated_at_utc')}")
print(f"generated_at: {m.get('generated_at')}")
print(f"keys: {sorted(m.keys())}")
print(f"evaluator field: {json.dumps(m.get('evaluator'), ensure_ascii=False) if m.get('evaluator') else 'MISSING'}")

# all bound evidence timestamps — scan receipts for generated_at/created
print("\n=== bound evidence timestamps (max wins) ===")
rec_dir = Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\evidence\receipts")
for f in sorted(rec_dir.glob("*.json")):
    try:
        d = json.load(open(f, encoding="utf-8"))
        ts = d.get("generated_at") or d.get("generated_at_utc") or ""
        if ts:
            print(f"  {f.name}: {ts}")
    except Exception:
        pass

# checker final receipt timestamp
print("\n=== checker final ===")
try:
    ck = json.load(open(rec_dir / "FDA_CHECKER_FINAL_RR7.json", encoding="utf-8"))
    print(f"  script_sha256: {ck.get('script_sha256')}")
    print(f"  generated_at_utc: {ck.get('generated_at_utc')}")
except Exception as e:
    print("  err", e)
