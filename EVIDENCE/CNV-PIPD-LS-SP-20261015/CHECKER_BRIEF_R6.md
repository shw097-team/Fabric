# R6 CHECKER BRIEF — independent Acceptance Officer (VERIFY_SECURITY lane)

mission: CNV-PIPD-LS-SP-20261015
lane: VERIFY_SECURITY (Codex CLI, opencode-go/glm-5.3-flash)
round: CNV-PIPD-LS-SP-20261015-R6
role: independent checker. You are NOT the writer. The writer ran on a different model family
(opencode-go/deepseek-v4.1-flash). Your job is to challenge, re-derive and falsify — not to agree.

## 0. What you are checking
The bounded writer produced a candidate evidence set under
  WRITER_ROOT = C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/
described by its own R6_WRITE_SET.json and R6_WRITER_RECEIPT.json. The authoritative job order is the
compiled thin prompt at
  THIN = C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/compiler_native_output_R5/thin-prompt.md
(section 8 gives the evidence rules; section 9 the terminal states). Read it before judging.
Treat every writer artifact as an unverified CLAIM.

## 1. Write scope
You may write ONLY under
  CHECKER_ROOT = C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_CHECKER/
WRITER_ROOT is READ-ONLY for you; it is a guarded subject (its digest must not change during your
turn — if it does, your verdict is VOID and you must say so). No writes anywhere else.

## 2. Checks you must perform (each with a raw command + raw output)
1. Integrity: recompute sha256 + bytes for every file listed in R6_WRITE_SET.json and every file that
   exists under WRITER_ROOT. Report: missing, unlisted-but-present, hash mismatch, byte mismatch.
2. Boundary: list every file under WRITER_ROOT whose mtime falls inside the writer's declared window,
   and every file written elsewhere in the round window that you can detect (e.g. stray C:/c/ trees,
   the lane_runs dir, the handover root). Any write outside the declared WriteSet = boundary violation.
3. Reproduction: for EVERY executed probe the writer claims (each RAW/ log with a command), re-run the
   command yourself in a copy/where safe and record your own exit code + output. Writer claim that does
   not reproduce => verdict CHALLENGED with both outputs side by side.
4. Anti-fake evidence: for every artifact, decide whether its verdict rests on a real execution or on a
   static inventory / identity listing / file presence / summary / maker-shared evidence. Static-only
   support for a runtime claim => verdict MISREPRESENTED. "Real runner bound" claims must name the file
   and line of the runner; otherwise UNVERIFIABLE.
5. Rollback: independently reproduce the writer's checkpoint/rollback drill on a COPY of the candidate
   (never mutate WRITER_ROOT). Confirm the mutation is detected and the rollback restores the exact
   prior hashes. Report your own before/after hash table.
6. Secret scan: scan every file under WRITER_ROOT for credential-shaped material (long token strings,
   private keys, bearer headers, env files) and for any reference to paths containing "API KEY".
   Report findings verbatim (do not print the secret value itself; report file + line + a redacted
   fingerprint).
7. Register consistency: TT_CR_REGISTER.json must record TT-PIPD-03 = RESOLVED under the Owner order of
   2026-10-15 option A (SRC-DOC03 -> SUPPORT, governs=false) and must NOT let the bridge-mapping item
   describe itself as an equivalent Oracle writer. Any deviation => CHALLENGED.
8. Claim ceiling: no artifact may claim above LOCAL, no artifact may carry a verdict other than
   PENDING_CHECKER, and no artifact may present maker output as final acceptance. Any occurrence =>
   MISREPRESENTED.
9. Gate honesty: GATES_A_TO_H.json entries must be NOT_RUN / real-receipt-backed. A gate marked PASS
   on inference or file presence => MISREPRESENTED.

## 3. Output
Write CHECKER_ROOT/R6_CHECKER_VERDICT.json with, per artifact:
  {artifact, checker_verdict: CONFIRMED|CHALLENGED|UNVERIFIABLE|MISREPRESENTED, why, raw_evidence_refs}
plus:
  - checks_performed[] (each: check id, command, exit, raw output ref)
  - challenges[] (writer claim vs your measurement, both verbatim)
  - boundary_violations[]
  - secret_findings[]
  - overall: {verdict, independently_verifiable_claims, unverifiable_claims, blockers, hitl_items}
  - your own claim ceiling: LOCAL; your verdict is a candidate verdict for the Owner, not acceptance.
Also write CHECKER_ROOT/R6_CHECKER_RAW/** for your raw logs, and CHECKER_ROOT/R6_CHECKER_RECEIPT.md
as a human-readable summary.

## 4. Hard prohibitions
- No network egress; no repository publication; no remote operations.
- Do not read credential material; "C:/Projects/Agent_Workspace/API KEY/" is off-limits.
- Do not modify WRITER_ROOT, the source corpus, or the Shared Spine.
- Do not accept the writer's work by agreement: every CONFIRMED needs your own measurement.
