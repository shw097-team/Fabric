# 《fabric-desktop-automation》外部第五輪 Focused Challenge Review 驗收報告

```yaml
report_id: FDA_EXTERNAL_FOCUSED_REREVIEW_20260814_R5
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review
review_mode: READ_ONLY_CLEAN_ROOM_FOCUSED_REREVIEW
review_time_local: 2026-08-14T11:25:00+08:00

target:
  component: fabric-desktop-automation
  blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2.md
  prior_external_report: FDA_EXTERNAL_FOCUSED_REREVIEW_2026-08-14_r4.md

actual_submitted_evidence:
  file: FDA_IMPLEMENTATION_EVIDENCE(4).md
  sha256: 025bd73d1398686a439cfb2051155dca9783c0ad50ec4cc908d32fb3aae12eb4
  bytes: 12643
  lines: 192

external_verdict: PARTIAL_CHALLENGE
external_acceptance: NOT_GRANTED
formal_all_pass: false

fda_blueprint: PASS
fda_local_implementation_conformance: STRONGLY_SUPPORTED
confirmed_product_architecture_defect: 0
confirmed_current_evidence_reducer_defect: 0

fda_profile_team_active: FAIL_CLOSED
sqs_live_trading: NOT_AUTHORIZED
production_autonomy: NOT_CLAIMED
remote_deployment: NOT_CLAIMED

remaining_blocker:
  type: EVIDENCE_GAP
  id: EXT-FDA-RR5-001
  description: final raw review bundle and its load-bearing raw edges were not directly delivered/readable to the external reviewer

product_rebuild_required: false
broad_rerun_required: false
smallest_next_action: PROVIDE_FINAL_RAW_REVIEW_BUNDLE_FOR_DIRECT_EXTERNAL_READBACK
```

---

# 0. 最終裁決

本輪完整依 `challenge-review-SKILL.md` 執行第五輪 focused clean-room re-review。

適用 hard rules：

```text
existing PASS = claim, not evidence
exact frozen subject binding required
raw deterministic evidence first
tested/executed bytes must match accepted subject
test command / denominator / counts / exit / raw logs must be reviewable
maker != final checker
PASS_CHALLENGE requires every required raw evidence edge in declared scope reviewed
PARTIAL_CHALLENGE applies when meaningful review is complete but required raw evidence edges remain unresolved
```

本輪裁決：

```text
FDA_EXTERNAL_FOCUSED_REREVIEW_R5 = PARTIAL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION_CONFORMANCE = STRONGLY_SUPPORTED
CONFIRMED_PRODUCT_RUNTIME_DEFECT = 0
CONFIRMED_CURRENT_REDUCER_DEFECT = 0

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

NEXT =
PROVIDE_FINAL_RAW_REVIEW_BUNDLE
→ DIRECT_EXTERNAL_REHASH/READBACK
→ FINAL_FOCUSED_ACCEPTANCE
```

這與上一輪不同：

```text
R4 = FAIL_CHALLENGE
```

因為當時存在 checker denominator 與 manifest exact-set 的 **confirmed contradictions**。

本輪這兩項已在 reducer層完成修正，因此不再符合 `FAIL_CHALLENGE` 的條件。

目前唯一剩餘問題是：

```text
raw required evidence edges are referenced but not directly delivered to this external reviewer
```

故正確 verdict 為：

```text
PARTIAL_CHALLENGE
```

---

# 1. Exact submitted evidence identity

本 external reviewer直接對本輪實際附件重算：

```text
file:
FDA_IMPLEMENTATION_EVIDENCE(4).md

sha256:
025bd73d1398686a439cfb2051155dca9783c0ad50ec4cc908d32fb3aae12eb4

bytes:
12643

lines:
192
```

此 exact identity是本輪直接可驗的 final reducer bytes。

Reducer聲明：

```text
single_current_truth:
this file is the ONLY final evidence reducer
machine-generated from final manifest + fresh checker
no mutation after Final
```

本輪未發現文件內 Final 後再追加 mutation 的情況。

---

# 2. R4 blocking findings closure adjudication

| R4 Finding | R5 evidence | External verdict |
|---|---|---|
| RR4-001 checker 176/174/175 contradiction | single current = 179；144/174/175/176 全列 historical | **CLOSED at reducer level** |
| RR4-002 manifest exact-set/self-entry contradiction | rows=54, payload=54, bundle=76, reducer=false, manifest self=false；table 54 rows | **CLOSED at reducer level** |
| RR4-003 post-folder-reorg subject/manifest rebind | final HEAD `e7b289...`; final manifest SHA `b07d...`; checker 179 same freeze | **CLOSED at reducer level** |
| RR4-004 raw bundle unavailable | only reducer MD actually mounted | **NOT CLOSED — EVIDENCE_GAP** |

因此：

```text
confirmed blocking contradiction = 0
blocking raw evidence gap = 1
```

---

# 3. Positive closure verification

## 3.1 Final subject is now single-valued

Reducer只宣稱一個 final subject：

```text
e7b289449775ba9be622d69c0547e7bad1256c18
```

並在：

```text
§1 Final frozen subject
§3 EvidenceManifest
§4 checker current run
§5 DoD-30/33
§6 verifier checklist
§8 Final
```

保持一致。

本輪未找到第二個 current subject root。

## 3.2 Final manifest identity is single-valued

Reducer聲稱：

```text
manifest SHA-256 =
b07d5d810d6ee2d4f18d6acaa93e0661cf43998b5987fbebf9296571aca804ea

schema =
FDA-EVIDENCE-MANIFEST/3

subject_root =
e7b289449775ba9be622d69c0547e7bad1256c18
```

上一輪 placeholder與 pre/post-rebind多值問題已消失。

## 3.3 Exact-set semantics are now internally coherent

Reducer現在明確區分：

```text
manifest_row_count = 54
payload_file_count = 54
bundle_file_count = 76
reducer_in_manifest = false
manifest_self_entry = false
```

並說明：

```text
manifest rows = one filesystem path each
reducer and manifest excluded from manifest rows
bundle count includes non-payload support files
```

本輪 table也實際列出 1..54，沒有再把 reducer自己列成 manifest payload row。

因此上一輪 RR4-002 的 **internal exact-set contradiction已關閉**。

## 3.4 Checker denominator is now single-current

Reducer現在：

```text
CURRENT = 179/179

144 = historical / superseded
174 = historical / superseded
175 = historical / superseded
176 = historical / superseded
```

verifier checklist也要求：

```text
179 checks
```

不再出現 174/175/176同時 current 的問題。

因此：

```text
RR4-001 = CLOSED at reducer level
```

## 3.5 XQ/UFO/claim ceiling未重新漂移

本輪 current reducer仍保持：

```text
UFO² v3.0.8 effective-load = QUALIFIED 7/7
XQ runtime = 3.20.02-260811
PAPER runtime = QUALIFIED claim
wrong_action = 0 claim
silent_wrong_action = 0 claim
broker_write = 0 claim

pywinauto:
XQ_LAUNCH_LOCATE promoted
FN03 Afx locate only 1/1
no broad MFC/Afx promotion

SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

沒有發現新的 claim expansion。

---

# 4. Remaining finding

## EXT-FDA-RR5-001 — Final raw review bundle is still not directly reviewable

### Finding

Current reducer給出非常完整的 raw bundle index，包括：

```text
54 manifest rows
76 physical bundle files
manifest SHA
subject root
checker 179/179
SensorLog 56 records
UFO2 7/7 receipt
XQ fingerprint
matrix / tests / receipts
```

但本輪實際 external reviewer可讀輸入中，只有：

```text
FDA_IMPLEMENTATION_EVIDENCE(4).md
```

本 reviewer檢查 mounted workspace，也沒有取得 reducer所引用的：

```text
FDA_EVIDENCE_MANIFEST.json
FDA_RAW_REVIEW_BUNDLE/*
independent_checker raw output/receipt
SensorLog raw extract/database/query result
SensorList raw extract
FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json
FDA_XQ_PAPER_RUNTIME_RECEIPT.json
final git subject repository/readback
```

因此不能獨立重算：

```text
manifest SHA = b07d...
54/54 hash match
bundle files = 76
git HEAD = e7b289...
checker = 179/179
UFO2 = 7/7
SensorLog = 56 rows
PAPER mandatory XQ action classes = 10/10
```

Challenge-review明確規定：

```text
existing PASS is not evidence
raw deterministic evidence first
confirm tested/executed bytes
confirm command/denominator/counts/exit/raw logs
PASS_CHALLENGE only when every required raw edge was reviewed
```

所以本 reviewer不能把 reducer中的 summary/index claim轉寫成「已獨立驗證」。

```yaml
finding_id: EXT-FDA-RR5-001
classification: EVIDENCE_GAP
blocking_for_pass_challenge: true

acceptance_edges:
  - exact final subject
  - EvidenceManifest integrity
  - DoD-13
  - DoD-17
  - DoD-18
  - DoD-19
  - DoD-25
  - DoD-30
  - DoD-33
  - DoD-35
  - DoD-36

earliest_owner: FDA_EVIDENCE_PACKAGER

smallest_repair:
  - provide the already-frozen final EvidenceManifest as a native file
  - provide the final raw review bundle, or the minimum load-bearing native raw files
  - do not mutate product/runtime/candidate

focused_retest:
  - external SHA-256 of manifest
  - manifest JSON parse and subject_root
  - 54 unique rows
  - 54/54 path/hash/size match
  - raw checker 179/179, exit=0, verify-only
  - UFO2 7/7 raw receipt
  - XQ PAPER raw receipt + SensorLog/SensorList
  - wrong_action=0
  - silent_wrong_action=0
  - broker_write=0
  - final subject root readback

affected_regression:
  - none unless raw bytes disagree with reducer

product_rebuild_required: false
broad_rerun_required: false
```

---

# 5. DoD-17 specific external status

Blueprint r2明文要求：

```text
STEP 9:
10 fresh runs/provider per applicable XQ PAPER action class

DoD-17:
every mandatory XQ PAPER action class
has >=1 provider with 10/10 fresh runs
```

Current reducer宣稱 DoD-17 PASS，並提供：

```text
SensorLog 56 records
FDAPaperFinal020037 14 rows
state 2→3→1
ExecState 1→8
2330.TW
2 trigger cycles
SensorList 6 strategies
wash-complete
```

這是有價值的 runtime evidence index，但 reducer本身沒有展開每一 mandatory action class 的：

```text
10 fresh run IDs
10/10 denominator
per-run readback
wrong_action
silent_wrong_action
```

因此本輪對 DoD-17 的精確 external adjudication是：

```text
LOCAL/AO CLAIM = PASS
CURRENT REDUCER CONSISTENCY = PASS
EXTERNAL RAW CHALLENGE = PENDING
```

不判 FAIL，因為 raw receipt可能確實包含這些紀錄；但在 raw receipt未交付前，也不能 external PASS。

---

# 6. DoD-33 specific external status

Reducer current checker現在很乾淨：

```text
179/179
failed=0
exit=0
VERIFY_ONLY
maker != checker
subject = e7b289...
```

而且歷史 denominator皆明確降級。

所以：

```text
DENOMINATOR_CONSISTENCY = PASS
```

但是 external reviewer未取得 checker raw receipt/stdout，也無法執行 repo內 checker。

因此：

```text
DoD-33 LOCAL/AO = PASS CLAIM
DoD-33 EXTERNAL RAW = PENDING
```

---

# 7. Gate Calibration Failure defense

## Objective alignment

PASS。

FDA仍是受治理 Windows desktop automation，不是 live trading authority。

## Risk proportionality

PASS。

沒有因需要 external raw readback而要求產品重做或新增功能。

## False-positive defense

本輪沒有因「manifest列了54個 SHA」「checker寫179/179」就把 summary proxy提升為 raw external PASS。

## Anti-overfitting

PASS。

pywinauto仍只 promotion已宣稱 qualified 的 `XQ_LAUNCH_LOCATE`；FN03保持 locate-only。

## No-new-gate

PASS。

本輪沒有把盤中 visual alert、Cua 0.19.4 nightly或 FN03 invoke加成 FDA r2 mandatory gate。

---

# 8. Current engineering assessment

### 是否確認 FDA implementation 有施工缺陷？

```text
NO CONFIRMED PRODUCT/RUNTIME DEFECT
```

### 是否確認 current reducer 有 consistency defect？

```text
NO
```

### 是否需要重做 FDA / RP-002？

```text
NO
```

### 是否需要 broad rerun？

```text
NO
```

### 是否已足以正式 external ALL PASS？

```text
NO
```

原因只剩：

```text
required load-bearing raw evidence
has not been directly reviewed
```

因此工程上最精確的狀態為：

```text
FDA_IMPLEMENTATION_COMPLETENESS
= PASS_CANDIDATE / STRONGLY_SUPPORTED

CONFIRMED_IMPLEMENTATION_DEFECT
= 0

FORMAL_EXTERNAL_ACCEPTANCE
= PENDING_RAW_READBACK_ONLY
```

---

# 9. Smallest next action

不再改 candidate。

只交付已存在的 frozen raw evidence：

```text
minimum external set:

1. FDA_EVIDENCE_MANIFEST.json
2. independent checker final raw receipt / stdout
3. FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json
4. FDA_XQ_PAPER_RUNTIME_RECEIPT.json
5. SensorLog/SensorList deterministic raw extract or DB/query output
6. F01/F06 wrong/silent-wrong raw receipt(s)
7. no-live/broker_write negative receipt
8. final subject-root readback / git receipt
```

若完整 76-file bundle方便，直接提交 entire final bundle亦可。

**不要再次 regenerate / mutate candidate**，除非 raw readback真的發現 mismatch。

---

# 10. Final promotion condition

下一輪若 external reviewer能直接確認：

```text
manifest SHA = b07d5d810d6ee2d4f18d6acaa93e0661cf43998b5987fbebf9296571aca804ea
subject root = e7b289449775ba9be622d69c0547e7bad1256c18

manifest rows = 54
unique = 54
missing = 0
hash mismatch = 0

checker = 179/179
failed = 0
exit = 0
VERIFY_ONLY
maker != checker

UFO2 7/7 = raw verified
XQ PAPER 10/10 applicable action classes = raw verified
wrong_action = 0
silent_wrong_action = 0
broker_write = 0

DoD-36 blocking contradiction = 0
blocking evidence gap = 0
```

即可簽：

```text
PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
```

但即使如此：

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

不變。

---

# 11. Final Stop

```text
FDA_EXTERNAL_FOCUSED_REREVIEW_R5 = PARTIAL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION_CONFORMANCE = STRONGLY_SUPPORTED
CONFIRMED_PRODUCT_RUNTIME_DEFECT = 0
CONFIRMED_CURRENT_EVIDENCE_REDUCER_DEFECT = 0

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

REMAINING_BLOCKER:
EXT-FDA-RR5-001
= FINAL RAW REVIEW BUNDLE NOT DIRECTLY REVIEWED

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

NEXT =
PROVIDE_EXISTING_FROZEN_RAW_EVIDENCE_ONLY
```

---

# 12. Source Locator Register

## Normative

- `challenge-review-SKILL.md`
  - independent challenge workflow
  - exact digest / tested bytes
  - test denominator/count/exit/raw logs
  - no proxy-to-PASS
  - verdict grammar

- `fabric-desktop-automation_藍圖_v2026.08.13-r2.md`
  - STEP 9: XQ PAPER / NO-LIVE-WRITE, 10 fresh runs/provider per applicable action class
  - STEP 13: fresh independent Acceptance Officer
  - §10.1 DoD-13/17/18/19/25/30/33/35/36
  - otherwise FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

## Prior external

- `FDA_EXTERNAL_FOCUSED_REREVIEW_2026-08-14_r4.md`
  - RR4-001 checker denominator
  - RR4-002 exact-set semantics
  - RR4-003 post-folder-reorg rebind
  - RR4-004 raw bundle unavailable

## Current evidence

- `FDA_IMPLEMENTATION_EVIDENCE(4).md`
  - exact external SHA `025bd73d1398686a439cfb2051155dca9783c0ad50ec4cc908d32fb3aae12eb4`
  - §1 final frozen subject
  - §2 exact set
  - §3 final manifest table
  - §4 checker 179
  - §5 DoD-36
  - §6 verifier checklist
  - §8 Final

---

**END OF EXTERNAL FOCUSED REREVIEW R5**
