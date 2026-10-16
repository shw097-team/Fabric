# FAR-20261019 errata and findings (own-round, measured)

Every entry was produced by this round's own execution, not carried over. Nothing here is a claim about a
subject; each is a statement about this round's process, with the tool output that proves it.

## ER1 — TaskSpec ids are derived from the project id's last segment, so two rounds collide

`lifecycle.plan()` builds `spec_id = f"TS-{project_id.split('-')[-1]}-{i:02d}"`. Two projects whose ids end
in the same token therefore collide: `FAR-018-R7R11-RESIDUAL` and `FAR-019-R7R11-RESIDUAL` both resolve to
`TS-RESIDUAL-01..05`, and admission dies with
`sqlite3.IntegrityError: UNIQUE constraint failed: taskspecs.taskspec_id`.
Failed closed — no partial taskspec row was committed and the spine was not corrupted (verified by query).
Second attempt with `FAR-019-OWNER-CLOSURE` hit an older project's `TS-CLOSURE-01..04`.
**Repair candidate:** derive the id from the whole project id or a digest of it.
**Side effect to disclose:** two orphan lifecycles, `FAR-019-R7R11-RESIDUAL` and `FAR-019-OWNER-CLOSURE`,
now sit at `PLAN_READY` with frozen requirements and no governed abandonment path. They were **not**
deleted: a direct write to the shared spine is itself an ungoverned mutation. Recorded here instead.

## ER2 — a guard root must not contain the harness's own outputs

First dispatch refused: `ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT` — the round directory was passed as the
guard root, and the harness's own receipt and attempt log live inside it, so the harness's writes would
have registered as subject changes and every run would have reported a false mutation.
The tool refused correctly and said why. Fixed by pointing the guard at a dedicated root.

## ER3 — an empty guard root is refused, not certified

Second dispatch refused: `ERR_GUARD_ROOT_EMPTY` — "a guard over an empty root proves nothing (an empty root
is vacuous even when another root contributes files)". A guard must have a non-empty baseline.
Fixed by seeding a real frozen subject pack (`subject/`) containing this round's authoritative inputs, with
the harness outputs deliberately outside it.

## ER4 — the spine cannot distinguish two rounds by goal

Both `FAR-019-R7R11-RESIDUAL` and `FAR-019-OWNER-CLOSURE`, and `FAR-018-R7R11-RESIDUAL`, carry the **same**
`goal_hash` (`ca448f8a…`) because the goal text was re-used verbatim. Round identity in the spine therefore
lives only in `project_id`, not in the intent. Recorded as a limitation of re-use-first rounds.

## ER5 — a substitution slip left the receipt under the previous round's filename

`far019_admission.py` was built by substituting a previous-round script, and the receipt it wrote was still
named `HGK_TYPED_ADMISSION_FAR018.json` while containing FAR-019 data. Renamed to
`HGK_TYPED_ADMISSION_FAR019.json`. Disclosed rather than silently corrected, because a filename is part of
an artifact's identity.

## ER6 — the contract compiler's source scan is stricter than it looks

Measured, in order: `PL-003` fires when a required source family is absent; it fires **again** when a family
appears more than once (`duplicate=True`), so `source_scan.reviewed` must hold exactly one entry per
family; and `PL-SCHEMA` fires on any extra key under `source_scan`, and on an `authority.sources` entry
missing `rank`/`governs` or carrying an unknown `kind`. All four conditions were hit and fixed this round,
and the contract now passes lint, activation, acceptance, hash and compile with zero errors.

## ER7 — two numbers in the previous pack disagree (carried finding, now recorded)

`POST_PUBLICATION_ADDENDUM.md` states 50/50 byte-exact while the machine readback receipt records 51/51
listed paths. Recorded as an additive currentness erratum (`ERRATA_CURRENTNESS_019.json`); the historical
addendum is left byte-identical so the published pack stays reproducible.

## ER8 — the publisher had no argument parser (previous round's finding, now bounded)

In the previous round a `--help` probe actually published, because the publisher parses no arguments. The
fix is delivered as a candidate with a test in which the network transport is monkeypatched to raise, so a
regression cannot silently publish.

## Positive finding

The canonical Codex executable pin was **stale** (declared path deleted; `declared_exists: False`), which is
what made every governed lane dispatch fail closed. Repairing it was the P0 that unblocked the lane
mechanism itself; it is now repaired with a backup, a one-line diff and a readback, and recorded in
`TIER_A_EXECUTION.json`.

## ER9 — the EXECUTE lane hit the harness timeout while still working, and the nonce check disagreed with the raw stream

The bounded writer ran on rank 1 (`opencode-go/deepseek-v4.1-flash`) for the full 1500 s and was still
working when the harness cut it off: the receipt reads `ok: false`, `code: ERR_LANE_ALL_ROUTES_EXHAUSTED`,
`attempts[0].exit: TIMEOUT`, `used_rank: null`, `completion_evidence.checked: false`.
It nevertheless emitted, in the same receipt, `nonce_present: false` **and** `nonce_present_raw_stdout: true`
with `nonce_source: "item.completed/agent_message"` — the arm did echo the nonce, in a completed agent
message, and the strict field still read absent. This is the documented nonce false-negative class, met
live again. Consequence for the claim: the lane's own binding verdict for this round is **TIMEOUT, not
PASS**, and that is how it is reported. What the artifacts do support is narrower and is stated as such:
the arm served the round through the relay with usage rows bound to the attempt (128 rows after the
attempt's byte offset), the frozen subject was verifiably unmutated (`subject_mutation.verdict: CLEAN`,
5 files before and after, nothing added, removed or changed), and every deliverable was re-executed by the
maker and by the pinned checker.

## ER10 — the writer's own manifest is missing, because the timeout landed before it

`writer/WRITER_MANIFEST.json` was never written: it was the writer's last act, and the harness cut the run
off first. The deliverables themselves are present (`receipt_attempt_numbering.patch` + test,
`nonvacuity_regression.py` + `t2_src/`, `publish_broker.candidate.py` + `publisher_arg_guard.patch` +
test, `fda_guard_hook.candidate.py` + `guard_predicate_candidate.patch`). Reported as a gap rather than
reconstructed: a manifest written after the fact by someone other than the writer would not be the writer's
manifest.

## ER11 — the dispatcher already derives attempt-numbered output directories

`output_dir_policy` in the EXECUTE receipt reads `mode: derived` and resolves to
`HG-KSEOS/var/far-019/EXECUTE/attempt-3-20261016T120703Z` with its own `attempt.marker.json`. So the
canonical dispatcher already keeps attempt-scoped output; what it does not do is protect a **caller-chosen
fixed `--json-out` path**, which is the path a retry overwrites. The writer's T1 patch addresses exactly
that narrower defect, and this measurement narrows the finding that the previous round left open rather
than confirming it wholesale.
