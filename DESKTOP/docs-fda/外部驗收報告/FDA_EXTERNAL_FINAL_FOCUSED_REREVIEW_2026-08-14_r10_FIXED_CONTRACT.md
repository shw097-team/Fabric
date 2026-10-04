# 《fabric-desktop-automation》外部第十輪固定合約驗收報告

```yaml
report_id: FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_20260814_R10_FIXED_CONTRACT
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review + corrected no-moving-goalpost contract
review_time_local: 2026-08-14T16:33:00+08:00

supersedes_method:
  - original moving-root acceptance loop
inherits_method:
  - FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_2026-08-14_r9_CORRECTED.md

submitted_evidence:
  file: FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8(1).md
  external_recomputed_sha256: 4150385fb15dd73151f971e4dfef52a993b9725d2ea7cb124b16b46666ca3bf3
  bytes: 69742
  lines: 2362

fixed_identity_model:
  candidate_root: be576bebe7672093039bfe7dbc265f25aa0a1164
  evaluator_sha256: 9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
  evidence_bundle_root: independent_from_candidate
  candidate_mutation_after_freeze: DENY

external_verdict: PARTIAL_CHALLENGE
external_acceptance: NOT_GRANTED_YET
formal_all_pass: false

fda_blueprint: PASS
fda_architecture: PASS
fda_runtime_qualification: PASS_CANDIDATE
fda_local_implementation: PASS_CANDIDATE
fda_profile_team_active: FAIL_CLOSED_EVIDENCE_RESEAL_ONLY

confirmed_product_defect: 0
confirmed_runtime_blocker: 0
runtime_rerun_required: false
broad_rerun_required: false
product_rebuild_required: false

remaining_work:
  class: EVIDENCE_RESEAL_ONLY
  blockers:
    - manifest exact_set count metadata stale (54 vs actual 63)
    - manifest generated_at stale relative to bound final evidence
    - evaluator digest not structured-bound in manifest
```

---

# 0. 本輪驗收方法

本輪不再採用會移動 goalpost 的舊模式，而完全沿用已校正並凍結的固定合約：

```text
Candidate Root
!= Evaluator Identity
!= Evidence Bundle Root
```

其中：

```text
Candidate Root =
be576bebe7672093039bfe7dbc265f25aa0a1164

Evaluator Identity =
9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
```

後續 evidence / manifest / review report 的產生不得再要求 candidate root跟著改變。

本輪亦維持先前校正：

```text
single-wash auto-terminal 10x
= current PAPER scenario可接受 terminal qualification

explicit manual STOP 10x
= NOT REQUIRED for current single-wash acceptance
```

因此本輪**不新增任何 runtime gate**。

---

# 1. Exact received evidence identity

External reviewer直接對收到的附件重算：

```text
FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8(1).md

SHA-256 =
4150385fb15dd73151f971e4dfef52a993b9725d2ea7cb124b16b46666ca3bf3

bytes = 69,742
lines = 2,362
```

文件包含四個完整 JSON body：

```text
1. FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8
2. FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7
3. FDA_CHECKER_FINAL_RR7
4. FDA_EVIDENCE_MANIFEST
```

---

# 2. Runtime / capability acceptance status

本輪依固定 scope，不重新擴張 gate。

## 2.1 XQ exact-build

```text
XQ = 3.20.02
build = 260811
```

### Verdict

```text
PASS
```

## 2.2 F01 current-build qualification

Current receipt已證：

```text
10/10
wrong_action = 0
silent_wrong_action = 0
```

### Verdict

```text
PASS
```

## 2.3 F06 fresh compile qualification

Current receipt已有十次 distinct compile evidence。

### Verdict

```text
PASS
```

## 2.4 UFO² effective-load

Carried raw qualification：

```text
v3.0.8
7/7
```

### Verdict

```text
PASS
```

## 2.5 PAPER single-wash

Current evidence提供：

```text
10 run IDs
single-wash lifecycle
post-terminal readback
wrong_action = 0
silent_wrong_action = 0
broker_write = 0
one_active_writer = true
```

且前序校正已確認 current single-wash scenario不再額外要求 manual STOP 10x。

### Verdict

```text
PAPER_SINGLE_WASH_10X = PASS
DoD-17 current applicable scenario = PASS
```

---

# 3. Final checker — PASS

本輪機械 parse：

```text
declared total_checks = 194
actual raw_records = 194
actual unique IDs = 194
PASS records = 194
failed = 0
errors = 0
exit = 0
mode = VERIFY_ONLY
subject_root = be576bebe...
```

歷史 denominator：

```text
144 = HISTORICAL
174 = HISTORICAL
175 = HISTORICAL
176 = HISTORICAL
179 = HISTORICAL
194 = CURRENT
```

本輪沒有再出現第二個 CURRENT checker。

### Verdict

```text
CHECKER_DENOMINATOR = PASS
CHECKER_RAW_RECORDS = PASS
CHECKER_UNIQUE_IDS = PASS
CHECKER_CURRENTNESS = PASS
CHECKER_SUBJECT = PASS
```

---

# 4. Canonical embedded manifest identity — PASS

Section 4 的 embedded manifest raw body以原始 LF bytes重算：

```text
SHA-256 =
0dd7a6d2d04fcd6390e7623167489a6e9808ac126a2025eb80052cf331a69ab9
```

與文件聲明完全一致。

本輪固定驗收方法允許：

```text
embedded reviewer-verifiable manifest
= canonical evidence serialization
```

因此文件另外提及的：

```text
on-disk re-serialized SHA =
b95492888efa4ee9e83a30183032885f7817e3d327c43a106991877e516729a5
```

只要明確視為 **NON_CANONICAL_RENDERING**，不再自動形成第二個 final manifest identity。

### Verdict

```text
CANONICAL_MANIFEST_SHA = PASS
```

這裡不再重犯舊驗收方式把不同 JSON serialization一律升格為 candidate defect的問題。

---

# 5. Remaining evidence-only preflight failures

目前剩餘問題全部屬 `EVIDENCE_RESEAL_ONLY`。

## EXT-FDA-R10-001 — exact_set count metadata仍是舊值

Manifest structured data：

```text
artifact_count = 63
actual artifacts array = 63
unique paths = 63
duplicate paths = 0
```

但 `exact_set` 仍寫：

```text
manifest_row_count = 54
payload_file_count = 54
```

且 note仍聲稱：

```text
manifest_row_count == payload_file_count == number of rows
```

因此 machine preflight：

```text
artifact_count == len(artifacts)      = PASS
unique_path_count == artifact_count  = PASS
manifest_row_count == artifact_count = FAIL
payload_file_count == artifact_count = FAIL
```

### Classification

```yaml
classification: EVIDENCE_RESEAL_GAP
runtime_blocker: false
product_defect: false
blocking_for_external_final_seal: true
```

### Smallest repair

只把 exact_set counters由 artifacts[] machine-derive：

```text
manifest_row_count = 63
payload_file_count = 63
```

不准重跑 runtime。

---

## EXT-FDA-R10-002 — manifest chronology metadata仍未 final-reseal

Manifest：

```text
generated_at_utc =
2026-08-14T03:21:39Z
= 2026-08-14 11:21:39 +08:00
```

但同一 final evidence set綁定後續：

```text
PAPER STOP receipt =
2026-08-14 14:35:32 +08:00

final checker =
2026-08-14 14:37:10 +08:00

PAPER semantics authority =
2026-08-14 14:54:27 +08:00
```

因此固定 preflight：

```text
manifest.generated_at > latest bound evidence timestamp
```

仍是：

```text
FAIL
```

### Classification

```yaml
classification: EVIDENCE_RESEAL_GAP
runtime_blocker: false
product_defect: false
blocking_for_external_final_seal: true
```

### Smallest repair

final EvidenceManifest必須**最後生成**，timestamp晚於所有 bound evidence。

不需要 candidate commit，不需要 runtime rerun。

---

## EXT-FDA-R10-003 — evaluator identity尚未 structured-bound

固定合約要求：

```text
Evaluator Identity =
9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
```

Current checker raw receipt確實提供：

```text
script_sha256 = 9009713...
```

Manifest `subject_root.note` 也提到：

```text
evaluator 9009713
```

但 manifest沒有 machine-readable structured field：

```json
"evaluator": {
  "sha256": "9009713..."
}
```

或等價欄位。

固定 preflight明確要求：

```text
manifest.evaluator_sha == final evaluator digest
```

目前只能由 prose/note推知，不能 machine-check。

### Classification

```yaml
classification: EVIDENCE_RESEAL_GAP
runtime_blocker: false
product_defect: false
blocking_for_external_final_seal: true
```

### Smallest repair

在 final reseal manifest加入 structured evaluator identity，例如：

```json
"evaluator": {
  "artifact": "independent_checker.py",
  "sha256": "9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e",
  "mode": "VERIFY_ONLY"
}
```

**不要求 evaluator重新執行**，因 current 194/194 raw receipt本身已通過。

---

# 6. Manifest current-state改善確認

相較前一版，本輪已有實質改善：

```text
artifact_count = 63
actual artifacts = 63
unique paths = 63

194 = ONLY CURRENT checker
179 and earlier = HISTORICAL

checker.subject_root = be576...
checker note = be576...

serialization = SINGLE_CANONICAL
```

因此先前的：

```text
179仍 CURRENT
stale checker HEAD note
```

已閉合。

---

# 7. Candidate / evaluator / evidence root separation adjudication

本輪不再要求：

```text
manifest中的 candidate independent_checker.py row hash
==
final evaluator digest
```

兩者可屬不同 identity layer。

正確 final record應是：

```yaml
candidate:
  root: be576bebe...

evaluator:
  sha256: 9009713...

evidence_bundle:
  manifest_sha256: 0dd7a6d2...
```

因此：

```text
Candidate Root = PASS
Evaluator Receipt = PASS
Canonical Manifest Body = PASS
Cross-layer structured binding = PARTIAL
```

剩下只是將三者在 final manifest用 structured fields明確關聯。

---

# 8. Fixed promotion matrix

| Acceptance Edge | R10 Fixed-Contract Verdict |
|---|---|
| FDA blueprint | PASS |
| FDA architecture | PASS |
| XQ 3.20.02-260811 | PASS |
| F01 current 10/10 | PASS |
| F06 fresh 10/10 | PASS |
| UFO² 7/7 | PASS |
| PAPER single-wash 10x | PASS |
| wrong_action=0 | PASS |
| silent_wrong_action=0 | PASS |
| broker_write=0 | PASS |
| one-active-writer | PASS |
| checker 194/194 | PASS |
| checker unique/current | PASS |
| canonical manifest SHA | PASS |
| manifest actual artifacts=63 | PASS |
| manifest exact_set counters | **PARTIAL / stale 54** |
| manifest chronology | **PARTIAL / stale timestamp** |
| structured evaluator binding | **PARTIAL / missing field** |
| confirmed runtime blocker | 0 |
| external final ALL PASS | NOT YET |

---

# 9. Final engineering judgment

目前最精確狀態：

```text
FDA_RUNTIME_QUALIFICATION = PASS_CANDIDATE
FDA_IMPLEMENTATION = PASS_CANDIDATE

CONFIRMED_PRODUCT_DEFECT = 0
CONFIRMED_RUNTIME_BLOCKER = 0
RUNTIME_RERUN_REQUIRED = NO
PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

EXTERNAL_CHALLENGE = PARTIAL_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = PENDING_EVIDENCE_RESEAL_ONLY
```

這不是 runtime還沒做好。

是：

```text
final machine-readable seal
尚有 3 個 preflight欄位沒有完全 reseal
```

---

# 10. 唯一允許的最後修補

**不得再修改 candidate，不得再跑 runtime。**

只重新 machine-generate EvidenceManifest：

```yaml
subject_root:
  candidate_root: be576bebe7672093039bfe7dbc265f25aa0a1164

evaluator:
  sha256: 9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e
  mode: VERIFY_ONLY

checker:
  total_checks: 194
  unique_ids: 194
  failed: 0
  errors: 0
  exit: 0

exact_set:
  manifest_row_count: 63
  payload_file_count: 63

artifact_count: 63

generated_at:
  AFTER all bound evidence timestamps
```

並：

```text
ONE canonical serialization
ONE canonical manifest SHA
```

完成前跑 machine preflight：

```text
candidate_root_count = 1
current_checker_count = 1
manifest_sha_count = 1

artifact_count = 63
len(artifacts) = 63
unique paths = 63
manifest_row_count = 63
payload_file_count = 63

checker total = 194
raw records = 194
unique = 194
passed = 194
failed = 0
errors = 0
exit = 0

manifest.evaluator_sha = 9009713...
manifest.generated_at > latest bound evidence
```

全部 PASS才交外部 reviewer。

---

# 11. No-Moving-Goalpost Commitment

下一輪不得新增：

```text
explicit STOP 10x
intraday visual alert
Cua 0.19.4 nightly
FN03 invoke
additional runtime fixtures
new action classes
new architecture gates
```

下一輪只允許驗：

```text
R10-001 exact-set counters
R10-002 manifest chronology
R10-003 evaluator structured binding
canonical manifest SHA
```

四者完成，即可考慮：

```text
PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
```

---

# 12. Scope Ceiling

即使最終 PASS：

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

維持不變。

---

# 13. Final Stop

```text
FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_R10_FIXED_CONTRACT
= PARTIAL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_ARCHITECTURE = PASS
FDA_RUNTIME_QUALIFICATION = PASS_CANDIDATE
FDA_LOCAL_IMPLEMENTATION = PASS_CANDIDATE

CONFIRMED_PRODUCT_DEFECT = 0
CONFIRMED_RUNTIME_BLOCKER = 0

REMAINING:
- EXT-FDA-R10-001 exact_set 54 -> must derive 63
- EXT-FDA-R10-002 manifest generated_at must be final
- EXT-FDA-R10-003 evaluator SHA must be structured-bound

FDA_EXTERNAL_ACCEPTANCE =
PENDING_EVIDENCE_RESEAL_ONLY

PRODUCT_REBUILD_REQUIRED = NO
RUNTIME_RERUN_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

ONLY_NEXT_ACTION =
FINAL EVIDENCE MANIFEST RESEAL
```

**END OF R10 FIXED-CONTRACT EXTERNAL REVIEW**
