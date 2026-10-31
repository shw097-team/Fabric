NONCE-ECHO: NONCE-PLAN-LANEACC-20261031-B

You are the PLAN lane (openai-codex/gpt-6.1-sol, medium) of HG-KSEOS round FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031.
Plan only: your single effect is to WRITE one file, `C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/oracle/ORACLE_LANE_ACCEPTANCE.md`.

MEASURED FACTS you must treat as the subject, not as claims to re-litigate:
- PLAN lane: rank 1, openai-codex/gpt-6.1-sol, exit 0, nonce echoed, 63.6 s, identity_source=codex-rollout,
  usage_rows_after_offset=0 (an OAuth-direct turn writes no relay usage row).
- EXECUTE lane: rank 1, opencode-go/deepseek-v4.1-flash, exit 0, nonce echoed, usage receipt ok.
- VERIFY_SECURITY lane: rank 1 is openai-codex/gpt-6.1-sol since registry epoch 40 (owner order this round);
  mimo-v2.6-flash is fallback 1. Under epoch 39 the same gpt-6.1-sol arm served VERIFY by rank 2 in 6.75 s and
  was refused only by --require-arm with ERR_ARM_NOT_IN_ASSIGNMENT (governance, not capability).
- With identity_source=relay-usage the dispatcher reports ERR_LANE_ALL_ROUTES_EXHAUSTED while the attempt record
  shows exit 0, model output present, usage_rows_after_offset 0, nonce_present false.

TASK: write an ACCEPTANCE ORACLE for the claim "all three lanes serve their assigned rank-1 arm, and the earlier
blocked-lane conclusion was an identity-source fault, not an arm fault". For each clause C1..C6 give the exact
observation that discharges it, the command/field producing it, and a FALSIFIER. Then three short paragraphs:
the minimum evidence set a checker needs; what the checker must NOT be given; the most likely vacuous pass.

C1 each lane serves its assigned rank-1 arm (required==served, no substitution)
C2 each lane's child echoes the round nonce verbatim
C3 relay-usage is the reason a run can report exhausted while the model answered (reproducible signature)
C4 codex-rollout resolves the served arm for an OAuth-direct turn without trusting a client-supplied session id
C5 an unassigned-arm refusal is distinguishable from a capability failure
C6 changing the dispatcher default must not weaken the frozen failure classification
   (no acceptable turn -> ERR_LANE_ALL_ROUTES_EXHAUSTED; answered without nonce -> ERR_NO_ARM_EMITTED_NONCE)

Begin the file with the NONCE-ECHO line, then C1..C6, then the three paragraphs. Write nothing else, anywhere.
