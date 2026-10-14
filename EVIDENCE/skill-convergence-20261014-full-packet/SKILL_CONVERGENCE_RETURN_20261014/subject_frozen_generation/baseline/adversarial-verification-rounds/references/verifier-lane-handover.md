# Briefing and handing over to an independent verifier lane

The rounds method fails more often at the handover than at the checking. These are the rules that keep a
verifier's verdict usable, in the order they apply.

## 1. Give the lane a write path that is inside the write-set allowlist

State the verifier's output directory as a **round-relative path inside the allowlisted prefix**, and say
explicitly which prefixes are forbidden. A brief that names a repository-root `verify/` while the round's
allowlist covers only `<round-dir>/**` produces evidence that cannot be committed - and committing it would
itself be an allowlist violation by the maker. The verifier will follow a relative path literally, so the
defect lands on the maker, not on the verifier. Name the exclusion in the brief instead of trusting the lane
to infer it.

## 2. Commit your own artifacts BEFORE you launch the verifier

Commit the brief, the launcher, the lane log, and any notes you wrote, then confirm the worktree is clean.
A dirty delivery fails the clean-handover subclaim even when the committed snapshot is clean - and the
finding is **unanswerable**: untracked-file authorship is not recoverable from `git status --porcelain`, so
the verifier can only report the deviation and decline to attribute it. Hand over a clean tree or accept an
unclosable finding.

Remembering to do this is **not** sufficient, because the lane log you are about to write lands in the
subject tree *after* the cleanliness check - so the handover goes dirty again by construction and the next
verifier reports the same finding. Mechanise it with a launcher that does all four of: (a) stage and commit the
round's harness artifacts, then require `git status --porcelain` to be empty and REFUSE to launch otherwise,
so a dirty tree fails closed instead of being noticed later; (b) write the lane log OUTSIDE the subject tree
and copy it in only after the run; (c) commit the lane's output postflight; (d) take the subject path from an
environment override so the refusal path can be exercised against an external clone without ever dirtying the
real delivery. A launcher counts as fixed only when a later round ATTACKS its refusal path - dirty an external
clone, expect a non-zero exit and no model launch - otherwise you have fixed the instance, not the cause.

**Do not touch the subject while a verifier is running**, not even to clean it. Staging, committing or
deleting mid-run moves HEAD while the verifier is resolving and re-checking identity, which is a worse defect
than the dirt it removes. Leave the dirt, let the verdict say what it saw, and fix the harness for the next
round.

The same rule covers RENAMING or MOVING a round path mid-run. The verifier inventories the tree as it goes, so
a path it already resolved and later cannot find is reported as moved or missing - a finding about the maker's
handling, not about the deliverable, and one that costs a round to explain. If you notice a misplaced path in
your own evidence while a lane is running, write it down and fix it after the verdict.

## 3. Force the copy OUTSIDE the subject tree

Say in the brief: clone with `git clone --no-hardlinks . <temp>/candidate`, then
`git checkout --detach <resolved-subject>`, and run every test in that snapshot. Never run the suite against
the delivery worktree, and never place a copy inside the subject - a nested copy changes the tree under test
and turns unrelated tests red for reasons that have nothing to do with the deliverable.

## 4. Make the lane resolve identity itself

Require the verifier to resolve HEAD, tree, and the remote tip on its own, and to state the commands it used.
Never hand it a digest to trust, and never let it reuse a hash from your document - a copied hash checks your
wording, not the artifact.

## 5. Reading back a file you wrote is part of the handover

After writing an evidence or brief file with a long argument, read it back and confirm the content is whole
(no truncation, no unexpected marker text inside it). Large arguments can be silently shortened on the way to
the filesystem; a half-written brief or evidence file is indistinguishable from a deliberate one to the next
reader. Write long files as several short appends and check the byte count, rather than one oversized write.

## 6. Relocating evidence: move it, never rewrite it

When a checker's output landed in a forbidden prefix, move the directory and **prove** nothing changed: hash
every file before and after and compare the sorted multiset (file count must match too). Leave the verdict's
bytes untouched - including its stale absolute path strings - and add a separate location note that explains
the move, why it was necessary, and that the paths inside the verdict are now one component stale. Editing a
checker's verdict to fix its paths destroys the artifact you are citing.

## 7. Keep the acceptance lane and the root-cause lane apart

The lane that decides *whether to accept* must not be the lane that investigates *why something failed*.
Run them as separate sessions with separate outputs, or the acceptance verdict gets contaminated by whatever
the investigation concluded. And the lane under investigation never studies its own failure: a maker
analysing its own defect is not an independent root cause.

## 8. Do not attribute a lane failure to "the model" from a self-reported field

When a lane fails, the brief for any root-cause study must separate three different failures with three
different remedies: the lane exited non-zero, the requested model was unavailable, and the transport was
broken. A probe log's self-reported model identity is worth what you can corroborate, and nothing more - a
process asked for one model family that announces a different one, plus a transport error line (a websocket
upgrade status, a fallback endpoint), tells you the routing is not what you asked for. That is a configuration
defect class, and it is a finding in its own right. Never let a convenient label ("it aborts", "it is flaky")
stand in for the causal statement.

## 9. Falsifying a closure claim

For a claim that a previously-found gap is closed, demand the smallest reproducing command and a path-set
proof: list every commit after the verified subject with its complete changed-path set, and treat a single
path outside the allowlisted prefix as falsifying the claim outright. Also require an ancestry check that the
verified subject is still an ancestor of the new tip - a rewritten branch invalidates the earlier verdict.

## 10. Write-set guards: allowlist, plus an explicit deny, plus refuse-to-guess

A guard that only blacklists frozen paths lets novel paths through. Express the guard as
`ALLOWED='^(...)$'` matched positively, an explicit `DENIED='^(...)'` for frozen prefixes, and an ancestry
check; fail the job when either test fails. Resolve the comparison base or **refuse**: on an empty or
unresolvable base, exit non-zero with a `BASE_UNRESOLVED` message rather than defaulting to `HEAD~1`, which
silently compares the wrong range and reports clean. Note in the verdict that "read-only" describes the
absence of remote mutation, not a literally read-only runner checkout.

**When the subject is not a git repo, prove the write scope by TIME instead.** A path-set proof needs history;
without it, enumerate every file whose modification time falls inside the lane's dispatch window and report
the ones outside the lane's declared write scope. Compare timestamps in the interpreter (`st_mtime`), not with
`stat`/`date`, and disclose the window's bounds and that mtime is advisory. Two traps: a lane's isolated home
is materialised inside the round tree and writes thousands of files there, so filter the scan by the declared
allowlist rather than assuming a short list; and a stray edit by an unrelated process on the same host lands
in the same window - say "outside the declared scope" and attribute it as unattributed rather than to the lane.
Distinguish an in-scope-but-unexpected write (own-scope `__pycache__` from running the suite) from an
out-of-scope one, and report the count of each.

## 11. The orchestrator applies the verdict, it does not form it

Acceptance is a verdict artifact, not a conversation. Give the lane a closed vocabulary
(`ACCEPT` / `ACCEPT_WITH_CONDITIONS` / `REJECT`), require it to enumerate conditions when conditional, and
require it to state what acceptance does **not** license. The orchestrator's job is to apply that verdict
verbatim and to repeat its ceiling - never to substitute its own judgement for a refused or missing one.
Missing evidence is `NOT_EXECUTED`, which is a result, not a gap to be filled by inference.

**A tracker that shows everything closed after a FAIL verdict is a trap.** When leftover board or task
cards are closed for book-keeping rather than because their work was done, annotate BEFORE closing and
put the words that prevent misreading into the closure text a reader actually sees (the summary field),
naming the follow-on artifacts and -- where an independent check of that subject returned FAIL --
naming that verdict. A bare status change erases the difference between satisfied and superseded. Close
parents before children, or unlink the dependency and say which you did, and record the before/after
board state in the round evidence.

## 12. Report coverage as discovered vs run, never as one "skipped" number

A test-runner summary line conflates things that must not be conflated in a verdict, so copy neither its
number nor its phrasing. `skipped=N` can be several individually skipped cases PLUS a module-level
`setUpModule` skip that hides every case in that module without any of them ever starting; the honest
denominator is the count the loader DISCOVERS. Report discovered, run, successes, individual skips, and
unexercised-by-module as separate figures, and name the unexercised ones as gates that were not exercised -
never as "the suite passed". A green exit alongside module skips is not coverage, and a total carried forward
from an earlier round without recounting is how a wrong number survives several rounds. When a skip is caused
by the interpreter lacking a package, re-run those cases under an interpreter that has it and label the extra
run supplementary, not as a second full run.

**Regenerate every count in the brief from the artefacts at dispatch time.** A brief written before the last
fixture repair states yesterday's numbers, and the verifier - which reads the delivered result files - is right
to report the disagreement as a finding. Either inject the counts from the result files when the brief is
built, or say in the brief that its numbers are unverified claims and that the raw result files govern. Do not
leave a stale figure in a document the verifier is told to trust.

## 13. State the lane's WRITE MECHANISM in the brief, and have it verify its own output

A brief that specifies what to produce but not how to write it can consume a lane's whole budget and end with
zero artifacts. On Windows, a lane that assembles a patch and pipes it through PowerShell into the CLI's patch
entry point fails with a UTF-8 argument error - the shell-to-native-executable handoff mangles the string.
Require the lane to write with the interpreter instead: a small script under its permitted output directory,
opening each artifact with an explicit `encoding="utf-8"`, one write per artifact. Then require it to read each
artifact back, print its byte size and hash, and treat a missing or short file as a failed write rather than a
completed step. A lane's exit code is not evidence that its deliverables exist.

## 14. Pre-create the lane's verdict artifact, and fail closed if the lane never takes it over

A verdict written only at the END of a turn is a terminal artifact: a lane that runs its context to the
model's ceiling, or dies at startup, leaves NOTHING - which is indistinguishable from "no check ran", while
the zero exit code still reads as success. Pre-create the artifact as a SKELETON before the lane starts, with
every item `INCONCLUSIVE` and an explicit "not taken over" flag, and make the harness's post-condition fail
closed (`ERR_<...>_NO_VERDICT`, non-zero exit) while that flag is unset:

1. the brief's FIRST required action is to load that file, set the takeover flag, and save it back BEFORE any
   analysis, then update the same file in place after each item it resolves;
2. after the lane exits, the harness re-reads the file and fails the lane unless the flag is set - an
   untouched skeleton is not a verdict;
3. the receipt records the flag, so a reader can tell a real verdict from a skeleton without opening it.

**Give the literal command, not the instruction to do it.** A brief that merely ASKS for the takeover as the
first action still fails when the lane has real investigation ahead of it: the lane reads the instruction,
plans, begins work, and the turn ends with the skeleton untouched. Put a copy-pasteable block in the brief
that loads the file, sets the takeover flag, fills every item `INCONCLUSIVE`, and saves - and say "run this
now, as your first action". Measured on one control with the same model: instruction-only ended its turn six
minutes later with the skeleton intact and every measurement it had made lost; the literal command had the
file taken over within ~75 seconds. A lane can also burn its whole turn budget building an elaborate harness
and never reach the write - so state in the brief that the artifact is written FIRST and rewritten after EACH
item, and that a turn ending early must leave a complete, honest artifact behind.

**Poll the takeover flag yourself a minute or two after dispatch.** It is the cheapest compliance check there
is, and it distinguishes "the brief's first action was skipped" from "the lane is working" long before the
run ends. A flag still unset after the first minutes means the artifact is on track to be refused, not that
the lane is slow.

**A retry needs a DIFFERENT brief and its own log path.** This failure class is "the lane spent its budget
before landing the artifact", so re-running the same brief reproduces it. On the retry: name the voided
attempt's failure in the brief's opening section, supply the literal takeover command, tell the lane to REUSE
the harness it already wrote (`<workdir>/<harness-dir>/**` is its own prior work, not the writer's) rather
than rebuild it, and never reuse the failed attempt's log path - the earlier raw output is the only evidence
that the first form failed.

Why this beats "just ask the lane for a verdict file": a lane that exhausts its context then leaves a complete
and honest `INCONCLUSIVE` set instead of vanishing, and an item nobody could resolve is recorded as unresolved
rather than absent. Measured: lanes sitting at 99.6 %, 100.7 % and 104.4 % of the declared ceiling still left a
taken-over verdict, where the same conditions previously produced no artifact at all, and the lane that crossed
the ceiling left four explicit `INCONCLUSIVE` items rather than a false green. `INCONCLUSIVE` with a stated
reason is a first-class outcome - never let a lane leave an item silently unmentioned, and never let the harness
read an untouched skeleton, an empty run, or a zero exit code as a pass.

Corollary for the gate around it: the lane does not self-report its budget. The harness measures it from the
provider ledger, and a threshold read off a wall-clock window is batch-scoped once lanes run concurrently -
see provider-routing-triage, `references/relay-ledger-and-lane-health.md`, and label such a claim accordingly.

## 15. Never rewrite a launcher that running lanes are executing, and pass every lane path absolute

bash reads a script incrementally as it executes it, so editing the launcher (or a generator it sources)
while lanes are mid-flight can make a live lane run a hybrid of two versions. Serialise it: dispatch the
harness-repair lane only after the last lane using that script has exited, and say in the report that the
repair was deliberately deferred for this reason.

Give every lane option as an ABSOLUTE path. A launcher that normalises some options but not others (a brief
and a schedule resolved, an isolated home or work directory passed through raw) fails instantly and confusingly
when it hands a relative path to a native executable, which resolves it against its own cwd - the lane dies in
under a second with no model call, and the receipt looks like a model or budget problem. Check each new option
against the launcher's own normalisation before dispatch, and keep per-lane option values distinct so a sibling
lane cannot inherit one.

## 16. Look for an EXISTING packaged lane before you hand-roll a brief or a wrapper

These stacks keep packaged lanes for the recurring independent roles - external challenge reviewer, acceptance
officer, security reviewer. Each ships a skill, a plugin manifest, a checksum file and a self-test, and each
carries its own workflow, its own output contract and its own verdict vocabulary. Search for one before you
write a brief or a dispatch wrapper:

1. **Search** the workspace for the role name (a `Fabric/`-style directory is the usual home) and read the
   package's own README for the supported install locations.
2. **Verify** it: check every entry in its checksum file and run the packaged self-test. Do not install a
   package whose integrity you have not confirmed.
3. **Install where its README says**, user-scoped for a Codex-style local skill (`~/.agents/skills/<name>/`).
   Prefer the user-scoped location over a repo-scoped one when the repository is the subject of the review -
   installing into the subject tree dirties the very delivery the review is about.
4. **Invoke it by its own selector** (``Use <skill-name>.`` as the lane's opening instruction) and let it own
   the procedure: its report template, its required headings, its verdict vocabulary, and its bundled
   validator, which you should require the lane to run on its own bundle and quote raw.
5. **Keep your launcher, if you have one, as the governed dispatch shell only** - out-of-tree logs, per-launch
   receipts, refusal paths, declared failover - and hand the round's bindings to the packaged lane in the
   brief. The role definition is not yours to restate.

Hand-rolling the role duplicates a lane that already exists, produces an artefact no earlier round can be
compared against, and spends the scarce checker budget on a second copy of the same work. If you have already
built a bespoke brief or wrapper for a role, treat that as the finding: find the packaged lane and re-dispatch
through it rather than defending the duplicate.

## 17. Hand the checker your OWN observations as leads, labelled as leads

A checker told only "verify the deliverable" re-derives the obvious and may miss what you already
suspect. Put your own observations in the brief as a numbered lead list, with the contract stated:
these are LEADS, NOT FINDINGS -- re-derive each one and either confirm or REFUTE it, and a refutation
is as valuable as a confirmation. Require a per-lead disposition in the verdict (confirmed / refuted /
could-not-check with the reason).

A hand-built lead list turns "attack it" into a bounded attack, and it is also the honest move: it puts
your suspicions on the record where a checker can falsify them instead of letting them stay private.
**Include leads that point at your own artifacts** and say in the output contract that `found_defects[]`
may name the orchestrator. The highest-value return of a lead list is a lead that comes back confirmed
against the orchestrator -- an over-claimed property in its own ledger, a sandbox described more
strongly than its header, a status asserted without a digest.

Give each lead something refutable: file paths, byte sizes, hash prefixes, the exact call that
reproduced it, and the timestamps that bound it. A lead carrying a size delta and a named assertion can
be falsified; a lead phrased as a suspicion can only be argued.

## 18. Record the model axis, and never let a same-model verdict supersede a different-model one

Independence has several axes: a different process, a fresh context, read-only discipline, and a
different MODEL. The model axis governs correlated blind spots -- a checker on the writer's own
provider and model shares its framing, while a different model attacks from outside it. Measured: a
round whose checker ran on a different provider's model found five HIGH-severity defects in work that
same-model rounds had already passed, and falsified a writer's claim that no test had been edited.

1. When a mandate or quota forces the checker onto the writer's model, record
   `sod_axis_model: NOT_SATISFIED` in the round ledger AND in the checker's own output, and name the
   axes that still isolate it (process, fresh context, read-only discipline).
2. Require the verdict to state that it does NOT supersede an earlier different-model verdict on the
   same subject. Keep both on record; a newer, weaker verdict must not overwrite a stronger one.
3. Keep the different-model route working and re-runnable, and record its probe evidence (the exact
   command, exit code, and window sampling before/after) so the next round can rebind without
   rediscovering it.
4. Do not oversell the axis either: call it necessary-but-not-sufficient and say that the remaining
   isolation is procedural.

## 19. Ship the verifier's INPUTS, not just your conclusions

A verdict of `INCONCLUSIVE` or `PARTIAL` is usually a defect in the **packet**, not in the subject: the
findings name inputs the checker needed and did not have, and every one of them is measurable. A checker
that has to ask for them costs a whole round, so freeze these WITH the deliverable:

1. the **source expectation values themselves** (the plan's/config's own pre- and post-digests), not only
your receipt's restatement of them - a receipt quoting its own numbers is a maker claim and the checker is
right to say the comparison to the raw source is missing;
2. a **three-column comparison per item**: receipt value, source value, current on-disk value, so the
comparison is recomputable rather than asserted;
3. the **undo artifact**: hash every backup and show it equals the source preimage, give the literal restore
command, cite the end-to-end rollback proof from a fixture run of the SAME code path, and state plainly that
no rollback was run against the live target after the apply - undoing a governed step as a test is itself a
subject mutation;
4. an **ordering witness** for anything claimed to have happened before the check (see 20);
5. a **side-effect inventory** carrying an explicit "these are the ONLY subject changes" statement, plus
digests for the binding files you did NOT touch;
6. an **artifact-to-gate map**: per artifact, what it closes, or which withheld item it is evidence for, with
prior-round artifacts marked carry-forward and superseded freezes marked superseded.

**Before you apply a candidate to a subject file at all, measure whether that path is listed in a frozen
subject manifest.** Editing a bound file breaks a digest the round is usually not authorised to re-seal, so
withhold that edit, name the gate that withholds it, and apply only the unbound ones. Do the measurement
from the manifest's own content rather than from memory, and expect the frozen subject manifest to exclude
the prose files you are about to touch - that exclusion is precisely what makes the edit lawful.

## 20. Pre-register the oracle, and state its ceiling

Register the expectations as a timestamped artifact BEFORE dispatch, written by the orchestrator rather
than by the checker. Each expectation must state what it PREDICTS and what would REFUTE it, and the
expected-verdict band must include `FAIL` whenever a FAIL condition has been written at all - an
oracle that omits the verdict it fears reads as decorative. Two observations worth carrying into the
artifact: a file mtime is an **ordering witness**, not a tamper-evident commitment, so say that; and do not
build a hash-chain or commitment mechanism to close a single round - that is a new machine and is
over-engineering unless the owner asks for one. When a freeze manifest lists an EARLIER round's verdict as
carry-forward evidence, say so in the same breath as the exclusion clause and name which (later) artifact is
the one excluded by construction; otherwise the checker reads your artifact list as contradicting your own
exclusion and reports it.

## 21. Adjudicate by paper when the lane has no tools

A tool-less checker cannot recompute a hash, so part of its `INCONCLUSIVE` may be structural rather than
fixable. Convert it with a SECOND pass over the SAME lane instead of building a harness: hand it its own
previous findings verbatim plus your errata, and require one closed decision per finding - `RESOLVED` /
`PARTIAL` / `NOT_RESOLVED` / `OUT_OF_REACH_FOR_THIS_LANE` (naming the capability it lacks) - with the
explicit instruction to distinguish "cannot be recomputed in this lane" from "still missing from the
packet", and not to upgrade anything because a second pass was requested. The result is per-finding
dispositions plus the short list of gaps that genuinely need a different capability, at the cost of one
lane run. Then close what the packet can close, and hand the structural gaps over with their gate rather
than inventing a mechanism to satisfy them.

## 22. Match the probe to the edit kind: insertion vs substitution

A line probe asserting the old anchor is ABSENT is valid only for a SUBSTITUTION. An insertion edit whose
`after` text CONTAINS its `before` text necessarily leaves the anchor present, so the same probe reports a
contradiction against a perfectly good apply. Detect the semantics from the data (`before in after`), state
the expected anchor-occurrence count for that semantics (0 or 1), and treat the source postimage DIGEST as
the authoritative check, with the anchor count as supporting evidence only. Say the semantics in the probe
output - a reader who sees "old text still present" beside "replacement succeeded" without the word
`INSERTION` will file it as a defect, and a checker did.

