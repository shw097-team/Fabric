# Harness & Evidence Defects (self-inflicted failures that fabricate results)

Governed work is only as trustworthy as the harness that produces its receipts. Every defect below
was authored by the agent, not the product, and each either fabricated a failure or a PASS.

## 1. Probe / assertion defects (the probe is guilty until proven innocent)

- **Dual module identity.** A probe that imports the product under a different package path than the
  product's own tests creates two distinct classes; `isinstance` then fails and the probe reports a
  type-guard error for a perfectly valid object. Import the product the way its tests do, or lift
  symbols from the already-loaded test module's namespace. Diagnose with `type(obj)` and
  `obj.__class__.__module__` against the callee's expected class before touching product code.
- **Wrong precedence expectation.** Asserting a later stage's reason code while an earlier stage
  legitimately fires first (expecting signature-integrity when exact-binding rejects the field first).
  The refusal is correct; your expectation encoded the wrong order.
- **Wrong fixture tier.** Asserting a tier-specific rule against another tier's object; the guard
  correctly does not fire and the probe calls it a gap.
- **A fixture helper that re-signs / re-derives on override** cannot express "changed AFTER signing".
  Use `dataclasses.replace()` on an already-signed value so the original signature is kept.
- **`str.replace` removes ALL occurrences.** Deriving an id via `x.replace("PREFIX-", "")` mangles ids
  containing the prefix twice. Parse ids explicitly.

## 2. Process / command-wrapper defects

- **A helper that raises on non-zero exit inverts meaning for "answer by exit code" commands.**
  `git diff --cached --quiet` (also `grep -q`, `diff -q`) returns **1 when there IS a difference**.
  Through a `check=True` wrapper the normal case looks like a crash. Pass `check=False`; test
  `.returncode` yourself.
- **Non-idempotent commits.** A receipts script that commits unconditionally fails on re-run with
  "nothing to commit", so a retry cannot converge. Stage, then commit only if
  `git diff --cached --quiet` (check=False) reports staged content.
- **A stripped child environment breaks networking.** Handing a child `git`/`curl` an `env=` with only
  `PATH` yields `getaddrinfo() thread failed to start` on Windows. Use
  `dict(os.environ, GIT_TERMINAL_PROMPT="0")`.
- **A string-replace patch whose anchor does not exist silently no-ops**, so a new helper is never
  defined and the `NameError` surfaces far from the edit. List real anchors (`grep -n "^def "`) before
  patching; assert the symbol exists after.
- **Pipelines hide the real exit code** (`... | tail`). When a run "succeeds" but looks wrong, re-run
  without the pipe to see the true status and full output.

## 3. Evidence-record defects

- **Never record a figure you did not just measure with the command you quote beside it.** The failure
  mode is writing the *expected shape* (last run's totals) after the test count changed. Re-measure
  after anything that alters the test count; pair every figure with its command.
- **A record corrected twice is a recorder defect, not a code defect.** Stop hand-transcribing; derive
  every number from a command's own stdout.
- **State counting conventions:** "N rows" vs "N lines incl. header"; `--stat` vs `--numstat`;
  collected vs run. Give the convention with the number.
- **Store the diff as a byte artifact** with hash, size and the exact producing command. A hash not
  reproducible from a quoted command is not evidence.

## 4. New canonical-transition API: the reviewer's attack list

When the control plane lacks a typed primitive and you add one, expect exactly these attacks:

- **Mandatory subject binding.** An optional subject parameter means a guard that fires only when the
  caller opts in - that is not a guard.
- **Evidence: existence vs subject.** If the evidence registry has no subject key you can prove a ref is
  *registered*, never that it belongs to *this* subject. Say "registered-evidence binding", open a TT for
  the schema extension, and do not claim subject-bound rejection.
- **Idempotency namespace.** When the key column is globally UNIQUE across entity types, matching
  `entity_id` alone lets a foreign event be inherited as a replay. Match `(entity_type, entity_id)` and
  fail closed when the key was spent elsewhere instead of returning the foreign event.
- **Replay parity.** The replay path must enforce the SAME preconditions as the first write (lease,
  evidence existence, subject). A weaker replay path yields an approval-shaped result without the
  discipline of the write.
- **Return persisted values, not caller-supplied ones**, or an idempotent replay silently contradicts
  persisted state.
- **The atomicity test must fail AFTER the UPDATE** (inject a failure into the event-insert step), not
  by pre-seeding a key that short-circuits before the write - otherwise rollback is never exercised.
- **Lawful = minimal.** Add only the genuinely missing primitive, and record a fresh inventory of the
  existing APIs as evidence before claiming a gap.

## 5. Verifying a claim of registration

1. Resolve the canonical store path from CONFIGURATION, not assumption - a project-local database and
   the canonical registry are different targets and writing to the wrong one looks successful.
2. Write through the typed API.
3. Read the canonical store back and print what you actually see.
4. If you wrote to the wrong place first, keep those rows as an accurate historical fact and DISCLOSE
   them; never silently delete and re-do.
