# Amendment 01 — the first four-surface driver completed normally

This amendment supersedes `ER-H1` of `ERRATA.md`, which is wrong. It is published as a separate artefact rather
than by rewriting `ERRATA.md`, because a published statement is corrected by supersession, not by editing.

## What was claimed, and what actually happened

`ER-H1` recorded that the round's first four-surface driver "hung with a zero-byte log" and "was killed". The
second half is false and the first half was a misreading:

- The driver exited **0** and its receipt printed in full. It was never hung. The log was empty because the
  driver's output was buffered and flushed only at exit, so an empty log at poll time proved nothing.
- The kill was attempted while it was still working; whether it survived the attempt or the attempt failed (the
  Windows taskkill returned 128), the process went on to finish its work and write its receipt.
- A zero-byte log is therefore **not** evidence of a hang, and "no output yet" is not evidence of a stall. Only a
  recorded timeout is. This is the correction to the round's own self-evolution record as well.

## What the completed receipt adds to this pack

The first driver's receipt is recovered here in full as `GOV_DRIVER_RECEIPT.json`. Three things in it are not in
the rest of the pack, and one of them strengthens the round:

1. **A named-method route with a negative control.** Its GSTACK measurement routed the positive flow
   `RESEARCH_LITERATURE_REPO` to `NATIVE`, and — separately — the negative control `PURE_QA_CHAT` to `GSTACK`
   (provider `gstack.qa`, state `CERTIFIED`, fallback `hgk_native_qa`). It also confirmed the registry carries the
   mandated arm. The bounded re-run only measured this round's own flow (`hygiene_readme_closure` -> `NATIVE`);
   the negative control is the stronger half of the surface evidence and belongs in the pack.
2. **A second SWARM graph.** The first driver created root `t_219dec8b` (three workers, verifier, synthesiser);
   the bounded re-run created root `t_02df625d`. Both exist. Any reader comparing this pack against the board
   should expect two graphs for this round, not one.
3. **The same OpenSpec failure as `ER-H3`, independently observed.** The first driver recorded `NOT_VALID` with
   the failing line `/bin/bash: line 1: cd: C:\Projects\Agent_Workspace\HG-KSEOS/` — the backslashed path
   again. It corroborates the errata rather than contradicting the later valid run.

## What does not change

- The board's cards are the same cards the bounded re-run read back; the ids are identical because the creation
  was idempotent. The published `KANBAN_SWARM_RECEIPT.json` is the bounded re-run's reading, and its histogram
  differs from the first driver's (`done 7 / running 7 / blocked 3` over 42 calls) because it was taken at a
  different moment against a board both drivers had touched. Neither reading is wrong; the bounded one is the
  later of the two.
- Every published blob still reads back byte-identical, the homepage candidate is unchanged, the fourteen branch
  removals are unaffected, and `main` is still untouched.
