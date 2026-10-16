# Enforcing a mandated route scheme for all later dispatches

Context: a contract names which engine + model must serve each role (planner / executor / verifier),
and the ask is not only to run the scheme once but to make later dispatches follow it. Running it
once is trivial — bootstrap one dispatch per lane. Making it hold is a build, and the shape below is
the one that survives a checker.

## The components (any one alone is insufficient)

1. **One registry as the single source of truth** — per role: engine, provider, model, auth mode,
   declared fallbacks, and admission status; plus the enumerated list of every projection site that
   must agree with it.
   If the registry requires a binding object to exist in the subject store (a work-order id in a
   spine table), the ORDER is fixed: freeze the requirement, then create the task spec, then the work
   order, then write the registry entry. Writing the entry first yields a route that fails audit and
   has to be withdrawn, and a task spec created before its requirement is frozen is refused outright.
2. **A generator plus a drift check.** Render the whole policy document from the registry, and walk
   every projection site in the live files, naming each disagreement by JSON pointer. Building the
   drift check pays for itself immediately: walked over the live declaration sites it finds stale
   entries no one has noticed (a binding file still naming a legacy home and an old model slug).
3. **A pre-dispatch guard** that refuses (a) a target model equal to the maker's model, (b) an arm
   with no lane-shaped admission, (c) a stale policy epoch. Distinct exit codes, a machine-readable
   verdict, an optional receipt. It must be fail-closed in the correct direction: with no admission
   record at all it refuses every arm, including the correct ones.
4. **A lane-shaped admission probe** (a direct completion may never set ADMITTED) plus the durable
   wiring — a per-task/per-card override, or the guard consulted by the dispatch path itself.
   A per-card override is not self-activating: the dispatcher skips a card with no assignee/profile
   (`skipped_unassigned` in its `--dry-run --json` report), so a board that looks routed can spawn
   nothing at all. Dry-run the dispatch and read `spawned` versus `skipped_unassigned` before you
   claim the board route works.

## The conformance regression test

- One test per projection site: mutate the site, then require the checker to fail loudly AND to name
  that pointer. Assert non-vacuity per case (the mutated state must actually differ, and the
  unmutated baseline must pass). No skips.
- Derive the subcase count from the site list and print it; a hand-typed count goes stale on the next
  added site, and a suite with fewer subcases than sites is silently vacuous for the extras.

## Report the demonstration as a matrix

| case | intent | expected |
|---|---|---|
| target model == maker model, admitted | SoD must outrank admission | refuse, sod code |
| mandated target model, admitted | the scheme's own case | admit |
| mandated target model, unadmitted | fail closed | refuse, not-admitted code |
| a different role's model (e.g. executor given the planner's) | separation is per role | refuse |
| the role's own model | admit |
| unknown role name | fail closed | refuse, unknown-lane code |

Run each row yourself and record its real exit code and verdict field; do not copy the writer's table.

## Adoption status is part of the claim

A kit that is delivered and demonstrated is **not** a kit that is adopted. Nothing in the live

dispatch path consults it until the wiring is applied, and applying that wiring is a separate
governed change. Keep three sentences distinct and say which one you can prove:

- "the scheme is declared" (the policy names the routes);
- "the machinery is built and demonstrated" (this is what a design round honestly delivers);
- "the live stack is enforced" (do not say this until the dispatch path consults the guard).

Keep the residual mechanism honest as well: if the round still routed its own lanes by flipping a
shared global pin, say so plainly — that fragility is the reason the kit exists, and reporting the
mechanism as durable would be an overclaim. Do not overcorrect into paralysis either: the pin binds
at spawn, so a running child keeps its model across a later flip, and ordered as
flip -> dispatch -> restore (runs overlapping, pin never left flipped past the last dispatch) it does
route one dispatch per lane correctly. What it cannot do is hold without a human or script in the
loop, and it is shared mutable state read and written by every other workstream on the host — which
is exactly the gap the kit closes.

## A gate is only as good as its trust boundary

- **Caller-supplied admission is not admission.** A guard that accepts a bare status string (the
  literal `ADMITTED`) on its command line is trust-in-caller; the hardened form accepts only a receipt
  FILE whose recorded arm matches the requested role, model AND provider. Then prove BOTH sides: re-run
  a positive control — a well-formed receipt for the mandated arm must still exit 0 — because a gate
  that refuses everything for an unrelated reason looks exactly like a working gate.
- **Provider is not an optional dimension.** If the provider is compared only when the caller passes
  the flag, omitting the flag silently becomes a wildcard. Compare it unconditionally and fail closed
  when either side does not declare one.
- **A flag that reads as an assertion must never be an override.** `--expected-<x>` implemented as
  "use this value instead of reading the live one" lets whoever controls argv force the check green.
  Always read the live value from disk and treat the flag as an additional requirement, reported under
  its own check id.
- **Fail closed on unreadable inputs.** A pinned source that cannot be read is stale, not exempt: an
  `if path.exists(): <check>` with no `else` branch silently skips the entire staleness test.

## When the round advances the file the gate pins

A trap that costs a whole landing: the kit pins the digest + revision of a canonical file, and the
same round then changes that file (a policy revision bump, a declaration sweep). Every admit case now
exits stale and the kit stops landing — a self-inflicted defect that presents as the round's own work
failing its own gate. Update the pin, the epoch and the recorded revision in the SAME pass that
changes the source, keep the superseded byte-preimage as a round backup (point the history entry at
the backup instead of claiming in-place immutable bytes for a file that has been rewritten), re-run
the positive control, and state the attribution yourself before an independent checker has to guess
who moved it.

## A declared field the projection drops cannot be checked

Adding a routing-relevant declaration (per-role reasoning effort, auth mode, fallback arm) is not done
when the registry carries it: if the projection compacts the route and drops the field, the drift
check cannot see it and the declaration is silently inert. Carry the field through the projection and
add a projection binding for every site that declares it, so a silent loss becomes a named finding.

## Documenting the gate without over-engineering it

The gate is usually documented in the wrong place or not at all, and the reflex fix — a chapter in the
operator-facing manual — duplicates a source that changes independently. Apply an explicit test to each
candidate: reject anything that copies a marker list, a route inventory or a repair recipe (they drift
from the code they describe), anything that creates a second place where the rules live, and any text
repeated into two independently maintained documents. What passes is a short troubleshooting POINTER
in the operator-facing manual, aimed at the one owner of the operational route. Stage such patches
beside the round rather than applying them to a maintained document, and before applying one check
whether the target exists in more than one home directory — a one-sided edit to a duplicated reference
desynchronises the copies.

## The sealed executor lane: relay readiness and board mechanics

- The executor lane usually depends on a LOCAL RELAY, and the sanctioned write path pre-checks that
  relay's health endpoint and refuses with its own error code — so a dead relay surfaces as a launch
  refusal, never as a silent fallback to another provider. Diagnose with the supervisor's Verify
  action (it reports a degraded state plus a specific unreachable error), recover with its Run action
  (a bounded restart window), then confirm the health BODY (status, version, pid, uptime) before
  re-running; keep the failed attempt as evidence rather than deleting it.
- The relay can also die MID-TURN, and the signature is different: the writer's TURN fails with a stream
  disconnect against the relay's own port (`turn.failed: stream disconnected before completion`), not a
  launch refusal. The writer has then done real work and stopped between steps, so do NOT re-run the round
  from the top — restart the relay with the sanctioned supervisor action, enumerate what the interrupted
  turn actually delivered against what the spec required, and dispatch a CONTINUATION spec bound to exactly
  the remainder (same boundaries, same receipt shape). The partial artefacts on disk are the input, and
  re-issuing the original spec mostly re-does finished work.
- **A monitoring crash is not a task failure.** A supervisor that tails the writer's JSON log dies on the
  first line that does not parse as a dict (`'int' object has no attribute 'get'`), which kills the MONITOR
  while the sealed writer keeps running. Before concluding anything: confirm the launcher and writer are
  still alive, then RE-ATTACH a fixed monitor to the SAME run — never relaunch the round. A supervisor that
  can only start a run, not rejoin one, converts a parser bug into a lost round. Guard every parsed line
  (`if not isinstance(ev, dict): continue`) and keep monitor state in the run directory so a restart resumes
  the same evidence file.
- Without a durable scheduled task for the supervisor the relay stays down after a kill or a reboot.
  Scheduling it is part of adoption, not an optional extra: record the exact creation command, its
  trigger, and the removal command that rolls it back.
- Board mechanics that cost dispatches: a board is created with its slug as a positional argument
  (there is no display-name flag); completing a card requires an explicit result/summary or the
  completion is refused as non-evidence; and linking a card under a parent flips it out of ready until
  the parent completes — so build the whole DAG before claiming anything. Set the per-card
  model/provider override at creation time and read the routing back from the CARD, so the durable
  route is visible on the board instead of living in the shared global pin.
- The sanctioned executor invocation takes the work as a SHORT prompt that POINTS AT a task-spec
  file, never an inlined essay: argv limits and shell quoting make a long inline prompt a bad bet.
  Shape: `pwsh -NoProfile -File scripts/<launcher>.ps1 -Action Write -Prompt "Execute the task spec
  at <abs>/CODEX_TASK_N.md exactly as written; write receipts into <dir>/receipts/ and your final
  message into <dir>/codex/." -ModelChain <provider/model>`, started as a background process with
  completion notification. Confirm the relay health BODY first — the launcher fail-closes before it
  runs anything, so a launch refusal is a relay finding, not an executor finding.
- Write the spec so the work is checkable without the transcript: hard boundaries (never touch the
  subject store, the canonical policy, or credentials), per-step preimage -> atomic write ->
  after-hash -> proof command -> rollback, the required receipt JSON shape, and an explicit list of
  points to RECORD AS BLOCKED rather than implement. A written spec is followed far more tightly
  than a paragraph of instructions, and it is the artifact that makes the run reviewable.
- Judge the run by its RECEIPT, not its exit code. The launch receipt's `write_model_used` (with
  `write_chain_exhausted`) names the model that actually served the work: exit 0 on a failover arm is
  a deviation to disclose, and exit 0 proves neither the model nor that any write happened. Then
  re-run every step's proof yourself against the live files (a zero-finding drift check, a
  byte-equality assertion across duplicated copies, a readback of any registered task) before
  crediting the step.

## Reconciling an adjudicated route change with the registry's own invariants

An authorized route change can CONTRADICT an invariant the registry already declares. Read the
registry's own prose before implementing the adjudication: a documented "the two arms are CO-EQUAL;
neither is a fallback of the other, so neither appears in `fallbacks`" is a contract, and the
conformance test enforces it (`assertEqual(route["fallbacks"], [])` for every lane). An
adjudication phrased as "demote the alternate arm to a fallback" therefore cannot be implemented
literally without breaking a pre-existing invariant.

- **Encode the intent inside the existing contract; never weaken the test to fit the change.** Set
the top-level route to the mandated arm, keep `fallbacks: []`, and record the demoted arm inside
`arms[]` with explicit non-default flags (`co_equal: false`, a role naming it a demoted alternate,
plus an explicit never-auto-selected flag). Then prove BOTH halves: every lane's `fallbacks` is
empty AND the SoD pair still passes. A change that requires editing the conformance regression is a
change that needs the owner, not a test edit.
- **A content change to the registry forces its own generation counter forward, and drags every
coupled declaration with it.** The registry's `epoch` documents the route-shape generation; the
source-of-routes revision + digest, the assignment's `registry_epoch`, and the projection bindings
must all move in the SAME pass, or the drift check reports the round's own work as drift. Validate
by re-reading the live registry (`check_drift` empty, `check_sod` OK, all `fallbacks` empty,
source digest equal to the file's own sha256) rather than by trusting the writer's summary.

## An isolated candidate reads its OWN frozen config copy

A candidate working copy carries its own copy of the registry/config, frozen when it was adopted.
Editing the CANONICAL registry does not reach it, so an in-copy conformance run keeps reproducing
the historical defect long after the canonical fix landed. That is an input-staleness artifact, not
a defect in the candidate's code, and it must be reported as such.

- Run the conformance regression against the CANONICAL root through the test's own source-root env
hook (that hook exists for exactly this), and confirm the test file is unmodified versus the maker's
receipt. `<APP>_SOURCE_ROOT=<repo>` is the intended mechanism, not a hack.
- **Do NOT "fix" it by syncing the candidate's config copy to canonical.** A candidate's tests and
fixtures are anchored to the VALUES of the config they were built against (an epoch, a revision), so
syncing flips a DIFFERENT set of tests red — most visibly a freshness guard refusing with a
stale-epoch error, which is correct behaviour, not a bug — and you have traded one red for another
while invalidating the receipt's recorded post-hashes. If a fully green in-copy suite is genuinely
required, that is a maker task (update the fixtures to the new canonical values) and it needs a
fresh independent verification afterwards.
- Revert cleanly if you already tried the sync: restore from the byte backups you took, then
re-verify that the product files hash to the maker's own recorded post-hashes. A round that leaves
the artifact mutated and the receipts stale has manufactured an unverified delta.
