<!-- SKCV-TOPIC-ENTRY path=skill/references/external-single-md-mandatory-route.md offset=181 length=2546 sha256=975407d870df5443901ce90a4ff32cbc9b5a2bc6b5dce6a998c1b9c1ece8f682 -->
# External Single-MD Mandatory Route (Step 6C) — full recipe

外部驗收證據提交：**單一 evidence MD = FULLY EMBEDDED，不是 pointers**（2026-08-14 user-mandated）。

## Why (verified twice by external reviews)
- FAR R7/R8 rule: the external reviewer's environment CANNOT open MEDIA attachments
  or local paths — the message body / single MD is the ONLY readable channel.
- External r2 (EXT-FDA-RR2-001) failed exactly because the claimed final file was
  NOT the file the reviewer received, and the submitted MD was pointer-rich
  (referenced SensorLog paths / receipt filenames instead of embedding raw bodies).

## MANDATORY ROUTE

1. **One file, one identity:** single final MD filename + sha256 in its header;
   the exact bytes you claim MUST be the bytes submitted (attachment identity check).
2. **Embed full raw bodies, not names:** every blocking receipt's CONTENT inline
   (checker verdict + denominator + pass/fail; F01/F03/F06/F07/F09/F10/F11 receipts;
   UFO² effective-load; PAPER runtime SensorLog/SensorList raw extracts; DoD-36 rows;
   claim ceiling; artifact hash table). External reviewer never opens a path.
3. **Single-valued truth:** one current value per state (UFO² / PAPER / checker
   denominator / subject root / artifact counts) — no stale superseded prose
   (Track A normalization; label old counts SUPERSEDED_PRE_<PATCH>).
4. **Freeze order:** freeze HEAD → freeze receipts → freeze tests → fresh checker →
   SubjectManifest → EvidenceManifest → render final MD LAST → mirror byte-identical
   → readback receipt → submit exact bytes.
5. **Never append a ChangeSet after manifest regeneration.**

## Execution tooling
`pack_external_single_md.py` (in this skill's references/ or var/fda/) reads
EvidenceManifest + receipts + runtime DBs and emits ONE self-contained MD with all
raw bodies inlined. Run it automatically at the internal→external handoff boundary.

## Master payload steps (per acceptance contract)

1. Render ONE master evidence payload (sections A..L per the acceptance contract) to a
   temp file. Do NOT embed the file's own final SHA in its body (self-referential hash loop).
2. Run a deterministic read-only independent checker (fresh readback of every fact, never
   trusting maker output; keep it in gitignored `var/a2/`).
3. `cp` the exact same bytes to `HGK\evidence\review\`, `SQS\evidence\review\`,
   `Fabric\evidence\review\` (same filename). Compute SHA-256 at all three locations;
   require equality. Do not edit any copy after hashing.
<!-- SKCV-TOPIC-ENTRY path=skill/references/external-acceptance-single-md-closure.md offset=2912 length=5544 sha256=5af0c9dfd49aa60faca75a8b0ce7fa7bb624d6c02f18e07c6f116f102540c688 -->
# External acceptance: single-MD closure with embedded raw evidence (FAR EXT-FAR r1→r7, 2026-08-13)

Verified end-to-end on fabric-autonomous-research (FAR): three external review rounds
(r1 PARTIAL_CHALLENGE with EXT-FAR-001..010 → r4/r6 narrow evidence gaps → r7
PASS_CHALLENGE / FAR-R1 PASS). The reviewer's rules: `existing PASS = claim`;
`PASS_CHALLENGE = no blocking contradiction AND every required raw edge reviewed`;
`PRODUCT_REBUILD_REQUIRED=NO / BROAD_RERUN_REQUIRED=NO` → evidence-only smallest repair.

## 1. Delivery transport: single acceptance MD with FULL inline raw content

Clean-room reviewers may NOT be able to open MEDIA attachments (renders as `[Open](#)`)
or local paths (they check their own `/mnt/data`). The ONLY reliable transport is the
message content itself.

- Deliver ONE acceptance MD (`FAR_FINAL_ACCEPTANCE_EVIDENCE.md` style) that EMBEDS every
  load-bearing raw edge inline:
  - Q4/Q10 receipts: full JSON bodies (never summaries)
  - crosswalk: ALL rows (ID|predicate|locator) — "92/92 independently reviewed" is only
    legal when all 92 rows are in the message; samples got flagged as EVIDENCE_GAP
  - subject root: ALL (relpath|sha256) rows so the reviewer can recompute the merkle digest
  - evidence manifest: ALL entries; spine readback: all WO rows incl. result_json + all EVD rows
  - kanban snapshots: full text; test stdout + exit code: full text; closure receipts: full JSON ×N
- Excerpts / hash-only / sample tables → new EVIDENCE_GAP finding (EXT-FAR-R5-001 class).

## 2. Freeze chain when the acceptance MD embeds the manifest

- The evidence manifest MUST exclude the acceptance MD from its entries (else regen loop:
  MD embeds manifest rows; manifest hashes MD).
- Single-direction binding: acceptance MD embeds manifest rows + references manifest by
  path; manifest references the MD by path only.
- ANY receipt change (NBO fix, new receipt, doc add) → full chain:
  1. fix artifact → 2. regenerate manifest (current bytes; excludes self + acceptance MD)
  → 3. regenerate acceptance MD → 4. mirror ×4 (FAR root + HGK/Fabric/SQS evidence\review)
  → 5. SHA-256 equality → 6. register SUPERSEDING EVD (R2/R3/R4…; never rewrite old rows).

## 3. Negative side-effect receipt (EXT-FAR-R6-002 class)

Locator-only negative claims (`"spine readback + evidence (no broker adapter)"`) get flagged.
Provide a subject-bound receipt with ALL of:
- exact `subject_root_digest` binding (must NOT change the frozen subject — it's an
  acceptance artifact, excluded from the subject tree)
- `unauthorized_side_effects=0` + run denominator (WOs/tests/canaries) + deterministic
  check (`find -newermt <window-start> <product paths>` = empty; evidence manifest locators
  all under allowed roots)
- `sqs_financial_truth_mutation=0` + check (FT manifest mtime BEFORE window; 0 files
  modified in window; consumer-boundary only per capability matrix)
- `live_broker_write=0` + check (`find -iname '*broker*'` over repo excluding .git/.venv
  = empty; product code has no order-path refs)
- `checker_identity`, `run_denominator`, `raw_locator`, receipt SHA-256
- Register as EVD; embed full content in the acceptance MD.

## 4. Generator QA checklist (run BEFORE any delivery)

- **No `None` in output**: receipt fields are often NESTED (`lane_1_fresh_ao.delegation_id`,
  not top-level). Read via explicit nested paths; grep the generated MD for `None` in data
  blocks (prose mentions of the defect are fine).
- **Closure table rows actually present**: files are `CLOSURE-{fid}.json` (HYPHEN). A
  generator using `CLOSURE_{fid}` (underscore) silently produces an EMPTY table.
- **Guide/stats counts current**: "93-entry manifest" / "35 EVD rows" hardcoded in prose go
  stale after regen — derive from the loaded JSON at generation time.
- **Heading counts match table rows** (e.g. "12 native files" vs 14 rows).
- Gate scripts: use `bool(v)` truthiness, NOT `v is True` — identity comparison on int
  counts (92/95/102) returns False and falsely fails the gate.

## 5. Stale-hash root cause + repair

Observed: `FAR_FIRST_USE_INDEX.json` embedded skill-reference hash `7e403e67` while current
bytes = `a1088d40`. Root cause: the index was generated at 19:48 BEFORE the reference
received its §11/12 append at 19:50 — a dependent index captured a pre-append state.
- Rule: after ANY append/edit to a hashed file, regenerate every dependent index/manifest
  from current bytes; verify with a fresh hash readback.
- Repair: regenerate as a NEW superseding artifact (PCIV-F01 pattern); never rewrite the old
  frozen row; record the supersedes reason; propagate the subject digest chain
  (first-use subject digest 671327cf → c4590d94 with a supersedes record in the closure
  receipt — CLOSURE-EXT-FAR-009).

## 6. Verdict ladder

- PARTIAL_CHALLENGE + findings = resume smallest repair, NOT rebuild. Close each finding with
  `CLOSURE_<FINDING_ID>.json` (classification / status / smallest_repair / focused_retest /
  bound_into / verdict).
- Reviewer does their OWN recomputation (merkle, hashes, row counts, LF/CRLF normalization).
  Our job: make every edge independently recomputable from the single MD.
- PASS_CHALLENGE lands only when the declared denominator (e.g. 14-condition matrix) is all
  PASS with blocking=0; post-acceptance docs/NBO cleanups do NOT reopen FAR-R1, but they DO
  trigger the §2 freeze chain (manifest → MD → mirror → superseding EVD).
<!-- SKCV-TOPIC-ENTRY path=skill/references/external-submission-gates.md offset=8629 length=7083 sha256=8525b204cc789419123321b49a0f61dea65216f9eecce1a313754feb27d3c7b0 -->
# HGK External-Submission Gates (2026-08-14, external 5-defect FAR root-cause)

外部驗收反覆不過的 5 個根因與對應 gate。任何外部證據提交前**必須**遵守。

## 根因（外部認定，FAR 三源確認）

1. 沒有真正 atomic finalization —— reducer 渲染後仍手動修 placeholder/stale fields
2. 沒有 machine preflight —— RR6 時 3 個 checker 數字（98/185/194）並存仍提交
3. stale fields 手動帶到下一版 —— 5 個 self-hash 舊 MD 殘留；RR6-004 標題 179 body 98
4. manifest/checker/root 沒有一次性重生 —— manifest 每輪 +1 累加；checker 從未 clean regenerate
5. 過早把 finding 標 CLOSED —— RR6-005/RR8-A 標 CLOSED 但外部判 PARTIAL/NOT_CLOSED

## Gate 1 — MACHINE PREFLIGHT（提交前必跑）

```bash
python var/fda/hgk_evidence_preflight.py   # PASS = 可提交 / BLOCKED = 先修
```

5 項阻擋檢查：
- (a) 單一 current checker denominator：舊 checker receipts 的 **JSON body** 須含
  `status: HISTORICAL` + `superseded_by`（只改檔名不算；只認最新 FINAL_RR7 為 current）
- (b) 最新 single-evidence MD（LATEST FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_*）無
  `this_file_sha256` self-hash（舊 MD 殘留不算——current-series 掃描只看最新）
- (c) manifest 0 missing / 0 hash mismatch
- (d) 三向 subject binding：manifest.subject_root == checker.subject_root == MD 宣告 final_subject_root
  （比較用前 12 字元，勿用 full-vs-truncated 混合比較）
- (e) 每個 CLOSED finding 有 authority receipt 在 disk

## Gate 2 — ONE-TIME REGENERATION

- 每個 external repair round **從零重生成** manifest（不得 +1 累加）
- 舊 receipts → JSON body 標 HISTORICAL（不刪除，保留 audit trail）
- 舊 evidence MD 留在 evidence/ 但**排除於 current-series 掃描**
- 永不用手 edit manifest row「carry forward」stale value —— 一律從 disk bytes 重算

## Gate 3 — CLOSED AUTHORITY

finding 標 CLOSED 的條件：
- 有 machine-readable authority receipt 在 disk（receipt JSON 含 verdict）
- evidence MD 中引用該 receipt 的**確切路徑**
- 無 receipt 即 CLOSED = premature（外部 r6: RR6-005; r8: RR8-A 實例）

## Gate 4 — ATOMIC RESEAL（RR8-final 實證，2026-08-14）

外部指「manifest 仍有 stale duplicated metadata」時的最後閉合步驟（evidence-only，
**不得**重跑 F01/F06/UFO²/PAPER、不得加新 gate）。執行 `scripts/atomic_reseal.py`：
- artifact_count **由 len(artifacts[]) 自動 derive**（不再手動維護數字——「54 vs 實際不符」類 defect 的根因）
- checker_history：最新者 ONLY CURRENT，全部前代 HISTORICAL + `superseded_by` 最新
- 清除舊 round 的 version/schema 殘留（RR4 時代 `FINAL_RR4_...` 等）
- 每個 artifact sha 從 bundle bytes 重算 → 0 missing / 0 mismatch
- 單一 serialization（sort_keys）+ 單一 SHA

## Gate 5 — 內嵌 manifest body SHA 陷阱（RR8 實證）

把 EvidenceManifest **內嵌進單一證據 MD** 時：
- `json.dumps(man)` 重序列化後 bytes 與磁碟檔**不同** → 內嵌 body 的 SHA ≠ 磁碟檔 SHA
- **MD 內宣告的 sha 必須是「內嵌 body 的 sha」**（外部 reviewer re-hash 才能 MATCH），
  磁碟檔 sha 另以註記列出並說明差異原因（僅 JSON re-serialization）
- 檢查「manifest 有無內嵌」要比對 embedded-body sha，不是磁碟檔 sha（`man_sha in body` 恆 False 誤報）
- MD builder 用 **placeholder `.replace()`**（如 `__MANIFEST_BODY__`），不要用 f-string 內嵌
  大量 `{...}`（f-string 的 `{` 會與 JSON/manifest 內容衝突）

## Gate 6 — checker 記錄 ID 唯一性（T100 實證）

- checker 的 T100_NOSECRET 掃描若用 `f.name` 當 check ID，**同名檔在不同子目錄會 duplicate ID**
  （r7 抓出 194 records 但 192 unique）→ **ID 改用相對路徑**
  （`str(f.relative_to(FDA)).replace("\\","_").replace("/","_")`）
- 外部驗收要求：actual record count == declared total == unique IDs，duplicate=0

## 執行者

- preflight：`scripts/hgk_evidence_preflight.py`（skill 內建，RR6 時代驗證）
- atomic reseal：`scripts/atomic_reseal.py`（skill 內建，RR8-final 驗證）
- 驗證：提交前跑 preflight → 全 PASS 才 pack/upload；reseal 後跑 derive/count/unique invariants

## r10/r11 Fixed-Contract Lessons (2026-08-14, external acceptance GRANTED)

**Identity separation model (no-moving-goalpost):** `candidate_root != evaluator_sha256 !=
evidence_bundle_root` — three distinct layers. Never demand candidate root change because
evidence changed; never treat a different JSON serialization of the same manifest as a second
canonical identity (on-disk re-serialization = `NON_CANONICAL_RENDERING`).

**FINAL reseal — the 3 fields that kept failing external review (r10):**
1. **exact_set counters must be DERIVED** from `len(artifacts[])` — `manifest_row_count ==
   payload_file_count == artifact_count`. Hand-set numbers (54 vs actual 63) fail; derive, never type.
2. **Chronology:** `generated_at_utc` must be AFTER every bound evidence timestamp. Scan all
   bound receipts' generated_at, take the max, generate the manifest LAST. Stale timestamp =
   EXT-FDA-R10-002.
3. **Evaluator must be machine-readable structured field** — prose in a note is NOT enough:
   ```json
   "evaluator": {"artifact": "independent_checker.py", "sha256": "9009713...", "mode": "VERIFY_ONLY"}
   ```
   Must equal the checker receipt's `script_sha256` exactly.

**Full reseal preflight (12 checks, ALL PASS before submit):**
candidate_root=1 · current_checker=1 (history has 0 CURRENT; the one current lives in the
checker field) · serialization SINGLE_CANONICAL · artifact_count==len(artifacts) ·
unique paths==count · manifest_row_count==count · payload_file_count==count ·
checker total==raw==unique==passed · failed=0/errors=0/exit=0 · evaluator_sha match ·
generated_at > latest bound · 0 missing / 0 mismatch.

**After GRANTED (r11):** update README/AGENTS/TEAM/USER_GUIDE in one commit with acceptance
state + claim ceiling (SQS_LIVE_TRADING still NOT_AUTHORIZED); run docs internal acceptance
check (27/27 pattern) before closing.

## FDA tool-path drift (2026-08-14, parallel-session rename)

Docs/skills may cite a tool at `var/fda/<NAME>.py` that a parallel session renamed (real case:
`FDA_PREFLIGHT_GUARD.py` → `fda_script_guard.py`). Before trusting a documented path:
- `find C:\Projects\Agent_Workspace -name "<NAME>.py"` to locate the actual file
- canonical copies live in skill `references/` / `scripts/` (stable across session churn)
- if a rename happened, prefer the skill-copy path over the doc-cited var/fda path, and note
  the drift in the doc gap-audit (run `docs_acceptance_check.py` pattern: file existence +
  knowledge-placement + discoverability in one pass). Re-runnable probe:
  `scripts/docs_gap_audit.py <project_root>` (themes A/B/C + tool-path + discoverability).
<!-- SKCV-TOPIC-ENTRY path=skill/references/external-challenge-evidence-closure-far.md offset=15900 length=5363 sha256=9412dfe386962e8e71280dbc129e16dfe89a93cb6c91e93c90390ffe1a157505 -->
# External-challenge evidence closure round (FAR EXT-FAR-001..010, verified 2026-08-13)

Extends `external-evidence-closure.md` (R1–R6) with the full EVIDENCE_ONLY closure
round as practiced on the FAR external PARTIAL_CHALLENGE. An external reviewer returns
findings classified EVIDENCE_GAP / CONFIRMED_DEFECT with
`RESUME_SMALLEST_REPAIR / EVIDENCE_ONLY_CLOSURE`; the maker must rebind + repackage raw
evidence, never rebuild product. Verified: FAR review findings EXT-FAR-001..010 all
closed in one round; focused re-review packet materialized as a single zip.

## The 8 closure workstreams (what the reviewer actually demands)

1. **Exact subject root** — `FAR_SUBJECT_ROOT_MANIFEST.json`: tree of
   `(relative_path + file_sha256)` over the implementation surface ONLY (exclude
   evidence-bundle, manifests, MDs, AO/closure receipts — those live under the
   evidence root); `subject_root_digest` = sha256 over sorted payload. The fresh AO
   lane must be able to RECOMPUTE this digest independently.
2. **Evidence manifest root** — `FAR_EVIDENCE_MANIFEST.json`: every raw entry with
   file_sha256 + role; **excludes itself** (pre-self-row rule) or its hash changes on
   every regen.
3. **Raw review bundle** — `evidence-bundle/`: raw-tests (see stderr trap below),
   raw-spine (fresh sqlite readback: WOs/REQs/TS/EVT/EVD/result_json), raw-kanban
   (final snapshots per board), raw-receipts (copies), raw-canary (run artifacts).
4. **Closure receipt per finding** — `CLOSURE-<FINDING_ID>.json` with
   classification / status CLOSED / smallest_repair / focused_retest predicates /
   bound_into / verdict. **Filenames use HYPHEN** (`CLOSURE-EXT-FAR-001.json`) —
   an underscore in the generator silently produces an empty closure table.
5. **Fresh AO for Q10** — blueprint requires fresh AO + blockers=0, NOT swarm
   agreement. Lane must be subject-bound (recompute merkle digest), maker-separated,
   no-write; Swarm/challenger evidence is input, never the final receipt.
6. **Real-invocation receipt (Q4-class)** — execute the pinned method workflow on a
   REAL local corpus (network DENY per WorkOrder), record method identity
   (commit + skill sha), input, execution trace, output digest; state
   `no_meta_apply_authority_import: true` and `reviewer_not_ao: true`.
7. **Regression crosswalk** — map every T0xxx predicate → exact evidence locator
   (92 rows for FAR); blocking contradiction must be 0.
8. **Post-freeze separate ChangeSets** — a later dogfood/self-upgrade round
   (e.g. FAR_FIRST_USE) is a SEPARATE subject with its own manifest digest; never
   absorb it into the older frozen core subject without explicit rebind.

## Evidence-MD generator hygiene (the three defects the reviewer caught)

1. **`None` in the generated MD** — reading NESTED receipt fields with top-level
   `.get()` (e.g. `ao.get("delegation_id")` when the id lives under
   `ao["lane_1_fresh_ao"]["delegation_id"]`) emits the literal string `None` into
   the evidence MD. **Always grep the generated MD for `None` before mirroring.**
   Materialize the full post-repair chain (lane1 FAIL → finding → repair → lane2
   PASS → final blockers=0), never a bare summary.
2. **Empty table from filename mismatch** — generator wrote
   `f"CLOSURE_{fid}.json"` (underscore) while files were `CLOSURE-{fid}.json`
   (hyphen) → 0-row closure table with no error. **Verify table row count ==
   expected denominator** after generation (`grep -c '^| EXT-FAR-'`).
3. **0-byte stdout evidence file** — `unittest` writes its output to STDERR;
   `subprocess.run(capture_output=True)` then writing only `r.stdout` produces an
   empty stdout evidence file (AO-FINDING-FAR-002). Capture merged output:
   `python -m unittest discover -s tests -t . > stdout.txt 2>&1` (+ append EXIT).
   A fresh AO lane WILL flag the 0-byte file; the fix is regenerating with merged
   capture, then a focused retest lane.

## Freeze order (drift-proof, as verified)

```text
1. complete ALL mutations (closures, receipts, gates receipt regen)
2. regenerate evidence manifest LAST among mutable artifacts (any receipt regen
   desyncs hashes embedded earlier)
3. register superseding EVD rows for regenerated receipts (EVD-*-R2 pattern)
4. generate the evidence MD LAST (read hashes FROM manifests — no transcription)
5. mirror byte-identical to HGK/Fabric/SQS evidence\review, hash all copies, require equality
6. no edits after hashing; MD never embeds its own hash (single-direction binding:
   MD references mirror-receipt by path; receipt carries MD hash)
```

## Package the focused re-review packet

A single zip (`FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip`) containing bundle + manifests +
closure receipts + evidence MD + mirror receipt, with a package receipt carrying the
zip sha256 (single-direction). The external reviewer's focused re-review then checks
~14 conditions (subject root, manifest root, bundle hashes, MD consistency, Q4/Q10
receipts, crosswalk, EVD denominator, mirror readback, zero blockers).

## Kanban/execution surfaces still apply

Closure round still rides a kanban board (`far-external-closure`) + claim/complete;
remember `unset HERMES_DELEGATED_CHILD_CONTEXT` after every delegate_task batch
(re-set on each batch; blocks kanban CLI).
<!-- SKCV-TOPIC-ENTRY path=skill/references/external-challenge-review-closure.md offset=21446 length=10097 sha256=85fc306679893ece6233bd26b1157b2735fc97efd6729571e23f6d9cca13a7aa -->
# External-challenge closure round (EXT-FDA-001..008 pattern, verified 2026-08-13)

After an external `PARTIAL_CHALLENGE` review returns `EVIDENCE_GAP` findings on the
submitted evidence MD, the resume is a **smallest-repair evidence closure**, not a
rebuild. This is the FDA round's recipe (same family as the R1-EVIDENCE_ONLY round
in `external-evidence-closure.md`, but with the subject-root + raw-bundle + DoD-matrix
extensions the FDA external reviewer demanded).

## What external reviewers actually fail you on

| Finding class | What they need |
|---|---|
| EXT-FDA-001 "no exact frozen subject root" | ONE `FINAL_GIT_HEAD` (or package digest) the whole evidence set binds to, recomputable by `git checkout <head>` |
| EXT-FDA-002 "51 raw artifacts not submitted" | RAW bytes of every artifact (a review bundle), not a hash pointer table |
| EXT-FDA-003 "checker denominator conflict" | ONE current denominator (e.g. 146), embedded fresh-run receipt, no stale value |
| EXT-FDA-004 "DoD pass-list self-contradiction" | Full 36-row machine matrix, no omitted IDs, PASS/PARTIAL/BLOCKED mutually consistent |
| EXT-FDA-005/006 "runtime gate not closed" | Either close it (see UFO2 below) or keep it HONESTLY BLOCKED/PARTIAL with the authority-gate owner named |

## Subject root via git commits (EXT-FDA-001)

Freeze identity by committing, not by hashing files in a dirty tree:

```bash
cd Fabric
git add fabric-desktop-automation/ profiles/fabric-desktop-cua/ profiles/fabric-desktop-ufo2/ \
        rp002/RP002_PROFILE_TEAM_MANIFEST.yaml rp002/RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml
git commit -m "FDA (WO-...): ..."
git rev-parse HEAD        # -> subject root; external verifier can git checkout this
```

Two-commit model (avoids the self-referential MD-embeds-own-HEAD loop):
- commit 1: all artifacts + evidence MD
- commit 2: EvidenceManifest + raw review bundle (manifest lives in the bundle dir)
- final HEAD = subject root; the evidence MD cites the artifact commit, not the
  commit that contains the MD itself. If the MD's text must mention the final HEAD,
  accept that the MD's own hash is a separate evidence artifact (never embed the MD's
  own hash in its body — single-direction binding).

## Raw review bundle + EvidenceManifest (EXT-FDA-002)

External reviewers cannot re-verify hash pointers without the bytes. Build:

```
Fabric/evidence/review/FDA_RAW_REVIEW_BUNDLE/
  FDA_EVIDENCE_MANIFEST.json     # generated LAST
  BUNDLE_INDEX.md
  <mirror of every artifact path>  # byte copies (cp), not symlinks
```

Manifest binds, per artifact: `path`, `sha256`, `size`; plus `subject_root.git_head`,
a fresh checker run (`verdict/checks/failed/run_at`), a fresh tests run, the DoD-36
matrix, and the claim ceiling. Manifest `sha256` is the bundle's own identity.

Generator pitfalls (all hit live):
- Path prefixes: `RAW_PATHS` must be repo-relative (`Fabric/fabric-desktop-automation/...`,
  `HG-KSEOS/var/fda/...`) against the workspace ROOT — omitting `Fabric/` reports all
  artifacts MISSING.
- `python -m unittest discover` writes "Ran N tests" to **stderr**, not stdout —
  combine `stdout + "\n" + stderr` before regex.
- Checker counts GROW as receipts are added (each new receipt file adds no-secret
  checks) — the denominator is a fresh-run snapshot, never a stale number from an
  earlier freeze. Regenerate the manifest at the END.

## Checker denominator (EXT-FDA-003)

Symptom: evidence MD said `checks: 126`, fresh run says `144`/`146`. Root cause: the
MD was generated at an earlier freeze and the checker grew. Fix: single current value
everywhere (MD §4 + manifest + verifier checklist), and note the old value was stale.
Never "pick" a denominator — run the checker once more and record that exact output.

## DoD-36 machine matrix (EXT-FDA-004)

Symptom: evidence MD claimed "DoD items 1–16 verified PASS" while also listing
UFO2 effective-load BLOCKED (DoD-13 ∈ 1..16) — a confirmed report-semantics defect.
Fix: materialize the full 36-row table with machine predicates, no omitted IDs
(21/22/25 were silently dropped in an earlier version), and explicit
PASS/PARTIAL/BLOCKED per row. Summary line `PASS=N PARTIAL=M BLOCKED=K` must equal
the row count. Keep DoD-17/35 PARTIAL honest with the authority-gate owner named.

## UFO² effective-load does NOT need an external API key (EXT-FDA-005 correction)

The earlier `BLOCKED_HITL (LLM API key = credential)` claim was OVER-CONSERVATIVE.
UFO² v3.0.8 supports three no-key paths:
- **Ollama local**: `API_TYPE: "ollama"`, `API_BASE: http://localhost:11434`,
  `API_KEY: "ollama"` (placeholder, not used)
- **Custom model**: subclass `ufo.llm.base.BaseService` (see `ufo/llm/placeholder.py`)
- **PlaceHolderService**: no-LLM module/config/UIA-backend verification mode

Effective-load probe = import package + import `ufo.llm.*` + instantiate
`PlaceHolderService` + import `ufo.automator.ui_control` + parse `config/ufo/system.yaml`
+ import `app_agent`/`host_agent` → 7/7 PASS.

### opencode-go as UFO² LLM backend (user-authorized, verified live)

- Hermes credential: `hermes_cli.config.get_env_value_prefer_dotenv("OPENCODE_GO_API_KEY")`
  (reads `AppData\Local\hermes\.env`); key never written to any file/evidence.
- **URLLIB IS BLOCKED**: `urllib.request` to `https://opencode.ai/zen/go/...` → `HTTP 403
  error code: 1010` (Cloudflare browser-signature block). This is NOT a bad key —
  the OpenAI SDK works: `OpenAI(api_key=key, base_url="https://opencode.ai/zen/go/v1")`,
  `chat.completions.create(model="deepseek-v4-flash", ...)` → 200, finish=stop.
- `max_tokens` too small (≤16) on deepseek-v4-flash returns `finish=length` + empty
  content — use ≥256 for canaries.
- Record in the receipt: base_url + model + `key_storage: Hermes dotenv; never written`.

### UFO² dependency install (venv, verified)

- `env -u PYTHONPATH` before any venv python (global hermes path shadows site-packages).
- `pip install --target .venv\Lib\site-packages <pkg>` — plain `pip install` under the
  shadowed env silently installs to the wrong place (`six` import failed until --target).
- pywinauto needs `pywin32_postinstall.py -install` + DLLs:
  `cp .venv\Lib\site-packages\pywin32_system32\pythoncom312.dll pywintypes312.dll .venv` (root).
- **langchain conflict**: UFO² v3.0.8 requires `langchain.docstore.document` (removed in
  langchain ≥0.3) → install `langchain==0.2.17 + langchain-community==0.2.19 +
  langchain-core==0.2.43`; uninstall the 0.3/1.x residue first (mixed dist-info dirs
  shadow the 0.2 package).

## XQ strategy radar PAPER runtime (EXT-FDA-006 — CLOSED 2026-08-14)

- Trial-mode radar: menu 策略(D) → 策略雷達(開放體驗)(L) → the 試用說明 dialog is a
  Win32 dialog invisible to UIA — dismiss with `press_key return` ("我知道了").
- Trial radar's strategy library is EMPTY (folder categories exist, no leaf nodes;
  search "KD" returns nothing). System strategies are read-only in trial
  (`請複製成自訂策略才能修改內容`). PAPER start/stop therefore cannot run on the
  trial subject — record `QUALIFIED_SURFACE / RUNTIME_START_STOP_BLOCKED_TRIAL_LIBRARY_EMPTY`
  and name the unblock owner (SQS/XQ PAPER fixture authority) per the external
  finding's `earliest_owner`. Do NOT fake a run; 0 wrong action / 0 broker write stays.
- **CLOSURE (verified 2026-08-14, NOT trial-era speculation):** subscribing the
  **盤中量化交易模組** (個人版策略雷達所在的加值模組) makes custom strategies
  **persist across XQ restart** and removes the 開放體驗警示 notice. DoD-17 then
  closes via the **SensorLog truth layer**, NOT the radar UI (XTP grid is
  uia-invisible): `DAQXQLITE_SHW097_SensorLog.sqlite` Table_YYYYMMDD records the
  full execution state machine per strategy (XSSensorState 2→3→1, ExecState 1→8,
  SymbolID, TriggerTime) — 56 records across 3 FDA strategies. Full recipe:
  `references/xq-radar-paper-runtime.md` §3b.

## External RE-REVIEW single-file packaging (r2 pattern, verified 2026-08-14)

When the reviewer asks "確認 previous findings 是否都已解決" (or the user asks for
ONE consolidated file for a second review), produce a **single self-contained
re-review evidence MD** — the answer to every prior finding + the full current
evidence, in one file, with NO local-path dependency (reviewer can't open MEDIA):

1. **Per-finding closure block** — one section per EXT-FDA-XXX: review requirement
   (quote) → closure evidence (concrete: commit hash, counts, receipt content) →
   external re-verify instruction (exact command the reviewer runs). Mark each
   CLOSED; keep genuinely-open items in a 誠實保留 section (e.g. 盤中觸發視覺驗證
   time-gated) — never promote FAIL_CLOSED yourself.
2. **Self-contained contract** — include the DoD matrix, checker denominator,
   raw-bundle manifest sha256, XQ fingerprint, and a 10-row external-verifier
   checklist (git rev-parse / sha256sum / checker rerun / SensorLog read) all inline.
3. **Finalize-sha loop** (the sha must be IN the file AND cover the file):
   write MD with placeholder → sha256 the file → patch placeholder (header yaml +
   body) with the real sha → re-hash → that final sha is the file's identity.
4. **Mirror byte-identical ×3** (Fabric/HGK/SQS evidence\review) + update
   EvidenceManifest subject_root to the CURRENT HEAD (not the last artifact commit)
   and append the re-review MD to the manifest artifacts. Verify equality with a
   3-way hash check (evidence MD itself stays 4-way).
5. Commit: subject root moves forward (e.g. cf24b65 → 75499ba) — the re-review MD
   is a NEW artifact; the frozen subject for the reviewer is the new HEAD.

Trap: keep the re-review MD's claim ceiling identical to the evidence MD's
(FDA_PROFILE_TEAM_ACTIVE stays FAIL_CLOSED until the EXTERNAL verdict — the file
answers the review, it does not self-accept).

