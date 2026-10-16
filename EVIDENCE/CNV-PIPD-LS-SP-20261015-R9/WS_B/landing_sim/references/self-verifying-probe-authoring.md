# Authoring gate probes that survive independent verification

You are the MAKER of a governed gate and must emit probe/receipt evidence that an
independent VERIFY_ONLY or adversarial lane will re-run and actively try to falsify.
A probe that cannot fail is a declaration, not a test — and an adversarial lane finds it.
These rules were learned by having an independent lane catch vacuous probes across
three consecutive verification rounds on one round.

## When to use
- You are writing the positive/negative probe set behind a gate receipt (knowledge
  admission, denominator proof, locator round-trip, conflict handling, regression).
- A receipt currently reports an aggregate PASS and you need to know whether the
  aggregate is actually supported by executed work.

## Core rules

1. **Every probe must be able to fail.** A hardcoded expected outcome (`"pass": true`, a
   literal `"resolver_output": "QUARANTINE"`) is a defect, not a shortcut. Invoke the real
   code path and let it produce the outcome.
   - Locate the real surface by grepping `src/` for the behaviour — a precedence/conflict
     resolver usually already lives in the project's assurance or control-validation module.
     Import and call it. Record the surface's dotted path **and its file SHA-256** so the
     claim is traceable to bytes.
   - Always ship a **control case the same mechanism accepts** alongside the case it must
     reject. A control that passes proves the harness can distinguish reject-from-crash;
     without it, a "REJECTED" outcome is indistinguishable from a typo or an exception.
2. **An aggregate PASS must never be satisfiable by not-applicable results.** If a probe
   reports N/A for a subject (zero denominator, no tokens, no applicable rows), that N/A must
   not feed the summary. Compute the summary over subjects that could actually be tested, and
   publish `executed` vs `expected-nonzero` counts so coverage is visible. State the rule in
   the field itself: *a NOT_APPLICABLE result never contributes to PASS*.
3. **Assert the lookup HIT, never a default fall-through.** `register.get(key, 0) == 0`
   cannot distinguish "the register says zero" from "my key was wrong". Key-format mismatches
   are silent and total — a register keyed `PD00` looked up as `PD-PKG-00` made an entire probe
   family short-circuit to N/A while the receipt still read PASS. Build both key forms (or
   normalise), then assert the resolved value is not the default.
4. **Match the whole token, with a boundary.** A substring test on a short suffix
   (`01`, `000`, `A`) has no discriminating power — short suffixes occur on thousands of
   unrelated lines. Use a boundary that excludes alphanumerics but permits the delimiter the
   source form actually uses.
5. **Drive the token set from the authoritative register, not a hand-written regex.** A regex
   narrower than the source's real identifier vocabulary reports a gate failure that does not
   exist. When a probe finds zero of N declared items, suspect the extractor before the corpus:
   check whether the register normalises/prefix-strips family tokens (`D03-WF-01` → `WF-01`),
   then re-anchor the assertion on the register's own recorded locator.
6. **Never let a broken instrument be reported as a failing subject.** An extractor bug that
   cannot find a declared token is a measurement defect, not a source orphan. Say which one it
   is; and if you fix the instrument after having claimed a PASS, record that the earlier claim
   was unsupported rather than quietly re-running.

## Reporting discipline

- **While a fix is unverified, the stated result is `PARTIAL` (pending), not PASS.** Replace the
  verdict line only when the re-verification returns. Never leave a "final verdict recorded"
  line and a `PENDING` block in the same document — an adversarial lane flags that pair as a
  contradiction.
- **Keep the run-level verdict in exactly ONE place** (a final-verdict artifact plus the
  dossier's first section). Any other artifact asserting a final verdict is a contradiction.
- **Record each verification round verbatim** in its own artifact: lane role, verdict, blocking
  findings, dissent, remediation. The producer must never restate its checkers' verdicts in
  softer words, and must not adopt a lane summary without confirming it addresses the goal.
- **Scope re-verification deliberately.** One full re-verify round for the whole artifact set,
  plus focused rounds that name the specific fixes and ask two questions: is the fix real, and
  did anything regress. Have the checker independently re-run the surface you claim to invoke.
- **Write a corrective-action record** when independent review finds defects: defect, finding,
  root cause, fix, re-run proof, status. Mark a fix that a later round superseded as
  `SUPERSEDED_BY_<newer>` — do not leave superseded wording reading as current.
- **Disclose residual weaknesses** in the same artifact as the verdict (reproducible
  serialization quirks, normalisation assumptions, zero-denominator subjects, open bounded
  blockers). A PASS with disclosed residuals survives review; a PASS that hides them does not.

## Artifacts that cannot contain their own hash

A pack that lists artifact SHA-256 values cannot include its own digest, and neither can the
umbrella document that cites the pack. Emit a separate **end-of-round READBACK artifact** that
hashes the final bytes of every returned artifact *including the pack and the umbrella
document*, with a `mismatches` list and an `all_verified` boolean. Flag the self-identity rows
so a reader knows why those two hashes were not pre-recorded. The order is complete only when
this readback is clean.

## Invalidation cascade

When a shared input changes (the compiled contract, a freeze digest, a HEAD), **every
downstream artifact hash is invalidated**. Re-run the whole tail — contract → per-stage
receipts → pack → umbrella document → readback — rather than patching one file. Publish the
new subject hash in the corrective record so a reader knows which generation the evidence
belongs to.

## Consistency validators and the rule they state

A validator that checks a manifest/evidence tree is a checker you authored, so it is
judged exactly like a probe — and it is the single richest source of returning findings.

1. **Prove the FAILURE path fires, by injection, for EVERY shape you claim.** An error
   list that is initialised and never appended to makes `assert not errors` always true:
   the validator is vacuous while its receipt claims it "fails on a contradiction". Read
   the error path, not just the pass path. Then inject each shape you assert you catch and
   require all of them to be caught, asserting non-vacuity inside the run so a regression
   aborts the build. Shapes worth covering: wrong value for a named target; the same kind
   of value under a differently-named key; a `commit:path` reference carrying a different
   blob's hash; a named target that resolves to nothing; a case-variant digest; a value
   that is a bare array element.
2. **Pair each declared hash with ITS OWN reference, not the first one you find.** An
   object carrying several references (a contract ref AND a compiled-prompt ref) will have
   every hash compared against whichever reference the walker reaches first, so one hash is
   silently checked against the wrong blob — your own validator then reports a false error
   against a correct artifact. Derive the target from the hash key's own stem (`X_sha256`
   -> `X_ref` / `X_path` / `X_file` / `X_artifact`), and give that name-affine tier
   PRECEDENCE over any generic path-key list. Enumerate the authoritative key list in one
   place (a tuple the code reads) rather than restating it in prose that drifts.
3. **Scope is every declared value — including bare list elements.** A walker that yields
   only dicts never inspects a hash that sits as an element of an array, so "every 64-hex
   value is checked" is false. Traverse both, and ship an injection fixture that IS a bare
   list element.
4. **Never claim the description is an EXACT description of the implementation.** That
   sentence is falsifiable and will be falsified: any wording broader than the code (a key
   order you restated wrongly, "the first present" where the code collects all present,
   "always an error" where the code errors only when nothing else resolved) is itself the
   finding. State the rule as a BEHAVIOURAL DESCRIPTION, say explicitly that the code is
   authoritative, and enumerate what it does NOT cover in `known_limitations` — including
   any constructible counterexample a reviewer already found. Do not restate an ordering
   you can avoid restating: point at the constant the code reads.
5. **Exempt scopes must be counted, never silently skipped.** When a `superseded/` (or
   similar) region is deliberately exempt, collect its failures into a counted, published
   list rather than dropping them — an exemption that hides its own contents is a loophole.
   Keep the allowlist minimal and individually justified, and state plainly which
   contradictions it could still absorb.
6. **A number that lives only in your message is not evidence.** Put counts (items,
   hashes checked, stale references, shapes caught) IN the artifact, produced by the
   generator. A figure quoted in prose that no artifact records is unverifiable and reads
   as wrong when the real number differs.
7. **Prefer cutting the claim over adding capability.** When a reviewer finds the stated
   rule ahead of the code, the cheaper correct fix is usually to shrink the claim (describe
   behaviour, declare limits) than to grow the validator — growing it introduces new
   wording that can outrun the code again. Fix the real hole only where the gap is
   substantive rather than documentary, and one revision at a time.

## Pre-handoff self-audit

Before giving gate evidence to any checker, answer all of these:
- Can each probe fail? Is any expected value hardcoded?
- Does every positive probe have a control case the mechanism accepts?
- Does the aggregate PASS count only executed subjects, with N/A excluded by construction?
- Does every register/lookup assert a hit rather than a defaulted miss?
- Are tokens matched whole, with a boundary, from the register's own vocabulary?
- Is the current stated result consistent with what is actually verified right now?
- Does every validator I ship have an injection proof that its failure path fires?
- Is each declared hash paired with its own reference, not a neighbouring one?
- Does any prose I wrote claim to describe the implementation exactly, and is it true?
- Is every count I quote actually recorded in an artifact?
