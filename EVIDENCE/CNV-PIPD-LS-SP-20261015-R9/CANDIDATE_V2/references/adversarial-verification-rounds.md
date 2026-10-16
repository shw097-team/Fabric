> NOTE: SKILL.md for this skill is already at its 100,000-char cap, so no pointer to this file
> could be added there. When SKILL.md is next trimmed, move a stale section into references/ and
> add a pointer: "running independent verification rounds → references/adversarial-verification-rounds.md".

# Adversarial verification rounds over a governed deliverable

Pattern: the producer freezes an evidence package with digests → a **fresh-context** checker
recomputes and attacks it → the producer applies corrections → re-freeze → next round. The
checker must not be the maker, its FAIL verdicts stay verbatim in the package, and each round's
findings become errata that the next round adjudicates.

## Rules that cost rounds to learn

1. **Apply errata IN PLACE, not only in an errata section.** A checker judges the operational
   tables, the OpenSpec tasks and the acceptance tests. An errata annex that leaves the repair
   table or task list still saying the old thing is scored PARTIALLY_RESOLVED ("acknowledges the
   blockers but does not consistently update the operational repair table"). Edit the rows and the
   task list themselves; keep the errata annex as the audit trail of what changed and why.
2. **Never let a manifest list its own digest or a post-build file's digest.** A manifest written
   last from a directory walk carries the *previous* build's digest for itself; a checker counts
   the mismatches and calls them undeclared. Exclude self-referential and post-build files from
   `artifacts`, carry the document digest as its own field, and declare `post_build_writes` up
   front — including the next verification round's output file.
3. **WAL forensics: magic first, then frame alignment, then the checksum chain.** A valid header
   magic (big-endian `0x377f0682` / `0x377f0683`) does NOT make the file usable. `(size-32) mod
   (24+page_size)` not integral ⇒ truncated tail. Frame checksums chain, so the first bad frame
   ends verification and everything before it is a **salvageable committed prefix**. A categorical
   "not a WAL / no replay" claim is both wrong and exactly what an adversarial checker contradicts.
4. **Tier loss accounting: proven / candidate / unverified — never one total.** Only a row you can
   show existed and is now gone is *proven* (e.g. it appears in a rescue export). An id-sequence
   gap does not prove the row ever existed. An earlier estimate you cannot reproduce is
   *unverified*, not disproved. Stating a single total was rejected in turn as understated then
   overstated; only the tiered form survived.
5. **Live metrics need an as-of stamp and an observed range.** Counts in a running store drift by
   hundreds between observers; an un-stamped number reads as a contradiction. Write the timestamp
   and the range you actually saw.
6. **Classify repairs by what they touch, not by intent.** Restoring a database or a skills tree
   *into a live home* is a canonical change even when the content is "only additive": stage first,
   then gate, backup, readback. Labelling such an item additive is itself a finding.
7. **Claim ceilings must separate subject stores from the control plane.** "No canonical mutation"
   is false when the round legitimately wrote spine records, kanban cards, an OpenSpec change and —
   with a non-hermetic test suite — extra canonical events. Say: no mutation of the *subject*
   stores, plus the enumerated control-plane/audit writes and disclosed side effects.
8. **Model identity is declared, not attested.** A runtime footer is a self-report; nothing in the
   package proves which model produced an artifact. State identity as declared by the runtime.
9. **A fail-closed tool gate can block a checker's own output write** (matcher over the whole
   payload, paths included). Keep payloads short, avoid pasting guarded substrings, report the
   block — never bypass. An already-admitted run dir should be whitelisted, and an over-broad
   matcher is a defect needing its own negative test (a genuinely secret-bearing payload must
   still be refused).
10. **Re-issue the freeze after every correction round and re-run the mirror.** Emit a freeze
    receipt as the boundary and state plainly that any later edit invalidates the digests and
    requires a re-build.
11. **Self-check before the checker runs.** Grep the document for the strings your last correction
    was supposed to remove (old wording survives inside quotations — verify each hit is genuinely a
    quotation of superseded text, not a surviving claim) and for un-stamped live numbers. This
    catches most findings one round earlier.
12. **Count the rounds honestly in the close-out.** Report per-round verdicts and what each round
    changed; never present the final revision as if it had passed verification it did not receive.
