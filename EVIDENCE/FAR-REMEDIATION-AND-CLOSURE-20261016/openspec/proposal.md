# FAR remediation and closure 2026-10-16

## Why

Round `LANE-RELIABILITY-CLOSURE-20261016` closed with a residual ledger rather than with a clean
board: three lanes were proven to be served and identity-matched in the turns that completed, but six
items were left deliberately unfixed — a registry route row that disagrees with every other declaration
of the PLAN arm, a verified change set that was never promoted, a declared SoD conflict left "open" when
the owner had in fact ordered it, an environment-limited test carried as an open gap, a turn-shape
reliability defect known to cost 900 s per occurrence, and the outstanding closure of the session.

An unfixed ledger is not neutral: the operator's own conformance gate stayed RED, and the product line
kept a live outage that a verified candidate had already closed.

## What changes

1. **R1 — PLAN route row rebind.** `config/lane-routing-registry.yaml` `routes[].PLAN` moves from
   `opencode-go/glm-5.3-flash` to `openai-codex/gpt-6.1-sol` (medium, OAuth), under the owner order in
   force for this session, and the stale `usable_now: QUOTA_429_2026-10-15` marker is replaced by this
   session's measurement. Registry `epoch` advances 20 -> 21.
2. **R3 — declared SoD conflict reclassified.** `declared_conflicts[SOD006-C2]` moves from
   `OPEN_OWNER_ORDERED` to `OWNER_ORDERED_IN_FORCE`, recording that PLAN and VERIFY/SECURITY are the
   same model **by owner order**, and stating exactly which independence remains.
3. **R2 — promotion of the verified candidate.** The product files the previous round verified
   (the effort axis, the absent-session-id outage and their tests) are applied to the canonical tree
   with per-file backups and recorded before/after digests. This is an APPLY under owner authorisation,
   not an acceptance.
4. **R5 — the turn-shape fix in the tool.** `scripts/hgk-lane-dispatch.py` gains an OPTIONAL
   `--turn-shape {normal,edit_only}` that prepends a fixed HARD RULES block when `edit_only`, and
   records the shape used in the receipt. Additive: no existing flag changes meaning.

## Impact

`lane-governance-gates` — the registry declaration surfaces and the lane dispatch surface. The
conformance gate that these declarations drive is expected to stop being RED on the canonical tree.

## Claim ceiling

Executing a ruling is not accepting it. Nothing here is accepted, and external acceptance remains
`NOT_PERFORMED`.
