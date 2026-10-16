# The independent verdict, including every part that disagrees with me

Raw verdict: `lanes/VERIFY_SECURITY/V3c/work/CHECKER_VERDICT.json` (10,536 bytes; CODEX CLI on
`openai-codex` / `gpt-6.1-sol`; frozen subject revision 2, aggregate `4147b47c…`).

Dispatched under an explicit mandate that the writer and this checker are the same model family, so the
independence that exists here is **process + evidence-path independence, not model independence**. The
checker was required to RE-DERIVE every decisive number and forbidden to restate the round's own conclusions.
It did — and it disagreed on four of seven claims.

| claim | verdict |
|---|---|
| C1 — F1 (PLAN route row) is closed | **AGREE** |
| C2 — the R1 rebind matches the owner order in force | **DISAGREE** |
| C3 — the R2 promotion was legitimate and byte-exact | **DISAGREE** (byte-exactness YES, legitimacy NO) |
| C4 — regression isolation is honest | **UNCERTAIN** |
| C5 — the R7 finding is real | **AGREE** |
| C6 — my own corrections are as stated | **DISAGREE** (mechanisms reproduce; one description imprecise) |
| C7 — R5 is honestly reported as NOT delivered | **AGREE** |

## F-IND-1 — the manifest hashed ITSELF (my defect; now fixed)

> *"Sole mismatching item is the round FROZEN_MANIFEST.json itself: expected bytes=18015
> sha256=5d51820b…; actual bytes=18180 sha256=48d91dc8…. This is forbidden self-reference, not a
> reference-tree count discrepancy."*

It found this by **recomputing the aggregate** — the same check my own gate performs. A manifest that lists
itself can only ever record the PREVIOUS revision's bytes, so the aggregate could never verify. Fixed: both
`FROZEN_MANIFEST.json` and `GATE_REPORT.json` are now excluded from the frozen item set, with the reason
declared in the manifest's own `excluded` field. Neither disappears from the packet — the packet manifest
still hashes both; they are excluded only from the aggregate this file computes **about itself**.

## F-IND-2 — a THIRD cross-field contradiction, and my R7 detector has a scope gap (OPEN)

> *"site /sod/plan_lane says GLM is never auto-selected and /sod/verify_security_selection says arm B is
> never auto-selected, while registry PLAN fallback1 and VERIFY_SECURITY arm B declare
> automatic_selection=true. VERIFY_SECURITY arm C also combines an operator-selectable role with
> automatic_selection=true."* — located at `config/lane-routing-registry.yaml:297`.

This is the same CLASS as R7 (prose contradicting a structured field, invisible to `check_drift`), on an
axis my detector does not read: R7's detector compares the **default arm** claims, not the
`automatic_selection` flags. So:

- **Reported open, not repaired.** Changing `automatic_selection` changes routing behaviour and is a
  governance mutation belonging to a WorkOrder, not to this round.
- **My detector's scope gap is recorded as correction SC-7**, not quietly widened: `check_declaration_agreement.py`
  is a `claimed_default` checker; it does NOT establish "all cross-surface declarations agree", and the
  closure must not read as though it does.
- **Low-friction remediation for the owner** (options, no engineering): (a) make the registry's
  `automatic_selection` flags authoritative and correct the `/sod/*_selection` prose to match; or
  (b) make the prose authoritative and set those flags false, then re-run `check_drift` + the conformance
  case; or (c) add an `automatic_selection` axis to the agreement detector so the contradiction is caught
  mechanically in future rounds. (c) is the only option that prevents the next occurrence.

## F-IND-3 — the R2 promotion lacked PRE-WRITE typed admission and was not authored by the mandated writer (OPEN, disclosed)

> *"apply_R2_promote.py copies canonical files before attempting create_workorder, and the receipt records
> ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC; later remediation cannot retroactively supply pre-write admission.
> Its recorded writer is hermes-plan-orchestrator rather than codex. Exclusive historical scope also lacks
> an atomic pre/post whole-tree inventory."*

Both halves are true and both were partly disclosed at the time; the checker is right that disclosure is not
compliance. The precise consequence: **the byte-exactness of the four promoted files is verified
(the checker recomputed canonical/candidate/reference hashes and they agree), while the PROMOTION PATH's
governance compliance is NOT.** The claim ceiling for R2 is therefore split and must be quoted that way:
`bytes: VERIFIED` / `pre-write typed admission: ABSENT` / `canonical writer: NOT the mandated writer` /
`exclusive pre/post tree inventory: NOT TAKEN`. It is handed to the owner as an open item, not smoothed over.

## F-IND-4 — the whole-tree absolute counts are environment-dependent; the DELTA is what reproduces (calibration)

> *"Own current-state discovery … ran 540 tests: 29 failures and 17 errors, not recorded 527 tests with 7
> failures and 2 errors … The paired name-set delta removes only test_registry_and_projection_shape and adds
> none, supporting isolation of F1."*

Two separate facts, and the second is the one the round actually needed:

1. My recorded **absolute** counts do not reproduce in the checker's restricted reference tree — it names
   the missing dependencies (`run_acceptance`, `tools/package_local.py`, the task-local toolchain manifest)
   and a different interpreter. That is a reproduction limitation of the ENVIRONMENT, which the checker
   states explicitly ("not proof that the change caused 37 new regressions").
2. The **paired delta** — the thing the isolation claim rests on — reproduces exactly: one removal (F1),
   zero additions. Its own independently measured pair is 47 → 46 named failures/errors.

Consequence for the closure: the isolation claim is restated as a **delta claim** (`only F1 removed, none
added` — independently reproduced), and the absolute counts are labelled **environment-specific and not
independently reproduced**.

## F-IND-5 — SC-1's description was imprecise (my defect)

> *"SC-1 incorrectly describes all four as 3 != 4: actual assertions are one 4 != 0 (the otherwise-admissible
> receipt case) and three 4 != 3."*

Correct. The guard refused the incomplete change for TWO distinct reasons, and my description collapsed them
into one. Fixed in `FINDINGS_SELF_CORRECTIONS.md`. The checker also confirms the substantive mechanism
("Reconstructed incomplete site and registry hashes exactly equal the completion receipt pre-fix hashes")
and confirms SC-4 and the F1-detection withdrawal.

## What the checker confirmed independently (the parts that hold)

- `source_of_routes` revision 21 + the site digest match; default providers/models, GPT-medium/OAuth
  settings, exact ordered fallback lists and site chains all conform (C2's conforming half).
- The four promoted files are byte-exact against canonical, candidate and reference copy; all 200 prior
  frozen-candidate entries match; the two candidate config files were correctly NOT promoted.
- The reference copy matched its own recorded digest before testing (`73c59b31…`).
- R7: 3 contradictions pre-change, 0 post-change, reproduced by running the detector itself on both states.
- F1's closure: the preserved pre-change pair fails `test_registry_and_projection_shape`, the post-change
  pair passes, epoch 20 → 21 net +1.

## Claim ceiling

Advisory challenge only. `hgk_canonical_acceptance: NOT_PERFORMED`. No repair, promotion, deployment or
acceptance transition was performed by the checker, and none is claimed here. Two of the checker's findings
(F-IND-2, F-IND-3) are **open** and are the most valuable thing in this round.
