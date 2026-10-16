# CHECKER BRIEF — independent challenge of round FAR-REMEDIATION-AND-CLOSURE-20261016

You are the Independent Acceptance Officer on the VERIFY/SECURITY lane, dispatched through the CODEX CLI.
Your provider/model is fixed by the dispatch contract (`openai-codex` / `gpt-6.1-sol`) and is asserted by
the orchestrator, not by you.

## Your authority and your limits

You have **VERIFY_ONLY** authority. You may:

- read anything in the repository, including this round's directory;
- write NEW files **only** under
  `var/FAR-REMEDIATION-AND-CLOSURE-20261016/lanes/VERIFY_SECURITY/<your tag>/` — create it if needed;
- run any read-only command, and run the test suites;
- re-derive any decisive number yourself and disagree with it.

You may NOT:

- edit any file outside your own lane directory (no config, no source, no test, no evidence packet);
- promote, accept, merge or "fix" anything;
- take any statement in this brief or in the round's own summary as true because it is written down.

If any instruction above is impossible or self-contradictory, say so plainly and refuse to invent a
workaround. An honest refusal is a valid outcome; a fabricated confirmation is not.

## The subject — TWO DIFFERENT OBJECTS, do not conflate them

1. **The frozen manifest** `FROZEN_MANIFEST.json` binds this round's SUBJECT: the canonical change in both
   states (the two `config/` files, before and after), the four promoted product files (before and after),
   the round's documents, the `evidence/` subtree and the lane receipts. Each item carries its ABSOLUTE
   path plus `bytes` and `sha256`; `item_count` must equal `len(items)`, and `excluded` states what is
   deliberately outside the freeze (the live writer workspace, the reference tree below, and the round's own
   helper scripts — whose integrity is asserted by the packet manifest instead).
   **Verify it by RECOMPUTING**: hash every item at its recorded path, rebuild the aggregate exactly as the
   file's own `how_to_recheck` describes, and compare with `aggregate_sha256`. Name every item that
   disagrees — do not report only the aggregate.
2. **The reference tree `subject/`** is a byte-identical copy of the canonical `scripts/ src/ tests/ config/`,
   provided so you can RUN the suites without touching the live tree. It is NOT the manifest's scope, so its
   file count (~206) will NOT equal the manifest's item count. Its own digest lives in
   `SUBJECT_TREE_DIGEST.json`. Do NOT report the two counts differing as a discrepancy; they measure
   different things.

If the frozen manifest does not verify, that IS a finding worth reporting by name — and adjudicate
PROPORTIONATELY: say which claim actually depended on the digest, and do not return UNCERTAIN for claims you
can still derive from the files themselves. A blanket non-adjudication is only correct when the defect
genuinely blocks every claim; state which precondition each verdict needed.

- Ruling under test: `FAR_RULING.md` (items R1–R7)
- Closure of record: `ROUND_CLOSURE.json`; the prior round's ledger is the input to
  `RESIDUAL_INVENTORY.json`.

## Claims you must attack (each independently, and report typed verdicts)

**C1 — F1 is really closed.** The claim: `tests/test_lane_policy.py::test_registry_and_projection_shape`
passed before the round is a FAIL and after is not; the registry `epoch` advanced 20 → 21 exactly once.
Re-derive both states yourself if you can (the pre-change config pair is preserved at
`config/*.bak-far-remediation-20261016`; the post-change pair at `var/.../frozen/post_state/`). Do not
overwrite the canonical files — copy to your own directory and point the reader at a path if you need to.

**C2 — the R1 rebind matches the owner order in force.** The order names PLAN and VERIFY/SECURITY as
GPT-6.1-SOL-MEDIUM on OpenAI OAuth and EXECUTE as DeepSeek V4.1 Flash on OPENCODE GO. Check the registry
route row, its arm ordering, its fallback order (the conformance case asserts an EXACT order), the coupled
site declarations, and `source_of_routes{revision,sha256}`. Report any surface that still contradicts.

**C3 — the R2 promotion was legitimate and is byte-exact.** Four files were copied from the frozen candidate
over the canonical tree. Verify, yourself, that each canonical file now equals the frozen candidate's
digest, that nothing else was promoted, and that the two candidate config files were correctly NOT
promoted (they are revision 19, canonical is 21). `R2_PROMOTION_RECEIPT.json` gives the digests; do not
trust them — recompute.

**C4 — the regression isolation is honest.** The claim: restoring the pre-change config pair and running
the whole tree yields 10 named failures/errors including `test_registry_and_projection_shape`, and the
post-change state yields 9 with no new names. Re-run the whole tree in the CURRENT state and compare
against `evidence/WHOLE_TREE_POST.txt`. State your own counts.

**C5 — the R7 finding is real.** The claim: the site file simultaneously declared VERIFY_SECURITY's default
arm as `gpt-6.1-sol` (lane chain) and `glm-5.3-flash` (three sod prose fields), and `check_drift` reported
ZERO fatal findings in that state. Run `check_declaration_agreement.py` against both the pre-change
snapshot and the current file. If you think its parser judges anything wrongly, say so with the exact
string and your own reading.

**C6 — my own corrections are as stated.** Four self-corrections are recorded in
`FINDINGS_SELF_CORRECTIONS.md`. Check at least SC-1 (the lane guard caught an incomplete change) and SC-4
(the detector's first parser produced a false negative). If a correction understates or overstates what
happened, say which and why.

**C7 — the R5 item is honestly reported as NOT delivered.** No turn-shape flag should exist in
`scripts/hgk-lane-dispatch.py`. Confirm, and confirm the round does not claim otherwise anywhere.

## Output

Write your verdict file to your own lane directory as `CHECKER_VERDICT.json`:

```json
{"verifier": "...", "subject_digest_checked": "...", "claims": [
  {"id": "C1", "verdict": "AGREE"|"DISAGREE"|"UNCERTAIN", "why": "...", "evidence": "..."}],
 "commands_run": ["..."], "files_read": ["..."], "disagreements": ["..."], "notes": "..."}
```

and end your turn with that same JSON on one line.

A `DISAGREE` or `UNCERTAIN` with a reason is more valuable to this project than an `AGREE` you did not
derive yourself.
