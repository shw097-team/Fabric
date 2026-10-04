# 《fabric-desktop-automation》外部第六輪 Final Focused Challenge Review 驗收報告

```yaml
report_id: FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_20260814_R6
review_role: Fabric External Independent Challenge Reviewer
review_method: challenge-review
review_mode: READ_ONLY_CLEAN_ROOM_FINAL_FOCUSED_REREVIEW
review_time_local: 2026-08-14T11:34:00+08:00

target:
  component: fabric-desktop-automation
  blueprint: fabric-desktop-automation_藍圖_v2026.08.13-r2.md
  prior_external_report: FDA_EXTERNAL_FOCUSED_REREVIEW_2026-08-14_r5.md

submitted_raw_evidence:
  file: FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md
  external_recomputed_sha256: 41eb23c14bcaba0c9fcbee922d24a0bb0359d524cb4d7e84b99b9c5ed769db2c
  bytes: 37356
  lines: 1998

external_verdict: FAIL_CHALLENGE
external_acceptance: NOT_GRANTED
formal_all_pass: false

fda_blueprint: PASS
fda_local_implementation: SUBSTANTIAL_NOT_OVERTURNED
fda_profile_team_active: FAIL_CLOSED

sqs_live_trading: NOT_AUTHORIZED
production_autonomy: NOT_CLAIMED
remote_deployment: NOT_CLAIMED

confirmed_product_architecture_defect: 0
confirmed_evidence_binding_defects: 2
blocking_evidence_gaps: 2
non_blocking_packaging_defects: 2

product_rebuild_required: false
broad_rerun_required: false
recommended_resume: RESUME_SMALLEST_REPAIR
```

---

# 0. 最終裁決

本輪依 `challenge-review-SKILL.md` 重新從 raw deterministic evidence 挑戰上一輪的 PASS candidate。

適用 hard rules：

```text
existing PASS = claim, not evidence
exact frozen subject binding required
raw deterministic evidence first
tested/executed bytes must match accepted subject
test command / denominator / counts / exit / raw logs must be reviewable
reject stale binding / proxy-to-PASS
try to falsify every major PASS
```

本輪 verdict：

```text
FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_R6 = FAIL_CHALLENGE

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION = SUBSTANTIAL_NOT_OVERTURNED

PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

NEXT = RESUME_SMALLEST_REPAIR
```

上一輪 R5 唯一 blocker「raw evidence not delivered」本輪已**實質改善**：manifest、UFO² receipt、XQ PAPER receipt、SensorLog/SensorList extract、F01/F06 receipts、broker-write negative都已內嵌。

但 raw evidence 一旦可直接檢查，發現新的 blocking problems，因此不能從 `PARTIAL_CHALLENGE` 直接提升成 `PASS_CHALLENGE`。

核心阻斷：

1. current F01 raw receipt綁的是 **XQ 3.18.02 / 260102**，不是 final XQ subject **3.20.02 / 260811**；
2. DoD-17要求每個 applicable XQ PAPER action class **10 fresh runs/provider**，但 current PAPER raw receipt只展示 3 個 runtime strategy groups、合計 8 個 ExecState=1 execution starts，沒有 10 fresh-run denominator；
3. F06「10-run」receipt十筆 `LastCompileTime` 全部相同到毫秒，無法證明 10 次 fresh compile；
4. checker「fresh raw stdout」本身是截斷片段，沒有完整 179-check denominator與 final summary。

因此至少存在 blocking stale-subject / denominator defects，符合 `FAIL_CHALLENGE` 而非 `PARTIAL_CHALLENGE`。

---

# 1. Exact Evidence Identity

## 1.1 External byte readback

本 external reviewer直接對實際上傳 bytes 計算：

```text
file:
FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md

actual SHA-256:
41eb23c14bcaba0c9fcbee922d24a0bb0359d524cb4d7e84b99b9c5ed769db2c

bytes:
37356

lines:
1998
```

文件 header 自稱：

```text
this_file_sha256 =
4611fe561ac1d539581e1161fd9906f4bbb829d1c7c49ca816b44a5298bd4820
```

與 actual bytes **不相等**。

此欄位屬 self-referential metadata；external reviewer已能以實際 bytes重新綁定，所以本輪將其列為 non-blocking packaging defect，而不是單獨阻斷 candidate。

正確作法是移除 self-hash，或由 sidecar / mirror receipt記錄 container SHA。

---

# 2. EvidenceManifest independent verification

內嵌 manifest body可直接 parse。

External readback：

```text
schema = FDA-EVIDENCE-MANIFEST/3
subject_root =
e7b289449775ba9be622d69c0547e7bad1256c18

artifact_count field = 54
actual artifact objects = 54
unique paths = 54
duplicate paths = 0

manifest_row_count = 54
payload_file_count = 54
bundle_file_count = 76
reducer_in_manifest = false
manifest_self_entry = false
```

本 reviewer以 embedded manifest JSON 的 LF canonical bytes重算：

```text
SHA-256 =
b07d5d810d6ee2d4f18d6acaa93e0661cf43998b5987fbebf9296571aca804ea
```

**精確等於 submitted manifest claim。**

所以：

```text
MANIFEST_BODY_IDENTITY = PASS
MANIFEST_INTERNAL_EXACT_SET = PASS
```

---

# 3. Embedded raw-body ↔ manifest hash verification

本 reviewer直接從 single MD抽取 full JSON body並以 manifest source newline semantics重算 SHA：

| Raw body | External SHA | Manifest SHA | Result |
|---|---|---|---|
| FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json | `1d7d149a...97781` | same | PASS |
| FDA_XQ_PAPER_RUNTIME_RECEIPT.json | `1730e416...905a74` | same | PASS |
| FDA_F01_LIVE_FIXTURE_RECEIPT.json | `36fff6f5...8d8697` | same | PASS |
| FDA_F06_TEN_RUN_RECEIPT.json | `17353bfb...5d97c` | same | PASS |

因此本輪 finding不是「raw body被抄錯」。

恰恰相反：

```text
embedded raw body = manifest-bound bytes
```

所以 raw body中的 stale subject / denominator缺口可以作 deterministic challenge evidence。

---

# 4. Positive closure — UFO² DoD-13

`FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json` raw body具備：

```text
provider = MICROSOFT_UFO2
pin = v3.0.8
mode = LOCAL_NO_LIVE_WRITE

PACKAGE_IMPORT = PASS
PLACEHOLDER_SERVICE = PASS
UIA_BACKEND = PASS
OPENAI_SERVICE = PASS
CONFIG_PARSE = PASS
LLM_BACKEND_OPENCODE_GO = PASS
AGENT_MODULES = PASS

verdict = PASS
wrong_action = 0
silent_wrong_action = 0
side_effect = NONE
```

本輪 external review認定：

```text
DoD-13 UFO² effective-load = PASS
```

注意 claim ceiling仍只到 effective-load；receipt自己也明確說 full AppAgent desktop execution是 separate qualification。

本 reviewer不額外新增該 gate。

---

# 5. Blocking Finding RR6-001 — F01 current-subject stale binding

## Raw finding

Final FDA subject現在是：

```text
XQ 3.20.02 / build 260811
```

但本輪用來關閉 F01 wrong/silent-wrong的 full raw receipt：

```text
FDA_F01_LIVE_FIXTURE_RECEIPT.json
```

其 `target.product_version` 明確是：

```text
3.18.02 (260102)
```

十個 run的 window title也全部是：

```text
[版本 3.18.02 260102]
```

也就是：

```text
current accepted subject = 3.20.02-260811
submitted F01 raw subject = 3.18.02-260102
```

兩者不是同一 exact subject。

而 blueprint/最新版 XQ修補契約對 version drift的規則正是：

```text
new XQ build
→ affected action class requalify
→ cannot assume selector compatibility
```

所以舊 build的 10/10不能被拿來閉合 current F01。

### 另有 receipt-local contradiction

Receipt欄位寫：

```text
login_state = NOT_LOGGED_IN
```

但每個 run title都顯示：

```text
SHW097:已登入
```

這進一步顯示該 receipt的 target metadata不是 current normalized truth。

```yaml
finding_id: EXT-FDA-RR6-001
classification: CONFIRMED_DEFECT
blocking: true

acceptance_id:
  - DoD-17 current mandatory action class qualification
  - DoD-18 wrong_action=0
  - DoD-19 silent_wrong_action=0
  - DoD-35 current XQ consumer binding

evidence_id:
  - FDA_F01_LIVE_FIXTURE_RECEIPT.json
  - final subject e7b289... / XQ 3.20.02-260811

earliest_owner: FDA_XQ_EVIDENCE_OWNER

smallest_repair:
  - do NOT rerun broad FDA
  - provide current-build F01 receipt if it already exists
  - preferably provide FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json for 260811 FN01 10/10
  - if no current receipt exists, rerun only XQ_LAUNCH_LOCATE 10x on 260811

focused_retest:
  - exact XQ fingerprint 3.20.02-260811
  - 10 distinct run IDs
  - readback each run
  - wrong_action=0
  - silent_wrong_action=0

affected_regression:
  - XQ_LAUNCH_LOCATE only
```

---

# 6. Blocking Finding RR6-002 — PAPER runtime raw evidence does not meet 10-fresh-run denominator

Blueprint STEP 9 hard requirement：

```text
Run 12-fixture XQ matrix.
10 fresh runs/provider per applicable action class.
wrong_action = 0
silent_wrong_action = 0
```

Current XQ PAPER receipt proves useful runtime execution：

```text
environment = PAPER
XQ = 3.20.02 / 260811
broker_write = 0
one_active_writer = true
```

並有三個 execution proof groups：

```text
FDAPaperProbe010447
FDAPaperClosure011939
FDAPaperFinal020037
```

從 receipt自己的 `exec_flow` 可直接計算 ExecState=1：

```text
Probe   = 2
Closure = 4
Final   = 2

total execution starts = 8
```

也就是 raw receipt目前可證明的 execution cycles是 **8**，不是 10。

它提供 56 SensorLog records，但：

```text
56 internal state/log rows
≠ 10 fresh runs
```

而且所謂 raw SensorLog extract只內嵌：

```text
first 30 rows
```

不是全部 56 rows。

因此：

```text
runtime engine execution = STRONGLY SUPPORTED
DoD-17 exact 10-fresh-run denominator = NOT MET BY SUBMITTED RAW EVIDENCE
```

```yaml
finding_id: EXT-FDA-RR6-002
classification: CONFIRMED_DEFECT
blocking: true

acceptance_id:
  - DoD-17
  - STEP 9 XQ PAPER 10-fresh-run qualification

evidence_id:
  - FDA_XQ_PAPER_RUNTIME_RECEIPT.json
  - SensorLog embedded extract

earliest_owner: FDA_XQ_RUNTIME_QUALIFICATION_OWNER

smallest_repair:
  - preserve current 260811 candidate
  - run only missing focused PAPER qualification attempts
  - materialize explicit 10-run denominator per applicable PAPER action class
  - do not use SensorLog row count as run count

focused_retest:
  - run_id 1..10
  - action_class
  - provider/backend
  - config/start/status/stop readback as applicable
  - per-run terminal state
  - wrong_action
  - silent_wrong_action
  - broker_write=0
  - one_active_writer=true

affected_regression:
  - XQ PAPER action classes only
```

盤中 visual alert仍不是 mandatory gate；本輪不新增它。

---

# 7. Blocking Evidence Gap RR6-003 — F06 10-run receipt does not prove ten fresh compiles

`FDA_F06_TEN_RUN_RECEIPT.json` 有十個 run entries，也宣稱：

```text
pass_count = 10
required = 10
wrong_action = 0
silent_wrong_action = 0
```

但十筆 run的：

```text
last_compile
```

全部完全相同：

```text
2026-08-13 16:30:08.395
```

每筆 elapsed約 7.2s。

對 file-readback contract而言，如果每一次真的是 fresh compile，最關鍵的 mutation/readback字段 `LastCompileTime` 應能區別事件；目前 receipt只證明十筆紀錄引用同一 compile timestamp。

因此不能由此 raw receipt獨立確認：

```text
10 distinct compile executions
```

```yaml
finding_id: EXT-FDA-RR6-003
classification: EVIDENCE_GAP
blocking_for_pass_challenge: true

acceptance_id:
  - XS_COMPILE_PASS 10/10
  - STEP 9 fresh-run semantics

earliest_owner: FDA_XS_FIXTURE_EVIDENCE_OWNER

smallest_repair:
  - if true per-run raw timestamps/logs already exist, submit them
  - otherwise rerun F06 only
  - each run must have unique invocation/readback evidence

focused_retest:
  - 10 distinct invocation IDs
  - per-run LastCompileTime or equivalent monotonic proof
  - CompileStatus=1
  - empty CompileMsg
  - wrong_action=0
  - silent_wrong_action=0

affected_regression:
  - F06 only
```

這不是確認 XQ compiler有 product defect；是確認 current receipt不足以證明「fresh 10x」。

---

# 8. Blocking Evidence Gap RR6-004 — checker raw stdout is truncated

Section 3標題宣稱：

```text
Independent checker — fresh raw stdout
```

且寫：

```text
exit: 0
```

但是內嵌 block：

- 開頭直接從一個 JSON object的中段開始；
- 沒有完整 opening structure；
- 只包含尾端一部分 T143/T160..T177/T150/T151；
- 沒有完整 179 個 check records；
- 沒有 raw final summary `179/179 / failed=0`。

所以：

```text
checker denominator consistency in manifest = GOOD
checker raw execution completeness = NOT VERIFIED
```

```yaml
finding_id: EXT-FDA-RR6-004
classification: EVIDENCE_GAP
blocking_for_pass_challenge: true

acceptance_id:
  - DoD-33 independent Acceptance Officer

earliest_owner: FDA_ACCEPTANCE_EVIDENCE_OWNER

smallest_repair:
  - submit untruncated stdout/JSON receipt from the already-frozen 179 run
  - no product mutation

focused_retest:
  - command
  - script SHA
  - subject root
  - total checks=179
  - passed=179
  - failed=0
  - error=0
  - exit=0
  - VERIFY_ONLY
  - maker!=checker

affected_regression:
  - acceptance evidence only
```

---

# 9. Non-blocking Finding RR6-005 — raw container self-hash mismatch

Raw container claims：

```text
4611fe561ac1d539...
```

External SHA is：

```text
41eb23c14bcaba0c9fcbee922d24a0bb0359d524cb4d7e84b99b9c5ed769db2c
```

Mismatch confirmed。

Because this file is not itself part of the candidate EvidenceManifest and external reviewer has independently bound the received bytes, this does **not** by itself invalidate FDA runtime evidence.

Recommended repair：

```text
remove self-hash from inside self-referential MD
or publish sidecar hash/mirror receipt
```

```yaml
classification: CONFIRMED_DEFECT
blocking: false
```

---

# 10. Additional evidence-truth observation — SensorList count wording

SensorList raw query returns 6 total rows, but only 5 are FDA_PAPER_ALERT strategies:

```text
1 pre-existing unrelated strategy
5 FDA strategies
```

Therefore prose such as：

```text
SensorList persistence = 6 FDA strategies
```

would be inaccurate.

Correct wording：

```text
SensorList total rows = 6
FDA-created PAPER strategies = 5
```

This count is not itself a DoD threshold, so classification：

```yaml
classification: NON_BLOCKING_OBSERVATION
```

---

# 11. Acceptance edge status

| Edge | R6 external status |
|---|---|
| EvidenceManifest body/hash | PASS |
| Manifest exact-set 54/54 unique | PASS |
| Raw-body ↔ manifest hashes for four embedded receipts | PASS |
| Final XQ runtime identity 3.20.02-260811 | PASS as declared subject |
| DoD-13 UFO² effective-load | PASS |
| broker_write=0 receipt | PASS |
| one_active_writer in PAPER receipt | PASS claim supported |
| F01 current-build qualification | **FAIL — stale 3.18.02 receipt** |
| F06 fresh 10x | **EVIDENCE_GAP** |
| DoD-17 PAPER 10 fresh runs | **FAIL — raw denominator only supports <10 execution cycles** |
| DoD-33 checker 179 raw execution | **EVIDENCE_GAP — stdout truncated** |
| wrong_action/silent_wrong_action global current scope | NOT CLOSED because F01/PAPER/F06 fresh qualification not closed |
| DoD-36 external 36/36 | NOT ESTABLISHED |

---

# 12. Gate Calibration Failure defense

## Objective alignment

PASS。

本輪只驗 FDA local/PAPER desktop automation，不觸碰 live trading authorization。

## Risk proportionality

PASS。

沒有要求重建 XQ adapter、Cua、UFO²或 RP-002。

## False-positive defense

PASS。

本輪特別拒絕以下 proxy：

```text
56 SensorLog rows → 10 fresh runs
10 JSON run rows with same LastCompileTime → 10 fresh compiles
historical 3.18 receipt → current 3.20 qualification
partial checker stdout + manifest count → fully reviewed 179 raw checks
```

## Anti-overfitting

PASS。

FN03 Afx仍不升格為已 qualification invoke。

## Claim ceiling

保持：

```text
SQS_LIVE_TRADING = NOT_AUTHORIZED
PRODUCTION_AUTONOMY = NOT_CLAIMED
REMOTE_DEPLOYMENT = NOT_CLAIMED
```

---

# 13. Smallest Legal Repair

不重做產品。

只補 4 個 focused edges：

```text
A. CURRENT F01
   submit existing 260811 FN01/F01 receipt
   or rerun launch/locate only 10x

B. F06
   submit distinct per-run invocation timestamps
   or rerun compile only 10x

C. PAPER
   complete explicit 10 fresh runs per applicable PAPER action class
   with run IDs + readbacks + wrong/silent/broker=0

D. CHECKER
   submit full untruncated 179-check raw stdout/receipt
```

同步修：

```text
raw single-MD self-hash metadata
SensorList "6 total / 5 FDA" wording
```

不要：

```text
rebuild FDA
rerun RP-002
change Cua/UFO architecture
add third profile
add visual-alert gate
authorize live trading
```

---

# 14. Next Final Stop Conditions

下一輪只需確認：

```text
F01 current subject = XQ 3.20.02-260811
F01 10/10
wrong=0
silent=0

F06 10 distinct fresh compiles
CompileStatus=1 each run
wrong=0
silent=0

PAPER:
10 fresh runs / applicable action class
per-run readback
wrong=0
silent=0
broker_write=0
one writer

checker:
full 179 records or complete signed/raw receipt
179 passed
0 failed
0 errors
exit 0
VERIFY_ONLY
maker != checker

blocking contradiction = 0
blocking evidence gap = 0
```

才可簽：

```text
PASS_CHALLENGE
FDA_EXTERNAL_ACCEPTANCE = GRANTED
FDA_PROFILE_TEAM_ACTIVE = PASS
```

---

# 15. Final Stop

```text
FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_R6 = FAIL_CHALLENGE

FDA_BLUEPRINT = PASS
FDA_LOCAL_IMPLEMENTATION = SUBSTANTIAL_NOT_OVERTURNED

FDA_EXTERNAL_ACCEPTANCE = NOT_GRANTED
FDA_PROFILE_TEAM_ACTIVE = FAIL_CLOSED

BLOCKING CONFIRMED DEFECTS:
- EXT-FDA-RR6-001 stale F01 subject (3.18.02 vs 3.20.02-260811)
- EXT-FDA-RR6-002 PAPER denominator does not establish 10 fresh runs

BLOCKING EVIDENCE GAPS:
- EXT-FDA-RR6-003 F06 ten fresh compiles not established
- EXT-FDA-RR6-004 checker stdout truncated

NON-BLOCKING:
- RR6-005 raw container self-hash mismatch
- SensorList wording: 6 total rows / 5 FDA rows

CONFIRMED_PRODUCT_ARCHITECTURE_DEFECT = 0
PRODUCT_REBUILD_REQUIRED = NO
BROAD_RERUN_REQUIRED = NO

NEXT = RESUME_SMALLEST_REPAIR
```

**END OF EXTERNAL FINAL FOCUSED REREVIEW R6**
