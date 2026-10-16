# FINDINGS — self-corrections this round (all four are my own defects)

Recorded because a round that only reports other people's defects is not reporting.

## SC-1 — R1/R3 was applied INCOMPLETE, and the existing test caught it

What I did: rebound `routes[].PLAN`, updated the coupled site prose and the registry expectations pinned on
those pointers, advanced the registry epoch, and stopped. I read `check_drift` (0 fatal) and
`test_registry_and_projection_shape` (green) as "done".

What was actually true: `tests/test_lane_guard.py` went from 0 failures to **4**, all `exit_code 3 != 4`.
The guard refused earlier than the tests exercise, with `ERR_LANE_SOURCE_STALE` and `epoch_current=false`,
because `source_of_routes{revision, sha256}` pins the site file's revision and byte digest, and because the
registry's `epoch` and the site's `revision` must move together. Neither coupling is drift-checked.

Correction: `apply_R1_R3_fix1.py` (receipt `R1_R3_COMPLETION_RECEIPT.json`) re-pinned both, re-ran the
guard suite (11 tests OK), the guard probe (now `exit 0 / ADMIT`), and `check_drift` (0 fatal).

Lesson recorded: **the gate that agrees with you is not the gate that covers you.** Two green gates said
"done" while a third was red by four tests.

## SC-2 — attempt 1 of R1/R3 was applied and then ROLLED BACK

What happened: after the first application, the conformance test failed on a different assertion
(`admission_status` must be one of `{ADMITTED, REFUSED, UNPROVEN}`; I had written a long measured string
there) and `check_drift` reported the aliased `/sod/provider_separation_status` pointer I had updated in the
registry but not in the site. I restored both files from the pre-change backups and re-applied after fixing
the script; `R1_R3_APPLY_RECEIPT.attempt1_ROLLED_BACK.json` is that attempt's receipt.

Side effect not smoothed over: the rollback restored **files only**. The requirement / taskspec / workorder
rows that attempt 1 had written to the Shared Spine SURVIVED, which is why attempt 2 raised
`UNIQUE constraint failed: requirements.requirement_id`. The consequence is benign — R1's WorkOrder exists,
created once — but it was an accident, not a design. `SPINE_STATE_READBACK.json` records the readback.

## SC-3 — R2's promotion first ran with no TaskSpec

`apply_R2_promote.py` called `create_workorder()` without creating the TaskSpec, so the spine refused with
`ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC` — **after** the four product files had already been promoted. The
record and the change were briefly out of step. `remedy_spine_workorders.py` created the missing
REQ/TS/WO; the failure and the remedy are both in `R2_PROMOTION_RECEIPT.json`.

## SC-4 — the R7 detector's first version hid the defect it exists to find

The first `claimed_default()` returned the first model token found in `MODELS` order rather than the first
by **position**. On the pre-change prose it returned `gpt-6.1-sol` for a sentence whose default is
`glm-5.3-flash`, and reported `AGREES` — a false negative on the very line under test, i.e. the detector
certified the defect as clean. Fixed to take the earliest position; the corrected run reports the 3
contradictions.

Correction to a claim I made from the buggy output: I said the detector independently catches F1. Under the
fixed parser it does not — pre-change, PLAN's prose agreed with PLAN's own chain (both `glm-5.3-flash`); F1
was a cross-file disagreement. Withdrawn here rather than left standing.

## SC-5 — the frozen subject was taken too early (found by the CHECKER, not by me)

Revision 1 of `FROZEN_MANIFEST.json` was taken before the checker's first verdict and before the round's own
helper scripts settled, so it no longer bound the paths it recorded. The first VERIFY/SECURITY turn (`V3b`)
recomputed the aggregate, obtained a different value, and **refused to adjudicate any claim** — `UNCERTAIN`
on C1–C7 — rather than inventing a replacement binding. That refusal is the correct behaviour and is the only
reason the defect is on the record; the checker also named the disagreeing files precisely.

Independently reproduced orchestrator-side: the round's own gate (`G2_frozen_subject_recomputes`) named the
same three helpers (`freeze_subject_round2.py`, `gate_round2.py`, `publish_packet_round2.py`).

Two lessons, neither of which the earlier freeze policy encoded:
1. **Freeze LAST, immediately before the manifest is consumed**, and retain every revision as a superseded
   file. A freeze taken mid-round is a claim about a moving target.
2. **Do not put the round's own tooling in the frozen set.** A helper script is edited legitimately between
   runs; freezing it manufactures a mismatch alarm about the orchestrator's own apparatus. Tooling integrity
   belongs to the *packet* manifest, which hashes every published file.

## SC-6 — the brief conflated two different objects

The first `CHECKER_BRIEF.md` gave the checker two things without saying they were different: the **frozen
manifest** (this round's subject) and the **`subject/` reference tree** (a byte-identical copy of the
canonical `scripts/ src/ tests/ config/`, provided so the checker can run the suites). The checker correctly
reported their differing file counts as a disagreement, because nothing in the brief said they measure
different things. `CHECKER_BRIEF.md` now names both objects, each one's scope, and requires **proportionate**
adjudication (a claim that does not depend on the digest must still be adjudicated) instead of a blanket
non-adjudication.

## Claim ceiling

These are self-reported corrections, evidenced by files on disk and by re-run commands whose output is
recorded. No external party has audited them, and no correction here has been accepted by anyone.
