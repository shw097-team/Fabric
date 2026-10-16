# Final-closure / resume rounds after an accepted governed ChangeSet (F01–F07)

Verified end-to-end on `A3_FINAL_CONTROL_PLANE_DOCS_PROMOTION_AND_EVIDENCE_CLOSURE_ONLY`
(2026-08-12). Recurring pattern: after a governed task (e.g. A-3) is accepted, the user
sends a THIN closure prompt that must NOT re-run the accepted work. Mode flags:
`THIN_FINAL_CLOSURE / FAIL_CLOSED / REUSE_VALID_EVIDENCE / NO_FULL_RERUN /
CODEX_PRIMARY_FOR_TRACKED_REPAIR`. Expected hash list in the prompt is a HINT — fresh
readback wins; if an artifact drifted after freeze: classify, don't overwrite, re-bind.

## F01 — current-health (doctor) repair

- Fresh-read config + actual location + doctor raw output. If the configured target was
  externally relocated (user moved a gitignored dir, e.g. 工程基座 → 知識庫), verify the
  relocated target's git HEAD matches `expected_head` BEFORE re-binding — then repair via
  `normal admission → smallest WorkOrder (writer=codex) → Codex (danger-full-access
  pattern) → focused readback → doctor PASS`. An external cause does NOT convert a current
  FAIL into PASS; you must actually repair the locator.

## F02 — WorkOrder normative state

- Fresh typed SharedSpine readback (never Kanban `done` as substitute). Legal
  CREATED→VERIFIED requires `record_workorder_result(wo, writer=codex,
  checker=<independent>, verdict=PASS, evidence_refs=[...])` with checker ≠ writer and
  non-empty refs. Record state / lifecycle / evidence refs / checker / rollback pointer.

## F03 — docs/AGENTS currentness (the classic defect classes)

1. `RP-002 尚未執行` (never executed) is FALSE wording — RP-002 has prior historical
   execution; current state is FROZEN_PRESERVED at SELF_HOSTING_CUTOVER; docs must say
   "don't infer the next gate; fresh-read current RP-002_v2.0 blueprint/handoff before
   execution; no RP-002 PASS claim".
2. `ACTIVE_SELECTED_CERTIFIED` vs `ACTIVE_SELECTED_REINSTALL_BASELINE` contradiction →
   prefer dynamic currentness ("binding status = fresh-read config/hermes.json").
3. Stale next-stage wording (`下一工程階段 = Reference Project-001`) when the milestone is
   already MILESTONE_CLOSED → historicalize.
4. Broken locators from a raw newline inside a path (`...\evidence` + newline + `review\...`)
   → repair to the single-line actual path.
5. README single-writable-root implication → clarify HGK root is the canonical product/control
   root; other roots (SQS/Fabric) may be admitted by WorkOrder.
6. AGENTS.md minimal clarification: sole governance control plane; in-repo canonical HGK
   product root; external admitted product/domain roots remain governed stacks.
7. When the user reorganized source dirs mid-task (compiler package moved into 知識庫),
   re-bind doc locators to the CURRENT path via Codex — locators are projections, bound as
   of the freeze time; frozen evidence MD stays untouched (historical).

All tracked doc/config edits go through Codex (never Hermes-direct authoring).

## F04 — isolated-worktree equivalence requalification

Use when the original implementation wrote canonical roots (sandbox fallback). Do NOT
re-author the candidate:

- `git worktree add -b <branch> <dir>` from each repo's recorded base HEAD.
- Copy the exact candidate bytes (README/guide/AGENTS/config/untracked skill package FROM
  ITS CURRENT location) into the worktrees.
- Byte-diff worktree vs canonical root (must be empty) + run affected tests IN the
  worktree; verify worktree change set == candidate surfaces only (no unrelated files),
  one writer per worktree.
- Record separately: `CODEX_EXECUTOR_FALLBACK=NO`, `SANDBOX_MODE_FALLBACK=YES`,
  `ORIGINAL_CANONICAL_ROOT_WRITE=YES`, `COMPENSATING_CONTROLS=<list>`,
  `ISOLATED_WORKTREE_REQUALIFICATION=PASS|FAIL`. Never disguise the sandbox downgrade as
  `CODEX_FALLBACK_USED=NO` alone.

## F05 — Governed Evolution Human Policy gate → HITL stop

- Fresh-read the candidate (`improvement_candidates` table: state QUALIFIED,
  independent_verdict PASS, promotion_state NOT_PROMOTED) + policy source
  (`HG-KSEOS_P0-CIP-PACK...#COV-11-06` — promotion requires independent verifier AND
  Human Policy Owner). Do NOT self-approve. Do NOT infer approval from the prompt.
- STOP per "stop at any required Human Policy Owner gate": F06 (expanded-denominator
  checker), F07 (Codex attempt lineage) and the final evidence reseal are DEFERRED to the
  resumed session — record a closure receipt (var/a3/final-closure/closure_receipt.json)
  with all F01–F04 facts + resume token so the resumed session re-discovers nothing.
- HITL response block (exact shape):
  `CURRENT_PHASE / CANDIDATE / POLICY_SOURCE (fresh locator) / CURRENT_STATE /
  ONE_MINIMAL_USER_ACTION (APPROVE or REJECT <candidate> under the cited policy) /
  RESUME_TOKEN (<task>::F05)`.

## Final reseal (resumed session)

- Old master evidence MD remains historical (never edit post-hash). New closure payload
  `..._FINAL_CLOSURE_ACCEPTANCE.md` + machine-readable `..._FINAL_INDEPENDENT_CHECKER.json`
  rendered once, mirrored byte-identically to HGK/SQS/Fabric; hash equality proof; no
  self-referential SHA in the body; STOP and wait for external acceptance.

## Pitfalls specific to closure rounds

- The user may be reorganizing repos CONCURRENTLY: re-verify canonical paths (compiler
  package, SSOT) at the start of each phase — they can move between your own steps
  (verified: 工程基座 moved 15:42, 實作執行/SSOT moved later, both mid-task).
- Closure WorkOrder result recording (`record_workorder_result`) should use the FINAL
  closure evidence refs — defer it to the resumed session when resealing.
- Kanban note/result text must avoid gateway-lifecycle trigger words (e.g. "gateway
  pattern") or the Hermes terminal guard blocks the call.
