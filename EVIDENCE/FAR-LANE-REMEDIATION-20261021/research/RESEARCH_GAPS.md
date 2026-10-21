# 殘留、缺口與阻斷關閉清單

本次為唯讀盤點；未修改 repo、未關閉卡片、未變更 ledger、未執行網路 probe。以下「關閉動作」均為待執行方案，不是已完成修復。

所有命令皆在 `C:\Projects\Agent_Workspace\HG-KSEOS` 執行。量測起始時間由 Python 實讀為 `2026-10-21T12:33:43.033205`。

**重要新發現：OpenSpec 不是只印提示。實跑 strict validation 回傳 exit 1，存在具體規格錯誤。**

## 證據命令索引

以下代碼供各項引用，均為本次實際執行的命令或其 Python 掃描核心：

| 代碼 | 實跑命令／掃描方式 | 讀到的值 |
|---|---|---|
| E1 | `git log --oneline -25`；`git status --short`；Python 解析 `git status --porcelain -z` | HEAD=`c442f07`；10 筆 tracked 修改、300 筆 untracked **status entries**。後者包含目錄，不能當成檔案數 |
| E2 | Python 對 `Path("var").iterdir()` 各目錄執行 `os.walk(..., onerror=...)`，逐一計算檔案、`REPORT.md`、檔名含 `receipt`／`manifest` 的數量 | 114 目錄；112 有可見檔案、2 空目錄；80 含至少一種命名指標、32 有檔但無上述指標；10,314 次遍歷錯誤 |
| E3 | Python 逐讀 `openspec/changes/*/tasks.md`，用 `^\s*-\s*\[ \]` 與 `^\s*-\s*\[[xX]\]` 計數 | 37 個 active changes；35 個有未勾項目，合計 471 個未勾項目；2 個全勾。另有 `archive/`，內含一個 archived change |
| E4 | Python `csv.DictReader` 讀 `source-freeze/TT_LEDGER.csv` 與 `registries/*.csv`，搜尋 status/state 欄位中的 OPEN/PENDING | TT ledger 11 列、OPEN 2 列、PENDING 0 列；registry CSV 2 份，未找到 OPEN/PENDING |
| E5 | Python `os.walk("tests")` 掃描 `.py/.md/.toml/.ini/.cfg`，搜尋 todo/skip/skipif/xfail/SkipTest/expectedFailure | 掃描 58 檔、12 個文字命中、0 讀取錯誤；真正 skip 控制點 6 處；未找到 TODO 或 xfail |
| E6 | `openspec validate far-lane-remediation-20261021 --strict`；`printf 'OPENSPEC_EXIT=%s\n' "$?"` | **exit 1**；`ADDED "Pool rank order and role labels agree" must include at least one scenario` |
| E7 | Python 逐行讀 `var/FAR-REMEDIATION-20261021/RECEIPT.md` 與 `probes/AO_verdict.json` | receipt：KANBAN 7 cards、6 done；SWARM worker/AO 卡未收。AO raw attempt：rank 1、exit 1、usage_status 400、`Model is unavailable` |
| E8 | Python 逐行讀 `AGENTS.md`、指定 change 的 `tasks.md`、`tests/test_mandatory_tool_guard.py` | 下列項目附具體行號或原始值 |

> 限制：E2 是「可見檔案／命名指標」盤點，不是 acceptance 查核。REPORT、receipt 或 MANIFEST 存在，不代表已結案；其不存在也不代表沒有等價產物。遍歷期間其他程序仍可能寫入，檔案數不是凍結快照。

## 缺口分類

### A. 可直接關閉的缺口（附關閉動作與驗收條件）

此類指可開立明確、受限的修補工作，不代表本唯讀回合可直接寫入或自行驗收。

| 缺口描述 | 證據（命令＋值） | 建議關閉動作 | 驗收條件 | 預估阻力 |
|---|---|---|---|---|
| **A1：OpenSpec strict validation 確實失敗** | E6：exit **1**；`lane-routing/spec.md` 的 ADDED requirement `Pool rank order and role labels agree` 缺 Scenario | 在該 requirement 下補符合既定行為的 `#### Scenario:`；涵蓋 rank/role 一致與不一致情況，不放寬規則 | 同一條 `openspec validate far-lane-remediation-20261021 --strict` exit 0；解析結果保有預期 requirements/scenarios | 低 |
| **A2：最新 remediation 的執行紀錄與 checklist 未同步** | E3/E8：`far-lane-remediation-20261021/tasks.md:3–13` 共 **11** 項全未勾；E7 receipt:11–18 已記錄 P0–P4、fresh-session、local gates；E1 HEAD=`c442f07`，與 receipt 的 local commit 一致 | 逐項將 checklist 綁定既存 raw receipt／commit。可證明完成的實施項目才勾；`4.2 Independent AO` 保持未完成，不能以 local green 代替 | 每個勾選項目都有對應原始證據與主體版本；AO 未取得時仍明示 NOT accepted；不重跑已完成的 apply 只為勾清單 | 低 |
| **A3：supervisor recovery budget 尚有一項未關閉** | E3/E8：`lane-supervisor-windowless-convergence/tasks.md:18`，done **12**／pending **1**：`3.3 Separate the recovery budget from the trigger interval so a recovery attempt cannot drop the next trigger` | 先重導出現有實作與測試；若未實作，將 recovery budget 與 trigger interval 分開，加入 recovery 跨越下一個 trigger 的確定性測試 | 跨 trigger 的 recovery 不漏掉下一次觸發；正／負／邊界測試及獨立 checker 證據齊全後更新該項 | 中 |

### B. 需 owner 決策才能關閉的缺口（附決策選項與建議）

| 缺口描述 | 證據（命令＋值） | 建議關閉動作／決策選項 | 驗收條件 | 預估阻力 |
|---|---|---|---|---|
| **B1：工作樹尚有未落地、未處置候選產物** | E1：10 tracked 修改、300 untracked entries；另實跑 `git status --short -- scripts/hgk-lane-dispatch.py src/hg_kseos/lane_policy.py src/hg_kseos/lane_route_resolver.py scripts/runtime_role_binding_assert.py`，四者均為 `??` | 選項：分批 admitted landing／保留為 candidate／受控封存。**建議按產品碼、治理配置、證據、備份分批處置，不做 `git add .`，不刪不明來源產物** | 每個 entry 有 disposition、owner、對應 change；要落地的程式與測試可從乾淨 checkout 重現；排除秘密與 runtime DB | 中 |
| **B2：114 個 var 目錄尚無本次可證明的統一結案投影** | E2：112 有檔、2 空；80 有命名指標、32 無；E7 最新回合 receipt 仍記載 SWARM/AO 卡未收 | 選項：逐回合結案／具名 superseded／保留 deferred／判定非回合的 runtime/cache。**建議先辨認目錄用途，再將每回合對應 WO、verdict、result、卡片；禁止以 receipt 存在批次標 COMPLETED** | 每個實際回合都有終態或 owner-approved deferral；最新 SWARM 每卡有 result、阻斷原因或具名 supersession；不以歷史 receipt 代替 live card readback | 高 |
| **B3：其餘 OpenSpec 未結案組合需逐 change 定義處置** | E3：35 changes、471 未勾；扣除 A2/A3 對應兩個 changes，仍有 **33** 個有未勾項目；完整名稱與數量見後表 | 選項：繼續實施／證據對帳後結案／由 successor supersede／owner 明確拒絕或延期。**建議先按既有授權與 supersession 對帳，不能把所有舊 checklist 當成現行待實作需求** | 33 個 changes 均有具名 disposition；保留歷史 FAIL、未授權邊界與 successor 引用；實施項目依各自 tasks 原定驗收，不將全勾直接當 acceptance | 高 |
| **B4：跨 subject 的 evidence binding 缺口仍 OPEN** | E4：`TT_LEDGER.csv:11`，`HGK-EBC-TT-001`，status=`OPEN`、blocking=`false`；close_criteria 要求 evidence_refs 加 subject/requirement key，`resolve_acceptance` 拒絕別的 subject 的 evidence | owner 決定獨立 engineering-base ChangeSet 與 migration 範圍；建議做欄位／資料遷移及 fail-closed 驗證，不直接 SQL 改 canonical acceptance | 相同 subject 正例通過；不同 subject 的 evidence 被拒；缺 binding、舊資料與 rollback 都有測試及獨立判定；再依 typed API 更新 ledger 狀態 | 高 |
| **B5：idempotency TT 的「局部已解」與 general note 尚未裁定終態** | E4：`TT_LEDGER.csv:12`，`HGK-EBC-TT-002` status=`OPEN`；close_criteria 明載 acceptance path revision 3 已比對 entity_type/entity_id，但保留 general cross-entity contract note | 選項：只驗收 acceptance 範圍並另立 general issue／確認 general contract 後關閉／明確保留 OPEN。**建議拆清已解範圍與一般 namespace 合約，不憑文字 RESOLVED 自動改 CLOSED** | 有可重跑的跨 entity replay／collision 測試；owner 明訂剩餘 general contract 的處置；TT 不再同時模糊表示「已解」與「未解」 | 中 |
| **B6：PLAN／VERIFY 同模型是 owner-ordered 例外，不能當已滿足模型軸獨立** | E8：`AGENTS.md` current chain 明載 PLAN/VERIFY 同為 `gpt-6.1-sol`、`SOD006-C4 OPEN_OWNER_ORDERED`、process separation only；E7 receipt:14 同樣記錄 C4 OPEN | 選項：保留同模型並接受明確主張上限／授權不同模型 checker。**建議保持 owner 現行模型值不動，由 owner 決定何種獨立性足夠；不得為過 SoD gate 私改路由** | exception 有適用主體、範圍、owner、解除或重審條件；若要求模型獨立，提供不同模型實際 served 的 checker verdict；若保留例外，不宣稱 model-axis independence | 中 |

B3 中已有明確 owner／授權邊界的例子：

- `sod-independent-verify-enforcement/tasks.md:4–5`：canonical apply、`subject_digest` migration 兩項都明載 **owner gate — NOT executed**。
- `hgk-r10-session-closure-20261016/tasks.md:84–85`：221 cases／8 Gates／Fresh G1／DOC-05／release-publication、canonical registry rebind 均為 **OWNER-BLOCKED**。
- `gcm-noninteractive-default-containment/tasks.md:40,54–55,62–63,86,93–94`：L2 未 activation、無 collision-free post-fix measurement、positive credential control 未取得、曾超過 live-measurement 授權上限、缺不同模型獨立 verdict。建議 owner 分別裁定 activation、受控重測、歷史超權事件處置；**不以補文件消除既有 FAIL，也不在本回合讀取 credential**。
- `hgk-r11-session-handover-20261016/tasks.md:17`：R10 carry-over findings 尚缺 carried-over／re-measured 標示，可作為 B3 第一批低阻力對帳。
- `hgk-round3-lane-rebind-20261016/tasks.md:54`：R11「產品沒有 admission-receipt producer」仍列 OPEN；本次只確認該紀錄，**未重新證明程式實作不存在**。

### C. 依賴外部／上游的缺口（附解除條件）

| 缺口描述 | 證據（命令＋值） | 建議關閉動作 | 驗收條件／解除條件 | 預估阻力 |
|---|---|---|---|---|
| **C1：最新 remediation 的指定 AO 尚無成功 verdict** | E7：實讀 `probes/AO_verdict.json`：rank=1、model=`gpt-6.1-sol`、sandbox=`read-only`、exit=1、usage_status=400、`usage_receipt_ok=false`；stdout 含 `Provider error 400…Model is unavailable`。receipt:5 記載 WOs 仍 CREATED、未記錄 result | 在 owner 核定的同一 engine／wire／account 路徑做有界健康測試；恢復後重派 fresh read-only AO。若要換 arm，先取得符合目前 mandate 的授權，不靜默 fallback | 指定 checker 真正 served、usage receipt 成功、verdict 綁定凍結主體且非 skeleton；逐項 adjudicate，之後才記錄 WO result／canonical acceptance／完成卡片。**本次沒有 live 重測，不能斷言上游此刻仍故障，也不能由單筆 400 證明 transient 根因** | 高 |
| **C2：部分證據樹不可讀，全面盤點有實際存取阻斷** | E2：10,314 遍歷錯誤；Python 解析原輸出得 WinError **5：6,221** 次、WinError **3：4,093** 次。首次 `Path.rglob` 亦因 WinError 3 中止，改用保留錯誤的 `os.walk` 才完成頂層覆蓋 | 由產生證據的帳號／執行環境匯出必要 raw artifacts 至 owner 可讀的受控位置；WinError 3 逐項確認路徑問題或消失，不預設成同一根因；不自行 broaden permissions | 所有被正式引用的證據可由 checker 讀取、重算與重跑；不可恢復者具名標 INCONCLUSIVE／缺失，不補造結果；未納入驗收的 runtime/plugin 樹明確排除 | 高 |

C2 的實際拒絕範例：

```text
WinError 5:
var/FAR-REMEDIATION-AND-CLOSURE-20261016/lanes/VERIFY_SECURITY/V3c/work/TEST_RESULTS/hgk-effort-3hsz6_i5

WinError 3:
var/hgk-solution-apply-20261012/execute/homes/checker-option1/.tmp/plugins/plugins/nvidia/skills/omniverse-usd-performance-tuning/references/usd-structure-assessment/references/usd-hierarchy-dedupe-candidates/references
```

## OpenSpec 未關閉清單

證據：E3 的實際逐檔讀取。下列數字是 **未勾 checkbox 數**，不是已證明尚未實作的功能數。

| Change | 未勾數 | 處置入口 |
|---|---:|---|
| far-lane-remediation-20261021 | 11 | A2；AO 另依 C1 |
| gcm-noninteractive-default-containment | 8 | B3：activation／重測／授權與既有 FAIL 分別裁定 |
| hermes-incident-2026-10-05-repair | 35 | B3 |
| hgk-checker-upgrade-adapter | 23 | B3 |
| hgk-cnv-evidence-archive-r7r11-20261016 | 10 | B3 |
| hgk-cnv-far018-far019-archive | 5 | B3 |
| hgk-far-018-r7r11-residual-closure | 9 | B3 |
| hgk-far-019-owner-authorized-closure | 14 | B3 |
| hgk-far-remediation-20261016 | 25 | B3 |
| hgk-lane-brief-and-guard-hardening-20261015 | 22 | B3 |
| hgk-lane-reliability-closure-20261016 | 16 | B3 |
| hgk-plan-plane-rebind-20261015 | 5 | B3：served receipt、卡片、ACC11／Matrix／E11 |
| hgk-r10-session-closure-20261016 | 5 | B3：push／draft PR／VERIFY／owner gates |
| hgk-r11-session-handover-20261016 | 1 | B3：補 carry-over 對帳 |
| hgk-r8-eia-closure-skill-slim-20261016 | 22 | B3 |
| hgk-r9-far-residual-closure-20261016 | 5 | B3：candidate 重測／overlay／owner gates |
| hgk-round3-lane-rebind-20261016 | 1 | B3：admission-receipt producer 紀錄 |
| hgk-skill-convergence-20261014 | 13 | B3 |
| lane-health-repair-20261011 | 4 | B3 |
| lane-mandate-rebinding-and-d01-revocation | 27 | B3：保留原 D-01 bytes，對 successor／撤銷證據對帳 |
| lane-model-chain-rebind-20261015 | 13 | B3：依現行 owner chain 對帳，不重套舊 epoch |
| lane-sod-enforcement | 27 | B3 |
| lane-supervisor-windowless-convergence | 1 | A3 |
| lane-toolchain-identity-and-failure-classification | 9 | B3 |
| lane-verify-dual-routing-and-plan-high | 23 | B3：先裁定舊 effort／dual-arm 要求是否仍適用 |
| lane-verify-routing-remediation | 14 | B3 |
| pipd-r17-install-doc-identity-guard | 21 | B3 |
| pipd-repo-hygiene-and-handover-20261016 | 21 | B3 |
| pipd-s4r6-closeout-doc-identity-and-update-route | 23 | B3 |
| pipd-unmerged-candidate-merge-20261016 | 1 | B3：VERIFY verdict 逐字入包 |
| s4-final-pr18-closeout-20261016 | 1 | B3：verdict 與 same-model-axis disclosure |
| skill-mainfile-cap-remediation | 11 | B3 |
| sod-independent-verify-enforcement | 2 | B3：canonical apply／migration owner gate |
| strict-declaration-20261011 | 17 | B3 |
| verification-artifact-contract | 26 | B3 |

另兩個 active changes 的 checkbox 已全勾：

- `hgk-cnv-hygiene-readme-closure`：17 done。
- `hgk-cnv-owner-decision-main-landing`：11 done。

這只代表 checklist 全勾，**本次未證明 canonical acceptance 已完成**。

`openspec/changes/archive/` 實讀有：

```text
2026-10-10-ao-lane-independent-verify-20261010
```

## var 目錄盤點與比例

### 判讀

E2 實讀結果：

| 可見狀態 | 目錄數 | 占 114 個頂層目錄 |
|---|---:|---:|
| 有檔案，且有 REPORT／receipt／manifest 命名指標 | 80 | 70.18% |
| 有檔案，但無上述命名指標 | 32 | 28.07% |
| 空目錄 | 2 | 1.75% |
| 有可見檔案合計 | 112 | 98.25% |

比例由 Python 實算。

**不能誠實將 112：2 報成「有產出但未結案：根本沒產出」。** 因為頂層包含 runtime、cache、DB、backup；遞迴又會碰到工具／plugin 的 manifest；且部分路徑不可讀。精確的「有產出但未結案比例」仍需 B2 對帳，現有證據不足。

### 全部 114 個頂層目錄

以下為 E2 實跑列出的全部名稱，依命名指標分組；不是結案判定。

**有命名指標：80 個**

```text
__pycache__
a2
a3
backups
FABRIC-CLOSEOUT-20261013
FABRIC-OPEN-ITEMS-20261013
FABRIC-REPO-ASSESS-20261013
FABRIC-REPO-PUBLISH-20261013
far
far-ao-independence-20261010
far-exec-identity-001
far-exec-identity-002
far-execute-model-expansion
FAR-GOV-SKILLS-20261014
far-hermes-incident-rca-001
far-iao-lane-skip-20261012
FAR-LANE-ENFORCEMENT-RCA-20261015
far-lane-health-repair-20261011
FAR-LANE-REPAIR-20261014
FAR-LANE-REUSE-RCA-20261015
far-lane-route-slots-012
far-lane-sod-003
far-lane-sod-004
far-lane-sod-005
far-lane-sod-006
far-lane-sod-007
far-lane-sod-008-console-window-20261008
far-lane-sod-009-supervisor-governance-20261008
far-lane-sod-010-converge
far-lane-sod-011-router-window
far-lane-verify-002
FAR-LANE-VERSION-MIX-20261021
far-oauth-window-20261010
far-plan-enforcement-011
far-planning-intelligence-fit-012
FAR-REMEDIATION-20261021
FAR-REMEDIATION-AND-CLOSURE-20261016
FAR-RO-TOOLREFUSAL-20261014
FAR-STACK-HYGIENE-20261013
far-strict-declaration-20261011
far-swof-kseos-rca-001
far-verify-drift-20261012
far-verify-lane-noverdict-20261012
far-verify-model-misselection-20261012
far-w6-closure-decision-20261012
far-w6-mandate-alignment-20261012
far-w6-nextstep-decision-20261012
far-w6-plan-sod-reconciliation-20261012
fda
hermes-disposable
hgk-gcm-apply-20261013
hgk-gcm-containment-20261013
hgk-gcm-repair-20261013
hgk-gcm-repair2-20261013
hgk-solution-apply-20261012
LANE-ENFORCEMENT-APPLY-20261015
LANE-RELIABILITY-CLOSURE-20261016
lane-resolutions
lane-route-001
opencodex-backup
pciv
provider-failover-routing
R5R-20261014-s4-preview4-focused-close
R5S-20261015-s4-preview4-verify-close
R5Y-20261014-gpt-plugin-publication-recheck
R5Z-20261014-session-conformance
R6-20261014-far-remediation-and-repair
R7-20261014-merge-hygiene-closeout
repair
ROUND3-LANE-REBIND-AND-CLOSURE-20261016
rounds
rp002-stage1
SKILL-CONVERGENCE-20261014
swof-construction-002
swof-construction-002-w2
swof-construction-002-w2-repair-001
swof-precon-001
swof-w1-r4-evidence-cleanup
swof-w1-r4-final-closure
workbench
```

**有檔案但無上述命名指標：32 個**

```text
_SKCV_PUBLISH_20261014
cnv-ea-r7r11-20261016
codex-home-g3-003
codex-relay
far-018
far-019
far-doc-update-20261013
FAR-LANE-ROUTE-REBIND-20261015
far-pending-decisions-20261013
hermes-qualification
lane-health-20261011
modred
R5-20261014-s4-r4-closeout
R5-PREFLIGHT
R5R-20261014
R5R3-20261016-preview4-closeout
R5Y-20261014-gpt-plugin-publication
R5Z-20261014-session-conformance-arm3
R5Z-20261014-session-conformance-arm4
R5Z-20261014-session-conformance-arm5
R5Z-20261014-session-conformance-recheck
R6-CHKS
rbwi-fullrun-001
releases
research
rollback-proof
S4R3FAR-20261013-decision-and-handover
S4R3FAR-probe
S4R3X-20261013-f006-and-stageb-successor
shared-spine
SQS-THC-PUBLICATION-20261015
swof-construction-002-r4
```

**空目錄：2 個**

```text
codex-app-server-logs
wiki-rebuild
```

## Git 候選產物

E1 的 10 個 tracked 修改：

```text
README.md
config/hermes.json
config/lane-route-slots.candidate.json
config/project.json
docs/HG-KSEOS使用說明文檔.md
scripts/hermes-core.ps1
source-freeze/TT_LEDGER.csv
src/hg_kseos/knowledge.py
src/hg_kseos/spine.py
tests/test_task014_named_method_closure.py
```

300 個 untracked entries 包含以下實際看見的候選集合：

- 核心 lane 程式：`scripts/hgk-lane-dispatch.py`、`scripts/hgk-lane-guard.py`、`scripts/runtime_role_binding_assert.py`、`src/hg_kseos/lane_policy.py`、`src/hg_kseos/lane_route_resolver.py`、`src/hg_kseos/role_binding.py`。
- 驗證配置：`config/verify-acceptance-matrix.json`、`config/verify-lane-contract.json`、`config/ssot-supersession-ledger.json`。
- OpenSpec changes、specs、config；review evidence；多份 lane tests。
- `.bak-*` 備份、`config/.hermes.json.tmp-6b165178e1074dd2881ef74fc72dae0a`、`ck2.py`／`ck3.py`／`ck4.py` 等待判定產物。

**未檢查上述檔案完整內容，因此不宣稱它們全部適合提交或全部屬垃圾。** 四個 routing 檔首次納入 Git 已由 HEAD `c442f07` 證明；不得把舊回合「四檔均未追蹤」再列為現況。

## tests 標記盤點

初次 `search_files` 回傳 0；未採信該結果，改以 E5 Python 直接遍歷重測，取得 12 個文字命中。實際控制 skip 的 6 處：

| 位置 | 實讀條件 | 關閉／處置方案 |
|---|---|---|
| `tests/test_mandatory_tool_guard.py:51–52` | 找不到任何 known layout 的 `mandatory_tool_guard.py` 時 `raise unittest.SkipTest`，提示設定 `HERMES_AGENT_SRC` | 在指定驗收環境提供正確 source binding，要求此必要 suite 有實際執行結果；缺 binding 不計 green |
| `tests/w3_solution/test_code_page_independence.py:23` | 非 Windows 時 module `skipif`：需要 cmd.exe batch stub | Windows lane 執行；其他 OS skip 保留理由 |
| `tests/w3_solution/test_mandatory_defects.py:114` | 非 `GIT_BASH` 時 `pytest.skip("needs a POSIX shell")` | 在具備 POSIX shell 的 Windows lane 執行 |
| 同檔 `:172` | `@pytest.mark.skipif(not GIT_BASH, ...)` | 同上 |
| `tests/w3_solution/test_served_vs_declared_identity.py:23` | 非 `GIT_BASH` 時 module skip | 同上 |
| `tests/w3_solution/test_substitution_gate.py:20` | 非 `GIT_BASH` 時 module skip | 同上 |

**這些是條件式 coverage 邊界，不是本次已證明的測試失敗或實際 skipped 數。** 本回合未執行測試，未找到 TODO／xfail；其餘 6 個命中是說明文字或路徑，不列成缺陷。

## 統計

以本報告的**關閉工作包**為單位，不把 checkbox、目錄或歷史紀錄重複加總：

| 分類 | 項數 |
|---|---:|
| A．可開立明確受限修補 | 3 |
| B．需 owner 決策 | 6 |
| C．依賴外部／上游或證據存取環境 | 2 |
| **總計** | **11** |

底層盤點：37 active OpenSpec changes，其中35個有未勾項目、合計471個 checkbox；TT ledger 2個 OPEN；114個 var 頂層目錄；Git 10筆 tracked修改、300筆untracked entries。這些數字各自代表不同集合，**不相加成缺口總數**。

**優先順序：A1 修正 strict validation → A2 對帳已完成實施 → B1 凍結可重現候選主體 → C1 取得指定 AO verdict → 依 typed API 與各卡片結果完成結案。** 同時由 owner 裁定 B3/B4/B5/B6；C2 未解除的證據不得拿來支撐完整驗收。

本回合未建立或修改任何 repo 檔案；工具自動保存的長 stdout capture 位於 Hermes cache，不是治理交付物。