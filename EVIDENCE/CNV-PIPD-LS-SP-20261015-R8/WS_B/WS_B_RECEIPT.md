# WS-B RECEIPT — R8-0 rebuild of the R7-0 validator hardening on `main`

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`.
HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`. Authority: PKG v2.0.0 + EIA-R6-04.
Closes `BLK-R7-WS1-STALE-BASELINE` (high).

**Claim ceiling: LOCAL / candidate-only.** A green local run is neither an acceptance nor a Gate
PASS. No acceptance case was run. No remote was contacted. No release branch was created.

Work root: `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/`
Worktree (left in place for the orchestrator): `C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt`

## 0. Bottom line

- The R7-0 hardening was **rebuilt on `main` (`dba4b19`)** as a semantic patch (not a file copy),
  resolved by hand at the two conflicts, and verified to be hardening-only against `main`.
- The 18-mutation rerun **on `main`**: `M04`, `M06`, `M16` = **REJECT** (the property EIA-R6-04
  requires), all 10 previously-detected ids stay detected, 0 not-detected, 8 `NOT_RUN`
  re-judged with reasons.
- **Honest partial:** the ported hardening introduces **2 test failures** on `main`'s newer
  suite (both pass on clean `main`). Root causes are recorded in §4; neither was "fixed", and the
  R7 target semantics were not altered.

## 1. Environment and anchors

Python: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (pytest 9.1.1).

| file | `main` `dba4b19` (sha256 prefix) | in-tree at worktree |
|---|---|---|
| `src/pipd_ls_sp/validate.py` | `50d69fe651cadebe` | ✓ matched |
| `src/pipd_ls_sp/pipeline.py` | `ace1c68c5cf2c5ac` | ✓ matched |
| `src/pipd_ls_sp/cli.py` | `cc97660b079f7c4f` | ✓ matched |

R7 pre-change anchors (`R7/RAW/pre_change/`): `f3da9e413cda1c7d` / `620a5f4f03458697` /
`29470f7f77214bea`.
R7 post-change target (found at
`R7/R7_CHECKER_ATTEMPT3/a3_driver/product_changed/src/pipd_ls_sp/`):
`5a298eb50685a9e3` / `844bc5433252b2dc` / `eb7c54293862129d` — **identical to the brief's "R7
post-change" column.** (The brief's sha column is the sha256 of file content with the trailing
newline normalized.)

## 2. Step 1 — new detached worktree at `main`

```
git -C C:/Projects/Agent_Workspace/PIPD worktree add --detach C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt dba4b19
git -C .../r8-wt rev-parse HEAD   ->  dba4b19456777d3b597fdf71480f6423dd974243   (exit 0)
```

`git rev-parse HEAD` = `dba4b19456777d3b597fdf71480f6423dd974243`; the three file shas equal the
`main` column above. The path did not pre-exist; the worktree was created clean.

The product repo's own working tree/index/branch at `C:/Projects/Agent_Workspace/PIPD` was not
modified (it was already dirty from prior rounds, unrelated to this turn; untouched here). No
`origin` operation, no branch creation.

## 3. Step 2 — reproduce the R7 change on `main` (semantic patch)

### 3.1 Derive the true R7 delta, prove it equals the archived patch

The delta was derived from the R7 pair (`RAW/pre_change/<f>` → R7 post-change `<f>`) with a real
`git diff --no-index`, then normalized (drop `index`/`diff --git` headers, blank the `a/`,`b/`
prefixes) and compared. `verify_derived_equals_pair.py`:

```
sha norm(real pair diff) : 937b44a721c43700a70527e9311ccdcb
sha norm(WSB derived)    : 937b44a721c43700a70527e9311ccdcb
sha norm(R7 archived)    : 937b44a721c43700a70527e9311ccdcb
derived == real pair diff: True        (exit 0)
```

So `WS_B/R8_0_DERIVED_FROM_R7.patch` is byte-for-byte (normalized) the archived
`R7_VALIDATOR_DIFF.patch`, and it is exactly `+203/−6`:

```
hunks: 7    added=203    removed=6
```

(Note: the archived `R7_VALIDATOR_DIFF.patch` is CRLF-encoded and will not `git apply` to
LF sources; the derived patch is LF and applies cleanly. This is a transport/encoding artifact,
not a semantic difference — proven by the normalized-equality above.)

### 3.2 Apply to `main` and resolve conflicts

`git apply -3` of the derived delta on the `main` tree: `pipeline.py` applied clean; `cli.py`
(~line 163) and `validate.py` conflicted. Both conflicts were resolved **by preserving `main`'s
surrounding code and re-expressing only the hardening intent** — no guessing, no semantic drift:

- **`cli.py` (~168).** `main` resolves schemas via `registry.resolve_for_validate(root)` →
  `schemas_dir`; R7 used the literal `root / "schemas"`. Resolution: kept `main`'s registry block
  and threaded the derived frozen context as the 3rd arg —
  `validate.validate_bundle(bundle, schemas_dir, frozen)`.
- **`validate.py` (~closure/tail).** `main` had added `trace_edges` / `closure_findings` and a
  `"closure"` key in the return dict; R7 added the `frozen_context` parameter and
  `derive_frozen_context`. Resolution: kept **both**.
  (The brief predicted a `CLAIM_LADDER` conflict at `validate.py:14`; that hunk actually applied
  cleanly. The real conflicts were in the closure/tail region described here — recorded as a
  divergence from the brief's prediction.)

No hunk required guessing, so no blocker was raised on step 2.

### 3.3 Verification that the rebased patch reproduces the worktree, applies on fresh `main`

`verify_rebased.py`:

```
worktree live diff == rebased patch: True      (normalized sha da374a7fe6fe09b1…)
apply --check on fresh main exit: 0
apply exit: 0
validate.py: applied=f8ea6c6be15db358 post=f8ea6c6be15db358 match=True
pipeline.py: applied=9e9f6ab02e385a7b post=9e9f6ab02e385a7b match=True
cli.py:      applied=6ee1cca26e4f5b15 post=6ee1cca26e4f5b15 match=True
```

### 3.4 Changed hunks vs `main` (hardening-only)

`git diff -U0` vs `main` — every changed hunk is the hardening's own; nothing else differs:

| file | hunks (new-file line ranges) | +/- |
|---|---|---|
| `cli.py` | `@@ -171 +171,7 @@` | +7 / −1 |
| `pipeline.py` | `@@ -206,0 +207,39 @@` | +39 |
| `validate.py` | `@@ -16,0 +17,11 @@`, `@@ -117,2 +128,12 @@`, `@@ -119,0 +141 @@`, `@@ -137 +159,5 @@`, `@@ -192,0 +219,88 @@`, `@@ -269 +383,2 @@`, `@@ -284 +399 @@`, `@@ -294,0 +410,37 @@` | +157 / −5 |

`git diff --stat` totals: `cli.py` 1 changed file, 7 insertions, 1 deletion; `pipeline.py` 39
insertions; `validate.py` 157 insertions, 5 deletions. Grand total `+203 / −6`.

Artifacts: `WS_B/R8_0_REBASED.patch` (sha256 `ba57bad8f395c4ef9ed42a4e6f9b9a77b4decc05e528f6bb5d43b5eefe23f96b`),
`WS_B/R8_0_DERIVED_FROM_R7.patch`, and `WS_B/post/{validate.py,pipeline.py,cli.py}`
(sha256 `f8ea6c6be15db358…` / `9e9f6ab02e385a7b…` / `6ee1cca26e4f5b15…`; all compile).

## 4. Step 3 — repository test suite inside the worktree

Command: `Set-Location $wt; & $py -m pytest tests -q`

Exact summary line:
```
2 failed, 609 passed, 20 skipped, 62 subtests passed in 262.18s (0:04:22)
```
Raw: `RAW/r8_pytest_full.stdout.txt`.

Failure list:
```
FAILED tests/test_s4ext_trace_closure.py::LegalTraceStillPassesTests::test_real_trace_link_is_legal_beside_its_endpoints
FAILED tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs
```

### 4.1 Comparison against the R7 run

R7 baseline: `7 failed, 319 passed, 2 skipped, 34 subtests passed` (376.00s). The numbers differ
because **`main` is a much newer/larger tree** than the `9bd33a1` base R7 ran against (609 vs 319
passing; the R7 failures were mostly environment `copytree` errors on a locked venv, absent here).
The counts are **not** expected to match and no test was adjusted to force a match.

### 4.2 Both failures are introduced by the ported hardening (not pre-existing on `main`)

Both tests were shown to **pass on clean `main`** by stashing the change in the worktree:
`2 passed in 23.07s` (raw: `RAW/r8_pytest_main_baseline_twofail.stdout.txt`). So they are
`main`-divergence findings exposed by the port, not regressions inherited from `main`.

**(a) `test_real_trace_link_is_legal_beside_its_endpoints`.** A legal `TraceLink` bundled with its
PI now fails closed:
```
TraceLink: UNBOUND_FROZEN_CONTEXT: from_hash cannot be verified against a frozen
subject->digest map (frozen context not supplied); binding is unproven, not a pass
```
The call in that test uses the 2-arg `validate.validate_bundle(bundle, SCHEMAS_DIR)` with no frozen
context. This test file **does not exist on `9bd33a1`** (verified absent from the `r5q-release-wt`
tree) — `main` added it. It exercises the "no frozen context supplied" branch, which the R7 design
deliberately makes fail closed. This is a genuine `main`-divergence: `main`'s newer suite encodes a
call pattern (2-arg validate of a bare legal TraceLink) that the R7 semantic intent rejects.

**(b) `test_cli_smoke_runs`.** `tools/cli_smoke.py` runs
`validate --bundle .hgk/artifacts/s1/bundle.json`, which now **crashes**:
```
AttributeError: 'str' object has no attribute 'get'
  validate.py:434 in derive_frozen_context
  oracle = ((atom.get("risk_guard") or {}).get("oracle") or {})
```
Root cause, reproduced directly (`repro_frozen_crash.py`): in `main`'s s1 bundle, each
`PI-PKG.stable_semantic_contract.atoms[i].risk_guard` is a **string**
(`'REQ-INTENT cannot self-accept'`), not a mapping, so `.get("oracle")` raises. `derive_frozen_context`
assumes a dict `risk_guard` and lacks an `isinstance` guard.

This defect is **faithful to the R7 target**, not introduced by the rebase: the R7 post-change file
carries the identical unguarded line (`R7_CHECKER_ATTEMPT3/.../validate.py:288`). It did not surface
in R7 because R7's older suite/base never fed a string `risk_guard` through this path. Decision:
**do not patch `derive_frozen_context`, do not alter the target semantics** — record the divergence
honestly. (Fixing it would be a behavior change beyond the R7 intent and is out of this turn's
scope.)

## 5. Step 4 — re-run all 18 mutations against the worktree tree

Runners copied to `WS_B/RUNNERS/` from
`R6_DELIVERY/RUNNERS/{probe_mutations.py,probe_lib.py,run_mutations.py}`. Only constants
redirected (no logic change):

- `probe_mutations.py`: `PIPD_SRC` → `…/worktrees/r8-wt/src`; `SCHEMAS` → `…/worktrees/r8-wt/schemas`; `RAW` → `WS_B/RAW`.
- `probe_lib.py`: `RAW` → `WS_B/RAW`.
- `run_mutations.py`: `ROOT` → `WS_B`.

Proof: `WS_B/R8_0_DRIVER_DIFF.patch` (sha256
`9886a564d7d359e200195694f1fae5139e739df2b513aac4ce58cb5733704f90`) — shows only these constant
lines changed. `pipd_scratch_source.md` copied into `WS_B/RAW/`.

Run: `run_mutations.py` → exit 0; 10/10 constructible cases observed `REJECT`
(`RAW/r8_run_mutations.stdout.txt`). Constructible observed=REJECT for M01, M03, M04, M05, M06,
M11, M12, M14, M16, M18.

Required outcomes:

- `M04` = **REJECT** (`ProfileBinding: content_hash does not match the record body …`).
- `M06` = **REJECT** (`RequirementAtom: content_hash does not match the record body …`).
- `M16` = **REJECT** (`TraceLink: content_hash does not match the record body …`).
- All 7 previously-detected ids stay detected (in fact all 10 R7-detected ids remain detected):
  M01, M03, M04, M05, M06, M11, M12, M14, M16, M18.
- 0 not-detected.

### 5.1 Row-level difference vs R7

Only one: **`M05` first_fail** changed from R7's
`PI-PKG/: Additional properties are not allowed ('_profile_meta' was unexpected)` to
`PI-PKG: content_hash does not match the record body (body edited without re-issuing identity)`.
Reason: `main` strips the `_profile_meta` non-record sidecar before the schema check
(`NON_RECORD_SIDECARS`), so the schema-level `additionalProperties` rejection no longer fires
first; the self-digest check catches the poisoned oracle instead. Still REJECT either way.

### 5.2 The 8 `NOT_RUN` ids, re-judged (not silently dropped)

M02, M07, M08, M09, M10, M13, M15, M17 — same set as R7/baseline. Each re-judged
`NOT_CONSTRUCTIBLE_FROZEN_BYTES_ABSENT`, with the specific reason recorded per row in the JSON
(frozen R5 corpus / legacy-T fixture / 64-bridge registry / PI-01 vendor title / WP-01 owner
artifact / technology-admission ledger / trace-crosswalk / registry-projection bytes not reachable
on the host without mutating frozen source; checked under the worktree, the R6 delivery, and
HG-KSEOS — no matching bytes).

## 6. Step 5 — outputs

- `WS_B/R8_MUTATIONS_18_ON_MAIN.json` — row shape `id / mutation / expected / observed /
  validator_verdict / first_fail / raw_receipt` (+ `raw_receipt_sha256`, `rejudgement`,
  `not_run_reason` where applicable) plus `base_commit` = `dba4b19…`, `product_tree` =
  `…/worktrees/r8-wt`, `driver_diff_sha256` = `9886a564…`. Totals: executed 10, detected 10,
  not_detected 0, not_run 8, total 18. `claim_level` = LOCAL / candidate-only.
- `WS_B/WS_B_RECEIPT.md` — this file.

## 7. Step 6 — cleanup

`r8-wt` is **left in place** (the orchestrator re-measures from it). No worktree not created by
this turn was touched. WS_B-local scratch dirs (`tmp_rebase`, `_verify_apply`, `_verify_rebased`)
created during the rebase/verification were removed (scoped, refused-on-outside-WS_B — see
`_cleanup_scratch.py`). Evidence scripts retained: `verify_norm.py`,
`verify_derived_equals_pair.py`, `verify_r7_apply.py`, `verify_rebased.py`,
`repro_frozen_crash.py`, `make_mutations_json.py`, `_cleanup_scratch.py`.

## 8. Evidence index (raw, unedited)

| artifact | sha256 / note |
|---|---|
| `R8_0_DERIVED_FROM_R7.patch` | normalized-equal to `R7/R7_VALIDATOR_DIFF.patch` |
| `R8_0_REBASED.patch` | `ba57bad8f395c4ef…`; +203/−6; applies clean on fresh `main` |
| `R8_0_DRIVER_DIFF.patch` | `9886a564d7d359e2…`; constants-only redirect |
| `post/{validate,pipeline,cli}.py` | `f8ea6c6b…` / `9e9f6ab0…` / `6ee1cca2…` |
| `RAW/r8_pytest_full.stdout.txt` | `2 failed, 609 passed, 20 skipped, 62 subtests passed` |
| `RAW/r8_pytest_main_baseline_twofail.stdout.txt` | `2 passed in 23.07s` (clean `main`) |
| `RAW/r8_run_mutations.stdout.txt` | 10 cases, exit=0 |
| `RAW/mut_mXX.stdout.txt` (+ `.json`, `.stderr.txt`) | per-mutation raw receipts |
| `R8_MUTATIONS_18_ON_MAIN.json` | 18 rows, 10 detected / 8 not_run |

## 9. Non-claims

LOCAL / candidate-only. No acceptance pass, no Gate PASS, no production readiness, no verdict
upgrade. The 221 acceptance cases were not run. No remote/network write. The `M04`/`M06`/`M16`
refusal is now measured on `main` (`dba4b19`)-derived bytes rather than only on the `9bd33a1`
tree, which is the property this turn set out to move; it remains a local measurement.
