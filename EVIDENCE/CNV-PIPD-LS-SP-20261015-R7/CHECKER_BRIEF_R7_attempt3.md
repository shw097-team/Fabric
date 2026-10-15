# CHECKER BRIEF — attempt 3 (close-out of the R7-0 independent verification)

You are the **independent checker** on the VERIFY/SECURITY lane (Codex CLI, provider/model
`opencode-go/glm-5.3-flash`). Claim ceiling: **LOCAL / candidate-only**; your verdict is a candidate for the
Owner — never an acceptance, approval or merge authorisation. Do not upgrade any verdict.

## Situation (read before acting)
- **Attempt 1** was voided by the dispatcher (`ERR_CHECKER_MUTATED_SUBJECT`, changed=14) because the mutation
  driver it re-ran wrote its raw receipts in place over the frozen subject `R6_DELIVERY/`. Those 14 files were
  restored byte-for-byte from the merged packet.
- **Attempt 2 was substantive and clean on your side** — it re-ran everything under its own root and wrote a
  verdict — but the dispatcher voided it too: `changed=0 removed=1`. The removed file was **not** removed by you:
  it was the gitignored byproduct `R6_DELIVERY/RUNNERS/__pycache__/probe_lib.cpython-311.pyc`, deleted *after*
  your turn by the orchestrator during a cleanup. That is an orchestrator fault, recorded as such, not a finding
  against your work.
- The subject is now verified intact: all 300 blobs under `_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/` are
  byte-identical to `origin/main:EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/**`, no byproducts.
- **Nobody will touch that subject while you run this attempt.** The dispatcher's rule is: `changed` or `removed`
  in the subject voids the verdict; `added` is recorded but not fatal. So: never change or delete anything there.

## Write-root rules
- Write **only** under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_CHECKER_ATTEMPT3/`.
- Write **nothing** under `…CNV-PIPD-LS-SP-20261015/` (contains the guarded subject) or under
  `C:/Projects/Agent_Workspace/PIPD/**`.
- Reads of the subject and of your own prior attempts are fine.

## What to produce (this attempt is a close-out, not a fresh review)
You may reuse your own raw outputs from attempt 2 — they are on disk and were produced by you:
`…-R7/R7_CHECKER_ATTEMPT2/RAW/` (33 files, incl. the 18-mutation re-run and the two pytest runs) plus your
attempt-2 `R7_CHECKER_VERDICT.json`. Re-derive rather than copy: for each item below, either re-run a short
confirming command in this attempt or cite the specific attempt-2 raw file that backs it, and say which.

1. Confirm the subject is intact **now**: 300 blobs under `R6_DELIVERY/` equal
   `origin/main:EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/**`, and
   `EVIDENCE/CNV-PIPD-LS-SP-20261015/PACKET_MANIFEST.json` sha256 =
   `27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b` at `main` (`b8ff8104…`), 581 blobs.
2. The central claim: re-confirm `M04`, `M06`, `M16` now `REJECT`; the seven previously detected stay `REJECT`;
   the eight never-executed stay `NOT_RUN`. One short driver run in your own root is enough (copy inputs first).
3. Weakening check on `R7_VALIDATOR_DIFF.patch` (no deleted/loosened predicate; fail-closed on a missing frozen
   context) — cite the diff lines you rely on.
4. Isolation fixture: cite your attempt-2 two-phase raw output (write succeeds → deny ACE → write denied →
   ACL restored) and re-confirm the ACL is not left applied on any subject path.
5. Regression classification: `7 failed, 319 passed, 2 skipped` — state whether your changed-tree and pre-change
   runs produced identical failure sets, with the two raw files that show it.
6. Unverifiable claims and disagreements with the writer.

## Output (write ALL of these, nowhere else)
`…-R7/R7_CHECKER_ATTEMPT3/`
- `R7_CHECKER_VERDICT.json` — schema `CNV-PIPD-LS-SP-20261015-R7/CHECKER-VERDICT/3`; per-item rows with `id`,
  `claim`, `method`, `evidence_path` (your own attempt-2 or attempt-3 file), `verdict` (`CONFIRMED`,
  `CONFIRMED_PRE_EXISTING`, `CHALLENGED`, `UNVERIFIABLE`, `ACL_UNENFORCEABLE`), `note`; plus
  `unverifiable_claims`, `boundary_violations`, `first_fail`, `overall_verdict` (`PENDING_OWNER` or `CHALLENGED`),
  and `claim_ceiling`.
- `R7_CHECKER_RECEIPT.md` — human-readable summary: what you ran in this attempt, what you re-cited from attempt 2,
  exact commands, exit codes, disagreements, and what remains unverifiable.
- `RAW/` — raw stdout/stderr of anything you run in this attempt.

## Hard constraints
- Do not modify the change under review, the product tree, or the guarded subject tree.
- Do not run any git write command, do not send anything to any outside host, never read or print credential material.
- Do not run the 221 acceptance cases, do not claim any Gate PASS.
- If a required condition cannot be met, stop and record it as a blocker with the raw error. A partial result
  reported honestly is the required outcome; a fabricated pass is a failure.
