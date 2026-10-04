# -*- coding: utf-8 -*-
"""FAR research execution — Gate 1 complete receipt for the fda_run.py-in-blueprint proposal.
Fills the template with REAL three-source investigation (done above)."""
import hashlib
import json
import time
from datetime import datetime, timezone

proposal = "把「fda_run.py 為唯一執行路徑」寫進 fabric-desktop-automation 藍圖執行面"
ph = hashlib.sha256(proposal.encode("utf-8")).hexdigest()[:16]

receipt = {
    "gate": "UD-FAR-RESEARCH-GATE-2026-08-14-001",
    "proposal": proposal,
    "proposal_hash": ph,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "three_source_check": {
        "source1_on_disk_assets": (
            "藍圖 STEP 6 = CANONICAL DESKTOP CAPABILITY MATRIX（能力矩陣），不是執行面；"
            "執行面為 STEP 7 EXECUTION BINDING / STEP 9 XQ PAPER fixtures。"
            "藍圖本體在 知識庫/實作相關DOC/FDA/（不在 Fabric repo，git 無追蹤）。"
            "並行 session 已重組目錄（DOC/evidence/governance，HEAD 34fbbd3，RR3-RR5 閉環 + Step 6B primary-home gate）。"
            "藍圖 STEP 7 尚未記載 fda_run.py。"
        ),
        "source2_callable_skills": (
            "fda-desktop-automation skill §2.2 已規範「所有 FDA 自動化腳本必須經 fda_run.py 執行」"
            "（含 preflight guard BLOCK + 異常自動 screen_state_check）— skill 層已覆蓋，"
            "且 skill 是操作時載入的權威；HGK §15 已標 LOCATION NOTE 指向 FDA skill。"
        ),
        "source3_fresh_context": (
            "fda_run.py 三測試實測通過（違規 BLOCK / 乾淨執行 / 異常自動查螢幕）；"
            "主目錄 47 違規腳本已隔離；screen_state_check 落實率從 0.3% 起由 fda_run.py 機械強制。"
            "但 agent 是否『實際經 fda_run.py』執行尚無長期觀察數據（機制存在，使用率未驗證）。"
        ),
    },
    "challenge_lane": (
        "反方：藍圖層再寫一次 fda_run.py 規範 = 重複文字規則（skill 已有），不增加機械強制；"
        "且藍圖本體在知識庫（非 repo），寫入無版本管控（git 不追蹤）→ 更新脆弱。"
        "反方：'唯一執行路徑'若寫死在藍圖，但未來有其他執行器（cua wrapper / 工具整合）會過度限制。"
        "正方：藍圖是 acceptance contract（外部驗收官讀藍圖），記載可讓驗收檢查表引用；"
        "但外部 r2 裁決是 evidence-only smallest repair，不要求藍圖新增條款。"
    ),
    "research_verdict": "REQUIRES_CONDITION",
    "condition": (
        "不立即寫入藍圖。先行：① 讓 agent 實際以 fda_run.py 執行 FDA 腳本 ≥3 天並觀察使用率；"
        "② 若使用率達標（無繞過），再以 WO 提案寫入藍圖 STEP 7 EXECUTION BINDING 的 runtime 段"
        "（非 STEP 6，位置已更正）；③ 藍圖若寫入須同步鏡像到知識庫並納入版本控制。"
        "skill §2.2 規範維持現狀（已覆蓋操作層）。"
    ),
    "gate2_user_submission_allowed": True,  # 條件式建議：現階段不寫藍圖，觀察後再議
    "evidence_refs": [
        "知識庫/實作相關DOC/FDA/fabric-desktop-automation_藍圖_v2026.08.13-r2.md STEP 6/7/9",
        "skill fda-desktop-automation §2.2",
        "HGK skill Step 10A (UD-FAR-RESEARCH-GATE-2026-08-14-001)",
        "fda_run.py 3-test live results (2026-08-14)",
        "Fabric git HEAD 34fbbd3 (parallel session RR3-RR5)",
    ],
}

out = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\fda\FAR_GATE1_RECEIPT_fdarun_blueprint.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(receipt, f, ensure_ascii=False, indent=2)
print("Gate 1 receipt written:", out)
print("verdict:", receipt["research_verdict"])
print("proposal_hash:", ph)
