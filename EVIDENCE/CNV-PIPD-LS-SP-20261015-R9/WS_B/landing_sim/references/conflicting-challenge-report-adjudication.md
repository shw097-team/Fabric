# Adjudicating conflicting challenge reports, and closing the closure layer

Loaded from SKILL.md rule (z). Use when TWO independent challenge reports disagree about the same
subject, when a repair order requires a probe gate before mutation, or when a fresh checker returns
PARTIAL on a reducer/claim layer that looked finished.

---

## 1. The conflict gate: probe the exact bytes, before any mutation

Two reports on one frozen subject can disagree about whether a product defect exists. Neither the newer
report, the more authoritative-sounding one, nor the one that agrees with your own reading is the
tie-break. The tie-break is a **source-bound deterministic probe against the frozen bytes**, run BEFORE
the first product mutation (this is usually the repair order's own first step).

Shape of the probe harness:

- one probe per claimed defect, recording: the exact call, the observed outcome, and the expectation
  derived from the CANONICAL SOURCE (quote the source locator — package + section + the invariant id),
  plus an explicit verdict token (`REPRODUCED_FAIL_OPEN` / `NOT_REPRODUCED` / `CONTROL_OK`);
- a POSITIVE CONTROL per axis, or "everything is broken" is indistinguishable from "the probe is broken";
- a dimension that the seam cannot even EXPRESS (no token structure, no nonce, no generation input)
  is recorded as `NOT_EXPRESSIBLE_IN_CURRENT_SEAM` with the reason — that is evidence too, and it is
  often the strongest statement of the gap;
- write the raw result to a JSON artifact; summary prose is index only.

Verdict mapping: any `REPRODUCED_*` on an axis => `PRODUCT_DEFECT_CONFIRMED:<finding id>` => Branch B
(product repair required). All axes clean => Branch A (preserve the source bytes exactly; governance and
evidence layers only; NO dummy commit to manufacture a new SHA).

### 1.1 The probe PAIR (before/after) is the evidence

Author the defect probes as a pair sharing the same oracle: the probe set that reproduced the defect is
re-run against the repaired source and must now refuse every case it previously allowed, with the same
positive controls still passing. That inversion is what converts "the defect no longer reproduces" from a
claim into evidence. Report it as a rerun of the IDENTICAL harness, not as two different test sets.

On a new probe failure, classify WRONG PROBE vs real DEFECT explicitly before touching code (SKILL.md
rule (u) Corollary 2). A probe whose input contract was misunderstood is not a product defect.

---

## 2. Proving a missing typed-API capability (CREATION != RESOLUTION)

Before promising to materialise required state "through the typed API only", prove the capability
EXISTS at the level of the statement:

```
scan every source file for:
  UPDATE <table> SET <the field>              <- a resolver
  INSERT ... ON CONFLICT DO UPDATE ... field  <- a resolver
  INSERT INTO <table> (... field ...)         <- CREATION ONLY, not a resolver
  SELECT ... FROM <table>                     <- reader
```

Classify CREATION separately from RESOLUTION. A scan that counts any statement NAMING the table reports
the capability PRESENT for a store that has no resolver at all (observed: the `INSERT` that creates the
row with its initial verdict was counted as a resolver). Only a statement that can move the field OFF its
initial value counts.

Corroborate from DATA as well: read the store and show every row still at its initial value, and identify
the reader that treats the initial value as an OPEN edge (e.g. a denominator that counts
`verdict != 'PASS'`). Two independent proofs — source surface and live rows — is the honest form.

When the control plane genuinely cannot materialise the state:

- terminal is `TEMP_CLOSED_STATE`;
- raise a SEPARATE engineering-base ChangeSet (proposed API signature, why it is core and not
  task-specific, the acceptance tests) — never a direct SQL write, and never a patch to shared core
  smuggled in under a project/repair order;
- flag it HITL: mutating shared core is an explicit human authority edge;
- deliver every INDEPENDENT leg anyway (product repair, reducer fix, fresh checker, evidence,
  publication) and REDUCE the claim; do not force a closure the typed API cannot make;
- word the non-claim narrowly: if some typed calls DO work (a checkpoint can be bound, a work-order
  result can be recorded) and only one field is unclosable, say which — an over-broad "closure is
  impossible" is itself an inaccuracy a checker will report.

---

## 3. The closure layer: reducer and claim string

Extract the aggregate gate as a PURE function over the checker receipt, and derive the claim from it.

Required truth function:

```
wave verdict == PASS  AND  governance verdict == PASS
  AND checker != maker  AND checker read-only  AND checker subject == candidate under closure
```

Mandatory fixtures (evaluate through the SHIPPED function, never a copy):

| fixture | expected |
|---|---|
| product PASS + checker PARTIAL | FAIL |
| product PASS + governance PARTIAL + checker != maker | FAIL |
| product PASS + governance PASS + checker PASS + checker == maker | FAIL |
| product PASS + governance PASS + checker PASS + checker != maker | PASS |
| all PASS but wave_verdict ABSENT | FAIL |
| all PASS but wave_verdict empty string | FAIL |
| all PASS but checker not read-only | FAIL |
| all PASS but subject != candidate | FAIL |
| the historical receipt shape (product PASS, governance on-substance) | FAIL |

Three traps that survived the first fix and were each caught by a fresh checker:

1. **No `.get(primary, fallback)` across semantic lanes.** A missing overall verdict must not inherit the
   product lane's verdict through a default argument.
2. **The disclaiming string must not contain the disclaimed literal.** A reduced claim of the form
   `<TOKEN>_NOT_CLAIMED_<verdict>` still matches a substring scanner for `<TOKEN>` and destroys the
   emitter's own absence assertion. Choose wording where the claimed token is unrepresentable.
3. **Exactly one emitter.** A hardcoded second copy of the claim in the packaging emitter survives a
   reducer fix untouched. Make the emitter READ the claim from the closure receipt (assert it exists),
   and grep the whole harness for remaining literals of the claimed token.

Assert claim/evidence consistency BOTH ways: the claimed token is present when the verdict is PASS, and
absent for every other verdict.

---

## 4. Delegated checks must receive the artifact they verify

A spec sentence of the form "X is verified / delegated / checked elsewhere" is only true if the interface
gives the delegate what it needs to perform that check.

- The delegate's signature must carry the bytes to RE-DERIVE the check (the canonical payload excluding
  the field under test, plus the field itself) and return a strict bool.
- Every other outcome — None, a truthy non-bool, a wrong arity, an exception, an absent delegate — fails
  closed as an integrity denial.
- Ship a deterministic `canonical_payload_bytes()` so a real verifier can recompute the bytes; state in
  the docstring that the library performs NO cryptography and that a registry which only checks key
  existence is a CONTRACT VIOLATION by the integrator.
- A shape-regex checked before delegation is not verification; never let it stand in a receipt as one.
- Same reading for any "trusted object" seam: RE-DERIVE the predicate from the primitive inputs
  (operation, tier, permission class) and refuse when the handed object UNDERSTATES them.
- An optional actor/approver argument defaulting to None creates a self-approval path; compare the
  approver against the request-bound actor inside the verifier, not only against the optional argument.

If you cannot point at the input that makes the check possible, the sentence is an over-claim.

---

## 5. Round shape

```
freeze subject -> probe gate on exact bytes (Branch A or B)
  -> Branch B: bounded repair spec -> tracked writer on a NEW commit (containment + focused tests)
  -> re-run the PAIR probes -> full denominator (never shrink; W1 baseline preserved)
  -> governance fixes in the SAME round (reducer, claim emitter, capability gap)
  -> fresh VERIFY_ONLY lanes on the NEW subject
  -> closure receipt via the CORRECTED reducer + derived claim
  -> evidence pack -> publication -> re-challenge
```

Label every prior verdict `SUPERSEDED` with the head it actually read. Keep a cumulative finding ledger
with an explicit disposition per id. Expect the first checker round to find defects in your OWN repair
(including the ones your spec introduced) — that is the loop working, not the loop failing.
