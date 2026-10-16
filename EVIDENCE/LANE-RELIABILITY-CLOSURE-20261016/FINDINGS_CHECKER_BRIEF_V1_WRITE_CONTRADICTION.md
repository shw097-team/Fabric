# FINDING — the checker brief V1 contradicted itself, and the checker caught it

**Severity:** high for the round's evidence quality · **Status:** repaired in-roundly (V2) · **Resolved by:** me (orchestrator), not by any lane

## What happened

`CHECKER_BRIEF.md` V1 told the Independent Acceptance Officer two incompatible things at once:

- HARD RULE 1: *"Do NOT create, modify, delete or move ANY file."*
- Step 2/3: *build fixture mandate/pool files, seed a temporary `hermes_home`, and run the cases.*

The V2 brief was dispatched with the fixtures-to-be-built instruction still in place. The checker did
not paper over it: it refused to fabricate, executed only the cases that needed no writes, marked
`claim_B` **UNCERTAIN**, declared `named_suite` **NOT_RUN**, and put the contradiction itself into its
`uncertainties`. It also did not exploit the contradiction to reach a convenient verdict.

Its V1 verdict, quoted verbatim from the extracted artifact:

- `claim_B.verdict = UNCERTAIN`, all six cases `exit: null` — *"creating mandate/pool files conflicts
  with the explicit HARD RULE forbidding any file writes. Static inspection is not substituted for
  observed exits or refusal codes."*
- `claim_C.verdict = UNCERTAIN` — cases 1/2/3/5 returned `exit 0, allow,
  no-session-id-unattributable` / `non-mutating`, **independently reproducing my own harness's D07/D08
  observations on the same fixtures**; case 4 (the bound-maker denial) was not run for the same reason.
- `named_suite.status = NOT_RUN`.
- `uncertainties[0]`: *"The brief simultaneously forbids all file writes and requires writing fixtures, a
  test driver, and a verdict file."*

## Why this matters more than the missing re-derivation

The checker's job is to be the lane that does not agree for convenience. A checker that had quietly
turned my own contradiction into "all cases confirmed" would have produced a cleaner-looking packet and
worthless evidence. The refusal is the reason its other findings can be believed — including the
`DRIFT_VALUE` sweep it returned on the candidate copy, which matches my harness's D09 failure and is
explained by the candidate's `config/` snapshot predating ChangeSet A.

## Repair

`CHECKER_BRIEF.md` HARD RULE 1 now scopes writes instead of banning them: writes are permitted **only**
inside the checker's own work directory (`.../VERIFY_SECURITY/<attempt>/work/`) and any scratch
directory it creates, and are forbidden everywhere else, explicitly including the frozen subject at its
canonical path. The stdout-only verdict rule is kept, reworded so that "no verdict file" cannot be
misread as "no fixture files". Attempt `V2` runs against that repaired brief; its verdict supersedes V1
for `claim_B`/`named_suite` and is recorded whether or not it agrees with me.

## Rule extracted for future rounds

A verification brief that forbids writes must never also require the checker to build fixtures. Scope
writes to the checker's own work directory, and never to the subject under judgement. Where an
instruction is contradictory, a correct checker returns `UNCERTAIN` — so a brief that makes `UNCERTAIN`
the only correct answer has already failed, regardless of what the checker reports.
