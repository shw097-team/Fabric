
<!-- BEGIN SLICE 1 src[3531,11574) sha256=1f94f3d6d6958009258d02b08033906ea5fd3889a37d9e16566838b3488fd89f -->
## Routing map（拆分 2026-08-15 起生效）

| 操作類型 / 情境 | 觸發條件 | 載入 |
|---|---|---|
| Hermes 模型供應跨 provider fallback 設定/排障 | 設定或修復 `fallback_providers`、手動換 provider、額度/5h 窗逃生、OpenRouter 免費模型選用 | references/hermes-provider-routing-failover.md |
| FDA 桌面自動化操作細節 | 任何 XQ/XS/cua/ufo2 操作執行步驟 | references/step-9-fda-cua-operations.md |
| FDA 執行前閘 | 任何 FDA 操作開始前 | SKILL.md §Step 9-0 inline（fda_preflight.py / fda_script_guard.py） |
| FDA 授權判定 | 自動調用 FDA 前自問授權來源 1/2/3 | SKILL.md §Step 9-0a inline（fda_guard_mint.py / FDA_ROUTE_REGISTRY.json / fda_guard_hook.py） |
| 異常/錯誤排查 | 任何失敗、守則違反疑慮、奇怪行為 | references/step-pitfalls-checklist.md |
| EVIDENCE_ONLY 閉環 | external PARTIAL_CHALLENGE / EVIDENCE_GAP | references/step-evidence-only-contract-a.md |
| 獨立驗收/挑戰 | VERIFY_ONLY / challenge lane / AO lane | references/step-verify-only-lane.md |
| 證據閉環 pipeline | freeze-order 證據生成 | references/step-6d-evidence-closure-pipeline.md |
| P0-TOOL registry 啟用 | 外部工具受治理啟用 | references/step-10-external-provider-tool-enablement.md |
| 全部支援檔說明 | 找某 references 檔的描述 | references/support-files-index.md |
| 既有 references 連結 | When to use / 各 step 內嵌 | 保留原文指標不變 |
| SQS-THC 知識庫唯讀研究 | RBWI/Spartoi/DOC 文檔的方法/ICT 內容定位與 §/ANCHOR 解析慣例 | references/sqs-thc-knowledge-base-research.md |
| FSDT-Stack DOC 系列研究 | FSDT-Stack DOC-29/27/28 + TW-ICT v3.0 DOC-05/14 的方法流程/當沖技術定位與真實檔案根 | references/fsdt-stack-doc-series-research.md |
| 台股當日沖銷(T0) 主軸研究 | 四家族(T0 axis/時間窗/SessionCandidatePool-S1/SetupQualification/盤中JobCards/DOC-05權威鏈/MTH·CMP當沖技)整合結論與 L 行號 | references/daytrading-t0-axis-authoritative-chain.md |
| 方法定案閉環（方案 D） | 走完候選方法草案→回測→自修補→定案 / 策略級回測定案 | references/method-finalization-contract.md |
| 策略回測正確性 + 方法定案誠實閉環 | 任何 strategy backtest：時序 split（非 per-symbol row slice）/ per-(symbol,date) gap 鍵 / cost reconciliation / 負 PnL 處置→Slow-Loop supersede→Paper-Shadow 前提。含 CODE_X_HOME export 與 CRLF 修復陷阱 | references/strategy-backtest-correctness-and-method-finalization.md |
| A判決×ExperimentSpec 合約獨立驗證 | 獨立驗證 NEGATIVE_RESULT(REJECTED/finding/禁overfit-rescue) + EXPERIMENT_SPEC(candidate/anti-overfit/cost_model/acceptance/nonclaim)，輸出 items[]/blocking[] JSON（唯讀禁寫） | references/a-verdict-experimentspec-contract-verification.md |
| HGK-KSEOS SSOT 治理接地 / upstream-vs-HGK | 提案、defect、修補要 ground 在 `知識庫/HG-KSEOS_SSOT`（P0-CIP-PACK / RBWI FINAL_r2 / 藍圖），判定「修復屬上游 provider 或 HGK 本體」，帶 claim-ceiling 語法 | references/hgk-ssot-authority-determination.md |
| 大型語料 source-freeze / 分母證明 / digest 對帳 | 訂單要求「full physical read / no sampling」+ deterministic inventory digest + current-vs-superseded 解析 + 決策分母（如 34/34 package bodies）；或凍結的 author-side digest 與現況對不上需判 drift | references/corpus-freeze-and-digest-reconciliation.md |
| 自證式探針撰寫 / 量測完整性 | 你要交出會被獨立 lane 重跑並試圖否證的 gate 探針與收據；或探針回 PASS 但可能是空洞/N-A 撐起來的；或獨立驗收抓到缺陷後要寫 corrective record / readback | references/self-verifying-probe-authoring.md |
| 外部驗收 bundle 打包 / 重封存 | 要把 frozen evidence 變成可上傳的 portable bundle + 獨立雜湊驗證；或獨立 lane 回報 manifest-hash stale、封存後新增檔案、root 檔列舉不全、宣告的 SHA 與現況不符；或 remote 讀回 hash 全對但 item 內部 subject 指向舊主體；或本機 hash 與 remote blob 不符（CRLF/LF） | references/external-review-evidence-packaging.md |
| GitHub acceptance mirror 建立 / 發佈 | 訂單授權建立或發佈 GitHub acceptance mirror（org/repo bootstrap、candidate/evidence publication）；或 `gh` CLI 缺席需以 REST 直驅；或 PAT 對 org 端點回 403 | references/github-acceptance-bridge.md |
| 治理順序 / authoritative binding 證明 | 閘門要求證明「admission/binding 先於 mutation」；或證據被拒因只有 wall-clock 時序；或 receipt 用慣例字串冒充 binding；或 evidence pack 需區分 direct vs transitive subject linkage；或 delegation window 零時長等退化值；或需判定「就地改檔 vs 整鏈重跑」；或獨立 lane 分母與你不一致 | references/governance-ordering-and-binding-proof.md |
| 驗收主體身分裁定 / 交付完整性 | 兩份同名治理產物 hash 衝突需裁「何者為現行」；或外部裁「權威檔案未交付」；或最終 rev 相對已驗 rev 有 delta 需揭露；或交付前要掃 null/placeholder | references/external-review-evidence-packaging.md §9 |
| 共享核心缺一個 primitive / engineering-base ChangeSet | 控制平面無法用 typed API 產出所需狀態（closure 卡住）；或獲授權要補一個最小 primitive；或 guard 被 replay/可選參數繞過；或 with/without 回歸數要交三個狀態；或 "已開 TT" 其實只在文件裡 | references/shared-core-primitive-changeset.md |


## RP-002 v2.0 status (2026-08-13)

Stage-1 (FABRIC-FOUNDATION) and Stage-2 (HGK) are EXTERNALLY ACCEPTED
(seal 12da14ac, handoff 93a7da26, external bundle 104d4cf2, PASS_CHALLENGE/GRANTED).
Stage-3 (RP002-STAGE-SQS: SQP1→S1→E1→E2→E3→R1) is LOCALLY COMPLETE:
child reducer = STAGE3_SQS_PASS_ELIGIBLE_FOR_MASTER_R1_REDUCTION, Master r2 final
reducer = RP002_LOCAL_ACCEPTANCE_PASS, single external review MD =
SQS-THC\evidence\rp002\stage3\RP002_R1_EVIDENCE_FOR_EXTERNAL_REVIEW.md
(mirrored byte-identical to Fabric/HGK evidence\review). Stage-3 SQP1 materialized
exactly 3 persistent SQS profiles (sqs-orchestrator / sqs-data-analysis / sqs-risk)
under SQS-THC\agents\profiles\ + TW-ICT Financial Runtime Pack at
SQS-THC\SQS\TWICT_RUNTIME_PACK_MANIFEST.yaml.

POST-CLOSURE ROUNDS (all 2026-08-13, same day as Stage-3):
- Post-closure integrated verification → PARTIAL, finding PCIV-F01 (FINAL_PACKAGE_MANIFEST
  internal E2-card digest stale fe824e17 vs d4f93610). Evidence MD ec3af640…
- Fabric autonomous self-evolution round closed PCIV-F01 via superseding manifests
  (999983fd…/b89edb2f…; accepted 68867e08/8d8d7f42 immutable). Evidence 3e6b0b72…
- External acceptance (R1 report) returned PARTIAL with EXT-F01..F07 evidence-closure
  findings → EVIDENCE_ONLY closure round closed all 7. Closure MD b50a11b2…
- SQS docs upgrade (README 50b54834…, User Guide r5 292ae148…, AGENTS.md new c1ef8b70…).
  Evidence 9e06939f…; CODEX-MOJIBAKE-001 + AO_PREDICATE_CORRECTION-001 recorded.
Terminal: STOP_FOR_EXTERNAL_FINAL_META_REVIEW — do NOT self-issue external meta
acceptance, production, live-trading, or remote-deployment claims. External final
meta acceptance remains PENDING_FOCUSED_REVIEW. Resume token:
RESUME:RP002_FABRIC_AUTONOMOUS_SELF_EVOLUTION_EXTERNAL_EVIDENCE_CLOSURE_ONLY.

CURRENT ROUND (2026-08-13, WO-RP2-DAILY-001, in-flight at last session end): user
decision UD-DAILY-OHLCV-2026-08-13-001 redefined the daily layer spec (5y all-eligible →
3~4y, 2023-01-03→2026-08-13, 263 TWSE/TPEx stocks); REQ-DAILY-001 FROZEN (EVT-2d94adb9),
board `rp002-daily-ohlcv` D0-D6. Acquisition: TWSE official STOCK_DAY primary + Yahoo
`.TWO` documented fallback (TPEx official endpoints 404/HTML — defect
TPEX_OFFICIAL_API_UNREACHABLE); pipeline + checker + endpoint knowledge:
`references/taiwan-daily-ohlcv-acquisition.md`.


<!-- END SLICE 1 -->

<!-- BEGIN SLICE 3 src[22333,97867) sha256=78f131ea9ba674df3ec2264f7929b2c1fb46526df2c0e2b2cef1395501b1fae2 -->
12. **Construction-wave execution law (verified 2026-10-02, SWOF-CONSTRUCTION-002 W0).** Four rules,
   each of which cost a real defect when ignored:
   (a) **FREEZE-001 — never mutate the subject while an independent checker is reading it.**
   Once a head, branch tip or bundle is handed to a VERIFY_ONLY lane, the target is FROZEN. A repair
   discovered during verification must WAIT for the verdict, then produce a NEW head and a NEW
   verification run. Editing the candidate mid-audit destroys the one-to-one attestation and a
   correct checker will return PARTIAL on that ground ALONE even when every substantive check
   passed. (Observed: the maker applied a citation fix ~1 min before the auditor read the tip; 17
   files / 0 write-set violations / all locator claims MATCH, yet the attestation was void.)
   Corollary 1: when a fix is queued but the head is under review, record it as QUEUED_NOT_APPLIED in
   an out-of-target receipt rather than applying it.
   Corollary 2: a verdict describes ONE subject. Once the head/branch tip moves, label every prior lane's
   verdict `SUPERSEDED` with the head it actually read and EXCLUDE it from the acceptance count — never
   carry a stale PASS forward as if it attested the new head, and never let a superseded PARTIAL
   linger as if it were current either.
   (b) **Write-set containment is enforced, not aspirational.** A repo-mutating WorkOrder may write
   ONLY inside its own admitted `proposed_bounded_write_set`. Before dispatch, print every planned
   WorkOrder's write-set; after writing, re-check every on-disk path against it (glob + prefix
   match) and record `containment_ok`. Real case: a greenfield bootstrap wrote `src/` and `tools/`
   that actually belonged to W1+ — a genuine governance violation. Correct response: delete the
   out-of-scope files and record the defect in the receipt, NOT widen the write-set. If a needed
   path is not granted, that is a typed blocker or packet recompilation, never self-service widening.
   Also note WorkOrders legitimately partition by subsystem (`src/fabric/`, `src/knowledge/`, ...),
   so "the repo skeleton needs src/" is not an entitlement.
   (c) **Never swallow a measurement error behind a bare `except OSError: pass`.** That is exactly how
   an aggregate PASS becomes satisfiable by a silently skipped item (skill rule 11). Assert per-item
   equality and let failures surface.
   (d) **Windows >MAX_PATH (260) silently corrupts corpus walks.** A file whose full path exceeds 260
   chars is invisible to plain Win32 access: `os.path.exists` -> False, and `pathlib.rglob()` /
   `is_file()` DROP it (observed 723 vs `os.walk` 724 on the same tree) while `os.walk` still lists
   it. It presents as a phantom "source drift" whose missing-byte total EXACTLY equals the dropped
   file's size — that exactness (file count short by 1 AND unexplained delta equal to one file) is
   the tell that the EXTRACTOR, not the corpus, is wrong. Fix: walk with `os.walk`, and stat/read via
   the `\\?\` prefix on a NORMALIZED BACKSLASH path (a stray forward slash makes the prefix fail
   with errno 22 / "Invalid argument"). Always suspect the extractor before declaring source drift;
   a false drift claim needlessly triggers re-freeze + invalidation of otherwise-valid cones.
   (e) **Test discovery is a denominator: run EVERY root and sum the counts.** A suite split across roots
   (`tests/` plus a co-located `src/<subsystem>/tests/`) is NOT discovered by one `discover -s tests -t .`
   run — when `src/` is not an importable package root the new subsystem's tests are skipped SILENTLY, so a
   receipt printing "13 tests OK" while 19 just-written tests never executed is a vacuous PASS (skill rule
   run each root explicitly, sum the counts, and assert the expected total; the tell that it bit you is
      that the count did NOT move after you added a module's tests. When a harness PARSES those runs
      programmatically, read the COMBINED stdout+stderr stream and assert the denominator is non-zero:
      `unittest` writes "Ran N tests" and OK/FAILED to STDERR, so a harness parsing only stdout reports
      `all_rc_zero: true` while `ran: 0` for every root — an all-green aggregate composed entirely of
      the parser's own blind spot.
   (f) **Assert the PERMANENT invariant, never the wave-scoped state — and repair a stale test under the
   OWNING WorkOrder's authority.** A wave's exit test legitimately encodes that wave's condition (e.g. "this
   wave introduced no `src/`"), which a later wave falsifies. When such an assertion blocks the next wave,
   re-express it as the invariant that survives (the specific forbidden path stays absent; the directory may
   contain only admitted later-wave packages). If that test file sits in a DIFFERENT WorkOrder's admitted
   write-set, the repair is a NAMED corrective attributed to the owning WorkOrder — never a silent edit
   folded into the current one. Two sibling defects this class also produced: a required-field check that
   CONSTRUCTS before validating raises a generic `TypeError` instead of the contract's specified error code
   (validate the raw mapping first), and a "subject key" content digest that includes mutable binding state
   changes the object's identity the moment it is bound (digest immutable semantic content only).
   (g) **A successful WRITE is not a successful FIX — re-run before the receipt says FIXED/ADDED.**
   After applying a repair, execute the thing that is supposed to have changed and confirm the effect, then
   write the receipt. Writing the file and asserting the defect is closed in the same breath is how a receipt
   ends up carrying an unsupported claim: a regression test was appended at file end and landed INSIDE the
   `if __name__ == "__main__": unittest.main()` block, so it was never collected — the receipt claimed it was
   'ADDED' while no test runner would ever see it. The tell is the same as (e): the collected count did not
   move. So when adding a test to an existing file, insert it INSIDE the test class (never append past the
   `__main__` guard) and treat 'the count went up by exactly one' as the acceptance proof. More generally: any
   receipt field asserting a state change must be re-derived from the artifact AFTER the change, not from the
   intent that produced it.
   (h) **Reconstructing a missing packet is allowed; disguising it is not.** If a repo mutation ran before its
   PD04 packet existed, materialize the packet afterwards but self-label it `RECONSTRUCTED` with the reason, and
   bind it to a hash the checker can recompute (e.g. the source RBWI's own sha256) so an independent lane can
   distinguish an honest reconstruction from a fabricated one. Never back-date a packet as if it had existed
   before the mutation.
   (i) **A documented precondition with no enforcing gate is NOT implemented — and a failing negative test may be
   the only thing that noticed.** When a source contract states a precondition ("disposition X requires all earlier
   dispositions to fail materially", "the subject-key digest must exclude mutable binding state"), restating it in a
   docstring or comment is not enforcement: there must be an explicit gate that FAILS CLOSED when it is violated.
   Real case: the admission ladder stated the BUILD_NEW_EXCEPTION precondition, but nothing raised — and the
   helper's ordinary behavior (return the strongest surviving disposition) made the law LOOK satisfied. The
   negative test was the only signal, and it signalled by asserting an exception from a function that correctly
   RETURNS, i.e. that test was wrong. The trap: "the test is wrong, so fix the test" turns the suite green while
   leaving the invariant unenforced. So when a negative test fails, decide explicitly which it is — WRONG TEST
   (the assertion is invalid) or UNENFORCED LAW (the contract has no gate) — and if it is the latter, add the gate
   FIRST, then correct the test. A green suite is never evidence that a documented invariant actually holds.
 (j) **Evidence SUBJECT IDENTITY is a separate check from hash integrity.** All SHA-256s matching proves
 transport, not meaning: an artifact can hash perfectly while its INTERNAL subject field names a
 superseded candidate, so a pack can carry a stale subject under a fresh manifest and pass every
 hash check. Before publishing, compare each item's own subject identity against the manifest subject —
 for JSON read `source_candidate_sha`/`subject`; for raw logs parse the `# git HEAD:` header instead of
 failing a log for not being JSON. Superseded-round artifacts are the usual offender: ARCHIVE them out
 of the new subject's evidence tree rather than leaving them in place.
 (k) **Hash the COMMITTED BLOB, not the working file.** Manifest hashes taken from local files disagree
 with what a remote reader receives whenever a write emits CRLF and git normalises the blob to LF —
 the mismatch surfaces only on remote readback, after you have already published. Compute with
 `git cat-file blob <rev>:<path>` AFTER the commit; in a throwaway evidence repo set
 `core.autocrlf=false` and `.gitattributes` `* -text`, and write JSON/logs with `newline="\n"`.
 Converge in passes: placeholder hashes -> commit -> hash the blobs -> rewrite the manifest ->
 re-commit -> re-verify against the remote ref. The pack excludes itself from its own item list, so
 rewriting it does not invalidate the items.
 (l) **When two vocabularies share one field, forbid the cross-axis value explicitly.** Validating a
 field against the WRONG vocabulary makes the defect type-legal — a canonical source state could be
 written as an execution label because the field was checked against the build/admission ladder
 (which is a different axis entirely). Model the axes separately: a closed registry retrieved
 VERBATIM from the source, a guard that execution-axis labels may never appear on the source axis,
 a guard that the token appears verbatim in the quoted source line, and a typed fail-closed unknown
 (`TEMP_CLOSED_REGISTRY_ROW`) instead of inventing vocabulary. The reviewer's counterexample must be
 UNREPRESENTABLE, not merely discouraged — encode the same law in the schema and ship tests proving
 the schema REJECTS each coercion, not just that it accepts the happy path. Where the source states
 no value for a row, mark it ASSIGNED_TERMINAL_SET rather than fabricating a token for it.
 (m) **Never name an entity your receipt cannot back with a row.** Before publishing a lineage/chain
 receipt, query the store for every id it names and confirm each resolves. If no table backs an
 identifier, list it separately as explicitly not backed (`spine_backed: false`) rather than letting
 it sit beside real ones — a named-but-absent entity is the same defect class as any other
 unsupported claim, and an independent lane reads it as one.
 (n) **A post-check edit needs its own verification — including the fix the checker asked for.**
 Corollary 2 covers a moved head; it applies equally to a corrected EVIDENCE artifact. Implement the
 checker's residual, then re-verify that artifact narrowly (does the new row really exist, does the
 digest recompute, does the store really lack the table the file claims) — do not reason that a change
 which only REMOVES a claim is exempt. And when a self-authored repair script applies the fix, read the
 artifact back and assert the old value is gone before any receipt says FIXED: a script that re-reads
 the file part-way silently discards its own in-memory edits while the receipt still reports success.
   (o) **Governance ORDERING is proven on one monotonic append-only stream, never by wall-clock.** A claim
   that "admission preceded the mutation" is only as strong as its ordering key. Timestamps (commit time,
   file mtime, epoch nanoseconds) are supporting metadata; a receipt asserting `wall_clock_only: false`
   while your own residual list says the oracle is host-clock-only is a self-contradiction an independent
   lane WILL find — before publishing, grep the whole evidence set for statements about the same property
   and make them agree. Use an ordinal the GOVERNANCE system generates and the writer cannot choose or
   backdate: an append-only table's DB-generated `rowid` over a SINGLE event stream; assert the stream is
   CONTIGUOUS (no gaps) as well as ordered; and record BOTH sides of the boundary on it (the lifecycle
   edge that means "admission closed, mutation permitted", plus a post-write event). Enforce it
   structurally rather than narratively: split the round into an admission process that is incapable of
   writing candidate source and an apply process whose FIRST assertions are that the permit artifact
   exists, that it records `source_mutation_started: false`, and that the tree is still exactly at the
   baseline and clean. Use the real governance vocabulary for those edges rather than invented stage
   names. Recipe + the rowid/contiguity queries: `references/governance-ordering-and-binding-proof.md`.
   (p) **Fetch the AUTHORITATIVE object before defining a local equivalent, and never assert a subject
   link an artifact cannot have.** When a gate demands an "authoritative binding/profile", grep the
   control plane for the object that already exists (its schema id, a live instance, the code that
   materializes it) BEFORE substituting a convention string — a convention is not a binding and an
   independent lane reads it as a defect. Corollary: an artifact that genuinely PREDATES the subject
   cannot contain the subject's final hash, so the evidence pack must model linkage explicitly —
   `DIRECT_FINAL_SUBJECT` only when the item itself derives the final subject, otherwise
   `TRANSITIVE_PRE_MUTATION_LINEAGE` with an explicit edge (baseline + workorder + permit -> final
   subject) — and a pre-mutation receipt must declare `direct_final_subject_match: false` rather than
   being marked as internally matching. Likewise a gate evidenced only by a boolean in a summary is NOT
   evidenced: persist each command's RAW output plus its own hash as its own artifact, because a
   reviewer correctly refuses `x_pass: true` as proof.
 (q) **A governance artifact needs a SEMANTICALLY REAL value, and its provenance must match the step
   that produced it.** Degenerate values are defects, not placeholders: a delegation whose
   `issued_at == expires_at` (zero-duration window) authorizes nothing, and an independent lane reads
   it as exactly that. Populate every window/limit/bound field with a real, positive, internally
   consistent value. A "pre-mutation" artifact must be GENERATED by the pre-mutation process —
   capturing it in the evidence step and labelling it pre-mutation reproduces the gate's own negative
   fixture (a stale pre-mutation readback), so capture it in the admission process and let the
   post-mutation side emit its own honestly-labelled artifact. When the correction target is an
   artifact that had to exist BEFORE the mutation, a RE-RUN is the only honest fix: editing it
   afterwards is retroactive fabrication. Re-run the whole chain from the clean baseline against a
   FRESH governed spine (ordinals then start at 1 and the stream is provably append-only with no
   prior-run residue) and a cleared evidence root.
 (r) **Classify each evidence item's linkage by what the artifact ACTUALLY derives, and resolve any
   denominator disagreement by reproducing the logged invocation.** A contract-bound artifact
   (compiler receipts and their rendered outputs) cannot be checked against the git HEAD — forcing it
   into `DIRECT_FINAL_SUBJECT` makes your OWN validator emit a false `invalid_direct_link_count` and
   blocks your own publish. Give each class its own linkage mode and check it by its own evidence
   (e.g. does the compiler receipt contain `PROMPT_COMPILE_PASS` at all); keep the counters SEPARATE
   per class, since one mixed counter both over- and under-reports. Likewise a `REQUIRED` manifest
   list must be built from each artifact's ACTUAL filename stem, or a present artifact registers as
   missing. When an independent lane's count differs from yours, do not settle it by asserting your
   own number: reproduce the EXACT logged invocation. Both harnesses can be wrong — a lane's scratch
   script using a different top-level dir under-reported 106 against a true 113, the mirror image of
   the maker-side stdout-only bug in (e).
 (s) **An EVIDENCE_ONLY cleanup round has its own five laws — each learned by shipping the defect first.**
   (s1) **A receipt that DESCRIBES an evidence set is invalidated by the next regeneration of that set, so
   it can never be stably true INSIDE it.** Generation/descriptive receipts (packaging, manifest, final
   readback, publish receipts) belong OUTSIDE the immutable set, or must be regenerated LAST after every
   artifact they hash. Expect SEVERAL instances of this class in one set (a packaging receipt, a
   final-readback receipt, a pack receipt) and treat the CLASS as the bug, not the instances: when one is
   found stale, preserve it VERBATIM under an explicit `superseded/` scope with a supersession record
   stating what it claimed and why — never silently overwrite or delete it — then remove the whole class
   by policy (an in-tree README stating it) so it cannot be reintroduced.
   (s2) **Derive every superseded enumeration FROM HISTORY, never from a hardcoded list:**
   `git rev-list <tip> --not <base>`. A hardcoded list silently omits commits created by an earlier run
   of the same script and leaves an undisclosed superseded pair — an independent lane reads an incomplete
   enumeration as a finding even when the retention claim itself is true.
   (s3) **Reference historical evidence as explicit `<commit>:<path>`, never a bare relative path.** A bare
   relative path is ambiguous about WHICH commit it means, and a consistency validator should reject it
   as an unresolvable named target.
   (s4) **Republish by ADVANCING the evidence branch (new commits), never force-pushing.** Earlier
   revisions are the audit trail of subjects a checker already read. Bind the new identity with a
   TWO-LAYER model: an in-tree immutable set that must NOT claim a commit id it cannot yet know (record
   `new_evidence_commit_sha: null` plus a DEFERRED marker), plus an out-of-tree readset naming the final
   evidence commit. Committing the readset would create a self-reference paradox.
   (s5) **Batch queued corrections into ONE revision while a checker is mid-flight.** Each republish
   invalidates the read the checker is performing, so serial-patching one finding at a time wastes whole
   verification cycles; fix the in-flight finding in the SCRIPT (so it is structural, not another literal)
   and land every pending fix together. If the target of the fix is inside the immutable set the reviewer
   has already read, a re-run is the only honest repair (see (q)), never an in-place edit.

   (w) **Construction-wave lessons from SWOF W2 (verified 2026-10-04): six harness defects/traps that each
   produced a false claim.** (w1) **`git commit -a` silently skips NEW files.**
   A writer round that only creates files commits NOTHING, and the receipt then points at the baseline
   (diff_count 0). Stage the admitted paths explicitly, assert the staged set is non-empty AND inside
   the write-set, and assert HEAD advanced — never `-a`. (w2) **A test count that moves while the commit
   delta does not is the tell that your stage list is narrower than your admitted write-set.** Real case:
   the observability root went 97 -> 102 while the commit contained no observability path, because the
   stage list still named three directories after the write-set had grown to four. Fix the stage list
   from the SAME constant the write-set uses. (w3) **The lifecycle idempotency key is
   `{project}:{run}:{from}->{to}:{attempt}`** (hg_kseos/lifecycle `_emit_transition`), so a second
   `EXECUTING->VERIFYING` after a corrective round collides unless the attempt counter advances. Use the
   data's own repair loop (`EVOLUTION_REVIEW/VERIFYING -> REPAIRING -> EXECUTING`, i.e. what
   `begin_repair()` does) or advance `repair_count`/`attempts_used` exactly as that method does; never
   hand-roll a second boundary without it. (w4) **An admitted glob entry like `src/x/*` is a DIRECTORY
   PREFIX, not a string to `startswith` against.** Matching the literal string mis-flags every nested
   file as unassigned and makes your own aggregate receipt self-report `containment_ok: false` while the
   per-WorkOrder receipts say true — an in-evidence contradiction a reviewer reads as a failed gate.
   (w5) **A receipt cannot show its own consumer as complete.** Any board/status snapshot written by the
   step that also closes the last card is structurally self-refuting if you claim it lists only open
   work: state `snapshot_semantics` (point-in-time) and list `items_completed_after_generation` rather
   than claiming liveness. Regenerate such snapshots LAST, and word the close-evidence to what the
   artifact actually supports. (w6) **Synthetic credential fixtures in the source make any evidence
   secret-scan non-empty.** A security suite proves its detectors with planted keys; a scanner cannot
   distinguish a fixture from a live secret. Redact the COPIES into the pack with a per-file receipt
   naming what was redacted and why — do not argue the finding away, and do not strip the fixtures from
   the product repo where they are load-bearing test data.

   (x) **Corrective-round shape that converged in four rounds (SWOF W2, 2026-10-04).** Each round:
   freeze the subject -> fresh VERIFY_ONLY lanes (one governance/evidence lane + one adversarial product
   lane, never the maker) -> the checker does NOT repair -> bounded corrective round via the tracked
   writer on a NEW commit -> NEW verification run on the NEW subject. Label every prior verdict
   `SUPERSEDED` with the head it actually read; never carry a stale PASS forward. Round severity should
   fall monotonically (2 blocking -> 1 blocking -> 0 blocking -> 0 blocking) — if it does not, the
   corrective round is addressing symptoms. Keep a CUMULATIVE finding ledger: per-round disposition
   objects omitted ids twice and the reviewer caught both; one ledger with every id and an explicit
   disposition (closed / disclosed / accepted-with-rationale) cannot be incomplete by construction.
   Some residuals are STRUCTURALLY unclosable (e.g. an artifact that cannot display its own completion)
   — disclose them, reduce the claim, and stop rather than recursing; the wave verdict then carries
   `WAVE_VERDICT_PARTIAL` while the product lane legitimately carries PASS.

   (z) **Repair-order adjudication: probe the exact bytes before mutating, and never let a LANE verdict
   satisfy an AGGREGATE gate (verified 2026-10-04, SWOF W2 closure repair).**
   (z1) **When two independent challenge reports disagree on whether a product defect exists, the
   tie-break is a source-bound deterministic PROBE on the frozen bytes** — not the newer report, not the
   more authoritative-sounding one, and emphatically not the one that agrees with your own reading.
   Observed: a report asserting "the product substrate is mature; only governance/evidence closure
   remains" was FALSIFIED by probes that reproduced both claimed fail-opens in the shipped code. Run the
   probe gate BEFORE any product mutation — that is usually the order's own first step, and skipping it
   turns a bounded repair into an unadjudicated rewrite. Probe the CONTROL cases too (a benign input must
   still pass), or "everything is broken" is indistinguishable from "the probe is broken".
   (z2) **Author the defect probes as a PAIR — the same oracle before and after the fix.** The probe set
   that reproduced the defect is re-run against the repaired source and must now refuse every case it
   previously allowed while its positive controls still pass: same call sites, inverted expectations.
   That is what turns "the defect no longer reproduces" into evidence instead of a claim. On a new probe
   failure, classify WRONG PROBE vs real DEFECT explicitly before touching code (rule (u) Corollary 2).
   (z3) **Prove a missing typed-API capability from SOURCE, and classify CREATION != RESOLUTION.** A scan
   that counts any statement NAMING the table as a "writer" reports the capability as present (observed:
   the `INSERT INTO acceptances` that creates the row with its initial verdict counted as a resolver, so
   the harness announced `TYPED_API_PRESENT` for a spine that has no resolver at all). Only a statement
   that can move the field OFF its initial value counts (`UPDATE ... SET verdict`, or
   `INSERT ... ON CONFLICT DO UPDATE`). When the control plane genuinely cannot materialize required
   state through typed APIs, the honest terminal is `TEMP_CLOSED_STATE` plus a SEPARATE engineering-base
   ChangeSet proposal plus HITL — never a direct SQL write, and never a patch to shared core smuggled in
   under a project/repair order. Deliver the independent legs anyway (product repair, reducer fix, fresh
   checker, evidence, publication) and reduce the claim; do not force a closure the typed API cannot make.
   (z4) **Every aggregate gate must read the AGGREGATE verdict, and every claim string must be DERIVED
   from it.** Real defect: the closure reducer computed the wave gate as `product_verdict == "PASS"`,
   dropping `wave_verdict`/`governance_verdict` entirely, so a product-lane PASS proxied an overall
   PARTIAL and the gate set reported PASS; separately the claim ceiling hardcoded a
   "W2_INDEPENDENT_CHECK_PASS" phrase while the checker's own verdict was PARTIAL. Fix shape: extract the
   reducer as a PURE function over the checker receipt (wave verdict == PASS AND governance == PASS AND
   checker != maker AND checker read-only AND subject matches the candidate), and DERIVE the claim string
   from that verdict so a non-PASS verdict makes the over-claiming phrase UNREPRESENTABLE. Ship the four
   fixtures the order names (product PASS + checker PARTIAL => FAIL; + governance PARTIAL => FAIL;
   + checker == maker => FAIL; all PASS + maker-separated => PASS), plus read-only and
   subject-mismatch cases, and evaluate them through the SHIPPED reducer rather than a copy. This is the
   Gate-Calibration-Failure class: a local metric satisfying a metric while the objective stays open.
 Three further traps in the SAME defect class, each caught by a fresh checker after the fix looked done:
 (i) **A truth function must never `.get(primary, fallback)` across two semantic lanes.** The reducer read
 `checker.get("wave_verdict", checker.get("verdict", ""))`, so a receipt carrying only the PRODUCT-lane
 `verdict: PASS` passed the aggregate gate with no overall verdict present at all — the historical proxy
 defect, merely relocated into a default argument. A field the gate depends on must be read as
 `checker["wave_verdict"]` and an ABSENT value must yield the empty/failing verdict; add the
 missing-field and empty-string fixtures alongside the four the order names.
 (ii) **A disclaiming string must not CONTAIN the literal it disclaims.** The reduced branch read
 `W2_INDEPENDENT_CHECK_PASS_NOT_CLAIMED_<verdict>`, which still matches any substring scanner for the
 claimed token and defeated the emitter's own absence assertion. Rename so the disclaimed token is
 unrepresentable (`W2_OVERALL_INDEPENDENT_PASS_NOT_CLAIMED_...`), then assert the absence BOTH ways:
 present when the verdict is PASS, absent for every other verdict.
 (iii) **There must be exactly ONE emitter of the claim string.** Fixing the reducer left a SECOND
 hardcoded copy of the claim literal in the packaging emitter, which never consulted the verdict at all —
 so the over-claim survived the fix. Make the emitter READ the claim from the closure receipt (assert the
 receipt exists first) and grep the whole harness for any remaining literal of the claimed token; a claim
 with two sources is a claim with none.

 (z6) **When a spec DELEGATES a check, the delegate must receive the ARTIFACT being checked — an
 identifier is not a verification (verified 2026-10-04).** A repair spec said signature verification was
 "delegated to an injected trusted key registry"; the interface it specified passed the registry only
 `(issuer_id, key_id, key_generation)`. That contract can assert KEY TRUST and nothing else, so a token
 carrying an arbitrary shape-valid signature was APPROVED whenever its key triple was trusted — the
 checker forged one and it passed, and the spec's own sentence became the finding. Rules: (1) the
 delegate's signature must carry the bytes to re-derive the check (the canonical payload WITHOUT the
 field under test, plus the field itself) and must return a STRICT bool, with every other outcome —
 None, a truthy non-bool, a wrong arity, an exception, an absent delegate — failing closed as an
 integrity denial; (2) ship a `canonical_payload_bytes()`-style function so the bytes are deterministic
 and a real verifier can recompute them, and state plainly in the docstring that the library performs NO
 cryptography itself and that a registry which only checks key existence is a CONTRACT VIOLATION by the
 integrator — do not let the module appear to have verified what it merely trusted; (3) a cheap
 shape-regex validated before delegation is not verification — never let it stand in the receipt as one;
 (4) the same reading applies to any "trusted object" seam: when the seam is handed a pre-built route/
 decision object, RE-DERIVE the predicate from the primitive inputs it carries (operation, tier,
 permission class) and refuse when the handed object UNDERSTATES them — otherwise a directly constructed
 `required=False` object silently skips the gate; (5) an optional actor/approver argument defaulting to
 None creates a self-approval path — compare the approver against the request-bound actor inside the
 verifier, not only against the optional caller-supplied one. Generalisation: any sentence of the form
 "X is verified/delegated/checked elsewhere" must name the input that makes the check POSSIBLE, and if
 you cannot point at that input in the interface, the sentence is an over-claim you will be caught on.
 (z5) **Maintenance traps when editing THIS skill: grep the existing letter labels before appending a
   lettered sub-rule** — a reused letter silently yields two different laws under one id and a later
   reader cites the wrong one; number from the highest label actually present. And after patching a
   multi-line Python literal that writes a receipt, RE-READ the region and parse-check it: a `return`
   left above the new code makes the payload silently empty, and duplicate dict keys are ACCEPTED by the
   parser (last wins), so the artifact is wrong while the syntax check is green.
   Probe-pair and capability-gap recipes, plus the ChangeSet shape:
   `references/conflicting-challenge-report-adjudication.md`.

 Three laws, each
   learned by shipping the defect first:
   (y) **Evidence sanitation must run on the PRODUCT's own detector, and be asserted on the COMMITTED
   blobs (verified 2026-10-04, SWOF W2).** A pack that redacts with its own local pattern list is a
   SECOND SEMANTIC ROOT: it drifts from the shipped classifier and silently leaves classes the product
   still calls SECRET/PII in the published bytes (observed: a pack-local rule set removed aws_key/
   bearer/private-key while the shipped detector simultaneously flagged github_token,
   bearer_auth_header, email_address, card_like_number and taiwan_national_id in the SAME files — and
   the pack's own `clean_after_redaction: true` was therefore false). Rules: (y1) redact with the
   product's classifier (`from src.security.classification import redact`), never with a copied rule
   list; (y2) after committing, re-classify every committed blob with the product's `classify()` and
   ASSERT nothing exceeds PUBLIC — fail closed, so the pack cannot certify itself; (y3) a scanner cannot
   tell a PLANTED fixture from a live secret, so transform the evidence copies and record per-file
   before/after sha256 in a transform receipt rather than arguing the finding away, and leave the source
   repository's load-bearing fixtures untouched; (y4) verify the claim on the REMOTE blobs (re-fetch and
   classify), not only locally — "clean locally" is not "clean as published"; (y5) if a published SHA was
   already read by a checker, correct it by ADVANCING the branch (fast-forward, never force-push) and
   record the revision history with the reason, so earlier readers' subjects stay resolvable.
   (aa) **Never record a figure you did not just measure with the command quoted beside it** - the
   failure mode is writing the EXPECTED SHAPE after the test count changed; a record corrected twice is
   a RECORDER defect, so derive every number from command output. **"Registered" is true only after a
   readback from the CANONICAL store** (resolve its path from config - a project-local DB looks like
   success). **Audit your own harness against the order's prohibitions before running it** (a script
   using forbidden direct SQL invalidates its own receipt). **Do not churn a FROZEN,
   independently-PASSing subject for non-blocking cosmetic items** - record them as TTs instead.
   Full catalogue: `references/harness-and-evidence-defects.md`.
   (z) **A verification probe that imports the product under a DIFFERENT package path than the product's
   own tests creates DUPLICATE CLASS IDENTITIES and fabricates failures (verified 2026-10-04, SWOF W2).**
   Symptom: a perfectly valid object is rejected with a type-guard error (here
   `NOT_A_CANONICAL_APPROVAL_TOKEN` from `isinstance(token, ApprovalToken)`) while the product's own
   suite is green. Cause: the product lives at `<repo>/src/security/`, the test helper did
   `sys.path.insert(0, "<repo>/src/security/tests")` and imported `security.humangate`, while the probe
   put `<repo>` on the path and imported `src.security.humangate` - two module objects, two
   `ApprovalToken` classes, `isinstance` False across them. Rules: (za1) import the product the SAME way
   the product's tests do, or lift the symbols out of the already-loaded test module's namespace
   (`verify = test_module.verify_fn; Cls = test_module.Cls`); (za2) before reporting a type-guard failure,
   print `type(obj)` and `obj.__class__.__module__` and compare against the callee's expected class - a
   module path difference means your harness is wrong, not the product; (za3) when a probe's expectation
   fails, first ask whether the assertion encoded the wrong PRECEDENCE (e.g. expecting the signature
   failure code on a field that the earlier exact-binding stage already rejects) or the wrong FIXTURE
   (asserting a P3-only reason code against a P2 request) before touching product code - three of the
   four probe misses in this session were harness errors, and the fourth was a helper that re-signed the
   token so it could not express "changed after signing" (use `dataclasses.replace` on an already-signed
   value instead). A probe is guilty until proven innocent.

   (aa) **An authorized shared-core repair is a bounded, inventoried, independently-checked ChangeSet**
   — full procedure in `references/shared-core-change-set-authorization.md`. Always-on rules: (aa1)
   inventory the typed API FIRST (grep writer statements per closure-primitive table + list public
   methods) and add ONLY the primitives genuinely missing; one missing method is a one-method diff.
   (aa2) Never add a generic `force_close()`-style escape hatch — a repair primitive carries the same
   discipline as its neighbours (closed value set, mandatory subject binding, lease/actor/token,
   idempotency, one atomic transaction, a canonical event carrying `from_state`, history never
   rewritten). (aa3) Consumers and project harnesses must not issue SQL WRITES against canonical tables,
   including "just one checkpoint row" — every write goes through a typed API and SQL is for SELECT-only
   readback; check your own harness for this before running it. (aa4) "Registered" means a ROW in the
   registry named by the project config (`canonical_database`), verified by readback — not prose in a
   JSON blob and not a row written into whichever spine database happened to be open. (aa5) Fix the
   whole failure class, not the instance: one missing-field bypass usually means the sibling branch has
   the same hole (a guard matching `entity_id` but not `entity_type` against a globally-UNIQUE key
   namespace lets a foreign entity's event be inherited as a valid replay).

   (bb) **Never write an evidence figure you did not just measure.** (bb1) Every count/hash/size must be
   produced by the exact command quoted beside it, and re-measured after ANY change to the test count or
   file set — recording the expected shape instead of the measurement is a recurring defect that
   survived three consecutive record revisions in one session. (bb2) Store volatile artifacts (a diff)
   as byte files with hash + size + the producing command; a re-derived diff hash is not reproducible
   across invocations. (bb3) When a checker's findings stop being about the CODE and start being about
   the RECORD or the REGISTRIES, the implementation is usually done: fix the record, tighten only the
   specific delta attacked, re-verify that delta, and do not re-open the implementation.
   (zb) **Adding ONE missing primitive to a shared core is a bounded ChangeSet with its own laws
   (verified 2026-10-04, HGK acceptance-resolution primitive).** (zb1) **Inventory from SOURCE first and
   add only what is genuinely absent** — a scan that counts any statement NAMING a table as a "writer"
   reports the capability as present, so classify CREATION (`INSERT ... (verdict NOT_RUN)`) separately
   from RESOLUTION (`UPDATE ... SET verdict`, `INSERT ... ON CONFLICT DO UPDATE`). (zb2) **A fail-closed
   guard whose subject parameter is OPTIONAL is not a guard** — a defaulted `requirement_id=None` makes
   the wrong-subject check opt-in. (zb3) **An idempotent-replay short-circuit must match the FULL subject
   key.** A globally UNIQUE idempotency namespace is shared across every entity type, so `entity_id`
   alone is not a key: a requirement/taskspec/workorder event carrying an `entity_id` equal to your
   acceptance id is handed back as a valid replay while the intended write is silently skipped — match
   `entity_type` AND `entity_id`, and put the subject check BEFORE the replay branch or the replay path
   is the one route that bypasses it. (zb4) **Prove an executed UPDATE rolls back**: a pre-seeded
   idempotency key tests the REPLAY path and an illegal-transition guard raises BEFORE the write, so
   inject the failure AFTER the UPDATE (patch the serialiser that builds the event row) and assert the
   row is untouched. (zb5) **A with/without regression table has THREE states, not two** — change+its
   tests / pristine-with-the-new-test-file-removed / code-reverted-with-the-tests-still-present — each
   with its own count; measure every one and never write a figure you did not measure (quoting the
   pristine number for the code-reverted state was caught twice, and "the remainder pass vacuously" was
   simply false). The durable claim is narrower and provable: the SAME pre-existing failures appear in
   every state, proven by diffing SORTED failure-name sets. (zb6) **"Opened as TT-xxx" must mean
   REGISTERED**, not described in a docstring or evidence JSON — write it through the typed API and the
   tracked ledger, then read the registry back. (zb7) **When a named property cannot be achieved inside
   the minimal scope, NARROW THE CLAIM rather than expand the scope or overclaim** — state the precise
   achieved claim in the code, open the gap as a typed non-blocking TT with its close criterion, and
   make code + docstring + evidence JSON + TT agree; that agreement across four surfaces is exactly what
   an independent lane checks. Procedure, guard rules and the measurement table:
   `references/shared-core-primitive-changeset.md`.

   (aa) **The authoritative HGK registry is a NAMED PATH, not "the spine you happen to have open"
   (verified 2026-10-04).** `config/project.json` → `canonical_database = var/shared-spine/hg-kseos.db`
   is THE canonical spine (AGENTS.md confirms). A per-wave/per-project DB such as
   `var/<wave>/hgk_spine.sqlite3` is only a project-local spine. Writing a TT/evidence/acceptance row
   into the project spine and then reporting it as "registered" is a FALSE claim that an independent
   checker will catch by querying the canonical path — exactly what happened here with `open_tt`. Rules:
   (aa1) resolve the registry path from config every time and read it BACK from that exact path before
   claiming a registration; (aa2) if you write to the wrong store, disclose it and re-register in the
   canonical one rather than deleting the stray rows (the stray write is a real historical fact);
   (aa3) symmetric trap for schemas — never count a canonical field list by eye: extract the `required`
   array from the law file and set-diff it against the implementation (the PI-PKG-06 ApprovalToken
   registry has **42** required fields plus one *conditional* `independent_checker_evidence_ref`; an
   implementation with 37 was reported as "41 fields complete", which is precisely the
   arithmetic-by-vibe error this rule prevents); (aa4) the same discipline applies to your OWN evidence
   record — a regression figure or registry claim that an independent checker cannot reproduce is a
   defect of the record, so quote the exact command next to every figure and re-measure whenever the
   test count changes.
   (t) **Closing an evidence-TRANSPORT or evidence-IDENTITY gap (verified 2026-10).** Three laws, each
   learned by shipping the defect first:
   (t1) **A "not supplied" finding is closed by DELIVERING the exact artifact, not by re-describing where it
   lives.** When a challenge rules that the authoritative file was never handed over, regenerate it LIVE for
   the current round (a stale round label or a placeholder identity field is itself a defect), bind it to the
   exact immutable subject, and ship a COMPLETENESS RECEIPT that enumerates every artifact the reviewer must
   receive together with its hash — plus the exact tuple. Inputs the evidence merely REFERENCES but does not
   contain (the order, the challenge report, the RBWI, the compiler bundle, predecessor prompts) are declared
   as referenced-not-supplied with their recorded hashes, never silently assumed present.
   (t2) **Adjudicate a conflicting artifact IDENTITY on the GOVERNED binding — never on mtime, citation
   count, or hash majority.** Two copies of one governed artifact with different hashes are resolved by
   (i) hashing each at its exact physical path NOW; (ii) finding which exact path the GOVERNED pipeline binds
   as NORMATIVE, read out of an already-accepted contract's source row; (iii) the content relationship (which
   revision is the superset). Then ask the decisive practical question: **is the mandated support bundle
   byte-identical under both candidates?** If the executed inputs are identical the choice has no downstream
   effect — say so and do NOT publish a commit merely to record a preference. A citation survey is weak
   evidence: a derived index (`.db` projection) and a self-declared derived manifest are NOT authority, and
   the losing candidate usually has exactly those and nothing else. If equal-rank sources stay unresolved,
   the honest terminal is a TEMP_CLOSED / CR state, never a silent pick.
   (t3) **Disclose the delta between the last independently-verified revision and the final one.** When a late
   change lands after a verified revision, enumerate the exact changed files, prove the substantive artifacts
   are byte-identical, and state plainly that the final revision is NOT independently re-verified — never let
   a new commit inherit the previous PASS. Then HASH-PIN THE ORDER'S OWN CITED INPUTS: recompute sha256 for
   every input the order names and compare; a mismatch means you edited a cited document after the order was
   authored, which is a disclosure rather than a detail to bury.
   Mechanics — path-independent blob readback (a path-based read past Windows MAX_PATH returns EMPTY and
   registers as a false mismatch), one-call two-layer transport reconciliation, the contract-row extraction
   trap (a row can be keyed `id` OR `source_id`), and the null/placeholder sweep that catches an over-claim
   references/external-review-evidence-packaging.md` §9.

   (u) **A completed card's recorded result is a CLAIM, not a fact — re-derive its numbers before anything
   downstream reads them (verified 2026-10, SWOF W2-D3).** A wave summary is copied verbatim into every
   child card's `worker_context`, so an inflated `N files` / `N tests` line propagates as if it were
   verified. To verify a DONE card, re-derive from artifacts rather than re-reading the summary: the
   WorkOrder SPEC's own file list, `git diff --name-only <base>..<head>`, the containment
   `workorder_delta`, the raw focused-test log, and the sha256 of every log the apply receipt names
   (mismatch there invalidates the pack, not just the count). Expect the recorded count to be WRONG —
   observed "19 files" against a verified 17 (SPEC list, commit stat and containment delta all agreeing
   at 17) — and report the discrepancy instead of rounding it away; a fabricated number and a merely
   miscounted one are indistinguishable until you re-derive. Because the parent snapshot is frozen at
   child-promotion time, post the correction as a comment on the CHILD cards too, not only on the
   parent.
   Corollary 1: **write your OWN probe rather than trusting the producer's tests** when the card's whole
   point is that a checker must be able to fail — enumerate the SPEC's rejection classes, inject each,
   and assert the exact typed error/reason_code; include the accepted control case so a probe that can
   only reject is equally visible.
   Corollary 2: **a probe that fails N cases is suspect before the code is.** Check the input CONTRACT
   first (here: an oracle that refuses any supplied order differing from canonical `(kind, item_id,
   sha256)` order and returns `NON_DETERMINISTIC_ORDER`, so a deterministic-but-unsorted caller looks
   like a defect). Classify every probe failure as WRONG PROBE or real DEFECT explicitly, and record a
   contract nuance as an observation in the handoff rather than silently fixing your own harness.
   Corollary 3: **scratch kanban workspaces are deleted at completion** — copy verification artifacts
   (probe source, raw output, sha256s) to a durable path outside the workspace (e.g.
   `<board>\verification\<task-id>\` BEFORE the terminal action; a receipt citing a path inside a
   scratch workspace is unreadable later, and the numbers it carries will survive only in the comment.

   (v) **A multi-round verification loop needs a per-round identity, and the lifecycle table has a key
   that WILL bite you (verified 2026-10-04, SWOF W2).** Independent checks of an implementation-heavy
   wave converge over ROUNDS (observed R1: 2 blocking -> R2: 1 blocking -> R3: 0 blocking). Round N's
   verdict binds exactly the head it read, so a post-verdict repair must produce a NEW head and a NEW
   verification run; preserve every round's RAW transcripts verbatim in the evidence root (e.g.
   `checker_live/ROUNDn_task-*.log`) with their sha256 recorded in that round's findings file, and label
   earlier rounds SUPERSEDED rather than editing them. Five defects this loop produced on first contact:
   (v1) **`project_transitions` / `canonical_events` derive their idempotency key from
   `{project}:{run}:{from_state}->{to_state}:{attempt}`** — so a SECOND `EXECUTING -> VERIFYING` (which
   every new write round needs) raises `UNIQUE constraint failed: canonical_events.idempotency_key`
   even though its rowid would be new. Do NOT work around it with a raw insert: do what `begin_repair()`
   itself does — advance `repair_count` and `attempts_used` on `project_lifecycles`, then emit — and
   prefer the real repair vocabulary (`VERIFYING|EVOLUTION_REVIEW -> REPAIRING -> EXECUTING`, with a
   `..._WRITE_PERMITTED` trigger BEFORE the write and `..._APPLIED` after) so the corrective round is
   ordered exactly like the initial one.
   (v2) **A write-set entry like `src/security/*` is a DIRECTORY PREFIX, not a glob to `startswith`
   against.** Matching the literal string mis-flags every nested file as unassigned, so your own
   aggregate containment receipt self-reports a FAILED gate (67 false unassigned paths observed) while
   the per-WorkOrder receipts and an independent recompute both say containment holds. Strip the
   trailing `*` and compare prefixes; a self-inflicted false negative is still an internal inconsistency
   an independent lane will report against you.
   (v3) **`git commit -a` silently skips NEW (untracked) files.** A first-time write of a whole new
   subsystem commits NOTHING, so the receipt reads `candidate == baseline` / `diff_count: 0` while the
   files sit on disk. Stage the admitted paths explicitly and ASSERT the staged set is non-empty and
   inside the write-set before committing, then re-derive the receipt from the new HEAD.
   (v4) **Generate any DESCRIPTIVE receipt LAST.** A kanban execution receipt / packaging readback is
   invalidated by the next state change; written early it claims "regenerated after completion" while
   still listing those cards as unclaimed — a legitimate (non-blocking) finding, and one the checker
   WILL find because it compares the receipt against the live board DB.
   (v5) **Keep a CUMULATIVE finding ledger** (id -> round -> state -> disposition -> close evidence)
   instead of per-round disposition objects: a finding mentioned only in one round's prose has no
   disposition and reads as an unclosed item several rounds later.

 ## Routing decision matrix (lane vs execution surface)

| Router output (lane) | Meaning | Execution surfaces that STILL apply |
|---|---|---|
| `NATIVE` / DIRECT | HGK/Hermes orchestrates directly | Kanban + Swarm + gstack/OpenSpec check + Codex writer |
| `OPENSPEC` (brownfield) | OpenSpec named method selected | Kanban + Swarm + Codex writer |
| `GSTACK` (review/qa/plan…) | gstack named method selected | Kanban + Swarm + Codex writer |
| Kanban/Swarm lane | routed for parallel/worker execution | same surfaces, now worker-backed |

The router never disables execution surfaces; it only picks the orchestrator.
Evidence to record for every task: `selected_route`, `reason_code`,
`registry_source_basis`, `workorder_ids`, `runtime_ids`, `fallback_degrade`.

## External-challenge evidence closure (EVIDENCE_ONLY Contract A — learned 2026-08-12)
> external PARTIAL_CHALLENGE / EVIDENCE_GAP 閉環 → 載入 `references/step-evidence-only-contract-a.md`。
> （2026-08-15 拆分搬移，原文 bytes 未改動。）

## Independent acceptance/challenge-verification lane (VERIFY_ONLY, verified 2026-08-13 FAR TRI_SOURCE challenge)
> 獨立驗收/挑戰 lane（VERIFY_ONLY / AO）→ 載入 `references/step-verify-only-lane.md`。
> （2026-08-15 拆分搬移，原文 bytes 未改動。）

## Step 0 — Mandatory baseline readback (before ANY mutation)

1. Task-A acceptance evidence: `Fabric\evidence\review\HGK_POST_HERMES_REINSTALL_BOOTSTRAP_ACCEPTANCE.md`
   — verify SHA-256 matches the expected value from the prompt and the internal claim is PASS.
   Mismatch → STOP.
2. Single Hermes runtime: `where.exe hermes` (one hit), CIM process tree (one canonical
   Desktop tree + its venv backend = 1). Check `var\hermes-v020` absent and no process
   references retired/recovery paths.
3. HGK doctor: `PYTHONPATH="C:\Projects\Agent_Workspace\HG-KSEOS\src" ".venv\Scripts\python.exe"
   -m hg_kseos --root "C:\Projects\Agent_Workspace\HG-KSEOS" doctor` → verdict PASS, blocking [].
   NOTES: (a) the MSYS path form `PYTHONPATH=/c/...` silently fails — use the Windows-style path;
   (b) in the Hermes desktop/gateway context the unquoted forward-slash executable form
   `.venv/Scripts/python.exe` can trip the gateway lifecycle guard (crash: "embedded null
   character in path" inside lifecycle_guard.py) — the reliably working form is the QUOTED
   BACKSLASH path `".venv\Scripts\python.exe"`; use it for every HGK venv python invocation.
4. RP-002 v2.0 state: `hg_kseos project status HGK-REFERENCE-PROJECT-002` → ACTIVE;
   Stage-1 (RP002-STAGE-FABRIC) **SEALED** 2026-08-12 after external PASS_CHALLENGE
   receipt (STAGE-1-SEAL.yaml SHA d1a219a5…; review MD SHA a9111783…; bootstrap
   receipt GRANTED; EG-001/002/003 CLOSED_CONFIRMED). Stage-2 (RP002-STAGE-HGK)
   entry authorized; next gate K1; Stage-2 local claim ceiling
   RP002_STAGE2_LOCAL_ACCEPTANCE_PASS.
   STAGE-2 entry NOT_AUTHORIZED until external PASS receipt + STAGE-1-SEAL.
5. Git snapshot of HGK/SQS/Fabric HEAD+branch+porcelain count — the task must not change
   these counts except the mandated evidence files.

## Step 1 — Resolve current authority

- HGK: `config/hermes.json` (runtime binding), `config/hermes-codex-lane.json` (sealed
  Codex lane), `scripts/hermes-core.ps1` + `scripts/start-hgk-hermes.ps1` (verify actions).
- SQS: `STATUS_VECTOR.json`, `evidence/review/SQS_RP001_MILESTONE_CLOSURE_RECORD.md`
  (MILESTONE_CLOSED), `docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md`, `risk/limits.yaml`,
  `survival/guards.yaml`, `SSOT/RBWI_WP_CONTROL_PACK/G01..G07`.
- Fresh source wins over prompt hints. No-Source-No-Norm.

## Step 2 — Admit ONE diagnostic WorkOrder (typed Shared Spine API)

Use the typed `SharedSpine` API directly (do NOT run the full project lifecycle for a
diagnostic task). Exact sequence with idempotency keys in
`references/shared-spine-admission.md`. Keep task tooling in gitignored `var/a2/`
(or similar) so the tracked tree stays untouched.

User decisions that CHANGE a blueprint spec (e.g. daily OHLCV 5y → 3~4y / 263 stocks,
verified 2026-08-13) must be frozen FIRST as a `USER_DECISION_<topic>_<date>.md`
evidence artifact (front-matter: decision_id, authority=USER, decided_at, status,
supersedes, supersession_basis, bound_into) and its SHA-256 bound into the REQ
source_locator. Never fold a verbal spec change into REQ wording without a hash-bound
decision record; the decision file is a first-class evidence artifact mirrored to the
three roots like any other.

## Step 3 — Kanban board + DAG

```bash
hermes kanban init
hermes kanban boards create <slug> --name "..."
hermes kanban boards switch <slug>
hermes kanban create "A2-K1 ..." --tenant hgk --priority 1 --json   # capture id from JSON
hermes kanban create "A2-K3 ..." --parent <K1> --parent <K2> ...     # DAG edges
hermes kanban assign <task> <profile> && hermes kanban claim --ttl 1800 <task>
hermes kanban heartbeat <task> --note "..." && hermes kanban complete <task> --result "..."
```

Pitfalls (empirically verified this stack):
- `--priority` is an INT, not "P0".
- Dependencies live in table `task_links` (parent_id, child_id), NOT `task_dependencies`.
- Task status is `done` (not `completed`) in the DB; `hermes kanban list` shows `✓ ... done`.
- **`HERMES_DELEGATED_CHILD_CONTEXT=1` in the terminal env blocks `kanban complete`**
  ("delegate_task child contexts cannot mutate Kanban tasks via the CLI" — same defect can also
  surface as "kanban: could not initialize database: …cannot mutate Kanban tasks or boards" on a
  fresh board). After running a delegate_task batch, `unset HERMES_DELEGATED_CHILD_CONTEXT` to
  restore orchestrator power. This is a session-snapshot env LEAK (the child's spawned shell marker
  round-trips into the shared snapshot and is re-sourced by the main session), not broken
  delegation — full verified mechanism + source map in `references/delegation-marker-env-leak.md`.
- `kanban create` returns `ready` for parentless tasks, `todo` for tasks with parents;
  dependents are promoted only after parents complete (visible in `task_events` kind=promoted).

## Step 4 — Genuine ≥2-lane Swarm

`delegate_task(tasks=[...])` batch with two read-only leaf workers (e.g. HGK lane + SQS
lane). Proof requirements: worker lane IDs, kanban task IDs, started_at/completed_at UTC,
overlap interval (both live simultaneously), heartbeat events, completion, no ghost worker.
Live transcripts at `C:\Users\user\AppData\Local\hermes\cache\delegation\live\<deleg_id>\task-*.log`
— timestamps there are the overlap evidence. No artificial mutations to fake concurrency.

**Reading multi-lane results: prefer the live transcript over the summary file (verified 2026-08-20 FAR
negative-PnL round).** `cache\delegation\subagent-summary-<task>-<ts>.txt` files can be cross-contaminated
(a lane-0 file this session contained an unrelated env-hijack audit instead of the requested root-cause JSON)
or truncated so the payload is cut off. Do NOT adopt a summary file's content as that lane's verdict without
confirming it matches the dispatched goal. Reliable path: reopen each `live\deleg_<id>\task-<n>.log` and pull
the last `final | status=completed ...` region or the final `agent_message` / executed JSON block; verify it
addresses the task goal before synthesizing. When goal vs returned content diverge, flag contamination and
extract the true JSON from the log — never fold mismatched content into the synthesis.

## Step 5 — Codex primary-execution canary

The sealed lane: pinned executable `%LOCALAPPDATA%\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe`
(verify `codex --version` → `codex-cli 0.147.0-alpha.6.5`), isolated CODEX_HOME/OPENCODEX_HOME,
**opencode-go/deepseek-v4.1-flash** (permanent user-set route; the older `deepseek-v4-flash`
slug is superseded), credential resolved by exact env-var name from the canonical
hermes .env. Full PowerShell invocation pattern + all capture pitfalls in
`references/codex-canary-powershell.md`.

Key decisions:
- **Inspect the REAL repo with `--cd <root>` + `--sandbox read-only`** — do NOT use a
  detached worktree of HEAD: untracked files (like `config/hermes-codex-lane.json`) are
  absent there and committed (stale) content shows instead.
- **WRITES through this lane are NOT possible with `--sandbox workspace-write`**: codex
  CLI 0.147.0-alpha.6.5 client-forces a read-only profile when talking to the custom
  opencodex endpoint (no apply_patch tool, shell writes "blocked by policy"), regardless
  of flags/config. The validated working write pattern is
  `--sandbox danger-full-access -c approval_policy=never` with process-boundary safety
  (WorkOrder-scoped narrow prompt enumerating exact files, git diff review, targeted
  tests, independent checker) — this is the Hermes `codex` skill's documented
  gateway-context pattern. **`--ask-for-approval never` was REMOVED from codex exec in
  this build (verified 2026-08-14 WO-HGK-MEM-RESEARCH-001):** passing it fails with
  `error: unexpected argument 'approval' found`; use `-c approval_policy=never` splatted
  BEFORE `--json`. Full investigation + invocation in
  `references/codex-workspace-write.md`.
- Prove `HERMES_DIRECT_TRACKED_PRODUCT_WRITE = 0` via porcelain count before/after.
- Provider receipt from `usage.jsonl` (provider/model/status 200) is the auth proof.
- **CODEX_HOME env trap (2026-08-20):** calling `codex.exe` from a shell WITHOUT
  exporting the lane env defaults to the HUMAN `~/.codex` (ChatGPT auth) → spurious
  `model is not supported when using Codex with a ChatGPT account` even when the
  daemon is healthy; export `CODEX_HOME`/`OPENCODEX_HOME` to `%LOCALAPPDATA%\HG-KSEOS\codex-hermes`
  /`opencodex-hermes` in the same invocation. And on `--sandbox read-only`/`danger-full-access`,
  codex cannot run `python -m unittest` (blocked by policy) — the proven pattern is a
  static read-only review (JSON verdict) + tests run separately by Hermes/Swarm.
  Full details: `references/codex-workspace-write.md` §CODEX_HOME + §static-review.
- **opencode-go REQUIRES the `x-opencode-session` header on EVERY request** (verified
  2026-10). Without it the provider answers `HTTP 400 MissingSessionID`, and the failure
  LOOKS like a bad model slug — do NOT re-probe models for it. The opencodex relay does
  not preserve the header; inject it once with `ocx provider edit opencode-go --headers`
  (stable session id + user-agent). The relay must also be running (`ocx start`, isolated
  `OPENCODEX_HOME`) or the lane fail-closes as `CODEX_LANE_BLOCKED_PROVIDER_ROUTE`. **Start that relay
  WITH the credential exported** — read `OPENCODE_GO_API_KEY` out of the canonical hermes `.env`
  without printing it and export it in the relay's own process environment; a relay started without it
  answers every request with `openai-chat requires a non-empty credential (authMode: key)`, which LOOKS
  like a bad key or a bad model slug but is only a missing env var in the RELAY process (the codex
  invocation's own env is irrelevant).
  Diagnosis + the three-surface route change: `references/codex-workspace-write.md`
  §session-header-and-relay.

## Step 6 — SQS canonical suite + operational canary

- Suite: `PYTHONPATH=src <python> -m unittest discover -s tests -t .` — pure stdlib +
  local `kernel.*` imports, so any Python 3.11 works. **The SQS `.venv-data` venv may have
  a broken base-interpreter path (hermes-managed generation dir removed post-reinstall);
  if so, run with `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe`**.
  Fresh count wins; record command/interpreter/count/duration/subject.
- **Missing `PYTHONPATH=src` makes the suite look REGRESSED (verified 2026-08-20):** running
  `python -m unittest discover -s tests -t .` WITHOUT `PYTHONPATH=src` surfaces import
  errors on every `tests/contract/*` module (`ModuleNotFoundError: No module named 'kernel'`)
  → a healthy 231 becomes "199 tests / 5 errors", which LOOKS like a regression. Before
  ever reporting a test-count drop, confirm the command included `PYTHONPATH=src`; the
  canonical baseline is `PYTHONPATH=src ... -m unittest discover -s tests -t .` = 231 OK
  (plus any new suites this run added).
- Operational canary: exercise the real kernel surface read-only (fsdt
  validate_contract/normalize/pit_validate/compute_value → temporal bind_clocks/quality_pass
  → risk limits/guards posture → harness dispatch/handoff → capability designate/qualify/finalize
  → deterministic replay). Dataclass field names are strict — read them from source before
  writing fixtures (e.g. `admission_status` not `state`, `stop_condition` must be exactly
  `"deterministic"`, qualification needs a non-empty `exit_manifest`).
- No-live-write proof: no broker adapter file, `no_broker_write: true` in handoff pack,
  negative invariants all 0.

## Long background acquisitions: progress watchdog + mid-run spot check

Verified 2026-08-13 on WO-RP2-DAILY-001 (~10k HTTP fetches, ~30-45 min background run).

- **Cron watchdog (no_agent=True, zero LLM cost):** script reads the run log each tick —
  running → print one progress line (delivered every tick); `SUMMARY` line seen → print the
  final summary once, write a marker file, then exit silently (watchdog pattern); `EXIT=`
  without a summary → print the tail once + marker. Bounded `repeat` (e.g. 14 × 5m covers
  70 min) so the job self-terminates.
- **Delivery caveat (desktop/CLI sessions):** scheduled cron ticks save to the cron log
  (`deliver=local` — no live push channel), so they will NOT appear in the chat; but
  `cronjob(action='run')` output DOES re-enter the conversation, and a terminal
  `background=true, notify_on_complete=true` process also re-enters on completion. Tell the
  user both paths up front.
- **Mid-run conformance spot check (don't wait for completion):** while the download runs,
  verify the raw layer against the blueprint — expected artifact count = symbols × months
  (+1 per Yahoo symbol), schema incl. all PIT columns, sample symbol's min/max dates and
  first-row OHLC plausibility, provider/venue distribution so far, receipts = artifacts 1:1.
  This catches layer-schema or provenance drift hours before the final check.
- Detect a stalled run by artifact/receipt growth (not `ps` — git-bash background `pid` ≠
  Windows python pid); if 0 artifacts after 2 min, bisect by importing the module and
  calling the per-item function single-threaded (see the concurrency pitfall above).
- **Progress reporting style (user preference, verified 2026-08-13):** between phases the
  user wants 白話 plain-language progress reports — % done, what is running, and explicitly
  "what we are waiting on" (e.g. "剩下 19 檔 + 全量重建，約 10 分鐘") — NOT contract-format
  output mid-run. Contract-format finals come only at the end. Plain-language answers to
  "白話簡述目前進度" / "回報進度" / "我們在等待啥?" are expected; keep tables small.

## Step 6B — EVIDENCE HOME RULE: every team keeps its evidence in its OWN folder (user-mandated 2026-08-14, FAR-investigated)

**GOVERNANCE RULE (prevents cross-project recurrence):** every Shared Infrastructure
Profile Team (FDA/FAR class) MUST keep its own `evidence/` collection layer inside its
own team folder — receipts, evidence MD, EvidenceManifest, single external-review MD.
`Fabric|HGK|SQS evidence\review\` stays the MIRROR root (byte-identical copies), never
the primary home.

Why (verified 2026-08-14 FAR investigation, FDA case):
- FAR (`fabric-autonomous-research/evidence/` + `evidence-bundle/`) and SQS
  (`SQS-THC/evidence/` with gates/readback/review) BOTH keep evidence in-team; FDA was
  the outlier (evidence scattered across `Fabric/evidence/review/`) — architectural
  inconsistency across sibling teams.
- External reviewers failed FDA 2× on "raw bundle not submitted" — root cause: evidence
  living outside the team folder makes packaging/attaching error-prone.
- Blueprint had NO rule for evidence location → execution drift.

MANDATORY STRUCTURE for every team folder:
```
<team>/
├── evidence/
│   ├── receipts/                    (runtime receipts, one per action/qualification)
│   ├── FDA_IMPLEMENTATION_EVIDENCE.md   (single evidence reducer — SOURCE of truth)
│   ├── FDA_EVIDENCE_MANIFEST.json   (loop-free manifest; rows exclude MD+self)
│   └── FDA_EXTERNAL_SINGLE_EVIDENCE_*.md (fully-embedded external review MD)
├── governance/                      (contracts/dispositions)
├── <product code + TEAM.md + matrix + tests>
└── Fabric|HGK|SQS evidence\review\  (MIRROR ONLY, byte-identical)
```
Checklist when landing a NEW team or reorganizing an existing one:
1. team folder has `evidence/` (receipts + reducer + manifest + single-MD) as PRIMARY home
2. `evidence\review\` mirrors are byte-identical copies, never the only copy
3. checker/reducer path references point into the team folder, not Fabric root
4. external submission = package the team's own `evidence/` (+ mirrors for readback)
5. **PRIMARY-HOME GATE (FAR root-cause 2026-08-14, RR5 repeat violation):** after ANY
   evidence artifact is generated, verify a byte-identical PRIMARY copy exists in the
   team's own `evidence/` BEFORE declaring done. Generator/packer scripts MUST write
   OUT to `TEAM/evidence/` FIRST, then mirror to review roots — never the reverse.
   Root cause of the RR5 violation: the packer hard-coded OUT to
   `Fabric\evidence\review\` and 5 evidence files (RR3 single-MD, RR5 raw-MD,
   re-review MD, full evidence, user guide) landed outside the team folder even
   though Step 6B existed. Detect with:
   `for f in <evidence file>; do [ -f <TEAM>/evidence/$f ] || echo VIOLATION; done`
   The packer reference (`references/pack_external_single_md.py`) now writes to
   TEAM/evidence FIRST (see its OUT config) — copy that pattern to any new packer.

## Step 6C — EXTERNAL-REVIEW SINGLE-MD MANDATORY ROUTE (user-mandated 2026-08-14)

## Step 6D — EVIDENCE CLOSURE PIPELINE: machine-generated, freeze-order-enforced (FAR self-evolution 2026-08-14, RR4 root-cause)
> 證據閉環 pipeline（freeze-order 證據生成）→ 載入 `references/step-6d-evidence-closure-pipeline.md`。
> （2026-08-15 拆分搬移，原文 bytes 未改動。）
> **AO 回 PARTIAL 後的 post-seal 修正**（編輯證據 MD → 重鏡像三根 + 重綁 spine hash；勿在 AO 驗證前預寫
> "→ PASS"；AO 可能用 md5 你可用 sha256，先比 bytes）→ 同檔 **POST-SEAL AMENDMENT** 一節（2026-08-20 三輪 AO dance）。

## Step 10A — Upgrade/self-evolution proposal routing: FAR research gate FIRST (user-mandated 2026-08-14, UD-FAR-RESEARCH-GATE-2026-08-14-001)

> **Scope (user 2026-08-14):** 「提案」= 方向選擇 / 選項 A/B/C/D / 修補方案 / 升級建議 — 任何呈報用戶決策的內容都先過 Gate 1；純呈報選項 ≠ 免研究。

**HARD ROUTE (trigger: ANY upgrade / patch / self-evolution proposal — FDA/FAR/SQS/HGK
alike, including skill self-upgrades):**

1. **Gate 1 — FAR research FIRST (mandatory, never skip):** run the proposal through
   FAR research execution (fresh research lanes ≤3 concurrent → re-survey the CURRENT
   on-disk assets + callable skills → gap analysis → fresh-context challenge lane →
   conditional closure). Output must carry evidence-backed conclusion "research
   confirms this is useful" (challenge PASS / conditions closed) before it may reach
   the user.
2. **Gate 2 — user submission ONLY after Gate 1 passes:** only research-confirmed
   proposals are submitted for HITL decision. Never submit an unresearched or
   research-rejected proposal to the user as a plan.
3. **Never re-install / re-probe what FDA/FAR already qualified:** first action of any
   FDA-class execution is to verify-and-CALL the existing qualified assets
   (cua-driver at `%LOCALAPPDATA%\Programs\Cua\cua-driver\bin\cua-driver.exe`,
   pywinauto in `HG-KSEOS\.venv\Lib\site-packages`, `xq_native_adapter.py` /
   `fda_router.py` / `FDA_DESKTOP_CAPABILITY_MATRIX.yaml` in
   `Fabric\fabric-desktop-automation\`, `screen_state_check.py` in this skill's
   references). Install/attempt only when preflight proves an asset absent — record a
   defect, never silently re-install. Forced route (§13/14/15 + user rule 08-14):
   anomaly → `screen_state_check.py` FIRST; input = pure messages + uia pattern +
   cua background ONLY; click_input/set_focus/send_keystrokes/foreground/pixel-first
   are PROHIBITED.
3a. **Cross-session upgrade overlap → run the integrity check FIRST (verified
   2026-08-14/15):** if another session may have touched the same domain while you
   worked (patch tool warns "file modified since last read", kanban board switched
   away, new files in references with your-domain tokens), OR the user asks whether
   their upgrade survived / was overwritten / regressed — run the cross-session
   integrity method BEFORE claiming any status: `references/cross-session-integrity.md`
   (per-item PRESERVED/OVERWRITTEN/REGRESSED/PARTIAL verdicts, status-marker
   discipline D1/B1 lessons, relationship classification, HITL response options
   A/B/C/D, rename-sync + two-phase-sequence construction details). Never assert
   "done"/"not done" without re-reading on-disk bytes at claim time.
4. Exception: emergency security repairs may ship a smallest patch while research
   runs in parallel, but the final upgrade plan still needs user decision.
5. Record the route application: WO id, decision id, research lane receipts, plan MD.

## Step 8 — A-3-class operability ChangeSet: evolution canary + cold-start canaries

For docs/Skill/README ChangeSets that include a governed self-evolution canary
(verified end-to-end on A-3, 2026-08-12):

1. **Gate A3-0 (compiler contract)**: run the construction-acceptance-prompt-compiler's
   deterministic functions on a task contract — see
   `references/capc-contract-building.md` for the schema traps that block
   lint/activation/acceptance PASS.
2. **Evolution chain** (typed `GovernedEvolutionController`, class name, not
   `EvolutionController`):
   `evolution signal` (signal_type MUST be in GAP_TYPES: KNOWLEDGE_GAP..POLICY_GAP)
   → `evolution candidate` (type MUST be in CANDIDATE_TYPES: KnowledgeCandidate..
   DocumentationCandidate) → `qualify(...)` (all 7 pass flags; forbidden-write set is
   auto-extended with frozen surfaces incl. the HGK User Guide — the candidate may NOT
   write the guide; that path belongs to the WorkOrder) → `independent_check(checker≠maker)`
   → `promotion_gate(human_approval=None)` → `PROMOTION_READY_HITL_SOURCE_REQUIRED`
   (COV-11-06 human gate; do NOT self-promote; PROMOTION_READY_HITL is the governed PASS).
3. **Cold-start canaries**: fresh-session `delegate_task` leaves (NO conversation history)
   given ONLY the repo root + README/AGENTS/User Guide; assert they derive role/identity/
   binding/doctor/admission/auto-route/claim-ceiling (HGK) and governance/truth-owner/
   NO-LIVE-WRITE/route/ceiling (SQS); plus a skill canary that loads the upgraded SKILL.md
   and emits a THIN prompt (no RBWI/WP restatement, no invented state). Extract full JSON
   from the delegation summary files at
   `...\hermes\cache\delegation\subagent-summary-<task>-<ts>.txt` (the live .log lines are
   truncated).
4. **External-environment regressions**: if the doctor/state regresses mid-task, AUDIT all
   agent command logs (codex exec logs + canary transcripts) for destructive commands
   BEFORE attributing; user-owned moves (e.g. relocating a gitignored dir) are not A-3
   defects — record them with the exact new location and do NOT "fix" user-owned state.

## Pitfalls checklist
> 任何異常/錯誤排查、操作失敗、守則違反疑慮 → 先載入 `references/step-pitfalls-checklist.md` 再動手。
> 兩個同層級外部 challenge report 對同一 tuple 給出相反結論（如 PASS vs S3 blocker）→ 先載入
> `references/equal-rank-external-conflict-adjudication.md`：以 exact-bytes repro + 凍結 canonical
> authority 定案，選 pick-a-report 前先質疑（Branch A/B/TEMP_CLOSED）。
> （2026-08-15 拆分搬移，原文 bytes 未改動；完整 40+ 條目見該檔。）


<!-- END SLICE 3 -->

<!-- BEGIN SLICE 5 src[103288,105116) sha256=dc1b5e15a5f6ad68cef958975ed3ee66f1fdf909678685e683ec89618e0e0ffb -->
### Step 9 操作細節（Fabric profile / cua items）→ 載入 `references/step-9-fda-cua-operations.md`（2026-08-15 拆分搬移，原文 bytes 未改動）。

## Step 9A — Shared Infrastructure Profile Team blueprint implementation (FDA/FAR class, verified 2026-08-13)

Second full landing (fabric-autonomous-research r2) after FDA. Recurring shape:
blueprint with its own WO batches (FAR-WO-001..008) + local gates (FAR-Q0..Q10/R1) →
admit ONE WorkOrder per blueprint batch (scripted, idempotent) → CAPC
NEW_IMPLEMENTATION contract (generator script, not hand-written) → Codex spawns per
deliverable batch → R0-R8-style product canary with real digests → ARIS-style method
pack pin → long-horizon detach/reattach canary → governed-evolution canary (stops at
PROMOTION_READY_HITL_SOURCE_REQUIRED) → swarm dual-lane Q10 → single evidence MD →
mirror 3 roots. Full recipe + CAPC unblock list + freeze-order traps:
`references/shared-infra-team-implementation.md`.
- First-use dogfood / self-upgrade convention (§10 of the reference, verified
  FAR-20260813-002): after a capability lands, use it to research its own improvement
  (R0-R8 run → challenge lane → HITL gate → patch → verify). Future self-upgrade /
  self-evolution requests follow this same governed process.

## Step 10 — External provider-tool governed enablement (P0-TOOL registry class, verified 2026-08-13 WO-HGK-GENIE-PREDESIGN-001)
> P0-TOOL registry 受治理啟用 → 載入 `references/step-10-external-provider-tool-enablement.md`。
> （2026-08-15 拆分搬移，原文 bytes 未改動。）

## Support files
> 查詢所有 references 支援檔說明 → 載入 `references/support-files-index.md`。
> （2026-08-15 拆分搬移，原文 bytes 未改動；完整索引見該檔。）


<!-- END SLICE 5 -->
