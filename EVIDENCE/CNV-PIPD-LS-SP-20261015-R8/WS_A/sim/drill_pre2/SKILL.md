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

## Rules

1. **Apply errata IN PLACE, not only in an errata annex.** A checker judges the operational tables,
   the task list and the acceptance tests; an annex that leaves them saying the old thing is scored
   PARTIALLY_RESOLVED ("acknowledges the blockers but does not consistently update the operational
   repair table"). Keep the annex as the audit trail of what changed.
2. **A manifest must not list its own digest or a post-build file's digest.** Written last from a
   directory walk it carries the *previous* build's digest for itself; a checker counts the
   mismatches and calls them undeclared. Exclude self-referential and post-build files from
   `artifacts`, carry the document digest in its own field, and declare `post_build_writes` up
   front — including the next round's output file.
3. **Manifest counts must be self-consistent and separately labelled — and DERIVED, not typed.** The
   artifact array length, the excluded-by-construction list and the raw directory-walk total are
   three different numbers; emit and print all three, or a checker reads the mismatch as a defect.
   Classify entries by rule (directory prefix, name pattern, dotfile, self) and have the builder
   rewrite any count sentence it embeds in the prose between markers. A literal file list or a
   literal count in a document goes stale on the very next added file, and every stale copy is a
   separate finding in a separate document. Derivation makes the documents unable to diverge from
   the manifest by construction instead of by discipline.
4. **Tier loss accounting: proven / candidate / unverified — never one total.** Only a row you can
   show existed and is gone is *proven* (it appears in a rescue export). An id-sequence gap does not
   prove the row ever existed → *candidate*. An earlier estimate you cannot reproduce is *unverified*,
   not disproved. Single totals get rejected in turn as understated then overstated.
5. **Every live metric needs an as-of stamp and an observed range.** Counts in a running store drift
   by hundreds between observers. A placeholder timestamp (`01:0x`, "recently") in a comparable field
   is scored as an un-stamped claim — write the value you actually measured and when.
6. **Classify repairs by what they touch, not by intent.** Restoring a database or a skills tree
   *into a live home* is a canonical change even when the content is "only additive": stage first,
   then gate, backup, readback. Labelling such an item additive is itself a finding.
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
12. **A fail-closed gate can block a checker's own output write** (matcher over the whole payload,
    paths included). Keep payloads short, avoid pasting guarded substrings, report the block — never
    bypass. An admitted run directory should be whitelisted, and an over-broad matcher is a defect
    needing its own negative test (a genuinely secret-bearing payload must still be refused).
    The trigger is usually a literal guarded substring in YOUR OWN payload — an unrelated round trips
    it merely by naming the guarded subject — and the marker set is PER TOOL: broad for shell
    commands, plus the bare subject token for the file-writing and code-execution tools, so a payload
    the shell accepts can still be refused. Audit your own text against the classifier before
    concluding the authorization mechanism is broken. When the caller HAS authorized and a call is still
    refused, inspect the AUTHORIZATION STORE before blaming the matcher: the token is per session and
    carries an expiry, and a refresh guard that compares identifiers as strings
    (`str(old) >= str(new)`) can never refresh an expired token, so every later authorization is
    silently a no-op — compare identifiers numerically. Two more measured facts: a child lane does NOT
    inherit the parent session's authorization — put the authorizing words in the child's OWN prompt
    and tell it to cite the registered route id when a call is refused, then watch it complete; and
    prefer the code-execution tool over a long shell heredoc to create a file, because a long heredoc
    can be mangled by the wrapper (parse errors) before the guard is ever reached.
13. **Self-check before the checker runs.** Grep every file that carries a claim you just corrected
    for the wording you meant to remove, and for un-stamped live numbers; verify each hit is a
    quotation of superseded text, not a surviving claim. Most findings are catchable one round
    earlier this way.
14. **A build that crashes after writing its outputs is still a broken build.** Fix it and re-run: a
    deterministic builder reproduces its digest, and a moved digest means the crash was hiding a
    content change.
15. **Never restate a "current" value inside an append-only claim file.** Errata, changelogs and
    correction notes that name the present revision, count or version go stale the moment the next
    artifact is added — and the first reader to notice scores it as a fresh finding, not as a fix.
    Write the *policy* ("current values are authoritative only in <generated artifact>") and let the
    generated artifact carry the number. Hand-restated current values were the single most-repeated
    defect class in one loop, surviving four consecutive correction attempts.
    The rule bites hardest on a file that sits INSIDE the measured surface: a document quoting the digest
    of the subject it belongs to can never be current, because committing the digest changes the digest.
    Measured: a first-screen banner naming the round's commit/tree/digest as "the current subject" was
    scored FAIL, then PASSED once it named only the immutable BASELINE, marked the superseded attempt's
    identity as history, and pointed at an evidence directory the product digest EXCLUDES as the external
    binding entry point — stating in the file that it deliberately carries no digest for the current
    subject because it is inside the measured set. Expect the checker's own wording to ask for exactly
    that ("supply an external binding entry point; do not require the file to self-reference its digest"),
    and give the entry point a reproduction command so any reader can re-derive the value themselves.
16. **Do not enumerate disproved values as a tombstone list.** A "values disproved so far" list
    invites misattribution: the round that *measured* a value gets written up as the round that
    *disproved* it, and the correction becomes the next finding. Keep the superseded artifacts as the
    authority and say only that they are the authority.
17. **A "preserved verbatim" claim needs a measured, per-item completeness test.** An append-only
    log that truncates its payload (`…(+N chars)`, `...(N bytes)`) cannot support a blanket
    preservation claim, and neither can the opposite blanket denial. Run an exact-substring test over
    every item, report "N of M intact", and scope the claim as "the full set is not independently
    verifiable" — never "no item is", which is equally false and equally checkable.
18. **Negative-test every guard / refusal script from the checker lane.** A refusal path that dies on
    a parse error exits with the interpreter's first code (1), not the intended one (e.g. 3), and
    superficially looks like it ran. Proof requires a fresh checker executing it with the escape-hatch
    env var removed, plus before/after byte + digest + mtime snapshots of the whole tree showing
    nothing was written. A guard that has never been negatively tested is an unverified guard. Read the
    tool's own verdict field too, never its exit code alone: argparse's 'unrecognized arguments' also
    exits 2, so a designed exit-2 refusal and a mistyped flag are indistinguishable from the code.
    Confirm the flag names it really accepts (`--help`) and the exact spelling of enumerated values
    (a lane enumerated `VERIFY_SECURITY` refuses `verify_security` as an unknown lane). Exercise the
    ADMIT case as well — a gate that refuses everything for an unrelated reason looks like it works.
19. **An arm that answers a probe is not an arm that can serve as a lane.** A direct completion
    returning 200 within seconds is not evidence a model can carry a lane; exercise the arm in the
    lane's own request shape (a real subagent turn) before accepting or rejecting a lane-model claim.
    The measured failure mode is an arm that answers a raw probe instantly and then never completes a
    single model call as a lane. Report the three states separately: listed / answers / usable as a lane.

20. **Attribute a modification by mtime against the lane's own window, never by the working tree's
    status.** A governed repository is usually shared with concurrent workstreams, so `git status`
    listing a file as modified says nothing about who modified it. Record each lane's start and end
    timestamps, then check per-file mtimes: entries outside that window belong to someone else and
    must not be credited or blamed. A lane's claim about what it did *not* touch is checked the same
    way, and a claim that the tree is clean is meaningless without the window. Derive each window from
    the process's own create time (the lane's launcher PID), never from a hand-typed epoch literal: one
    wrong constant made every guard row read `modified_during_round=True`, inverting the whole table at
    once. Sanity-check the derived window against one known-old and one known-new file before trusting
    any row of it.
    Before blaming an external tool or a concurrent workstream for churn you did not cause yourself,
    exclude the writers YOU dispatched: check whether a child you launched was running in that window and
    whether its own restore or cleanup step would produce exactly the observed state. Skipping this step
    produced two confidently-published external explanations that were both false; the machinery of that
    attribution order, and of what pollutes a boundary signal besides a source change, is in
    `references/git-tree-integrity-signals.md`.

21. **Budget a fresh-context checker in its dispatch, or pay for a run that yields no verdict.**
    An unlimited checker reads everything, re-reads ~200K-token contexts per call, and can be
    interrupted after ~45 minutes with no artifact written at all. Put the budget in the prompt: a
    tool-call cap (~30), a per-command output cap (~2 KB, via `grep -c` / `head -c` / `tail -3`), a
    files-read cap (~8), and a ban on using the interpreter to read files. Require the verdict file
    to be written FIRST as a skeleton with a TODO marker and refined at most three times, so an
    interruption still leaves a usable partial verdict. Record the interrupted attempt (duration,
    call count, absent output) as evidence instead of quietly re-dispatching.

    **Give every attempt its OWN immutable log path.** A re-dispatched lane that writes to the same log
    filename destroys the first attempt's raw output, and the first attempt is often the only record of a
    rejected launch shape (an uncontained sandbox, a refused shell). Version the path per attempt
    (`log_<wo>_a1.txt` / `log_<wo>_a2.txt`) and never overwrite a log a verdict or a brief already cites.

    **Read BOTH exit codes: the wrapper's and the worker's.** A lane whose log ends `worker_exit=124`
    while the outer process returns 0 — and the completion notification therefore reads "completed
    normally" — was killed at its own budget and never ran its closing acceptance command, so no receipt
    exists whatever the outer code says. Inspect the log for the worker's own exit marker, and when it is
    a timeout, re-run the gate-bearing measurements from the supervisor side instead of reading the
    absence of a receipt as a pass.

    **The cap alone does not yield a verdict — contract the WORK SHAPE too.** A checker left to its own
    devices spends every turn on many SMALL commands (one directory listing, one text search, one test
    invocation) and
    the run ends with the skeleton still carrying its TODO marker. Raising the cap without changing the
    shape just buys more small commands. Require a two-step contract: STEP 0 writes the skeleton
    verdict file; STEP 1 is ONE script that performs every listed check in a single interpreter run and
    rewrites the verdict itself, driven by ONE tool call; then reply with the verdict and paths. Batch
    the check list into that script (import the module under test rather than shelling out per case).
    Without the batched step the budget increase changes nothing, and a skeleton still holding its TODO
    is not a partial verdict — it is the absence of one.

    **A lane that dies with NO verdict leaves a residue you grade as a TALLY, never read as one.**
    Measured: a checker ran to its wall-clock budget and was killed by the timeout (`exit 124`) with its
    per-case records complete and its verdict file absent. The salvage is real but it is not a verdict,
    and that distinction has to survive into the deliverable: label the artifact a DERIVED TALLY with an
    explicit `explicitly_not` list (not the verdict, not a pass, not a substitute for the signer),
    preserve the raw per-case records in the round directory, and state plainly that no signer exists.
    Then adjudicate every recorded FAIL from the FAILING RECORD'S OWN captured argv/exit/stdout — a case
    whose captured output contains the expected value under a NESTED key while the harness read a
    top-level key is a harness extraction defect, and a case that failed once and passed on every later
    pass is a first-pass transient; grade both as such, with no product change, citing the re-run
    observations. Finally, declare the tally's COVERAGE LIMIT: a case block the lane reported only as
    prose in its log (never as machine-readable rows) is counted nowhere, so say the tally UNDERCOUNTS
    the run's real coverage instead of presenting its case ids as the complete set — an undercounted
    tally published as complete turns a single witness with no verdict into apparent independent
    confirmation.

    **When a lane dies mid-run TWICE in the same class, change the SHAPE instead of re-dispatching it.**
    Measured: two checker lanes ended after writing only the skeleton, each time with the transport failing
    mid-stream (`responses_websocket: HTTP Error: 426`) right after the lane had pulled the 443-line subject
    and its 423-line test module into context. The third attempt must shrink what the lane must READ. Have the
    ORCHESTRATOR author a deterministic harness that performs every check in one interpreter run and prints a
    single JSON blob, and DISCLOSE that authorship in the brief; the checker then (a) reviews the harness as a
    referee — could it report a false PASS, does it measure what it claims — (b) re-runs it once, (c)
    hand-reproduces at least two DECISIVE probes without it, and (d) judges each row on both. Judgement stays
    with the checker; only the context that killed the lane is removed. Name the input files explicitly (three
    small ones, not the subject sources) and forbid exploring anything else. Expect the harnessed rows to be
    its own bug surface — see rule 42.

22. **Account for artifacts by recomputation, and never rewrite the historical receipt.** Compare
    every recorded digest against one you recompute from disk yourself. A receipt is a historical
    record: a later DECLARED change legitimately leaves its values stale, and the remedy is an
    accounting layer, not an edit to the receipt. Emit that layer with each mismatch attributed —
    either a change this round declared (name the file, the old and new digest, the reason, and the
    backup) or an unexplained one handed to the independent checker as an open finding — and report
    the counts (match / mismatch / missing) plainly. An artifact whose recorded digest cannot be
    reproduced AND cannot be attributed is a finding, not bookkeeping. Recompute over the artifact's
    PRODUCT file set — the files the deliverable actually consists of — never over the whole tree: any
    run of the artifact's own suite writes fresh randomised fixtures into the tree, so a whole-tree
    digest moves every time you exercise the thing you are verifying and can never be pinned. Record
    the product digest and the excluded scratch root explicitly, and keep your own probe scratch
    OUTSIDE the artifact; if you already wrote into it, MOVE the scratch out rather than deleting it
    (a non-destructive round forbids deletion, and the move preserves the evidence), then re-verify
    that the product files still hash to the maker's own recorded post-hashes.

    **Hash the COMMITTED bytes, not the working-tree file, whenever the repo normalises line endings.**
    With `* text=auto eol=lf` (or any `eol`/`-text` attribute in play) a checkout on a CRLF host writes
    files whose sha256 is NOT their blob's, so a digest taken from the working tree cannot be reproduced
    from a clone and a comparison against the repository's own bytes fails on content that is identical
    in the repository. Take the hash from `git cat-file -p HEAD:<path>`, or normalise the file to LF and
    commit that, and record which of the two you hashed — for an artefact you are ABOUT to commit as
    well, since verifying the editor's copy proves nothing about the blob other consumers will read.

    **Re-verify a FETCHED remote artefact with the subject's OWN verifier, not only a raw sha compare.**
    Fetch the pushed blob/tree down and run the repository's own `--verify` (or equivalent) against those
    bytes, then record its exit code, the ref the bytes came from, the branch you pushed, and the
    branches you did NOT touch. A byte compare proves transport; re-running the verifier proves the
    artefact still means what it claimed when it was built, and it is the only step that catches a
    binding a push silently invalidated.

    **A digest handed to an EXTERNAL reviewer must be attached to the exact bytes of the hand-off, and
    the reviewer's claimed digest is a fact to REGISTER, not to match.** An evidence document that is
    appended to after review can never reproduce the reviewer's digest, so record and freeze the
    revision that was read at hand-off. When a claimed digest cannot be reproduced by ANY local
    revision, reconstruct the pre-append revision as the pre-image (that is which bytes the reviewer
    could have hashed), register the mismatch as an identity finding with its own owner, and never
    answer it by restating the file's current hash as though the two agreed.

    **When the repair folds in an INDEPENDENT lane's findings, the maker's post-fix self-test is a
    self-report, not the closing evidence.** The pre-fix verdict does not cover the repaired bytes, so a
    green suite re-run by whoever made the change cannot close the defect the lane reported — schedule the
    narrow delta lane over the FIXED revision and state the fix as UNVERIFIED until it returns. Never let
    "N/N tests pass after folding the findings" sit beside a defect as though it answered it.

23. **Repair where the verdict points, then re-verify the REPAIR SET, not the package.** A verdict
    that names defects splits the work by role: the maker repairs, the checker never repairs (its own
    verdict says disposition belongs to the owning lanes), and the closing round is a NARROW
    re-verification — re-run the refusal and admit matrix, both suites, and one closure check per named
    defect — so it finishes in minutes instead of re-reading the whole package. Number the defects in
    the verdict and answer them one by one, so "closed" is a per-defect claim rather than a mood. Two
    disclosure obligations attach: if the repair had to run outside the mandated engine (a sealed relay
    refused connections, a spawn recipe was never persisted), that substitution is a named deviation in
    the deliverable, not a silent convenience; and a defect the maker caused itself (its own revision
    bump going stale against its own pin) is attributed as such rather than left for the checker to
    label unattributed.

    **Require every verdict to name the revision and digest it read, and treat a head that moves
    afterwards as an unverified delta.** A verdict produced against revision N does NOT cover revision
    N+1. A repair round issued after the independent lanes ran leaves those verdicts one repair behind
    the frozen head, so the artifact finally frozen has been verified by nobody — and an acceptance
    officer's own recomputation does not fill the hole, because that is one role's arithmetic, not an
    independent lane verdict. Close it with a NARROW delta lane: establish the real change set by
    diffing the byte PRE-IMAGE against the current file, classify every changed pointer as an intended
    edit or an unintended one, re-derive the gate, and stop there rather than re-running the whole
    mandate. Make the pre-image the authority for "was this restored to its original value", so the
    answer does not rest on the receipts' own account of what changed. Name the verified revision in
    the freeze receipt too, so "which bytes were verified" is answerable without reading the
    transcript.

24. **A checker's finding is a hypothesis — re-derive it yourself before propagating it, and expect a
    false "the fix was never applied" to come from a DUPLICATED artifact.** The same hook, skill
    reference or script often exists in more than one home, and which copy is live is decided by that
    artifact class's own registration, not by which looks newer — one hook was found executing the
    legacy tree's file while that skill's references load from the packaged home. Resolve the live copy
    from the registration, then diff THAT file against its pre-repair backup: a grep for the old broken
    line proves nothing, because a correct repair frequently keeps the original expression and guards it
    with an extra condition, so the naive search still matches. Publish the correction explicitly and
    keep both facts — the loaded copy's real state AND the divergence that produced the false finding.
    Repairing one copy is itself a hazard: sync the other, or record the divergence as a named open
    defect, since a later session that resolves the other home silently regresses to stale bytes.

25. **Make the mandated route durable on the CARD, not in the pin.** The global delegation pin is
    shared mutable state and binds only at spawn (rule 11); the durable surface is a per-task/per-card
    model+provider override, written when the card is created and carried by every later dispatch of
    that card. Record both the declared override and the model the runtime log shows actually served
    the calls. Note the practical limit found in practice: a board dispatch requires an assignee
    (`dispatch --dry-run` reports `skipped_unassigned` otherwise), so the delegation surface remains
    the lane-dispatch mechanism unless cards are assigned.

26. **Adopting a plan: implement the applied subset under preimage discipline, and record the blocked
    points rather than fabricating a diff for them.** Each blocked point becomes `BLOCKER-<code>` with
    its named mechanism (no trusted resolver/binding accessor exists in the source; the live probe
    returns a not-implemented verdict) instead of a plausible-looking change that would forge authority
    or simply not achieve the goal. Each applied point carries preimage → atomic write → after-hash →
    its own proof command with raw output tail → rollback command, and the orchestrator RE-RUNS every
    proof rather than accepting the writer's receipt (a zero-finding drift check, a byte-equality
    assertion across duplicated copies, a readback of any registered scheduled task). Report the applied
    list and the blocked list separately: a plan adopted only in part, with the residue named, is a
    governed outcome — hiding it is the failure.

27. **Assert mirror equality over the INTENDED paths, and treat a missing intended path as a build
    failure.** A builder can only compare the copies it *made*, so a path expression that is wrong
    (a mistyped segment, an adjacent string literal concatenated into the wrong directory name) writes
    a mirror into the wrong tree while the builder still reports "all copies equal" — the copies agree
    with each other and the intended root holds nothing. Enumerate the mirror roots as literal absolute
    path constants, assert every one EXISTS and hashes equal (fail the build otherwise), and after any
    mirror step re-verify per path by hand. Also assert the builder actually ran: a script without its
    `__main__` guard exits 0 with empty output, and an empty stdout with a success code is a silent
    no-op, not a clean build. Delete any stray tree a wrong path created, and disclose the correction
    (the earlier "all mirrors equal" claim was false at the time it was written) rather than editing
    the record silently.

28. **A pinned digest can be legitimately superseded mid-round by a CONCURRENT governed round — record
    the supersession, never restore.** The repository is shared with other workstreams, so a boundary
    check that finds a frozen artifact's digest changed must attribute it before calling it drift.
    Attribution order: the control-plane store's own event log (a new requirement/workorder id, a moved
    canonical-events counter), sibling run directories with fresh mtimes, and other live sessions in the
    runtime log. When the change is a later round advancing the same single source of truth (a policy
    file, a routing registry), the disposition is **superseded by round N**, and the pin is recorded as a
    *dual pin* — the digest pinned at admission versus the digest observed at freeze — in the freeze
    manifest and the evidence document. Restoring the old bytes is forbidden: it would clobber the later
    round's legitimate work. This is the same "superseded, not reverted" principle that governs a
    superseded wording, and the operational fix is a lock on those single-source files plus a rule that
    each round names which round supersedes its pinned digests, so a boundary check can distinguish
    "superseded by round N" from "unattributed drift".

29. **Measure a lane's slowness before blaming its model.** Per-call latency in a long verify lane
    tracks what the lane *generates* and the tool work it drives, not how much context it re-reads, and
    its single-call maxima sit orders of magnitude above a maker lane's — so a top-down "the verify
    model is slower" conclusion is unsupported until the lane's transcript and the runtime log have been
    parsed. Diagnose with the recipe in `references/verify-lane-performance.md`, then apply the two
    bounding fixes it names (scope discovery to authoritative roots; cap per-command output) on top of
    on top of the dispatch budget in rule 21.

30. **A green suite is not evidence until you have controlled the environment it ran under.** A
    supervising session that exports a variable keeps it for every later command, so a variable set
    for one run (a source-root override, a scratch dir, a config path) silently changes what a later
    "clean" run reads — and a suite that passes only because it was pointed at a different tree looks
    identical to a suite that passes. Before trusting any green, print the variable (`env | grep
    <VAR>`), unset it, and re-run bare: a run that flips to red proves the first green was an
    artifact, and reporting it would have been a false green. Prefer `env -u VAR <cmd>` for one-off
    runs over exporting into a persistent session, and never accept a pass produced under a variable
    you did not set deliberately for that run.

    The same control applies to the TOOL, not only to your shell: a check that spawns child processes
    inherits the environment, so `PYTHONPATH` aimed at the source tree makes an "import fails after
    uninstall" assertion pass or fail purely from the caller's variables. Strip `PYTHONPATH`/
    `PYTHONHOME` inside any tool that spawns a subprocess (`env = {**os.environ}; env.pop("PYTHONPATH",
    None)`) and re-run the check both ways once to prove it is environment-independent. An independent
    checker legitimately scores the unhardened version as a tool-hygiene defect even when the product
    behaviour is correct.

31. **When the declared verify arm has no sanctioned launcher, stand the checker lane up on the
    runtime's own one-shot CLI - never re-point the maker's launcher and call it sanctioned.** A
    governed runtime exposes a non-interactive one-shot that runs tools without an approval prompt:
    `HERMES_HOME=<home> ./venv/Scripts/python.exe -B -m hermes_cli.main -m <checker-model>
    --provider <checker-provider> --reasoning <level> --in <repo> -z "<contract path + write scope>"`,
    with stdout redirected to a log. Three operational facts: the one-shot emits its output only at the
    END, so a byte-empty log mid-run is NOT a stall and the spawned child processes are the liveness
    signal; the separation from the maker is carried by `-m`/`--provider`, which is what makes this a
    real second model axis rather than a second context; and the prompt should name a CONTRACT FILE
    plus the write scope rather than inlining the contract. Smoke-test tool use first (`-z "run: echo
    X; then report its exact stdout"`) before spending a full contract on the run.

    **Flags belong to the SUBCOMMAND, not the root parser.** Budget/quiet/format flags are accepted by
    the CLI's command (`<cli> chat --max-turns N -q ... -Q ...`); invoking the program with the
    subcommand omitted makes the root parser read a flag's VALUE as a command name and exit non-zero
    with `'<value>' is not a `<cli>` command`. The outer process still returns a plausible code, so
    read the INNER log before believing the lane ran at all — a launcher receipt records the launcher,
    not the lane. State what the lane
    does NOT establish: it is a runtime-level lane, so the arm stays UNPROVEN until served-identity
    evidence exists - and a request ledger that carries provider/model rows for OTHER models while
    holding zero rows for the target arm is not evidence for that arm.

    **The checker is a self-report too.** Snapshot the boundary before AND after it runs - the frozen
    declaration/assignment digests, the product digest, HEAD - and re-verify its own disclosures
    instead of accepting them: a checker instructed to delete nothing can still clear the probe
    scratch it created, and that is a deviation to report, not a detail to absorb.

32. **Read the candidate's own suite, and its own evidence records, at the scope they were built for.**
    A candidate that ships a FROZEN copy of a governed input legitimately fails a test comparing it to
    the LIVE input; that is input staleness, and the remedy is never to sync the copy - the tests and
    fixtures are anchored to the values they were built against, so syncing trips the freshness anchor
    and trades one red for another. Run it instead against the canonical root through the test's own
    source-root env hook, report frozen-input red / live-input green as two scoped observations, and
    never call the suite all-green; the full recipe is in `references/route-scheme-enforcement.md`.
    Separately, a maker's own RED/GREEN records can carry a digest from an INTERMEDIATE revision
    because the artifact advanced after capture: re-run the recorded command natively against the
    FINAL artifact yourself, and classify a stale capture as a labeling defect - explicitly not
    fabrication - rather than letting it pass unremarked.

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

34. **Bind the dispatch brief by RULE, not by a frozen SHA, or it becomes a moving target the checker
    rightly flags against you.** A brief naming one commit goes stale the moment any later step in the
    same round rebinds artefacts to a newer candidate, and the checker reports a stale-binding finding
    instead of judging the product. State the rule — every artefact carries `candidate_head == <sha>`
    AND the source-path diff between candidate and evidence commit is empty — and re-point the brief at
    the current head immediately before each dispatch.

    Prefer a candidate/evidence PAIR over a single SHA, and make the rebind deterministic: regenerate
    every artefact while HEAD is the candidate C, commit ONLY the artefact paths as the evidence commit
    E, then assert `git diff <C> <E> -- <source paths>` is empty and `<C>` is an ancestor of `<E>`. The
    empty diff is what proves the artefacts describe that source tree; the ancestor check is what makes
    the pairing meaningful. Never leave artefacts bound to the pre-commit HEAD — that is the stale
    binding this rule exists to prevent, and it is invisible until a checker re-derives it. Record the
    evidence commit alongside the candidate in the deliverable and in the final readback.

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

36. **Preserve the previous round's artifact byte-identical BEFORE editing, and keep the oldest
    baseline a PURE snapshot.** Each round moves the superseded version of any file it edits into an
    `rN_baseline/` sibling (move, never delete) so the delta is provable against a pre-image. The
    original baseline directory must keep containing EXACTLY the original round's file set: when later
    output lands in the artifact tree, relocate the strays into a `*_not_baseline/` sibling instead of
    letting them inflate the baseline — an independent checker verifies baseline membership AND its
    hashes against the earlier freeze, and reads pollution as a defect.

    Related freeze hygiene: **exclude interpreter caches (`__pycache__/`, `*.pyc`) by construction.**
    They regenerate on every suite run, so any artifact set that hashes the tree gets a digest that
    moves each time you exercise the thing you are verifying, and it can never be pinned. If one got
    in, remove it AND disclose the removal in the round record.

37. **Verify the DELIVERED tree, not the maker's opinion of it - a green suite can sit on top of a
    corrupted artefact.** A suite whose tests build the artefact in a temp directory is green about a
    tree it never touches; measured case: `138 tests OK` while the committed `dist/web/` had been
    overwritten with 28-127 byte stubs. Separately check (a) the strict gate pointed at the committed
    artefact, (b) the bytes on disk yourself, and (c) the PRODUCT entry point rather than the module
    the gate imports - a repair that lands only in the new module leaves the legacy caller live and
    "closed" findings open for every user. Suspect any smoke/self-check that runs a writing subcommand
    without an explicit scratch `--out`: that is how the delivered tree got corrupted while the suite
    stayed green. After the checker returns, ASSERT the pairing instead of claiming it
    (`git diff <verified>..HEAD --name-only | grep -v '^<evidence-dir>/' | wc -l` must print 0), and
    for a non-blocking finding choose between a narrow delta re-verification (if you repair) or a
    tracked TT carrying the exact remediation (if you do not) - never edit bytes a checker has already
    read. Recipe and the two measured shapes in `references/delivered-tree-vs-gate-verification.md`.

38. **A maker's SELF-DISCLOSED limitation is not disclosure — convert it into an adjudicated claim,
    and write the DISCRIMINATOR that decides it.** A maker that honestly flags an open item in its
    receipt (a design-interface divergence, an acceptance row that cannot pass as written, a live
    check that failed closed) has done its job, but the item is unverified until the checker rules on
    it. Add each one to the verify contract as its own numbered claim, and instruct the checker in
    writing NOT to accept the maker's framing: read the producer side, the consumer side and the code
    path, then state whether the disclosed resolution is real or papering-over. State the claim as the
    discriminator, not the topic, so the verdict is decidable:
    - *A gate whose own live path fails closed would block every real operation, and that is a
      DIFFERENT defect from a gate that never gates.* Require the checker to read the default timeout
      constant and the default prompt construction, and to separate the default path from a
      deliberately enlarged probe — "the probe timed out" is not evidence about the shipped path.
    - *A consumer that accepts two incompatible producer contracts reads both but writes only one.*
      Ask whether the unemitted contract blocks a designed acceptance row, and require the verdict to
      say which side of the mismatch is the defect.
    These claims are what separate PARTIAL from PASS, and the maker that flagged its own open item
    instead of silently patching it should see the distinction recorded rather than absorbed.

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

41. **Freeze BEFORE you dispatch, and give your own re-measurement a positive control.** Two inverse
    errors, each of which cost a round here.
    *A lane dispatched against a tree a writer is still writing returns time-of-check labels.* An
    independent audit read a config file and reported a constant missing from a script; by adjudication
    time the constant existed and was being sent — the writer had added it mid-audit. The label was true
    as of the read and false as of the freeze, and the tell is that every claim about that file is
    contradicted by the current bytes. Freeze the tree, then dispatch. When a lane's finding is
    contradicted, check whether the file MOVED after its window before recording a lane error: attribute
    a stale read as a stale read, and re-measure each label against the frozen tree rather than adopting
    or discarding the set wholesale.
    *A failed re-measurement does not make the lane wrong — first prove your probe reached the code.* A
    lane reported a blocking defect (an over-long id raising out of the function); my first
    re-measurement did NOT reproduce it, because my fixture failed an intake gate, so every run was
    refused pre-spawn and never reached the faulty path. "Not reproduced" would have closed a real
    blocker. Make the fixture valid, assert a positive control (an ordinary input takes the same path
    and succeeds), and only then report NOT_REPRODUCED.
    Both are one discipline: your instrument's window and its reach are themselves claims, so pin them
    before reading a verdict off them. Corollary for GENERATED evidence documents: fix the generator and
    regenerate — never hand-edit the output — and re-grep the regenerated text for escaping artifacts
    that patching a concatenated string literal can inject.

42. **Your own measurement apparatus is the likeliest source of a misleading artifact — audit what it
    WRITES, not only what it reads.**
    *A before/after integrity guard must CLASSIFY the comparison, not diff it.* Guarding a bounded writer
    by digesting the frozen tree before and after and reporting any difference as `DRIFTED` flags the very
    file the brief MANDATED the writer to create — measured: the guard announced frozen-bytes drift when
    the only difference was an added file that the write set required. Emit MODIFIED / REMOVED / ADDED
    separately, carry an explicit allowed-additions set, and fail only on modified, removed, or
    unbriefed-added paths; then re-judge the SAME stored snapshots with the fixed guard to show it now
    reads clean. A guard that cries wolf is worse than no guard, because the next REAL modification gets
 waved away as the usual false alarm — and every later run's label becomes unreadable.

 *An EMPTY or absent measurement is a harness symptom before it is a finding.* Capture a command's
 output into a shell variable and split on a terminator (`raw=$(curl -s -w '\n__CODE__%{http_code}'
 ...)`, then `${raw##*__CODE__}` for the code and `${raw%$'\n'__CODE__*}` for the body), or write to a
 path a NATIVE tool can actually open (`$LOCALAPPDATA/Temp`, never `$(mktemp)` — an MSYS `/tmp/...`
 handed to the native curl yields NO body at all while the call still reports 200). Measured: a
 zero-byte body was read straight through as a product defect ("returns 200 with an empty body") and
 had to be retracted once the capture was fixed — and the tool-free CONTROL in the same run had looked
 fine only because it used direct variable capture, which made the false reading look like a
 tool-specific bug. So: when a result is damning, re-run the SAME probe against a known-good input
 before recording it, and never let the presence of a plausible contrast convince you. Same class, and
 equally silent: a key-PRESENCE test on provider JSON is wrong when the provider emits the key with a
 null value — `'error' in o` is TRUE for `"error": null`, so test the value (`o.get('error') is not
 None`) or a good response gets mis-read as an error.

 **A harness inherits that hazard: its probes are code, and each bug arrives disguised as a product
 finding.** Three measured shapes from one delta harness, all read as defects until re-derived: (i) an
 EXISTENCE test for a landing zone is wrong when the zone already exists on the host for an unrelated
 reason — test MTIME before/after instead, or a months-old directory reads as fresh creation; (ii) a
 baseline run needs the accepted revision staged under the EXACT module name the tests import
 (`import <module> as E`), or the baseline reports a spurious `FAILED (errors=1)` against a healthy tool;
 (iii) a probe reusing a FIXED destination path is refused by a newly-added replace-guard and reads as a
 broken normalisation — give each destructive probe a unique destination per run. Keep the harness's own
 scratch and every probe inside throwaway trees, and re-assert after each run that the subject is
 untouched (HEAD, porcelain SET, index flags) so a harness that damages what it measures cannot pass
 unnoticed. Fix the harness, then re-run and RESTATE the row — never publish the buggy run's number, and
 keep the buggy revision on disk as the record that it existed.

 **The harness must also be UNABLE to destroy real data, and that is a property you assert, not hope.**
 A probe that hands the real home directory, a drive root, or a live repository to a path that deletes is a
 defect of the INSTRUMENT — and an independent checker is right to refuse to run it and to return FAIL on
 that row, because a guard regression would then delete the very data under protection. Build it so the
 dangerous destinations are exercised only against PURE guard predicates that cannot delete anything, send
 every end-to-end probe to a disposable destination behind an explicit sandbox assertion that ABORTS the
 probe when the target escapes the scratch root, and prove "nothing was deleted" with a recursive manifest
 rather than an exit code. A refused-and-reported probe is a valid result; a probe that could have destroyed
 real data is never a pass of the guard under test. Contract and testing recipe: the
 `destructive-path-guards` skill.

 **Let the DECLARATION decide a hunk's scope, never a keyword match.** Classifying changed hunks by
    searching each one for the repair's vocabulary is a substring heuristic that an unrelated edit can satisfy,
    and a checker is entitled to reject it as an oracle. Map each hunk to the functions/classes it actually
    touches and take the declared in-scope set from the maker's own repair record (falling back to the dispatch
    brief only when the record is silent); report hunks whose touched functions all fall outside that set as
    UNDISCLOSED rather than classifying them by intent. Expect false alarms from an over-narrow declared set —
    re-derive it from the record before reporting anything as undisclosed scope.

    **Function membership is METADATA, not semantic verification — and the fix for that is to widen the
    checker's AUTHORITY, not to re-tune the instrument.** A membership map accepts an unrelated edit made
    inside a whitelisted function or at `<module>` scope, and a checker is right to return FAIL on the row
    for it ("function membership is not semantic scope verification"), because the harness is reporting that
    a hunk is *inside* a declared region, never that its content *is* the declared repair. Do not answer that
    finding by refining the whitelist; classify the finding for what it is — a restriction on what the
    checker was allowed to READ — and lift it: authorise the checker to read the subject source and its
    pre-repair revision **in full**, and make the per-hunk semantic judgement (required by a declared repair /
    harmless by-product / unexplained) its own deliverable, with the unaccounted-line list as the output.
    A checker whose brief limited it to the harness and a file list cannot perform that judgement, will say so
    in `unfinished`, and will keep returning FAIL — so grant the read rather than sending the harness round again.
    Emit, per hunk, the removed and added line TEXT alongside the real-file line ranges so the judgement is
    available without pasting the subject into the harness output. Expect one diff-ALIGNMENT artifact: an
    appended `return` in the repaired revision makes a neighbouring function look inserted, so instruct the
    reader to cross-check the full source — a hunk that only looks inserted because of alignment is
    HARMLESS_BY_PRODUCT, not an edit to another function.

43. **Probe a fail-closed component with a battery, because its handler is the usual escape route.**
    A branch documented "fail-closed, never PASS" fails closed only for the input class its author had in
    mind. Drive it with (a) valid-but-incomplete input (missing fields), (b) unparseable/corrupt input,
    (c) empty input, (d) well-formed but non-object input (scalar or array), and (e) a healthy control that
    must return the ordinary decision. Measured on one handler: the incomplete case produced the documented
    structured pause, corrupt and empty RAISED the parse error, and the non-object case raised
    `AttributeError` — three escapes out of the branch that promised to fail closed — because the handler
    itself re-read and re-parsed the input that had just failed, then called `.get()` on whatever the parse
    returned.
    Grade by CONTRACT, not by likelihood. "The record is written atomically, so it is unlikely" answers a
    different question than "does the documented contract hold"; where the contract is "always a structured
    decision", an escaping exception is a defect at any trigger probability, of the same class as any other
    escaping-exception finding. State where the exception lands — contained where the caller catches it,
    unguarded in another entry point — because the same defect is a crash in one path and a nuisance in
    another, and the maker will report only the benign reading.

44. **An identifier used as a path component wants an ALLOW-LIST plus a length bound, and its OS
    manifestations must be MEASURED rather than asserted.**
    A denylist of forbidden characters admits over-long ids, reserved device names, and trailing dots or
    spaces. Measured: an over-long id escaped a denylist and RAISED out of the writing function with no
    record written at all, while a gate expressed as an allow-list fullmatch with an explicit `{0,100}`
    bound refused the same id up front as a clean fail-closed refusal.
    Then measure the filesystem instead of reasoning about it. Same-day: a reserved device name (`NUL`)
    created NO enumerable entry while `exists()` answered True — writes under it are silently discarded and
    a monitor reads a directory that looks present and is empty; a trailing dot normalized onto the same
    name, so two distinct ids resolved to ONE directory (`resolve()` equality) and could cross-contaminate;
    a trailing SPACE was refused. Report which of these the module's own gate admits.
    Finally, SCOPE the defect before grading it: read the artifact that will actually ship and probe its own
    gate. The same identifier bug is frequently deliverable-only or port-only — an allow-list in the
    deliverable means the blocking defect you just confirmed does not exist in the shipped bytes, which
    reorders the whole repair queue. Report the shared subset (reserved names both accept) as SHARED and
    measured, never deferred as an open question.

45. **A lane can spend its entire budget on commands the harness REFUSES — dispatch the interpreter's
    exact path and forbid the shell's alternatives.** Measured: a fresh-context checker lane completed
    ZERO probes and consumed ~680K tokens because its probing reached for PowerShell; every refused
    command in that log was `pwsh` (all 25 distinct refused shapes, zero non-pwsh, ~1060 refusals in the
    one run) and the lane looped instead of proceeding. The dispatch never named the interpreter, so
    "locate the runtime" was its first act — and it tried that with the refused shell. Put in every
    lane brief: the exact interpreter path, an explicit statement that PowerShell is refused here, and
    the one-line import/suite invocation including the platform's PATH separator (a Windows `PYTHONPATH`
    needs `;`, not `:`, or the import fails and an empty result reads as a product finding). Add a ban on inline
    interpreter one-liners: a `python -c "..."` (or `-Command`) payload with nested quotes is corrupted by
    cmd.exe before the interpreter sees it, and the lane burns its budget on `SyntaxError: unexpected character
    after line continuation` that it misreads as a code fault. Require the lane to WRITE a script file and run
    `python -B <script>`. Keep the
    POSTURE question separate from the tool-choice question: a `read-only` sandbox does NOT itself block
    plain argv (a plain `echo` executes under it, measured), so do not conclude "read-only cannot run
    probes" — but a lane can still be silently unproductive under a posture and exit 0, which is what
    makes an unverified checker dangerous. The combination that ran reliably: full access for the lane,
    with non-modification enforced by BEFORE/AFTER DIGESTS over both the frozen tree and the candidate,
    so the audit property is verified rather than assumed. And gate the dispatch on the ROUTE: probe the
    model endpoint's health first and ABORT on a non-200 rather than starting an audit that cannot reach
    its model.

46. **Prove a suite "regression" against the pristine baseline's FAILING-NAME SET — and check the test
    does not assert on repository STATE.** Two separate errors, both of which cost rounds here.
    *A test that reads version-control state is a cleanliness detector, not a behavioural test.*
    Measured: a candidate carried one "real regression" for several rounds — `git status --porcelain`
    in the repo root, asserting only allow-listed paths changed — and it flipped FAIL to PASS the moment
    the candidate was committed, with no code change in between. Never record such a test as a
    behavioural regression; name it as what it is, and do not let a later commit "fix" it silently.
    *Totals hide whether a failure is new.* Run the identical suite on a PRISTINE worktree at the SAME
    base commit and compare the failing test NAME sets: an identical set is pre-existing (environment or
    baseline) failure, and only a name present in the candidate and absent in pristine is a candidate
    regression. Report the counts, the delta names, and the sample sizes (the two suites legitimately
    differ in test count once the candidate adds tests). A candidate whose failing-name set equals the
    baseline's has ZERO behavioural regression, whatever the raw problem count moved to.

    **A writer's "these failures are pre-existing" is a CLAIM ABOUT THE BASELINE, and it must be re-run on
    the frozen candidate before anything inherits it.** Measured: a lane reported two failures as
    "pre-existing and unrelated (verified against the untouched baseline before my edits — same 2
    failures)" and used that to justify not investigating them; both PASS on the delivered candidate.
    A false known-failing baseline is the most damaging self-report to absorb, because the next round
    budgets around a defect that does not exist and the real question — why did the lane see them? — is
    never asked. Re-run the named tests yourself, publish the raw result, and record it as a CORRECTION
    whose disposition is usually "no product change; the claim was unverifiable" rather than a fix.

47. **Before adopting a test-bearing tree into a repository, probe whether the discovery root actually
    COLLECTS it — placement decides whether the adopted suite contaminates the repo suite or is
    invisible to it.** Measured: repo-root `unittest discover` collected a deliberately-failing probe
    under `tests/` once, and 0 times under `tools/<component>/tests/` (with or without an `__init__.py`
    chain). So a component whose own suite carries host-specific failures (a symlink-privilege error, a
    frozen-input mismatch) can be adopted without dragging them into the repo suite — or can silently
    poison it — depending only on where it lands. Always run the deliberately-failing probe in BOTH
    locations before choosing, and re-run the repo suite before and after the copy to show the adoption
    changed no result; an unchanged before/after with a byte-identical copy is the evidence that the
    placement was inert. Corollary: when a component is "adopted", say whether it is WIRED IN or merely
    co-located — a directory that no production path imports is co-location, and calling it integration
    is the rounding-up this user rejects.

48. **Keep the checker's footprint invisible to the SUBJECT's own guards, or the round fails itself.**
    The artifact under verification usually ships scanners and tests that police its own tree, so anything the
    round writes inside that tree is judged by them. Three measured shapes, one class:
    - a VERDICT/receipt that quoted credential-SHAPED example strings tripped the product's own secret scan
      (`ExportSecretFound`), which then failed two of its tests — a self-inflicted red that reads as a product
      defect. Redact shapes at WRITE time (`<redacted-shape:...>`, or assemble the pattern from fragments at
      runtime) and, for any scanner or test fixture you author, NEVER write the literal shape: a test that
      proves detection must build the dummy as `"sk" + "-" + r"[A-Za-z0-9]{8,}"`, otherwise your own source
      is the hit;
    - a round-owned BRIEF copy whose illustrative example used a forbidden invocation form tripped the
      product's deny-list scan; fix it on the DATA side (reword the example in the in-tree copy, keep the
      original scratch copy) and never weaken the gate's classifier to make your own prose pass;
    - the subject's suite may COPY THE REPO ROOT (`shutil.copytree`, excluding only `.git`/caches), so a single
      extra directory the checker left inside the tree makes that copy recurse and the suite error out. The
      rule is therefore "scratch lives OUTSIDE THE TESTED TREE", not merely outside the artifact set — and
      the dispatch brief must say so explicitly, since a brief that only says "work in the current directory"
      will put scratch inside it.
    **A copy-filter workaround INSIDE the subject MASKS this class instead of fixing it — fix it at the
    mount boundary.** Measured: the checker itself diagnosed the recursion from inside its sandbox and
    wrote a copier with `SKIP={'.<control-plane-dir>'}` plus a comment naming the alias. That repairs the
    checker's OWN copy and does nothing about the subject's own walkers, which read the REAL tree — so the
    competent instinct keeps the product broken while making the checker's view look clean, i.e. the
    workaround hides the very defect it was written around. Put the fix where the boundary is: scratch
    outside the tree, plus a launch-time refusal (non-zero exit, before any work begins) when the resolved
    scratch path falls inside it. A convention the writer must remember is not a guard; a refusal at the
    mount is. Verify the fixed lane is genuinely out-of-tree by running the subject's own health command
    WHILE the lane works — an in-tree scratch makes it fail again immediately.
    Corollary — run the subject's own scanners over the round's own NEW text BEFORE acceptance (a 5-second
    step): a hit then costs a rewording instead of a repair round. Check the whole new surface, not just the
    verdict file: briefs, logs and checkpoint records are all read by the same matchers.
    Scratch also arrives from a DIFFERENT lane's earlier attempt and stays invisible until a re-run contradicts
    it: before re-running an acceptance matrix whose root is the repository, scan the tree for scratch left by
    other attempts (measured: container-created venvs under the round directory carrying Linux `lib64`
    symlinks the host cannot resolve, so the subject's own walk aborted with an unhandled error and the matrix
    reported five FAILs that were scratch-induced, not regressions). Treat a FAIL that appears only after
    another lane has written inside the tree as a scratch hypothesis FIRST, re-run against a clean root, and
    keep the contaminated run on disk as a superseded artefact rather than deleting it.

49. **Stand the checker's workspace up so the SUBJECT CAN RUN — a missing precondition reads as a
    product defect.** A lane verifies by EXECUTING the subject, so the subject's own runtime needs are the
    lane's needs: a tool that reads version-control state needs a real repository in the workspace
    (measured: a tool resolving a HEAD returned nothing outside a repo, its `head_ok` assertion went
    false, and every downstream check read as a failure); a subject that imports a package needs it
    installed; one that reads a config needs the file present. Enumerate what the subject touches at
    STARTUP before dispatching and provide it, then say in the brief that the workspace is already primed,
    so a missing-dependency result is a real finding rather than an unprovisioned sandbox. Corollary to
    rule 45: a lane that cannot run the subject produces findings about the harness while looking like a
    verdict about the product.

    **When the lane's raw LOG cannot be sanitized, keep it OUT of the product tree and bind it by path and
    digest.** A log that quotes a forbidden literal many times fails the subject's own scanner the moment
    it is copied in (measured: 32 occurrences of a sandbox-mode literal). Fold the verdict file in, record
    the log's absolute path, byte count and sha256 in the receipt, and state why it was excluded. This is
    rule 48's instrument: sanitize at write time where you can, exclude-by-digest where you cannot — never
    paste the log in and repair the tree afterwards.

50. **Contract the checker to INVENT cases beyond your claim list, and expect the findings that matter
    to come from three shapes.** Recomputing your claims proves your arithmetic; the defects arrive from
    inputs you did not imagine, so make "design at least three probes outside the package" a deliverable
    in every dispatch, and grade the round on what it found.
    *An injected dependency that is ABSENT must refuse, never default to success.* Measured: a resolver
    whose probe parameter was optional returned SUCCESS carrying `no probe injected`, and its start gate
    reported `started: true` — an unmeasured route presented as available, exactly the false-availability
    claim the round existed to prevent. An unsafe default is graded as a blocker at any likelihood, the
    same as an escaping exception (rule 43).
    *An input that can match more than one target must not be resolved silently.* A bare model name
    matching two entries in a preference pool was answered with the first match and no error, turning an
    ambiguous instruction into a quiet choice; the repair is an exact-identity match first, then an
    explicit ambiguity refusal.
    *A component documenting "always a typed refusal" must be driven with failure from EVERY injected
    seam.* An exception raised by the probe, and one raised by the governance hook itself, escaped as raw
    `AttributeError` / `RuntimeError`, so a caller catching only the documented error type would misread
    an infrastructure failure as a product fault.
    Then prove the repair at the OBSERVABLE, not the return value: assert on the dependency's INVOCATION
    LEDGER — the list of targets it was actually called for — because an empty ledger under a refusal is
    what proves no silent fallback happened, and run the same case WITHOUT the refusing seam as a positive
    control, so a refusal caused by a broken probe cannot read as a governance refusal.

51. **Enumerate the mandate's REQUIRED SOURCE READBACKS in the deliverable, and mark the ones you did
    not perform.** A governed mandate names the sources to read at execution time (a remote branch, the
    baseline commit, an upstream receipt set) and usually states a policy like "fresh readback required
    before writes". A deliverable SILENT about one of them reads as "every source was checked", which is
    the same rounding-up as a false PASS — so emit a per-source table (required read / performed / how
    the bytes arrived / blocker) and carry the un-executed rows into the claim-ceiling table, not only
    into prose.
    A **local copy of the mandate is not the remote original**: a byte-verified attachment of the prompt
    and the audit report satisfies "read the document", never "re-read the remote at execution time".
    Prove which one you hold from the contract's own `locator` values — a locator pointing into a local
    attachment directory means the frozen inputs came from a copy.
    When the checkout has no remote AND the mandate's observed baseline commit is absent from the local
    object store (`git cat-file -t <sha>` answers "could not get object info"), the candidate cannot be
    bound to the externally reviewed subject at all: state it as an EVIDENCE_GAP, because no amount of
    local evidence repairs it and it is precisely what blocks a remote acceptance later.
    Keep two checklist items apart in the reply — "the mandate's findings were addressed" and "the
    mandate's readback was performed" are different claims with different evidence.

52. **A GENERATED evidence master must be swept for internal contradiction before it is published, and
    every captured input it renders must be REGENERATED first.** The document is a builder plus the
    files the builder reads, and each is a place a stale value survives a late change. Three measured
    shapes, all of which a reviewer meets in the first two screens:
    *A claim-ceiling row that was true before a late owner ruling and is contradicted by the body.* The
    ceiling table is read first and the sections last, so when a ruling flips a section, fix the ceiling
    row in the same pass — never leave "maintained FAIL" standing above a section reporting the
    adjudicated PASS, and never leave the section heading describing the pre-ruling state either.
    *A captured tool output that has gone stale relative to the code producing it.* The generator renders
    a saved JSON/text artefact (a metrics table, a check result), so the section displays the PRE-change
    rows and verdicts while the prose describes the new ones. Re-run the tool to refresh the captured
    file, then re-run the generator — fix the INPUT, never the generated output — and confirm the section
    now carries every current row, including the newly added deciding metric.
    *A count restated in prose that the last change moved* (a suite size after the ruling added tests).
    The same derivation discipline as rule 3, applied to the document's own narrative.
    Finish with a grep of the regenerated file for the superseded value and the old wording: the sweep
    costs seconds, and it is the difference between a document a third party trusts and one that refutes
    itself the moment it is checked.

53. **A contract must be satisfiable by the candidate AS IT EXISTS, and a DISAGREED verdict is as likely
    to indict YOUR INSTRUMENT as the product.** Both halves were measured in one round: the verdict came
    back FAIL with two disagreements, and the maker's raw output proved the product correct in both.
    *An UNCOMMITTED candidate cannot be verified by a pristine checkout of the commit beneath it.* The
    clone carries the pre-fix bytes, so a contract property stated as "a pristine clone shows the new
    value" is unsatisfiable by construction — and the bare clone's disagreement is the CONTROL, not a
    finding. State such a property in its achievable form (copy the working-tree subject files INTO the
    pristine clone, run there, and say the bare clone is expected to differ), or commit first and keep the
    literal-clone assertion, which is the stronger claim. Mark the achievable form as the contract author's
    correction so a later reader does not read it as the maker's workaround.
    *Keep from-memory baselines OUT of the contract.* A quoted suite count, failure count or named failure
    cause is a claim the checker will measure and find wrong, and the divergence then reads as a product
    defect. Require the checker to re-derive the control side itself — the parent revision, or a matched
    parent-subject copy — and to report the delta it measured against its own control.
    Then ADJUDICATE each disagreement before repairing anything: ask whether it is with the product or with
    the instrument, and let the checker's own captured raw output decide. Revoke the property in the next
    contract revision, record the superseded wording as the contract author's defect, and carry the
    correction into the deliverable rather than quietly dropping the row. Repair the product only for the
    disagreements its raw output supports. Mechanics, the copy/MAX_PATH hazard and the revision discipline:
    `references/checker-contract-authoring.md`.

54. **A negative-control result is a result only once you prove the MUTATION WAS EXERCISED — an
    unexercised mutation reports the guard as held, and that is a false PASS.** Re-running an acceptance
    case whose subject is a deliberately broken artefact (a mutated module, a removed schema, a truncated
    file) returns the reassuring verdict in three ways that have nothing to do with the guard:
    * *The corruption never reaches the tool.* Measured: a mutated wheel was written under a name pip
      rejects on sight (`ERROR: <name>.whl is not a valid wheel filename`), so the install never ran and
      the case was recorded PASS. Package the mutation under a name the installer ACCEPTS and read the
      install's own tail back before taking any run verdict.
    * *The probe command does not touch the subject.* Measured: a probe drove a `doctor` subcommand that
      only calls a workspace health function, while the code under test (`load_registry()`,
      `load_schema()`) is called by the CLI zero times, so "silently succeeded" described the probe, not
      the product. Grep the SUBJECT for the API under test, drive the MODULE directly, and record "no CLI
      path invokes it" as its own finding (that is a wiring gap, rule 39 — not a pass).
    * *The harness failed, not the subject.* A duplicated or mistyped flag makes argparse exit 2 for
      EVERY case, which reads as universal detection. Assert each captured failure carries the subject's
      own error TEXT and type; a usage error is a harness defect (rule 18).
    Run every case in TWO variants — subject untouched, and subject repaired — because a single variant
    cannot distinguish "the guard held" from "the mutation never landed". Preserve the superseded
    false-pass artefact ON DISK (never delete it) and list it in the verdict's own `retractions`,
    restating the retracted claim in the same reply that carries the contradicting evidence.
    A case the ENVIRONMENT cannot exercise — a symlink-escape case on a host whose account lacks the
    privilege — stays NOT_RUN permanently: name the mechanism, keep it out of the closure count, and
    never present it as fixed. Measured recipe and the two-variant harness:
    `references/delivered-tree-vs-gate-verification.md`.

55. **Bind evidence AT CAPTURE, inside the artefact — a companion receipt describing the same run is scored
    an EVIDENCE_GAP.** Measured: a suite's raw output file carried only the unittest summary, and the
    independent checker refused it ("no command line, no exit code, no subject receipt, skip inventory
    incomplete") although a separate note described the run. Emit the binding INTO the artefact the run writes:
    a header block before the command's own output — exact command line, cwd, `rev-parse HEAD` and
    `HEAD^{tree}`, interpreter version, start/finish UTC stamps — plus an explicit `# exit_code: <n>` line
    appended AFTER the run (a redirect cannot write its own exit code, so append it in the same compound
    command), the suite's own named SKIP lines, and a note naming any non-product tree entries the run itself
    produced (a test that rewrites a tracked evidence file leaves the tree dirty, and unaccounted entries read
    as an unverified subject). Record that artefact's sha256 in the verdict so a later reader can prove which
    bytes were judged, and have the checker re-hash it rather than trusting a quoted digest. Any log a checker
    is asked to trust but which cannot bind itself is an unverified claim.

56. **A subject-binding finding closes on the PRODUCT's own artefacts, never on your round directory — grep
    for the subject identity before claiming closure.** Measured: a round built a complete binding inside its
    evidence directory (return pack, digest definition, artefact hash, four independent passes) and reported
    the binding finding CLOSED; a later self-check grepped the publication-attestation files the repository
    itself ships and found that NONE named any commit of the round's chain — the product's own publication
    artefacts still pointed at superseded commits. The finding was PARTIAL and the claim had to be retracted in
    the same reply that carried the contradicting evidence. So: search every manifest, attestation, receipt and
    provenance file the candidate ships for the subject identity (`grep -rl '<short-sha>'` across the artefact
    and evidence roots), treat a hit naming only the immutable baseline as NOT a binding of the current
    subject, and leave the finding open with an owner and a next action when the product's own artefacts do not
    carry it. A round-local binding answers "can I prove which bytes I verified"; it never answers "does the
    delivered artefact say what it is", and only the second question closes a binding, attestation or
    provenance finding. When you over-claim, downgrade in place and say so explicitly — a self-retraction is
    cheap, a downstream stage inheriting a false CLOSED is not.

57. **Before trusting a repository's own publish/verify helper, check that its DEFAULTS agree — and
    revert any regeneration that does not clear the red check.** Two measured shapes, one discipline:
    never let a tool's convenience default become the claim.
    * `--build` and `--verify` resolved DIFFERENT defaults (build took the current local branch ref, verify
      compared against a commit constant pinned in the source), so the artefact attested one thing while
      verify expected another — and the repository's own test passed only while the branch tip happened to
      equal that constant, and SKIPPED from a clone. Pass the ref AND the commit explicitly on both calls,
      assert the produced payload's attested commit equals the one you passed, and file the default
      divergence as its own tracked defect instead of quietly working around it.
    * A product gate reported paths uncovered by its GENERATED manifest; regenerating that manifest with the
      tool did NOT clear the finding, so the regenerated file was REVERTED, the shipped version left
      byte-identical, and the finding recorded as a tracked item naming its real remediation (the manifest
      and whatever seals it must be extended in ONE publishing action). Committing a regenerated generated
      artefact that leaves the check red is an unexplained canonical-store divergence that also hides the
      fix. State which artefacts you reverted: "the gate is still red and here is the open item" is the
      honest close, never a quiet regeneration.

58. **A checker's `not_verified` list is a CLAIM BOUNDARY, not a defect list — classify every entry, and
    refuse to "close" the ones governance requires to stay open.** Require the field in every dispatch: an
    unstated scope limit is read as "everything else was checked", which is the same rounding-up as a false
    PASS. Then triage each entry by asking which of four things it is:
    *DEFECT* (fix it), *CLAIM BOUNDARY* (closing it would BE the over-claim), *OPTIONAL ENHANCEMENT* (valuable,
    not blocking), *METHODOLOGY NOTE* (how deep the instrument's probe went). Measured on a 9/9 receipt with a
    seven-entry list: none was a defect; two were boundaries the governing acceptance document explicitly
    forbade claiming (deferred execution stages, and host-native / OS-specific behaviour) so closing them
    would have violated the mandate; two were enhancements that each required new credentials and CI surface;
    three were methodology notes.
    An unclassified list reads as a to-do — the user's own question is "is this also something that needs
    closing?" — and answering it by closing a boundary entry converts a truthful scope limit into exactly the
    over-claim the round existed to prevent. Publish the classification, and for each boundary name WHERE in
    the public documents the limit is disclosed (release body, entry-point README, notes), so a reader can see
    it was disclosed rather than discovered. Keep the two directions apart in the reply: "what the verdict
    covers" and "what remains open by design" are different claims.

## Working notes

- Later rounds keep returning FAIL while the findings migrate from substance to metadata: wording,
  labels, counts, citations, scope statements. That is normal — expect several such rounds, keep the
  measurement layer frozen, and let rule 13 shrink them.
- Open SQLite subjects read-only: `file:/abs/path?mode=ro`, adding `&immutable=1` for static copies.
  Never let a re-measurement write to the subject.
- Pass native `C:/...` paths in ENV VARS, not only as arguments: an MSYS-style `VAR=/c/...` reaches a
  native program unnormalized, so a tool that resolves a home or root from it silently uses the wrong
  one — a CLI reporting 'board does not exist' had merely looked in another home. A plain ARGUMENT has
  the same effect, and there it typically CREATES rather than merely misreads: `git clone <url> /c/pub`
  handed a native git the literal `/c/pub` and built a full clone at `C:\c\pub`, complete with a
  tokenised remote URL in its own `.git/config`. Treat a directory under the drive root whose mtime
  moved as this signature, remove the stray tree after checking it for credentials, and pass `C:/...`
  to every native binary — including the `-o`/output path of a native curl, where the same argument
  silently fails to write and reads like a broken fetch. Related: bound
  filesystem walks, because a recursive `find -newermt` over the Hermes install tree or the runtime
  cache times out; scope mtime checks to the paths actually under audit.
- Scope control in a multi-round loop: when the round's own INSTRUMENT (a detector, probe, or test
  harness built to support the deliverable) starts consuming rounds on its own correctness —
  fail-closed semantics, fixture hygiene, docstrings — stop and re-anchor on the deliverable, and say
  plainly in the reply how much of the loop went to the instrument rather than to the question asked.
  Repairing the instrument is legitimate work, but it is not the answer, and a long green instrument
  loop reads as progress while the deliverable stands still.
- Re-derive the numbers from raw bytes on every round; that is what makes the verdict worth having.
- Write probe and receipt output to a NATIVE path, never an MSYS `/tmp/...`: a native interpreter
  handed `open('/tmp/x.json')` resolves a different location, the parse fails, and the harness reports
  "(no json)" — which reads like a broken script rather than a wrong path. Capture a command's JSON
  verdict into the run directory and parse that file, instead of pipe-parsing interleaved stdout and
  stderr. Prefer `search_files` over shelling out to a shell text search from an interpreter
  subprocess, whose PATH is not the shell's.

## Support files

- `references/verify-lane-performance.md` — measuring why a delegated verify lane runs long and
  stalls: the per-lane metrics to compute, the output-vs-input latency correlation, the interruption
  classification that keeps casualties out of lane-quality statistics, the failure modes, and the
  ordered remediation set.

- `references/sqlite-wal-forensics.md` — the WAL checks in order (magic → alignment → checksum
  chain), with the frame arithmetic and what each outcome licenses you to claim.
- `references/git-tree-integrity-signals.md` — what pollutes a `dirty`-count boundary signal besides a
  source change (config `ignoreSubmodules`, index `assume-unchanged` flags, self-managing tools), how to
  restore a repository from a frozen byte-copy and prove the restore by counts and sets, the attribution
  order that excludes your own dispatched writers first, and why a recursive manifest beats a single mtime.
- `references/route-scheme-enforcement.md` — the machinery that makes an ordered per-role model
  scheme (or any mandated route) hold for later dispatches: registry SSOT, generator + drift check,
  the guard's refusal matrix, the conformance test, and how to state adoption status honestly.
- `scripts/freeze-subject-and-guard.py` — one deterministic pass that freezes a subject tree by
  digest, derives the boundary window from a LIVE pid (or an explicit stamp) and prints
  `modified_during_window` per guard path, and reports each pre-image/candidate pair as a numstat
  plus hunk headers so "differs by exactly N edits" is checked rather than asserted. Use it instead
  of hand-writing the freeze receipt: the hand-typed epoch literal is how a whole guard table ends
  up inverted.
- `scripts/run-gate-matrix.py` — runs a pre-dispatch lane gate's case matrix (SoD, admit, unevidenced
  admission, provider mismatch/omission, stale source pin, forced epoch) against the CURRENT registry
  and prints observed vs intended exit codes with a mismatch count, so the gate claim is measured
  rather than copied from the writer's table. Compare the verdict's named error codes, not just exit
  codes: argparse also exits 2 on a mistyped flag, which is indistinguishable from a designed refusal.
- `references/mandate-completion-audit.md` — the recipe for "is the mandate complete / can a third party
  accept this now": taking the mandate's own enumeration as the denominator, the closed disposition
  vocabulary that must not be summed into a pass count, reading the mandate's termination clause before
  writing a verdict, the seconds-long remote-acceptance blocker checks (`git remote -v`,
  `git cat-file -t <baseline-sha>`, the artifact's own publication gate), and the honest local-vs-remote
  split. Load it whenever you are asked whether a governed round is finished or acceptable.
- `references/checker-contract-authoring.md` — how to write a verification contract that yields a
  DECIDABLE verdict: the uncommitted-candidate / overlay form, the control-probe rules that keep a
  disagreement from being read as a product defect, why the suite is graded in a clean copy and what to
  exclude from that copy (Windows MAX_PATH), and the contract-revision discipline. Load it before authoring
  or revising any independent-checker contract.
