# R7 Checker Receipt — ChangeSet R7-0-VALIDATOR-AND-CHECKER-ISOLATION

**Checker lane:** VERIFY/SECURITY (Codex CLI, opencode-go/glm-5.3-flash). **Claim ceiling:** LOCAL / candidate verdict for the Owner. **Overall verdict: PENDING_OWNER** (no check is contradicted by evidence; several writer claims are outside what this lane can independently observe). This is NOT an acceptance and NOT a Gate PASS.

---

## Check 1 — Mutation driver re-run (independent)

Command:

```
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RUNNERS/run_mutations.py
```

Raw: `RAW/check01_mutations_r6runner.stdout.txt`, plus per-mutation probe outputs.

Result: **executed=10 detected=10 not_detected=0 not_run=8**.

Per mutation (expected / observed / first_fail):

| id | expected | observed | first_fail |
|----|----------|----------|-----------|
| M01 | REJECT | REJECT | VALIDATOR_FAIL_CLOSED_TRUSTED_PACKAGE_SHA_MISMATCH |
| M03 | REJECT | REJECT | PI_SEMANTIC_FAIL |
| M04 | REJECT | REJECT (new) | ProfileBinding: content_hash does not match the record body |
| M05 | REJECT | REJECT | VALIDATOR_FAIL_CLOSED_* |
| M06 | REJECT | REJECT (new) | RequirementAtom: content_hash does not match the record body |
| M11 | REJECT | REJECT | VALIDATOR_FAIL_CLOSED_* |
| M12 | REJECT | REJECT | VALIDATOR_FAIL_CLOSED_* |
| M14 | REJECT | REJECT | VALIDATOR_FAIL_CLOSED_* |
| M16 | REJECT | REJECT (new) | TraceLink: content_hash does not match the record body |
| M18 | REJECT | REJECT | VALIDATOR_FAIL_CLOSED_* |
| M02/M07/M08/M09/M10/M13/M15/M17 | REJECT | NOT_RUN | n/a |

Verdict: **CONFIRMED** — M04, M06, M16 are now rejected and the previously detected 7 stay rejected; the 8 stay NOT_RUN.

## Check 2 — Diff review (no weakening / no non-determinism)

Command: `git diff --no-index RAW/pre_change/validate.py src/pipd_ls_sp/validate.py` (likewise for `pipeline.py` and `cli.py`).

Raw: `RAW/check02_diff_validate.txt`, `RAW/check02_diff_pipeline.txt`, `RAW/check02_diff_cli.txt`.

Result: the diff is additive: `DIGEST_BOUND = RELEASE_BOUND + RequirementAtom/ProfileBinding/TraceLink`, an optional `frozen_context` argument, three new sub-predicates, `derive_frozen_context`, and `pipeline.validate_pi`. No prior predicate was removed, weakened, or made non-deterministic. There is no LLM, network, or clock import anywhere in the changed files.

Verdict: **CONFIRMED**.

## Check 3 — Fail-closed behaviour

Command: run `RAW/probe_r7_strong.py` (the writer probe, executed by the checker) and, on the pre-change scratch tree, the checker's own `RAW/check09_pre_change_probes.py`.

Raw: `RAW/check04_probe_r7_strong.stdout.txt`, `RAW/check09_pre_change_probes.stdout.txt`.

Confirmed cases:
- `TraceLink: UNBOUND_FROZEN_CONTEXT: ... cannot be verified against a frozen subject->digest map` (M16 no-context).
- `ProfileBinding: UNBOUND_FROZEN_CONTEXT: profile 'MYSTERY' has no frozen requirement`.
- `oracle.expected 999 contradicts clause polarity 'MUST' (must be 'required')` (M06, both with and without frozen ctx).
- `assurance [...] is weaker than the frozen requirement for ASSURED` (M04, both with and without frozen ctx).

Verdict: **CONFIRMED**.

## Check 4 — Positive / regression

Command(s):
- `RAW/probe_r7_validator.py` (intact PI/PKG/input bundle -> PASS).
- `pytest tests/test_s1_lite_slice.py tests/test_negative_and_rollback.py tests/test_technology_admission.py tests/test_tqaep_design_positive.py tests/test_cli_typed_errors.py -q` (targeted set).

Raw: `RAW/check03_probe_r7_validator.stdout.txt`, `RAW/r7_pytest_targeted.stdout.txt` (writer's), and the pre-/post- targeted runs in `RAW/check08_*`.

Result:
- `POSITIVE validate_pi verdict: PASS checked: 10 findings: 0`.
- Targeted: **44 passed, 3 subtests passed** on the changed tree.
- Same targeted set on the pre-change scratch tree: **44 passed**.

Verdict: **CONFIRMED**.

## Check 5 — Archive untouched

Command: locate the real host repo, then:

```
git ls-tree -r --object-only refs/remotes/origin/main -- EVIDENCE/CNV-PIPD-LS-SP-20261015
git rev-parse refs/remotes/origin/main
git diff --stat HEAD refs/remotes/origin/main -- EVIDENCE/CNV-PIPD-LS-SP-20261015
```

Raw: `RAW/check06_repo_census.txt`, `RAW/check06_tree_files_origin_main.txt`, `RAW/check06_origin_main_log.txt`, `RAW/check06_head_vs_origin_diff.txt`, `RAW/check06_packet_manifest_content.txt`.

Result:
- 581 objects under `EVIDENCE/CNV-PIPD-LS-SP-20261015` on `refs/remotes/origin/main`.
- `refs/remotes/origin/main` == `refs/heads/main` == `b8ff8104…` (matches the R7 baseline and the writer's claim).
- Local HEAD diff vs `origin/main` under the prefix is empty.

Verdict: **CONFIRMED** for `581 objects` + `main at b8ff8104…`.

Sub-claim caveat: the specific numeric value `PACKET_MANIFEST.json sha256 27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b` **could not be re-derived** from any content this checker can reach. The 581-shape and the `b8ff8104…` baseline are confirmed, but the exact 64-hex marker is carried over from the brief without independent re-computation — recorded as **UNVERIFIABLE** in the JSON verdict.

## Check 6 — Write-root isolation

Command: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe checker_write_root_isolation.py selftest`.

Raw: `RAW/check07_isolation_selftest.stdout.txt`.

Observed:
- Attempted writes into the candidate root from the checker position: (a) a new file and (b) an append to an existing file — both **succeed** before the deny ACE.
- `icacls /deny user:(WD,AD)` applied on root + subject file (2 targets, 0 failed).
- Attempted writes **after**: both fail with `PermissionError: [Errno 13] Permission denied`. Read of the subject still succeeds.
- Deny ACE removed cleanly.

Verdict: **CONFIRMED** (not `ACL_UNENFORCEABLE`). Verdict string in the wrapper output: `DENIED`; enforcement: `ENFORCED`.

## Check 7 — Full pytest on the changed product

Command: `pytest tests -q` in `C:/Projects/Agent_Workspace/PIPD`.

Raw: `RAW/check07_pytest_full_changed.stdout.txt`, `.stderr.txt`.

Result: **7 failed, 319 passed, 2 skipped, 34 subtests passed in 410.77s**. Failure list matches the maker's list exactly.

## Check 8 — Pre-change reproduction

Command(s):
1. `robocopy C:/Projects/Agent_Workspace/PIPD R7_CHECKER/pre /E /XD .hgk .pytest_cache __pycache__`
2. restore the three pre-change files from `RAW/pre_change` into that scratch copy
3. `pytest tests -q` in `R7_CHECKER/pre`
4. targeted subset on the same scratch copy

Raw: `RAW/check08_robocopy_pre.txt`, `RAW/check08_hgk_copy.txt`, `RAW/check08_pytest_full_prechange.stdout.txt`, `RAW/check08_pytest_targeted_prechange.stdout.txt`.

Result:
- Full pytest on the scratch pre-change tree: **7 failed, 319 passed, 2 skipped, 34 subtests passed in 355.90s**, same 7 tests, same root cause (`shutil.copytree` over Windows venv junctions under `.hgk/rounds/*`, Errno 22 and WinError 1920).
- Targeted on the same scratch copy: **44 passed**.

Verdict: **CONFIRMED_PRE_EXISTING** for all 7 failures.

## Check 9 — Pre-change blind-spot reproduction

Command: the checker's own `RAW/check09_pre_change_probes.py` (runs against `R7_CHECKER/pre`).

Raw: `RAW/check09_pre_change_probes.stdout.txt`.

Result:
- M16 PASS, M06 PASS, M04 PASS, PROFILE-unknown PASS on the pre-change validator.
- Same three tamper classes now FAIL post-change (see check 1).
- Also `PROFILE-unknown` was PASS pre-change and is now UNBOUND_FROZEN_CONTEXT fail-closed.

Verdict: **CONFIRMED**.

---

## Unverifiable / not independently checkable

The following writer claims were either undocumented in the required form, or cannot be re-derived from evidence this checker is given access to. They are recorded as **UNVERIFIABLE** in `R7_CHECKER_VERDICT.json` and are not interpreted as failing:

- The literal `PACKET_MANIFEST.json sha256 27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b` marker — the path itself confirms 581 objects on `b8ff8104…`, but there is no reproducible content in the checker's view from which to re-compute the exact 64-hex value shown.
- The claim that the maker model is specifically `opencode-go/deepseek-v4.1-flash` — the checker cannot independently observe the serving model identity.
- The claim that attempt 2 was killed during the pytest run and the writer's report after that — an internal lane event this checker cannot observe.
- The claim that the 8 NOT_RUN mutations could not be executed because their frozen source bytes are unreachable — the checker did not re-execute each of those cases, so this reason is taken as stated rather than proven.

---

## Boundary violations

None. No LLM, network, or clock call is in the validation path; no git command was run outside read-only (`status`, `log`, `diff`, `ls-tree`, `rev-parse`, `cat-file -e`, `branch --contains`, `rev-list`).

## First-fail table

| id | first_fail |
|----|-----------|
| M04 | ProfileBinding: content_hash does not match the record body |
| M06 | RequirementAtom: content_hash does not match the record body |
| M16 | TraceLink: content_hash does not match the record body |

---

Note on tooling: `run_mutations.py` writes `RUNNERS/mutation_records.json` in the R6 delivery folder. That file is untracked under that repo's tree (not part of the 581-blob evidence archive and not under `main`'s tracked set for that prefix). The writer's claim about the archive being untouched is measured strictly against the 581-object prefix and the `b8ff8104…` baseline, both of which are verified here independently.
