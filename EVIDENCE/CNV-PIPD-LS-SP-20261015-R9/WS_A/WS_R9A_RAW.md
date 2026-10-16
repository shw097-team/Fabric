# WS-R9-A RAW TRANSCRIPT

Nonce: R9A-WSRITER-NONCE-7f3c1d
Role: bounded writer (Codex CLI EXECUTE lane). Claim ceiling: LOCAL / candidate-only.
Worktree: C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt
Base commit: dba4b19456777d3b597fdf71480f6423dd974243
Interpreter: C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe (3.11.9)

## SS0 ANSWER (before touching anything)

Q: Does r8-wt still carry the R8-0 hardening (3 modified files) and do the two named tests still fail there?

A: YES. `git status --short` shows the three modified files
(`src/pipd_ls_sp/cli.py`, `src/pipd_ls_sp/pipeline.py`, `src/pipd_ls_sp/validate.py`) at base
`dba4b194...`, and the two named tests FAIL on the unedited worktree:

```
FF                                                                       [100%]
...
FAILED tests/test_s4ext_trace_closure.py::LegalTraceStillPassesTests::test_real_trace_link_is_legal_beside_its_endpoints
FAILED tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs
2 failed, 629 deselected in 20.09s
```

(Test 1 failed with `TraceLink: UNBOUND_FROZEN_CONTEXT`; test 2 failed with cli_smoke exit 2.)
Therefore I proceeded to edit.

## WRITE SET

Only `src/pipd_ls_sp/validate.py` edited, only the two regions named in the brief.
`Any` was already imported (line 9: `from typing import Any`) - verified before inserting.

## HUNKS AS APPLIED (line numbers AFTER the edit)

Hunk 1 - `validate_bundle()`, inserted AFTER the empty-bundle guard and BEFORE
`for contract, record in bundle.items():` — lines 392-416:

```python
392     # R9-0 (BLK-R8-WS2): when the caller supplies no frozen context, discharge the endpoint /
393     # oracle bindings against the bundle's OWN atoms instead of failing closed. Each atom's
394     # frozen digest is its own content_hash, which the record-level self-digest check already
395     # verifies, so this adds a resolvable binding without removing one: a caller-supplied
396     # context is never overridden, and a supplied context that lacks an endpoint still fails
397     # closed in semantic_invariants.
398     if frozen_context is None:
399         derived: dict[str, Any] = {}
400         for _c, _rec in bundle.items():
401             if not isinstance(_rec, dict):
402                 continue
403             for _atom in ((_rec.get("stable_semantic_contract") or {}).get("atoms") or []):
404                 if isinstance(_atom, dict) and _atom.get("subject_id") and _atom.get("content_hash"):
405                     derived.setdefault("trace_endpoint_hashes", {}).setdefault(
406                         str(_atom["subject_id"]), str(_atom["content_hash"]))
407                 _rg = _atom.get("risk_guard") if isinstance(_atom, dict) else None
408                 _oracle = _rg.get("oracle") if isinstance(_rg, dict) else None
409                 if isinstance(_atom, dict) and _atom.get("req_id") and isinstance(_oracle, dict) \
410                         and _oracle.get("expected") is not None:
411                     derived.setdefault("oracle_expected", {}).setdefault(
412                         str(_atom["req_id"]), _oracle["expected"])
413             if isinstance(_rec, dict) and _rec.get("subject_id") and _rec.get("content_hash"):
414                 derived.setdefault("trace_endpoint_hashes", {}).setdefault(
415                     str(_rec["subject_id"]), str(_rec["content_hash"]))
416         frozen_context = derived or None
```

Hunk 2 - `derive_frozen_context()`, replacing the old single line — now lines 459-463:

```python
459             # R9-0 (BLK-R8-WS2): `risk_guard` may be a free-text string in a submitted PI, so the
460             # mapping access is guarded: an unusable shape yields no oracle expectation rather than
461             # an AttributeError, and the fail-closed branch for that binding still fires.
462             rg = atom.get("risk_guard")
463             oracle = (rg.get("oracle") if isinstance(rg, dict) else {}) or {}
```

## SS4 COMMAND 1 - two named tests

```
$ python -m pytest tests -q -p no:cacheprovider -k "test_real_trace_link_is_legal_beside_its_endpoints or test_cli_smoke_runs"
..                                                                       [100%]
2 passed, 629 deselected in 18.49s
```
EXPECTED `2 passed` -> MATCH.

## SS4 COMMAND 2 - NEGATIVE CONTROL (M04 / M06 / M16 via the R8-0 runner)

Invocation shape reused verbatim from the R8-0 receipts (RAW/mut_m04.json `command`):
`PY <R8/WS_B/RUNNERS/probe_mutations.py> <mode>`, cwd `.../CNV-PIPD-LS-SP-20261015-R8/WS_B`.
The runner imports `r8-wt/src` (line: `PIPD_SRC = ".../r8-wt/src"`), so it exercises the edit.

```
$ python .../R8/WS_B/RUNNERS/probe_mutations.py m04
{
 "id": "M04",
 "mutation": "ProfileBinding assurance downgraded ASSURED->LITE",
 "expected": "REJECT",
 "observed": "REJECT",
 "validator_verdict": "FAIL",
 "first_fail": "ProfileBinding: content_hash does not match the record body (body edited without re-issuing identity)",
 "raw_receipt": "RAW/mut_m04.json"
}
EXIT=0

$ python .../R8/WS_B/RUNNERS/probe_mutations.py m06
{
 "id": "M06",
 "mutation": "domain oracle expected changed to 999",
 "expected": "REJECT",
 "observed": "REJECT",
 "validator_verdict": "FAIL",
 "first_fail": "RequirementAtom: content_hash does not match the record body (body edited without re-issuing identity)",
 "raw_receipt": "RAW/mut_m06.json"
}
EXIT=0

$ python .../R8/WS_B/RUNNERS/probe_mutations.py m16
{
 "id": "M16",
 "mutation": "trace atom digest mismatched",
 "expected": "REJECT",
 "observed": "REJECT",
 "validator_verdict": "FAIL",
 "first_fail": "TraceLink: content_hash does not match the record body (body edited without re-issuing identity)",
 "raw_receipt": "RAW/mut_m16.json"
}
EXIT=0
```
EXPECTED `observed=REJECT, validator_verdict=FAIL` for each -> MATCH (hole remains closed).
The probes only print to stdout; no JSON was written into the worktree.

## SS4 COMMAND 3 - full suite

```
$ python -m pytest tests -q -p no:cacheprovider
................................................................ [ 10%]
....s........................................................ [ 19%]
................................................................ [ 29%]
........................................................................ [ 41%]
............s....................s....................sssssss [ 50%]
ssssssssss.............................................................. [ 62%]
........................................................................ [ 73%]
.......................................................................................................................... [ 92%]
.............................................                            [100%]
611 passed, 20 skipped, 62 subtests passed in 190.94s (0:03:10)
PYTEST_EXIT=0
```
Verbatim: `611 passed, 20 skipped` (0 failed).

## SS4 COMMAND 4 - git diff --stat (read-only)

```
$ git -c core.pager=cat diff --stat
 src/pipd_ls_sp/cli.py      |   8 +-
 src/pipd_ls_sp/pipeline.py |  39 +++++++++
 src/pipd_ls_sp/validate.py | 191 +++++++++++++++++++++++++++++++++++++++++++--
 3 files changed, 232 insertions(+), 6 deletions(-)
```
`pipeline.py` (39) and `cli.py` (8) are unchanged by me (identical to the pre-edit R8-0 state);
`validate.py` grew from 162 to 191 insertions (+29), which is exactly my two hunks.
The R9-0 additions are present verbatim in the diff (verified with a targeted grep of the diff).

## WHAT I DID NOT RUN / DID NOT DO

- Did not run M01/M03/M05/M11/M12/M14/M18 (not required by the brief); the full MUTATIONS_18 set
  was not re-run.
- Did not run any git WRITE command (no add/commit/branch/checkout/stash/reset).
- Did not edit any file other than `src/pipd_ls_sp/validate.py`.
- Did not touch `_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/**` or `C:/Projects/wt-r8-cleanmain`.
- Did not read or print any credential file.
- Did not send anything to any outside host.
- Did not weaken any check to make a test pass (the negative control proves the hardening holds).

## BLOCKERS

None. All four acceptance commands completed; commands 1-4 match their expected results.
