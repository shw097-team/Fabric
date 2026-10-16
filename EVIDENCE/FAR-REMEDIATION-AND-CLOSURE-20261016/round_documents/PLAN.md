# PLAN — FAR-REMEDIATION-AND-CLOSURE-20261016

Round 2 of session `20261016_104922_d455e7`, following `LANE-RELIABILITY-CLOSURE-20261016`.
Round dir: `var/FAR-REMEDIATION-AND-CLOSURE-20261016/`.

## 0. Reuse first (the owner's standing instruction)

This round does **not** build a lane, a mechanism or a harness from scratch. It reuses, by name:

| reused asset | where | how it is used here |
|---|---|---|
| the four lanes and the sealed CODEX-CLI dispatch | `var/LANE-RELIABILITY-CLOSURE-20261016/run_lane.py`, `scripts/hgk-lane-dispatch.py` | EXECUTE and VERIFY turns for this round |
| the round's own detection harness | `var/LANE-RELIABILITY-CLOSURE-20261016/selfcheck.py` + `annotate_selfcheck.py` | the D-list below, extended |
| the freeze / publish / gate chain | `freeze_candidate.py`, `publish_packet.py`, `packet_gate.py`, `verify_remote.py` | publication of this round |
| the FAR ruling format | `var/LANE-ENFORCEMENT-APPLY-20261015/FAR-GAP-RULING-20261015/FAR_PLAN_ORCHESTRATOR_MODEL_RULING.md` (`一、研究問題` → `二、事實` → `三、最佳工程裁決` → `四、執行方案` → `五、claim ceiling`) | `FAR_RULING.md` |
| the residual ledger | `var/LANE-RELIABILITY-CLOSURE-20261016/ROUND_CLOSURE.json` | every item in `RESIDUAL_INVENTORY.json` cites it |
| KANBAN / SWARM / GSTACK / OPENSPEC | `kanban.db`, `KANBAN_SWARM_GRAPH.json`, `references/gstack-named-method-readback.md`, `OPENSPEC/config.yaml` | enabled for this round (see T3/T4) |

## 1. 核心大目標 (the single large goal)

**Turn this session's own residual ledger into an executed, owner-authorised remediation, then close
and hand over the session.** Concretely: run a FAR study over every residual, gap, owner-decision item
and closure item; produce the best engineering ruling with a low-friction, high-necessity,
not-over-engineered execution plan aligned to the session's goal; and — the owner having pre-authorised
execution — EXECUTE it, self-detect, self-repair, self-verify, then publish implementation + evidence to
`github.com/shw097-team/Fabric` and hand over.

Why this is the right large goal rather than "fix F1": the residual ledger is the only place where the
*system's* remaining deviation is written down, and its items are heterogeneous — a config row, an
unpromoted verified change, an owner-ordered model overlap, an environment-limited test, a turn-shape
reliability fix. A FAR study is what decides which of those need engineering, which need a decision,
and which should be reclassified out of existence.

## 2. SPEC

### 2.1 In scope

1. A FAR study over the full residual inventory, with an options matrix per item and an explicit
   engineering-necessity verdict (do / decide / drop).
2. Execution of the ruling the study produces, including canonical changes, under a WorkOrder per
   change, with backups and before/after digests.
3. The four mechanisms enabled and evidenced for this round.
4. Independent verification of the result by the VERIFY/SECURITY lane over a frozen subject.
5. Session closure: checkpoint/handover, and publication of implementation + evidence to Fabric.

### 2.2 Explicitly OUT of scope

- Any change to the lanes' model assignments beyond what the 2026-10-16 owner order already names
  (PLAN and VERIFY = `openai-codex/gpt-6.1-sol` medium OAuth; EXECUTE = `opencode-go/deepseek-v4.1-flash`).
- Any `git push --force`, any history rewrite, any merge into `main` without a PR.
- Declaring acceptance. External acceptance stays with the external acceptor.

### 2.3 Authorisation basis, stated exactly

The owner's message for this round authorises: (a) the FAR study; (b) **direct execution of the ruling
the study produces**. That is a *forward* authorisation to apply. It is **not** an acceptance, and it
does not authorise claiming acceptance. Where an item is an owner decision, the study proposes and the
execution either applies it under this authorisation (recording the order it rests on) or leaves it,
and says which.

## 3. 任務執行清單 (task list)

| # | task | output |
|---|---|---|
| T1 | Build the machine-readable residual inventory from the ledger + prior rounds | `RESIDUAL_INVENTORY.json` |
| T2 | FAR study: per item — deviation vs the named governing document, options, necessity, ruling | `FAR_RULING.md` |
| T3 | Enable KANBAN + SWARM: board tasks and the execution graph | `KANBAN_SWARM_GRAPH.json`, board DB rows |
| T4 | Enable OPENSPEC: change with delta spec validated `--strict` | `OPENSPEC/changes/hgk-far-remediation-20261016/` |
| T5 | HGK admission: typed admission, role mandate, WorkOrder per ruling item | `admission.json`, `role_mandate.json` |
| T6 | EXECUTE the ruling (canonical applies per WorkOrder; product code via the EXECUTE lane, edit-only) | apply receipts |
| T7 | Detection list D01..Dn re-derived orchestrator-side | `SELFCHECK_REPORT.json` |
| T8 | Independent VERIFY over the frozen subject (CODEX CLI, `openai-codex/gpt-6.1-sol`) | `CHECKER_VERDICT.json` |
| T9 | Closure: closure JSON, README, checkpoint/handover | `ROUND_CLOSURE.json`, `README.md`, `_handover/CHECKPOINT_*.md` |
| T10 | Publication to Fabric, then read the remote back | PR + `verify_remote` output |
| T11 | Self-research / self-learning / self-iteration / self-evolution record | `RETROSPECTIVE.md`/`.json` |

## 4. 檢測清單 (detection list — each item must be re-derived, none taken from a lane's prose)

| id | assertion |
|---|---|
| D01 | the canonical conformance suite's PLAN-route case passes after the ruling is applied (`test_registry_and_projection_shape`) |
| D02 | `check_drift` reports no fatal item on the canonical registry |
| D03 | registry `epoch` advanced exactly once for this round's config change |
| D04 | every canonical mutation has a backup, a WorkOrder and before/after digests |
| D05 | the promoted product files equal the frozen candidate's digests, byte for byte |
| D06 | the promoted product files are exactly the PROMOTE set — nothing round-local leaked into canonical |
| D07 | the 7-module suite at the canonical root is green (no failures, no errors) |
| D08 | a new test file present in canonical is importable and its declared test count matches |
| D09 | the EXECUTE lane receipt for this round: `required_arm == served_arm`, `usage_receipt_ok`, nonce present |
| D10 | the VERIFY lane receipt: same, plus `subject_mutation == CLEAN` (the checker did not alter the subject) |
| D11 | the checker's own verdict is present, extracted and quoted — agreeing or not |
| D12 | any item the FAR classified as "decide" or "drop" is recorded with the basis, not silently removed |
| D13 | KANBAN board DB carries this round's root, workers, verifier, synthesizer and edges |
| D14 | OPENSPEC change validates with the project CLI `--strict` |
| D15 | no artifact claims acceptance; every closure carries a claim ceiling |
| D16 | publication: remote branch sha == local HEAD, and the manifest is byte-identical on the remote |

## 5. Claim ceiling for this round's plan

Planning is not execution. Nothing in this file asserts that any item is fixed; the detection list
above is what will decide that, and it is re-derived rather than reported.
