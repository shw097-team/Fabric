# R9-0 mission plan — FAR residual closure (mission CNV-PIPD-LS-SP-20261015)

ChangeSet `R9-0-FAR-RESIDUAL-CLOSURE` · HGK project `CNV-R9-FARCLOSURE` (`WO-TS-FARCLOSURE-01..06`) ·
board `r9-far-residual-closure-20261016` · FAR run `FAR-20261016-012-r9-residual-closure`.
Claim ceiling **LOCAL / candidate-only**.

## Control plane
HG-KSEOS is the only control plane; Hermes is bound as its governed runtime/orchestration plane. The round's
admission is typed (`hgk_admission_r9.py`) and the lane model plan is honoured EXECUTE=`opencode-go/deepseek-v4.1-flash`,
VERIFY/SECURITY=`openai-codex/gpt-6.1-sol`; the PLAN & Orchestrator plane is bound and proven by the
`hgk-governed` profile's own session store, NOT by the canonical default profile.

## Board (KANBAN/SWARM)
| card | workstream | status |
|---|---|---|
| t_0ce1cbb9 | swarm root (SWARM graph) | done |
| t_e6fe5877 | W1 FAR run 012 | done |
| t_dd87f823 | W2 BLK-R8-WS2 validator adaptation | done |
| t_ef66297f | W3 repaired-candidate guarded apply | in flight |
| t_3047b673 | W4 owner-ready records | done |
| t_d645c403 | W5 PKG alignment | done |
| t_7bc0c046 | W6 evidence packet publication | pending |
| t_b9f2a8aa / t_02b48a10 | verifier / synthesizer | todo |

## Executed this round
1. **W2** — two-hunk adaptation in `validate.py` (worktree `r8-wt`, base `dba4b19`): derive the trace binding
   from the bundle's own atoms only when no frozen context is supplied, and guard the `risk_guard`/oracle
   mapping access. Acceptance: 2 passed / 629 deselected (orchestrator 20.26s, lane 18.49s) against 2 failed
   pre-edit; negative control M04/M06/M16 each `observed=REJECT`.
2. **W3** — guarded apply of the repaired `hgk-governed-execution` candidate. The round's own gate REFUSED the
   first candidate (C6: one live reference absent) in two independent runs (lane + orchestrator). A successor
   candidate (CANDIDATE_V2) restoring that file passes C1–C6; the apply of the successor is the open step.
3. **W1/W4/W5** — FAR run 012 artifact set, three owner-ready one-action records, PKG alignment record.
4. **OPENSPEC** — `openspec validate hgk-r9-far-residual-closure-20261016 --strict` → valid.

## Findings and corrections carried
- `R8-F7` resolved (10/6 = AVR ten pieces + HGK six pieces, per `ACC-RQ06`).
- `R8-F4` recalibrated (no PKG cap; the platform limit is `MAX_SKILL_CONTENT_CHARS` on LF-normalized `len()`).
- `R8-F6`/`R9-D1` drift claim withdrawn (`check_drift` = `[]`); the surviving fact is the PLAN row conflict,
  already registered by the stack as `F1-PLAN-ROUTE-ROW-OUTLIER` and already proposed as
  `hgk-far-remediation-20261016` R1.
- `TF-06` closed with a corrected reading (attribution recoverable; the R8 VERIFY turn ran on its lane's rank-2
  fallback, permitted by the standing failover rule and now stated).
- New: `R9-F1` lifecycle taskspec-id collision; `R9-F7` the repair denominator was one file short.
- Harness reporting defect: the recorded `subject_live` field is written before `--live` is honoured (a
  report-only defect; both runs' CHECKS used the passed tree).

## Not claimed
No acceptance, no Gate PASS, no AO verdict, no release; the registry rebind, the checker identity, the
candidate's canonical-accept policy, the lifecycle id fix, the 221 cases, the eight Gates and Fresh G1 all
remain owner acts.
