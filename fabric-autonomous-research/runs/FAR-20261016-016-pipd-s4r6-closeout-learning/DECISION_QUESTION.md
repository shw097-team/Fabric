# Decision question

Round `PIPD-S4-R6-CLOSEOUT-20261016` asked: given the R6 challenge report's ruling (S4 Preview MVP
`TEMP_CLOSED`, `preview.4` published and immutable, one bounded docs pass, no new `.5`), what was the
best engineering action set — low-friction, feasible, necessary, not over-engineered, aligned with the
governing documents — and what did executing it actually teach?

Sub-questions answered with measurement rather than opinion:

1. Is the command薄's own `compiler_verdict_here: PROMPT_COMPILE_BLOCKED` a property of the product or of
   the environment that produced the薄?
2. Does the published `v0.1.1-preview.4` release still serve the frozen bytes, measured rather than
   quoted — and independently of the CI that produced it?
3. Is the served release content self-consistent with the tag it is published under?
4. Does a local full-suite run reproduce the challenge report's CI counts?
5. When the lane pool's rank-1 checker is the same model as the writer, is the round's independence
   evidence real, and what is the correct way to obtain the mandated checker without editing the registry?
6. What is the minimal defect set in the two documents the R6 report named, and does repairing only the
   literally-named line leave the reader with a working example?

## Out of scope by the R6 ruling (not re-litigated)

`.hgk/` migration, public plugin directory / KYC / review, S5–S8, production promotion, four-host
qualification, additional MCP/apps/hooks surfaces, PR #14/#15 CNV lanes.
