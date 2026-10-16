# R8-0 MISSION PLAN — skill-slim regression+apply, stale-baseline closure, EIA closure

Mission `CNV-PIPD-LS-SP-20261015` · ChangeSet `R8-0-SKILL-SLIM-REGRESSION-AND-EIA-CLOSURE`
Round root `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/`
Produced 2026-10-16 · claim ceiling **LOCAL / candidate-only** (no acceptance, no approval, no Gate PASS)

## 1. Authority and planes
| item | value |
|---|---|
| Authority anchor | `Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` v2.0.0 (SHA-256 `96d9d564…`) |
| Standing order | `Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md` (27,815 B) |
| External findings | `Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md` (`EIA-FABRIC-CONVERGENCE-R6-20261015`) |
| Control plane | HG-KSEOS (`C:/Projects/Agent_Workspace/HG-KSEOS`, AGENTS.md) — single control plane, no second DB/plane built |
| Runtime / orchestration plane | canonical Hermes (`…/LocalCache/Local/hermes`), governed profile `hgk-governed` |
| Prior rounds in this session | R6 typed admission → R6R7 archive merged (Fabric main `b8ff8104`); R7-0 packet (PR #4, head `04a1e118`, 306 blobs) |

## 2. Model plan (owner-mandated this round) — and what is verifiable
| plane | mandated | how it is bound here | evidence |
|---|---|---|---|
| PLAN & Orchestrator (in Hermes) | `gpt-6.1-sol`, OpenAI OAuth, effort medium | governed profile `profiles/hgk-governed/config.yaml` → `model.default: gpt-6.1-sol`, `provider: openai-codex`, `reasoning_effort: medium`, `_plane: PLAN & Orchestrator (in-Hermes)` | file read this round |
| delegation / sub-agent plane | (aligned to PLAN) | `config.yaml → delegation.provider: openai-codex`, `delegation.model: gpt-6.1-sol` (was `opencode-go/glm-5.3-flash`) | config SHA-256 before `dfdb3575…` → after `7029050c…` |
| EXECUTE (bounded writer) | `deepseek-v4.1-flash`, OpenCode Go | lane pool `config/lane-route-slots.candidate.json` rank 1; dispatched via `dispatch_r6.py` | lane receipts |
| VERIFY / SECURITY | `gpt-6.1-sol`, OpenAI OAuth, medium | lane pool rank 1 for `VERIFY_SECURITY` | lane pool read this round |

**Honest limit:** this session was started on `opencode-go/deepseek-v4.1-flash` and a running session cannot be
rebound by the agent; the PLAN-plane binding above is the governed profile + the delegation plane, not a claim
about the serving model of this process. Recorded as a claim limit, not smoothed over.

## 3. HGK admission
- Project `CNV-R8-SKILL-SLIM-EIA-CLOSURE` (own lineage; R6 / R6R7 / R7VH projects untouched)
- `HGK_TYPED_ADMISSION_R8.json`: intake `READY`, transitions → `DESIGN_READY` → plan → `WORKORDERS_ADMITTED`
- WorkOrders `WO-TS-CLOSURE-01 … -04` · state `WORKORDERS_ADMITTED`
- 9 source paths hashed into the admission record (PKG, PROMPT, EIA, AGENTS.md, skill-round closure + candidate files)

## 4. Board and swarm (KANBAN + SWARM)
Board `cnv-r8-skill-slim-eia-closure-20261016`; one-shot DAG:
root `t_4fc7d040` → workers `t_22bcbca7` (WS-A), `t_a715589a` (WS-B), `t_a5fb3944` (WS-C), `t_d170ea41` (WS-D),
`t_2caa0523` (WS-E), verifier `t_50cadaf6`, synthesizer `t_0ee9d4ea`.

## 5. Workstreams
| id | workstream | producer | status at writing |
|---|---|---|---|
| WS-A | skill-slim regression detection + guarded apply | ORCHESTRATOR (harness) → EXECUTE lane (repair+apply) | harness done (AVR FAIL / HGK PASS); lane running |
| WS-B | R8-0 rebuild of the R7-0 hardening on `main` + 18-mutation re-measurement | EXECUTE lane | rebased patch produced; suite + mutations running |
| WS-C | checker write-root isolation (EIA-R6-03) | ORCHESTRATOR (raw OS probe) | **done** — evidence-of-absence + mechanism proven + proposal only |
| WS-D | EIA-R6-01..09 counterexample-first reconciliation | ORCHESTRATOR | **done** — see `WS_D/EIA_R6_RECONCILIATION.json` |
| WS-F | OpenSpec change proposal for R8 | sub-agent (PLAN model) | running |
| WS-G | GSTACK named-method / role-map readback | sub-agent (PLAN model) | running |
| WS-H | self-check harness repair (TF-10) | sub-agent (PLAN model) | running |
| WS-E | evidence pack + publication to Fabric | ORCHESTRATOR (`publish_r8.py`) | harness ready, awaiting the round artifacts |

## 6. Side effects disclosed (canonical, this round)
1. `config.yaml` `delegation.provider/model` changed to `openai-codex/gpt-6.1-sol` (sha `dfdb3575…` → `7029050c…`);
   rollback = set back to `opencode-go` / `glm-5.3-flash`.
2. KANBAN board + swarm DAG created (Hermes kanban store).
3. PIPD worktree `worktrees/r8-wt` added at `dba4b19` (detached) for WS-B; three product files modified **inside that worktree only**.
4. New Fabric branch + evidence prefix R8 (publication step; will be reported with its readback).
5. Target of WS-A: the canonical skills tree `…/hermes/skills/software-development/…` (guarded apply with pre-image + rollback) — reported with its before/after table.
6. Scratch: `WS_C/acl_probe` created and removed; ACL deny/remove applied and reverted **only on that scratch path**.

## 7. Ledger
- **Blockers** — `BLK-R7-WS1-STALE-BASELINE` (closing via WS-B); EIA-R6-03/04/05 remain open (see WS-D);
  `TF-01` dispatcher brief-marker misfire (0 occurrences this round); `TF-10` selfcheck expectations (WS-H);
  `TF-06` `ERR_NO_ARM_EMITTED_NONCE` (not observed this round — no lane arm fired yet).
- **Incidents** — none new this round; the pre-existing `INC-R7-03/04/05` (verifier lane) stay as recorded.
- **Findings** — `R8-F1` the AVR slim candidate is not apply-clean (10 slice markers, frontmatter not at byte 0)
  and one absorbed reference is stale (`verifier-lane-handover.md`: recorded `aebb35ea…` vs live `2126b82e…`);
  `R8-F2` the R6 packet manifest declares 2 `__pycache__` `.pyc` paths that were not shipped (count mismatch identified);
  `R8-F3` the guarded subject has no OS-level write denial — `Authenticated Users:(I)(M)` inherited (EIA-R6-03 root cause);
  `R8-F4` 2 skills exceed the 100,000-byte main-file cap and one exceeds the 60-reference soft cap (118 live).
- **Claim ceiling** — unchanged; nothing in this round upgrades a verdict, Gate, or acceptance state.
