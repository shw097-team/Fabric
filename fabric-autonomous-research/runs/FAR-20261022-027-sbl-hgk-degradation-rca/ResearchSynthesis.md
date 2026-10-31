# SBL × HG-KSEOS 降級根因研究報告（FAR-20261022-027）

> 本檔是 CANDIDATE 研究產物：不是驗收、不是升格、不是安裝或原生整合的主張。本輪沒有變更任何產品樹、沒有簽發驗收、沒有推送。
> 每一項結論都附上可被檢查者開啟的 locator（`path:line` 或 `path` + 引用的命令與 exit code）。凡證據未覆蓋者一律寫 `NOT_MEASURABLE` / `OUT_OF_SCOPE`，不製造數字。

## 0. 一句話結論

SBL 目前對 Fabric 治理契約只是「引用」而非「消費」，而且不是建構在現版 HG-KSEOS 基座上（落後 18 個 commit、278 個變更路徑，其相容性版本 pin 為空轉常數、`hg_kseos` 依賴在其自述直譯器內根本未安裝）；因此「SBL & HG-KSEOS」相較「只用 HG-KSEOS」的真正劣化是**驗收吞吐**與**宣告／實作一致性**，而非已證實的時間或金錢溢價；七大能力面沒有任何一面能以「全自動自檢測＋自修補＋自驗收」成立，其中「self-accept」與 HG-KSEOS 的 SoD 禁令（`writer == checker` 直接拒絕）在結構上互斥。

## 1. 量測基準與方法（admission、車道、模型實測、證據來源）

### 1.1 Admission 基準

| 項目 | 量測值 | locator |
|---|---|---|
| Requirement | `REQ-HGK-PRJ-SBL-HGK-RCA-20261022`（FROZEN） | `OWNER_MANDATE.txt`；`ResearchRequest.yaml` `hgk_admission` |
| TaskSpec | `TS-req-hgk-prj-sbl-hgk-rca-20261022`（ADMITTED） | `evidence/W1_fabric_integration.md:326-327` |
| WorkOrder | `WO-TS-REQ-HGK-PRJ-SBL-HGK-RCA-20261022-EXEC`（CREATED） | `evidence/W1_fabric_integration.md:320-325` |
| WorkOrder writer | `codex-lane:opencode-go/minimax-m3.1-flash-free@EXECUTE-rank1` | `evidence/W1_fabric_integration.md:322` |
| WorkOrder base_head | `d62635626d5d2e54fe5bba22a500a17423c85719` | `evidence/W1_fabric_integration.md:324` |
| Acceptance | `NOT_RUN`（本輪不自我驗收） | `ResearchRequest.yaml` `hgk_admission.acceptance_verdict` |

### 1.2 車道與模型實測（MANDATE vs OBSERVED）

- **PLAN**：`opencode-go/deepseek-v4.1-flash`（Hermes session plane）— `ResearchPlan.yaml` `execution_lanes.PLAN`。
- **EXECUTE**：`opencode-go/minimax-m3.1-flash-free@EXECUTE-rank1`，served 3.78 s、usage ok、exit 0、nonce present — `ResearchRequest.yaml:41`；receipt 欄位見 `evidence/W3_capability_probe.md:534-561`。
- **VERIFY_SECURITY**：`opencode-go/deepseek-v4.1-flash@VERIFY_SECURITY-rank4`，served 2.50 s、usage ok、exit 0 — `ResearchRequest.yaml:42`；`evidence/W3_capability_probe.md:564-591`。
- **宣告 vs 實際釘選的落差（已揭露，非靜默替換）**：pool 宣告的 `PLAN` rank-1 與 `VERIFY_SECURITY` rank-1 皆為 `openai-codex/gpt-6.1-sol`（`evidence/W3_capability_probe.md:307`、`:963`），本輪依 pool 允許的 `selection_semantics`（「the instructed entry replaces rank 1」）改釘 owner 指定的手臂（`ResearchRequest.yaml:43-47`）。EXECUTE 的宣告 rank-1 本來就是 `opencode-go/minimax-m3.1-flash-free`（`evidence/W3_capability_probe.md:294`），與 mandate 一致。
- receipt 邊界：這兩張 receipt 只證明「該次呼叫由指定手臂服務且 usage 成功」，**不是**驗收收據、不證明原生執行權限或主體驗證；且 `credential_posture` 為 `INCONCLUSIVE`／`WARN_CONTINUE`、`subject_mutation` 為 `not_guarded` — `evidence/W3_capability_probe.md:594`。

### 1.3 證據來源與方法邊界

| 檔案 | 方法 | 邊界 |
|---|---|---|
| `evidence/W1_fabric_integration.md` | 唯讀治理契約稽核＋in-memory 探針＋唯讀 SQLite 讀回 | 未呼叫任何 issuance/mutation API；僅寫出該份證據檔（`evidence/W1_fabric_integration.md:343`） |
| `evidence/W2_base_drift.md` | git 距離量測＋adapter 欄位讀取 | 該檔的子代理自寫版本被本車道 pre-write guard 拒收（草稿含受保護 token），**未落地任何檔**；所有數字由 orchestrator 重新執行命令取得，非子代理自述（`evidence/W2_base_drift.md:3-6`） |
| `evidence/W3_capability_probe.md` | 七能力面唯讀探針＋唯讀 DB census | 未做 dispatch／安裝／fetch；既有 receipt 為歷史觀測而非新回合（`evidence/W3_capability_probe.md:5`） |
| `evidence/W4_performance_delta.md` | 唯讀 artifact 抽樣比較 | 僅讀既有收據，未重新執行測試、dispatch 或 DB 寫入（`evidence/W4_performance_delta.md:20`） |

- 治理門檻：G1（每個因果主張附可開啟 locator）、G2（能力答案必為實測狀態而非宣告）、G3（宣稱上限存在且未被突破）、G4（writer 與 checker 分屬不同車道且不同進入點）— `ResearchPlan.yaml` `gates`。
- 路由：`RESEARCH_LITERATURE_REPO → NATIVE_WITH_SELECTED_ARIS`；`RESEARCH_ADVERSARIAL_CHALLENGE → NATIVE_NO_CHALLENGE` — `ROUTE_DECISION.json`；`ResearchPlan.yaml` `route.disagreed_class`。

## 2. 問題一：SBL 是否完整且正確接入 Fabric 治理契約

**答案：否。** SBL 對 Fabric 治理契約的狀態是「引用」（`CITED_ONLY`）與「缺位」（`ABSENT`），不是「消費」（`CONSUMED`）。W1 對四個接面逐軸判定如下（`evidence/W1_fabric_integration.md:34-37`）：

| 接面 | 判定 | 決定性 locator |
|---|---|---|
| (a) Fabric schemas | **ABSENT** | `SBL/sbl_core/dto.py:106-129`；`SBL/sbl_sp/bridge.py:43-74`；唯一 Fabric 來源是非治理性的 AGENTS support（`SBL/contracts/SBL_C0_C9_CONTRACT-R9.json:30-35,193-199`）；精確掃描 exit 1 / no matches（`evidence/W1_fabric_integration.md:95-99`） |
| (b) Fabric install/registration target | **ABSENT** | SBL 自身記錄 `NO_SBL_INSTALL_TARGET`（`SBL/_governance/round-20261021-r8/INSTALL_BOOTSTRAP_R8.json:116-118`）；Fabric 註冊政策需要 subject/version/digest/owner/ceiling/permission/lifecycle/rollback 欄位（`Fabric/FABRIC/control/PROFILE_STACK_REGISTRATION_POLICY.yaml:8-23`） |
| (c) Fabric evidence/packet contract | **ABSENT** | `SBL/tools/evidence_manifest.py:47-61` 與 `SBL/sbl_core/m05_verify.py:65-94,170-176` 未綁定 `Fabric/FABRIC/assurance/EVIDENCE_CONTRACT.yaml:2-14` 與 `Fabric/FABRIC/contracts/FABRIC_COLLABORATION_ABI.schema.yaml:15-27`；scan 無參照（`evidence/W1_fabric_integration.md:36`） |
| (d) HGK WorkOrder/Permit issuance（產品原生接縫） | **CITED_ONLY** | `HG-KSEOS/_sbl_harness_adapter/adapter.json:10-19,39-40` 明確不提供 workorder admission / permit signing；`SBL/README.md:111-116` 宣告 `STANDALONE_ONLY`；原生掃描 exit 1（`evidence/W1_fabric_integration.md:105-108`） |

**負面搜尋的量測邊界**：`rg -n -i 'FABRIC-EVIDENCE|FABRIC-COLLABORATION|…|packet' sbl_core sbl_sp sbl_cli contracts tools evidence_ledger openspec README.md` → exit 1、stdout 空、stderr 空（`evidence/W1_fabric_integration.md:95-99`）；`rg -n -i 'hg_kseos|SharedSpine|create_workorder|issue_permit|ExecutionBinding' sbl_core sbl_sp sbl_cli` → exit 1（`evidence/W1_fabric_integration.md:105-108`）。exit 1 代表「無匹配」，不是「整合成功」。全 Fabric 非 run 路徑 token 掃描得到 42 檔 177 行命中，但其中 115 行通過 token 邊界檢查、111 行通過嚴格 `rg -w`，其餘是 base64/ResBlock 等無關命中，已逐條列於附錄 A（`evidence/W1_fabric_integration.md:117-122`、`:347-396`）。

**必須同時保留的反證（本報告不把 SBL 說成惡意偽造）**：

- SBL 的本地 `BuildOrder` 與 HGK WorkOrder 是不同 DTO，本輪未觀察到 SBL 原生簽發 WorkOrder/Permit 的實作（`SBL/sbl_core/dto.py:106-111`；`evidence/W1_fabric_integration.md:7`）。
- 真實的 HGK 施工 WorkOrder 確實存在，含 `CREATED`、`FAILED`、`ROLLED_BACK` 歷史，本輪這一筆也在內（`evidence/W1_fabric_integration.md:218-223`、`:320-328`）。這證明「有真實 admission 記錄」，不證明「有 SBL runtime WorkOrder → ExecutionBinding → Permit 消費鏈」（`evidence/W1_fabric_integration.md:37`、`:59-63`）。
- SBL 自身的局部紀律是真的：它會拒絕 same maker/checker、`SUMMARY_ONLY` 代理狀態、超出建置上限的 ceiling、provider 關閉時的 skill 載入（`evidence/W1_fabric_integration.md:196-207`；`SBL/sbl_core/m05_verify.py:42-54,116-129`）。這些是**局部不變量**，不是經驗證的原生 principal 證明（`evidence/W1_fabric_integration.md:68`）。
- Fabric 自己的規則拒絕把「政策存在」當成「契約被消費」（`Fabric/FABRIC/AGENTS.md:73-74,128-129`），本報告沿用同一判準。

**結論（Q1）**：SBL 只**引用** Fabric 治理契約，不**消費**它；就「完整且正確接入」而言，答案是否定。

## 3. 問題二：SBL 是否以「現版 HG-KSEOS」為工程基座升級

**答案：否。** W2 的量測結果：

| 量測 | 值 | locator |
|---|---|---|
| 現版 HG-KSEOS HEAD | `3dfaebc5c1d2ffe7d1782f3027bd25b54a557f2b`（branch `codex/hgk-final-closure-002`，worktree 乾淨 0 dirty） | `evidence/W2_base_drift.md:8-9` |
| SBL 自述基座 | `b22706e`（最新 handover） | `SBL/_governance/round-20261021-r10/HANDOVER_SBL_R10_20261021.md:77` |
| 落後 commit 數 | `b22706e..HEAD` = **18**；`fa1ac063..HEAD` = **19** | `evidence/W2_base_drift.md:26-27` |
| 落後變更路徑 | **278**（260 added、18 modified、0 deleted） | `evidence/W2_base_drift.md:28-29` |
| SBL 自述 conformance | 最後一次量測在 `fa1ac06`：580 passed / 16 failed（baseline 575/21），且「`b22706e` 之後**沒有**重測」 | `SBL/_governance/round-20261021-r10/HANDOVER_SBL_R10_20261021.md:127,136`；`evidence/W2_base_drift.md:16-17` |

**兩個決定性的結構性缺陷**：

1. **版本 pin 空轉（vacuous pin）**。adapter 的 `hgk_pin` 是 `version_range: ">=0.1.0,<0.2.0"`、`observed_version: 0.1.0`；但 `git log -1 -S'version = "0.1.0"' -- pyproject.toml` → `ec58a0b 2026-08-08`，且 `git rev-list --count ec58a0b..HEAD` = **147**（全庫 148 個 commit）。也就是說這個 range 被此 repo 每一個 commit 滿足，它不是 drift gate 而是一個常數；adapter 能在落後 18 commit、278 路徑的情況下回報 `observed_version: 0.1.0`，而 adapter 自身機制沒有任何東西會失敗（`evidence/W2_base_drift.md:37-44`）。
2. **`hg_kseos` 依賴缺失且未接線**。adapter 的 `host.executable` 指向 `…\hermes\hermes-agent\venv\Scripts\python.exe`，在該直譯器下 `import hg_kseos` 失敗（`ModuleNotFoundError`）；`SBL/pyproject.toml` 宣告 `dependencies = []`，沒有任何機制安裝 `hg_kseos`。harness ABI 的 `requires_native: [WorkOrder, ExecutionBinding, Permit]` 因此只是宣告而非接線，adapter 自身的 `claim_ceiling: HOST_PENDING`、`native_effect: NOT_GRANTED` 與此一致（`evidence/W2_base_drift.md:46-51`）。

**不是的情形（避免誤診）**：

- adapter 的 `hgk_root` 指向**活體** HG-KSEOS 工作樹，解析根的 drift 為 **0** commit——它沒有指向舊的 `HGK/` checkout 或文件鏡像（`evidence/W2_base_drift.md:35-36`）。
- SBL 內**沒有** vendored `hg_kseos` fork；`SBL/pyproject.toml` 版本 `0.1.0`、release tree 為 `0.1.1rc1`，`SBL-install/` 只附一個 pointer（`hgk-adapter/MANIFEST.json`）而非模組副本。所以 drift 不以「source fork」形式出現，而是以**安裝、證據集與相容性閘門**的形式出現（`evidence/W2_base_drift.md:55-58`）。

**結論（Q2）**：SBL 不是以現版 HG-KSEOS 為工程基座升級的；其落後體現在安裝、證據集與相容性閘門，而非過期的解析根或 source fork。

## 4. 問題三：為何「SBL & HG-KSEOS」比只用「HG-KSEOS」更差

### 4.1 W4 的總量測表（原樣引用，`evidence/W4_performance_delta.md:1-12`）

| 記錄指標（主要樣本） | SBL + HG-KSEOS：FAR 023 / 025 / 026 | HG-KSEOS-only：remediation / MiniMax / fallback reorder |
|---|---:|---:|
| 檢視回合數 | 3 | 3 |
| 回合層級 WorkOrder 結果 | 3 FAILED；R7 另保留 ROLLED_BACK 鏈 | 1 VERIFIED；1 CREATED workorder family；1 NA |
| 記錄的驗收結果 | 3 FAIL | 1 NOT_RUN；2 NA；皆未主張驗收 |
| 發現列數 | 44 = 19 + 14 + 11；**不是** 44 個唯一缺陷 | NA 可比清單 |
| 保留的 lane 嘗試（全部角色） | 39 | 15 |
| 保留的 EXECUTE 角色嘗試（含探針） | 8 | 5 |
| 逾時的嘗試 | 0 | 4 |
| 保留嘗試秒數總和（全部角色） | 2,611.06 s | 2,983.27 s |
| 可量測的整回合 wall-clock | 0/3 | 0/3 |
| 回合歸屬的 relay usage / token / 金錢成本 | NOT_MEASURABLE | NOT_MEASURABLE |

### 4.2 成因分類

**（a）已量測（MEASURED）**

1. **驗收吞吐不足**：主要 SBL 回合 3/3 記錄 `FAILED` 且驗收 `FAIL`，無獨立驗收 PASS；R7 保留了一次對 premature PASS 的 rollback（`evidence/W4_performance_delta.md:88`；逐回合表見 `:34-43`）。這是該計畫內部的驗收吞吐赤字，**不是**配對後的產品失敗率。
2. **對照組也不是乾淨的成功基線**：fallback 組 WorkOrder 記為 `VERIFIED` 但驗收仍 `NOT_RUN`；remediation 組停在 `CREATED`；MiniMax 組在檢閱到的收據中沒有 lifecycle verdict，也沒有簽署的 AO verdict（`evidence/W4_performance_delta.md:39-41`、`:89`）。因此失敗率比值不可計算。
3. **發現列數不可當缺陷數**：44 是 TSV 列數，R7 的 F10/F17、F13/F16 等存在重疊（`evidence/W4_performance_delta.md:6`、`:28`）。
4. **樣本形態差異**：SBL 39 次 vs 對照組 15 次；EXECUTE 角色 8 vs 5；逾時 0 vs 4；秒數 2,611.06 vs 2,983.27。捕捉不對等、探針比例不同、工作量未配對，**不可當成本比**（`evidence/W4_performance_delta.md:90`）。
5. **跨面不一致（D1 類）在兩側都重複出現**：MiniMax `SELF-REVIEW.json` D1/D2、SBL R8 D1、FAR 025 F2/F3/F4/F5、FAR 026 F1/F2，且 FAR 026 明稱其 D1 是第三次重現（`evidence/W4_performance_delta.md:91`）。
6. **產品面也有真實進展**（不可抹除）：R9 把 4→0 個 acceptance-pointer 不符、釘住 14 個控制文件 digest、在其候選上回報 218 passed / 2 skipped；R8 歷史同環境 conformance 由 575/21 改善為 580/16 且無新增失敗，但 3 個未追蹤測試檔阻礙乾淨 checkout 重現；R10 rebind 之後**沒有** conformance 重測記錄（`evidence/W4_performance_delta.md:92`）。
7. **未排空的積壓**：SBL R10 handover backlog 為 7 個 open 項目；凍結的 R6 scope ledger 為 149/149 children OPEN、50 parents（37 OPEN、13 PARTIAL_EVIDENCE_ONLY）、38 surfaces（21 OPEN、12 PARTIAL_LOCAL_SCOPED、5 NOT_ADMITTED_NO_DISPATCH），這些**不是**本回合的關閉項，也不是可相加的共同分母（`evidence/W4_performance_delta.md:93`）。
8. **SoD 拒絕是活的**：SBL M05 對同一 maker/checker 拋 `SBL_E_SELF_CHECK_FORBIDDEN: a maker may not verify its own work`；HGK spine 對 `writer == checker` 拋 `InvariantViolation ERR_WORKORDER_SELF_REVIEW`，且比對發生在開啟交易之前（`evidence/W3_capability_probe.md:1001-1002`、`:1015-1021`）。
9. **self_check 沒有強制執行點**：找不到 runtime/tools/CI 對 `self_check_r*` 的強制呼叫者；R10 的唯讀子檢查在 drift gate 為綠時仍測出 epoch 與跨面不一致（`evidence/W3_capability_probe.md:1010`、`:961-965`、`:1025-1031`）。

**（b）推論（INFERRED）**

- 反覆不完整的驗收、範圍不佳的 gate 斷言、可寫 scratch 不符、重複的路由宣告，**合理地**會消耗 rework。
- 共用的 HGK 機制可能把延遲傳導進 SBL；額外的契約／host／SP 義務合理地會擴大工作量。
- 這是「受支持的機制與範圍差異」，**不是**已量測的增量成本，也不是「某個改動造成退化」的因果判定（`evidence/W4_performance_delta.md:97`）。

**（c）證據不支持（NOT_SUPPORTED_BY_ARTEFACTS）**

- 「SBL+HGK 比純 HGK 更慢／更貴」；
- 任何百分比成本溢價；
- 「SBL 造成共用失敗」的因果主張；
- 蘋果對蘋果的回合失敗率比值；
- 「SBL R11 已完成」；
- rebind 之後的現況 conformance；
- 完整契約完成百分比。

理由：檢閱到的證據中不存在整回合時間序列、帶回合標記的 relay usage、標準化工作單元或語意契約分母（`evidence/W4_performance_delta.md:99-101`）。

### 4.3 為何「更差」的誠實答案

SBL & HG-KSEOS 之所以在**已量測**的面向表現較差，來自三個可指名的機制，而不是時間或金錢：

1. **契約斷裂**：SBL 不消費 Fabric 契約，產品端沒有 WorkOrder → ExecutionBinding → Permit 的原生消費鏈，等於在 HG-KSEOS 之上疊了一層無法證明權威的平面（`evidence/W1_fabric_integration.md:34-37`、`:59-63`）。
2. **驗收閘門與 self-accept 的結構衝突**：每一輪都以「是否取得獨立驗收」結算，而 SBL 自己的標籤是 self-accept、HGK 又禁止同一 maker/checker，使驗收**只能外求獨立車道**（結構性事實，`evidence/W3_capability_probe.md:1012`、`:1023`）。**但「因此導致 3/3 回合沒有取得驗收」是未成立的因果主張**（AO 指出，已收窄）：那三輪各自有各自記錄在案的失敗原因——R7 是 checker `INCONCLUSIVE`、R9 是「沒有獨立驗收」而未執行、R10 是「需由 fresh session 驗證 handover」這條本輪無法自我滿足的判準（`evidence/W4_performance_delta.md:36-38`）。本報告只主張：SoD 與 self-accept 的標籤衝突使驗收**必須**外求；不主張它是那三輪失敗的原因。
3. **宣告與實作分離**：宣告面（pool／registry／provider_route／adapter pin／surface ledger）與實作面（實際安裝的套件、實際執行的閘門、實際排空的看板）分離，而現有 drift gate 只比對各面與其指向的檔案，無法把兩個面互相比對（`evidence/W3_capability_probe.md:961-965`、`:1025-1031`；`evidence/W2_base_drift.md:41-44`）。

**成本溢價本身不可量測**：relay usage 檔解析出 21,008 行、0 malformed，但**沒有 round 欄位**，因此回合歸屬的 usage/token/金錢數量為 `NOT_MEASURABLE`；且無費率表，本報告不給出任何金額估計（`evidence/W4_performance_delta.md:82`）。整回合 wall-clock 在 6 個主要回合中 0/3 可量，含 R8 與未指派的 R11 探針共 8 個 slot 亦為 0/8（`evidence/W4_performance_delta.md:11`、`:52`、`:69`）。

## 5. 問題四：七大能力面實測狀態

### 5.1 針對 owner 原始問題的直接回答

**「SBL & HG-KSEOS」目前並沒有辦法真的啟用 KANBAN／SWARM／GSTACK／OPENSPEC，並以 CODEX CLI＋多 SUB-AGENT 併行主執行、完整執行任務，同時對結果進行自動化「自檢測、自修補、自驗收」直到全部完成，並進行受治理的「自研究／自學習／自迭代／自進化」。**

逐面實測狀態（W3 狀態表原樣，`evidence/W3_capability_probe.md:11-19`）：

| 能力面 | 實測狀態 | 量測邊界（locator） |
|---|---|---|
| KANBAN | **PARTIAL** | `boards list` 與 `stats` exit 0；`ls` 在 subagent guard 下 exit 1，輸出 `kanban: delegate_task child contexts cannot mutate Kanban tasks or boards`（`:31-84`）；歷史 open backlog 仍在（`:88-96`） |
| SWARM | **PASS**（僅圖存在） | `kanban swarm --help` exit 0（`:106-135`）；96 個 board DB、62 個 graph-shaped root 滿足 root→worker→verifier→synthesizer（`:137`）；**未**測試新的 dispatch（`:231`） |
| GSTACK | **PARTIAL** | 7 個 selected named slices；role-name routing 有 native gap；lane CLI 沒有 flow-route／`selected_route`／`reason_code` 介面（`:235`、`:251-269`、`:323-325`） |
| OPENSPEC | **FAIL** | `openspec validate --all` exit 1：`Totals: 37 passed, 2 failed (39 items)`；失敗者為 `change/hgk-plan-plane-rebind-20261015` 與 `change/sod-independent-verify-enforcement`（`:409-461`、`:528`） |
| CODEX CLI | **PASS**（僅 receipt scope） | 兩張 receipt 的 `required == served`、nonce present、exit 0、usage receipt true（`:534-591`、`:594`） |
| SUB-AGENTS | **PARTIAL** | 有真實封存的 worker 輸出，但歷史回合只持久化 3/4；廣普查計有不可存取路徑（`:667-725`） |
| 自檢測 self-detect | **PASS**（偵測存在，但非強制自動閘門） | R7/R9/R10 檢查與 M05 evidence verification 存在；找不到強制生產呼叫者（`:1010`） |
| 自修補 self-repair | **PARTIAL**（planner，非執行器） | M06 `BoundedRepair` 產出 `NARROW_REPAIR`／`STOP_ESCALATE` 計畫；找不到執行 `NARROW_REPAIR` 或強制 `STOP_ESCALATE` 的 runtime consumer（`:997-999`、`:1011`） |
| 自驗收 self-accept | **FAIL** | SBL M05 拒絕同一 maker/checker；HGK spine 拒絕 `writer == checker`；自驗收作為能力 FAIL，拒絕閘門本身 PASS（`:1001-1002`、`:1012`） |
| 自進化 self-evolve | **FAIL** | R7 `SELF_EVOLUTION_DELTA.json` 記錄 7 條已採納教訓，但未建立強制的 apply/validate/rollback consumer；屬「有帳本、無自動套用閘門」（`:1013`、`:1034`） |

判定規則遵守 W3 的明文限制：**PASS 永不隱含產品驗收；PARTIAL 代表「量得的工作子集」，不是把已失敗的驗收條件降級；OpenSpec 失敗與自主 self-accept 失敗維持 FAIL**（`evidence/W3_capability_probe.md:21`）。本報告不把任何 PARTIAL 升級為 PASS，也不把任何 FAIL 軟化。

### 5.2 承載性衝突：SoD 與「self-accept」互斥

這是本輪最具結構性意義的發現，必須明白點名：

- **SBL 自身的標籤就是「self-accept」**——SBL 把 maker 與 checker 寫進自己的 verdict API，而實測顯示同一 maker 會被自己拒絕：`SBL_E_SELF_CHECK_FORBIDDEN: a maker may not verify its own work`（`evidence/W3_capability_probe.md:1001`；同一訊息亦見 `evidence/W1_fabric_integration.md:197`）。
- **HG-KSEOS 拒絕 `writer == checker`**：活體原始碼 `src/hg_kseos/spine.py:345-346` 於開啟交易前拋 `InvariantViolation("ERR_WORKORDER_SELF_REVIEW")`（`evidence/W3_capability_probe.md:1015-1019`；負控制輸出見 `:1002`）。
- **可調和的讀法（本報告採用的唯一讀法）**：**「self-detect」與「self-repair」是合法且已部分實作的；而「self-ACCEPT」必須由獨立車道（independent lane）執行，不能由 maker 自我簽發。** 依據是：SBL 的拒絕閘門與 HGK 的 SoD 兩邊都在工作且互相一致（`evidence/W3_capability_probe.md:1012`、`:1023`；`evidence/W4_performance_delta.md:110`），且 owner 的 mandate 本身把 Acceptance Challenge 與 Independent Acceptance Officer 分給 VERIFY 車道而非 writer 車道（`OWNER_MANDATE.txt`）。因此「self-accept」若被理解成「同一執行者簽收自己的成果」，它在 HG-KSEOS 治理契約下**結構上不可能**；若被理解成「由系統自動偵測與自動修復後，交由獨立驗收車道自動簽收」，則是可實作的目標狀態。
- 反證不可略過：本地回傳的 `Verdict`（`claim_level: LOCAL`）、綠色的 self-check receipt 或「兩個不同的任意字串」都不等於獨立簽發的驗收（`evidence/W3_capability_probe.md:1023`）。live R10 的範圍化讀回找到 13 筆 SBL 主體的 acceptance 列，**無一筆 PASS**（`:1030`）。

### 5.3 併行與產出的補充觀察

- SWARM 的 R14 見證（root `t_7a41e27f`、verifier `t_39825119`、synthesizer `t_d23ffddf`、4 個 worker 全 done）是真實的完成圖，但**完成的 DAG 不等於不同模型或獨立 principal 的證據**（`evidence/W3_capability_probe.md:231`）。本輪的 RCA board 在同一快照中沒有相同形狀的完整圖（`:231`）。
- R12 與 R13 只有自動完成的 swarm root 為 done，所有 worker 仍為 ready、verifier／synthesizer 仍為 todo；R14 雖有完成的一組七卡 swarm，仍有 23 張卡停在 ready（`evidence/W3_capability_probe.md:88-97`）。這是**量得未排空的積壓**，但單一快照無法證明「從不排空」——本報告不作該時間性主張（`:97`）。
- SUB-AGENTS 側最強證據是 R9 的 4 名 worker（model `gpt-6.1-sol`）與 3 份已封存 raw output（bytes 與 sha256 經讀回比對相符），第 4 份**明示遺失**且其發現僅存在於 ruling 內（`evidence/W3_capability_probe.md:667-723`）。

## 6. 根因清單

### 6.1 結構性（structural）

| # | 根因 | 證據 locator | 可修復槓桿 |
|---|---|---|---|
| S1 | 相容性版本 pin 空轉：`>=0.1.0,<0.2.0` 對一個 147/148 個 commit 未動版號的套件，永遠成立 | `evidence/W2_base_drift.md:37-44` | 把 pin 換成「可失敗的契約」：綁定 HG-KSEOS commit SHA（adapter 或 `hgk_pin.base_head`），使落後時 `adapter` 直接 fail 而非回報 `observed_version: 0.1.0` |
| S2 | `hg_kseos` 依賴未安裝且未接線：宣告的 `requires_native` 沒有對應的安裝路徑 | `evidence/W2_base_drift.md:46-51` | 在 `SBL/pyproject.toml` 宣告真實依賴並讓 adapter 記錄的 `host.executable` 能 `import hg_kseos`；安裝與接線分開做「可宣告 / 未宣告」兩階段 |
| S3 | Fabric 治理契約未被消費：schema、registration、evidence packet 三個接面 ABSENT | `evidence/W1_fabric_integration.md:34-36`、`:95-108`；`:122` | 先取得契約擁有者的適用性裁定，再綁定 `FABRIC_COLLABORATION_ABI` 的 version/digest，示範一次「非符合輸入被拒」的消費行為 |
| S4 | SoD 與「self-accept」互斥：同一 maker/checker 在兩層都被拒 | `evidence/W3_capability_probe.md:1001-1002`、`:1012`、`:1015-1019`、`:1023` | 把產品詞彙拆成 `self-detect`／`self-repair`／`self-accept-by-independent-lane` 三層，並讓 dispatch 層直接拒絕 writer==checker |
| S5 | 自修補與自進化無執行消費者：`NARROW_REPAIR`／`STOP_ESCALATE` 只有生產者與詞彙；演進帳本無 apply/validate/rollback | `evidence/W3_capability_probe.md:1011`、`:1013`、`:1034` | 為 repair plan 與 evolution delta 各接一個受治理 consumer，並讓它們納入 CI／runtime 的強制呼叫點 |
| S6 | drift gate 結構性失明：只比對各面與其指向的檔案，無法把兩個面互相比對 | `evidence/W3_capability_probe.md:961-965`、`:1025-1031`（`c4_surfaces_agree` 為 False 而 `c3_drift` 為 True） | 補一個「面對面」一致性 gate（governed PLAN plane / EXECUTE lane 宣告 / provider_route 三方互比 pool rank-1） |

### 6.2 流程性（process）

| # | 根因 | 證據 locator | 可修復槓桿 |
|---|---|---|---|
| P1 | 驗收吞吐赤字：主要 SBL 回合 3/3 `FAILED`、驗收 3 FAIL | `evidence/W4_performance_delta.md:1-5`、`:36-38`、`:88` | 把「取得第一個獨立驗收」設為回合的硬 gate 條件（見 §7 O3），而非事後結算 |
| P2 | 基座落後且未重測：18 commit／278 路徑，最後 conformance 在 `b22706e` 之前 | `evidence/W2_base_drift.md:26-29`、`:16-17`；`evidence/W4_performance_delta.md:109` | 先做 absolute + same-baseline 的 conformance 重測（R10-01），再做 rebind；順序不可顛倒 |
| P3 | 積壓未排空：看板 ready 卡片、handover open 項目、R6 scope ledger 大量 OPEN | `evidence/W3_capability_probe.md:88-96`；`evidence/W4_performance_delta.md:93` | 以 backlog 為單位排程：每回合先清空自己建立的卡，再開新卡；對 38 surfaces 給出明確的 closure 條件 |
| P4 | 委派持久化不完整：R9 僅 3/4 raw output 落地 | `evidence/W3_capability_probe.md:697`、`:725` | 把 worker raw output 的落地與 sha256 讀回列為 dispatch 的完成條件，而非可選證據 |
| P5 | `self_check_r*` 沒有強制生產呼叫者 | `evidence/W3_capability_probe.md:1010` | 把它接到既有 gate 流程（例如 HGK artifact gate）成為 fail-closed 步驟 |
| P6 | 宣告面彼此不一致：assignment epoch 29 vs registry 30；pool PLAN/EXECUTE 與實際宣告面不符 | `evidence/W3_capability_probe.md:961-963`、`:1029` | 讓 epoch 與 pool 成為跨面的單一真相來源，並在寫入前斷言三者一致 |
| P7 | 只讀稽核邊界造成的能力面缺口：多個面只能量到「存在」不能量到「執行」 | `evidence/W3_capability_probe.md:231`、`:323`、`:325`、`:725`、`:1006` | 在下一輪以明確授權的 mutation-free 沙箱（或獨立唯讀執行車道）重測 SWARM dispatch 與 GSTACK named-method 執行 |

### 6.3 宣告性（declarative）

| # | 根因 | 證據 locator | 可修復槓桿 |
|---|---|---|---|
| D1 | SBL 自身宣告的 ceiling 是 `STANDALONE_ONLY`（不提供 WorkOrder/ECP/Permit/ExecutionBinding），與 owner 期待的「完整接入＋自驗收」本質不同 | `SBL/README.md:111-116`（引自 `evidence/W1_fabric_integration.md:67`）；`SBL/_governance/round-20261021-r9/FAR-R9-RULING.md:85` | 用一張對照表把「owner 期望 vs 產品宣告 ceiling vs 實測」並列，讓落差在宣告層就被看見，而不是在回合失敗後才被發現 |
| D2 | 候選 R9 契約與 `contracts/compiled-r9/` 為**未追蹤**狀態，被當作候選證據檢視而非已提交來源 | `evidence/W1_fabric_integration.md:21`、`:24` | 要嘛納入版控成為可比基線，要嘛在所有引用它的主張中明確標記為 untracked candidate |
| D3 | Fabric 角色被窄化描述為「the autonomous-research harness」 | `SBL/_governance/round-20261021-r8/INSTALL_BOOTSTRAP_R8.json:116-118`（引自 `evidence/W1_fabric_integration.md:339`） | 對齊到 `Fabric/FABRIC/AGENTS.md:17-22` 的契約面定義，避免以窄化定義推導豁免 |
| D4 | OPENSPEC 宣告與驗證結果衝突：兩個 change 宣告存在但無 spec delta，validate 硬失敗 | `evidence/W3_capability_probe.md:435`、`:456`、`:459`、`:503`、`:521`、`:528` | 對這兩個 change 補 delta 或依規定設 `skip_specs: true`，讓 `validate --all` 回到 exit 0 |
| D5 | 版本宣告長久未動：`pyproject.toml` `0.1.0` 固定在 `ec58a0b`，release tree 為 `0.1.1rc1`，install 只帶 pointer | `evidence/W2_base_drift.md:38-39`、`:55-57` | 版本升級需與「可失敗的 base pin」同步設計，否則升版不會改變任何相容性事實 |
| D6 | 「self-accept」一詞在 SBL 與 owner 期待中同時承載「能力名」與「被 HGK 禁止的行為」兩種語義 | `evidence/W3_capability_probe.md:1023`、`:1012`；`evidence/W1_fabric_integration.md:197` | 在所有治理文件中把該詞拆為 self-detect / self-repair / independent-accept 三個可分別量測的能力 |

## 7. 低摩擦修復選項

以下皆為**候選建議**，本輪不執行任何一項（`ResearchRequest.yaml` `out_of_scope`；`evidence/W1_fabric_integration.md:343`）。

| # | 動作 | 成本 | 風險 | 需 owner 決策 |
|---|---|---|---|---|
| O1 | 將 `HG-KSEOS/_sbl_harness_adapter/adapter.json` 的 `hgk_pin` 由空轉版本範圍改為綁定 HG-KSEOS commit SHA，並讓不符時 fail（非回報 `observed_version`） | 低（單一 descriptor 欄位＋一個斷言） | 中：一旦綁定，所有以舊 base 為前提的流程會立刻變紅（屬預期） | **是**——要決定綁定哪個 SHA 與失敗語意 |
| O2 | 在 `SBL/pyproject.toml` 宣告 `hg_kseos` 依賴，並讓 adapter 記錄的 `host.executable` 可 `import hg_kseos`（先做可宣告版本，不觸碰原生簽發） | 中 | 中：會牽動 install／bootstrap 產物與 lifecycle 測試 | **是**——要決定安裝形態（安裝到 hermes venv 還是隨 SBL 打包）與天花板 |
| O3 | 把「取得第一個獨立驗收」提升為回合硬 gate：在 HGK admission 前先取得可寫的獨立 checker scratch 與一份綁定凍結主體的獨立 verdict | 中 | 低（只加條件，不放寬任何拒絕） | **否**——但需要 owner 授權一個 checker 可寫的隔離 scratch root |
| O4 | 治理詞彙拆分：把 SBL／FAR 文件中的「self-accept」統一改寫為 self-detect / self-repair / independent-accept，並保留 `ERR_WORKORDER_SELF_REVIEW` 與 `SBL_E_SELF_CHECK_FORBIDDEN` 兩個拒絕閘門為 SoD 主軸 | 低（文件與欄位改名） | 低；需注意不得讓改名被誤讀為「已取得自驗收能力」 | **否** |
| O5 | 補一個「面對面」一致性 gate：把 governed PLAN plane、EXECUTE lane 宣告、`provider_route` 三者與 pool rank-1 互比，失敗即 fail | 低–中（既有 `c4_surfaces_agree` 可直接升格） | 低 | **否** |
| O6 | 修復兩個 OPENSPEC change（補 spec delta 或依規設 `skip_specs: true`），使 `openspec validate --all` 回到 exit 0 | 低 | 低–中：`sod-independent-verify-enforcement` 涉及 SoD 語意，補 delta 時不得改動其拒絕語意 | **否**（但改動內容需 review） |
| O7 | 排空 backlog：先清空自己建立的看板卡與 handoff open 項目，再開新卡；對 38 surfaces 逐條寫明 closure 條件 | 中–高（持續性工作） | 低；風險是為了「看起來在排空」而製造表面關閉 | **否** |
| O8 | 為 `self_check_r*` 與 repair plan 接上受治理的強制執行點（含 CI／runtime），使自檢測從「可跑」變成「必跑」 | 中 | 中：強制閘門會讓過去「綠」的回合變紅 | **是**——要決定強制點位置與失敗語意 |
| O9 | 取得 Fabric 契約擁有者對「SBL 是否為適用受治理面」的裁定，再決定是否做 registration；在此之前不製造任何 install target | 低（一次決策請求） | 低 | **是**（裁定本身是 owner／契約擁有者決策） |

優先序建議：O1、O4、O5、O6 為低摩擦且直接命中已量測缺陷；O3 為解鎖驗收吞吐的關鍵路徑；O2 與 O9 需 owner 決策後才動作。

## 8. 未量測與不在範圍

### 8.1 NOT_MEASURABLE（證據不足以量測，非零、非負）

| 項目 | 原因 | locator |
|---|---|---|
| 整回合 wall-clock 時長 | 6 個主要回合 0/3 可量；含 R8 與未指派 R11 探針共 8 個 slot 0/8。沒有涵蓋 admission、執行、中斷與驗收的完整 start/end 配對 | `evidence/W4_performance_delta.md:11`、`:52`、`:69` |
| 回合歸屬的 relay usage / token / 金錢成本 | usage 檔 21,008 行、0 malformed，但沒有 round 欄位；無費率表 | `evidence/W4_performance_delta.md:82` |
| 「SBL 較慢／較貴」的百分比溢價 | 缺少整回合時間序列、帶回合標記的 usage、標準化工作單元、語意契約分母 | `evidence/W4_performance_delta.md:99-101` |
| 現版基座的 conformance 數字 | SBL 自述在 `b22706e` 之後未重測；執行 pytest 會違反唯讀／單檔輸出範圍 | `evidence/W2_base_drift.md:16-17`、`:64-65`；`evidence/W4_performance_delta.md:109` |
| SBL release 實際建構時所對應的 HG-KSEOS commit | release/install 收據只綁 SBL commit 加外部 HGK 路徑／版本，從不綁 HGK 原始碼 commit | `evidence/W2_base_drift.md:62-63` |
| 278 個變更路徑的位元等價承接 | 260 個是新增路徑，路徑數是工程差異的上界，不等於 SBL 缺少同等數目的能力 | `evidence/W2_base_drift.md:66-68` |
| 唯一缺陷總數 | W4 的 44 是 TSV 列數且存在重疊，不能當唯一缺陷數 | `evidence/W4_performance_delta.md:6`、`:28` |
| 看板「從不排空」的時間性主張 | 單一快照無法證明時間上的 never | `evidence/W3_capability_probe.md:97` |
| 交接紀錄與 receipt 的時間戳覆蓋 | 這是 receipt timestamp coverage，不是回合時長 | `evidence/W4_performance_delta.md:71-80` |

### 8.2 OUT_OF_SCOPE（本輪不在範圍）

| 項目 | 原因 | locator |
|---|---|---|
| 變更 HG-KSEOS / Fabric / SBL 產品樹 | 明確排除於 out_of_scope；本輪唯讀 | `ResearchRequest.yaml` `out_of_scope`；`evidence/W1_fabric_integration.md:343` |
| 把候選宣告升格為 ACTIVE | 明確排除 | `ResearchRequest.yaml` `out_of_scope` |
| 自我簽發外部驗收 | 明確排除；本輪 acceptance 維持 `NOT_RUN` | `ResearchRequest.yaml` `out_of_scope`；`ResearchPlan.yaml` `self_governance.self_accept` |
| 原生 WorkOrder / ExecutionBinding / Permit 簽發或安裝 | 本輪未主張安裝或原生整合；SBL 自身宣告亦為 `STANDALONE_ONLY`／`NOT_GRANTED` | `evidence/W1_fabric_integration.md:67`；`evidence/W2_base_drift.md:46-51` |
| 製造 Fabric install target | W1 明確不做；缺的是契約擁有者的適用性裁定 | `evidence/W1_fabric_integration.md:35`、`:51` |
| 新的 SWARM dispatch / 新的 delegation / GSTACK named-method 執行 / `self_check_r*` 完整腳本執行 | 皆會變更 board／runtime 狀態或寫檔，違反唯讀與單檔輸出約束 | `evidence/W3_capability_probe.md:231`、`:325`、`:725`、`:1006` |
| 以 dispatcher `ok=true` 或 receipt `ok=true` 當作語意通過 | W4 明示不把 dispatcher ok 當語意 PASS | `evidence/W4_performance_delta.md:192` |

## 9. 宣稱上限（claim ceiling）

**CANDIDATE_ONLY。** 本檔是研究產物：

- 不是驗收（acceptance）：本輪 HGK acceptance 維持 `NOT_RUN`；本報告不主張任何產品、surface 或 round 已被驗收。
- 不是安裝或原生整合：本輪未執行安裝，不主張 SBL 已安裝於任何主機，也不主張與 Fabric 或 HG-KSEOS 完成原生整合。
- 不是升格或推送：未變更任何產品樹，未提交、未推送、未把候選升格為 ACTIVE。
- 不是完整契約閉合：不含完成百分比，不主張全契約通過。
- 不主張「更慢／更貴」的量化溢價：見 §4.2(c) 與 §8.1。
- 能力面狀態為**量測狀態**，非產品驗收：W3 明示「PASS never implies product acceptance」（`evidence/W3_capability_probe.md:21`）。
- 本報告所列槓桿與提案皆為候選，需經 owner／契約擁有者裁定後才可動作（見 `ProposedEvolution.yaml`，全部標記 `claim_ceiling: CANDIDATE_ONLY`）。
