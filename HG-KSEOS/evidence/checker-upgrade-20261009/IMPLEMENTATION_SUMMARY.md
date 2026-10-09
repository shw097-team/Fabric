# HGK Independent Checker Upgrade — consolidated implementation summary (round HGK-CHU-20261009)

**Status: CANDIDATE. `TEMP_CLOSED/UNVERIFIED` at the cutover gate.** This document summarises what was
actually implemented and verified, and states plainly what is NOT claimed. It is built to be publishable:
it contains no credentials, no keys and no token material.

## 1. What was built

An **independent checker capability** for HG-KSEOS: a checker lane that runs on a model distinct from the
maker, reached through Codex CLI -> a loopback Responses/Completions bridge -> the checker model, whose
output is **advisory only**.

| surface | artifact |
|---|---|
| adapter package | `src/hg_kseos/checker_bridge/` — `binding.py`, `runner.py`, `watchdog.py`, `verdict.py`, `integration.py`, `advisory_verdict.schema.json` |
| runtime wiring | one named method (`named_methods.py`), one CLI subcommand (`cli.py`), consumer side `integration.py` |
| config | `config/checker/checker-binding.candidate.json` (`status: CANDIDATE_NOT_ADMITTED`), `config/checker/monitor-policy.json` |
| qualification | `scripts/checker_bridge_qualify.py` (loopback-only, positive-only preflight) |
| tests | `tests/checker_bridge/` — 113 tests, OK (skipped=1) |
| harness | `scripts/checker_bridge_qualify.py`, the round's lane launchers and probes under `.hgk/checker-upgrade-20261009/tools/` |

## 2. The advisory ceiling (the load-bearing invariant)

A checker verdict is **never** an OracleReceipt and **never** a canonical acceptance status. The adapter
fails closed on: a binding that claims a canonical token (`PASS` / `PARTIAL` / `FAIL` / `TEMP_CLOSED` /
`INDEPENDENT_PASS` / `RELEASED` / `PRODUCTION_VERIFIED`), a non-candidate binding, a verdict outside the
advisory enum, and a verdict whose digests disagree with the intake. Watchdog pauses are advisory requests
(`WATCHDOG_ADVISORY_ONLY`); resuming canonical state always requires an operator decision.

## 3. What was measured (evidence-backed)

- **Connector, end-to-end**: a real Codex -> bridge -> checker-model trace with tool carrying, shell
  execution and file writes: 114 `POST /v1/responses`, a 10,513-byte verdict file with 3 verdicts, 5 proven
  shell executions, 8 proven file writes.
- **Watchdog semantics**: 4 repeats -> investigate, 5th -> pause; stale heartbeat pauses; corrupt state
  fails closed; and the pause marker advances on **verified progress only** — a repair verified
  independently by two different models.
- **Negative/security fixtures**: mutation, digest, enum and poisoned-instruction families pass natively;
  the symlink family is verified on a platform that can express a symlink (see §5).
- **Cross-model acceptance**: the same three repair claims audited by DeepSeek V4.1 Flash and by
  GLM-5.3-Flash, **both NOT_CONVICTED on all three**, with non-modification re-derived independently by
  per-file sha256.

## 4. Governance chain (all through the typed API — no raw SQL)

Requirement -> taskspec -> WorkOrder lineage admitted via `ProjectLifecycleController.admit_requirement`
(`REQ-CHU-01..08`, plus `REQ-CHU-04-WIRING` admitted this round to name the runtime-wiring write scope).
Kanban gate board `hgk-checker-upgrade`: **12 of 14 gates closed** (C0, G1-G7, G9, G10, G11). Every gate
closed on a re-measured acceptance command, never on a writer's own prose.

## 5. Ceilings and non-claims — stated, not implied

- **The cutover gate is `TEMP_CLOSED/UNVERIFIED` and NOT accepted/released.** The authoritative
  specification's §15 precondition list is measurably unmet: no canonical v2 binding, no trusted signature
  payloads, no Go upstream route-attestation trace, no ACL/egress/proc-tree negative matrix, no live
  supervisor ack, no Golden/Holdout sets, **no Shadow A/B run**, no authorized OracleReceipt, no rollback
  drill. Missing any one of these forbids promotion.
- **Advisory only**: `hgk_canonical_acceptance: NOT_PERFORMED`.
- **Symlink fixture**: the assertion is proved on a symlink-capable surface, not on Windows; Developer
  Mode is off and a directory junction was measured to FAIL as a substitute (the code tests
  `p.is_symlink()`, which is false for a junction). Cross-platform substitute evidence, disclosed.
- **Write denial is DETECTION, not an ACL boundary**: the read-only attribute is clearable by the same
  user. The specification itself scopes Windows isolation as `BLOCKED_LIVE`.
- **Process independence vs model independence**: where the designated checker model equals the maker's
  model, that lane's independence is PROCESS-only; model diversity comes from the second (GLM) lane.
- **Two documentation items remain** by the specification's own ordering: the two User Guide currentness
  edits, deferred to after cutover is formally accepted.

## 6. Round findings ledger

34 findings, 8 blocking. Several of the blocking ones were defects in the round's own harness rather than
in the product, and are recorded as such rather than quietly fixed — including four verification-harness
defects that each produced a confident false result and were caught only by re-measuring.

## 7. Where the evidence lives

- `HG-KSEOS/evidence/checker-upgrade-20261009/HGK-CHU-20261009_CHECKER_UPGRADE_EVIDENCE.md` — the frozen
  single-file evidence MD, generated from the machine artifacts and mirrored byte-identically.
- `Fabric/evidence/review/checker-upgrade-20261009/` — the mirrored copy.
- `.hgk/checker-upgrade-20261009/` — the round's working artifacts: finding ledger, decisions
  (including the FAR adjudications), probes, lane launchers, freeze manifests.
