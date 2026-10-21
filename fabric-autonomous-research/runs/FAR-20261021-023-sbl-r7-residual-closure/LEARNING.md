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
