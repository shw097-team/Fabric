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

## Verification status

- Every decisive claim was **re-derived by the orchestrator**, not accepted from a child's summary: the 2×2
  failure matrix, the two-hunk acceptance pair, the three mutation probes, the C6 defect and its successor
  measurement, the drift call, the PKG byte-interval quotes, and the harness's own reporting defect.
- The independent VERIFY/SECURITY lane runs with the **mandated arm pinned at rank 1**
  (`dispatch_r9.py --force-rank 1 --require-arm openai-codex/gpt-6.1-sol`); if that arm is unavailable the
  dispatcher fail-closes rather than silently serving the backup, which is how the R8 provenance defect arose.
- A green harness is a **machine gate**: it is not an acceptance and it does not clear the 221 planned cases,
  the eight Gates, Fresh G1 or the external report's `FAIL_CLOSED` production decision.

## Open owner actions

1. complete the successor overlay's own gate result and the candidate's canonical-accept policy (OQ-05);
2. apply the already-proposed PLAN-route rebind (`hgk-far-remediation-20261016` R1) (OQ-01);
3. decide the checker identity / governed write root (EIA-R6-03) (OQ-02);
4. fix the lifecycle taskspec-id derivation (OQ-06);
5. decide the 221-case applicability owner and source #6's status (OQ-03, OQ-04);
6. dispatcher: populate the served arm on a nonce-failed turn (EV-01).
