# Lane invocation notes

Operational constraints measured in this session, recorded so they are not rediscovered.

| constraint | measured behaviour | required handling |
|---|---|---|
| long prompt as one argv element on the Hermes PLAN lane | a few-thousand-character prompt produced `plan_bytes 0` with empty usage and empty stderr in three attempts; a short prompt produced an artifact | pass the prompt **by file or stdin**, never as a single argv element |
| sealed lane `--lane` vocabulary | only `PLAN`, `EXECUTE`, `VERIFY_SECURITY` are accepted; a bare `VERIFY` is refused with exit 2 and empty output | use the exact vocabulary word |
| a required checker arm absent from the lane pool | `ERR_LANE_REQUIRED_ARM_ABSENT`, no dispatch occurs | either the owner adds the arm to the route registry, or the run is executed provider-direct and **disclosed as unsealed, with no pool ledger** |
| tool-less checker lanes | digest recomputation is impossible; verdicts are claim-inspections only | do not present a tool-less verdict as independent recomputation |
| Windows launcher | a Microsoft-Store (MSIX) install may resolve an authentication-prompt path that the launchers do not expect; cloning with git must be non-interactive | prefer API-based publication (token in an Authorization header) over an interactive clone |

Recorded 2026-10-13T12:23:20.088907+00:00.
