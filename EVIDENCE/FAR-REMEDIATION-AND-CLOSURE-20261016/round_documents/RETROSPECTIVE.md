# RETROSPECTIVE — FAR-REMEDIATION-AND-CLOSURE-20261016

Proposals only. Nothing below is applied, accepted or merged. Ordered by this round's judgment of
value-per-unit-of-change, not by a measured cost model.

## What this round settled

- **F1 is closed.** The registry route row that disagreed with every other PLAN declaration was rebound to
  the arm the owner order names, and the whole-tree regression isolation shows exactly one test moving:
  `test_registry_and_projection_shape`, FAIL → absent, with **no test newly failing**.
- **The verified candidate is promoted.** Four files, byte-identical to the frozen candidate, with the
  orchestrator re-running the oracle itself (6 + 16 tests, OK).
- **The declared SoD conflict is reclassified** from "open, awaiting a decision" to "ordered and in force",
  with the surviving independence written down in the same record.
- **A previously invisible defect class is named, detected and demonstrated** (R7).

## What this round did NOT deliver

- **R5, the turn-shape flag.** The bounded writer did not return within its window. The cause of the second
  attempt's failure was diagnosed to this round's own brief (an ambiguous output path under the sandbox
  cwd) and the brief was corrected and re-dispatched — but the item is recorded as open, not as done.

## Proposals

| # | Proposal | Why it matters | Rough cost | Risk |
|---|---|---|---|---|
| P1 | Cross-field declaration sweep inside `lane_policy.check_drift` | closes the R7 class permanently; the rule is one comparison per single-lane prose field | ~30 lines + a RED-first test | low; it can only add findings, and a RED-first test pins the detection |
| P2 | Coupled-pin sweep (site digest, site revision, registry epoch) in the same pass | turns a half-applied declaration change from a dispatch-time guard failure into an edit-time gate failure | ~20 lines, reusing P1's walker | low |
| P3 | `--turn-shape {normal,edit_only}` in `scripts/hgk-lane-dispatch.py` | four bounded-writer turns across two rounds, two wedges; the fix is additive and already specified in this round's brief | small, additive; two of its three call sites are one-line | low, if the default path is proven unchanged by a receipt comparison |
| P4 | Hermetic lane-guard tests + two typed metadata-refusal catches in the dispatcher | the E11 investigation found a real contract defect: unreadable credential metadata crashes instead of producing the promised refusal receipt (`scripts/hgk-lane-dispatch.py:862-873`, `:1134-1135`) | moderate; test isolation plus two exception handlers and a regression each | medium — a refusal path is security-adjacent and must not become permissive |
| P5 | Prose-revision sweep of superseded narration (`sod_across_all_arms`, the retired deviation record) | removes text that contradicts the current declaration | low | lowest; documentation only |
| P6 | Fresh one-shot PLAN probe in the next round | this round carried D01 forward; a fresh probe makes the PLAN-plane claim self-contained | ~2 minutes of lane time | none |

## Standing lessons carried forward

1. Run the adjacent gate, not the gate you expect to pass. Two green gates read "done" while a third was red
   by four tests.
2. A declaration change is a multi-file change. Enumerate the surfaces that name the thing you are changing,
   and the pins that reference them, before the first edit.
3. A per-pointer comparator cannot see two pointer groups contradicting each other. Drift zero is not
   agreement.
4. State the sandbox root and cwd-relative paths in a bounded-writer brief. A probe sequence of tiny writes
   into new directory names is a path-ambiguity wedge, not an idle stall — the remediation is a corrected
   brief, not a longer timeout.

## Claim ceiling

CANDIDATE_ONLY. Every measurement behind these proposals was taken on this host by this session. No external
party has reviewed the round; no proposal is product code; executing a ruling is not accepting it, and
`hgk_canonical_acceptance` remains `NOT_PERFORMED`.
