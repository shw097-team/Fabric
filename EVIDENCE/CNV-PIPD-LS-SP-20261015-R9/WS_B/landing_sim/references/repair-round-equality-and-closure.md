# Repair-round closure & equal-rank external conflict (SWOF W*-REPAIR waves)

Rules distilled from an R-series repair on SWOF W2 (HGK-KSEOS governed).

## Equal-rank external-review conflict — resolve deterministically, never by preference

When two same-rank external challenge reports bind the SAME immutable tuple but disagree
on whether something is a blocker (one PASS/NON_BLOCKING, one FAIL/BLOCKING):

1. Do NOT pick by preference, majority, chronology, test count, or model judgment.
   Do not self-issue PASS either way.
2. Adjudicate read-only against the EXACT frozen bytes: probe the ORIGINAL subject SHA
   AND, after a candidate repair, the new head, using the same full-route counterexample.
   `git show <old_sha>:src/...` + importlib-load the old file; import the new file via
   sys.path onto the repo src.
3. To verify a claimed source-candidate exists, do NOT trust a bare full-SHA lookup that
   returns "Not a valid object name": git resolves the bare 40-hex against the object-db
   index and can miss a commit that IS real and IS the tip of an observed branch. Confirm
   via `for-each-ref` (find the branch whose HEAD has the short prefix), `cat-file
   --batch-all-objects`, or `rev-list --all`, then grep content with the ref-qualified
   form (`refs/heads/<branch>:path`) or `git rev-parse <branch>` — never conclude "commit
   does not exist / is a fabricated probe" from a bare-Hex failure alone.
3. Resolve in favor of the report whose blocker actually REPRODUCES on the exact bytes.
   A control (same request WITHOUT the suspect seam) that stays correct proves the seam
   is the injection path and the fail is real.
4. Mount the full production route (the public exported entry, e.g. the gate function in
   rights.py), not just a unit-constructor. The public contract exporting a caller-
   controlled selector IS current-scope reachability even with no in-repo consumer.
5. Only after BLOCKER_CONFIRMED on all Gate-2D predicates open a repair cone. Never widen
   to a broad refactor; delete-over-invent when no authoritative legacy adapter exists.

## Closure is NOT done at commit + green tests

Committing the repaired source and passing the focused/regression suite is NOT HGK closure.
A fresh governance checker must verify the spine: after product commit, run a typed
closure projection that:

- opens the NEW obligation cone under the CORRECT project scope (REQ/TS/WO/ACC + FROZEN
  requirement + workorder result + resolve_acceptance verdict with evidence_ref);
- registers the new subject-bound evidence refs (adjudication / regression / fresh checker
  receipt, each sha256'd);
- issues a per-obligation checkpoint AND ONE final normative checkpoint whose stored
  payload carries `SRC:<new_sha>`;
- PROVES exact-source binding by recomputation: `source_digest == sha256_text(canonical_json(
  payload))` where payload = `project_lifecycles.intent_json['_checkpoint']` (repo_head is
  '' in this schema — not the binding surface);
- asserts `lifecycle.last_checkpoint_id == final_checkpoint`;
- reports a NON-VACUOUS denominator (requirements/workorders/acceptances all > 0) and
  blocking-open == 0 (guard against the 0/0 mis-scoping trap: denominator joins on
  project_id, so rows registered under the wrong project scope are invisible).

Order honored: product mutation -> focused/regression -> FRESH checker PASS -> THEN
closure projection. Projecting before the checker PASS is a sequencing error; skipping the
projection after is an incompleteness failure — both get caught by the fresh checker.

## Backfilling a skipped task-time compile for an earlier round

When a closure round ran without its own Gate-0 compiler pass (readset claimed
`PROMPT_COMPILE_ADJUDICATED_VIA_PRIOR_COMPILER` / "compiler NOT re-run"), backfill it
read-only: it does not taint the frozen product SHA. Build the round's CONTRACT.json from
the previous round's PASSING contract (see `capc-contract-building.md` — including the
duplication-diversify trap), then run `lint` → `activation` → `acceptance` → `compile`
→ `duplication` until all five are `PROMPT_COMPILE_PASS`. Persist `R5_COMPILER_RECEIPT.json`
with a `stages` array carrying per-stage `{stage, verdict, error_count, validator}` (the
compiler's lint/activation/acceptance bodies are byte-identical on PASS, so stage identity
must come from the receipt, never from the returned JSON), then UPDATE the readset's
`canonical_compiler_disposition` and append an `EVD-<ROUND>-COMPILER` evidence item — the
old "NOT re-run" prose in the readset becomes a contradiction and must be replaced, not
left alongside the new PASS. Mirror the receipt + readset byte-identically into the SWOF
evidence tree so both copies hash the same.

## Stale earlier-round receipts pollute the evidence dir

Later rounds reuse round-prefixed filenames (e.g. `R5_APPLY_RECEIPT.json`) and can leave
leftovers from an EARLIER round that carry the same workorder name but a stale
repair_id / candidate SHA / base. Before including any receipt in the return pack:

- validate the identity fields (workorder id, repair_id, candidate, base) against the
  current round; a mismatch means stale/duplicate, not current.
- Judge a round's identity from the SET of round-bound receipts (adjudication /
  regression / fresh-checker / closure projection / readset), not from the apply receipt
  alone: `repair_id` inside `*_APPLY_RECEIPT.json` is chronically stale across rounds
  (e.g. the R3 apply file labels itself R1, R6 labels itself R2). When the other five
  receipt classes all agree on the same round + candidate, a mismatched apply-receipt
  label is a cosmetic/stale field — raise it as hygiene, NOT as proof the round is fake.
- when the authoritative delta is a single commit, prefer listing the exact path set
  (git diff stat) and EXCLUDE stale files from the return pack — and DISCLOSE the
  exclusion in the pack rather than silently dropping it.

## Independent checker must attack the trust axis, not just the lattice

For an authn/authorization repair, the CHECKER (fresh-context VERIFY_ONLY, read-only,
checker != maker) must independently: attempt caller-controlled selector bypass through the
admitted/current route (malformed/typed/unicode/case-variant/duck-typed/subclass values),
verify the AAC lattice (floor+token+decision matrix) AND the CRITICAL/AAC3 holdout, and
confirm no implicit floor can enter canonical verification. Report every counterexample
with its reproduction; keep the transcript full. Checker never patches — routes findings
back to the maker for a new candidate identity.

### Attack the boundary's ENTRY, not only its body (trust-order inversion)

A trust-boundary repair placed INSIDE a downstream function is INCOMPLETE when an EARLIER
predicate decides whether that function runs at all. Pinning the caller request inside the
verifier still leaks when the route/admission predicate derives gate necessity from the
SAME caller-supplied request and returns at a `required == false` / benign fast path — the
verifier and its resolver are never entered. The repair must enforce the trusted resolution
BEFORE the earliest decision that can suppress enforcement (before any early return / NONE /
benign path), not merely at the function the finding named. Reuse the SAME owner-injected
resolver; do not add a second policy engine.

For the checker this is the highest-value attack: after any repair that introduces a
boundary, reproduce the OLD-vs-NEW counterexample through the PUBLIC seam (the exported gate,
not the internal verifier), and vary the fields that DRIVE THE DECISION (operation / risk
tier / permission class / autonomy tier) as well as the fields the boundary compares. Also
enforce request_id parity on the benign path (a resolver returning a foreign request with
otherwise-equal policy fields must still fail closed). A checker that only re-runs the
maker's verifier-level fixtures shares the maker's scope blind spot and returns PASS on a
still-open bypass; report the sweep (gated x benign x route combinations) so coverage is
auditable, and require the exact deny code observed (not just 'denied').
