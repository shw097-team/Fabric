# Validator / control-authoring lessons (L12–L21)

Each lesson is an imperative rule plus why. These came from authoring additive acceptance-integrity
predicates over the HG-KSEOS control plane, delivering the ChangeSet that implemented them, and having
both adversarially checked.

## L12 — A validator that cannot run must emit NOT_APPLICABLE, never `clean`

A predicate that silently returns `[]` on an unrunnable input (empty descriptor list, absent selector,
missing required-matrix definition) is a **vacuous pass**: the caller reads `[]` as "all valid", and the
whole control silently no-ops. Give every predicate an explicit "inputs unresolvable → NOT_APPLICABLE"
branch, and make the test class assert it. An independent checker showed only 1 of 7 predicates in a
first revision honoured this.

## L13 — Adversarially test each predicate for OVER-BREADTH on legitimate artifacts

A predicate that catches the defect it was written for but ALSO fires on legitimate artifacts is worse
than no predicate — it fail-closes the acceptance path. Counterexample shapes to test on every control:

- an artifact that **negates** the token — `MUST_NOT_CLAIM_X` still *contains* `X`; substring removal
  is insufficient. Scan a preceding window (~24 chars) for a negation marker instead.
- an artifact that **declares itself** carried / immutable / cumulative — needs an explicit declaration
  escape hatch, not merely a path-based (`historical/`) exemption.
- a nested field that legitimately names a DIFFERENT namespace (e.g. an out-of-tree publication naming
  the evidence commit) — fire only when it matches NEITHER current field.
- a receipt carried under a canonical **alias key** (`checker_receipt` vs `independent_receipt`).

Encode each counterexample as a permanent regression test class, named after the fact that a checker
found it. Also test the mirror-image false NEGATIVE: substring coverage lets a case that is merely
*mentioned in prose* count as covered — require an explicit machine-readable list instead.

## L14 — A fixture runner must call the SHIPPED predicate, not an inlined copy

A runner that hand-inlines a reduced re-implementation of the predicate under test produces evidence
numbers that exercise **divergent code**: the numbers look right while the shipped module is untested
by the run. Have the runner materialise the input into a temp tree and call the shipped module, and
record the predicate's own identity in the result (`predicate_source`). Related trap: `git show
<sha>:<path>` needs the **subtree root** prefix; a missing prefix makes every read fail and silently
yields 0 findings — which reads as "clean".

## L15 — After any structural splice, re-read the signature and re-run the suite

An index- or anchor-based splice inside a long file silently deletes adjacent helpers and constants
(the module still imports, so only runtime use fails). Immediately after a splice: confirm the edited
function's signature is intact, confirm any helper it used still exists, and re-run the full suite.
A predicate whose `round_of` argument became required instead of optional, or whose `read()` helper
vanished, only shows up at call time.

## L16 — Attribute test failures EMPIRICALLY by reverting, never by asserting

"That failure is pre-existing" is a claim, not an observation. To prove a change caused zero
regressions: copy the touched files aside, restore the pre-change versions, re-run the failing set,
and confirm the SAME failure set appears; then restore your change. Record it as
`PRISTINE-EQUIVALENT` with the exact failing test ids and `attribution_caused_by_this_change: 0`.
This is stronger than reading the test name and guessing — the failing tests may read a corpus or a
path the change never touched, which is exactly what the revert proves.

## L17 — Establish control-plane claims against the LIVE source, not the proposal

Before implementing a control, every "the control plane lacks X" premise must be re-derived from the
live source and recorded with the command that proved it (e.g. grep the schema for a sequence column,
grep the package for a table). A research/proposal artifact may mark the same question UNKNOWN; an
UNKNOWN is a to-do for a fresh inventory, never a licence to assume. Inventing a field name because
none was found is the failure mode this rule prevents.

## L18 — Inventory the existing convention BEFORE proposing any schema or signature change

Grep the codebase for an existing precedent first: if ordering is already done with SQLite's implicit
`rowid` somewhere, then a "needs a new monotonic sequence column" conclusion collapses to a one-line
ordering fix — no migration, no shared-core change. Minimality is a standing user requirement: run the
inventory, then let the scope shrink to what is actually missing.

## L19 — A source-scanning guard must match the QUALIFIED form of the pattern it bans

When a guard or lint bans a pattern in source (a bad ORDER BY, a forbidden API call, a banned import),
match the qualified variants too, not just the bare form: `(\w+\.)?` for `alias.` / `schema.`, and the
quote/backtick variants for SQL and shell. A literal pattern silently passes a real defect site — a
checker found `ORDER BY v.created_at` surviving a guard whose regex was `ORDER BY created_at`, i.e. an
entire site of the very class the guard existed for. Test the guard itself with a positive fixture of
the qualified form, so an alias-blind guard fails its own test instead of the review.

## L20 — Never append an inline comment to a line that continues a multi-line expression

In Python a `#` placed after the closing delimiter of a multi-line call or string runs to end of line
and **swallows the continuation token** — the trailing comma or operator. The statement silently
changes shape: here a string literal became the callee, surfacing only at runtime as `'str' object is
not callable` in an unrelated test. Put the comment on its own line ABOVE the expression. After any
edit that inserts a comment near a multi-line expression, run the focused tests for that module
immediately — the symptom appears in a test you did not touch.

## L21 — Stage a governed ChangeSet by explicit file list, never `git add -a`

In a repo whose working tree already carries unrelated modifications, `git add -a` / `-A` sweeps that
foreign work into your ChangeSet, which destroys attribution and makes the rollback command wrong.
Stage the exact paths belonging to the ChangeSet; verify with `git diff --stat <paths>`; then confirm
`git status --porcelain <paths>` is empty afterwards. One ChangeSet per commit, and put the ChangeSet
id, the independent-checker verdict, and the literal rollback command in the commit message so the
commit is self-describing. A ChangeSet whose commit cannot be reproduced or reverted from its own
message is not a governed deliverable.
