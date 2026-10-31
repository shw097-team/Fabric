NONCE-ECHO: NONCE-PLAN-LANEACC-20261031-A

You are the PLAN lane (openai-codex/gpt-6.1-sol, medium) of HG-KSEOS round
FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031. You are planning, not executing: write no files, run no
network calls, change no state. Produce one artifact and nothing else.

CONTEXT
The owner states: "this round measured that all three lanes can serve; the failure was the identity
source (the default relay-usage can never obtain a usage row on this host), not the arm."
A previous round recorded VERIFY_SECURITY as unusable (P5C_LANE_VERIFY_BLOCKED) on that basis.
We must now accept or refuse that claim *by measurement*, then, if it passes, solidify it:
(a) change the dispatcher's default identity source, (b) make the no-usage-row case a named failure
instead of the generic exhausted code, (c) promote the finding into the control plane, (d) push it.

The lane policy is at epoch 40: PLAN=openai-codex/gpt-6.1-sol medium, EXECUTE=opencode-go/deepseek-v4.1-flash,
VERIFY_SECURITY=openai-codex/gpt-6.1-sol medium (rank 1, automatic), with opencode-go/mimo-v2.6-flash as
fallback 1. Dispatcher: scripts/hgk-lane-dispatch.py. Relay: loopback 127.0.0.1:10101 (healthz ok).

YOUR TASK
Produce an ACCEPTANCE ORACLE for the claim set below. For each clause give: the exact observation that
discharges it, the command or field that produces that observation, and a FALSIFIER (the observation that
would make it fail). The oracle must be decidable by a checker that did not run the probes.

C1  Each of the three lanes serves its assigned rank-1 arm: required==served, no substitution.
C2  Each lane's child echoes the round nonce verbatim (the run is provable, not asserted).
C3  The relay-usage identity source is the reason a run can report exhausted while the model answered:
    reproduce it and show exit 0 + model output + usage_rows_after_offset 0 + nonce_present false.
C4  The codex-rollout identity source resolves the served arm for an OAuth-direct turn, and does so
    without reading a client-supplied session id.
C5  A lane refusal for an unassigned arm is distinguishable from a capability failure
    (ERR_ARM_NOT_IN_ASSIGNMENT before spawn, versus a transport error after spawn).
C6  Changing the dispatcher default must not weaken the frozen C1 failure classification: a run with no
    acceptable turn still reports ERR_LANE_ALL_ROUTES_EXHAUSTED, and a run that answered without a nonce
    still reports ERR_NO_ARM_EMITTED_NONCE.

Also state, in one paragraph each: the minimum evidence set the checker needs; what a checker must NOT
be given (so the maker does not write the officer's claim set); and the single most likely way this
acceptance could pass vacuously.

OUTPUT FORMAT
Plain text, starting with the NONCE-ECHO line above, then sections C1..C6, then the three paragraphs.
No preamble, no apology, no file writes.
