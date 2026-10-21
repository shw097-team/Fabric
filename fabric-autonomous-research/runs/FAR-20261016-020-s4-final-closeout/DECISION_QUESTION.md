# FAR-20261016-020 — Decision Question (S4 FINAL closeout)

**Round** `PIPD-S4-FINAL-PR18-CLOSEOUT-20261016`｜**Predecessor** `FAR-20261016-019-s4r6-external-handover`
**Class** decision study over an already-measured state + a deviation study over this round's own method.

## The question

The external acceptance report `PIPD-LS-SP-S4-EXTERNAL-FINAL-20261016` ruled the phase
`TEMP_CLOSED_CHALLENGE`, approved PR #18 and PR #17 for scoped merge, and installed a STOP RULE: no new
S4 core repair round unless one of five counterexamples is confirmed. The Owner now wants the work
executed and landed.

**What is the smallest set of governing-document-aligned actions that (a) restores an auditable,
externally checkable evidence trail, (b) does not reopen the repaired engineering surface, and
(c) leaves outstanding only effects that genuinely belong to the Owner — and how do we know the set is
complete rather than merely plausible?**

## Sub-questions this study had to answer with evidence, not prose

1. **Which subjects are actually frozen right now?** The report is a point-in-time review; a closeout
   must be reproducible after it. (Answer: re-read live; 13 field-level checks.)
2. **How do we report test numbers without laundering them?** Four environments produce four
   denominators; the report warns explicitly against reconciling them. (Answer: publish each raw line.)
3. **How do we judge a candidate whose own governed gate lives *inside* the candidate?** PR #18 modifies
   `.github/workflows/public-plugin-verify.yml`, which is the very artefact that declares the write-set
   allowlist. (Answer: run the classifier at the subject's head — and record that the naive route is
   wrong.)
4. **What happens when an orchestration lane the plan depends on dies mid-flight?** (Answer: declared
   deterministic fallback, recorded, not hidden.)
5. **What may not be claimed even though the tools technically allow it?** The credential could merge;
   governance says merge is an owner gate. (Answer: hand back, do not act.)

## What would have falsified the closeout

Any of the five STOP-RULE counterexamples, or freeze drift in `main` / PR #18 / PR #17 / the tag chain /
the release assets. None was found; (e) user-unusable version could not be excluded because no host
account was operated, so it is reported `NOT_RUN` rather than cleared.
