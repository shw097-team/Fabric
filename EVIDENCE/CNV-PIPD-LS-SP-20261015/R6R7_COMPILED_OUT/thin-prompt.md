# EXECUTABLE THIN CONSTRUCTION & ACCEPTANCE PROMPT

## 0. Machine Header
task_id: CNV-PIPD-LS-SP-20261015-R6R7
contract_schema: CAPC-PROMPT-CONTRACT/1
compiler_state: PROMPT_COMPILE_PASS

## 1. Mission / ChangeSet
Mission: 依外部獨立驗收報告 EIA-FABRIC-CONVERGENCE-R6-20261015 的三個合併關卡（M1 manifest/currentness、M2 可信範圍與秘密掃描、M3 維護者 prefix 授權），對既有 PR #3 的 R6 候選證據包做最小、就地的發布修補並交付可獨立查驗的 Draft PR；不重跑 221、不改產品、不自行驗收、不代簽 AO/Release。
Expected outcome: 既有 PR #3 分支上一個 tracked_inventory 與實際 Git tree 完全一致、local-only 2 檔被明確標示、發布記錄不再自稱舊 HEAD/569-published 的證據包；外加可信 scope/secret 掃描結果、Maintainer prefix 授權紀錄、以及 POST-commit 的外部 readback。
ChangeSet: NARROW_REPAIR
Affected domains: Fabric GitHub projection: EVIDENCE/CNV-PIPD-LS-SP-20261015/** publication metadata

## 2. Authority / Files-first order
Read and hash the exact sources below in order. Use their owned controls directly; do not restate or replace them.
- A0 C:\Projects\Agent_Workspace\_handover\CNV-PIPD-LS-SP-20261015\OWNER_TRUST_LOCK.json C:\Projects\Agent_Workspace\_handover\CNV-PIPD-LS-SP-20261015\OWNER_TRUST_LOCK.json role=NORMATIVE
- A0-OWNER-INPUT C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric × Hermes × HG-KSEOS｜R6 外部驗收後續作指揮薄 PROMPT.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric × Hermes × HG-KSEOS｜R6 外部驗收後續作指揮薄 PROMPT.md role=NORMATIVE
- A0-OWNER-DELIVERED-REVIEW C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md role=SUPPORT
- A3 C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\attachments\Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md head role=NORMATIVE
- A1 C:\Projects\Agent_Workspace\HG-KSEOS\AGENTS.md module root role=NORMATIVE
- A6 C:\Projects\Agent_Workspace\Fabric\AGENTS.md policy/contracts role=SUPPORT
- A5 C:\Projects\Agent_Workspace\知識庫\實作相關DOC\HG-KSEOS\construction-acceptance-prompt-compiler references/prompt-contract.schema.json role=NORMATIVE
- A7-PROJECTION https://github.com/shw097-team/Fabric/pull/3 EVIDENCE/CNV-PIPD-LS-SP-20261015/ role=SUPPORT
Equal-rank conflict => quarantine, TT, and stop the affected work.

## 3. Intent / Non-goals / Claim ceiling
Expected experience: 由本地受治理執行器一次跑完 M1→M2→M3 準備→推送→readback；缺任一權威/權限時回傳精確 blocker 與 checkpoint，不反覆詢問已提供的來源。
Constraints:
- HG-KSEOS 唯一控制平面；Hermes 為受治理 runtime；Codex 為 admitted bounded writer；GitHub 只是投影鏡像
- PLAN & Orchestrator = opencode-go/glm-5.3-flash；EXECUTE = Codex CLI opencode-go/deepseek-v4.1-flash；VERIFY/SECURITY = Codex CLI opencode-go/glm-5.3-flash
- 只准變更遠端前綴 EVIDENCE/CNV-PIPD-LS-SP-20261015/**；不得觸碰 main、HG-KSEOS/、FABRIC/、.github/workflows/、secrets、canonical DB
- 不得加入兩個 .pyc；不得刪除或改寫 R6 失敗 receipts；不得對未改過的候選碼重跑 221 或宣稱八 Gate PASS
- Maker≠Checker≠AO；本輪不得自行核准（M3 屬 Maintainer/Owner）
- token 不得出現在模型脈絡、argv、URL、log、PR、.git/config 或 evidence；且不得執行 PR 內 helper
Non-goals:
- 重跑 221 live cases
- 宣稱 G-A..G-H PASS
- 修 M04/M06/M16 產品 validator
- 修 OS ACL / Fresh G1
- 建立新 CI 或第二控制平面
- 部署／production
- 把已歸檔 567 檔當已授權執行碼
Authorized mutations:
- 本地 archive metadata：PACKET_MANIFEST.json、R6_PUBLICATION_VERIFICATION.json、以及新增的 errata／scope-scan／approval 紀錄
- 既有 PR #3 分支（evidence/cnv-pipd-ls-sp-20261015-r6）在 EVIDENCE/CNV-PIPD-LS-SP-20261015/** 內的提交與推送（非 force）
- HG-KSEOS 內的 narrow admission 與本地 checkpoint／handover 紀錄
Forbidden mutations:
- main 直寫或 force push
- 產品／canonical DB／sealed Stage-2 變更
- 第二控制平面或 RBWI
- 自行核准或代簽 AO/Release
- 執行 PR 內腳本或 helper
- 加入 .pyc 或移除失敗證據
Claim ceiling: LOCAL

## 4. Active / Deferred / Forbidden scope
Active:
- native-prompt-compiler: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- archive-publication-metadata-repair-M1: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- trusted-scope-secret-preflight-M2: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- bounded-branch-update-and-readback: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
- r7-handoff-return-pack: ACTIVE_REQUIRED; action=QUALIFY; runtime_required=true
Non-active:
- none
Do not install, enable, or qualify a non-active capability.

## 5. Baseline / Reuse / Do-not-redo
Baseline: required=true; verified=true; reuse_prior_pass=true
Do not reopen:
- R6 567 blob 原包 bytes
- R6 失敗 receipts (M04/M06/M16、checker transient write、driver exit3)
- sealed RP-002 Stage-2
- SQP1／Stage-3
- 221／18／24／8 Gate 的既有 NOT_RUN 事實
Verify source and candidate bindings before reuse. A tracked mutation invalidates the affected seal.

## 6. Implementation and qualification gates
Use Manifest → owner WP/RBWI → TaskSpec/WorkOrder → active AGENTS/SKILLS → Harness/Loop.
Runtime closure:
- native-prompt-compiler: verdict=NOT_READY; work=本輪實跑 C0-C9 四階並保留 receipt；不因此轉 READY
- archive-publication-metadata-repair-M1: verdict=NOT_READY; work=以提交後實際 Git tree 驗證 tracked_inventory 集合等價
- trusted-scope-secret-preflight-M2: verdict=NOT_READY; work=受信任、PR 包外的固定掃描器；保留工具版本與 scan digest
- bounded-branch-update-and-readback: verdict=NOT_READY; work=非 force push；POST-commit 外部讀回 new_head/tree/blob 集合
- r7-handoff-return-pack: verdict=NOT_READY; work=EIA-01..09 去向、R7 blockers、rollback pointer、non-claims
Required user journeys:
- R6R7-ARCHIVE-MINIMAL-REPAIR: 外部驗收後對既有 PR #3 做最小發布修補，讓驗收官能重算 manifest 且看到可信的範圍/秘密掃描與維護者授權紀錄 → 更新後的 Draft PR #3、M1/M2/M3 raw refs、POST-commit external readback、R7 blockers
Acceptance predicates:
- ACC-CAP-01 subject=native-prompt-compiler depth=L4_FAILURE_RECOVERY
- ACC-CAP-02 subject=archive-publication-metadata-repair-M1 depth=L4_FAILURE_RECOVERY
- ACC-CAP-03 subject=trusted-scope-secret-preflight-M2 depth=L4_FAILURE_RECOVERY
- ACC-CAP-04 subject=bounded-branch-update-and-readback depth=L4_FAILURE_RECOVERY
- ACC-CAP-05 subject=r7-handoff-return-pack depth=L4_FAILURE_RECOVERY
- ACC-DEL-10 subject=D1-manifest-metadata-repair depth=L4_FAILURE_RECOVERY
- ACC-DEL-11 subject=D2-trusted-scope-secret-scan depth=L4_FAILURE_RECOVERY
- ACC-DEL-12 subject=D3-maintainer-prefix-approval-record depth=L4_FAILURE_RECOVERY
- ACC-DEL-13 subject=D4-post-commit-external-readback depth=L4_FAILURE_RECOVERY
- ACC-DEL-14 subject=D5-pr-body-and-dispositions depth=L4_FAILURE_RECOVERY
- ACC-DEL-15 subject=D6-return-pack-and-blockers depth=L4_FAILURE_RECOVERY
- ACC-DEL-16 subject=D7-versioned-errata depth=L4_FAILURE_RECOVERY
- ACC-REQ-40 subject=AR-00 depth=L4_FAILURE_RECOVERY
- ACC-REQ-41 subject=AR-01 depth=L4_FAILURE_RECOVERY
- ACC-REQ-42 subject=AR-02 depth=L4_FAILURE_RECOVERY
- ACC-REQ-43 subject=AR-03 depth=L4_FAILURE_RECOVERY
- ACC-REQ-44 subject=AR-04 depth=L4_FAILURE_RECOVERY
- ACC-REQ-45 subject=AR-05 depth=L4_FAILURE_RECOVERY
- ACC-REQ-46 subject=AR-06 depth=L4_FAILURE_RECOVERY
- ACC-REQ-47 subject=AR-07 depth=L4_FAILURE_RECOVERY
- ACC-REQ-48 subject=AR-08 depth=L4_FAILURE_RECOVERY
- ACC-REQ-49 subject=AR-09 depth=L4_FAILURE_RECOVERY
- ACC-REQ-50 subject=Q01 depth=L4_FAILURE_RECOVERY
- ACC-REQ-51 subject=Q02 depth=L4_FAILURE_RECOVERY
- ACC-REQ-52 subject=Q03 depth=L4_FAILURE_RECOVERY
- ACC-REQ-53 subject=Q04 depth=L4_FAILURE_RECOVERY
- ACC-REQ-54 subject=Q05 depth=L4_FAILURE_RECOVERY
- ACC-REQ-55 subject=Q06 depth=L4_FAILURE_RECOVERY
- ACC-REQ-56 subject=EIA-R6-01 depth=L4_FAILURE_RECOVERY
- ACC-REQ-57 subject=EIA-R6-02 depth=L4_FAILURE_RECOVERY
- ACC-REQ-58 subject=EIA-R6-06 depth=L4_FAILURE_RECOVERY
- ACC-JRN-01 subject=R6R7-ARCHIVE-MINIMAL-REPAIR depth=L4_FAILURE_RECOVERY
Proxy, static, maker, shared, file-presence, or summary evidence cannot close runtime behavior.

## 7. Failure / HITL / Repair / Resume
Use the smallest affected repair, focused tests, affected regression, independent recheck, and a new checkpoint.
Require HITL for: Maintainer 對 evidence prefix 的一次性授權（M3）, 若 remote head 漂移需重新綁定, 若掃到真 secret 需通報與輪替.
No silent fallback. Use only a certified explicit substitute; otherwise return BLOCKED_EXTERNAL or BLOCKED_HITL.

## 8. Evidence / Independent acceptance / Candidate binding
Return case-specific raw receipts, command or probe, stdout/stderr/exit, producer, independent checker, source hashes, candidate head/package hash, invalidation, rollback, and residue readback.
Maker output is an evidence candidate, not a final verdict.

## 9. Termination / Final output
Terminal states: CANDIDATE_READY_FOR_INDEPENDENT_REVIEW, INDEPENDENTLY_ACCEPTED, TEMP_CLOSED, FAIL.
Nonterminal pauses: ITERATION_BUDGET_PAUSE, SESSION_BOUNDARY, HITL_AUTHORITY_EDGE.
Iteration or session pause requires a checkpoint and is not completion.
Return no claim above LOCAL.
