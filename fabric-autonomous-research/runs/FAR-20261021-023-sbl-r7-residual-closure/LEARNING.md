# LEARNING — FAR-20261021-023-sbl-r7-residual-closure

> The rules below were each extracted from a failure that ACTUALLY happened in this round,
> with the measurement that produced it. Nothing here is a generalisation from theory.

## L1 — A build that is not a function of its source cannot be a release artifact
**Trigger.** `TT-R6-WHEEL-NONREPRODUCIBLE-001` was filed as an open defect. The obvious reading is
"Python packaging is not reproducible, so this is a property of the platform and we record it".
**Measurement.** `git cat-file blob` showed the committed objects were already LF-clean (CRLF=0),
while the working tree had CRLF — because `core.autocrlf=true` and there was no `.gitattributes`.
zip then recorded 39 differing member timestamps.
**Rule.** Export the build input from the object store, never from the disk. The tool
(`tools/build_reproducible.py`) exports a NAMED COMMIT with `-c core.autocrlf=false` and pins
`SOURCE_DATE_EPOCH`.
**Transfer.** A "known limitation" in our own build inputs is not a limitation; it is our bug.

## L2 — Verify reproducibility per ARTIFACT, not per build system
**Trigger.** After the LF fix, the wheel became reproducible but the sdist did not.
**Measurement.** The `.tar.gz` carried 21 distinct member mtimes and its gzip header embedded the
wall-clock time. setuptools honours `SOURCE_DATE_EPOCH` for the wheel and not for the sdist.
**Rule.** A wheel that is reproducible says nothing about the sdist sitting next to it. Check each
artifact separately and repack the ones the build system does not pin.

## L3 — When normalising an archive, strip the extended header, not just the field
**Trigger.** The first `normalise_sdist` set `member.mtime = epoch` and still emitted 20 non-constant
mtimes.
**Measurement.** `tarfile` in PAX_FORMAT keeps a sub-second mtime in `member.pax_headers["mtime"]`,
and `create_pax_header` only OVERWRITES that header when the value does not fit the 12-digit ustar
field. An integer epoch fits, so the original float survived.
**Rule.** `member.pax_headers = {k: v for k, v in member.pax_headers.items() if k != "mtime"}` before
assigning. A partial fix that leaves the output looking plausible is worse than no fix.

## L4 — Before deferring a residual, ask WHO is missing
**Trigger.** The R6 residual list mixed four different kinds of "not done": a human decision, a
host/native effect, a new build slice, and a defect in our own inputs.
**Measurement.** The wheel item sat in the same list as the plugin-host items, but its missing thing
was US. It closed in one round.
**Rule.** Classify every open item as HUMAN AUTHORITY / HOST-NATIVE EFFECT / NEW BUILD SLICE /
OUR OWN INPUTS. The fourth is fixable now; conflating it with the others is how a fixable item
becomes a permanent "known limitation".

## L5 — A nonce proves the model answered only if the model was asked to say it
**Trigger.** The first R7 lane probe returned `ERR_NO_ARM_EMITTED_NONCE` with `exit=0` and a good
usage row — the arm had served perfectly.
**Measurement.** The nonce must appear in an ASSISTANT message, and the prompt is what puts it there.
Adding the token to the prompt turned all three lanes `ok`.
**Rule.** The prompt carries the nonce, not just the `--nonce` flag. Without it, a healthy lane looks
broken and a broken lane can look healthy.

## L6 — An admission that returns an id is not an admission
**Trigger.** `admit_requirement` returned a workorder id, but the spine readback showed the TaskSpec
still in `DRAFT` and no WorkOrder row at all.
**Measurement.** `_repo_head()` runs `git rev-parse HEAD` in the CALLER's cwd. Outside a repo it
returns `''`, `create_workorder` raises `InvariantViolation`, and the `except InvariantViolation: pass`
swallowed it. The API reported success anyway.
**Rule.** Read the three rows back — requirement, taskspec, workorder — before believing an admission.
A swallowed exception is indistinguishable from a completed transition at the API boundary.

## L7 — A branch review that is not a measurement is an opinion
**Trigger.** 49 non-main branches across two repos, each with a merge decision.
**Measurement.** merge-base, ahead/behind, `diff --stat`, `git merge-tree --write-tree` exit code and
patch-equivalence collapsed 49 branches to exactly one `MERGE_NOW`.
**Rule.** `merge-tree` exit code is the conflict answer; ancestry is the supersede answer. Read the
CI check-runs of the frozen head SHA, never of main and never of a hypothetical merge result.

## L8 — The 8 official PIPD skills were already on main
**Trigger.** A candidate branch in PIPD-LS-SP looked like it might carry the official skills.
**Measurement.** All eight (`pipd-route-intake`, `pipd-authority-source`, `pipd-profile-tailor`,
`pipd-pi-compile`, `pipd-pd-bind`, `pipd-execution-contract`, `pipd-assurance-tqaep`,
`pipd-package-project`) are present on `main` with full contracts, typed IO and POS/NEG/EDGE/SEC cases.
**Rule.** Before merging a branch to obtain a capability, check whether main already has it. Merging
a branch that only restates main brings back conflicts and stale READMEs.

## L9 — The pre-authorisation covered the ruling, not the human boundary
**Trigger.** The owner's message pre-authorised executing the FAR ruling, and the ruling's most
valuable step is merging PR #2.
**Measurement.** The R6 report states plainly that the Reviewer recommended a scoped merge and **did
not press the button**; merge, release, permission grants and Host plugin creation are separately
gated effects.
**Rule.** A pre-authorisation of "execute your recommendation" is not a grant of a Native effect. The
ruling names the merge as a one-action Owner item with a mechanically executable step list, and the
rest of the work was done without waiting for it. That is the honest reading, and it is also the
reading that survives an external acceptance.

## L10 — A test that greps the source cannot fail when the source lies
**Trigger.** The maker's own reproducibility tests for the R7 build fix were green, and the
independent VERIFY lane mutated the candidate three ways and two mutants still passed.
**Measurement.** `.gitattributes` rewritten to `eol=crlf` → PASSED (the test only checked the file
contained the literal `eol=lf`); `normalise_sdist(sdist, epoch)` replaced by `pass` → PASSED (the
test checked the source for the *call*, so removing the call was invisible); `.gitattributes`
deleted → FAILED, the only mutant that was caught.
**Rule.** Assert the behaviour, not the spelling. A source-text assertion survives exactly the
mutation it was written to prevent. The durable fix is a mutation probe: break the mechanism on
purpose in a throwaway copy and assert the suite goes red. A suite that cannot fail is not a suite,
and a green suite that cannot fail is worse than no suite, because it converts an unverified fix
into a claimed verification.

## L11 — A build tool that depends on the ambient interpreter is an environment bug wearing a product costume
**Trigger.** The independent checker's venv has no `build` package, so the candidate's build step
failed with `No module named build.__main__` — an error that reads like a broken artefact.
**Measurement.** `import build` succeeds in exactly one ambient interpreter on this machine; the
checker's dedicated venv does not have it. The artefact was never the problem.
**Rule.** The tool that produces the evidence must resolve its own dependencies and say what it
checked. Resolution order must be explicit and overridable (`SBL_BUILD_PYTHON`), and the failure
message must name the interpreters it tried. When a reviewer hits a dependency error, the first
question is always "is this the product or the environment?" — and the answer must be
mechanically checkable, not asserted.

## L12 — An exhausted quota is not a verdict, and not a defect
**Trigger.** The first independent VERIFY round ended `exit=1` with the upstream message "You've hit
your usage limit… try again at 2:59 PM" after 392 seconds of real work.
**Measurement.** The round's own bytes are intact: `nonce_present=true`,
`usage_status=200`, `usage_receipt_ok=true`, `stdout_sha256=80397dbb…`, `stdout_byte_exact=true`.
The failure is `turn.failed` from the provider, not a candidate failure. The substantive findings
made before the limit (2 of 3 mutants passing) were still valid, and were fixed and re-measured on
the maker side.
**Rule.** Classify the exit before classifying the candidate. A provider-side `turn.failed` after a
successful usage receipt is an *incomplete round*, not a FAIL verdict, and it must be recorded as
such: preserved, not counted, re-run. Never round an incomplete round up to a verdict, and never let
its incidental findings be lost just because the round did not finish.


## L14 — When a concurrent process writes the same file, the owner's ruling outranks every variant
**Trigger.** Mid-round, the owner changed the PLAN and VERIFY/SECURITY lane models. A concurrent background
process on the same working tree wrote a *different* pool variant in which the EXECUTE lane was rebound
too, and left the file merge-conflicted with a stash on the repository.
**Measurement.** Three states existed at once: the committed revision 11 (owner-ruled: PLAN=minimax,
VERIFY=minimax, EXECUTE=deepseek), a conflicted working tree, and a stash holding the all-minimax
variant. The dispatcher then failed with `ERR_SLOT_POOL_MALFORMED ... Expecting property name enclosed in
double quotes` — the conflict markers were in the JSON the resolver reads.
**Rule.** A file under concurrent write is not a source of truth; the committed state plus the owner's
words are. When two variants of a binding exist, do not merge them and do not pick silently — ask, then
restore the ruled variant over the working tree and DROP the other, never apply it. And record the
conflict itself: a stash on the control-plane repository and a conflicted artifact are round events an
external reviewer must be told about, not noise to be cleaned up quietly. A parse error in a governance
artifact is a governance incident, not a syntax bug.

## L15 — A lane binding is only real if the lane can RUN on it
**Trigger.** The machine was rebooted between rounds and the Codex CLI had been upgraded in place. The
declared toolchain pin named `.../bin/896a0166b774037a/codex.exe`; that directory no longer existed.
**Measurement.** Every lane dispatch failed BEFORE SPAWNING with `ERR_LANE_PIN_IDENTITY_INVALID` /
`ERR_LANE_TOOLCHAIN_BINARY_MISSING`. The SBL EXECUTE and VERIFY lanes could not run at all — including
the independent acceptance officer, which is why the round could not close. Repairing it required TWO
surfaces to move together: the live declaration and the registry's `/codex_version` and
`/codex_sha256` expected values. Changing one alone made the drift gate report fatal errors; that is
the gate working, not a regression.
**Rule.** A configuration that parses is not a configuration that works. After any host toolchain
upgrade, re-derive the pin FROM THE INSTALLED BINARY — discover the path, ask the binary its version,
hash the file — and re-pin every expected value in the same change. Then prove the lane RUNS: a live
probe with a nonce and a usage receipt is the only evidence that a lane binding is real. A config-only
test suite would have stayed green while every lane was dead.

## L16 — A hand-written declaration of a machine-checked file is a defect, not a convenience
**Trigger.** After the owner order promoted GPT 6.1 SOL to rank 1 on PLAN and VERIFY_SECURITY, all three
lanes' `selection_note` still read "minimax-m3.1-flash-free (opencode-go) is rank 1".
**Measurement.** The note contradicted the same file's `declared_by`, its `change_log`, and its own
`ordered_pool[0]`. A reviewer reading the note would have concluded MiniMax was the PLAN binding — the
exact lane-vs-session confusion the owner ordered to be eliminated. The drift gate did NOT catch it:
the gate compares machine-checked values, and prose is not one.
**Rule.** Never hand-write what a machine-checked file already states. Generate the note from
`ordered_pool[0]` so it cannot drift. And treat a stale prose field as a real defect even when every
automated gate is green: a green gate only means the gate's own fields agree, not that the document
tells the truth.

## L17 — An acceptance check that pins an earlier run's value checks the past, not the state
**Trigger.** The R7 self-check C6 asserted that the checker transcript contained round 1's nonce token.
**Measurement.** The nonce is per round. A fully successful, correctly-armed, correctly-nonced round 4
would still have failed C6, so the round could never have reached 16/16 — the check was validating the
checker's ability to echo a token it was never given. Fixed to read the nonce from the receipt, with a
fallback to the token found in the transcript.
**Rule.** Read the expected value from the artefact under test, never from a constant that a past run
produced. And verify an acceptance-check fix against synthetic scenarios — success, stale-arm,
missing-token, wrong-arm — before trusting it. A check that cannot fail for the right reasons will
eventually fail for the wrong ones.

## L18 — A green maker run and a red CI run are two facts, not a contradiction
**Trigger.** The maker's Windows suite was green while the hosted CI had been red for five consecutive runs, on both ubuntu and windows.
**Measurement.** The CI workflow installs pytest and nothing else, so the `build` package is absent on the runner. The sdist-normalisation test stubbed the build COMMAND but still let `build()` resolve a backend interpreter, so it raised SystemExit there — an environment gap reported as a product failure. Because the mutation probe requires the unmutated tree to pass, the whole probe went red with it. Reproduced locally by removing the backend from PATH: the failure reappeared exactly, and vanished when the backend was reachable.
**Rule.** When two environments disagree, build the second environment before theorising. The maker's machine had a build backend and a PATH with interpreters on it; the runner had neither. A defect that only appears where a tool is missing is usually the tool's absence being misreported as a defect — find the exact difference and reproduce it.

## L19 — An INCONCLUSIVE verdict is not an empty verdict
**Trigger.** The R7 checker round 4 returned INCONCLUSIVE — NOT ACCEPTED because its sandbox forbids every filesystem write, which would normally mean "nothing learned".
**Measurement.** The same verdict reproduced the W1 defect and reported the fail-open skip and the weak mutation oracle as defects. All three were real and independently reproducible on the maker side.
**Rule.** Read a non-acceptance for what it actually measured. "Could not verify" and "found nothing" are different statements, and the first one can carry real findings about the thing that could not be verified. Dumping the round on the word INCONCLUSIVE would have left three live defects in the acceptance oracle itself.

## L20 — Isolation is a property of the whole environment, not of one call
**Trigger.** The mutation probe's write-through defect looked fixed after giving the copy its own git dir, and the independent SWARM audit still found two escape routes.
**Measurement.** The probe copied `os.environ` wholesale and overrode only GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE, so GIT_COMMON_DIR or GIT_OBJECT_DIRECTORY could still point into the protected repository. And `copytree(symlinks=True)` kept symlinks, so a mutation writing to a linked file could follow it back into the protected tree. The audit also reported two protected files changing during the run; that turned out to be the orchestrator's own concurrent edits, verified independently by the staged tree, HEAD and cached diff all being unchanged.
**Rule.** When you isolate a write, enumerate every channel the write could take — environment, filesystem, IPC, subprocess — and close each one. Then verify the invariant semantically (staged tree, HEAD, status) rather than by a file hash: git rewrites the index's stat cache on any read, so a hash changes without the staged content changing. And check a reported violation yourself before believing it.

## L21 — When the maker is green and CI is red, the difference between the environments is the subject
**Trigger.** Hosted CI had been red for five consecutive runs (27..33) on both ubuntu and windows while the maker's Windows suite was green. The available reading was "the product is broken"; it was wrong.
**Measurement.** The CI workflow installs pytest and nothing else, so the `build` package is absent. `build()` still resolved a backend interpreter even when the build COMMAND was stubbed, so the resolution raised SystemExit, the environment gap was reported as a product failure, and the mutation probe went down with it because it requires the unmutated tree to pass. Reproduced locally by putting git on PATH and removing the backend: the failure was byte-identical, and it vanished the moment a backend was available. After the fix, hosted CI was 37/37 green.
**Rule.** Do not fix the product because CI is red. Enumerate what CI has that the maker does not, reproduce that gap exactly, and only then decide whether the defect is in the product or in the environment. A suite that turns green while the difference stays unexplained is not a fix.

## L22 — A toolchain upgrade is a governance event
**Trigger.** The Codex CLI was upgraded in place and every governed lane broke at once with `ERR_LANE_PIN_IDENTITY_INVALID` -> `ERR_LANE_TOOLCHAIN_BINARY_MISSING`, before anything was spawned.
**Measurement.** The declared pin, the installed binary and the registry's two expected values are three surfaces. Refreshing only the active declaration left the registry stale and the drift gate reported findings. Refreshing all of it in one commit took the drift gate to 0 findings / 0 fatal / 90 sites, and all three lanes then re-measured on the canonical pool with a nonce and a usage receipt.
**Rule.** A dependency that is pinned by digest is part of the control plane, not part of the environment. Pin, binary and every expected-value surface move in the same commit, the drift gate must read 0 findings before "recovered" is claimed, and historical evidence keeps the old path, because the old path is a fact about what ran then.

## L23 — When only PASS and FAIL are available and the truth is neither, under-claim
**Trigger.** The independent checker's formal verdict was `INCONCLUSIVE -- NOT ACCEPTED`, and the round's own merges and release were sitting there ready to be recorded as a PASS.
**Measurement.** The typed acceptance API offers exactly PASS and FAIL from NOT_RUN. The checker's own words were INCONCLUSIVE. An earlier workorder had recorded a PASS nobody gave and was retracted to ROLLED_BACK; the correct move was a NEW requirement/taskspec/workorder/acceptance carrying FAIL, with the checker's own transcript as the evidence ref, leaving the retracted record intact for the audit trail.
**Rule.** Prefer the verdict that under-claims. An acceptance that says FAIL is actionable and cheap to advance; an acceptance that says PASS and cannot be defended is a liability that lands on whoever reads it next. Never rewrite a retracted record — add a new one and let the history show both.

## L24 — A check that breaks because the world legitimately moved must be re-derived, not relaxed
**Trigger.** Three self-checks started failing right after the release, and the fast path was to loosen them until they went green.
**Measurement.** C6 read the guard verdict from a field the dispatcher does not write. C8 asserted "no tag, main unmoved", which the legitimate release had invalidated. C10 compared the release commit to the merge commit, which are different commits by construction. Each was corrected to assert the property that actually matters: read the field the dispatcher writes, pin the published state, and compare the version commit's TREE with the merge commit's tree. The self-check then read 16/16 with every check still able to fail.
**Rule.** Before editing a failing check, decide which of three things happened: the product regressed, the check was wrong about the state, or the state was replaced. Only the second case justifies changing the check, and the corrected check must be at least as strict as the old one. A check that cannot fail is decoration, and decoration is how a round convinces itself it passed.
