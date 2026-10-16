# Authorized shared-core (engineering-base) ChangeSet repair

When a project repair proves the reason it cannot close is a MISSING CAPABILITY in the shared control
plane, that is not a project defect. Route it to a separate, bounded, independently-checked
engineering-base ChangeSet — never patch shared core under the project order, and never weaken the gate
to make the project pass.

## 0. Trigger

A read-only diagnosis shows the project's closure predicate is structurally unreachable through the
TYPED API — e.g. `denominator()` counts `verdict != 'PASS'` as an open edge while nothing in the API can
move that column off its initial value. Write the diagnosis as raw evidence first (a read-only
source+DB readback), state the exact close condition, and stop the project leg as `TEMP_CLOSED_STATE`
until the ChangeSet is admitted. Do not reach for SQL.

## 1. Inventory BEFORE you add anything

Run this first and paste the result into the ChangeSet evidence. Do not add a primitive that already
has a typed method.

```
for each closure-primitive table (workorders, acceptances, evidence_refs, checkpoints,
 project_lifecycles, canonical_events, requirements, taskspecs, tt_records):
     grep the whole core package for UPDATE <table> | INSERT INTO <table>   -> writer statements
list every public method on the spine/lifecycle classes
classify each primitive as EXISTS / MISSING / CANNOT_COMPLETE_THE_CONTRACT
```

Rules:
- Add ONLY what the inventory marks MISSING. One missing method means a one-method diff.
- NEVER add a generic `force_close()` / `set_state()` escape hatch. A repair primitive carries the same
discipline as its neighbours: closed state set, subject binding required, lease/actor/token, idempotency
key, SINGLE atomic transaction, canonical event carrying `from_state`, history never rewritten.
- Distinguish "can resolve" from "can create". A creation INSERT (e.g. registering a row with a default
status) is NOT a resolver; only a statement that can move the value away from its initial state counts.
Check the counting logic itself — a naive "any INSERT counts as a writer" test reports a gap as present.

## 2. Contract shape the independent checker will attack

```
method(identity, *, target_value, evidence_ref, actor, token,
       expected_version, idempotency_key, subject_id, payload=None)
```

Every one of these is a property a checker will try to falsify — get them right the first time:

| property | how it is broken | guard |
|---|---|---|
| closed value set | `'PASS '`, `'pass'`, `'MAYBE'` slip through | membership test against the transition table, then a per-from-state lookup |
| subject binding MANDATORY | optional subject arg means the wrong-subject guard is opt-in | require it: `not isinstance(subject_id, str) or not subject_id.strip()` -> typed error |
| no orphan evidence | unregistered ref accepted | SELECT the evidence registry, refuse if absent |
| lease | caller writes without holding it | the same lease assert the sibling transitions use |
| no overwrite | second resolution silently rewrites | refuse when the row left its initial state; terminal states have empty successor sets |
| stale version | old caller wins | `expected_version` compare, then `UPDATE ... WHERE <still initial>` + rowcount check |
| idempotent replay | double apply | match the spent key AND the entity identity |
| atomic | half-write survives a later failure | one transaction; prove it by injecting a failure AFTER the UPDATE and asserting the row rolled back |
| audit trace | silent UPDATE | INSERT a canonical event with `from_state`, actor, versions, evidence ref |

**Namespace trap (cost a round):** a globally-UNIQUE idempotency key namespace is NOT subject-scoped.
Matching `entity_id` alone lets a key spent by a DIFFERENT entity type (whose id happens to equal yours)
be inherited as a valid replay, silently skipping the write. Match `entity_type` AND `entity_id`, and
fail closed with a distinct code when the key is spent elsewhere.

**Ordering trap (cost a round):** whichever checks run AFTER a replay short-circuit are effectively
unconditional for replays. Put subject binding, evidence existence and the lease assert BEFORE the
replay return, so the replay path is held to the same discipline as the first write. Then re-check that
no legitimate first-write or legitimate replay case got broken.

## 3. Test classes the authorization will name

Implement one class per required failure/positive class, and make each NON-VACUOUS:

1. legal transition + valid evidence, and the readback predicate reflects it
2. a legal non-pass value is not misjudged as pass
3. missing/stale/foreign/wrong-subject evidence fails closed
4. identical replay is idempotent
5. conflicting re-resolution and stale version are rejected
6. a failure AFTER the state write rolls it back (inject it; do not rely on a guard that raises early)
7. a scratch entity end-to-end typed closure with NO caller-side SQL

Vacuous-test tells: `assertRaises(Exception)` (passes with the method absent), a fixture that
pre-seeds the condition the code short-circuits on, and a docstring claiming a property the test does
not exercise. Fix by asserting the specific error type, injecting the failure at the intended point, and
asserting the method exists where the test's whole point is that it does.

## 4. Independent check and convergence

Each round is fresh-context, read-only, and must try to falsify rather than read summaries. Ask it to:
attack each property, name any VACUOUS test class, RE-MEASURE the regression numbers rather than trust
the record, verify registry rows by readback, and confirm minimality (one file, no schema change, no
second writer).

Convergence pattern, worth recognising early: round 1 finds real code defects; later rounds' findings
shift from the CODE to the RECORD and the REGISTRIES. When that shift happens the implementation is
typically done — fix the record, tighten only the specific delta the checker attacked, and re-verify the
delta instead of re-opening the implementation.

## 5. Evidence-record discipline (a recurring self-inflicted defect)

- Every count, hash and byte size in the record must be produced by the exact command quoted beside it.
  Re-measure after ANY change to the test count or file set. Recording the expected shape instead of the
  measurement is the failure mode; it survived three consecutive revisions in one session.
- Measure all the states you claim: with the change, without it, and (for a single-file core change) the
  change's own test file against the unpatched core. Note which of them you actually ran.
- Store a volatile artifact (a diff) as a BYTE FILE and record its hash, size and the exact command that
  produced it. A re-derived diff hash is not reproducible across invocations.
- When a reverted-core run is reported, distinguish "N ran / M broken" from "M failures" — moving the
  tests aside changes the denominator, and a pre-existing failure set must be shown IDENTICAL both ways
  before it can be called pre-existing.

## 6. Registration means a ROW, verified by readback

Describing a TT/CR in a JSON blob is not registering it. Registration is a row in the registry the
project config names (e.g. `canonical_database` in `config/project.json`) AND in the freeze ledger CSV
table if one is authoritative. Resolve the canonical path FROM CONFIG — do not write into whichever
spine database happens to be open, and verify by reading the rows back. If a mistaken write lands in a
non-canonical database, disclose it; do not silently delete it.

## 7. Consumer-side no-direct-SQL rule

The prohibition is on CONSUMERS and project harnesses issuing SQL writes against canonical tables —
including "just one checkpoint row". The spine's own repository/transaction implementation may use
persistence SQL internally; that is different. Before running your own projection harness, read its
writes: if any is a raw INSERT/UPDATE against a canonical table, replace it with the typed call (for
checkpoints, call the controller's checkpoint method once per work item rather than inventing ids by
SQL). SQL is for SELECT-only readback and before/after snapshots.

Make the projection script refuse to run unless the independent verdict is exactly PASS with
checker-is-not-maker, checker-read-only and a matching subject — so it cannot be used to launder a
PARTIAL into a closure.
