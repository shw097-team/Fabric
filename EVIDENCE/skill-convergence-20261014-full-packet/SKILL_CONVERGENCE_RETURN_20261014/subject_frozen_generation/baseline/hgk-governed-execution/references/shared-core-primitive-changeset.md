# Bounded engineering-base ChangeSet: adding ONE missing primitive to a shared core

When a governed round is blocked because the control plane *cannot* materialize required state through
its own typed API, the honest route is a separate, minimal, independently checked ChangeSet against the
shared core — never a direct SQL write, never a patch smuggled in under the project order. This file is
the procedure and the traps.

## 1. Inventory BEFORE designing

Enumerate every closure primitive the round needs and classify each as EXISTS / MISSING from SOURCE,
not from the API's naming:

```
workorder terminal/result   -> SharedSpine.record_workorder_result      (exists)
acceptance resolution       -> (nothing)                               (MISSING)
evidence-ref registration   -> SharedSpine.register_evidence           (exists)
normative checkpoint        -> ProjectLifecycleController.checkpoint   (exists)
lifecycle advancement       -> ProjectLifecycleController.transition   (exists)
```

Add **only** what is missing. If one primitive is absent, the ChangeSet is one primitive — not a
refactor, not a second workflow/reducer/control plane, and never a generic `force_close()` bypass.

Grep discipline for the inventory itself: a scan that counts any statement NAMING the table reports the
capability as present. `INSERT INTO acceptances ... (verdict NOT_RUN)` is a CREATOR; only
`UPDATE ... SET verdict` or `INSERT ... ON CONFLICT DO UPDATE` is a RESOLVER. Counting creators as
resolvers produced a harness that announced `TYPED_API_PRESENT` for a spine that had no resolver at all.

## 2. Guard design rules (each cost a real bypass)

1. **A fail-closed subject parameter must be MANDATORY.** An optional `requirement_id=None` makes the
   wrong-subject guard opt-in, so a caller who omits it gets no subject binding at all. Defaulted
   guards are not guards.
2. **An idempotent-replay short-circuit must match the FULL subject key.** A globally UNIQUE
   idempotency namespace is shared across EVERY entity type, so `entity_id` alone is not a subject
   key: a requirement/taskspec/workorder event can carry an `entity_id` equal to your acceptance id,
   and your guard will hand that foreign event back as a valid replay while silently skipping the
   write. Match `entity_type` AND `entity_id`.
3. **Put the subject check BEFORE the replay short-circuit**, otherwise the replay path is the one
   route that bypasses it (observed: a replay with a wrong-but-non-empty subject returned the original
   event instead of raising, so the word "unconditional" in the docstring was not literally true).
4. **An executed UPDATE must be proven to roll back.** A test that pre-seeds the idempotency key
   exercises the REPLAY path, and a test that triggers an illegal-transition guard raises BEFORE the
   write — neither exercises rollback. Inject the failure AFTER the UPDATE (patch the serialiser used to
   build the event row) and assert the row is untouched. A reviewer's independent mutation
   (replace rollback with commit and show the row moved) is the strongest form; do it yourself first.
5. **Terminal states must be terminal.** Closed verdict set read from the transition table; a resolved
   row cannot be re-resolved; the prior value survives as the event's `from_state`.

## 3. Measurement discipline for a with/without comparison

A "the change caused no regression" table has **three** distinct states and each has its own count.
Measure every one; never write a number you did not measure:

| state | what it is |
|---|---|
| with-change | change + its own new tests present |
| pristine | change reverted AND the new test file removed |
| revert-code-only | change reverted but the new test file still present |

Reverting only the code while the new tests remain yields a much larger failure count; quoting the
pristine figure for that state is wrong. The substantive claim to verify is narrower and easier:
**the same pre-existing failures appear in every state**. Also do not write "the remainder pass
vacuously" without measuring the file alone — claiming tests pass when they error is the same defect
class as any other unsupported receipt field. If a checker catches a figure once, expect it to catch
the repeat; re-measure rather than re-assert.

Confirm the pre-existing set is genuinely pre-existing by running the same command on a pristine copy
and diffing the SORTED failure-name sets — identical sets is the proof, not a shared count.

## 4. A disclosed limitation must be REGISTERED, not described

"Opened as TT-xxx" in a docstring or an evidence JSON is not opening a ticket. Register it where the
canonical registries live — the typed API (`SharedSpine.open_tt(...)`) AND the tracked ledger file —
then confirm by reading the registry back. A named-but-absent entity is the same defect class as any
other unsupported claim.

## 5. Narrow the CLAIM rather than expand the scope

When a property the authorization names cannot be achieved inside the minimal scope (the shared
evidence registry has no subject column, so foreign-evidence rejection would need a schema
migration), do NOT: overclaim in the docstring, silently widen the ChangeSet, or delete the property.
Instead: state the precise achieved claim in the code ("registered-evidence binding", explicitly NOT
"subject-bound evidence"), record the gap as a typed non-blocking TT with its close criterion, and make
code + docstring + evidence JSON + TT all say the same thing. Consistency across those four surfaces is
what an independent lane checks.

## 6. Independent check is mandatory and iterative

A shared-core ChangeSet needs its own fresh-context VERIFY_ONLY checker, distinct from its maker, and a
repair of that ChangeSet needs its OWN fresh check — a fixed artifact does not inherit the previous
verdict. Expect the checker to (a) inject its own mutation tests, (b) find that a docstring overstates
what the code does, and (c) catch arithmetic/figures in your evidence record. All three are findings to
act on, not to argue with.

## 7. Rollback is part of the deliverable

Record the revert path explicitly and demonstrate it (stash/pop the single file during the baseline
comparison): one file, no table or column added, no data migration. A ChangeSet that cannot be cleanly
reverted is not minimal.

## 8. Do not let a lane verdict satisfy an aggregate gate

A product-lane PASS must never proxy an overall/wave verdict (see the aggregate-gate rules in
SKILL.md). When the ChangeSet's own checker returns PARTIAL, the round's claim is reduced accordingly,
even if every product assertion passed.
