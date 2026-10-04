# 《fabric-desktop-automation》外部獨立 Challenge Review 驗收報告

```yaml
report_id: FDA_EXTERNAL_CHALLENGE_REVIEW_20260813_R1
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review
review_date: 2026-08-13
timezone: Asia/Taipei
target_blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2.md
submitted_evidence: FDA_IMPLEMENTATION_EVIDENCE.md
submitted_evidence_sha256: f3c7f5637f8861a20c17409d1c61e91ead4c290e4a999f0b7a86a2d8f815bd82
submitted_evidence_bytes: 19444
submitted_evidence_lines: 232
external_verdict: PARTIAL_CHALLENGE
external_acceptance: NOT_GRANTED
fda_blueprint: PASS
fda_profile_team_active: FAIL_CLOSED
sqs_live_trading: NOT_AUTHORIZED
production_autonomy: NOT_CLAIMED
remote_deployment: NOT_CLAIMED
product_rebuild_required: false
broad_rerun_required: false
recommended_resume: RESUME_SMALLEST_REPAIR
```

---

# 0. 最終外部裁決

## 0.1 一句話結論

本外部驗收官依 `challenge-review-SKILL.md` 的 clean-room、raw-evidence-first、maker != final checker、exact-subject binding、fail-closed 規則重新驗收後，裁決如下：

```text
FDA_BLUEPRINT = PASS

FDA_LOCAL_IMPLEMENTATION_PROGRESS
= SUBSTANTIAL / STRONGLY SUPPORTED BY SUBMITTED EVIDENCE INDEX
= NOT EXTERNALLY FINAL-ACCEPTED FROM RAW EVIDENCE

EXTERNAL_CHALLENGE = PARTIAL_CHALLENGE
EXTERNAL_ACCEPTANCE = NOT_GRANTED

FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO
SMALLEST_REPAIR = EVIDENCE_BINDING + TWO_FOCUSED_RUNTIME_GATES
```

核心原因不是 FDA 架構或主要施工方向錯誤，而是：

1. 本輪實際上傳給外部驗收官的 `FDA_IMPLEMENTATION_EVIDENCE.md` 是 **pointer-rich evidence index / summary**，不是 51 個 raw artifacts 本身；依 challenge-review 規則，不能把其中的 `PASS`、hash list、test count、checker verdict直接視為外部最終證據。
2. Submitted evidence 尚未提供一個足以讓外部 reviewer 對「exact frozen implementation subject」做單一 root binding 的 final candidate root，例如 final Git HEAD / package digest / canonical subject-root digest + EvidenceManifest root。
3. HERMES任務回報宣稱 `independent checker = 144/144`，但上傳的 canonical evidence MD 明載 `independent_checker.py = PASS, checks: 126, failed: 0`；外部驗收不能自行猜測哪一個 denominator 才是 current。
4. 藍圖 DoD-13 要求 `fabric-desktop-ufo2 valid/effective-load qualified`，但 evidence MD 明載 UFO² 僅完成 pinned candidate qualification，runtime effective-load 仍 `BLOCKED_HITL`，且「runtime not installed」仍列於 blocker。
5. 藍圖 DoD-17 要求「每個 mandatory XQ PAPER action class 都至少有一個 provider 10/10 fresh runs」；目前 `XQ_PAPER_CONFIG` 只有 radar surface open + 84-element UIA readback，沒有 PAPER strategy runtime start/stop，因此不得宣稱 DoD-17 完成。
6. Evidence MD 本身存在一個可確認的 evidence-report semantic defect：它一方面寫「DoD items 1–16 verified PASS」，另一方面又明確寫 UFO² effective-load 未完成。由於 DoD-13 位於 1–16，兩者不能同時成立。

因此，**HERMES最終回報中維持 `FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED` 的大方向是正確且符合治理的；但「內部 ALL PASS」只能解讀為 bounded local sub-gates 的內部完成，不得提升成 FDA Profile Team active 或外部 final acceptance。**

---

# 1. 驗收角色、方法與邊界

本次完整掛載並依 `challenge-review-SKILL.md` 執行。

## 1.1 Hard invariants

本外部驗收遵循：

- Existing PASS is claim, not evidence。
- 每個 verdict 必須綁 exact frozen subject。
- Maker 與 final checker 必須隔離。
- Candidate、evaluator、acceptance artifacts均 read-only。
- Raw deterministic evidence 優先於模型／HERMES摘要。
- 不把 file presence / install presence / UI presence當 runtime PASS。
- 不把 local/package qualification提升成 production authorization。
- 發現 defect 時只指定 earliest owner + smallest repair + focused retest，不替 candidate 修補。
- 不修改 acceptance predicate 讓 candidate 變綠。
- 金融／live trading 權威保留給 SQS domain authority；FDA 不得藉 desktop automation偷渡 broker-write authority。

## 1.2 本次外部 reviewer 實際可驗證範圍

本輪實際取得：

- `fabric-desktop-automation_藍圖_v2026.08.13-r2.md`
- `challenge-review-SKILL.md`
- `FDA_IMPLEMENTATION_EVIDENCE.md`
- 本專案中已掛載的 Fabric / HG-KSEOS / SQS / TW-ICT / XQ&XS operational / technical corpus

本輪**沒有實際取得** evidence MD 所列 51 個 artifact 的 raw bytes、current repository root、final package、raw test stdout、raw checker stdout/JSON、raw CAPC verification output、SharedSpine DB/readback、XQ fixture JSON receipts等。

因此本報告能做：

```text
blueprint acceptance reconstruction
claim consistency challenge
evidence-package integrity check
source/claim ceiling challenge
runtime blocker adjudication
smallest-repair planning
```

但不能誠實聲稱：

```text
51/51 raw artifact hashes independently recomputed
38/38 tests independently re-run
126/126 or 144/144 checker independently re-run
CAPC independently re-run
live XQ/UFO runtime independently replayed
```

---

# 2. Frozen subject / Evidence identity

## 2.1 Submitted evidence artifact

本外部 reviewer 對實際上傳的 `FDA_IMPLEMENTATION_EVIDENCE.md` 直接做 byte-level readback：

```text
SHA-256:
f3c7f5637f8861a20c17409d1c61e91ead4c290e4a999f0b7a86a2d8f815bd82

bytes:
19,444

lines:
232
```

這與 HERMES 回報中的 `sha256 f3c7f563...` 相符。

**External result：PASS — submitted evidence MD identity itself is verified。**

但此 SHA 只證明：

> 「本外部 reviewer 讀到的 MD 就是這一份 MD。」

它**不自動證明** MD 裡所列 51 個 artifacts、38 tests、checker、SharedSpine、XQ runtime receipt 的內容真實成立。

## 2.2 Missing exact candidate root

Evidence MD 提供：

- WO-FDA-001
- REQ-FDA-001
- TS-FDA-001
- CAPC contract hash
- 51 individual artifact hashes

但在本次 submitted external packet 中，未看到一個外部 reviewer可直接重算的：

```text
FINAL_GIT_HEAD
or
FINAL_PACKAGE_SHA256
or
CANONICAL_FDA_SUBJECT_ROOT_DIGEST
+
EVIDENCE_MANIFEST_ROOT_DIGEST
```

使 51 個 individual artifacts、tests、checker、runtime receipts全部被明確綁為「同一 frozen subject」。

因此 exact subject binding 尚未達 challenge-review final acceptance標準。

---

# 3. Authority / Claim Ceiling 重建

依 FDA r2：

```text
FDA = Fabric Shared Infrastructure Profile Team
team_id = fabric-desktop-automation
heavy_stack = false

profiles:
- fabric-desktop-cua
- fabric-desktop-ufo2

control:
HG-KSEOS = sole normative control plane
Hermes = runtime/orchestration/Kanban/Profile
WorkOrder = normative task truth
Acceptance Officer = verify-only independent checker
```

Hard architecture invariants：

```text
NO_THIRD_HEAVY_STACK
NO_SECOND_SCHEDULER
NO_SECOND_TASK_DB
NO_SECOND_REDUCER
NO_SECOND_KNOWLEDGE_PLATFORM
NO_PARALLEL_TASK_AUTHORITY
ONE_ACTIVE_DESKTOP_WRITER
READBACK_BEFORE_SAFE_FAILOVER
NO_SELF_ACCEPT
NO_SELF_PROMOTE
NO_CREDENTIAL_AUTOMATION
NO_SQS_LIVE_BROKER_WRITE
```

XQ/SQS current ceiling：

```text
FDA_V1 = LOCAL / PAPER / SHADOW / NO-LIVE-WRITE
SQS_LIVE_TRADING = NOT_AUTHORIZED
```

Future：

```text
Human Entry Approval
→ frozen XScript mechanically manages position lifecycle
```

是 separate SQS ChangeSet 的 future compatibility，不屬於本次 FDA v1 active claim。

---

# 4. Blueprint DoD 36 predicates 外部驗收矩陣

狀態定義：

- `SUPPORTED_SUMMARY_ONLY`：submitted evidence有明確 claim / hash pointer，但 raw artifact未交付給本外部 reviewer。
- `BLOCKED_RUNTIME`：submitted evidence明確承認 runtime gate尚未完成。
- `PARTIAL`：只完成 predicate 的部分語義。
- `EVIDENCE_GAP`：外部 reviewer缺足以重建 hard PASS 的 raw evidence。
- `NOT_CLAIMED`：不屬本次 active claim。
- `PASS_EXTERNAL_READBACK`：本外部 reviewer本輪能直接重算。

| DoD | Predicate | External adjudication | 說明 |
|---:|---|---|---|
| 01 | current Fabric/HGK/RP002 authority fresh-bound | SUPPORTED_SUMMARY_ONLY | C0 readback receipt只有 hash/index，raw bytes未附 |
| 02 | Prompt Compiler C0-C9 + lint PASS | SUPPORTED_SUMMARY_ONLY | CAPC hash與PASS claim存在；未外部 rerun |
| 03 | no new RP002 Gate | SUPPORTED_SUMMARY_ONLY | checker claim存在；machine truth raw diff未附 |
| 04 | heavy stacks exactly HGK + SQS | SUPPORTED_SUMMARY_ONLY | negative claim合理；parent matrix raw bytes未附 |
| 05 | no second scheduler/task DB/reducer/KG | SUPPORTED_SUMMARY_ONLY | architecture方向正確；raw tree/diff未附 |
| 06 | shared-infra schema resolution PASS | SUPPORTED_SUMMARY_ONLY | CR_OPEN-FDA-001 claim CLOSED；raw manifest未附 |
| 07 | one canonical FDA Team artifact | SUPPORTED_SUMMARY_ONLY | TEAM.md hash存在 |
| 08 | Team refs/assignee/router/knowledge/interop/acceptance exact | SUPPORTED_SUMMARY_ONLY | checker claim；raw TEAM/manifest未附 |
| 09 | canonical FDA Desktop Capability Matrix PASS | SUPPORTED_SUMMARY_ONLY | matrix hash存在；raw matrix未附 |
| 10 | parent tool rows missing = 0 | SUPPORTED_SUMMARY_ONLY | checker claim；raw parent/child matrices未附 |
| 11 | FDA exact-set tool rows missing = 0 | SUPPORTED_SUMMARY_ONLY | checker claim；raw exact-set未附 |
| 12 | Cua valid/effective-load qualified | SUPPORTED_SUMMARY_ONLY | evidence claim = cua-driver 0.19.3 doctor/UIA; receipt raw bytes未附 |
| 13 | UFO² valid/effective-load qualified | **BLOCKED_RUNTIME** | evidence明載 effective-load `BLOCKED_HITL` 且 runtime not installed |
| 14 | both providers exact-pinned + disable/rollback | PARTIAL / SUMMARY_ONLY | UFO² pin有，但 active runtime qualification未完成 |
| 15 | parent ExecutionBinding/2 validates; no schema fork | SUPPORTED_SUMMARY_ONLY | binding hash/claim存在；raw schema validation未附 |
| 16 | idempotency/replay/prior-effect PASS | SUPPORTED_SUMMARY_ONLY | lease concurrency摘要有；raw receipt未附 |
| 17 | every mandatory XQ PAPER action class >=1 provider 10/10 | **PARTIAL / BLOCKED_RUNTIME** | F01/F06已有10/10；PAPER strategy start/stop未執行 |
| 18 | wrong_action = 0 | EVIDENCE_GAP | F01明載0；全部mandatory action class denominator尚未閉合 |
| 19 | silent_wrong_action = 0 | EVIDENCE_GAP | 同上 |
| 20 | simultaneous desktop writers = 0 | SUPPORTED_SUMMARY_ONLY | 4/4 concurrency summary；raw receipt未附 |
| 21 | unknown-state failover/replay = 0 | SUPPORTED_SUMMARY_ONLY | summary稱 unknown-state replay BLOCKED；DoD pass list卻漏列21 |
| 22 | duplicate side effect on retry/reclaim = 0 | EVIDENCE_GAP | DoD pass list漏列22；raw prior-effect/duplicate receipt未附 |
| 23 | credential/secret access = 0 | SUPPORTED_SUMMARY_ONLY | no-secret checker claim；raw security output未附 |
| 24 | unauthorized network desktop control = 0 | SUPPORTED_SUMMARY_ONLY | summary claim；raw socket/network negative evidence未附 |
| 25 | SQS live broker write = 0 | EVIDENCE_GAP | authority是NOT_AUTHORIZED，但 run-level write_count raw evidence未附；DoD pass list漏列25 |
| 26 | Knowledge candidate/approved/ACL semantics PASS | SUPPORTED_SUMMARY_ONLY | KG1 mapping claim；raw ACL fixtures未附 |
| 27 | WO→Binding→Hermes/Kanban→Profile→provider trace proven | SUPPORTED_SUMMARY_ONLY | SharedSpine/route claim；raw trace未附 |
| 28 | OASF/ContextForge/MCP/A2A qualified or exact N/A | SUPPORTED_SUMMARY_ONLY | disposition claim；raw promotion lineage未附 |
| 29 | OTel parent disposition preserved | SUPPORTED_SUMMARY_ONLY | summary=`INHERIT_CONDITIONAL_EMBEDDED` |
| 30 | interop same-subject drift = 0 | EVIDENCE_GAP | final subject-root仍未外部重建 |
| 31 | unaudited governed-path bypass = 0 | SUPPORTED_SUMMARY_ONLY | security/checker claim；raw negative test未附 |
| 32 | open BreakGlass = 0 | SUPPORTED_SUMMARY_ONLY | summary claim；raw current counter未附 |
| 33 | independent Acceptance Officer PASS | **EVIDENCE_GAP** | 126 vs 144 denominator conflict；raw checker receipt/identity/isolation未附 |
| 34 | rollback PASS | SUPPORTED_SUMMARY_ONLY | rollback plan存在；actual rollback readback raw未附 |
| 35 | HGK/SQS consumer binding current | PARTIAL / EVIDENCE_GAP | XQ product version drift存在；需要 exact current binding raw readback |
| 36 | docs/AGENTS/README current | SUPPORTED_SUMMARY_ONLY | current patched bytes / readback未附 |

結論：

```text
DoD 36/36 externally closed = NO
DoD 13 = BLOCKED
DoD 17 = PARTIAL/BLOCKED
DoD 33 = external evidence gap
DoD exact denominator mapping = internally inconsistent
```

因此：

```text
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED
```

是唯一合規結論。

---

# 5. Findings

## EXT-FDA-001 — Exact frozen subject root未交付

```yaml
classification: EVIDENCE_GAP
blocking: true
acceptance_edges:
  - DoD-09
  - DoD-15
  - DoD-27
  - DoD-30
  - DoD-33
earliest_owner: FDA_EVIDENCE_PACKAGER / HGK_SHAREDSPINE_EVIDENCE_OWNER
smallest_repair: MATERIALIZE_ONE_CANONICAL_SUBJECT_ROOT_AND_EVIDENCE_MANIFEST_BINDING
focused_retest:
  - final head/package/subject root
  - all 51 hashes bound to same root
  - checker bound to same root
  - runtime receipts bound to same root
affected_regression: evidence-binding only
product_rebuild_required: false
```

### 判定

Individual file hashes不能取代 final subject identity。

---

## EXT-FDA-002 — 51 raw artifacts沒有提交給外部 reviewer

```yaml
classification: EVIDENCE_GAP
blocking: true
acceptance_edges:
  - DoD-01..36 as applicable
earliest_owner: FDA_EVIDENCE_PACKAGER
smallest_repair: PROVIDE_RAW_REVIEW_BUNDLE_OR_RAW_BLOCKING_ARTIFACT_SET
focused_retest:
  - rehash current bytes
  - rerun 38 tests
  - rerun checker
  - rerun CAPC
  - inspect live fixture receipts
affected_regression: none unless raw evidence contradicts summary
product_rebuild_required: false
```

### 判定

`FDA_IMPLEMENTATION_EVIDENCE.md` 是良好的 external review index，但不能替代 raw receipts。

---

## EXT-FDA-003 — Independent checker denominator / identity conflict

HERMES回報：

```text
independent checker = 144/144 PASS
```

submitted evidence：

```text
independent_checker.py
verdict = PASS
checks = 126
failed = 0
```

```yaml
classification: EVIDENCE_GAP
blocking: true
acceptance_edge: DoD-33
earliest_owner: FDA_ACCEPTANCE_EVIDENCE_OWNER
smallest_repair: FRESH_SUBJECT_BOUND_CHECKER_RECEIPT
focused_retest:
  - checker script SHA
  - candidate subject digest
  - exact denominator
  - pass/fail/error
  - exit status
  - verify-only/no-write
  - maker/checker session isolation
  - raw output digest
affected_regression: none
```

### 判定

外部 reviewer目前只能採 `126` 作 submitted canonical evidence的 denominator；`144` 為 unsupported summary claim，除非有更新後 raw receipt。

---

## EXT-FDA-004 — Evidence MD 的 DoD pass-list 自我矛盾

Evidence MD 寫：

```text
DoD items 1-16 verified PASS
```

同一份 evidence MD 又寫：

```text
FDA_UFO2_QUALIFICATION
= QUALIFIED_CANDIDATE_PIN_ONLY
effective-load = BLOCKED_HITL

UFO2 runtime not installed
```

而 blueprint DoD-13 明確要求：

```text
fabric-desktop-ufo2 valid/effective-load qualified
```

此外 pass-list漏列：

```text
21
22
25
```

但正文其他段落又似乎對這些 predicate給出部分 supporting claim。

```yaml
classification: CONFIRMED_DEFECT
blocking: true
defect_scope: EVIDENCE_REPORT_SEMANTICS_ONLY
acceptance_edges:
  - DoD-13
  - DoD-21
  - DoD-22
  - DoD-25
earliest_owner: FDA_EVIDENCE_REDUCER
smallest_repair: REGENERATE_DOD_MATRIX_FROM_MACHINE_PREDICATES
focused_retest:
  - 36-row exact denominator
  - no omitted IDs
  - blocked/partial/pass cannot conflict with claim ceiling
  - generated twice -> deterministic normalized payload
affected_regression: evidence/report only
product_rebuild_required: false
```

### 判定

這是目前唯一可直接確認的「實質 defect」，但它是 evidence report semantics defect，不是 FDA architecture/product defect。

---

## EXT-FDA-005 — UFO² effective-load未完成

```yaml
classification: EVIDENCE_GAP
blocking_for: FDA_PROFILE_TEAM_ACTIVE
acceptance_edge: DoD-13
earliest_owner: FDA-UFO2 Profile owner / admitted HGK WorkOrder
smallest_repair: HUMAN_GATE_CREDENTIAL_THEN_EFFECTIVE_LOAD_QUALIFICATION
focused_retest:
  - exact pinned distribution
  - credential supplied by HumanGate only
  - effective-load
  - bounded WorkOrder scope
  - target-only desktop permission
  - network deny
  - failure/degraded
  - disable/rollback
  - independent receipt
affected_regression:
  - provider routing matrix
  - interop subject binding if promoted
product_rebuild_required: false
```

### 判定

這是合法 HumanGate blocker，不應為了「全綠」要求 FDA 自行配置 API key。

---

## EXT-FDA-006 — XQ PAPER action class未完成 runtime closure

Evidence只證明：

```text
策略雷達 surface open
84-element UIA readback
no mutation
```

但 blueprint current allowed/qualification actions包含：

```text
configure PAPER strategy/radar
start/stop PAPER runtime
readback
```

```yaml
classification: EVIDENCE_GAP
blocking_for: FDA_PROFILE_TEAM_ACTIVE
acceptance_edge: DoD-17
earliest_owner: SQS/XQ PAPER fixture authority + FDA Cua profile
smallest_repair: ADMIT_ONE_NO_LIVE_WRITE_PAPER_FIXTURE_AND_RUN_FOCUSED_10X
focused_retest:
  - paper config
  - start
  - status readback
  - stop
  - post-stop readback
  - 10 fresh runs
  - wrong_action=0
  - silent_wrong_action=0
  - broker_write=0
affected_regression:
  - XQ PAPER action-class matrix row
  - router preference row
product_rebuild_required: false
```

### 判定

不需要 live trading authorization；只需要 SQS/XQ domain authority對 **PAPER/no-live-write fixture** 明確 admission。

---

## EXT-FDA-007 — Cua UIA Invoke deadlock workaround

```yaml
classification: NON_BLOCKING_OBSERVATION
blocking: false
risk_ref: R-FDA-011
observation: cua-driver 0.19.3 UIA Invoke deadlocks on XQ Afx button
current_workaround:
  - pixel click
  - clipboard ctrl+v
  - Ctrl+Tab
external_condition:
  - must remain explicit in matrix/provider evidence
  - no silent fallback
  - version-bound qualification required
```

### 判定

藍圖 readback hierarchy本來就允許 pixel/coordinate作最後 fallback；只要：

```text
wrong_action = 0
silent_wrong_action = 0
readback exists
provider/action-class route explicit
```

此 workaround 不必阻擋局部 Cua qualification。

---

## EXT-FDA-008 — XQ version identity drift要保持單一 current subject

Evidence中同時有：

```text
exe file version = 1.10.0.0
live product version = 3.20.02 (260811)
```

```yaml
classification: NON_BLOCKING_OBSERVATION
blocking: false_if_current_rows_rebound
risk_ref: R-FDA-013
required_rule: application.version must use one current canonical live product identity for selector-bound qualification
focused_check:
  - all current 10/10 receipts show 3.20.02 subject where applicable
  - stale selector-bound rows invalidated/requalified
  - 1.10.0.0 retained only as file-version metadata, not promoted runtime identity
```

### 判定

Evidence表示已做 version correction；外部 raw receipt仍需驗證。

---

# 6. 對 HERMES「內部 ALL PASS」回報的逐項工程鑑定

| HERMES claim | External verdict | 說明 |
|---|---|---|
| F01 10/10 | NOT_OVERTURNED / RAW_PENDING | summary與hash pointer完整，尚未 raw replay |
| F03 editor open | NOT_OVERTURNED / RAW_PENDING | 合理且符合 readback hierarchy |
| F06 10/10 compile | NOT_OVERTURNED / RAW_PENDING | CrossOver function form路徑合理；raw receipt未附 |
| F07 compile fail readback | NOT_OVERTURNED / RAW_PENDING | negative fixture設計正確 |
| F09 PAPER config | **DOWNGRADE TO QUALIFIED_SURFACE ONLY** | 目前只有 radar surface/readback，不是完整 runtime config/start/stop |
| F10/F11 | NOT_OVERTURNED / RAW_PENDING | log/export readback符合設計 |
| bounded control | NOT_OVERTURNED / RAW_PENDING | notepad probe是合理的 non-financial local reversible canary |
| lease 4/4 | NOT_OVERTURNED / RAW_PENDING | 對 one-writer/unknown-state有價值 |
| unit+integration 38/38 | SUMMARY CLAIM / RAW MISSING | 不能由本外部 reviewer重跑 |
| checker 144/144 | **NOT ACCEPTED** | submitted evidence canonical denominator = 126 |
| checker 126/126 | SUMMARY CLAIM / RAW MISSING | 可作 current submitted denominator，但尚未 raw re-run |
| CAPC PASS | SUMMARY CLAIM / RAW MISSING | contract hash存在，未重跑 |
| HGK doctor PASS | SUMMARY CLAIM / RAW MISSING | 未提供 raw doctor output |
| 51/51 embedded hash match | SUMMARY CLAIM / RAW MISSING | 只拿到hash表，未拿到51 raw files |
| 4-way mirror equality | UNVERIFIED | current submitted packet沒有四份 mirror raw bytes |
| UFO² pin | NOT_OVERTURNED | pin本身可成立，但不能升成 effective-load |
| FDA_PROFILE_TEAM_ACTIVE FAIL_CLOSED | **CONFIRMED CORRECT CLAIM CEILING** | DoD-13/17未閉合 |
| SQS_LIVE_TRADING NOT_AUTHORIZED | **CONFIRMED CORRECT CLAIM CEILING** | 與 FDA blueprint/domain boundary一致 |

---

# 7. Gate Calibration Failure Defense

## 7.1 Objective alignment

PASS。

FDA的產品目標是「受治理的 Windows desktop shared capability」，不是自動交易 authority。

目前 evidence沒有把：

```text
UI control success
```

誤升成：

```text
Financial Truth
live trading permission
```

這是正確的目標對齊。

## 7.2 Risk-proportionate strictness

PASS with blockers preserved。

UFO² API key被視為 credential/HumanGate，不允許 agent自填，是正確的 fail-closed。

PAPER runtime需要 SQS/XQ authority admission，也不應被 FDA 自己越權關閉。

## 7.3 Positive / Negative coverage

設計上覆蓋度良好，包括：

```text
positive:
launch
editor
compile good
radar/readback
log/export
bounded control

negative:
compile bad
second writer
unknown state
secret
network
self promotion
broker write
BreakGlass bypass
```

但 external reviewer尚未取得 raw receipts，因此只能評為「coverage design good / raw verification pending」。

## 7.4 False-positive defense

目前最大的 false-positive 風險是：

```text
summary PASS
→ treated as external PASS
```

challenge-review明確禁止，因此本報告維持 PARTIAL。

## 7.5 Anti-overfitting

F01/F06有 10 fresh runs是好方向；但不能只用已通過的 action classes推論全部 XQ PAPER action class已完成。

因此 DoD-17仍必須 focused close。

## 7.6 HITL / domain boundary

PASS。

- UFO² key → HumanGate
- PAPER execution → SQS/XQ authority
- live broker write → NOT_AUTHORIZED
- future semi-auto → separate SQS ChangeSet

沒有必要也不應為了驗收改寫此邊界。

---

# 8. 外部接受狀態字典

```yaml
FDA_BLUEPRINT:
  verdict: PASS

FDA_PROFILE_TEAM_MATERIALIZATION:
  external_status: NOT_OVERTURNED_BUT_RAW_NOT_REVIEWED

FDA_DETERMINISTIC_ROUTER:
  external_status: NOT_OVERTURNED_BUT_RAW_NOT_REVIEWED

FDA_CUA_INSTALL_EFFECTIVE_LOAD:
  external_status: NOT_OVERTURNED_BUT_RAW_NOT_REVIEWED

FDA_XQ_LAUNCH_LOCATE:
  external_status: NOT_OVERTURNED_BUT_RAW_NOT_REVIEWED

FDA_XS_COMPILE_PASS:
  external_status: NOT_OVERTURNED_BUT_RAW_NOT_REVIEWED

FDA_XS_COMPILE_FAIL_READBACK:
  external_status: NOT_OVERTURNED_BUT_RAW_NOT_REVIEWED

FDA_XQ_PAPER_CONFIG:
  external_status: QUALIFIED_SURFACE_ONLY

FDA_UFO2_QUALIFICATION:
  external_status: PIN_ONLY_BLOCKED_HITL

FDA_PROFILE_TEAM_ACTIVE:
  external_status: FAIL_CLOSED

EXTERNAL_CHALLENGE:
  verdict: PARTIAL_CHALLENGE

EXTERNAL_ACCEPTANCE:
  verdict: NOT_GRANTED

SQS_LIVE_TRADING:
  verdict: NOT_AUTHORIZED

PRODUCTION_AUTONOMY:
  verdict: NOT_CLAIMED

REMOTE_DEPLOYMENT:
  verdict: NOT_CLAIMED
```

---

# 9. 最小續跑／修補方案

不建議 broad rerun，也不建議重構 Fabric/HGK/Hermes/FDA。

## Track A — Evidence-only external closure

只補：

```text
A1. Freeze one exact FDA candidate identity:
    final HEAD/package or canonical subject root

A2. Materialize EvidenceManifest root:
    bind all 51 artifact hashes to same subject

A3. Provide raw blocking evidence:
    - exact TEAM / manifest / capability matrix
    - execution binding
    - tool matrices
    - 38-test raw stdout/exit
    - independent checker raw receipt
    - CAPC raw receipt
    - live fixture JSON receipts
    - rollback/readback
    - BreakGlass/security/no-live evidence

A4. Resolve checker denominator:
    126 or 144 — one current value only

A5. Regenerate DoD-36 machine matrix:
    no omitted 21/22/25
    DoD-13 = BLOCKED until UFO2 closes
    DoD-17 = PARTIAL until PAPER runtime closes

A6. Re-hash regenerated external evidence MD
    and verify mirror equality if mirrors are still current policy
```

## Track B — Runtime focused closure

### B1 UFO²

```text
Human supplies credential through admitted HumanGate
→ install/effective-load exact v3.0.8
→ bounded scope
→ target-only
→ network deny
→ fail/degrade
→ rollback
→ independent receipt
```

### B2 XQ PAPER

```text
SQS/XQ authority admits no-live-write PAPER fixture
→ config
→ start
→ status readback
→ stop
→ final readback
→ 10 fresh runs
→ wrong_action = 0
→ silent_wrong_action = 0
→ broker_write = 0
```

## Track C — Focused external re-review

只重驗：

```text
DoD-13
DoD-17
DoD-18/19 as affected by new PAPER runs
DoD-30 same-subject binding
DoD-33 checker identity/denominator
DoD-35 current XQ binding if version-dependent
DoD-36 only if docs refreshed
EvidenceManifest / subject-root / final MD
```

其餘 unaffected passing edges不需重跑整個 RP-002 或重建 FDA。

---

# 10. 是否需要產品重做／重構

```text
PRODUCT_REBUILD_REQUIRED = NO
FABRIC_REDESIGN_REQUIRED = NO
HGK_REDESIGN_REQUIRED = NO
FDA_ARCHITECTURE_REWRITE_REQUIRED = NO
```

理由：

- Shared Infrastructure Profile Team架構仍是最合適的 reuse-first方案。
- Cua primary + UFO² specialist 的 provider abstraction仍合理。
- one-writer lease、known-state failover、readback hierarchy、Knowledge ACL、SoD、PAPER/no-live ceiling都符合成熟工程做法。
- 本輪發現的最大問題是 external evidence reproducibility / denominator consistency，而不是 architecture no-fit。
- Runtime剩餘兩 gate均可 focused close，不需要另建新 scheduler、RAG、router、Heavy Stack或第三 runtime。

---

# 11. 最終 Stop Condition

只有在下列全部成立後，本外部 reviewer才會考慮：

```text
PASS_CHALLENGE
```

必要條件：

```text
exact frozen FDA subject root = verified
raw blocking evidence available
all required artifact hashes recomputed
test command/denominator/exit verified
checker denominator unique/current
maker != checker isolation verified
DoD-36 mapping deterministic and contradiction-free

UFO2 effective-load = PASS
mandatory XQ PAPER action classes = >=1 provider 10/10
wrong_action = 0
silent_wrong_action = 0

credential/secret = 0
unauthorized network = 0
broker_write = 0
open BreakGlass = 0

rollback = PASS
current consumer binding = PASS
docs current = PASS

blocking contradiction = 0
blocking evidence gap = 0
```

即使未來：

```text
FDA_PROFILE_TEAM_ACTIVE = PASS
```

仍不得推論：

```text
SQS_LIVE_TRADING = AUTHORIZED
PRODUCTION_AUTONOMY = PASS
REMOTE_DEPLOYMENT = PASS
```

這些是不同 authority / acceptance scope。

---

# 12. 最終外部驗收結論

> 《fabric-desktop-automation_藍圖_v2026.08.13-r2》的架構設計仍可維持 **PASS**；HERMES目前完成了大量有價值的 local implementation、Cua/XQ runtime qualification、one-writer/recovery、安全與 evidence materialization 工作，且沒有看到需要重構 FDA 的證據。
>
> 但是，依 `challenge-review-SKILL.md`，本次實際交付給外部 reviewer 的是單一 pointer-rich evidence MD，而不是其所列 raw evidence bundle，因此無法把 local `38/38`、checker `126/126`、51 artifacts、CAPC、SharedSpine、live fixtures直接重判為 external raw-evidence PASS。
>
> 此外，UFO² effective-load與 XQ PAPER runtime仍明確未閉合，所以 `FDA_PROFILE_TEAM_ACTIVE` 必須保持 **FAIL_CLOSED**。Evidence MD 的 DoD pass-list還有「1–16 PASS」與 DoD-13 blocked互相矛盾，以及 21/22/25漏列的 evidence-reducer問題。
>
> 因此，本輪唯一符合工程專業、治理契約與 fail-closed原則的外部裁決是：

```text
EXTERNAL_CHALLENGE = PARTIAL_CHALLENGE
EXTERNAL_ACCEPTANCE = NOT_GRANTED

FDA_BLUEPRINT = PASS
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

REPAIR_MODE = RESUME_SMALLEST_REPAIR
PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO
```

下一次只需：

```text
1. 補 exact subject + raw review bundle + checker denominator closure
2. 完成 UFO² effective-load
3. 完成 XQ PAPER no-live runtime 10x focused qualification
4. focused external re-review
```

不應重做已封閉的 RP-002，也不應把 evidence gap擴張成 Fabric/HGK/FDA大重構。

---

# 13. Source Locator Register

## Primary normative / acceptance

- `fabric-desktop-automation_藍圖_v2026.08.13-r2.md`
  - §1.1 Blueprint claim ceiling
  - §1.2 r2 non-regression contract
  - §5.2–§5.16 architecture/runtime/security/XQ contracts
  - §6.4 XQ qualification harness
  - §6.7 Test Tracking List
  - §10.1 FDA_PROFILE_TEAM_ACTIVE DoD 36
  - §10.2 separate semi-auto compatibility claim
  - §11 final architecture/provider/knowledge/XQ verdicts

- `challenge-review-SKILL.md`
  - Role
  - Invariants 1–10
  - Intake
  - Workflow 1–5
  - PASS_CHALLENGE / PARTIAL_CHALLENGE / FAIL_CHALLENGE / TEMP_CLOSED_CHALLENGE

## Submitted evidence

- `FDA_IMPLEMENTATION_EVIDENCE.md`
  - §0 Claim ceiling
  - §1 Governance binding
  - §2 Execution surfaces
  - §2A Live desktop runtime evidence
  - §3 Materialized artifacts
  - §4 Independent checker
  - §5 CR_OPEN closure
  - §6 XQ/SQS consumer ceiling
  - §7 Interop/OTel/BreakGlass
  - §8 Known runtime blockers
  - §9 Rollback
  - §10 External verifier checklist

## Supporting project authority

- `Fabric使用說明文檔(2).md`
- `HG-KSEOS使用說明文檔(20260813-052051).md`
- `SQS-THC_TW-ICT_FSDT-Stack使用說明文檔(6).md`
- `XQ&XS_專業技術文檔_DOC-00~13`
- `TW-ICT_RBWI_v3.0.0_r2_2026-07-30(1).md`
- `Spartoi｜台股當沖/隔日沖_RUNBOOK/WI_v2.0.0(2).md`

---

**END OF EXTERNAL CHALLENGE REVIEW**
