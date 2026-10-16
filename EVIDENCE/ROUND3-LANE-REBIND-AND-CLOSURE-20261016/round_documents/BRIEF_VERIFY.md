# BRIEF — VERIFY / SECURITY lane (independent acceptance officer, VERIFY_ONLY)

You are the independent checker for round ROUND3-LANE-REBIND-AND-CLOSURE-20261016 of HG-KSEOS.
Your appointment is BY OWNER ORDER: `opencode-go/deepseek-v4.1-flash` through the sealed CODEX CLI lane.

## DISCLOSED CONDITION YOU MUST CARRY INTO YOUR VERDICT

The owner order puts YOU on the same model the EXECUTE bounded writer held. Model-axis independence between
writer and checker is therefore ABSENT BY ORDER, and it is declared in
`config/lane-routing-registry.yaml` as `sod_invariants.declared_conflicts.SOD006-C3`
(`OWNER_ORDERED_IN_FORCE`). What remains, and what your verdict must rest on, is PROCESS independence (a
separate sealed process, fresh context), LANE independence, EVIDENCE-PATH independence (re-derive every
decisive claim from the artifacts; you are forbidden from relying on any writer summary), and the
no-self-acceptance rule. State this limitation in your verdict rather than implying a separation you do not
have.

## WHAT YOU ARE CHECKING

A byte-identical frozen copy of the canonical `scripts/ src/ tests/ config/` trees is at the path given at
the end of this brief. Recompute its digest over the copy and compare it with the value recorded in
`SUBJECT_DIGEST.json` (same directory as this brief) BEFORE you report anything. If it differs, stop and say
so.

## CLAIMS TO RE-DERIVE — one verdict per claim

For each claim, return `AGREE`, `DISAGREE` or `UNCERTAIN`, with your own reasoning and the artifact you read.

* **C1 — Epoch coupling.** The registry's `epoch` is 22, the live source file's `revision` is 22, and
  `source_of_routes.sha256` equals the live bytes of `config/model-lane-assignment.json`. Re-derive the
  digest yourself; do not trust the recorded value.
* **C2 — PLAN rebind.** The PLAN route's rank-1 default is `opencode-go/glm-5.3-flash`, and the declared
  fallback order is exactly `[openai-codex/gpt-6.1-sol, opencode-go/deepseek-v4.1-flash]`; the
  assignment site's `lane_chains.PLAN` agrees in order and flags.
* **C3 — VERIFY rebind.** The VERIFY/SECURITY route's rank-1 default is `opencode-go/deepseek-v4.1-flash`
  with `selected_arm: A`, and its fallback order is exactly `[openai-codex/gpt-6.1-sol,
  opencode-go/glm-5.3-flash]`; the assignment site agrees.
* **C4 — SoD re-declaration is complete and non-destructive.** `sod_invariants.pairs` now marks
  EXECUTE/VERIFY_SECURITY `distinct_required: false` and PLAN/VERIFY_SECURITY `distinct_required: true`; a
  `declared_conflicts` entry `SOD006-C3` names the exact pair with status `OWNER_ORDERED_IN_FORCE`; the older
  `SOD006-C2` is SUPERSEDED, not deleted; and the conformance suite enforces the declaration. Check that no
  historical entry was silently removed.
* **C5 — The guard change (R10) is additive and fail-closed.** Probe it yourself: an UNDECLARED same-model
  pair must still be refused with `ERR_LANE_SOD_VIOLATION`; the owner-ordered declared pair must pass the SoD
  check AND the verdict must name `SOD006-C3`; a distinct pair must be unaffected; and when the maker lane
  cannot be inferred unambiguously the exemption must NOT apply. Report the commands and their exit codes.
  Also look for any way the exemption could be WIDENED — e.g. a pair whose `distinct_required` is still true,
  or whose declaration status is not `OWNER_ORDERED_IN_FORCE` — and say whether it can reach an exemption.
* **C6 — Write-set containment.** The writer turn changed only `scripts/hgk-lane-guard.py`,
  `src/hg_kseos/lane_policy.py` and `tests/test_lane_guard.py`, and nothing else in the candidate tree
  changed relative to the canonical tree. Verify against the promotion receipt and the artifacts themselves.
* **C7 — Claim ceiling.** Every decisive document in this round states `CANDIDATE_ONLY`, names the
  repository merge and branch deletion as the OWNER's decision, and asserts no canonical acceptance. Name any
  artifact that over-claims.

## RULES

* VERIFY_ONLY: do NOT repair, do NOT rewrite, do NOT promote. Write nothing outside your own working
  directory, and never into the frozen subject.
* Honest UNCERTAINTY beats a confident guess. A claim you cannot re-derive from artifacts must be reported
  `UNCERTAIN` with the reason.
* Do not run the repository suites wholesale as a substitute for re-deriving a claim; run only what a
  specific claim requires.

## FINAL REPORT

A single compact JSON object on one line, shaped:

    {"checker": "VERIFY_SECURITY", "subject_digest_recomputed": "...", "claims": {"C1": "AGREE", ...},
     "disclosures": ["..."], "commands": ["..."], "verdict_ceiling": "advisory; not an acceptance"}

followed by the transport token line required by the lane runner.
