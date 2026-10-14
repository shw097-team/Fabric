## Support files

- `references/cross-session-integrity.md` — cross-session upgrade integrity CANONICAL recipe (consolidated 2026-08-15 from 2 parallel drafts, verified 2026-08-14 FDA U1-U5 vs RR6-RR8): when-to-use triggers (user asks "was my upgrade overwritten/regressed?", patch-tool modified-warning, challenge FAIL on status claim), read-only other-session inventory (git log/show/diff/receipts/skill-layer), relationship classification (conflict/complement/supersede/Do-NOT-letter-vs-spirit, dual-tool collision taxonomy), per-item survival verdicts (PRESERVED/OVERWRITTEN/REGRESSED/PARTIAL with path+line+mtime evidence, run-artifact proof), status-marker discipline (D1/B1 FAIL_CHALLENGE lessons: claimed status must equal on-disk bytes, patch-warning = mandatory re-verify, no CLOSED-without-pending, fix MD not verdict), HITL response options A/B/C/D (B+D recommended pattern), rename-sync step-by-step + two-phase-sequence construction details, pitfalls (stale grep counts, receipt field inconsistency, CRLF path-split bytes-fix), preflight-gate construction appendix. Pre/post pair with the "Parallel-session skill-dir drift" pitfall (pre-build) — this file is post-build.
- `references/opencodex-human-home-hijack-restore.md` — opencodex (ocx) human-home hijack CANONICAL recipe (consolidated 2026-08-15 from 3 parallel drafts): diagnosis route, ocx CLI surface, minimal restore 方案A (CRLF/RFC3339 traps), HGK-lane isolation, route re-verification after Probe (daemon-stop trap, ERR_CODEX_ROUTE_EXIT_ false alarm), FAR daemon 常駐 vs on-demand 判定.
- `references/hermes-memory-full-handling.md` — Hermes persistent memory full (MEMORY.md
  95%+) handling recipe (verified 2026-08-14 WO-HGK-MEM-RESEARCH-001): mechanism facts
  (no auto-compact, §-delim, frozen snapshot, drift guard, apply_batch, 3-attempt fuse),
  config keys (memory_char_limit tunable; flush_min_turns = dead key), official full-load
  paths, DOC-11 governance mapping (state→WorkOrder, skills dedup ≠ promotion), P0
  classify→prune→verify recipe, and the proof that FABRIC already has a cross-session
  retrieval layer (spine knowledge_fts 354 docs + FAR tri-source + 知識庫 9,706 md +
  session_search) so external providers are NOT a memory-full remedy.
- `references/external-provider-tool-enablement.md` — external provider-tool governed enablement (TOOL-24 class, mattpocock-skills canary 2026-08-13): registry-vs-install ground truth, upstream identity/tags, shallow-clone pin, Hermes vendor-category install, loader verification, USER_DECISION freeze, registry-honesty non-claims, grilling design-discussion method.
- `references/predesign-design-discussion.md` — pre-implementation design discussion under HGK governance (GENIE vNext case 2026-08-14): 文檔工廠 (Spec-Driven Document Factory) mode contract, grilling design-tree rounds (❓+➡️ frontier, user's 照建議 wholesale-adoption pattern), fact-lane patterns (old-stack inventory / hot-OSS GitHub API scan / capability matrix), gap-matrix methodology (landed/partial/gap with file citations) + today-lens FAR re-research when new corpora land (supersede/extend/orthogonal), close-out contract per round.
- `references/oss-landscape-research.md` — FAR research EXECUTION mechanics (2026-08-14): ≤3-lane batching + single-task `goal`+`context` form (tasks array rejects 1 item), GitHub unauth rate-limit fallbacks (shields.io badges / commits.atom / HTML aria-label / raw READMEs), challenge-lane conditional closure (PASS_CHALLENGE → close every condition + artifact version bump), new-corpus SUPERSEDES/EXTENDS/ORTHOGONAL re-classification, product-lane landing judgment (✅已落地/✅大部分/⚠️部分/❌自建 per lane).
- `references/fda-desktop-automation-cua.md` — Cua install/daemon/call recipes, live
  fixture 10/10 qualification, XQ version readback, matrix promotion, evidence-MD
  self-reference fix, delivery_mode=background rules (§11), Afx Win32-dialog
  interaction matrix (§12), mouse-free pywinauto recipe + XQ radar control-ID
  tables + big5 SensorList.sqlite DB location (§13).
  **FDA 完整使用手冊：`Fabric/fabric-desktop-automation/FDA_USER_GUIDE.md`**
  （12 章節：架構/安裝/action-class/運算子操作/資格化/驗收/治理/疑難排解/FAQ；4-way mirror）。
- `references/fda-folder-reorganization.md` — FDA/FAR profile-team folder tidy-up recipe
  (verified 2026-08-14): root-vs-receipts-vs-governance classification, snapshot-hash →
  move → hash-stable verify, checker path patch + EvidenceManifest path update, reorg
  receipt + directory tree + 3-root mirror. Recurring user request (「檔案很雜亂」— FAR then FDA).
- `references/fda-upgrade-research-2026-08-14.md` — FDA upgrade/patch research under the
  FAR-gate route (WO-HGK-FDA-UPGRADE-RESEARCH-001, UD-FAR-RESEARCH-GATE-2026-08-14-001):
  root cause "prose rules fail at execution", verified asset state (4/5 CUA QUALIFIED,
  T170 no-mouse lock), known-gaps inventory (router-not-wired-to-matrix, stale
  CLOSURE_V8 ref, version drift, UFO2 over-claim, 64/64 unreproducible, T170 narrow
  coverage), upgrade plan v1 (U1 fda_preflight.py / U2 Step 9-0 / U3 screen_state_check
  only-entry / U4 prose fix / U5 record-only), frozen-asset do-NOT list, verification
  recipe (checker 179/179 unchanged, 3-state preflight test, cold-start canary).
 DoD-17 closure detail (2026-08-14, WO-FDA-XQ-002) incl. **fsState readback
 semantics correction** (`fsState & 4` enabled = execution truth; `& 2` pressed =
 XTP visual, NOT reliable), **模組訂閱 gate** (個人版策略雷達=盤中量化交易模組;
 台股進階不含 → 自訂策略不持久化執行 → DoD-17 =
 RUNTIME_QUALIFIED_AUTOMATION / EXECUTION_BLOCKED_SUBSCRIPTION; **訂閱後閉合** —
 SensorLog `DAQXQLITE_SHW097_SensorLog.sqlite` Table_YYYYMMDD = 執行真相層，
 56 筆狀態機紀錄 (XSSensorState 2→3→1 / ExecState 1→8)，「新增成功」dialog
 偽裝成 `時間：[HH:MM:SS]` 時鐘窗陷阱，加入=自動執行), SensorList big5
 decoding, Win32 message details (WM_SETTEXT return 0 is normal; PostMessage+
 ctypes buffer GC bug), CEF dialog Enter-close, startswith window-match pitfall:
 `references/xq-radar-paper-runtime.md`.
- `references/xq-community-automation-solution.md` — community XQ automation repo
  (would2000/XQ-Auto-Writer-Skill, live-verified XQ 3.19.03): strategy-radar toolbar
  command IDs (NEW 17551 / START 17554 / STOP 17555 / COPY 17627 / DELETE 17553),
  dialog control IDs (name 17500, script 17202, product 17107, trigger combo 17035,
  toolbar 59392, search 33005), pywinauto dual-backend rules + 3.20.02 UIA-deadlock
  workarounds, Scintilla SCI_SETTEXT editor write (bypasses UIPI), start/verify
  green-light pattern, red/green trigger pair, parameterized alert-script template.
- `references/external-challenge-review-closure.md` — FDA external-challenge closure
  (EXT-FDA-001..008): subject-root via git commits, raw review bundle + EvidenceManifest,
  checker-denominator single value, DoD-36 machine matrix, UFO² keyless effective-load
  (opencode-go/Ollama/PlaceHolderService), XQ radar trial-mode limits.

- `references/shared-spine-admission.md` — typed SharedSpine WorkOrder admission sequence.
- `references/codex-canary-powershell.md` — sealed Codex lane invocation + PowerShell
  capture pitfalls (Start-Process ExitCode, UTF-16, EAP, NDJSON parsing).
- `references/codex-workspace-write.md` — why `workspace-write` is forced read-only on the
  sealed lane, the 10-probe investigation, and the validated `danger-full-access` write
  pattern with process-boundary safety.
- `references/capc-contract-building.md` — building a construction-acceptance-prompt-compiler
  contract that passes lint/activation/acceptance (schema + semantic traps).
- `references/final-closure-resume.md` — thin post-acceptance closure rounds (F01-F07):
  doctor repair via WorkOrder+Codex, WorkOrder normative readback, docs/AGENTS currentness
  defect classes, isolated-worktree equivalence requalification, evolution HITL gate
  (stop + resume token), and deferred evidence reseal.
- `references/external-evidence-closure.md` — EVIDENCE_ONLY Contract A closure after an
  external PARTIAL_CHALLENGE: R1-R8 recipe (freeze-order, single-direction hash binding,
  single-MD FULL inline raw content, canonical single-hash-per-path audit, wrapper-MD
  self-exclusion, subject-bound negative side-effect receipt, `all(v is True)` trap,
  spine-capture vs EVD timing).
- `references/external-challenge-evidence-closure-far.md` — FAR closure round
  (EXT-FAR-001..010): subject-root manifest (merkle, self-excluded), evidence manifest
  root, 49-file raw bundle, closure receipts per finding (hyphen names), fresh-AO
  subject-binding, Q4 real-invocation receipt, T001..T092 crosswalk, separate-ChangeSet
  freeze, single-zip review package; plus the evidence-MD generator hygiene traps
  (None grep, row-count verify, unittest-stderr capture).
- `references/external-acceptance-single-md-closure.md` — condensed r1→r7 single-MD closure recipe (see external-evidence-closure.md R7/R8 for overlap).
- `references/post-acceptance-subject-hygiene.md` — post-acceptance evidence immutability
  (verified 2026-08-13 FAR): NEVER modify a signed evidence MD at its canonical path;
  re-freeze resolution (archive bytes → regenerate → mirror ×4 → sweep ALL hash refs
  short+full forms → FAR_R8_HISTORICAL_BASELINE.md supersession chain → superseding EVD);
  byte-exact restoration traps (dynamic generator timestamps, evolved embedded sources —
  abandon after failed timestamp brute-force); embedded-manifest freeze-loop and how to
  end it (final-freeze-then-STOP, canary artifacts copied into evidence-bundle/raw-canary/
  for manifest scope); re-freeze checklist.
- `references/sqs-data-plane-verification.md` — SQS-THC 台股歷史資料庫 cross-confirmation vs
  the Shioaji-first blueprint: data_plane four-layer layout, DSV manifest↔catalog↔receipts
  hash-consistency recipe, provider/data-policy spec values, 知識庫 legacy disambiguation
  (finmind 6.7GB / Taiwan STOCK vs governed DSV), duckdb reserved-word + pandas quirks,
  truncated-listing false-absence pitfall.
- `references/taiwan-daily-ohlcv-acquisition.md` — building the governed daily OHLCV layer
  (WO-RP2-DAILY-001): TWSE STOCK_DAY endpoint + ROC-date parsing, TPEx official unreachable
  (defect record), Yahoo `.TWO`/`.TW` fallback, market-probe routing (6xxx ≠ always TPEx),
  raw/core/duckdb/catalog pipeline + receipts idempotency, check_daily C1-C10 predicates,
  legacy CSV cross-validation oracle.
- `references/taiwan-isin-venue-master.md` — authoritative listing-venue resolution via the
  TWSE ISIN C_public.jsp master (never code-prefix inference; negative-control pattern;
  Big5 parse recipe) + the Five-Clocks conservative contract closure template
  (publication := availability := known_at, causal-ordering checker C11, same-day negative).
- `references/acceptance-verification-lane.md` — independent challenge/AO verification lane
  (VERIFY_ONLY): documented-hash vs on-disk bytes, evidence-file existence, production
  call-site grep, WO/rollback-pointer existence, empirical canary reproduction, test
  blind-spot analysis; defect classes found 2026-08-13 (stale-loop-variable on exception,
  stub-probe landmine, unreachable guard branch, dual TSV header) + exact commands and
  output shape.
- `references/python-security-review-probes.md` — Python security-review probe bank
  (WO-FAR-HARDENING-001, 2026-08-14): SSRF adversarial matrix (scheme/host-suffix/
  userinfo/IP-literal cases), 6to4/Teredo-embedded-address gap, DNS-rebinding TOCTOU,
  XML DOCTYPE-window smuggle + entity-bomb tests (expat amplification protection),
  truncation-receipt edge cases, hardening-round H-item verification (denominator
  nodeids-digest recompute, deterministic canary re-run, spine read-only URI, banned-lib
  grep semantics, mutation=0 three-layer evidence), AO verdict output format.
- `references/focused-hardening-rereview.md` — external focused RE-REVIEW of closure
  rounds (EXT-FAR-TS-HARD-001..006 closure, 2026-08-14): verify fix in source (grep +
  read class body + wiring in real call path), canary on-disk + embedded==disk JSON,
  digest recomputation recipes (nodeids sorted/as-listed join, subject-manifest sorted
  rows, on-disk vs manifest rows incl. byte counts), timestamp-monotonicity check
  (all receipt timestamps <= MD §0 generation), section-scoped JSON extraction from
  multi-```json MDs (split on `## N.` headers first), native-Windows-python path form,
  heredoc backslash mangling, LOW-vs-blocking finding classification + verdict output.
- `references/final-evidence-reseal-binding.md` — evidence-only re-seal after an
  external PARTIAL_CHALLENGE with zero product defects (EXT-FAR-TS-RE-001/002,
  2026-08-14): candidate subject manifest = code/config/runtime-contract ONLY (never
  include mutable evidence receipts — regen makes them stale), final evidence manifest
  generated AFTER all evidence bytes, single FINAL_INTAKE.json binding subject + EM +
  MD + every receipt digest (generated LAST = the loop-breaker; intake binds MD, MD
  references intake by path), drift=0 check that justifies skipping the test rerun,
  maker-side timestamp integrity (never hardcode placeholder times; local time + `Z` =
  confirmed defect; all `*_at_utc` <= MD §0), async worker-verbatim claims fidelity
  (superseding EVD `-R2`/`-R3` after receipt updates), Swarm default-on as a governed
  USER_DECISION change (contract `default_on: true` + safety invariants + real dual-lane
  fanout canary) — external reviewers accept the user decision and only check invariants.
  Also: MASTER single-evidence-MD consolidation (user asks for ONE MD for the reviewer —
  19-section master embedding intake MINUS self-binding fields; rebind intake to the
  master hash after generation; mirror ×4; superseding EVDs), accepted-MD immutability
  under NBOs (reviewer NBOs on a PASS_CHALLENGE master are archival-only — do NOT
  regenerate the signed identity), and the activation close-out round (activation
  receipt v3 + docs sweep README/AGENTS/TEAM/UserGuide + FABRIC routing update via a new
  capability-matrix execution class + directory-tree deliverable). r3 ALL-PASS closure
  (2026-08-14): reviewer falsification attempts (stale hashes/byte counts, denominator
  inflation, nodeid mismatch, future timestamps, redirect re-enabled, swarm multiple
  writers, r8 rewrite) → 0 counterexamples; NBO on the master MD §18 = the intake-file
  SHA went stale after rebinding — single-direction binding makes reverse references
  informational-only, do NOT regenerate the signed master for an NBO; CANARY-7 worker
  claims must be the workers' VERBATIM output (superseding EVD `-R2`/`-R3` after
  fidelity updates). Folder reorganization after acceptance: see the pitfalls checklist
  (frozen-identity/subject stay at root; spine EVD locator migration in backslash form).

- `references/equal-rank-external-conflict-adjudication.md` — 兩份同層級外部 challenge report 對
  同一 tuple 各執一詞時的解決程序（verified 2026-10-04 SWOF R5 local_adapter）：先凍結 exact
  subject identity、grep 凍結 canonical authority 的 literal 欄位（PI06 DOC-03 CRITICAL->AAC3）、
  全樹 reachability inventory、以真實 production caller + 有效 token 鏈做 full-route counterexample
  （含 contrast control）、再依全部 predicate 判 Branch A（最小修補，delete fallback 非 rename）/
  Branch B（無 mutation + TT-W3-boundary）/ TEMP_CLOSED。平等 rank 衝突嚴禁 pick-a-report。
- `references/repair-round-equality-and-closure.md` — R-series（SWOF W*-REPAIR wave）閉環規則：
  equal-rank 衝突以 exact-bytes repro + contrast control 決定性定案（不 pick-a-report）；closure
  ≠ commit + green tests——產品 mutation → focused/regression → FRESH checker PASS → 才做 typed HGK
  closure projection（正確 project scope 開 cone、subject-bound evidence refs、recompute source_digest
  == sha256(canonical_json(payload))、non-vacuous denominator、blocking-open==0、lifecycle→final
  checkpoint）；封存前清 stale earlier-round receipts（identity 欄位對 round，排除並揭露非靜默）；
  信任軸 checker 必須攻擊 caller-controlled selector bypass 而非只跑 AAC lattice。
- `references/external-review-evidence-packaging.md` — 外部驗收證據包八輪教訓（FDA r1→r8）：單一
  self-contained MD（宣告 SHA = reviewer 可重算的嵌 body SHA）、checker 三鐵律（chronology/duplicate-id/
  single-denominator/subject 三向）、authority-bound domain semantics、封存鏈單向（files→manifest→
  MANIFEST.sha256→SEAL，SEAL 記 expected count+bytes 抓 add-only；禁 self-referential root）、hash 對了
  ≠ 語意對（逐 item 比內部 subject identity vs manifest subject）、committed-blob hash（CRLF/LF）、
  readset 必放 repo 外（evidence_commit_sha 自指循環陷阱）、Windows 長路徑 blob-SHA readback 免疫。
- `references/external-publication-mirror.md` — 治理 workspace mirror 發佈至外部 repo：private-first、
  curated tree（每 subject assert file count，tar 而非 glob cp 防靜默掉整 subject）、secret-scan
  adjudication（real credential vs test placeholder vs bare variable NAME 三分）、remote tip readback
  （git ls-remote + recursive tree）、mirror README 必含 exclusion list + claim ceiling。
  （2026-10-04 index 補登上述三檔：內容早已存在且已路由進 SKILL.md，本索引先前漏列。）
- `references/step-pitfalls-checklist.md` — 異常/錯誤排查完整 40+ 條目（2026-08-15 拆分搬移；SKILL.md §Pitfalls checklist 指標指向）。
- `references/step-9-fda-cua-operations.md` — FDA 桌面自動化操作細節（Fabric profile / cua items 1-9+；2026-08-15 拆分搬移）。
- `references/support-files-index.md` — 本索引自身（全部支援檔說明總表；2026-08-15 拆分新增自索引條目）。
- `references/step-6d-evidence-closure-pipeline.md` — EVIDENCE CLOSURE PIPELINE（freeze-order 證據生成；2026-08-15 拆分搬移）。
- `references/step-evidence-only-contract-a.md` — EVIDENCE_ONLY Contract A 閉環（PARTIAL_CHALLENGE/EVIDENCE_GAP；2026-08-15 拆分搬移）。
- `references/step-10-external-provider-tool-enablement.md` — P0-TOOL registry 受治理啟用（2026-08-15 拆分搬移）。
- `references/step-verify-only-lane.md` — 獨立驗收/挑戰 lane（VERIFY_ONLY/AO；2026-08-15 拆分搬移）。
