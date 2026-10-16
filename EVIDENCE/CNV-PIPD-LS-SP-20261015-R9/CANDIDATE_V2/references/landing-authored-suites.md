# Landing an authored test suite into another tree (and other landing lessons)

From round HGK-SOLUTION-APPLY-20261012 (Option-1 execution: apply a candidate change into the repo, then
land an authored solution suite). Each lesson is a rule you can apply before the lane runs, not a story.

## 1. Separating REPO_ROOT from SUBJECT is mandatory before moving a suite

An authored suite often uses one constant (e.g. `SOLUTION_ROOT`) for TWO jobs: locating the code under test
(`SCRIPTS`, `FIXTURES`) and naming the **subject tree** that tests hash wholesale (`tree_sha256_map(subject)`).
When you relocate the suite, the correct value for each job differs.

- Rule: give the suite `REPO_ROOT` (where the repo is) and a bounded `SUBJECT` (the deliverable itself) as
  SEPARATE constants, and make `SUBJECT` an explicit file set or a copied deliverable — never a directory that
  contains the live agent home, runtime state, or anything another process writes.
- Why: with `SUBJECT` = repo root, a whole-tree walk (a) is slow, (b) races any concurrent writer, and (c) on
  Windows fails outright on paths past the legacy 260-char limit (`LongPathsEnabled=0`). Result: the suite goes
  red for reasons that have nothing to do with the code under test, and the failure looks like a real defect.
- Symptom to recognize: a test failing with `FileNotFoundError` on a path under `execute/homes/<lane>/.tmp/...`
  or a `>260`-char path, in a test whose name mentions "subject".

## 2. A package-configured `tests/` breaks suites that import their own `conftest`

If the target tree's `tests/` contains `__init__.py` (making it a package), pytest puts the PARENT on
`sys.path`, so a test module's `from conftest import ...` cannot resolve and the whole module fails to collect
(`ModuleNotFoundError: No module named 'conftest'`). Authored suites typically work only where `conftest.py`
sits beside the tests.

- Rule: land a self-contained suite into its OWN non-package directory (e.g. `tests/<suite>/`) so pytest again
  inserts that directory on `sys.path`. Verify by running the suite from the repo root AND from its own dir.
- Confirm the cause before fixing: copy the suite without `__init__.py` -> green; with it -> collection errors.

## 3. Deliverable-scoped files become tree-scope side effects when landed at the root

`pytest.ini` (`addopts`), `sitecustomize.py` (import-time hooks), and a root `conftest.py` all apply to EVERY
run in the tree once placed at the root, not to the deliverable.

- Rule: keep them inside the suite directory and remove any root-level copy you created. Files authored for a
  deliverable are not tree configuration.
- Disclose what the blast radius was, and measure it (re-run the round's own gates) rather than asserting it.

## 4. An import-time bytecode guard does not cover the outer test process

`sys.dont_write_bytecode = True` inside `conftest.py` runs too late for `conftest.py` itself, and a
`sitecustomize.py` in the suite dir is only imported when the interpreter starts with that dir on `sys.path`
(and in practice may not be imported at all). So `__pycache__/*.pyc` lands INSIDE the deliverable.

- Rule: if "writes nothing inside the tree" is a claimed invariant, carry it in the INVOCATION
  (`PYTHONDONTWRITEBYTECODE=1` / `python -B`) and add a test that asserts no `.pyc` appears. Grep the suite: if
  `pycache`/`pyc` appear only in docstrings, the invariant is unasserted.

## 5. A number copied from another party's log is not a measurement

Labelling a receipt row "not re-run by me, taken from the lane's log" does NOT make it true; an independent
checker will falsify it, correctly.

- Rule: every number in a receipt is either measured first-hand or marked as an unverified quotation — and
  keeping it out of the receipt's measured section. Prefer fewer invocations, each measured.

## 6. Repair briefs are where the author's error shows up

When a repair turns out wrong, check whether the BRIEF specified the wrong thing before blaming the lane. In
this round the brief said "make the repo root explicit (`parents[2]`)" — right for `SCRIPTS`, wrong for the
subject anchor, and the lane followed it faithfully.

- Rule: attribute the defect honestly in the findings ("the PLAN plane's own brief"), because the next author
  will otherwise repeat it.
- Rule: bound a repair lane's stop condition explicitly. A lane that cannot be steered mid-run (one-shot
  `codex exec`) must be given a mandated stop ("if X cannot be done faithfully, STOP and report"), or it will
  keep probing. If it exceeds the monitoring threshold, kill it and take over the residual — then label the
  artifacts you author yourself.

## 7. Rollback artifacts go stale the moment a later leg edits a landed file

`rollback --check` comparing against an older receipt WILL fail after any subsequent edit. That failure is
correct behaviour and must be reported as an uncertified rollback, not suppressed by re-keying the tool before
a checker has seen it fail.

- Rule: re-key rollback to the newest receipt only after an independent run has recorded the stale failure.
