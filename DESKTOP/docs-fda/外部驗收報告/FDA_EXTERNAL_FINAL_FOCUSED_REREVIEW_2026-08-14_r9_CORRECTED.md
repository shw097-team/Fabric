# 《fabric-desktop-automation》外部驗收方法校正暨新版最終驗收報告

```yaml
report_id: FDA_EXTERNAL_FINAL_REREVIEW_20260814_R9_CORRECTED
report_status: SUPERSEDES_R9
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review + gate-calibration correction
review_time_local: 2026-08-14T15:56:00+08:00

target:
  component: fabric-desktop-automation
  blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2.md
  submitted_final_evidence: FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md

method_correction:
  moving_goalpost_frozen: true
  candidate_evidence_root_separation: true
  evaluator_identity_separated: true
  single_wash_explicit_manual_stop_10x_required: false
  new_gate_after_this_report: prohibited

revised_verdict:
  external_challenge: PARTIAL_CHALLENGE
  external_acceptance: NOT_GRANTED_YET
  fda_blueprint: PASS
  fda_runtime_qualification: PASS_CANDIDATE
  fda_local_implementation: PASS_CANDIDATE
  fda_profile_team_active: FAIL_CLOSED_EVIDENCE_RESEAL_ONLY
  confirmed_product_architecture_defect: 0
  confirmed_runtime_repair_required: 0

remaining_work:
  class: EVIDENCE_RESEAL_ONLY
  candidate_mutation_allowed: false
  runtime_rerun_required: false
  broad_rerun_required: false

claim_ceiling:
  sqs_live_trading: NOT_AUTHORIZED
  production_autonomy: NOT_CLAIMED
  remote_deployment: NOT_CLAIMED
```

---

# 0. 本報告的效力

本報告**正式取代 / supersede**：

```text
FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_2026-08-14_r9.md
```

原因不是執行方新增了新的產品修補，而是外部驗收官對前序驗收方式完成 Gate Calibration 自我勘誤。

本次修正兩項過度或結構性不佳的驗收方式：

1. 不再把「candidate root」與「後生成 evidence / checker / external report」綁成同一會持續變動的 git/evidence root；
2. 不再把 XQ `single-wash` 情境的自動停止，額外要求成「explicit manual STOP 10x」才算通過。

`challenge-review` 本身要求：
- acceptance predicate必須由 frozen authority推導，不可由 reviewer隨輪次漂移；
- deterministic mismatch從 subject-bound evidence裁決；
- unresolved domain truth才交 domain authority；
- gate calibration必須避免 false-positive、false-negative、overfitting；
- confirmed defect只能要求 smallest legal repair。

因此本次校正符合 `challenge-review`，而不是放寬其核心證據要求。

---

# 1. 根因回顧：為什麼 R2–R9 一直循環

## 1.1 主要結構性問題

前序驗收實務反覆使用：

```text
final subject = whole Fabric git HEAD
```

同時又把：

```text
EvidenceManifest
checker receipt
runtime receipt
external evidence MD
repair report
```

寫回同一 repository。

結果形成：

```text
freeze HEAD A
→ run checker
→ add checker/evidence
→ HEAD becomes B
→ prior checker appears stale
→ rerun checker
→ add new receipt
→ HEAD becomes C
→ repeat
```

這是 **self-invalidating evidence topology**。

因此，前序「每補 evidence一次、subject又變一次」不能全部歸類成 candidate defect。

---

# 2. 新版固定驗收模型：NO-MOVING-GOALPOST CONTRACT

自本報告起，FDA final acceptance採以下固定三層 identity。

## 2.1 Candidate Root

```yaml
candidate_root:
  type: IMMUTABLE_IMPLEMENTATION_SUBJECT
  legacy_reference: be576bebe7672093039bfe7dbc265f25aa0a1164
  mutation_after_freeze: DENY
```

Candidate Root代表被驗收的 FDA implementation / governance / runtime contract狀態。

**後續 evidence reseal不得再修改 candidate。**

即使 evidence bundle另產生新檔，也不得要求 candidate root跟著改。

---

## 2.2 Evaluator Identity

Final checker獨立於 candidate：

```yaml
evaluator:
  artifact: independent_checker.py
  digest_from_final_receipt:
    sha256: 9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
  mode: VERIFY_ONLY
  maker_checker_isolation: REQUIRED
```

因此前 R9 將：

```text
checker receipt script SHA = 9009713...
candidate/legacy manifest row = 8a9b761...
```

直接判成 candidate byte-binding defect，**過度把 evaluator與 candidate 混成同一 root**。

新版規則：

```text
candidate_root
!= evaluator_identity
!= evidence_bundle_root
```

但 final report必須清楚記錄三者關聯。

---

## 2.3 Evidence Bundle Root

Evidence bundle由 candidate freeze之後產生：

```yaml
evidence_bundle:
  binds_candidate_root: be576bebe7672093039bfe7dbc265f25aa0a1164
  contains:
    - runtime receipts
    - final checker receipt
    - manifest
    - review reducer
  mutation_of_candidate: false
```

Evidence bundle可以有自己的 digest。

它**不得再反過來改變 Candidate Root**。

---

# 3. Acceptance Scope 現在永久凍結

以下 gate自本報告後不得再擴張。

## 3.1 必須驗收

```text
FDA architecture / Team / Profiles
deterministic action-class routing
one-active-writer
unknown-state fail-closed
no silent fallback
UFO² effective-load
XQ 3.20.02-260811 exact-build binding
F01 current-build qualification
F06 fresh compile qualification
PAPER/no-live-write runtime
wrong_action = 0
silent_wrong_action = 0
broker_write = 0
fresh independent checker
rollback / docs / currentness
```

## 3.2 非本輪 mandatory gate

```text
Cua 0.19.4 nightly shadow
FN03 Afx explicit invoke 10x
intraday visual-alert UI
SQS live trading
production autonomy
remote deployment
```

以上不得在下一輪重新成為 blocker。

---

# 4. PAPER STOP Gate 校正

## 4.1 Blueprint 真正要求

FDA r2 STEP 9 的硬規則是：

```text
10 fresh runs/provider per applicable action class
wrong_action = 0
silent_wrong_action = 0
```

關鍵字是：

```text
applicable
```

不是「所有模式必須同時具備所有 terminal mechanics」。

---

## 4.2 Single-wash scenario

Current qualification明確使用：

```text
single-wash / 單次洗價
```

目前 raw evidence對十個 strategy instance均顯示：

```text
state sequence = 2,2,2,2,3
exec sequence  = 1,2,3,4,5
single trigger
post_stop_stopped = true

runs = 10
wrong_action = 0
silent_wrong_action = 0
broker_write = 0
one_active_writer = true
```

RR8亦提供 single-wash「一次判斷後自動停止」的 domain-support mapping。

因此新版 acceptance contract為：

```text
SINGLE_WASH mode:

CONFIG
→ START
→ execution/readback
→ auto-terminal readback

10/10
```

而不是：

```text
single-wash auto-terminal
+ 額外 manual STOP 10/10
```

---

## 4.3 Explicit STOP 的正確定位

Explicit `STOP`仍是有價值能力，但應屬：

```text
continuous/manual-stop scenario
或
separate action-class qualification
```

它不得被拿來倒逼目前 single-wash fixture的 PASS。

因此正式撤回 R9：

```text
RR9-001 explicit XQ_PAPER_STOP 10x mandatory blocker
```

新版裁決：

```text
PAPER_SINGLE_WASH_RUNTIME = PASS_CANDIDATE
PAPER_TERMINAL_READBACK = PASS_CANDIDATE
EXPLICIT_MANUAL_STOP_10X = NOT_REQUIRED_FOR_CURRENT_SINGLE_WASH_ACCEPTANCE
```

這不是降低安全標準；`broker_write=0`、one writer、wrong/silent-wrong=0仍保留。

---

# 5. 已閉合的 Runtime / Capability Edges

## 5.1 XQ exact subject

```text
XQ = 3.20.02
build = 260811
```

Current F01 receipt已修掉舊 3.18.02 subject。

### Verdict

```text
XQ_EXACT_BUILD_BINDING = PASS
```

---

## 5.2 F01 current-build locate

Current receipt具：

```text
run_id 1..10
10/10 PASS
version_match=true
class_match=true
wrong_action=0
silent_wrong_action=0
```

### Verdict

```text
F01_XQ_LAUNCH_LOCATE_260811 = PASS
```

---

## 5.3 F06 fresh compile

Current receipt具十個不同：

```text
LastCompileTime
```

且：

```text
CompileStatus=1
CompileMsg=""
10/10
wrong_action=0
silent_wrong_action=0
```

### Verdict

```text
F06_XS_COMPILE_PASS = PASS
```

---

## 5.4 UFO² effective-load

前序 raw receipt已驗：

```text
v3.0.8
7/7
wrong_action=0
silent_wrong_action=0
```

### Verdict

```text
DoD-13 / UFO2_EFFECTIVE_LOAD = PASS
```

---

## 5.5 PAPER single-wash 10 fresh runs

RR6/RR7/RR8 evidence chain已提供：

```text
10 distinct strategy instances
10 SensorList persistence
10 SensorLog execution lifecycles
10 single-wash terminal shapes
wrong_action=0
silent_wrong_action=0
broker_write=0
one_active_writer=true
```

### Corrected verdict

```text
PAPER_SINGLE_WASH_10X = PASS
DoD-17 current applicable single-wash scenario = PASS
```

不再要求額外 manual STOP 10x。

---

# 6. Final Checker：PASS

Current final checker receipt：

```text
total_checks = 194
actual raw records = 194
unique IDs = 194
passed = 194
failed = 0
errors = 0
exit = 0
mode = VERIFY_ONLY
```

Chronology：

```text
PAPER repair completed before checker
checker generated after repair
```

Maker/checker separation亦有明確宣告。

### Verdict

```text
CHECKER_DENOMINATOR = PASS
CHECKER_RAW_RECORDS = PASS
CHECKER_CHRONOLOGY = PASS
CHECKER_ISOLATION = PASS_CANDIDATE
```

Evaluator identity採 checker receipt中：

```text
sha256 = 9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
```

不再要求它等於 Candidate Root內的 historical script row。

---

# 7. 對原 R9 Findings 的正式勘誤

| R9 finding | 新版判定 | 原因 |
|---|---|---|
| RR9-001 explicit STOP 10x missing | **RETRACTED** | single-wash auto-terminal為current applicable mode；manual STOP不應成新增 gate |
| RR9-002 three manifest SHA | **EVIDENCE_PACKAGING_GAP** | 不是 candidate/runtime defect；需一個 canonical evidence serialization |
| RR9-003 54 vs 63 manifest count | **EVIDENCE_PACKAGING_GAP** | actual artifacts[]為63；duplicated count metadata stale |
| RR9-004 179 still CURRENT | **EVIDENCE_PACKAGING_GAP** | final checker raw body 194已可驗；history metadata stale |
| RR9-005 stale HEAD note | **NON_BLOCKING_STALE_METADATA** | structured current subject比 note具較高 machine specificity |
| RR9-006 evaluator SHA mismatch | **RETRACTED_AS_CANDIDATE_DEFECT** | evaluator identity應與 candidate root分離 |
| RR9-007 manifest chronology | **EVIDENCE_RESEAL_GAP** | 必須最後重生 evidence manifest，但不要求 runtime rerun |

---

# 8. 為什麼新版 verdict 是 PARTIAL，而不是 FAIL

`challenge-review`：

```text
FAIL_CHALLENGE
= blocking defect directly contradicts frozen acceptance

PARTIAL_CHALLENGE
= meaningful review complete,
  but required evidence / authority edge remains unresolved
```

校正 root model之後，目前沒有 confirmed runtime/product defect直接反證 frozen acceptance。

剩下的是：

```text
final evidence bundle尚未依新 root model做一次 atomic reseal
```

因此：

```text
FAIL_CHALLENGE
```

已不再是比例正確的 verdict。

新版：

```text
PARTIAL_CHALLENGE
```

更符合 Gate Calibration。

---

# 9. Current Acceptance State

```yaml
FDA_BLUEPRINT:
  status: PASS

FDA_ARCHITECTURE:
  status: PASS

FDA_RUNTIME_QUALIFICATION:
  status: PASS_CANDIDATE

FDA_XQ_260811:
  status: PASS

F01:
  status: PASS

F06:
  status: PASS

UFO2_EFFECTIVE_LOAD:
  status: PASS

PAPER_SINGLE_WASH_10X:
  status: PASS

WRONG_ACTION:
  status: PASS
  value: 0

SILENT_WRONG_ACTION:
  status: PASS
  value: 0

BROKER_WRITE:
  status: PASS
  value: 0

FINAL_CHECKER:
  status: PASS
  denominator: 194/194

EXTERNAL_CHALLENGE:
  status: PARTIAL_CHALLENGE

FDA_EXTERNAL_ACCEPTANCE:
  status: PENDING_EVIDENCE_RESEAL_ONLY

FDA_PROFILE_TEAM_ACTIVE:
  status: FAIL_CLOSED_EVIDENCE_RESEAL_ONLY

PRODUCT_REBUILD_REQUIRED:
  status: NO

RUNTIME_RERUN_REQUIRED:
  status: NO

BROAD_RERUN_REQUIRED:
  status: NO
```

---

# 10. 唯一允許的下一步：ONE-SHOT FINAL EVIDENCE RESEAL

這一步**不得修改 candidate**。

## 10.1 Freeze candidate

固定：

```text
CANDIDATE_ROOT =
be576bebe7672093039bfe7dbc265f25aa0a1164
```

之後：

```text
candidate mutation = DENY
```

---

## 10.2 Freeze evaluator identity

固定：

```text
EVALUATOR_SHA256 =
9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
```

若執行方認為此 digest不是 final evaluator，必須只修 evaluator/evidence identity，不能回頭改 runtime。

---

## 10.3 Machine-generate final EvidenceManifest outside candidate write-set

禁止人工維護 duplicated truth。

只允許：

```yaml
candidate_root: be576bebe...
evaluator_sha256: 9009713f...
current_checker:
  total: 194
  passed: 194
  failed: 0
  errors: 0
  exit: 0
  mode: VERIFY_ONLY

artifacts:
  # machine enumerated
```

以下欄位全部由程式 derive：

```text
artifact_count
unique_path_count
manifest_row_count
payload_count
current checker
generated_at
manifest SHA
```

---

## 10.4 Historical metadata不得污染 current truth

```text
144 = HISTORICAL
174 = HISTORICAL
175 = HISTORICAL
176 = HISTORICAL
179 = HISTORICAL
194 = CURRENT
```

不要再在 `checker_history` 留第二個 CURRENT。

---

## 10.5 Canonical serialization

只選一種：

```text
UTF-8 + LF
```

或：

```text
UTF-8 + CRLF
```

均可。

但必須：

```text
ONE byte serialization
ONE SHA-256
```

不能再同時把 LF SHA、CRLF SHA、舊 header SHA都稱為 final manifest。

---

## 10.6 最後順序

```text
Candidate freeze
→ runtime receipts frozen
→ evaluator frozen
→ checker receipt frozen
→ generate EvidenceManifest
→ validate manifest
→ generate external reducer/report
→ external hash/readback
```

**不得再 commit這些 evidence回 candidate而使 candidate root改變。**

---

# 11. Mandatory Final Preflight

執行方在交外部驗收前必須機器檢查：

```text
candidate_root_count = 1
current_checker_count = 1
manifest_sha_count = 1

artifact_count == len(artifacts)
unique_path_count == artifact_count
manifest_row_count == artifact_count

placeholder_count = 0
stale_current_count = 0
duplicate_current_checker = 0

checker_total == len(raw_records)
checker_unique == checker_total
checker_passed == checker_total
checker_failed == 0
checker_errors == 0
checker_exit == 0

manifest.candidate_root == frozen candidate root
manifest.evaluator_sha == final evaluator digest

manifest.generated_at > latest bound evidence timestamp
```

任何一條失敗：

```text
DO NOT SUBMIT TO EXTERNAL REVIEW
```

這可避免再發生 R10、R11、R12 的循環。

---

# 12. Final Promotion Condition — 從此不再新增

下一輪外部 reviewer只驗：

```text
1. Candidate Root = be576...
2. Evaluator digest = 9009713...
3. ONE canonical EvidenceManifest
4. artifact/count/current-checker fields self-consistent
5. 194/194 checker receipt bound
6. current F01/F06/UFO2/PAPER receipts bound
7. wrong_action=0
8. silent_wrong_action=0
9. broker_write=0
10. blocking evidence inconsistency=0
```

全部成立：

```text
PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
```

**不再允許加入：**

```text
explicit STOP 10x
intraday visual alert
Cua nightly
FN03 invoke
其他未在本報告 frozen scope的 gate
```

---

# 13. Scope Ceiling

即使下一輪 `FDA_PROFILE_TEAM_ACTIVE = PASS`：

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

不得提升。

FDA external acceptance只表示：

```text
Fabric-governed bounded desktop automation
for admitted local/PAPER/no-live-write scope
```

---

# 14. Final Verdict

```text
R9 ORIGINAL VERDICT = SUPERSEDED

CORRECTED EXTERNAL VERDICT =
PARTIAL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_ARCHITECTURE = PASS
FDA_RUNTIME_QUALIFICATION = PASS_CANDIDATE
FDA_LOCAL_IMPLEMENTATION = PASS_CANDIDATE

CONFIRMED_PRODUCT_DEFECT = 0
CONFIRMED_RUNTIME_BLOCKER = 0

FDA_EXTERNAL_ACCEPTANCE =
PENDING_EVIDENCE_RESEAL_ONLY

FDA_PROFILE_TEAM_ACTIVE =
FAIL_CLOSED_EVIDENCE_RESEAL_ONLY

PRODUCT_REBUILD_REQUIRED = NO
RUNTIME_RERUN_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

ONLY_NEXT_ACTION =
ONE-SHOT OUTSIDE-CANDIDATE EVIDENCE RESEAL
```

---

# 15. Reviewer Self-Correction Record

本 external reviewer正式記錄以下勘誤：

```text
CORRECTION-01
candidate root 與 evidence root未及早分離
→ caused self-invalidating acceptance loop

CORRECTION-02
R9將 single-wash auto-stop 再要求 explicit STOP 10x
→ gate over-tightening / mode-scope calibration issue

CORRECTION-03
R9把 evaluator digest mismatch直接視為 candidate defect
→ evaluator identity應獨立綁定

CORRECTION-04
EvidenceManifest stale metadata應阻斷 external final seal，
但不應在沒有 runtime counterevidence時被升格成產品/runtime FAIL
```

這些修正自本報告起固定，不得再回復舊標準。

---

# 16. Source / Authority Register

## Normative Review Method

`challenge-review-SKILL.md`

Key rules:
- existing PASS = claim
- exact frozen subject
- maker != checker
- raw deterministic evidence first
- preserve domain authority
- gate-calibration defense
- smallest legal repair
- PASS / PARTIAL / FAIL verdict grammar

## Normative FDA Blueprint

`fabric-desktop-automation_藍圖_v2026.08.13-r2.md`

Key locators:
- §1.1 claim ceiling
- §1.2 non-regression
- STEP 6 capability matrix
- STEP 9 XQ PAPER / no-live-write: 10 fresh runs/provider per applicable action class
- STEP 13 independent acceptance
- §10 FDA_PROFILE_TEAM_ACTIVE DoD

## Prior External Reports

- `FDA_External_Challenge_Review_2026-08-13_r1.md`
- `FDA_EXTERNAL_FOCUSED_REREVIEW_2026-08-14_r2.md` through `r8`
- `FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_2026-08-14_r9.md` — SUPERSEDED by this report

## Current Evidence

`FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md`

External byte identity from prior direct readback:

```text
sha256 =
344f8d74c7939c1b75aeb414b7fc93c2d5ce879bdcaa649a8e58e7f804036190

bytes =
69,735

lines =
2,361
```

Current embedded deterministic facts used in this corrected adjudication:
- checker 194 records / 194 unique / all PASS;
- final checker subject `be576...`;
- PAPER single-wash 10-run evidence;
- XQ build `3.20.02-260811`;
- F01 current-build evidence;
- F06 fresh 10-run evidence;
- UFO² 7/7 carried raw qualification;
- broker_write=0;
- current manifest body exists but contains stale duplicated metadata requiring evidence-only reseal.

---

**END OF CORRECTED EXTERNAL ACCEPTANCE REPORT**
