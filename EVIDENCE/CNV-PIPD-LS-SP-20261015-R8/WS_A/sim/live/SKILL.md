---
name: adversarial-verification-rounds
description: "Use when verifying a frozen deliverable adversarially."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [verification, evidence, digests, manifest, governance, acceptance, fresh-context]
---

# Adversarial verification rounds over a frozen deliverable

The class of work: a deliverable (an RCA, an audit, a repair plan, a research product) must be shown
to survive an independent check before anyone trusts it. The method that works is a bounded series
of rounds: **freeze a digest-bound package → a fresh-context checker recomputes and attacks it →
fold every finding in place → re-freeze → next round**, closing on a stated terminal verdict.

Most rounds do not fail at the checking - they fail at the **handover**: a write path outside the
write-set allowlist, a delivery worktree left dirty, a copy taken inside the subject, an acceptance
lane entangled with the root-cause lane, or a lane failure blamed on "the model" from a self-reported
field. The rules for briefing and handing over to a verifier lane are in
`references/verifier-lane-handover.md`; read it before you write a lane brief. Checker-side binding and false signals: `references/checker-binding-and-false-defect-signals.md`. The launcher, the admission
gate in front of it, and the counterexample checklist that shows how a gate pretends to protect you are in
`references/lane-harness-and-admission-gate.md`.

## When to Use

- A deliverable must be defensible to a third party, not merely plausible: governed audits, incident
  write-ups, repair proposals, RCAs — anything where "I checked it" is not evidence.
- The checker's verdict is an ARTIFACT, not a terminal message, and a long item list must be sized
  against the checker model's own context ceiling. Pre-create the verdict file, refuse an untouched
  skeleton, and shard. Contract, sizing, control-acceptance test and the false-green shapes to hunt for:
  `references/verdict-artifact-and-budget.md`.
- Evidence has to be added to an **already-sealed corpus** without moving the sealed binding, and a
  checker selects which files it reads by name — run `references/sealed-evidence-corpus.md` before
  naming or committing any new artefact near a frozen manifest.
- You are staging, running or reporting an **independent acceptance lane** (AO / VERIFY / host UAT) →
  run `references/independent-verification-hygiene.md` (where the checker's copy may live, the
  discovery-vs-effective-load tiers, the read-back check on evidence your own lane writes, and how to
  mark a superseded candidate branch so nobody accepts bytes no one tested).
- A claim about what *must be done* has to be earned by a measurement, and a ruling the owner has already
  given must not be re-raised — read `references/finding-classification.md` before writing any finding,
  open item, or "should also…" sentence.
- Artifacts are published with digests and someone else will recompute them from the raw sources.
- A round's verdict came back with findings and the corrections have to be provable, not asserted.

Do NOT use it for routine edits: one review pass is enough when nothing is published or re-measured.

Two properties are non-negotiable: the checker is **not the maker** (fresh context, no shared
history), and **every FAIL verdict is preserved verbatim** in the package. Never rewrite a FAIL as a
PASS, and never present a revision as having passed a check it did not receive.

## Procedure

1. **Decide the terminal state before round 1.** Write the verdict rules into every dispatch: PASS
   requires the checker's own recomputed digests to match, all declared mirrors byte-equal, every
   manifest artifact to match, and no residual finding of blocker/major severity. A new minor or
   observation makes it PARTIAL with those items in a `carry_forward` list — a legitimate final
   state. Declare the last round as the last round, so the series ends closed.
   State the **closure condition** as an explicit "if this recurs, close with FAIL + carry_forward
   instead of adding a round" rule, and put it where the checker can read and invoke it (the freeze
   receipt is the natural home). A checker that holds the condition terminates the series itself.
   Without one, "one more round" becomes the mechanism by which an unfixed class is reported as
   progress; with one, stopping is a governed outcome, not an abandonment. Honesty about the round
   count is not a substitute for a rule that ends it.
2. **Build the package deterministically.** One builder script writes the document, then the manifest
   (artifact list + digests + `as_of` + `post_build_writes` + `excluded_by_construction`), then a
   freeze receipt naming the document digest, then the byte-identical mirrors. Re-running the
   builder unchanged must reproduce the digest — if it moves, something in your inputs moved.
3. **Sweep the freeze boundary** before dispatching: only the files you declared may be newer than
   the document. `find . -type f -newer "$DOC"` is the whole check.
4. **Dispatch a fresh-context checker** with an explicit JSON output contract. Always include a
   `quotation_check` array (suspect phrase → occurrences → all-are-quotations → exceptions) and a
   `carry_forward` array. Tell it which files count as narrative text and which are records.
5. **Fold the verdict in place.** Every finding gets a fix in the artifact that carries the claim
   (repair table row, task list item, spec, front matter, checkpoint), plus one errata row recording
   what was superseded and why. An errata annex alone is not a fix.
6. **Re-build, re-mirror, sweep, dispatch the next round.** The next round adjudicates the previous
   round's residuals by name and re-measures the raw artifacts from scratch.
7. **Close out honestly:** per-round verdicts, what each round changed, the final verdict as stated,
   and the unresolved/carried items listed one by one.

## Refusal-first entry routing (PARTIAL_ENTRY_ONLY)

Refuse before acting when any of these hold:
- R-01 subject not frozen (no master/stage digest) - do not open a round.
- R-02 required arm/checker unbound or self-declared - refuse; never swap in a healthy-looking arm.
- R-03 evidence summary-only, stale or foreign - refuse; recompute from raw bytes.
- R-04 guard/comparator passes on missing input (vacuous pass) - refuse; demand PASS/FAIL/INCONCLUSIVE.
- R-05 promotion is not acceptance - no maker self-accept, no commander-signed receipt.
- R-06 a human token closes only what it names - never extend it.

Index (this file holds the protected cores; the topic reference holds the rest, verbatim):
| Rules | Subject | Where |
| 1-6 | errata in place, manifest self-exclusion, derived counts, tier loss, as-of stamps | topic A |
| 7-11 | claim ceilings / quotation-coverage / model-binding | inline below |
| 12-32 | write ceilings, self-check, arm-that-serves, budget, mirrors, durable routes | topic B |
| 33 | human-act authority | inline below |
| 34 | brief bound by rule, not a frozen SHA | topic C |
| 35 | CLAIM-vs-CODE agreement as its own axis | inline below |
| 36-38 | preimage byte-identical, delivered tree, self-disclosed limits | topic D |
| 39-40 | wiring contract / frozen instrument | inline below |
| 41-58 | measurement apparatus, fail-closed probes, subject binding, claim boundaries | topic E |

- reference: `references/topic-source-remainder.md` (all complementary source bytes, verbatim).

## Protected rule cores (verbatim)

7. **Claim ceilings must separate subject stores from the control plane — and be fixed everywhere.**
   "No canonical mutation" is false if the round wrote audit records, board cards, a proposal, or
   (with a non-hermetic suite) extra events. State: no mutation of the *subject* stores, plus the
   enumerated control-plane writes and disclosed side effects. Then grep the whole package for the
   headline: front matter, summary rows, logs and embedded copies each carry it, and one surviving
   denial rejects the revision even after the others were fixed.
8. **Explain quotation vs surviving claim in every dispatch.** The package must keep errata rows and
   earlier verdicts verbatim, so superseded wording legitimately reappears inside them. Without an
   explicit instruction plus a `quotation_check` block, rounds flag their own records as surviving
   claims and the loop cannot converge.
9. **Anything you cite must be IN the package.** A transcript, receipt or log referenced by an
   outside path is scored as a missing artifact. Copy them into the run directory so the manifest
   binds them by digest (embed only the newest if the document would bloat) and list genuinely
   external paths under `external_citations` with the reason.
10. **Labels and trend words must match the numbers they sit beside.** A heading or Q&A row that lags
    the register (naming an initial range after the register grew) is a finding, as is calling a
    count "decreasing" beside its own `3 / 3 / 7 / 5` series. Restate the registered range, and say
    which dimension actually improved — usually severity, not count.
    The same discipline governs a BLOCKING TOTAL, which is the number a reader turns into "how far from
    done". A multi-round ledger re-files ONE root cause under a fresh id each round (four ids here were a
    single bridge-config defect seen from four angles), so the raw count overstates the work remaining and
    is not the number of defences missing. Group by root cause, separate the defects touching the artifact
    that will actually SHIP from those touching only a superseded or comparison artifact, and quote both
    numbers — the count is a claim, the grouping is its evidence. This matters most when you are asked
    whether the round can close: "N blocking" and "2 distinct deliverable blockers" are different answers
    and only the second one is actionable.
11. **Model identity is declared, not attested — and a role name does not route it.** A runtime
    footer is a self-report; nothing in the package proves which model produced an artifact. State
    identity as declared. Separately: naming a lane "the VERIFY lane" in its dispatch text changes
    its instructions, not its model — if the platform routes children from one global pin, every
    lane runs that model whatever its charter says, so an ordered per-role model scheme cannot run
    through that surface at all. That pin is also shared mutable state, not a stable route: every
    workstream on the host reads and writes the same value, and it has been found EMPTY at the start of
    a round even after a previous round recorded restoring it. Re-read the live config FILE (not a CLI
    readback, and never a delegation banner) immediately before a dispatch, treat the pin as a
    bootstrap good for one dispatch, and note that making the scheme hold for all LATER dispatches
    requires a scoped route (a per-task/per-card override) or a pre-dispatch gate that refuses a
    dispatch whose model equals the maker's. **Context separation and model separation are independent axes:**
    fresh-context lanes can attack a package effectively while the model axis is collapsed onto the
    executor's model, which is exactly why a long green round loop does not evidence that the ordered
    SoD scheme executed. Report the axes separately. And when the executed model deviates from the
    ordered one, writing the actual value into a field is not disclosure — name the deviation in the
    deliverable and in the reply.

    **Never report a mandated arm as unavailable without probing it.** "No usable credential / no
    bindable lane" is itself a claim, and one such blocker was found false by a three-second one-shot
    against the very arm declared unreachable (the credential pool listed it; other sessions had used
    it heavily). An untested unavailability claim is an invented blocker, and its damage is subtler
    than a false PASS: it converts a PROCESS MISS (you never routed the work through the arm) into an
    ENVIRONMENT FACT (the arm cannot be reached), which is exactly the rounding-up this user rejects.
    Probe the arm through its own entry point, print the result, and only then state availability — or
    state plainly that the arm was never exercised.

    **The pin binds at SPAWN, and that is what makes an ordered scheme runnable.** A child keeps the
    model it was spawned with; flipping the pin afterwards does not retarget a running child. Verify
    that once at call granularity — grep the runtime log for the child session's per-call
    `API call #N: model=... provider=...` lines and confirm every call held the spawn model even
    AFTER the pin was restored — then rely on it: order the dispatches flip -> dispatch -> restore,
    repeat per lane, and let the RUNS overlap while never leaving the pin flipped past the last
    dispatch. That turns the pin from "bootstrap good for one dispatch" into a usable per-lane routing
    surface, and the same log check is your evidence of which model served which lane. A cheaper and equally
decisive confirmation at DISPATCH granularity: query the runtime's own session store for the child rows and
read their model column (in Hermes, `SELECT id, model FROM sessions ORDER BY rowid DESC LIMIT <n>` against
`state.db`), which is where the served model is actually recorded — the delegation manifest records
provider/model as NULL there, so it is NOT the place to confirm a pin, and reading it as "no model" would
retract a pin that worked. Restore hygiene: back up the config FILE before the flip and copy it back
afterwards. Setting the key back to an empty string leaves a stray empty entry and makes the restore a diff
rather than byte-identical; diff against the backup and say which you achieved.
33. **A human decision closes only what it names - record the token verbatim, and never let a PASS
    become acceptance.** When the owner answers a decision request, write a SEPARATE decision record
    that quotes the answer verbatim as the authority token, binds the covered artifacts by digest, and
    classifies the decision by the state machine rather than by tone: approving a SCOPED artifact is a
    scoped local approval, not promotion, release, deploy or live adoption, and everything the token
    does not name stays PENDING and is listed as such. A defect the owner accepts as a bounded
    disposition is DISPOSITIONED, not repaired - keep the failing observation standing, never restate
    it as green, and carry every other blocking item forward. Number the decisions when you raise them
    so the answer can name one. Raise each decision PRE-ANALYSED rather than as a bare question: state the
    contention, the verified facts behind it, the FAR root cause, and the recommended low-resistance option
    FIRST with the alternatives behind it, so the owner can ratify in one line (`A1 = ACCEPTED_AS_IS` /
    `AUTHORIZE_REBUILD`). A decision pack that forces the owner to re-derive the trade-off is work pushed
    back up the chain; one that ends every item in a pickable token is closure-ready. Recommend the option
    that requires no engineering action when the honest answer is "the current state is already correct".
    **Some rulings are a CONTRACT REDEFINITION, and the deliverable must say so in those words.** When a
    threshold is proved UNREACHABLE rather than merely missed (measured: an absolute per-artifact byte
    budget against a lossless floor more than an order of magnitude above it, with the artefact's own size
    unchanged), the honest repair is not a loosened number but a re-specified DECIDING metric — a
    scale-invariant rate — with the unreachable absolute and every noisy/timing-dependent row demoted to
    non-voting ADVISORY. Keep the historical FAIL as a row that STILL PRINTS on every run, add a regression
    guard against a frozen baseline with a single writer flag for re-freezing, and cite the adjudication
    record as the metric's own `source_of_truth` inside the tool. Then disclose the pass for what it is:
    the DEFINITION changed, not the artefact — the artefact hashes identically before and after, so "the
    performance problem is fixed" is false at exactly the moment it is most tempting to write. A demoted
    row is demoted, never deleted, and the suite should assert BOTH that the preserved FAIL is structurally
    visible AND that the deciding row is the new one.
    Carrying out a bookkeeping ruling is frequently a READ, not a write: before editing a canonical
    register or artifact, check whether the recommended projection is ALREADY present in the
    authoritative field — a row can carry a fresh `state` beside a stale legacy `status`, and the
    recommendation may have been phrased against the legacy field alone. Run the artifact's own
    consistency check to confirm, and report "already satisfied; no canonical write made" rather than
    performing an edit so the response looks responsive. An unnecessary write to a canonical store is a
    side effect to disclose, and the user's prohibitions do not exempt edits made in a good cause. Do not try to bind, in that record, the post-write digest of a file the
    same turn will rewrite (a file cannot hold its own post-write hash) - log those in a readback
    addendum and name which bound values are stale by construction. The closure record carries an
    explicit `is_acceptance=false`, a list of what the token did and did not authorize, and the
    still-open decisions; the orchestrator never signs the acceptance receipt.

35. **Score CLAIM-vs-CODE agreement as its own axis; a receipt that overstates the code is a blocker.**
    A maker receipt is a claim ABOUT the artifact, and it is the text a third party reads first. When a
    receipt promises a property ("a missing provider OR model fails closed, never OK"), read the code
    condition and reproduce the case against it; a receipt describing behaviour the code does not
    implement is a blocker even when the product behaviour is defensible. The closure is not "fix the
    code" — it is MAKE THEM AGREE, and both directions are legitimate: tighten the code to the claimed
    property, or narrow the receipt and the docstring to what the code does. Name which direction was
    taken, and have the delta round verify the agreement literally (read the receipt wording AND the
    code condition, then state whether they match). Corollary: **your own probe expectation string is
    not the contract.** When the artifact documents its own fail-closed status (an explicit UNDETERMINED
    for an incomplete identity), a probe asserting a stricter neighbour status (REFUSED) is the thing at
    fault — reclassify your expectation and say so, rather than demanding the maker rename its status.

39. **Contract for the WIRING, not just the behaviour — a gate that nothing invokes is a false closure.**
    When the change under verification closes a control gap, the decisive question is not "does the new
    component gate correctly" but "does any code path CALL it, and does anything READ the state it
    emits". Put both in the contract as separate numbered claims, and require the evidence to be greps
    that EXCLUDE the round's own worktree: the authoring directory trivially contains the new files, so a
    search that includes it proves nothing. Two measured shapes — a launcher that calls only the
    seal/mint helper and never the verify runner (so the write path still exits 0 with its gate
    unsatisfied, while the helper's own tests are green), and a consumer whose repo-wide caller count is
    zero. Distinguish three states in the verdict and never let one stand for another: *would fail closed*,
    *gates when invoked*, *is invoked*. Report DETECTION_ONLY with the callsite quoted when the third is
    unproven, and hand the missing wiring to the owner as a design decision rather than a maker defect.
    Corollary: an officer's PASS returned against a contract that never asked the caller question is not
    evidence about the wiring — it is evidence about the question that was asked, so fix the contract
    before reading the verdict as closure.

40. **The judging instrument must be inside the freeze, not amended after it.** Freeze the verify
    contract and pin ITS digest in the same operation that pins the subject digests. A contract extended
    afterwards — the natural reflex when the maker discloses a new limitation mid-round — is itself an
    un-pinned artifact whose bounds moved during the round, and both the officer and any challenge lane
    will (correctly) score its additions as lower authority. If the addition is truly needed, re-freeze
    the contract, record the dual pin exactly as for a superseded subject file, and make the verdict name
    the contract revision it read. Never edit the instrument to match a finding and then present the
    amended version as the one that governed the round all along.

