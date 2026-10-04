# 《fabric-desktop-automation》外部第四輪 Focused Challenge Review 驗收報告

```yaml
report_id: FDA_EXTERNAL_FOCUSED_REREVIEW_20260814_R4
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review
review_mode: READ_ONLY_CLEAN_ROOM_FOCUSED_REREVIEW
review_time_local: 2026-08-14T11:13:00+08:00

target:
  component: fabric-desktop-automation
  blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2.md
  prior_external_report: FDA_EXTERNAL_FOCUSED_REREVIEW_2026-08-14_r3.md

actual_submitted_evidence:
  file: FDA_IMPLEMENTATION_EVIDENCE(3).md
  sha256: dfb2da72149fcc673514345c868618f56c19f43262674fcb16eeff62b60da582
  bytes: 15949
  lines: 263

external_verdict: FAIL_CHALLENGE
external_acceptance: NOT_GRANTED

fda_blueprint: PASS
fda_local_implementation: SUBSTANTIAL_NOT_OVERTURNED
fda_profile_team_active: FAIL_CLOSED

sqs_live_trading: NOT_AUTHORIZED
production_autonomy: NOT_CLAIMED
remote_deployment: NOT_CLAIMED

confirmed_product_architecture_defect: 0
confirmed_evidence_consistency_defects: 2
blocking_evidence_gaps: 2

product_rebuild_required: false
broad_rerun_required: false
repair_class: EVIDENCE_PACKAGING_AND_POST_REORG_REBIND_ONLY
recommended_resume: RESUME_SMALLEST_REPAIR
```

---

# 0. 最終裁決

本輪依 `challenge-review-SKILL.md` 重新對新 evidence bytes 做 focused challenge，而不是延續上一輪判定。

適用 hard rules：

```text
existing PASS = claim, not evidence
exact frozen subject + EvidenceManifest identity required
raw deterministic evidence first
maker != final checker
test denominator/count/exit/raw logs must be deterministic
blocking deterministic mismatch -> FAIL_CHALLENGE
missing raw edge without contradictory defect -> PARTIAL_CHALLENGE
```

最終裁決：

```text
FDA_EXTERNAL_FOCUSED_REREVIEW_R4 = FAIL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION = SUBSTANTIAL_NOT_OVERTURNED

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

NEXT =
RESUME_SMALLEST_REPAIR
→ CHECKER_DENOMINATOR_NORMALIZATION
→ MANIFEST_EXACT_SET_NORMALIZATION
→ POST_FOLDER_REORG_SUBJECT_REBIND
→ RAW_BUNDLE_SUBMISSION
→ FOCUSED_FINAL_REREVIEW
```

本輪不是產品或架構 failure。阻斷點仍集中在 **final acceptance evidence consistency / exact binding**。

---

# 1. 本輪相較 r3 的確定改善

## 1.1 RR3-001 manifest SHA placeholder — substantive closure

前輪 `<REBOUND_MANIFEST_SHA>` 已被實際值取代：

```text
EvidenceManifest sha256:
4ac3fb8247db8342f5118470e55750683103ed93fb86e297e8124c89cb166d29

schema:
FDA-EVIDENCE-MANIFEST/2

declared subject root:
83e8138
```

因此：

```text
RR3-001 placeholder defect = CLOSED_AT_REDUCER_LEVEL
```

但因本輪後面又新增 folder reorganization / manifest path update，是否仍是 post-reorg final manifest，需重新綁定，見 RR4-003。

## 1.2 RR3-004 timestamp — CLOSED

current reducer 已寫：

```text
generated_at_utc: 2026-08-13T18:45:00Z
local: 2026-08-14T02:45:00+08:00
```

前輪 +12h label error 已修正。

## 1.3 UFO² / XQ PAPER / XQ identity reducer semantics仍保持單值

本輪沒有重新出現：

```text
UFO² PASS vs BLOCKED
PAPER PASS vs BLOCKED
XQ 1.10 file-version vs runtime 3.20.02 identity
```

等前輪主要 runtime-state矛盾。

因此：

```text
DoD-13 reducer semantic defect = NOT REOPENED
DoD-17 reducer semantic defect = NOT REOPENED
DoD-35 XQ identity semantic defect = NOT REOPENED
```

但 raw receipt仍未實際提供給本 external reviewer，故只能說「未被推翻」，不能說已獨立重放。

---

# 2. Exact submitted evidence identity

本外部 reviewer對實際附件重新計算：

```text
file:
FDA_IMPLEMENTATION_EVIDENCE(3).md

sha256:
dfb2da72149fcc673514345c868618f56c19f43262674fcb16eeff62b60da582

bytes:
15,949

lines:
263
```

此 identity為本輪可直接 external byte-readback 的唯一主 evidence artifact。

Reducer內的：

```text
evidence_reducer_sha256 = <FINAL_FREEZE_VALUE>
```

本輪不再當 blocking defect，因同一段已明文定義 reducer 不自嵌自己的 hash，以避免 self-reference，並要求 external reviewer從 submitted bytes重算。

本 reviewer 已完成此重算：

```text
external_recomputed_reducer_sha256
= dfb2da72149fcc673514345c868618f56c19f43262674fcb16eeff62b60da582
```

建議未來將欄位名稱改為：

```text
evidence_reducer_sha256 = EXTERNALLY_RECOMPUTED
```

或直接移除 placeholder，避免被誤讀成未填值。

分類：

```yaml
classification: NON_BLOCKING_OBSERVATION
```

---

# 3. Blocking Findings

## EXT-FDA-RR4-001 — Current checker denominator 再次變成三值

Current reducer §4 明確宣稱：

```text
checks = 176
SINGLE current denominator
174 = pre-folder-reorg
144 = superseded
```

DoD-33也使用：

```text
checker 176/176
```

但 §9 External verifier checklist 又要求：

```text
Re-run independent_checker.py
→ PASS, 174 checks
```

而 §12 Folder reorganization 又寫：

```text
Checker paths patched
→ 175/175 PASS
```

因此 exact submitted reducer 同時存在：

```text
176 current
174 verifier expected
175 post-reorg
```

三個互斥 acceptance denominator。

這直接違反 challenge-review 對：

```text
test command
denominator
pass/fail/error counts
exit status
```

必須 deterministic 的要求，也直接阻斷 DoD-33。

```yaml
finding_id: EXT-FDA-RR4-001
classification: CONFIRMED_DEFECT
blocking: true

acceptance_id:
  - DoD-33
  - independent Acceptance Officer
  - exact final checker denominator

evidence_id:
  - FDA_IMPLEMENTATION_EVIDENCE(3).md §4
  - FDA_IMPLEMENTATION_EVIDENCE(3).md §9
  - FDA_IMPLEMENTATION_EVIDENCE(3).md §12

earliest_owner: FDA_ACCEPTANCE_EVIDENCE_OWNER

smallest_repair:
  - freeze the final post-folder-reorg tree first
  - run independent_checker.py exactly once against that tree
  - record one denominator only
  - mark all previous denominators SUPERSEDED with their subject roots
  - regenerate DoD-33 and verifier checklist from the same receipt

focused_retest:
  - checker script SHA
  - final subject root
  - exact test IDs
  - denominator
  - passed/failed/error
  - exit
  - VERIFY_ONLY/read-only
  - maker != checker isolation

affected_regression:
  - acceptance evidence only

product_rebuild_required: false
```

### External adjudication

```text
DoD-33 external status = FAIL / BLOCKED_BY_CONTRADICTION
```

不是因 checker一定失敗，而是 current reducer無法回答「到底哪一個 fresh run才是 final」。

---

## EXT-FDA-RR4-002 — Manifest exact-set / self-entry semantics仍互相矛盾

§3宣稱：

```text
payload_entries = 51
```

並明文說這 51：

```text
EXCLUDES evidence reducer MD
EXCLUDES manifest file
```

同段又說：

```text
manifest rows
do NOT include evidence reducer MD
do NOT include manifest itself
```

但緊接著 artifact table 又列：

```text
#51 FDA_IMPLEMENTATION_EVIDENCE.md (this file) | manifest
```

並宣稱：

```text
exact 52 payload paths + sha256 + size in EvidenceManifest
```

而 row 52 甚至是：

```text
FDA_USER_GUIDE.md
+ DOC/FDA_USER_GUIDE.md
+ reorg receipts
+ tests/ suite
```

多個不同 filesystem objects 被壓在一個 abbreviated table row。

所以目前同一 reducer仍同時存在：

```text
manifest payload rows = 51
manifest excludes reducer
exact manifest payload paths = 52
row 51 = reducer itself
```

這不是單純文字風格問題，而是 external reviewer無法由 reducer重建：

```text
manifest row set
payload set
bundle set
self-entry policy
```

的唯一 exact denominator。

```yaml
finding_id: EXT-FDA-RR4-002
classification: CONFIRMED_DEFECT
blocking: true

acceptance_id:
  - exact EvidenceManifest set
  - DoD-30 same-subject drift
  - final evidence package integrity

evidence_id:
  - FDA_IMPLEMENTATION_EVIDENCE(3).md §3

earliest_owner: FDA_EVIDENCE_PACKAGER

smallest_repair:
  - use four separate exact counters:
      manifest_row_count
      payload_file_count
      bundle_file_count
      non_manifest_support_count
  - define reducer_in_manifest = true|false exactly once
  - define manifest_self_entry = false
  - remove grouped artifact table rows from denominator math
  - generate table directly from manifest instead of hand-written abbreviation
  - make every manifest row correspond to exactly one filesystem path

focused_retest:
  - JSON parse
  - row count
  - unique path count
  - duplicate count
  - reducer entry count
  - manifest self-entry count
  - every row path exists
  - every row size/hash matches bytes

affected_regression:
  - evidence packaging only

product_rebuild_required: false
```

### External adjudication

```text
DoD-30 external status = NOT CLOSED
```

即使 `4ac3fb...` 是真 manifest hash，本 reviewer仍未取得 manifest bytes，且 reducer自身對 manifest exact set 的描述不一致。

---

# 4. Blocking Evidence Gaps

## EXT-FDA-RR4-003 — Folder reorganization 後 final subject / manifest binding 未外部閉合

本 reducer主體宣稱：

```text
POST_XQ_SUBJECT_REBIND = 83e8138
EvidenceManifest SHA = 4ac3fb...
subject root = 83e8138
```

但文件最後又新增一個 durable filesystem mutation：

```text
29 evidence receipts moved
4 governance contracts moved
checker paths patched
EvidenceManifest paths updated
directory tree regenerated
```

這類 path reorganization即使「file contents SHA 不變」，仍會改變：

```text
git tree / HEAD
manifest path fields
checker path assertions
directory-tree artifact
```

因此它不是 byte-content no-op。

Current evidence沒有提供一個明確的：

```text
post-folder-reorg final git HEAD
post-folder-reorg final EvidenceManifest SHA
post-folder-reorg final checker receipt
```

三者綁定。

加上 §12 的 checker 175/175 與 §4 的 176/176不一致，更顯示 folder reorg chronology尚未被 final freeze正常 reducer 化。

```yaml
finding_id: EXT-FDA-RR4-003
classification: EVIDENCE_GAP
blocking_for_pass_challenge: true

acceptance_id:
  - DoD-30
  - DoD-33
  - DoD-36
  - exact frozen subject

earliest_owner: FDA_EVIDENCE_PACKAGER

smallest_repair:
  - treat folder reorg as the last candidate mutation
  - freeze one post-reorg git HEAD
  - regenerate EvidenceManifest from post-reorg paths
  - run fresh checker after that freeze
  - render reducer last

focused_retest:
  - git rev-parse HEAD
  - manifest subject_root
  - manifest SHA
  - checker receipt subject_root
  - docs/tree currentness

affected_regression:
  - path/binding/currentness only
```

---

## EXT-FDA-RR4-004 — Raw review bundle仍未提交給本 reviewer

本輪實際附件仍只有：

```text
FDA_IMPLEMENTATION_EVIDENCE(3).md
```

本 reviewer未實際取得：

```text
FDA_EVIDENCE_MANIFEST.json
FDA_RAW_REVIEW_BUNDLE/*
independent checker raw output
SensorLog raw extract
SensorList raw extract
UFO2 effective-load receipt
git repository / subject-root readback
```

因此依 challenge-review，不得把 reducer中的：

```text
0 mismatch
176/176
56 SensorLog records
7/7 UFO2
83e8138
```

自行提升成 independently reviewed raw PASS。

```yaml
finding_id: EXT-FDA-RR4-004
classification: EVIDENCE_GAP
blocking_for_pass_challenge: true

acceptance_id:
  - external final acceptance
  - DoD-13
  - DoD-17
  - DoD-30
  - DoD-33
  - DoD-35

earliest_owner: FDA_EVIDENCE_PACKAGER

smallest_repair:
  - submit final EvidenceManifest
  - submit exact raw review bundle
  - or embed deterministic raw bodies sufficient to reproduce final stop conditions

focused_retest:
  - manifest rehash
  - final checker raw receipt
  - SensorLog/SensorList query result
  - UFO2 7/7 receipt
  - subject-root readback

affected_regression:
  - none unless raw evidence contradicts reducer
```

如果 RR4-001/002 不存在，單獨 RR4-004只會導致：

```text
PARTIAL_CHALLENGE
```

但本輪有兩個 deterministic blocking defects，所以總 verdict仍是：

```text
FAIL_CHALLENGE
```

---

# 5. Positive Findings / Not Reopened

以下 current claims的 reducer語義本輪沒有發現新的內部矛盾：

```text
DoD-13 UFO2 effective-load = QUALIFIED 7/7
DoD-17 XQ PAPER runtime = QUALIFIED
DoD-18 wrong_action = 0
DoD-19 silent_wrong_action = 0
XQ runtime identity = 3.20.02-260811
file version 1.10.0.0 = metadata only
pywinauto promotion = XQ_LAUNCH_LOCATE only
FN03 Afx = locate 1/1 only
SQS_LIVE_TRADING = NOT_AUTHORIZED
```

因此：

```text
confirmed FDA runtime/product defect = 0
```

這些項目為：

```text
NOT_OVERTURNED_BY_R4
```

但因 raw bundle未交付，不能改寫成：

```text
INDEPENDENTLY_REPLAYED_PASS
```

---

# 6. DoD-36 external state

Reducer自身列出：

```text
36/36 PASS
```

本 reviewer確認表格結構確實呈現 1..36 continuous。

但 external challenge不是只驗「表格有沒有寫 PASS」。

至少以下 edges目前不能 external close：

```text
DoD-30 = NOT CLOSED
  reason:
  manifest exact-set + post-reorg binding unresolved

DoD-33 = FAIL/BLOCKED
  reason:
  176 vs 174 vs 175 checker denominator contradiction

DoD-36 = EVIDENCE_GAP
  reason:
  folder reorg後 docs/path currentness未綁 final post-reorg subject
```

因此：

```text
EXTERNAL DoD 36/36 = NOT ESTABLISHED
```

---

# 7. Gate Calibration Failure Defense

## Objective alignment

PASS。

本輪沒有把「folder reorg完成」誤當成 XQ runtime能力，也沒有把 FDA local qualification提升成 live trading authorization。

## Risk-proportionate strictness

PASS。

阻斷的是 exact evidence / checker / subject binding，不是要求新的產品功能。

## Anti-overfitting

PASS。

FN03仍維持 locate-only 1/1；沒有因 pywinauto部分成功就擴張所有 Afx action-class promotion。

## False-positive defense

本輪主要 false-positive counterexample：

```text
"single current checker denominator"
```

實際同檔找出：

```text
176
174
175
```

故成功攔住 proxy PASS。

## Domain authority

保持：

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
```

FDA external acceptance即使未來 PASS，也不改變此 scope。

---

# 8. Smallest Legal Repair

本輪不需要任何 XQ/Cua/UFO runtime broad rerun。

只做：

```text
TRACK A — post-folder-reorg final freeze
1. 完成所有 folder moves
2. 不再修改 candidate paths
3. git freeze final HEAD

TRACK B — regenerate exact evidence package
4. regenerate final EvidenceManifest from final paths
5. define exact manifest/payload/bundle counters
6. no grouped multi-file denominator rows
7. bind manifest to final HEAD

TRACK C — one final Acceptance Officer run
8. run independent_checker once
9. record one current denominator only
10. mark 144/174/175/176 historical values with subject IDs, not current

TRACK D — render reducer last
11. generate final reducer from machine outputs
12. do not append folder-reorg section after "Final"
13. external mirror/readback

TRACK E — external submission
14. upload final reducer
15. upload final manifest
16. upload raw review bundle
```

不要：

```text
rebuild FDA
rerun RP-002
change pywinauto/Cua architecture
add third profile
add third Heavy Stack
add visual alert gate
authorize live trading
```

---

# 9. Next Final Re-review Stop Conditions

下一輪只需要驗：

```text
ONE final post-reorg subject root
ONE final EvidenceManifest SHA
ONE manifest exact-set definition
ONE current checker denominator

manifest row count = deterministic
bundle count = deterministic
reducer self-entry policy = deterministic
manifest self-entry = 0
hash mismatch = 0
missing path = 0

checker:
PASS
one denominator
failed=0
exit=0
VERIFY_ONLY
maker!=checker

DoD-30 = PASS
DoD-33 = PASS
DoD-36 = PASS

raw required evidence edges reviewed
broker_write=0
blocking contradiction=0
blocking evidence gap=0
```

才可簽：

```text
PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
```

即使如此：

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

仍保持不變。

---

# 10. Final Stop

```text
FDA_EXTERNAL_FOCUSED_REREVIEW_R4 = FAIL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION = SUBSTANTIAL_NOT_OVERTURNED

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

BLOCKING CONFIRMED DEFECTS:
- EXT-FDA-RR4-001 checker denominator 176/174/175 contradiction
- EXT-FDA-RR4-002 manifest exact-set/self-entry contradiction

BLOCKING EVIDENCE GAPS:
- EXT-FDA-RR4-003 post-folder-reorg final subject/manifest rebinding
- EXT-FDA-RR4-004 raw review bundle unavailable

CLOSED:
- prior manifest SHA placeholder
- prior generated_at UTC label defect
- prior UFO2/PAPER/XQ identity reducer multi-value defects

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

REPAIR_CLASS =
EVIDENCE_PACKAGING_AND_POST_REORG_REBIND_ONLY

NEXT =
RESUME_SMALLEST_REPAIR
```

---

# 11. Source Locator Register

## Normative

- `challenge-review-SKILL.md`
  - Role
  - Invariants 1–10
  - Intake
  - Workflow §3 challenge independently
  - Workflow §5 verdict grammar

- `fabric-desktop-automation_藍圖_v2026.08.13-r2.md`
  - FDA_PROFILE_TEAM_ACTIVE DoD-36
  - XQ qualification/action-class 10-run contract
  - one-active-writer
  - readback/checkpoint
  - independent Acceptance Officer
  - SQS live trading claim ceiling

## Prior external

- `FDA_EXTERNAL_FOCUSED_REREVIEW_2026-08-14_r3.md`
  - RR3-001 manifest placeholder
  - RR3-002 denominator/self-entry
  - RR3-003 raw bundle
  - RR3-004 timestamp
  - smallest evidence-packaging-only repair

## Current evidence

- `FDA_IMPLEMENTATION_EVIDENCE(3).md`
  - §0 Claim ceiling
  - §3 Materialized artifacts / denominator
  - §4 Independent checker
  - §7 DoD-36
  - §8 XQ native hybrid
  - §9 External verifier checklist
  - §10 residuals
  - §11 Final
  - §12 Folder reorganization

---

**END OF EXTERNAL FOCUSED REREVIEW R4**
