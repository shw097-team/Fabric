# 《fabric-desktop-automation》外部二次 Challenge Review 驗收報告

```yaml
report_id: FDA_EXTERNAL_FOCUSED_REREVIEW_20260814_R2
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review
review_mode: READ_ONLY_CLEAN_ROOM_FOCUSED_REREVIEW
review_date: 2026-08-14
timezone: Asia/Taipei

target:
  component: fabric-desktop-automation
  blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2.md
  prior_external_report: FDA_External_Challenge_Review_2026-08-13_r1.md
  current_patch_plan: FDA XQ Exact-Build-Aware Native Hybrid Upgrade

actual_submitted_file:
  file: FDA_IMPLEMENTATION_EVIDENCE(1).md
  sha256: fdb0bfcff4aabd404ccde66caa62bae42f253c0aa8bb52d72be64fc5137db0b1
  bytes: 27672
  lines: 329

hermes_claimed_final_review_file:
  file: FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md
  claimed_sha256: f9606a61043bc6c8c0472c60ad6e43c15d67d24fd6766c7a0a6435ffa0364bf4
  submitted_to_this_reviewer: false

external_verdict: FAIL_CHALLENGE
external_acceptance: NOT_GRANTED
fda_blueprint: PASS
fda_local_implementation: SUBSTANTIAL_NOT_OVERTURNED
fda_profile_team_active: FAIL_CLOSED
sqs_live_trading: NOT_AUTHORIZED
production_autonomy: NOT_CLAIMED
remote_deployment: NOT_CLAIMED

confirmed_product_architecture_defect: 0
confirmed_evidence_consistency_defects: 6
blocking_evidence_gaps: true
product_rebuild_required: false
broad_rerun_required: false
recommended_resume: RESUME_SMALLEST_REPAIR
```

---

# 0. 最終外部裁決

本輪完整掛載 `challenge-review-SKILL.md`，依其 hard invariants 執行 clean-room 二次驗收：

- existing PASS 只先視為 claim；
- verdict 必須綁 exact frozen subject / Evidence Manifest identity；
- maker != final checker；
- raw deterministic evidence first；
- 不接受 file presence、hash list、summary、agent consensus 作 proxy PASS；
- 每個 major PASS 必須嘗試 falsify；
- blocking defect 只交 earliest owner + smallest legal repair + focused retest；
- local/package qualification 不提升 production / live / remote authorization。

本輪外部 verdict：

```text
FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION = SUBSTANTIAL / NOT_OVERTURNED

EXTERNAL_CHALLENGE = FAIL_CHALLENGE
EXTERNAL_ACCEPTANCE = NOT_GRANTED

FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO
NEXT = RESUME_SMALLEST_REPAIR
```

之所以是 `FAIL_CHALLENGE` 而不是 `PARTIAL_CHALLENGE`，不是只因缺 raw artifacts，而是 **exact submitted evidence 本身存在 blocking deterministic contradictions**，直接破壞 frozen acceptance truth：

1. HERMES 宣稱 final evidence 為 `FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md` / `f9606a...`，本外部 reviewer實際取得的卻是另一檔 `FDA_IMPLEMENTATION_EVIDENCE(1).md` / `fdb0bfcff4aabd404ccde66caa62bae42f253c0aa8bb52d72be64fc5137db0b1`。
2. 同一 submitted file 對 UFO² effective-load 同時寫 `QUALIFIED 7/7`、`BLOCKED_HITL`、`runtime not installed`、DoD-13 `PASS`。
3. 同一 submitted file 對 XQ PAPER runtime 同時寫 `pending/not executed`、DoD-17 `PASS`、`BLOCKED_SUBSCRIPTION`、external checklist 又寫 DoD-17/35 `PARTIAL`。
4. checker 同時宣稱 `144 single current denominator` 與 `174/174 current`。
5. final subject / manifest lineage同時出現 `72cb450...`、`fa192ab...`、`1308eb1...`，但沒有一個 post-XQ-patch final manifest把全部新舊 artifacts / tests / runtime receipts / checker重新綁成同一 final root。
6. artifact denominator同時出現 §3 的 **53 rows**、HERMES摘要的 **52 artifacts**、§4A 的 **42 raw artifacts + manifest + index**、§10 checklist 的 **40 raw artifacts**。

因此不能誠實宣告 `PASS_CHALLENGE`。

---

# 1. Review Authority / Acceptance Reconstruction

## 1.1 challenge-review hard rules

本輪使用以下核心規則：

```text
existing PASS = claim, not evidence
exact frozen subject binding required
raw deterministic evidence first
maker != final checker
candidate/evaluator/acceptance artifacts read-only
no proxy-to-PASS
falsify every major PASS
blocking contradiction -> FAIL_CHALLENGE
unresolved evidence only -> PARTIAL_CHALLENGE
```

## 1.2 FDA r2 retained hard architecture

r2 主幹仍維持：

```text
Fabric Shared Infrastructure Profile Team
→ fabric-desktop-automation
→ fabric-desktop-cua + fabric-desktop-ufo2
→ HGK WorkOrder / current ExecutionBinding
→ Hermes Profile + project-scoped Kanban
→ deterministic action-class route
→ one active desktop writer
→ readback/checkpoint hot-swap
→ Fabric-governed Knowledge / SoD / independent Acceptance
```

並禁止：

```text
third Heavy Stack
second scheduler
second task DB
second reducer
second Knowledge platform
parallel desktop task authority
```

## 1.3 FDA r2 promotion denominator

本輪仍以 r1 外部報告及 r2 DoD-36 為 denominator，特別是：

```text
DoD-13:
fabric-desktop-ufo2 valid/effective-load qualified

DoD-17:
every mandatory XQ PAPER action class
has >=1 provider 10/10

DoD-18:
wrong_action = 0

DoD-19:
silent_wrong_action = 0

DoD-30:
same-subject drift = 0

DoD-33:
fresh independent Acceptance Officer PASS

DoD-35:
HGK/SQS consumer binding current
```

以及：

```text
SQS live broker write = 0
SQS_LIVE_TRADING = NOT_AUTHORIZED
```

---

# 2. Exact Submitted Evidence Readback

本外部 reviewer直接對實際附件做 byte-level readback：

```text
file:
FDA_IMPLEMENTATION_EVIDENCE(1).md

sha256:
fdb0bfcff4aabd404ccde66caa62bae42f253c0aa8bb52d72be64fc5137db0b1

bytes:
27672

lines:
329

§3 artifact rows:
53
```

HERMES本輪回報聲稱：

```text
FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md
sha256 = f9606a61043bc6c8c0472c60ad6e43c15d67d24fd6766c7a0a6435ffa0364bf4
```

但該 exact file / exact hash **沒有作為本輪附件提交給 external reviewer**。

因此：

```text
HERMES_FINAL_RE_REVIEW_FILE_IDENTITY = UNVERIFIED
ACTUAL_SUBMITTED_EVIDENCE_IDENTITY = VERIFIED
```

這不是檔名小差異，而是 challenge-review 的 exact evidence identity gate。

---

# 3. r1 八項 finding 二次 closure adjudication

| r1 Finding | HERMES r2 claim | External second verdict | Blocking |
|---|---|---|---|
| EXT-FDA-001 subject root | CLOSED | **NOT CLOSED** — root/manifest lineage 72cb450 / fa192ab / 1308eb1 未形成單一 final rebind | YES |
| EXT-FDA-002 raw artifacts | CLOSED | **NOT CLOSED** — final raw bundle未實際提交，且 40/42/52/53 denominator衝突 | YES |
| EXT-FDA-003 checker denominator | CLOSED 174/174 | **NOT CLOSED** — same file仍有144與174兩組 current denominator | YES |
| EXT-FDA-004 DoD contradiction | CLOSED 36/36 | **NOT CLOSED** — DoD-13/17/35均有相互矛盾 final-state文字 | YES |
| EXT-FDA-005 UFO² effective-load | CLOSED 7/7 | **NOT CLOSED** — effective-load PASS / BLOCKED_HITL / runtime-not-installed三值並存 | YES |
| EXT-FDA-006 XQ PAPER runtime | CLOSED SensorLog | **NOT CLOSED** — SensorLog PASS claim與 `BLOCKED_SUBSCRIPTION` / “not executed”並存 | YES |
| EXT-FDA-007 Cua deadlock | CLOSED pywinauto | **PARTIAL** — native route方向正確，但 FN03 只有 locate 1/1；不足以概括所有 MFC/Afx actions 已 qualification | conditional |
| EXT-FDA-008 version drift | CLOSED fingerprint | **PARTIAL** — 3.20.02-260811 fingerprint方向正確，但舊段仍稱 exact local=1.10.0.0，且新 ChangeSet尚未 final-root rebind | YES via binding |

因此：

```text
r1 findings externally CLOSED = 0/8 strict
PARTIAL = 2
BLOCKING NOT CLOSED = 6+
```

此處不是否定施工成果，而是拒絕把 contradictory evidence reducer當作 final external truth。

---

# 4. Detailed Findings

## EXT-FDA-RR2-001 — Final evidence identity mismatch

```yaml
classification: CONFIRMED_DEFECT
blocking: true

acceptance_id:
  - exact frozen subject / evidence identity
  - EXT-FDA-001
  - EXT-FDA-002

evidence:
  hermes_claim:
    file: FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md
    sha256: f9606a61043bc6c8c0472c60ad6e43c15d67d24fd6766c7a0a6435ffa0364bf4
  actual_attachment:
    file: FDA_IMPLEMENTATION_EVIDENCE(1).md
    sha256: fdb0bfcff4aabd404ccde66caa62bae42f253c0aa8bb52d72be64fc5137db0b1

earliest_owner: FDA_EVIDENCE_PACKAGER

smallest_repair:
  - materialize one final re-review evidence artifact
  - give it one exact filename/hash
  - submit those exact bytes to external reviewer
  - bind mirror receipt to those exact bytes

focused_retest:
  - external byte hash readback
  - mirror equality
  - final EvidenceManifest root binding

affected_regression:
  - evidence only
```

---

## EXT-FDA-RR2-002 — UFO² final-state contradiction

Submitted file simultaneously states:

```text
line 20:
FDA_UFO2_QUALIFICATION = QUALIFIED
effective-load 7/7

lines 86-88:
effective-load BLOCKED_HITL

lines 220-222:
effective-load PASS
but UFO2 runtime not installed / FDA-C3 blocked

line 249:
DoD-13 = PASS
```

這四個狀態不能同時作為 current final truth。

```yaml
classification: CONFIRMED_DEFECT
blocking: true
acceptance_id: DoD-13
earliest_owner: FDA_EVIDENCE_REDUCER
smallest_repair:
  choose one exact current UFO2 runtime truth from raw receipt
  remove/supersede stale state
focused_retest:
  exact UFO2 distribution
  import/effective-load
  backend provenance
  exit/result
  disable/rollback
affected_regression:
  DoD-13
  DoD-14
  final claim ceiling
```

若 7/7 raw receipt是真的，這是 **evidence reducer repair**，不需重跑 UFO² broad suite。

---

## EXT-FDA-RR2-003 — XQ PAPER runtime / DoD-17 contradiction

Submitted file同時存在：

```text
line 21:
DoD-17 pending

lines 28-31:
item 17 partially PASS

line 219:
strategy runtime start/stop not executed

line 253:
DoD-17 PASS
SensorLog 56 rows

lines 275-280:
PASS=36 / DoD-17 PASS / no contradiction

lines 302-303:
FDA_XQ_PAPER_RUNTIME_RECEIPT
runtime execution BLOCKED_SUBSCRIPTION

lines 327-328:
DoD-17/35 honestly partial
FDA_PROFILE_TEAM_ACTIVE FAIL_CLOSED (DoD-17)
```

這是直接阻斷 DoD-17 final PASS 的 deterministic contradiction。

```yaml
classification: CONFIRMED_DEFECT
blocking: true
acceptance_id:
  - DoD-17
  - DoD-18
  - DoD-19
  - DoD-35

earliest_owner: FDA_XQ_EVIDENCE_REDUCER

smallest_repair:
  - pick one post-run PAPER runtime receipt as canonical
  - explicitly supersede BLOCKED_SUBSCRIPTION / not-executed states if stale
  - bind SensorLog/SensorList raw extracts to exact XQ subject
  - regenerate DoD matrix from canonical machine predicates only

focused_retest:
  - config
  - start
  - running-state readback
  - stop
  - post-stop readback
  - SensorLog exact row count/digest
  - wrong_action=0
  - silent_wrong_action=0
  - broker_write=0

affected_regression:
  - XQ PAPER action classes only
```

### 盤中視覺 trigger

HERMES誠實保留的「盤中警示 UI 視覺觸發」本身**不必自動成為 DoD-17 blocker**，如果 frozen DoD 的 runtime truth可由 authoritative SensorLog/state-machine readback閉合，且該 visual alert並非 mandatory action class。

因此本報告**不新增**「一定要等盤中視覺警示」的新 Gate。

---

## EXT-FDA-RR2-004 — Independent checker denominator conflict

Submitted file：

```text
§4:
checks = 144
single current denominator

§10b:
Checker = 174/174
T160-T177 added

§10 External verifier:
re-run checker -> 144
```

HERMES回報則宣稱：

```text
174/174 current
```

所以 current denominator不是 deterministic single truth。

```yaml
classification: CONFIRMED_DEFECT
blocking: true
acceptance_id: DoD-33
earliest_owner: FDA_ACCEPTANCE_EVIDENCE_OWNER
smallest_repair:
  regenerate one fresh post-XQ-patch checker receipt
focused_retest:
  checker script sha
  exact final subject root
  exact predicate IDs
  denominator
  passed/failed/error
  exit status
  verify-only/no-write
  maker-checker isolation
affected_regression:
  Acceptance Officer only
```

如果 T160-T177 是真正新增 acceptance assertions，current denominator理論上應是 174，而 144 應被明確標為 `SUPERSEDED_PRE_XQ_PATCH`。

---

## EXT-FDA-RR2-005 — Same-subject binding / stale manifest defect

Submitted file存在：

```text
§4A final frozen subject root:
72cb45086e48...

§9A DoD-1 / DoD-30:
subject root fa192ab...

§10b new XQ ChangeSet:
Fabric HEAD 1308eb1
```

`1308eb1` 顯然是 XQ exact-build-aware patch之後的新 subject identity。

但 EvidenceManifest段落仍描述舊 root lineage；沒有看到「post-1308eb1 final EvidenceManifest」綁：

```text
new xq_native_adapter
new build fingerprint
new XQ qualification
new PAPER runtime receipt
new tests
174 checker
```

```yaml
classification: CONFIRMED_DEFECT
blocking: true
acceptance_id:
  - DoD-30
  - DoD-33
  - DoD-35
earliest_owner: FDA_EVIDENCE_PACKAGER
smallest_repair:
  freeze final post-XQ-patch HEAD
  regenerate subject manifest + EvidenceManifest after all receipts/tests/checker are frozen
focused_retest:
  tested bytes == claimed bytes == accepted bytes
affected_regression:
  exact binding only
```

不需要重做 RP-002/FDA product runtime。

---

## EXT-FDA-RR2-006 — Raw artifact denominator ambiguity + raw bundle absent

實際 submitted file §3 列出：

```text
53 artifact rows
```

HERMES本輪摘要宣稱：

```text
52-artifact raw bundle
```

submitted file §4A宣稱：

```text
42 raw artifacts + manifest + index
```

§10 verifier又要求：

```text
40 raw artifacts
```

這些可以是不同 scope，**但文件沒有給出清楚 scope-name / exact-set semantics**，因此 external reviewer不能知道哪個才是 final acceptance denominator。

另外，本輪實際附件仍只有 summary/index MD；raw bundle本身沒有提交給本 reviewer。

```yaml
classification: CONFIRMED_DEFECT
blocking: true
acceptance_id:
  - EXT-FDA-002
  - exact evidence set
  - DoD-30
  - DoD-33
earliest_owner: FDA_EVIDENCE_PACKAGER
smallest_repair:
  define one named final review denominator
  e.g. review_payload_count / manifest_entry_count / external_bundle_entry_count separately
  upload exact raw bundle or self-contained raw bodies
focused_retest:
  count
  path
  size
  sha256
  same-subject binding
affected_regression:
  evidence packaging only
```

---

## EXT-FDA-RR2-007 — pywinauto native hybrid方向正確，但 Afx qualification被過度概括

最新版 XQ upgrade plan要求：

```text
exact-build
× action-class
× backend
× readback
```

作最小 qualification unit，不能由一個 action class外推全部 native controls。

Submitted evidence §10b支持：

```text
FN01 main locate 10/10
FN02 editor locate 10/10
FN03 Afx 新增 button locate 1/1
PYWINAUTO_WIN32 promoted for XQ_LAUNCH_LOCATE
```

但同段又宣稱：

```text
pywinauto Win32 native first-choice for MFC/Afx actions
```

目前 raw claim只能支持：

```text
XQ_LAUNCH_LOCATE route promoted
Afx button discoverability demonstrated
```

不能支持：

```text
all MFC/Afx action classes qualified
```

```yaml
classification: EVIDENCE_GAP
blocking: false_if_matrix_only_promotes_launch
acceptance_id:
  - EXT-FDA-007
  - XQ build-aware routing
earliest_owner: FDA_NATIVE_ADAPTER_OWNER
smallest_repair:
  narrow claim to qualified rows
  or run 10x invoke/readback for Afx action before promotion
focused_retest:
  target action only
affected_regression:
  XQ native action rows only
```

此 finding **不要求新增第三 Profile/Heavy Stack**。

---

## EXT-FDA-RR2-008 — XQ build fingerprint方向正確，但 current identity prose仍有 stale contradiction

本輪新增：

```text
XQ 3.20.02-260811
exe_sha256 6c0c7cbc...
public 260731 mismatch acknowledged
LOCAL_BUILD_QUALIFICATION_REQUIRED
```

這符合最新版 XQ upgrade plan。

但舊段仍寫：

```text
CR_OPEN-FDA-006:
exact local = XQLite 1.10.0.0
```

後段又寫：

```text
single current XQ identity = 3.20.02-260811
file version 1.10.0.0 retained as metadata only
```

所以新設計方向是對的，但 final evidence prose尚未完全 normalized。

```yaml
classification: CONFIRMED_DEFECT
blocking: true_via_DoD35_and_same_subject_binding
acceptance_id:
  - EXT-FDA-008
  - DoD-35
earliest_owner: FDA_EVIDENCE_REDUCER
smallest_repair:
  rewrite all current identity fields to:
    runtime_product_identity = 3.20.02-260811
    file_version_metadata = 1.10.0.0
focused_retest:
  build drift firewall
  selector-bound row freshness
affected_regression:
  XQ binding only
```

---

# 5. Positive Findings — 本輪確實有實質進展

雖然 external verdict 是 FAIL_CHALLENGE，但不能把它誤讀成施工失敗。

以下方向有明顯改善，而且沒有 evidence顯示需要推翻：

## 5.1 UFO² closure方向

新增 `FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json` 與 7/7 effective-load claim。

如果 raw receipt可重放並成為唯一 current truth，EXT-FDA-005 很可能只剩 evidence reducer修補。

## 5.2 XQ PAPER runtime

SensorLog / SensorList / state 2→3→1 / ExecState 1→8 / 2330.TW 等是比「只開 radar surface」強很多的 runtime evidence形狀。

這正是 r1 要求補的 runtime truth方向。

## 5.3 XQ build drift firewall

`3.20.02-260811 + exe hash + public-build mismatch` 是正確的 current XQ compatibility key，比單用 `3.20.02` 成熟。

## 5.4 pywinauto Win32 native path

以 `BM_CLICK / TB_PRESSBUTTON / WM_SETTEXT` 等 pure-message path降低 mouse/pixel dependency，符合最新版 XQ native-first deterministic upgrade的方向。

## 5.5 不新增第三 Heavy Stack

目前 submitted evidence仍維持：

```text
no new profile/stack/gate
```

這符合 anti-overengineering要求。

---

# 6. Gate Calibration Failure Defense

## Objective alignment

PASS。

驗收目標仍是：

```text
受治理的 Windows desktop automation
```

不是：

```text
live trading authorization
```

## Risk-proportionate strictness

PASS。

PAPER/no-live-write與 SQS authority ceiling仍保留。

## False-positive defense

本輪主要阻止的正是：

```text
SensorLog summary
+ checker summary
+ manifest pointer
→ 直接升格 external PASS
```

## Negative / adversarial

應保留：

```text
wrong_action=0
silent_wrong_action=0
unknown-state auto-retry=0
second writer=0
credential access=0
network control=0
broker write=0
```

## Anti-overfitting

不能因 FN01/FN02通過，就把所有 MFC/Afx actions標為 pywinauto primary-qualified。

## HITL / domain boundary

保留：

```text
SQS live trading = NOT_AUTHORIZED
future semi-auto = separate SQS ChangeSet
```

這些不因 FDA external acceptance而改變。

---

# 7. Smallest Legal Repair

## Track A — Final evidence reducer repair

只做：

```text
A1. choose one final evidence filename/hash
A2. remove all stale superseded final-state prose
A3. make UFO2 state single-valued
A4. make PAPER runtime state single-valued
A5. make checker denominator single-valued
A6. give all artifact denominators explicit scope names
```

## Track B — Final post-XQ subject rebind

順序：

```text
1. freeze final FDA + XQ patch HEAD
2. freeze raw runtime receipts
3. freeze affected tests
4. run one fresh checker
5. create subject manifest
6. create EvidenceManifest
7. render final external re-review evidence MD
8. mirror it
9. generate mirror readback
10. submit exact final bytes + raw review bundle
```

不要在 manifest之後再追加 XQ ChangeSet。

## Track C — Focused runtime retest only if raw truth仍不清楚

只重驗：

```text
UFO2 effective-load
XQ PAPER config/start/status/stop
Afx action only if pywinauto wants promotion beyond locate
XQ build fingerprint
```

不重跑：

```text
RP-002
FDA team materialization
unchanged Cua F01/F03/F06
unaffected Fabric/HGK/SQS contracts
```

---

# 8. Promotion Conditions for Next Re-review

下一輪只要 external reviewer能重新計算並確認：

```text
1 final evidence artifact identity
1 final post-XQ subject root
1 EvidenceManifest root

raw artifact denominator explicit
all raw bytes match manifest

checker denominator unique/current
maker != checker
verify-only/no-write

DoD-13 single-valued PASS
DoD-17 single-valued PASS
DoD-18 = 0 wrong
DoD-19 = 0 silent wrong
DoD-30 same-subject = PASS
DoD-33 fresh AO = PASS
DoD-35 exact XQ 260811 current binding = PASS

blocking contradiction = 0
blocking evidence gap = 0
broker_write = 0
```

即可重新考慮：

```text
PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
```

不需要第三次 broad architecture review。

---

# 9. Final Stop

```text
EXTERNAL_FOCUSED_REREVIEW = FAIL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION = SUBSTANTIAL_NOT_OVERTURNED

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

CONFIRMED_PRODUCT_ARCHITECTURE_DEFECT = 0
CONFIRMED_EVIDENCE_CONSISTENCY_DEFECT = YES
BLOCKING_EVIDENCE_GAP = YES

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

NEXT =
RESUME_SMALLEST_REPAIR
/ FINAL_EVIDENCE_REDUCER_NORMALIZATION
/ POST_XQ_SUBJECT_REBIND
/ RAW_BUNDLE_SUBMISSION
/ FOCUSED_EXTERNAL_REREVIEW
```

---

# 10. Source Locator Register

## NORMATIVE

- `challenge-review-SKILL.md`
  - Role
  - Invariants 1–10
  - Intake
  - Workflow 1–5
  - PASS/PARTIAL/FAIL/TEMP_CLOSED grammar

- `fabric-desktop-automation_藍圖_v2026.08.13-r2.md`
  - §1.1 claim ceiling
  - §1.2 non-regression
  - STEP 5 provider qualification
  - STEP 6 capability matrix
  - STEP 9 XQ PAPER / no-live-write 10-fresh-run contract
  - STEP 13 independent acceptance
  - §10.1 DoD-36
  - §11 XQ/SQS claim ceiling

- Current A0 accepted patch plan:
  - `FDA XQ Exact-Build-Aware Native Hybrid Upgrade`
  - exact-build × action-class × backend × readback
  - build drift firewall
  - pywinauto Win32 as bounded native backend
  - Cua general path
  - UFO² specialist
  - no new Heavy Stack/Profile/scheduler/DB

## PRIOR EXTERNAL REPORT

- `FDA_External_Challenge_Review_2026-08-13_r1.md`
  - EXT-FDA-001..008
  - final stop conditions
  - smallest-repair Track A/B/C

## CURRENT SUBMITTED EVIDENCE

- `FDA_IMPLEMENTATION_EVIDENCE(1).md`
  - exact hash `fdb0bfcff4aabd404ccde66caa62bae42f253c0aa8bb52d72be64fc5137db0b1`
  - lines 5–31 claim ceiling
  - lines 54–93 live runtime section
  - lines 95–151 artifact table
  - lines 153–179 checker + manifest
  - lines 214–223 blockers
  - lines 233–280 DoD-36
  - lines 283–309 WO-FDA-XQ-002
  - lines 311–328 external verifier checklist

---

**END OF EXTERNAL FOCUSED REREVIEW**
