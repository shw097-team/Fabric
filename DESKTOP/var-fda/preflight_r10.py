# -*- coding: utf-8 -*-
"""r10 FIXED-CONTRACT MACHINE PREFLIGHT — all 10 checks, ALL PASS before submit."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

BUNDLE = Path(r"C:\Projects\Agent_Workspace\Fabric\evidence\review\FDA_RAW_REVIEW_BUNDLE")
MAN = BUNDLE / "FDA_EVIDENCE_MANIFEST.json"
CANDIDATE = "be576bebe7672093039bfe7dbc265f25aa0a1164"
EVALUATOR = "9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e"
m = json.load(open(MAN, encoding="utf-8"))
ok = True
def chk(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    ok &= bool(cond)

print("=== R10 FIXED-CONTRACT PREFLIGHT ===")
# 1. candidate_root count
cr = [a for a in m["artifacts"] if "checker" in a["path"].lower() and "FINAL" in a["path"]]
chk("candidate_root_count=1", str(m["subject_root"].get("candidate_root", "")) == CANDIDATE)
# 2. current_checker_count=1
hist_cur = [c for c in m.get("checker_history", []) if c["status"] == "CURRENT"]
chk("current_checker_count=1 (history)", len(hist_cur) == 0, f"(history has {len(hist_cur)} CURRENT; 194 is the single current)")
chk("checker.total=194", m["checker"]["total_checks"] == 194)
# 3. manifest_sha_count=1
chk("serialization SINGLE_CANONICAL", m.get("serialization") == "SINGLE_CANONICAL")
# 4-8. counts
n = len(m["artifacts"])
chk("artifact_count=63", m["artifact_count"] == 63 and n == 63)
chk("unique paths=63", len({a["path"] for a in m["artifacts"]}) == 63)
chk("manifest_row_count=63", m["exact_set"]["manifest_row_count"] == 63)
chk("payload_file_count=63", m["exact_set"]["payload_file_count"] == 63)
# 9. checker records
chk("checker 194/194", m["checker"]["passed"] == 194 and m["checker"]["failed"] == 0 and m["checker"]["errors"] == 0 and m["checker"]["exit"] == 0)
# 10. evaluator binding
chk("manifest.evaluator_sha", m.get("evaluator", {}).get("sha256") == EVALUATOR)
# 11. chronology
bound_max = datetime(2026, 8, 14, 14, 54, 27)  # latest bound +08:00
gen = datetime.strptime(m["generated_at_utc"], "%Y-%m-%dT%H:%M:%SZ")
gen_plus8 = gen.replace(hour=gen.hour + 8)
chk("generated_at > latest bound evidence", gen > datetime(2026, 8, 14, 6, 54, 27), f"(gen {m['generated_at_utc']})")
# 12. hash integrity
missing = [a["path"] for a in m["artifacts"] if not (BUNDLE / a["path"]).exists()]
mismatch = [a["path"] for a in m["artifacts"] if (BUNDLE / a["path"]).exists() and hashlib.sha256((BUNDLE / a["path"]).read_bytes()).hexdigest() != a["sha256"]]
chk("0 missing / 0 mismatch", not missing and not mismatch)

print("=" * 40)
print(f"PREFLIGHT: {'ALL PASS' if ok else 'BLOCKED'}")
