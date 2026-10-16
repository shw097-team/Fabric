"""FAR run driver — R6R7 closure + R7 slice adjudication (far fabric-autonomous-research).

Uses the FAR router as the normative route input (governance/FAR_CAPABILITY_MATRIX.yaml) and emits the
R0-R8 run directory under Fabric/fabric-autonomous-research/runs/ per
research-product/RESEARCH_ARTIFACT_CONTRACTS.yaml.

Decision question (R0): of the items still open after the R6R7 archive round, which must be engineered now,
which need a human/owner gate, which are denominator work that should be sequenced, and should R7 start;
plus whether the three workspace-only closure records must be published into the repository.

Read-only apart from the FAR run directory. No credential material is read.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

FAR = Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research")
RUN_ID = "FAR-20261015-010-r6r7-closure-and-r7-slice"
OUT = FAR / "runs" / RUN_ID
sys.path.insert(0, str(FAR))

from far_router import route  # noqa: E402

REQ = {"challenge_required": True, "source_classes": ["pkg_authority", "prompt_brief", "external_review",
                                                       "repo_evidence", "hgk_machine_truth"],
       "network_requirement": "none", "credential_availability": "none"}
ROUTE = route("RESEARCH_LITERATURE_REPO", REQ)

SOURCES = [
    ("SRC-PKG", "pkg_authority", "required", "上位權威", "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md v2.0.0",
     "96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f", "READ"),
    ("SRC-PROMPT", "prompt_brief", "required", "Owner 指揮輸入", "R6 外部驗收後續作指揮薄 PROMPT.md v2",
     "b8526954b4ce9e0f70a387d19ebd5345e9a4bcd58686a9395b30e07537d1704d", "READ"),
    ("SRC-EIA", "external_review", "required", "外部獨立審查裁決", "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md",
     "10caf4dbdb1993cd46ff2c50394dd01dfd5f34d635816f95e3d2e5ab6c566206", "READ"),
    ("SRC-R6-PACKET", "repo_evidence", "required", "已發布封存證據", "EVIDENCE/CNV-PIPD-LS-SP-20261015 @ a10f7bea (main b8ff8104)",
     "581 blobs, manifest sha256 27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b", "READ"),
    ("SRC-R6-MUT", "repo_evidence", "required", "反例原始紀錄", "R6_DELIVERY/MUTATIONS_18.json",
     "10 executed / 7 detected / 3 not detected / 8 not run", "READ"),
    ("SRC-PIPD-SRC", "repo_evidence", "required", "bound validator 原始碼", "C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp/",
     "module path read-only inspection", "READ"),
    ("SRC-FAR", "pkg_authority", "required", "研究能力自身契約", "fabric-autonomous-research/AGENTS.md + RESEARCH_ARTIFACT_CONTRACTS.yaml + FAR_CAPABILITY_MATRIX.yaml",
     "route decision input", "READ"),
    ("SRC-HGK", "hgk_machine_truth", "required", "控制平面真相", "HG-KSEOS var/shared-spine/hg-kseos.db + config/lane-routing-registry.yaml",
     "epoch 19; candidate-only", "READ"),
]

CLAIMS = [
    ("CL-01", "M04/M06/M16 的反例不是測試資料問題，而是 bound validator 缺少三類 predicate（profile assurance 綁定、oracle expected 綁定、trace digest 重算）", "HIGH",
     "R6_DELIVERY/RUNNERS/probe_mutations.py:84-175 皆以 report['verdict']=='FAIL' 判定；三個未偵測案例的 tamper 不在 validator 檢核面"),
    ("CL-02", "這三類漏拒會讓後續任何「獨立驗收」在假綠基礎上成立，因此優先序高於 221 live 全跑", "HIGH",
     "EIA §4.1 HIGH 級局部反例；EIA §7 將 M04/M06/M16 列為 P0（下次正式安全/Runtime Admission 前）"),
    ("CL-03", "checker 可寫 candidate root 是權限防線失效而非模型選擇問題", "HIGH", "EIA §4.2 明示『模型／lane 名稱 ≠ filesystem least-privilege』；R6 attempt 3 實測寫入"),
    ("CL-04", "已合併的 R6 封存必須保持 byte-stable，新紀錄不得回寫既有 prefix", "MEDIUM",
     "R6R7_POST_COMMIT_READBACK.json 已把 581 blob id 綁定在 main；回寫會使既有外部讀回失效"),
    ("CL-05", "三個 workspace-only 收據若只存在 PR 留言，外部驗收官的驗收輸入不可重現", "MEDIUM",
     "指揮薄 §9 要求「最後的 HEAD/SHA/驗證結果存外部 PR receipt／comment 或 separate signed evidence」；檔案化可重現性更高"),
    ("CL-06", "221 live 全跑在本輪屬於過度工程：在適用性未簽核前全跑會產生假 PASS/假 FAIL", "MEDIUM", "EIA §5「不適用者須以已核定的理由…聲明 N/A」"),
    ("CL-07", "Fresh G1／DOC-05／AO 是人力授權閘門，任何自動化模型都不能代替", "HIGH", "EIA §9 M3 與 §10 分層裁決；KP01 authority"),
]

CONTRADICTIONS = [
    ("CT-01", "EIA §9 允許不必等 221/8 Gate 即可合併，EIA §5 又要求 221 每個 ID 必須有完整去向",
     "不衝突：前者管 evidence-only merge，後者管正式 Convergence；但需以『適用性簽核』把兩者接起來，否則 221 永遠處於無去向狀態"),
    ("CT-02", "指揮薄 §4 允許本輪推送與 PR 更新，但 M3 為一次性、綁特定 head 的授權",
     "以新前綴＋新分支＋新 PR 取得新的單一 prefix 授權即可，不需改寫舊授權範圍"),
]

REJECTED = [
    ("RA-01", "把三個收據直接 push 進已合併的 EVIDENCE/CNV-PIPD-LS-SP-20261015/", "破壞已綁定的 byte-stable 封存與既有外部讀回"),
    ("RA-02", "建立第二控制平面／新 DB／常駐 CI 服務來承載 R7 驗證", "過度工程，且 EIA §7 已明確 N/A 否決"),
    ("RA-03", "本輪一次跑完 221 live + G-A..H + AUD-24", "高成本、低邊際價值；在適用性簽核前結果不可信"),
    ("RA-04", "由 maker 自行重跑並自簽 R7 修正的驗收", "違反 SoD；EIA §8 要求 maker ≠ checker"),
    ("RA-05", "把 checker 隔離僅以 lane 名稱／模型名稱完成", "EIA §4.2 已證否；必須以檔案系統層拒絕為證據"),
]

OPENQ = [
    ("OQ-01", "221 個 ID 的適用性簽核由哪個 Domain/Gate Owner 出具，N/A 的格式為何？", "R7-07"),
    ("OQ-02", "source #6 屬於 active normative 或 historical archive，需 Owner 裁決，裁決後 PI/PD 分母如何重算？", "R7-01"),
    ("OQ-03", "checker 的隔離 write root 應落在哪個受治理路徑，才能同時滿足 OS ACL 與證據可讀？", "R7-03"),
    ("OQ-04", "20 條 KP *-R04 極性修正由 KP Policy Owner 出具後，是否需對既有 gate 重跑 cross-KP 負測？", "R7-08"),
]

ADJUDICATION = {
    "verdict": "PARTIAL",
    "q1_unclosed_items": {
        "P0_engineer_now": [
            {"item": "R7-02 validator hardening: M04 (ProfileBinding ASSURED->LITE), M06 (domain oracle expected 999), M16 (trace atom digest mismatch) 必須 REJECT",
             "why": "三個實跑反例目前被 ACCEPT；這些漏拒會使後續所有獨立驗收建立於假綠之上（EIA §4.1 HIGH、§7 P0）",
             "cost": "低（bound validator 加三類 predicate + 以既有 driver 重跑 M01..M18）", "risk_if_skipped": "假綠、gate 誤放行"},
            {"item": "R7-03 checker SoD: candidate root 於驗證期間不可寫；verifier/temp 置於隔離 write root，並以實際 write-denial 為證據",
             "why": "R6 attempt 3 實測 checker 可寫 candidate root；EIA §4.2 明示 lane/模型名稱不構成 least-privilege",
             "cost": "中（runner 層 write-root 約束 + denial fixture）", "risk_if_skipped": "證據污染、INDEPENDENT_PASS 不可成立"}],
        "owner_human_gate": [{"item": "Fresh G1（declared 0.20.0 vs observed 0.21.5 重認證）", "gate": "Human Owner"},
                             {"item": "DOC-05 effect Admission、AO verdict、Release", "gate": "AO / Release Owner"}],
        "denominator_sequenced": [{"item": "221 cases / G-A..G-H / AUD-24 / 18 PI-10 PD-64-129 trace", "approach": "先出適用性簽核（applicable vs lawful N/A），再對 applicable 抽樣真跑，最後才全量；不對未簽核分母跑測試"},
                                  {"item": "checker/dispatcher 通道（nonce、timeout partial stdout+stderr、long-prompt file/stdin）", "approach": "與 R7-04 合併成單一 ChangeSet"}],
        "documentation_fix": [{"item": "20 條 KP *-R04 極性缺陷", "owner": "KP Policy Owner", "note": "先隔離自動匯入，已在本輪 contract 以 QUARANTINE 記錄"},
                              {"item": "source #6 active vs historical", "owner": "PIPD Source Owner"},
                              {"item": "94>60 refs", "note": "維持 soft warning，不得升硬門（ACC-RQ08）"}],
        "tooling_defects_recorded": [{"item": "HGK taskspec id = project_id 末段 → 跨專案 UNIQUE 碰撞；workorder 准入讀 ambient cwd 的 git HEAD", "owner": "HGK Lifecycle Owner"},
                                     {"item": "dispatcher ERR_NO_ARM_EMITTED_NONCE（nonce 走 agent_message 通道）", "owner": "HGK Lane Owner"}],
        "no_action_recorded": ["8 個 NOT_RUN mutations 維持 NOT_RUN", "R6 失敗 receipts 與 checker 暫態寫入事件維持原樣記錄"],
    },
    "q2_start_r7": {"decision": "YES — 以有界 slice 開跑", "slice": "R7-0 = R7-02 + R7-03（P0 兩項）",
                    "not_this_round": "R7-01/04/05/06/07/08/09 立 TaskSpec/Issue，不本輪執行",
                    "why": "唯二會使後續驗收失去意義的路徑；其餘項目成本高且不改變本輪結論，一次全做即過度工程（EIA §7 N/A）"},
    "q3_publish_workspace_files": {"decision": "YES — 以新前綴發布，不回寫已合併封存",
        "shape": "新分支 + Draft PR，prefix EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/，內含 R6R7 closure 三收據（讀回、合併結算、M3 核准＋final-head 掃描）、FAR 研究產物、R7-0 的 writer/checker 證據",
        "why": "外部驗收官的驗收輸入必須存在於 REPO 內且可重現；PR 留言易失且非版本化",
        "authority": "需 Owner 對新 prefix 的單一授權（本次訊息已授權執行；紀錄為 Owner 授權）"},
}

PLAN = {
    "subquestions": ["哪些未閉合項必須現在工程化", "R7 是否開跑、以何種 slice", "workspace-only 收據是否需入 REPO"],
    "claim_classes": ["engineering_necessity", "authority_gate", "denominator_sequencing", "reproducibility"],
    "source_classes": ["pkg_authority", "prompt_brief", "external_review", "repo_evidence", "hgk_machine_truth"],
    "query_strategy": ["唯讀定位既有 artifact 與原始碼", "以 R6 原始紀錄交叉比對 EIA 裁決", "以 HGK machine truth 驗證准入與車道"],
    "candidate_methods_providers": [ROUTE["primary"]] + ([ROUTE["challenger"]] if ROUTE.get("challenger") else []),
    "challenge_trigger": ["challenge_required=True → 對每個建議提出對立論證並記錄處置"],
    "experiment_trigger": ["不需要新的世界效應實驗；以既有 R6 原始紀錄 + 重跑 mutation driver 為實驗面"],
    "stop_criteria": ["三題皆有可執行結論且每一建議有成本/風險/最小修補"],
    "abstain_criteria": ["若 bound validator 位址不可唯讀確認 → 對 R7-02 宣告 ABSTAIN 並改立 OpenQuestion"],
    "budget_allocation": {"read_only_sources": 8, "lane_runs": "writer 1 + checker 1"},
}


def write(rel: str, text: str) -> None:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    write("ResearchRequest.yaml", "\n".join([
        "schema: LOGICAL_FAR_RESEARCH_REQUEST_V1",
        f"run_id: {RUN_ID}",
        "workorder_ref: {id: WO-TS-R6ARC2-01, digest: see HGK_TYPED_ADMISSION_R6R7.json, note: R6R7 narrow-repair admission}",
        "decision_question: >- 本輪未閉合項中哪些必須立即工程化、R7 是否開跑、以及三個 workspace-only 收據是否必須發布進 REPO",
        "owner: human owner (shw097-team)",
        "task_class: RESEARCH_LITERATURE_REPO",
        "source_requirements: [pkg_authority, prompt_brief, external_review, repo_evidence, hgk_machine_truth]",
        "freshness_requirement: as-of 2026-10-15 (Asia/Taipei)",
        "budget_ref: local, no external spend",
        "security_boundary_ref: read-only; no credential material read; packet content never executed",
        "expected_decision_output: CandidateResearch + ProposedEvolution (execution plan) for the owner",
        ""]))
    write("ResearchPlan.yaml", "schema: LOGICAL_FAR_RESEARCH_PLAN_V1\n" + "\n".join(
        f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in PLAN.items()) + "\n")
    write("ResearchSourceDenominator.tsv", "source_id\tsource_class\trequirement\tauthority_role\tidentity_locator\tsnapshot_digest_or_locator\taccess_status\tdisposition\treason\n"
          + "\n".join("\t".join([s[0], s[1], s[2], s[3], s[4], s[5], s[6], "USED", "reviewed and cited in the ledgers"]) for s in SOURCES) + "\n")
    write("SourceSnapshotLedger.tsv", "source_id\tidentity_locator\tsnapshot_digest\n"
          + "\n".join("\t".join([s[0], s[4], s[5]]) for s in SOURCES) + "\n")
    write("SourceDispositionLedger.tsv", "source_id\tdisposition\treason\n"
          + "\n".join("\t".join([s[0], "ACCEPTED_AS_EVIDENCE", s[3]]) for s in SOURCES) + "\n")
    write("ClaimLedger.tsv", "claim_id\tclaim\tconfidence\tevidence_ref\n"
          + "\n".join("\t".join(c) for c in CLAIMS) + "\n")
    write("ContradictionLedger.tsv", "id\tapparent_contradiction\tresolution\n"
          + "\n".join("\t".join(c) for c in CONTRADICTIONS) + "\n")
    write("RejectedAlternativeLedger.tsv", "id\talternative\treason_rejected\n"
          + "\n".join("\t".join(r) for r in REJECTED) + "\n")
    write("OpenQuestionLedger.tsv", "id\topen_question\towner_route\n" + "\n".join("\t".join(o) for o in OPENQ) + "\n")
    write("HypothesisLedger.tsv", "id\thypothesis\tstatus\n"
          "H-01\tM04/M06/M16 為 validator predicate 缺口而非資料問題\tSUPPORTED\n"
          "H-02\t重寫已合併封存可提升可驗性\tREJECTED\n"
          "H-03\t221 全跑是本輪最高價值動作\tREJECTED\n")
    write("DisagreementLedger.tsv", "id\tdisagreement\tresolution\n"
          "D-01\tmaker 傾向『先把 221 全跑』；FAR 認為那是過度工程且結果不可信\t以適用性簽核為前置，先做 P0 兩項\n")
    write("ExperimentPlan.yaml", "schema: LOGICAL_FAR_EXPERIMENT_PLAN_V1\nexperiments:\n"
          "  - id: E-01\n    what: 以既有 RUNNERS/run_mutations.py driver 重跑 M01..M18\n"
          "    pass_condition: M04/M06/M16 由 ACCEPT 變為 REJECT，且原 7 個 detected 維持 REJECT\n"
          "    executed_by: Codex CLI EXECUTE lane (bounded writer)\n    verified_by: Codex CLI VERIFY/SECURITY lane (independent)\n")
    write("ResearchSynthesis.md", f"""# FAR synthesis — {RUN_ID}

## Route decision
- task_class `RESEARCH_LITERATURE_REPO` → primary `{ROUTE['primary']}`，reason `{ROUTE['reason_code']}`，
  challenger `{ROUTE.get('challenger')}` / method `{ROUTE.get('challenger_method')}`（challenge_required=True）。
- FAR router 依 FAR_CAPABILITY_MATRIX.yaml 決定路徑；本 run 不新增第二套流程。

## Adjudication (verdict {ADJUDICATION['verdict']})
1. **必須現在工程化（P0）**：R7-02 validator hardening（M04/M06/M16 必拒收）與 R7-03 checker 檔案系統層隔離。
   兩者共通的性質是「一旦缺失，之後所有驗收都可能建立在假綠與被污染的證據上」，因此優先於任何分母工作。
2. **人力閘門（不可自動化）**：Fresh G1、DOC-05 effect Admission、AO、Release。
3. **分母工作需先簽核適用性**：221 / G-A..G-H / AUD-24 / trace 圖譜；先 applicable vs lawful N/A，再抽樣真跑，最後全量。
4. **文件與政策缺陷**：KP `*-R04` 極性（已隔離）、source #6 裁決、94>60 維持 warning。
5. **工具鏈缺陷記錄**：HGK taskspec id 尾段碰撞＋ambient cwd、dispatcher nonce 通道。

## Answers to the three questions
- Q1 未閉合項：見 `CandidateResearch.yaml` 的 P0 / human-gate / sequenced / doc-fix 四類，每項附成本、風險與最小修補。
- Q2 R7：**開跑，但只有 R7-0 = R7-02 + R7-03**；其餘立 TaskSpec 不本輪執行。
- Q3 三個 workspace-only 收據：**必須進 REPO**，但以**新前綴**發布（`EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/`），
  已合併的封存不回寫，維持 main 上 581 blob 的 byte-stability 與既有外部讀回的有效性。

## Rejected alternatives
見 `RejectedAlternativeLedger.tsv`（回寫舊前綴、建第二控制平面、221 全跑、maker 自簽、以 lane 名稱代替隔離）。

## Confidence and limits
- 高信心：P0 兩項的必要性與最小修補形狀（直接由 R6 原始碼與 EIA 裁決交叉得出）。
- 中信心：適用性簽核的格式與 owner 指派（列 OpenQuestion OQ-01）。
- 本 run 的輸出是 **CandidateResearch / ProposedEvolution**，不是接受、不是 promotion。
""")
    write("CandidateResearch.yaml", "schema: LOGICAL_FAR_CANDIDATE_RESEARCH_V1\nclaim_level: LOCAL\n"
          + json.dumps({"run_id": RUN_ID, "route": ROUTE, "adjudication": ADJUDICATION}, ensure_ascii=False, indent=2) + "\n")
    write("ProposedEvolution.yaml", "schema: LOGICAL_FAR_PROPOSED_EVOLUTION_V1\ncandidate_only: true\n"
          + json.dumps({"change_set": "R7-0-VALIDATOR-AND-CHECKER-ISOLATION",
                        "workorders_proposed": [
                            {"id": "WO-R7-VALHARD", "writer": "Codex CLI EXECUTE lane (opencode-go/deepseek-v4.1-flash)",
                             "scope": "PIPD bound validator: reject M04/M06/M16 tamper classes",
                             "writeset": "C:/Projects/Agent_Workspace/PIPD/src/pipd_ls_sp/** + R7-0 handover evidence",
                             "evidence": ["R7_MUTATIONS_18_RERUN.json", "R7_WRITE_SET.json", "R7_WRITER_RECEIPT.json", "raw stdout"]},
                            {"id": "WO-R7-CHECKDENY", "writer": "HGK runner configuration (no product change)",
                             "scope": "checker write root isolation + denial fixture",
                             "evidence": ["R7_CHECKER_DENIAL.json"]}],
                        "checker_route": "Codex CLI VERIFY/SECURITY lane (opencode-go/glm-5.3-flash), independent",
                        "publication": "new branch + Draft PR, prefix EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/",
                        "rollback": "revert the PR merge commit or drop the branch; product change reverted in its own worktree",
                        "claim_ceiling": "LOCAL / candidate-only"}, ensure_ascii=False, indent=2) + "\n")
    write("ResearchHandoff.yaml", "schema: LOGICAL_FAR_RESEARCH_HANDOFF_V1\nto: owner (shw097-team)\n"
          "decisions_requested:\n  - approve the R7-0 slice (R7-02 + R7-03) for execution\n"
          "  - approve the new evidence prefix EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/ for publication\n"
          "explicitly_not_granted: [production release, AO verdict, claim upgrade]\n")
    files = sorted(p for p in OUT.rglob("*") if p.is_file())
    receipt = {"schema": "FAR-RESEARCH-RUN-RECEIPT/1", "run_id": RUN_ID, "route": ROUTE,
               "artifacts": [{"path": str(p.relative_to(OUT)).replace("\\", "/"), "bytes": p.stat().st_size,
                              "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
               "verdict": ADJUDICATION["verdict"], "claim_ceiling": "LOCAL / candidate-only",
               "note": "candidate research product for the owner; never an acceptance"}
    (OUT / "ResearchRunReceipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_dir": str(OUT), "artifacts": len(receipt["artifacts"]), "route": ROUTE}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
