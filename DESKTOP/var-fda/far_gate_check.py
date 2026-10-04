# -*- coding: utf-8 -*-
"""far_gate_check.py — HGK Step 10A Gate 1 程式化執行器（FAR research gate enforcement）。
任何升級/patch/自進化提案提交給用戶前，必須先跑本檢查器產生 Gate 1 receipt；
無 receipt 的提案不得作為「建議」提交（Gate 2 阻擋）。

用法：
  python far_gate_check.py --proposal "<提案描述>" [--output <receipt.json>]

輸出（Gate 1 receipt）：
  - proposal_hash
  - three_source_check: 三源取證（on-disk assets / callable skills / fresh context）
  - challenge_lane: 挑戰面（反方論點）
  - research_verdict: CONFIRMS_USEFUL / REJECTS / REQUIRES_CONDITION
  - evidence_refs
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

def main():
    args = sys.argv[1:]
    if "--proposal" not in args:
        print("usage: far_gate_check.py --proposal \"<proposal>\" [--output <receipt.json>]")
        sys.exit(2)
    prop = args[args.index("--proposal") + 1]
    out = None
    if "--output" in args:
        out = args[args.index("--output") + 1]

    ph = hashlib.sha256(prop.encode("utf-8")).hexdigest()[:16]

    # 三源取證模板（執行者必須以真實調查填寫，不可留空）
    receipt = {
        "gate": "UD-FAR-RESEARCH-GATE-2026-08-14-001",
        "proposal": prop,
        "proposal_hash": ph,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "three_source_check": {
            "source1_on_disk_assets": "",   # 檢查現有 asset（藍圖/skill/腳本）是否已覆蓋
            "source2_callable_skills": "",  # 檢查可呼叫 skill 是否已規範
            "source3_fresh_context": "",    # fresh-context 驗證（不憑記憶）
        },
        "challenge_lane": "",
        "research_verdict": "PENDING",      # CONFIRMS_USEFUL / REJECTS / REQUIRES_CONDITION
        "evidence_refs": [],
        "gate2_user_submission_allowed": False,
    }

    if out:
        Path(out).write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Gate 1 receipt template: {out}")
        print(f"proposal_hash: {ph}")
        print("REMINDER: fill three_source_check + challenge_lane with REAL investigation;")
        print("verdict CONFIRMS_USEFUL required before Gate 2 user submission.")
    else:
        print(json.dumps(receipt, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
