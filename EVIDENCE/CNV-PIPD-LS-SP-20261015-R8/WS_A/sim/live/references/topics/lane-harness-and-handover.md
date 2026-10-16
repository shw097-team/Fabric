===== SKCV-TOPIC-BATCH BEGIN theme=lane-harness-and-handover =====
topic: lane-harness-and-handover
note: complete verbatim bytes of absorbed files; envelope only, no byte edits; byte offset = offset of the absorbed file's first byte within this topic file
segment_count: 3

===== SKCV-TOPIC-SEGMENT 1 BEGIN path=references/verifier-lane-handover.md offset=457 bytes=26549 sha256=aebb35ea0ef523de9d64940081706fc62bd36fb4712abe51ef8baa19e3dd939b =====
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

===== SKCV-TOPIC-SEGMENT 1 END =====
===== SKCV-TOPIC-SEGMENT 2 BEGIN path=references/checker-binding-and-false-defect-signals.md offset=27240 bytes=5403 sha256=31ae9774cd4e245c47aa051adfae17ac3e14f68b5ba49b1e867c5cb8225053c4 =====
# Binding the checker, and the two ways its signal lies

Two failure families on the checker side of a round: the checker is not actually independent, or its
findings are not actually true. Both are cheap to prevent and expensive to discover late.

## 1. Bind the checker to a different model ONLY by stripping the default route's environment

A sealed CLI lane usually defaults to an internal relay. To put the checker on another provider over
native OAuth:

- Strip the relay environment around the invocation (`env -u OPENAI_BASE_URL -u OPENAI_API_KEY ...`).
  With the relay base URL present, a `<vendor>/<model>` request is routed to the default provider and
  answers HTTP 400 — the lane never reaches the OAuth backend, and you will misread that as "the
  provider is unsupported".
- Point the CLI's home directory at the one holding that provider's auth, and pin model AND reasoning
  effort on the command line. Pinning the model alone can silently come back with a different effort.
- Take the binding from the run's OWN stdout header (`model:`, `provider:`, `sandbox:`, effort). A
  registry or config declaration is a claim; the run's header is evidence.
- Ignore a declared route status in either direction. A registry can carry `UNPROVEN` or a stale
  failure string from a sibling model while your route works, and vice versa. Probe, then believe.

### Guard the interactive-login fallback before probing

Read the auth file's `last_refresh` first. A stale access token refreshes silently, but a revoked
refresh token falls back to an INTERACTIVE login — which opens a browser window on the user's desktop.
So probe with stdin from a file (never a tty), a hard timeout, and a visible-window sample taken
immediately before and after. Record both samples; "0 new windows" is only meaningful as a comparison.

### If the mandate forces the checker onto the maker's model

Record the axis as NOT_SATISFIED in the verdict, state that isolation now rests on process
separation + fresh context + read-only discipline alone, and state explicitly that this verdict does
NOT supersede an earlier different-model verdict on the same subject. A same-model round may still be
worth running — it just cannot carry the independence claim.

Why the axis is worth insisting on: in one measured pair, a different-model checker falsified five
HIGH-severity defects in a deliverable the same-model round had accepted, including a false statement
in a writer's self-report and an over-claim in the orchestrator's own ledger. The axis is necessary
but not sufficient — process and context separation are the rest of it.

## 2. False RED: your hand-built input is not the producer's shape

When you test a classifier, checker or guard by calling it directly, you must use the shape its REAL
producer emits. A hand-built dict that is missing a key the code now requires can produce a whole
category of bogus failures.

Measured case: probing a credential-helper classifier with `{"origin": ...}` entries returned
"unclassifiable" for the real, installed program, which looked like an over-blocking defect. The code
expected a `scope` key (as the real config reader emits); with the real shape every realistic input
passed. The "defect" was entirely constructed by the probe.

Rules:

- Before reporting a defect, get one REAL sample: call the production entry point (the gate/CLI the
  pipeline actually uses) and read what it passes, or read the producer function. Compare shapes.
- Exercise the production entry point end to end as the no-over-block control. If the production gate
  still says continue, an alarm raised from a hand-built input is probably yours.
- Retract a false alarm explicitly and say it was your probe. An unretracted false defect is worse than
  a missed one: it sends the next round chasing a non-existent bug.

## 3. Never let an in-place edit destroy its own verifiability

A rule for whoever writes the deliverable, enforced from the verifier side:

- Every in-place edit of a pre-existing file must leave a timestamped preimage copy, and the lane
  report must quote that path and its digest. Without it, "revertible" is unprovable, and a bad edit
  is unrecoverable in practice.
- An untracked file has NO git-verifiable preimage. A git index blob is a usable preimage only if the
  file was staged before the edit; say which of the two you relied on.
- Put the preimage requirement in the lane brief, not in the post-mortem. A round whose headline change
  has no preimage tends to be the round that also has a defect in that same change.

## 4. Mirrored evidence documents are immutable — corrections go in a NEW file

When an evidence artifact is mirrored byte-identically into several review roots, editing the
original silently diverges the copies while every hash in the transcript still looks correct. Write
superseding information into a NEW addendum file that quotes the sentence it supersedes, and re-mirror.

Related, same reasoning: do not mutate a shared version-control index while another session may be
writing the same repository. Establish that no foreign writer is active (recent mtimes under other
work areas, other running workers) before any staging decision, and treat "an unnamed actor already
staged files" as a reason to record state rather than to stage more.
===== SKCV-TOPIC-SEGMENT 2 END =====
===== SKCV-TOPIC-SEGMENT 3 BEGIN path=references/lane-harness-and-admission-gate.md offset=32869 bytes=22476 sha256=61bdb0cd1763f7494bef8337c42a2d1e53c3550ab18102b7ee4f219eaf52c140 =====
# Governing a worker-lane harness that must fail closed

This is the harness side of a verification round: the launcher that starts worker/verifier lanes, the
admission gate in front of it, and the checklist of ways a gate pretends to protect you. Every rule below
came from a real counterexample an independent officer produced against a harness that claimed to be
fail-closed.

## Handover rules

- **Never hand a verifier a tree your own harness just wrote into.** Write lane logs, manifests and
  receipts OUTSIDE the subject worktree and copy them in at postflight. A launcher that writes its
  manifest inside the tree after its clean preflight has dirtied its own handover, and the officer will
  return NOT_CLOSED - correctly.
- **Commit harness artifacts, then refuse to launch if the tree is still dirty.** The refusal is the point;
  do not make it a warning.
- **Create officer output directories round-relative.** `mkdir -p "$WT/$OUTSUB"` silently makes a directory
  at the repository root, outside the write-set allowlist, and defeats the round-relative fallback.
- **Give each officer a unique write set** (its own round subdirectory) and tell it that everything else -
  candidate copies, stubs, clones, fixtures - lives outside the tree in a system temp dir.
- **Make receipts per launch** (a token per invocation), not a wildcard: an older run's receipt must not be
  able to satisfy the current check.

## Fail-closed rules, each from a demonstrated counterexample

- **Propagate the child's exit status.** A concluding `echo` is not error propagation; a wrapper that ends
  with `echo DONE` exits 0 over a failed child.
- **Treat a FAILED cleanliness query as dirty.** A `git status` that errors has empty output, so
  `| wc -l` reads as 0 paths and the wrapper prints `PREFLIGHT_CLEAN`. Check the command's own status.
- **Never commit an index you did not scope.** `git add -A -- <round>` then `git commit` also commits
  anything already staged outside the round. Refuse if any staged path is outside your write set.
- **Validate every configurable count.** `GATE_QUALIFY_RUNS=0` runs no qualification and prints
  `QUALIFICATION_PASSED ... consecutive_runs=0`. A zero-iteration loop that reports success is a fail-open.
- **Qualify through the same configuration you will launch with.** A gate that validated the catalog route
  and launched writers through the default route validated one lane and started another.
- **Validate log/manifest destination against the subject tree.** A `TMPDIR` that resolves inside the
  worktree defeats the whole out-of-tree discipline.
- **Check every copy.** A failed copy of a log or a receipt must be fatal, not a printed note.

## Evidence rules for the gate's own judgement

- **One passing run is a sample, not a property.** When the fault is intermittent, require k consecutive
  passes and report counts ("3 of 6"), never a reliability percentage from a small sample.
- **A gate that fails closed on its own misconfiguration manufactures authoritative refusals.** A refusal
  must name the exact configuration it refused, model and effort included. If the operator cannot
  reproduce the refusal by hand, it is a harness bug until proven otherwise - and a gate that refuses a
  healthy lane is worse than no gate, because it looks like evidence.
- **A stub binary proves control flow and nothing about the model.** Wherever a stub replaces the real
  worker, say so in the report; the officer's ceiling statement must carry it.
- **Re-run a dead counterexample against the current script before claiming it closed.** "Fixed" without a
  fresh reproduction is a claim, not a result.
- **A green suite is evidence about the checks you exercised, not about the harness being correct.** Report
  it with that ceiling instead of as acceptance, and say so when a round of repairs activates a check that
  had never run - the suite can turn red for that design reason alone.

## Traps that survive a first fix

These all passed a review of the *fixed* script. Each one is a check that looks present and does nothing.

- **A prefix check built by regex, not by fixed string.** `grep -v "^$ROUND/"` treats the `.` in a path
  like `.hgk/rounds/x` as a wildcard, so `Xhgk/rounds/x/outside.txt` is read as INSIDE and committed. Use
  `grep -F` or a `case` pattern; a path prefix is a literal, never a pattern.
- **`git diff --cached --name-only -z` captured into a shell variable.** Command substitution strips NUL
  bytes and the final newline, so the output is one unterminated line; `while read` then never executes its
  body once, the function returns empty, and every staged path - outside ones included - reads as none.
  This re-opened the exact hole the -z form was introduced to close. Use plain newline output with `-F`,
  and state the limit: names containing a newline are not covered.
- **Receipt existence is not receipt validity.** A gate that tests `[ -f $receipt ]` is satisfied by an
  empty file and by a forged one. Validate CONTENT: token matches this launch, lane matches, route matches
  the one qualified, `child_exit=0`, and the file is a non-empty regular file.
- **Announce a receipt only after the write is verified.** If the path already exists as a *directory*,
  `printf > $path` fails while the wrapper still prints `RECEIPT_WRITTEN` and exits 0. Test the write.
- **Run the final status query AFTER the last commit, and report only that result.** A post-commit hook (or
  any late writer) can dirty the tree after an earlier query; a wrapper that prints the earlier `dirty=0`
  returns 0 over a dirty handover.
- **`BASH_ENV` / `ENV` can restore a mismatch you just closed.** A startup file re-exporting the route
  variable makes the gate qualify one route and launch another. Start children with
  `env -u BASH_ENV -u ENV` **and** have the child re-derive the expected model/effort/route itself.
- **A child that re-derives its assignment must also honour the owner-authorised deviation.** Otherwise the
  gate admits the deviation the owner approved and the child refuses it, and the authorised lane fails
  (observed: lane-set exit 8). Make the owner record the single authority BOTH sides read, and label the
  authorised values as a statement of fact about the accepted artefacts, not as a widening of permission.
- **A qualification that greps sentinel strings is a filter, not a qualification.** A stub that prints the
  two expected strings - doing no tool call at all - passes. Require the CLI's own header and evidence of
  at least two real tool executions; then still state the ceiling, because any transcript check can be
  forged by a stub.
- **An exposed skip/qualify switch is a bypass.** Require a separate, owner-visible acknowledgement file
  naming the reason, and record that lane in its receipt as unqualified.
- **A document claiming a copy that the code never makes.** Moving a manifest out of the tree but never
  copying it back, while the brief or comments say postflight copies it, is a finding in itself: audit
  doc-vs-code disagreement, not only code-vs-counterexample.
- **An authorisation check is fail-open until it is fixed-string, value-validated, role-scoped and total.**
  A gate that matched the owner-approved value with `grep -qx` (a BRE) accepted a value of `.*` as "named in
  the record"; an exception written for one role admitted a different role; a caller-set provider was compared
  by nobody because only model and effort fed the deviation test; and the effort axis had no check at all.
  Match the authorised value as a FIXED STRING after rejecting anything that is not a plain identifier, key the
  record per ROLE and per AXIS (`authorizes_model: <ROLE> <value>`), check every axis a caller can set, and
  make the gate and the child read the identical form so the two cannot disagree. The axes include the ROUTE:
  an owner ruling that runs a checker through a different route is a deviation on that axis, and leaving the
  route unchecked either refuses a legitimate lane or admits an unaudited route.
- **Re-enabling a dormant check re-couples every default to its wrong source.** Making a role parameter
  mandatory switched on an assignment check that those lanes had never executed - and the child then refused
  its own harness every time, because its defaults were derived from the LANE'S NAME: a checker lane named
  `FO*` took the writer's effort and the writer's route against a role assigned the checker's. When you
  enable a check over an axis, make the authority document the source of EVERY default on that axis - model,
  provider, effort, route - and treat only an explicitly overridden value as a deviation. Expect the suite to
  go red for this reason and read it as a design fault in your change, not as broken fixtures.
  Then grep the suite for every call site that BYPASSES the shared helper: those invocations never received
  the newly mandatory input, so one dies on the new requirement instead of reaching the behaviour it tests,
  and another passes FOR that reason while asserting a different rule (a containment case reported PASS
  because the lane had been refused for having no role). Fix the call sites and assert the refusal's reason.
- **Assert with fixed strings.** `grep -q "hard_failure=["` reads the bracket as a character class, so the
  assertion fails against output that plainly contains the string; three assertions were lost that way in one
  session, twice inside helpers whose only job was literal matching. Use `grep -qF --` in every assertion
  helper and keep any real pattern in the individual case, not in the helper.
- **A lexical containment test is defeated by a link.** Comparing `cd "$dir" && pwd -P` output against the
  subject root let a Windows junction write the gate's own log INSIDE the worktree and still return 0. The
  shell's resolver does not resolve a junction at all, and a VCS probe does not either when the destination
  is an ignored directory: git reports the ignored DIRECTORY, never the probe file you put inside it, so the
  probe reads as absent. Decide containment with the OS resolver instead - `os.path.realpath` of the
  destination against `os.path.realpath` of the subject, compared case-insensitively - in the gate AND in the
  child. Then make it **fail closed**: an empty or unrecognised resolver answer must refuse. Treating
  "undecided" as "outside" is how a gate qualified a lane while writing through a junction into the subject.
- **Classify a failure by its STRONGEST marker, not by the presence of a weak one.** A declared failover that
  triggered on exhaustion words found anywhere in the log switched models for a protocol 400 whose text
  happened to contain a quota word, and then reported success - the switch silently did the work the ruling
  forbade. Test the hard-failure markers first (`invalid_request_error`, a reasoning-content round-trip error,
  a provider safety flag, an explicit 400) and veto the switch outright; only a log with none of them may be
  classified as exhaustion. A mixed signal is a refusal to switch, never a licence to try the other model.
  Read the markers from the PROVIDER's own error channel (`^ERROR:`-style lines, the log's last lines as the
  fallback), never from the whole log: a review lane is reading the sources that quote a 400 and a safety
  notice, so a whole-log matcher classifies by quotation and is wrong in BOTH directions - it switched models
  for a lane that had merely quoted one, and it would never switch for a genuine exhaustion in a lane that
  quotes quota text. Add the spellings a provider actually emits (`HTTP 4xx`, `malformed payload`, not only
  `error 400`): a hard failure written the other way beside a quota word still switched and then "succeeded".
  Calibrate the veto POSITIVELY too. A hard-failure pattern widened to catch `4xx` spellings also matched a
  genuine `HTTP 429` exhaustion and vetoed the very signal the failover exists for - a rule that swallows
  its own trigger. Every veto pattern needs a companion case proving the case it must still let through
  still switches, and a bounded refusal is still a defect when it removes the mechanism's only legitimate use.
- **An outer wrapper's own record must be committed before it reports success.** The inner launcher's
  postflight cannot cover a file the wrapper writes after it returns, so a wrapper could exit 0 with its
  failover record still untracked. Commit the record, then re-read `git status --porcelain` and exit non-zero
  on anything left over - the same discipline the launcher applies to itself. Write a record for EVERY
  outcome, not only for a failover: the decision NOT to switch is evidence too, and a wrapper that refuses
  without leaving a tracked artefact is indistinguishable from one that crashed.

## Fixture hygiene in the harness's own tests

- **A test fixture must not delete committed files to build itself.** `rm -f "$CLONE/.../*.manifest"`
  dirtied the clone, and every later case then refused at the clean-preflight check - five unrelated tests
  turned red for one fixture's reason. Locate the current run's artefact by its own stamp instead.
- **A variable used before it is defined kills a whole suite silently.** Creating a fixture file above the
  line that defines the directory variable produced `unbound variable` at line 14 and zero test output;
  the suite reported nothing rather than failing loudly. Order fixture setup after every path is defined.
- **A fixture that injects through a GLOBAL marker can mutate the wrong instance.** A post-commit hook that
  guarded on one marker file appended its forged lines to an OLDER receipt during the preflight commit, set the
  marker, and never touched the receipt under test - so the gate returned a correct 0 and the case failed for
  its own fixture's reason, which reads exactly like the fail-open it was written to catch. Key the injection
  per FILE (append a sentinel line, skip files that already carry it) and, before interpreting the gate's
  verdict, assert that the artefact you meant to corrupt actually changed.
- **A fixture hook must target the current run's artefact, not "the newest" one.** Clones accumulate
  receipts, manifests and logs from earlier cases, so a wildcard plus last-modified ordering silently picks an
  older one. Locate by this run's own stamp or token.
- **Harden into a SCOPE, and prove the scope with a positive control.** Every refusal rule added for a
  counterexample needs a companion case showing the authorised, in-scope value still passes end to end -
  otherwise the suite proves only that lanes are blocked, and a blanket refusal reads as security. Assert the
  axes the exception was granted for, not merely the exit code.
- **A link fixture must target the tree the invocation actually uses, and never the delivered tree.** A
  junction built to point at the delivery worktree instead of the test clone made a containment comparison
  compare two different trees, so the rule under test never fired while the case reported PASS - and the
  fixture then wrote two lanes' logs INTO the delivered tree. Point fixtures at the clone, assert the object
  you meant to create exists, and check afterwards that the delivered tree holds only the changes you meant.

- **An officer lane doing security review can be killed by the provider's content filter.** A lane whose
  context accumulates credential-shaped strings - an ignore rule naming a credential file, an environment
  dump, token-looking values - gets its next request refused (`content was flagged for possible
  cybersecurity risk`), the thread is lost, and the lane exits non-zero with no artefact and no verdict.
  Brief officers to refer to such material as "redacted" and never echo it, tell them not to resend refused
  content, and have them write each finding to disk as they go so a killed attempt still leaves evidence.
  The kill also lands at the REPORTING stage - after every evidence file exists and before the verdict does -
  so require the report to be written in bounded, incremental chunks (headings first, findings as they close)
  and have it name the attack material by FILE rather than re-pasting it into the request.
  A launcher that refuses to mint a receipt for that exit status is working correctly - do not "fix" it.
- **Distinguish an infrastructure kill from a lane-logic failure before reporting it.** The exit code is
  the same. Read the lane log: a provider safety notice or a lost thread is an infrastructure blocker and
  must be reported as one, with the failed round recorded as having no verdict rather than folded into the
  next round's evidence.

## Reading the officers

- Expect the verdict to name its own ceiling: local stub control-flow verification, no model launched, no
  identity authenticated. Carry that ceiling forward instead of rounding it up.
- An officer's `STILL_NOT_CLOSED` on handover hygiene is usually about the harness, not the candidate code.
  Split the finding: the officer independently confirmed the closure's CONTENT (every path under the round,
  no code path changed) while rejecting its CLEANLINESS. Report both halves.
- Officers find real defects three rounds running. Budget for the loop and do not present round N as final.
- **Adjudicate blocker counts by CLASS and by SAMPLE, never by total.** When monitoring a long officer run,
  grep the lane log per error class and then read sample lines of every class above the intervention
  threshold before acting. A class firing hundreds of times is usually the material the lane is REVIEWING
  quoted back into its own log - your wrapper's regexes in its source inventory, the failure records of
  earlier rounds, your own script's lines - while a genuine block shows the lane's own tool invocations
  failing repeatedly without recovery. Intervene only when the samples are the lane's own calls; never steer
  a verification lane to fix its environment, since steering changes its input and costs you its independence.

## A case that passes for the wrong reason is worse than a red suite

- One stub label per case. Two cases sharing a label let the worker succeed on its first call, so the
  case proves nothing while still reporting PASS.
- Assert the REASON for a refusal, not only its exit code, whenever two mechanisms can refuse the same
  input: add a negative assertion for the wrong reason. A junction case whose junction was never created
  refused because the path was unresolvable, and passed.
- Create OS objects (junctions, links) through an API that does not go via the shell: `cmd //c mklink //J`
  returned success and created nothing here, quietly turning the case into a no-op.
- Keep one positive control per admission gate. A gate that refuses everything satisfies every negative
  case; only the control shows the mechanism is a scope and not a wall.
- Re-read the fixture after every re-entry: a repair that shortens a case can leave the original summary
  line and its exit check above the new block, and the file still passes `bash -n`.

## Deriving a repo-relative path is a trap where two path spellings exist

- Never compute a relative path by stripping a prefix off an absolute one: the artifact may carry an MSYS
  spelling (`/tmp/..`) while the worktree is native (`C:/..`), the strip silently does nothing, and a
  native git is handed a path it cannot resolve. Run git from the artifact's own directory and name it by
  basename, so nothing is translated.

## What an officer needs in order to be able to fail you

- Freeze the round while a review lane runs. A repair landed mid-review destroys its frozen observation
  and becomes a finding against the maker.
- Never restate a count in a brief that the artifacts can contradict. Regenerate counts from the raw
  result files at dispatch time and tell the officer to read the files rather than the brief.
- Hand the officer a packaged lane contract when one exists instead of writing your own role prompt:
  reuse its intake template, its report headings and its own bundle validator, and let it fill the
  candidate identity from its own freeze so the maker never authors the binding.
- Give the officer a path adapter in the brief, not a warning. The mismatch runs BOTH ways: a native
  binary cannot resolve an MSYS spelling (git, python), and an MSYS tool cannot create a directory from a
  native `C:/` argument (`mkdir: cannot create directory 'C:/Users/user': Permission denied`). An officer
  burned twenty attempts on the second direction before building its own `cygpath` shim for mkdir/cp.
  Hand it the shim up front, and never steer a running verification lane to fix it - that changes its
  input; fix the brief for the next lane instead and disclose the count per error CLASS.

## An officer's evidence must survive the officer

- **The tree-side bundle is not the evidence.** Read the manifest the officer writes and ask whether the
  files it indexes are readable by YOU. An officer running as a different OS identity stages its reproducers
  in a temp root whose ACLs exclude the repository owner, so the maker - and therefore any third party - gets
  `Permission denied` on the directory listing and on every indexed file while the report's locators point
  straight into it. The findings then survive only as the officer's own account of them: nothing can be
  reproduced, and nothing can be refuted either. Treat a round whose raw evidence you cannot open as
  un-auditable output, regardless of how good the report is.
- **Require the handover, not the promise.** Have the lane archive its external root into its declared,
  in-tree write set from inside its own identity before it exits, or run the lane as the repository owner so
  the temp ACLs match. Accept the round only after reading one indexed file yourself as the maker.
- **Size the bundle before copying it into a repository.** One officer's root ran to tens of megabytes over
  hundreds of files, so preserve the small re-runnable artefacts - case scripts, per-case stdout/stderr and
  result files, index files - and record what was deliberately left behind, with sizes, instead of committing
  a bulk dump that no reviewer will page through.
===== SKCV-TOPIC-SEGMENT 3 END =====
===== SKCV-TOPIC-BATCH END =====
