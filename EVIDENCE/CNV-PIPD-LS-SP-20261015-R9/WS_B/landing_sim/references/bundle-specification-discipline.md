# Bundle specification discipline for lane/checker audits

A checker that can only see what you hand it will return INCONCLUSIVE for every claim whose inputs you
left out, and that failure looks like the checker being weak when it is your packaging. The residue recurs
forever unless the rule lives in a guard, not in a lesson.

## Rules

1. **Carry inputs, not computed flags.** A block that says `invariant_holds: true` is an assertion; the same
   block carrying the two hashes, the parent record and the ancestry exit code is recomputable. If a claim
   needs a flag, ship what the flag was computed from.
2. **Name the recompute command for every claim, and carry it in the bundle.** No named command means the
   claim cannot be re-derived by the receiver; a named command the bundle does not carry is the same defect
   one step later. Make both refusals hard, e.g. `ERR_CLAIM_WITHOUT_RECOMPUTE`, `ERR_RECOMPUTE_NOT_CARRIED`,
   each with a negative self-test so the rule is demonstrated rather than asserted.
3. **A partition claim needs its denominator.** "42 affected / 14 untouched" is unverifiable without the
   total the scanner saw and the set that cited nothing. Assert the partition reconciles
   (affected + untouched == cited; cited + uncited + skipped == total).
4. **Scope-anchor every receipt to the heads in force when it was produced.** A receipt generated at a head
   a later commit superseded cannot support a current-state claim, and the round's own affected-only ledger
   will list it as affected - a contradiction the checker will find. Print the resolved head(s) inside the
   receipt, and recompute against the live tree.
5. **Check the assembly, not just the content.** A guard can only verify the blocks the spec declares, and
   the spec drifts with the surgery. Assemble bundles with a script that refuses to emit unless every block
   label appears exactly once, and leave real headroom under the dispatcher's argv ceiling (aim well under
   the limit; a few dozen characters of margin is a false green).
6. **Keep the earlier bundles and their residues.** A residue that has been fixed is not the same artefact
   as one that was never raised; the ledger of attempts is the evidence that the mechanism improved.

## Reporting

State the checker's residues as they stand, including the one that was never confirmed. A claim ceiling that
says "S2 was never CONFIRMED" is worth more than a rounded-up "all verified", and the residue should name
the exact block that would settle it.
