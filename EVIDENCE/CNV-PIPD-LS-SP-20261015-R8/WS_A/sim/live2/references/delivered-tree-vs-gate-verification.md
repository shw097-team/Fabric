# Verifying the DELIVERED tree, not the suite's opinion of it

A maker's evidence is a claim about a delivered artefact. The suite passing is a separate fact, and
the two can disagree in both directions. These are the measured failure modes from a repair round
where every gate was green on the day the delivered tree was already corrupted.

## 1. A green suite coexists with a corrupted deliverable

Measured: `python -m unittest discover -s tests -v` -> `Ran 138 tests ... OK`, reproducibly, while the
artefact actually on disk (`dist/web/`) had been overwritten with 28-127 byte stubs. The suite did not
notice because **its own tests build the artefact in a temp directory** (`tempfile.TemporaryDirectory`)
and compare there. The suite is therefore green about a tree it never touches.

The gate is what catches it - but only when pointed at the DELIVERED tree. So:

- Run the strict gate with no `--out` override so it reads the committed artefact, and read its
  denominator.
- Then LOOK AT THE TREE YOURSELF, independent of the tool: `ls` the exact expected filename set and
  print byte sizes. A marker stub is visible as absurd size (35-37 B) with a single key, e.g.
  `{"surface": "host:genie-adapter"}`.
- Treat "the tool says PASS" and "the bytes on disk are real" as two separate claims.

## 2. The product entry point and the gate can disagree

Measured: the new gate module (`projection.project_surfaces`) was correct and its strict check passed,
while the PRODUCT CLI path (`cli.py project`) still called the LEGACY function
(`workspace.project_surfaces`) which wrote hardcoded UI files plus marker stubs. The finding was
"closed" by every gate and still open for every user.

Check the consumer entry point, not only the module the gate imports: grep the CLI/branch that a user
actually invokes and follow its call one level down. A repair that lands only in the new module leaves
the old caller live.

## 3. A smoke test that runs against the real repo root mutates the deliverable

Measured: `tools/cli_smoke.py` invoked `project` with no `--out`, so the CLI defaulted to the real
`dist/web` and the smoke run overwrote the delivered artefact - while the suite stayed green (see 1).
The corruption timestamp matched the suite run, and the maker's own earlier check had been correct.

Rule: any test, smoke or self-check must write to a scratch root. Assert it in the round: grep the
tool for the command list and confirm every writing subcommand carries an explicit `--out`.

## 4. Assert code-delta = 0 after the independent verification

Verify a PAIR, and prove the pairing afterwards:

```sh
git status --porcelain            # group by top-level dir; ALL of it must be the evidence journal
git diff <verified_commit>..HEAD --name-only | grep -v '^<evidence-dir>/' | wc -l   # must print 0
```

Evidence receipts legitimately keep landing during and after a verification run (gate re-runs,
measurement receipts). What must not move is the source set. Print the assertion and its result; do not
assert it in prose. Record which commit the verdict actually read, and re-issue the seal on the
evidence-complete tree while stating that the delta is evidence-only.

## 5. A finding that is non-blocking: raise a TT, do not edit the verified artefact

A checker's verdict binds the bytes it read. Editing an artefact afterwards makes that verdict stale,
even when the edit is a pure improvement - so the choice is between two governed outcomes:

- **Repair** -> you owe a NARROW delta re-verification of exactly the changed set, not a re-read of the
  whole package.
- **Do not repair** -> record each finding as a tracked item (id, owner, exact remediation text,
  `closed_requires_fresh_verification: true`) against the artefact, and leave the verified bytes alone.

Choose the second when the findings are label/prose/ambiguity class and the substance was verified
correct. State the reason explicitly ("editing an artefact a checker has verified invalidates that
verification"), because a reader will otherwise read the untouched finding as an unfixed defect. Copy
the checker's own verdict file into the artefact journal so the TT rows cite a bounded artefact rather
than a scratch path.

## 6. A strengthened contract legitimately reddens the maker's own fixtures

When a lane intentionally tightens a rule, the round's OWN pilots and fixtures start failing for the
right reason. Two measured shapes:

- A pilot hand-asserted `currentness: FRESH` with no epoch; the strengthened binder refuses an
  unverifiable freshness claim. The fix is to make the pilot DERIVE the context from the host (so it
  exercises the real provider), never to relax the binder.
- A LITE pilot was fed a whole 17 KB spec as its clause source; the clause-bound compiler produced
  hundreds of atoms and the product legitimately escalated the profile away from LITE. The fix is a
  LITE-sized clause source, not a disabled escalation.

Classification that keeps this honest: fixture staleness (fix the fixture) versus a weakened gate (never
do it). If the "fix" would remove an assertion, a refusal, or a required field, you have crossed from
one to the other - stop and re-diagnose.

## 7. Check for deleted assertions before believing "nothing was weakened"

```sh
git diff <base>..<head> --numstat -- tests | awk '$2>0'          # per-file deletions
git diff <base>..<head> -- tests | grep -E '^-[^-]' | grep -iE 'assert|expect'
```

Measured result worth copying as a pattern: two test files changed (+136/-5, +93/-1) and the removed
lines were entirely docstring and comment text plus one fixture path swap - zero removed assertion
lines. That is the evidence that a repair was not bought by editing the test.

## 8. Re-running an acceptance case that was previously NOT_RUN — without manufacturing a false PASS

An acceptance ledger with `NOT_RUN` cases invites a quick re-run, and the quick re-run is exactly where a
false PASS is cheapest to produce. Every shape below was measured in one round that had to re-run two
mutated-artefact cases after the packaging prerequisite (pip) became available; two of the three initial
results were wrong, and the third was void.

**The invariant: the verdict means nothing until you have shown the corruption reached the run.** For an
installed-package case, assert all four, in this order:

1. the mutation package is written under a name the installer ACCEPTS (a mutated wheel named
   `<case>.whl` is refused on the FILENAME — `ERROR: <case>.whl is not a valid wheel filename` — so
   `install_exit` fails for a reason unrelated to the product and the case still looks "detected");
2. `install` exits 0 and the mutated path is confirmed present-or-absent INSIDE the installed tree
   (`site-packages/...`), not at the source path;
3. the run drives the API the mutation targets — grep the subject for it first. Measured: `doctor` calls
   only `workspace.doctor()`, and the CLI references `load_registry` / `load_schema` ZERO times, so a
   `doctor`-based probe can never see a missing schema; driving the loader directly is what produced
   `ValidationFail: 'schema file missing for <X>'` and `FileNotFoundError` from `site-packages`;
4. the failure text is the SUBJECT'S — a typed, named error — not the harness's own usage error. All
   three commands of one probe exited 2 on argparse misuse (a duplicated flag, a missing required
   argument) while the report read as three detections; that whole run was void and had to be withdrawn.

**Run two variants per case, and name which is which.** `record_untouched` (the mutated companion file
left as shipped — the install must be REFUSED) and `record_fixed` (the companion repaired so install
succeeds and the corruption surfaces at RUN time). One variant cannot separate "the guard held" from
"the mutation never landed"; the pair is what proves the guard reacts to the corruption rather than to
something else. Expect the two to fail at DIFFERENT stages (install refusal vs. a runtime `SyntaxError`
from the installed CLI) and report the stage with each verdict.

**A false PASS is evidence, not garbage.** Keep the superseded harness output on disk under a name that
says what it is (`*_v1_falsepass.json`), carry a `retractions` list inside the current verdict naming each
withdrawn claim and the measurement that killed it, and rebuild the evidence manifest so the re-run's
artefacts are in the delivered set. Withdrawing in the same reply as the contradicting evidence is the
only version of this that costs nothing.

**An unexercisable case is a permanent NOT_RUN, not a defect.** A symlink-escape case on a Windows host
whose account lacks the privilege (`WinError 1314`) cannot be closed by any code change: say the mechanism,
state it is an operating-system capability limit rather than a product defect, and exclude it from the
closure count instead of listing it as resolved.
