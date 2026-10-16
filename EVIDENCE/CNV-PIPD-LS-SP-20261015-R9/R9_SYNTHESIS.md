# R9-0 synthesis — FAR residual closure (candidate-only)

Mission `CNV-PIPD-LS-SP-20261015` · ChangeSet `R9-0-FAR-RESIDUAL-CLOSURE` · HGK project `CNV-R9-FARCLOSURE` ·
FAR run `FAR-20261016-012-r9-residual-closure` (route `FAR_ROUTE_NATIVE_ARIS`) · board `r9-far-residual-closure-20261016`.
**Claim ceiling: LOCAL / candidate-only.** No acceptance, no Gate PASS, no AO verdict, no release.

## What was executed

| # | item | outcome | evidence |
|---|---|---|---|
| 1 | R8-0 validator adaptation (`BLK-R8-WS2`) | **EXECUTED** — two hunks confined to `validate.py`; the two named tests pass and the M04/M06/M16 mutations still REJECT | WS_A/WS_R9A_RECEIPT.json, WS_A/probe_m0{4,6}.stdout.txt, WS_A/validate_py_r8wt_vs_main.diff |
| 2 | slim `hgk-governed-execution` candidate (`R8-F5`) | **EXECUTED + APPLIED** — guarded overlay, zero deletions; canonical `SKILL.md` 105,116 → 21,026 bytes; C1–C6 PASS; rollback drilled; loader `enabled` | WS_B/WS_R9B_RECEIPT.json, WS_B/WS_R9B_RAW.md, WS_B/own/orchestrator_post_apply_gate.json |
| 3 | FAR run 012 decision surface | **EXECUTED** — 21 contract-conformant artifacts incl. rejected-alternative and open-question ledgers | FAR/ run directory |
| 4 | OPENSPEC | **EXECUTED** — `openspec validate hgk-r9-far-residual-closure-20261016 --strict` → valid | openspec changes dir |
| 5 | owner decisions | **PREPARED** — three one-action records + the PKG alignment record | R9_OWNER_READY_*.json, PKG_ALIGNMENT_R9.json |

## What this round corrected about itself

- `R8-F7` **resolved** by the package's own wording: `ACC-RQ06` names "AVR/10-piece" and "HGK/6-piece" byte
  reconstruction; HGK measures exactly 6 slices, AVR carries 10 markers.
- `R8-F4` **recalibrated**: the PKG contains no size cap; the platform limit is `MAX_SKILL_CONTENT_CHARS`
  (100,000) enforced on the LF-normalized `len()`, and the R8 harness had recorded **bytes**.
- `R8-F6`/`R9-D1` **withdrawn as stated**: `check_drift(registry=load_registry())` returns `[]`. The surviving
  fact is that the canonical `routes[].PLAN` row disagrees with the pool, the file's own SoD text and today's
  mandate — already registered by the stack as `F1-PLAN-ROUTE-ROW-OUTLIER` and already proposed as
  `hgk-far-remediation-20261016` R1 (so it was cited, not duplicated).
- `TF-06` **closed with a corrected reading**: attribution is recoverable from the receipt's `attempts[]`; the
  missing nonce voids completion attestation only.
- New this round: `R9-F1` (lifecycle taskspec-id collision), `R9-F6` (harness records `subject_live` before
  honouring `--live`), `R9-F7` (the FAR repair's live-reference denominator was one file short), `R9-F8` (the
  round's dispatch wrapper pinned the checker to its backup arm, so the mandated rank-1 checker never ran).

## Corrections the independent checker forced on this round

- **Package byte count**: recorded 2,580,690; the file measures **2,689,181** (sha256 unchanged). Corrected in three
  artifacts (R9-F10).
- **The PLAN route is no longer the one this round measured**: it was rebound to `openai-codex/gpt-6.1-sol` by an
  act **outside** this round at 2026-10-16T12:36:30 (epoch 21). The prepared handover is therefore already applied;
  this round neither performed nor claims it (R9-F12).
- **Two defects in this round's own verifier brief**: it named a FAR path that does not exist (`FABRIC/` segment)
  and asked for an `evidence_ref` column the FAR contract does not define. The checker refused to substitute
  silently; the brief is kept with the note rather than rewritten.
- **Precision on the diff**: the `r8-wt` delta against `dba4b19` includes `cli.py` and `pipeline.py` from the R8-0
  hardening; only this round's two guard blocks are confined to `validate.py`.
- **The checker's own nonconformance**, self-reported: its first test invocation wrote fixtures under the default
  TEMP instead of its write root. Recorded verbatim; no process-purity claim is made for that run.

## Verification status

- Every decisive claim was **re-derived by the orchestrator**, not accepted from a child's summary: the 2×2
  failure matrix, the two-hunk acceptance pair, the three mutation probes, the C6 defect and its successor
  measurement, the drift call, the PKG byte-interval quotes, and the harness's own reporting defect.
- The independent VERIFY/SECURITY lane runs with the **mandated arm pinned at rank 1**
  (`dispatch_r9.py --force-rank 1 --require-arm openai-codex/gpt-6.1-sol`); if that arm is unavailable the
  dispatcher fail-closes rather than silently serving the backup, which is how the R8 provenance defect arose.
- The independent checker's **overall is UNVERIFIABLE**: 2 of its 7 claims are CONFIRMED and 4 findings forced
  corrections here; it could not re-run the round's named two-test pair because that fixture creates a git
  repository and its own guard forbids git writes (it ran a disclosed adapted fixture instead), and it could not
  attribute its own serving arm at verdict time. Nothing is upgraded on the strength of its 4 confirmations.
- The R9 checker turn was served by **rank 1 `openai-codex/gpt-6.1-sol`** (768.19 s), i.e. the mandated checker
  actually ran this round's verification, unlike R8 where the wrapper pinned the backup arm.
- A green harness is a **machine gate**: it is not an acceptance and it does not clear the 221 planned cases,
  the eight Gates, Fresh G1 or the external report's `FAIL_CLOSED` production decision.

## Open owner actions

1. complete the successor overlay's own gate result and the candidate's canonical-accept policy (OQ-05);
2. apply the already-proposed PLAN-route rebind (`hgk-far-remediation-20261016` R1) (OQ-01);
3. decide the checker identity / governed write root (EIA-R6-03) (OQ-02);
4. fix the lifecycle taskspec-id derivation (OQ-06);
5. decide the 221-case applicability owner and source #6's status (OQ-03, OQ-04);
6. dispatcher: populate the served arm on a nonce-failed turn (EV-01).
