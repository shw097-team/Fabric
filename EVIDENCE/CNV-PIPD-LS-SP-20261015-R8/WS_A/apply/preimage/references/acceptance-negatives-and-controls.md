# Acceptance negatives: a refusal is only evidence when a control completes

A negative acceptance item ("X cannot complete", "a foreign receipt is refused", "the guard blocks
this") asserts a REFUSAL. A refusal is cheap: almost any broken fixture produces one. These rules make
the negative actually test the claim it names.

1. **Pair every refusal assertion with a control that COMPLETES when only the defect under test is
   removed.** Same fixture, same lane, one field changed. If the control also refuses, the negative is
   confounded and proves nothing about its claim — report that as a FAIL of the ITEM, not of the
   product.
2. **Keep the control as a permanent test in the same suite.** A control run by hand once cannot stop
   the negative from silently re-confounding later. Measured shape: a "foreign surface cannot complete"
   case asserted a refusal, but the lane fixture emitted a nonce that could NEVER match the one the
   dispatcher expected, so the turn was refused for the nonce, not for the surface; the control
   (mandated surface, same fixture) refused too — which is what exposed it. Before the control existed,
   the suite was green and the item was worthless.
3. **Assert the SPECIFIC code/reason the claim implies, and print the observed one on failure.** A bare
   "must refuse" passes for any reason, including the wrong one. Accept a set of codes only with a
   comment naming why each is admissible, and update that comment — never loosen the assertion to make a
   run green.
4. **Read the fixture's control inputs, not the test's intent.** Ask which field the harness actually
   matches on, and whether the fixture sets it to a value that can match at all. A fixture whose
   satisfied-field is hard-coded to a sentinel that can never equal the requested value turns every
   "refusal" case into a test of the sentinel mismatch.
5. **A runner flag is not a child argument.** An expectation the runner takes (a nonce, a token, a run
   id) is usually the RUNNER's own flag and is never forwarded to the child process — so a fixture that
   tries to "echo argv" to satisfy it silently falls back to its default. Drive the fixture through an
   ENVIRONMENT VARIABLE carrying the exact expected value, and make it an opt-in so fixtures that DEPEND
   on the mismatch keep working.
6. **Read the per-attempt result fields that name the expectation.** Fields such as `nonce_present:
   false` sitting next to a satisfied `usage_receipt_ok: true` localise the cause in one line. Check them
   before forming a hypothesis about which layer refused.
7. **Verify a claimed repair of a finding by re-running the INDEPENDENT check on the new revision.** A
   finding you fixed yourself is not closed by your own green suite; the gate the finding came from must
   be re-armed against the re-frozen revision. Report both revision digests so the reviewer can see the
   checker was pointed at new bytes and not the ones it already rejected.
8. **A re-freeze after a repair must cover EVERY changed file, fixtures included.** Re-derive the
   changed set from the frozen copy and diff it against the tracked list; a helper or fixture you also
   edited is a silent omission that makes the digest attest to less than the reviewer believes. Extend
   the apply/landing manifest with those same files too, so the rollback covers what the apply touches.
