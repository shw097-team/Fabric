# R8_VERIFY_RECEIPT — Round CNV-PIPD-LS-SP-20261015 / ChangeSet R8-0

**Independent Verifier:** local, non-authoritative. **Claim ceiling: LOCAL / candidate-only.** This receipt is
not an acceptance, not an approval, not a Gate PASS, and not a product statement. It records what was
independently re-measured, what could not be re-measured, and any counterexamples found.

**Write root:** `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/R8_VERIFY/` (writes confined here).

## Subjects read

- Applied canonical tree (read-only): `.../hermes/skills/software-development/adversarial-verification-rounds/`
- Pre-image: `CNV-PIPD-LS-SP-20261015-R8/WS_A/apply/preimage/`
- Candidate HGK tree: `.../HG-KSEOS/var/SKILL-CONVERGENCE-20261014/candidates/hgk/skill`
- Live canonical HGK tree: `.../hermes/skills/software-development/hgk-governed-execution/`
- PIPD worktree: `C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt` at `dba4b19456777d3b597fdf71480f6423dd974243` (detached)
- Reference R7 patch: `CNV-PIPD-LS-SP-20261015-R7/R7_VALIDATOR_DIFF.patch`
- Reference R7 mutations: `CNV-PIPD-LS-SP-20261015-R7/R7_MUTATIONS_18_RERUN.json`

## WS-A — what was independently re-measured

| # | Claim | Result | Basis |
|---|---|---|---|
| 1 | Main-file byte budget + frontmatter identity | **CONFIRMED** | Recomputed size = 21,332 bytes (cap = 100,000). Name, description, frontmatter at byte 0 all match the live skill. |
| 2 | No instructional content lost; every reference's bytes survive | **CONFIRMED** | Maker harness (run independently): `lost_lines=0`, `live_references=25`, `byte_identical=19`, `absorbed_but_present_verbatim=6`, `lost=0` (C4/C6 all PASS). |
| 3 | Apply receipt before/after table consistency | **CONFIRMED** | Recomputed all 31 receipt rows against the pre-image / repaired_candidate / live bytes. No sha or byte-count mismatch. |
| 4 | Rollback script restores pre-image byte-for-byte | **CONFIRMED** (review only; not executed) | Code review: `replaced` rows → write preimage bytes, verify sha256 == `before_sha256`; `added` rows → delete; `retained_untouched` → no action. Behavior matches the verified receipt table exactly. |
| 5 | HGK candidate was NOT applied and why | **CONFIRMED** | Live tree holds 126 files vs candidate 109 with 21 divergences. The two loss files genuinely do not survive in the candidate: `lane-conformance-gate.md` (live 3,299 B, sha `77e8b77164c0f0d3...`) is absent; `step-verify-only-lane.md` (live 7,994 B, sha `d8e7f1a561551fce...`) appears as a 6,029-byte rewrite. |

## WS-A — counterexample / discrepancy note

- The WS-A harness's `subject_live` field is written with the WRONG path
  (points to `adversarial-verification-rounds` when I feed it the HGK tree). The C2 loader
  identity check still resolves correctly, and the C6 verdict (`FAIL`, 2 lost refs) is
  reproduced by independent file-tree comparison. This does not affect the loss determination,
  but it means the harness writer conflated `subject_live` with `subject_candidate` in this
  configuration — worth fixing if the harness is reused.

## WS-B — what was independently re-measured

| # | Claim | Result | Basis |
|---|---|---|---|
| 1 | Rebased files differ from `main` only in the hardening's own hunks | **CONFIRMED** | Line-level diff of the worktree diff against the R7 patch: 203 injected lines identical (203 in, 203 out) except ONE line — `cli.py` uses `schemas_dir` (registry-resolved) instead of R7's `root / "schemas"`. 11 hunks in 3 files; +203/−6 total. |
| 2 | `post/{validate,pipeline,cli}.py` sha256s | **CONFIRMED** | All three match the maker's recorded prefixes: `f8ea6c6be15db358`, `9e9f6ab02e385a7b`, `6ee1cca26e4f5b15`. |
| 3 | Test-suite summary reproduced | **CONFIRMED** | Own run: `2 failed, 609 passed, 20 skipped, 62 subtests passed in 206.15s`. Same counterexample: `test_real_trace_link_is_legal_beside_its_endpoints` and `test_cli_smoke_runs` fail. They pass on clean `main` (verified by overlay test) — i.e., they are pre-existing on `main`, not caused by the hardening port. |
| 4 | 18-mutation table: M04/M06/M16 REJECT + previously-detected stay detected + NOT_RUN has real reason | **CONFIRMED** | Independently re-ran M04, M06, M16 (all `REJECT`, validator_verdict=FAIL, first_fail = "content_hash does not match the record body ..."). Cross-checked all 18 rows against both the maker's table and the R7 rerun: 10 detected / 8 NOT_RUN, each NOT_RUN row carrying a concrete evidence-class reason. |
| 5 | Runner adaptation is constants-only | **CONFIRMED** | Diff vs R6 originals shows only 6 lines total across 3 files, all constant reassignments (`PIPD_SRC`, `SCHEMAS`, `RAW ×2`, `ROOT`). No logic changes. |

## Reproduced raw outputs (own run)

```
pytest (r8_worktree):
2 failed, 609 passed, 20 skipped, 62 subtests passed in 206.15s (0:03:26)
FAILED tests/test_s4ext_trace_closure.py::LegalTraceStillPassesTests::test_real_trace_link_is_legal_beside_its_endpoints
FAILED tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs

m04:  observed=REJECT  validator_verdict=FAIL  first_fail="ProfileBinding: content_hash does not match the record body (body edited without re-issuing identity)"
m06:  observed=REJECT  validator_verdict=FAIL  first_fail="RequirementAtom: content_hash does not match the record body (body edited without re-issuing identity)"
m16:  observed=REJECT  validator_verdict=FAIL  first_fail="TraceLink: content_hash does not match the record body (body edited without re-issuing identity)"
```

## Counterexamples and findings

1. **Harness `subject_live` conflation** (WS-A). Cosmetic but worth fixing. Does not change the loss determination.
2. **Two tests fail on `main` after the port** (WS-B). Reproduced as stated; both pass cleanly on clean `main`. Root causes are as described in `WS_B/WS_B_RECEIPT.md` §4. Honest partial, as the maker recorded.
3. **The rebase adds up to the R7 target** (WS-B). Line-level comparison shows the R7 delta is applied verbatim except for the `cli.py` path resolution; no extra semantics entered. No undocumented substitution.

## What was NOT re-measured (and why)

- The 221 acceptance cases — explicitly out of scope by the brief.
- The R7 `main` test baseline (`7 failed, 319 passed, 2 skipped, 34 subtests passed`) — that is a baseline of
  a different (older) base tree, directly compared by the maker. Not re-measured this turn.
- The rollback drill against a scratch copy — skipped because the receipt table was verified by hash
  recomputation rather than a live drill. Reasonable by the brief's own framing ("reason about it from the code").

## Verdict type

Per-claim independent verification. No acceptance, no approval, no Gate PASS, no product claim,
and no upgrade of the claim ceiling. **Claim ceiling: LOCAL / candidate-only.**
