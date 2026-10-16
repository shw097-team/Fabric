# Lane rebind and closure for the 2026-10-16 owner order

## Why

The owner order in force for session `20261016_104922_d455e7` (round 3) re-points the three governed lanes
in a way that inverts the separation-of-duties axis the policy was built around:

* PLAN & Orchestrator becomes `opencode-go/glm-5.3-flash`;
* the EXECUTE bounded writer stays `opencode-go/deepseek-v4.1-flash` (CODEX CLI);
* the Independent Acceptance Officer / VERIFY / SECURITY becomes `opencode-go/deepseek-v4.1-flash`
  (CODEX CLI) — **the same model the writer holds**.

Epoch 21 had it the other way round: PLAN and VERIFY shared `openai-codex/gpt-6.1-sol` (declared as
`SOD006-C2`, owner-ordered) while EXECUTE and VERIFY were required to be distinct. Applying the new order
without moving every coupled declaration would leave the registry, its projections, the assignment site,
the dispatch-time pool and the conformance fixture contradicting one another — and the pre-dispatch guard
would be left refusing, permanently, the very dispatch the owner ordered.

## What changes

1. **PLAN rebind.** `routes[].PLAN` moves to `opencode-go/glm-5.3-flash` (medium) with the owner chain
   `[glm-5.3-flash, gpt-6.1-sol (non-default), deepseek-v4.1-flash]`; `selection_authority` names the new
   order; the dispatch-time pool promotes GLM to rank 1.
2. **VERIFY rebind.** `routes[].VERIFY_SECURITY` moves to `opencode-go/deepseek-v4.1-flash` with
   `selected_arm: A` and the chain `[deepseek-v4.1-flash, gpt-6.1-sol (non-default), glm-5.3-flash]`.
3. **SoD re-declaration.** `sod_invariants.pairs` flips both flags (EXECUTE/VERIFY demoted, PLAN/VERIFY
   required again), `declared_conflicts.SOD006-C3` declares the new collision as `OWNER_ORDERED_IN_FORCE`,
   and `SOD006-C2` becomes `SUPERSEDED` — retained, never deleted.
4. **Coupling.** `epoch` 21 -> 22, `revision` 21 -> 22, `source_of_routes` re-pinned to the live digest,
   every affected `projections[].bindings[].expected` re-bound, and the conformance fixture's owner chain
   moved in the same change.
5. **Enforcement agreement (R10).** The pre-dispatch guard gains an additive, fail-closed path: a
   same-model pair is admitted ONLY when the registry declares the pair with `distinct_required: false` AND
   a `declared_conflicts` entry naming that exact pair with status `OWNER_ORDERED_IN_FORCE`; the verdict
   must record the conflict id. Undeclared collisions are refused exactly as before.

## Impact

The three lanes are dispatchable under the order; the declaring surfaces and the enforcement surfaces agree;
and the residual — model-axis independence between writer and checker is deliberately absent — is declared
in the registry and in every affected artifact rather than hedged. Model diversity between writer and checker
is NOT claimed anywhere.

**Claim ceiling:** CANDIDATE_ONLY. The repository merge and branch deletion remain the OWNER's decision. No
canonical acceptance is asserted by this change or by the round that produced it.
