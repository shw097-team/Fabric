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
