# Cross-model verification rounds: what actually earned its keep

Observed on a repair round where the maker was `opencode-go/deepseek-v4.1-flash` and the
independent checker was `openai-codex/gpt-6.1-sol` (native OAuth), each in its own context.

## A cross-model checker is not ceremony — it finds real defects

The maker's own end-to-end probe and full test suite were green, and the maker had already reasoned
about the exact risk area. The checker still returned FAIL, with a counterexample the maker had
explicitly flagged as *possible* but had concluded was unreachable. It was reachable.

Rule: when a repair narrows what a validator strips or tolerates, state the residual widening as a
claim for the checker to rule on **by name**, and expect a ruling rather than agreement. Do not
pre-empt it by asserting the risk is latent.

## Ask for comparative evidence, not just a verdict

The strongest part of the checker's FAIL was that it ran the **baseline** (the already-published
artifact) against the same fixtures and showed the two disagreeing. A bare "this passes" from the
checker would have proved nothing about widening.

Rule: for any claim of the form "X is still enforced", require the checker to show the pre-repair
artifact rejecting the same fixture. Two artifacts disagreeing is evidence; one artifact agreeing
with itself is not.

## The same checker re-testing its own counterexample is a re-verification, not a fresh officer

Closing a counterexample normally means the officer who filed it re-tests. That is correct process,
but the resulting PASS is **weaker** than the original FAIL and must be labelled: same lane, did not
write the fix, nothing verified outside the named claims. Ask for that disclosure in the verdict
file rather than leaving it implicit.

## A child's "this failure is pre-existing" verdict must be measured, not believed

A bounded-writer child reported a failing test as "pre-existing and unrelated". It had only tested
the commit that already contained the change. Counting the subject at both commits showed the base
was below the threshold (996) and the change pushed it over (1015), so **the child's own change**
caused it. Always diff the metric at the parent commit before accepting a pre-existing claim.

## Prefer repair-the-check over drop-the-evidence

When a size or count heuristic trips because legitimate evidence grew, the fix is to make the check
assert its stated intent (e.g. "no tracked path is version-control machinery") rather than to raise
a magic number or stop committing receipts. Whenever you repair a guard, add a test that proves the
guard still **fires** on a poisoned input — a guard that only ever sees a clean list proves nothing.

## Reproduce the counterexample yourself before dispatching the fix

Run the checker's fixture by hand first. It confirms the finding is real, gives the writer an exact
red state to turn green, and prevents a fix aimed at the wrong mechanism.

## An isolated checker INHERITS the parent's model unless you pin it

Context isolation and model independence are different properties, and only the first is free. A
child dispatched for independent acceptance runs on the parent's model by default, so a checker can
end up on the *same model family as the maker* while every other independence property holds: own
context, no sight of the maker's reasoning, every value re-executed from the published bytes. That
still leaves common-mode error uncontrolled — a same-model checker can fail the same way the maker
does and agree with it.

Rules:

- **Pin the checker's model explicitly, or verify what actually ran before labelling a PASS.** The
delegation manifest at `delegation/live/<delegation_id>/manifest.json` records `model`, `provider`,
`status` and `exit_reason` per task. Read it — do not infer the model from the task text or from the
config you believe is active.
- **Label the verdict by what the manifest says**, e.g. `INDEPENDENTLY_RE_DERIVED` (isolation only)
versus cross-model corroborated. Never let "independent acceptance officer" in a prompt be read as
evidence that a different model served it.
- When the mandate names a specific checker model/lane and you substitute, disclose the substitution
as **weaker, not equivalent** — and say which property was lost.

## Recover a child's result from its transcript when the completion message does not arrive

A finished child's consolidated result normally re-enters the conversation as a completion message,
but delivery can lag or miss. The output is not lost:

- `delegation/live/<delegation_id>/manifest.json` — per-task `status`, `exit_reason`, duration,
  `model`/`provider`, and the log path.
- `delegation/live/<delegation_id>/task-<n>.log` — append-only, the full assistant/tool trace, and the
  child's final report verbatim.

Check `delegation_task(action='list')` first to confirm the child is finished; reading a *completed*
child's files is recovering a result, not polling. When the formal message later arrives, re-read it
against your transcription — it can carry facts the transcript did not surface.

## Quote the checker's could-not-verify list in full, not summarised

The list is the verdict's real boundary. Paraphrasing it hides exactly the limits a downstream reader
needs, and the checker often names one nobody asked about (a commit sitting after the tag, the
narrower scope of a headline number). Carry it verbatim into the round's evidence, and keep the raw
transcript alongside it.

## Fix the CLASS, then RE-RUN - a fix alone ships the second instance

Measured over four verification runs on one artefact: FAIL(1 of 12) -> fix -> FAIL(2 of 12) -> fix the
class + correct the over-claim -> PASS(12 of 12). The middle FAIL mattered most. The first defect was a
pinned target pointing at a path that never existed; the second was a *different field in the same file*
pointing at the same never-created path. Repointing the first field did not repoint the second.

Rules:

- When a checker finds a defect, grep the whole artefact for the PATTERN, not the symptom. "One dangling
  target fixed" invites "the other dangling target" as the next verdict.
- **Always re-run after a fix.** A re-run with no change would have missed the second instance; a fix
  with no re-run would have shipped it. The re-run is what makes the fix a fix.
- Expect the checker to be right more often than comfortable. Sorting verdicts into "harness artefact"
  versus "real defect" is necessary, but the default must be *real defect* - three FAILs in this work
  were the artefact's, only the earlier two were the prompt's.
- **A class that recurs across passes is the MAKER's habit, so hunt it without the checker's help.** Count
  the disagreements by class, not per pass, and when one class dominates, sweep EVERY artefact for it
  mechanically instead of fixing the next instance the checker names. Measured: one round's dominant class
  was "a claim outrunning its measurement", appearing across successive passes; a scan of the round's own
  files for strong-claim words ("proves", "proof", "demonstrably", "guaranteed") found two live instances
  that no pass had reported yet. A checker reads what you hand it; only you can read everything you wrote.

## A table of PASSes will be FAILed for over-claiming - grade it by EVIDENCE CLASS instead

The clause that kept failing was not a check but a *summary table* inside the artefact, listing
acceptance criteria each marked PASS. An honest checker FAILs that, because several rows assert what no
checker can establish: a test run on another host, the absence of a secret anywhere in a repo, a write
to a governance database nobody queried.

Rule: grade every row by the kind of evidence behind it, in the artefact itself -
**INDEPENDENTLY VERIFIABLE / HISTORICAL-NOT-REPRODUCED / SELF-REPORTED-NOT-ESTABLISHED /
RECORDED-NOT-QUERIED** - and say which rows must not be cited as established. This makes the artefact
claim LESS, which is why it is a fix rather than a rewrite-to-agree. Confirm afterwards that the
checker passed it as a **disclosure-accuracy** finding, not as proof that an outside party re-ran
the verifiers; if you cannot tell the difference, you have rounded a caveat up into a PASS.


## A kill you did not VERIFY is a claim you must not make

Measured: a long verification run was "aborted" with `taskkill //F //PID <pid>` inside a git-bash/MSYS
shell. MSYS mangled the `//F` switch, taskkill printed an error, and the command's `| head -2` hid it; the
run kept going to completion in parallel with its replacement. The operator had already told the user the
round was aborted - a reported intervention that never happened.

Rule: verify termination like any other side effect. Check that the pid is gone (and that no child such as
the agent CLI survives) before claiming a run was stopped, and prefer a kill form the shell cannot rewrite.
Worse than the wasted compute is the dishonest status: a run you believe is dead but is not can write the
same output path as its replacement, so you no longer know which result you are reading.

## Guarding against smoothing can MANUFACTURE a discrepancy - "unreconciled" is also a claim

Measured: told to report honestly, a builder wrote that two accounting axes "do NOT reconcile" and that
the difference was "recorded, not smoothed over". A checker FAILed it: the two axes had already been
reconciled in the previous round, with the arithmetic written out, and an independent re-count confirmed it.

Rule: never report "these figures disagree" as a virtue without attempting the reconciliation first. An
assertion of unreconciled-ness is an unchecked claim, the same class of error as asserting a PASS without
running the check - just pointed the other way, and it is no more honest for sounding cautious. Derive the
bridge (does A = B + C across every term? which single row separates the axes?) or state that you tried and
could not. "I could not reconcile these" is a finding; "these do not reconcile" without the attempt is a
fabrication with a modest tone of voice.

## A prompt encodes an EXPECTED SHAPE - change the artefact and the old prompt manufactures a FAIL

Measured: after an adjudication deliberately changed an artefact's fields (dropping a
`provisional: true` / `ratification_required: true` claim in favour of an explicit refusal), the
NEXT verification run was launched with the previous round's prompt. That prompt still asked the
checker to confirm the OLD flag values, so it would have FAILed an artefact that was correct.

Rule: when the subject changes by design, the prompt is part of the subject. Either rewrite the prompt
in the same change, or expect the checker to be marking an answer to a question nobody is asking.
Before every launch, re-read the prompt against the current artefact and ask: does any line assert a
value this round deliberately changed? Treating a stale expectation as a defect finding is the same
error as the branch-pin mistake, in a different costume.

## Pin the IMMUTABLE refs; REPORT the mutable ones

A verification prompt that pins a **branch** to a fixed sha manufactures its own FAIL. Measured: a
prompt told the checker to confirm `branch main -> still <sha>`, but the round had legitimately
advanced `main`, so the checker correctly failed check 1 while every substantive check passed. The
verdict read FAIL and the cause was entirely the prompt's.

Rules:

- Assert only what cannot move: release **tags**, content hashes, published asset bytes. Never assert
  a branch tip, a run id, or anything a later commit changes.
- Tell the checker explicitly which facts are fixed and which it should merely *report*, or it will
  dutifully fail the report-only one.
- When a checker FAILs on a stale expectation, classify it as a **harness artifact** and say so
  plainly — then fix the prompt and re-run. Do NOT quietly re-run until it passes without disclosing
  that the first verdict was manufactured by the prompt.
- Prefer re-runnable prompts by construction. A prompt that must be edited every round is a prompt
  that will eventually be edited *to pass*.

## A lane that "requires" a model may still run a different one

Measured: a dispatcher flag `--require-arm <provider>/<model>` verified the arm survived the identity
gate but did **not** restrict the candidate list. The run walked the pool in rank order and stopped at
rank 1 — the maker's own model — then reported `required_arm != served_arm` after the fact. The
receipt's `attempts` array is the authoritative record of what actually ran; a usage-log window is
not (unrelated traffic on the same relay lands in the same window and can be mistaken for the run).

Rules:

- Read `attempts` and `used_rank` from the receipt to establish which model served the turn, and
  corroborate with the relay's own usage row for that window — never infer from the flag you passed.
- Pin the rank as well as the arm, and cap the candidate count, or the arm you required may never be
  reached.
- Label a same-model run as isolation-only, never as cross-model corroboration.

## Freeze the subject BEFORE you launch the guard

The guard snapshots the subject tree at launch and re-snapshots it at exit, so **any write during the
run** — including a legitimate evidence or report file the round is supposed to produce — makes the
non-mutation check fire. The verdict then reads as though the subject were volatile, and the cause is
entirely the harness. This has bitten twice in the same shape, so treat it as the default failure:

- **Commit or otherwise freeze everything before starting the guarded check**, including the round's
own evidence and report files, so nothing is written while it runs. Writing the report is the LAST
step, after the check, not something done in parallel with it.
- Have the checker's prompt distinguish the two cases: an **untracked** round artefact is not a defect
of the release, but a **modified tracked** file is. Ask for exactly what the untracked entries are
rather than letting a bare `git status --porcelain` decide the verdict.
- If you do write mid-run, do **not** quietly re-run until it passes. Say the verdict was manufactured
by the harness, then re-run on a frozen subject. A silently-repeated run is indistinguishable from
editing the prompt to pass.

## A fail-closed pre-spawn gate may refuse the run — read the gate, do not guess

Pointing a runner at a home/credential store that holds a real login makes every key-auth arm's
"no human-attended identity" claim false, so a properly built dispatcher **refuses before spawning**
and returns a named error code plus its own acknowledgement flag. Do not guess at the flag, and do not
read the refusal as a broken tool:

- **Grep the dispatcher for the error code** and read the guard's condition and its comment. The code
names both the reason and the acknowledgement flag.
- Passing the acknowledgement flag is legitimate — it is an explicit, recorded consent, and the receipt
carries a field showing it was acknowledged. That is not the same as suppressing a check, and it must
be disclosed in the round's evidence as such.
- A refusal that returns in seconds with no spawn is the gate working. Record the code and the flag you
used; do not retry the identical invocation hoping for a different result.

 ## Classify a FAIL per occurrence — the harness is not the default explanation

 The mirror of the harness rule above, and the easier one to get wrong once you have learned that rule. A
 checker FAIL is **not** presumptively your harness's fault: if it names a target, path or claim that YOU
 declared, the defect is in your artefact.

 - Look at **where** the FAIL lands. A FAIL on a value you pinned, a path you listed or a sentence you
 wrote is your artefact. A FAIL on a fact that legitimately moved after the prompt was written is the
 harness.
 - **Fix the artefact and re-verify.** Do not soften the prompt so the item passes. A checker that only
 ever disagreed for harness reasons would be useless, and a maker who assumes every FAIL is the
 harness's fault is worse off than one who never learned the rule.
 - Report the shape exactly: FAIL on one item and PASS on the rest is that, and the item gets named. Not a
 broad failure, and not a pass with a footnote.
 - Report a **held guard** as a fact separate from the verdict. A FAIL with an unmoved subject digest and a
   clean receipt still proves the run was real, and that distinction is what a downstream reader needs.

## State the QUESTION, never the maker's conclusion - an asserted claim becomes the thing that FAILs

Measured: a brief told the checker to confirm that a gate "refuses a configured-but-unprobed credential".
That sentence was the maker's belief, not a measured fact. The checker executed the source, found an
explicit opt-out flag under which the same configuration returns `verdict: OK, abort: false`, and FAILed
ai - correctly, because the artefact asserted something false. The defect the round then had to fix was
the brief's own assertion.

Rules:

- Write the brief as **questions plus the exact reproduction**, not as a list of the maker's conclusions.
  "Determine X by executing the committed source" survives a checker that disagrees; "confirm X" turns
  every disagreement into a FAIL of your artefact.
- **Enumerate the opt-outs.** For any gate you claim is enforcing something, require the checker to list
  every flag, env var or branch that turns the enforcement OFF, and to report the verdict each one yields.
  A control is only as strong as its escape hatches, and the maker reliably forgets its own.
- When the checker disproves an asserted claim, fix the CLAIM first and say so in the artefact. Changing
  the code's semantics to rescue a sentence is the wrong order, and broadening what a verdict name means is
  a contract change that belongs in its own round.

## A rejected turn is VOID, not a FAIL - and its WORK must be retained if you act on it

A lane gate that requires a token in the child's final message will reject a turn that did the entire job
but omitted the token: the receipt reads as a lane error while the cause is the delivered brief, and the
verification is discarded unread. Two rules follow.

- **Put the output contract in the brief, explicitly** - any required nonce or sentinel on its own line,
  then the verdict block, and nothing after it. "Output JSON only" is a complete instruction that still
  omits the protocol element the gate checks, and the child will comply exactly and be voided.
- **Classify it as VOID, never as a failed check**, and keep the raw output. If you then act on the
  findings, retaining them is what makes the corrections traceable - but store them with an explicit
  `status: VOID` and `is_an_acceptance_input: false`, because a void turn is not an acceptance input even
  when its reasoning is the reason your artefact changed. Deleting it hides the basis for the fix;
  citing it as a verdict launders an unverified turn into acceptance.

## An acceptance rule can be self-referential or infeasible - test the rule, not just the artefact

Two measured cases, one cause: the rule as written could not be satisfied by a correct subject.

- **Self-referential.** A check ordered the checker to scan the round for secret-shaped literals and
  listed those literals as examples in the brief - so the brief matched its own scan. The checker reported
  the hit, and correctly labelled it an acceptance-rule failure rather than a leak. Never write a literal
  you are also searching for; describe the pattern instead, or exclude the instruction document by name.
- **Infeasible.** A brief ordered "no writes anywhere" while two of the required suites create temporary
  files. The checker refused to run them and returned UNCERTAIN, which is the honest answer - and it
  converted two checkable claims into unverifiable ones. A no-write rule must name **one permitted
  directory** for temporary files, and the artefact must say the designated subjects are still protected.

Rule: before dispatch, read the required checks and ask what a compliant checker is FORCED to do to
satisfy them. If any check needs a write, a literal, or a network call you forbade, the rule is wrong, not
the checker.

## When you change what a suite reports, grep the artefacts that DECLARE the old count

Measured: a fix split one test into three, so the suite began reporting seven checks instead of five. The
manifest that INVOKES that suite still declared "5/5 PASS" in its expectation field, and a checker caught
it by reading the committed suite. Nothing in the code was wrong; the declaration was stale.

Rule: a declared expectation is part of the artefact. When a count, a list length, a verdict name or a
pinned target changes, grep the whole repository for the OLD value - manifests, guides, admission
receipts, generated crosswalks - and update each declaration in the same change. This is the same
"declared != measured" class as a gate that claims to enforce what an opt-out bypasses, and a checker will
find both by reading what you wrote rather than by running what you built.

## Threading a flag through ONE return path is not threading it through the FUNCTION

Measured: a new field had to be added to every verdict a gate returns, so an unproven pass could be told
from a probed one. The flag was given to the function's FINAL `_verdict()` call. The function had **four**
return points; the early ones kept the old default. A path that returned early therefore still reported
`provenance: PROBED` while the flag had just skipped the probe - the exact mislabel the field existed to
prevent, reintroduced by a partial fix. The next checker pass caught it with a concrete counterexample,
not with a reading.

Rule: when you thread a parameter, a capability or a guard through a function, **enumerate the call sites
mechanically and assert the count** - regex the function body for every `_verdict(` / `return` / `raise`,
list them, and check each one. Do not fix the site you were looking at: that is the one you already fixed.
A spot-check proves nothing about the sites you never opened.

Corollary for the checker side: after a maker fixes a counterexample, re-run **every reachable mode**, not
just the one that failed. The modes an early return hides are exactly the ones the first pass never
exercised - and "the counterexample no longer reproduces" is satisfied by a fix that closed only that one
door. Likewise for the report: a mid-loop fix is VOID as evidence until a pass measures the corrected
tree, because "a fix was written" and "a fix works" are different claims.

## Give the loop a STOP CRITERION - some items can never be PASS

A verification loop that keeps finding smaller true defects looks like progress and is not converging,
because a subset of a verdict can never come back clean. Name that subset **before** the final pass, in the
brief, and stop paying for it:

- **A defect inside an IMMUTABLE artefact is corrected FORWARD, never rewritten.** A false sentence in a
  commit MESSAGE, or in a published tag's annotation, cannot be amended without rewriting history - which
  the owner grant forbids. Fix it where it is mutable (the FAR, a docstring, a later commit), disclose that
  the original stands, and mark it terminal: every later pass will re-report it, and re-fixing it is the
  stuck shape. Say in the brief that this item is expected and is not progress.
- **A claim the checker structurally cannot establish is terminal too.** Attribution of a write made with a
  credential you deliberately withheld from a credential-free checker does not become provable by running
  more passes. State it as a claim ceiling, not as an open defect.
- **Ask the checker to say so when it finds nothing.** Absent that instruction, "no new fixable defect" gets
  dressed up as a finding, and a pass with genuinely nothing to report is indistinguishable from one that
  was fished for a failure. Explicitly forbid manufacturing one.
- **Publish the criterion, do not hold it in your head.** Write which items are terminal and why into the
  round's own closure evidence, so the decision to stop is reviewable rather than an unstated judgement
  made at the moment the loop got tiring.
