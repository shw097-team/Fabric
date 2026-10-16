# -*- coding: utf-8 -*-
"""far_gate_check.py — HGK Step 10A Gate 1 程式化執行器（FAR research gate enforcement）。
任何升級/patch/自進化提案提交給用戶前，必須先跑本檢查器產生 Gate 1 receipt；
無 receipt 的提案不得作為「建議」提交（Gate 2 阻擋）。

用法：
  python far_gate_check.py --proposal "<提案描述>" [--output <receipt.json>]

Gate 1 receipt 欄位：
  - proposal_hash
  - three_source_check（三源取證：on-disk assets / callable skills / fresh context — 必須真實調查）
  - challenge_lane（反方挑戰）
  - research_verdict（CONFIRMS_USEFUL / REJECTS / REQUIRES_CONDITION）
  - gate2_user_submission_allowed
"""
import hashlib
import json
import sys
from datetime import datetime, timezone

def main():
    args = sys.argv[1:]
    if "--proposal" not in args:
        print('usage: far_gate_check.py --proposal "<proposal>" [--output <receipt.json>]')
        sys.exit(2)
    prop = args[args.index("--proposal") + 1]
    out = None
    if "--output" in args:
        out = args[args.index("--output") + 1]

    ph = hashlib.sha256(prop.encode("utf-8")).hexdigest()[:16]
    receipt = {
        "gate": "UD-FAR-RESEARCH-GATE-2026-08-14-001",
        "proposal": prop,
        "proposal_hash": ph,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "three_source_check": {
            "source1_on_disk_assets": "",
            "source2_callable_skills": "",
            "source3_fresh_context": "",
        },
        "challenge_lane": "",
        "research_verdict": "PENDING",
        "evidence_refs": [],
        "gate2_user_submission_allowed": False,
    }
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(receipt, f, ensure_ascii=False, indent=2)
        print(f"Gate 1 receipt template: {out}")
        print(f"proposal_hash: {ph}")
        print("REMINDER: fill three_source_check + challenge_lane with REAL investigation;")
        print("verdict CONFIRMS_USEFUL required before Gate 2 user submission.")
    else:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
