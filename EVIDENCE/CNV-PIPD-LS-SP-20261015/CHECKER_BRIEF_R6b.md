# R6 CHECKER BRIEF — ADDENDUM b (attempt 3): persist the verdict, escalate authorized

mission: CNV-PIPD-LS-SP-20261015
lane: VERIFY_SECURITY (Codex CLI, opencode-go/glm-5.3-flash)
round: CNV-PIPD-LS-SP-20261015-R6, attempt 3

Read `CHECKER_BRIEF_R6.md` (the base brief) and this addendum together. This addendum changes only the
three environment blockers the previous attempt measured, and requires the verdict to be persisted.

## A. What the previous attempt (attempt 2) already established
Your previous turn produced an inline-only verdict (no file) because the checker identity had no write
authority. That verdict is preserved at
`C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_CHECKER_INLINE_attempt2/ALL_AGENT_MESSAGES_attempt2.md`
and summarised as: all 16 core artifacts CONFIRMED at declared (non-inflating) scope; overall
PENDING_OWNER; 46/57 probe re-runs UNVERIFIABLE (identity could not read Python311 or write); boundary
scan clean; secret scan clean; integrity 299/299 byte+sha exact; anchor guard unchanged (verdict not
voided). You may reuse those measurements, but you must STATE which ones you re-verified this attempt.

## B. What changed for this attempt
1. This dispatch runs the lane with an ESCALATED sandbox (`danger-full-access`), explicitly authorized
   in the dispatcher receipt. You now have write authority.
2. Write root (create it if absent):
   `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_CHECKER/`
   Required products:
   - `R6_CHECKER/R6_CHECKER_VERDICT.json` — the structured verdict (same shape as the base brief §3)
   - `R6_CHECKER/R6_CHECKER_RECEIPT.md` — human-readable summary, including the blockers section
   - `R6_CHECKER/R6_CHECKER_RAW/**` — one raw file per check/probe (command, cwd, UTC, exit, stdout, stderr)
3. `WRITER_ROOT` (`.../R6_DELIVERY/`) remains READ-ONLY for you and is a guard subject of this dispatch:
   if its digest changes during your turn, your verdict is VOID and you must say so.
4. Reproducing probes that write: copy the runner and its inputs into
   `R6_CHECKER/COPIES/<probe-id>/` and run it there. Do NOT write into `R6_DELIVERY/RAW/`. Record the
   substitution explicitly (declared path -> substituted path) so the Owner can see it.
5. Interpreters now readable: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`,
   `C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe`, and the Hermes venv python. If a
   declared `rerun_command` still cannot run verbatim, record the exact command you ran instead of it.

## C. Scope of this attempt (do not expand it)
Same nine checks as the base brief. Priority order:
1. Re-run as many of the 46 previously-unverifiable probes as you can, from your copies, and record the
   real exit codes/outputs. Keep the ones you still cannot run under UNVERIFIABLE with the measured reason.
2. Re-do the CHECKPOINT_AND_ROLLBACK re-run on your own copy of the candidate and report your own
   before/after hash table.
3. Persist the full verdict + raw evidence to the files above.
Anything you did not re-measure this attempt must be labelled as carried-over from attempt 2, not as
measured now.

## D. Unchanged hard prohibitions
No network egress; no repository publication or remote operations; no reading credential material
(`C:/Projects/Agent_Workspace/API KEY/` is off-limits); no writes outside `R6_CHECKER/`; do not modify
WRITER_ROOT, the source corpus, or the Shared Spine. No acceptance by agreement: every CONFIRMED needs
your own measurement in this attempt or an explicit carry-over label. Your verdict is a candidate verdict
for the Owner; claim ceiling LOCAL.
