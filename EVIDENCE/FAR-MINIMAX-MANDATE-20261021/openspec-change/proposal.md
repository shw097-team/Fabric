# Proposal — FAR MiniMax mandate (epoch 24 → 25)

## Why

The owner (2026-10-21) ordered a single model for all three governed lanes:

| Role | Model |
|---|---|
| PLAN execution model | MiniMax M3.1 Flash (OPENCODE GO) |
| EXECUTE (Codex CLI bounded writer) | MiniMax M3.1 Flash (OPENCODE GO) |
| VERIFY / SECURITY (Codex CLI checker) | MiniMax M3.1 Flash (OPENCODE GO) |

The previous binding was GPT-6.1-SOL for PLAN and VERIFY, with DeepSeek V4.1 Flash for EXECUTE.

The owner also asked for a FAR ruling over three residual subjects (460 unchecked OpenSpec items,
120 `var/` directories, 2 TT ledger OPEN rows), cross-checked against the knowledge base, with
the ruling to be **proposed for the owner's confirmation** rather than executed unilaterally.

## What changes

### 1. The lane binding (epoch 24 → 25)

- `config/lane-route-slots.candidate.json` — MiniMax becomes the rank-1, default and
  automatically-selected arm of all three pools. Ranks stay contiguous. **No prior arm is
  deleted**; each becomes a reachable fallback, so a future owner order can restore the old
  binding without re-deriving the pool.
- `config/lane-routing-registry.yaml` — epoch, the three routes' provider/model, primary arm,
  canonical identity and selection authority follow the pool. A new declared conflict
  `SOD006-C5` records the consequence of the order, and the `EXECUTE → VERIFY_SECURITY` pair's
  `distinct_required` becomes `false` **with the reason recorded**.
- `config/model-lane-assignment.json` — the lane chains, the assignment rows, the VERIFY supply
  selector and the SoD declarations are **derived from the pool**, not hand-written, so the pool
  remains the single selection authority. The registry's projection bindings are re-derived from
  the written artifact, and pointers whose semantic slot moved are re-pointed.

### 2. The three residual subjects — measured, indexed, not closed

| Subject | Owner's figure | Measured | Action taken |
|---|---:|---:|---|
| OpenSpec unchecked items | 471 | **460** | indexed per item; **0 ticks** |
| `var/` top-level directories | 114 | **120** | indexed per directory; **0 deletions** |
| TT ledger `status == OPEN` rows | 2 | **2** | verified; **0 status changes** |

The `var/` finding is the material one: the directories are **not** 120 unfinished rounds. Only
83 are round artifacts at all; 3 are runtime/cache/DB/backup, 2 are empty, and 32 need an
owner ruling. The "114 outstanding directories" figure was a stale denominator.

## The consequence that must not be buried

With one model on all three lanes, **model-axis independence is zero**. This is declared as
`SOD006-C5` (`OPEN_OWNER_ORDERED`) rather than hedged, and the registry's SoD pair now records
`distinct_required: false` for the writer/checker pair. What remains is process separation (a
separate Codex-CLI process with a fresh context), lane separation (EXECUTE makes, VERIFY
checks), evidence-path separation (the checker re-derives every decisive claim from the
artifacts and is forbidden from reading the writer's summary), and the no-self-acceptance rule.
Correlated blind spots inside the shared model family are **not** claimed to be absent.

## Non-goals

- No deletion of any `var/` directory, any file, or any historical lane arm.
- No ticking of any OpenSpec checkbox in this change.
- No change to the TT ledger's status column.
- No change to the canonical Hermes **session** profile: the session plane and the lane plane
  are different planes, and a session pin is not a lane binding.
- No interference with the parallel SBL construction under
  `fabric-autonomous-research/runs/FAR-20261021-02{3,4}-*`.

## Impact

- `config/lane-route-slots.candidate.json` — the three pools
- `config/lane-routing-registry.yaml` — epoch, routes, SoD declarations, projections
- `config/model-lane-assignment.json` — chains, rows, selector, SoD text, revision 24 → 25
- `openspec/changes/far-minimax-mandate-20261021/` — this change
- `var/FAR-MINIMAX-MANDATE-20261021/` — receipts, indexes, the ruling report, the SBL exclusion
  note
