# Known findings ledger

Every finding raised by an independent checker in this session's rounds, with its **current** status.
Three values only: `RESOLVED` (a named artifact closes it), `PARTIAL` (remaining gap stated),
`OWNER` (cannot be closed by engineering alone), `WITHDRAWN` (the finding no longer applies).

| # | finding | status | evidence / remaining gap |
|---|---|---|---|
| K-01 | a wholesale repository rewrite was refused as over-engineered | `RESOLVED` | `EVIDENCE/repo-hygiene-20261013/REPO-ASSESSMENT-ENGINEERING-EVALUATION.md`; the refusal is recorded as a scope rejection |
| K-02 | the owner requirement was not closed by ready-made readiness artifacts | `PARTIAL` | `INTEGRATION/` readiness set published; closure still needs owner-class evidence (K-06, K-07) |
| K-03 | generated files and shortcuts polluting the payload | `RESOLVED` | `EVIDENCE/repo-hygiene-20261013/REPO-HYGIENE-REPORT.md`: `*.pyc` 127 -> 0, `*.lnk` 1 -> 0 |
| K-04 | a declared exclusion contradicted what was published | `RESOLVED` | `MANIFEST.json` schema v2 `exceptions[]`: declaration reconciled, runtime subtree named, nothing deleted |
| K-05 | publication procedure not reproducible (no in-repo builder) | `PARTIAL` | `SOURCE-PROJECTION.md` records the procedure; the builder itself is gated on the approval list (see `APPROVAL-LIST-PROPOSAL.md`) |
| K-06 | the canonical runtime binding baseline is uncertified (declared 0.20.0 / 3c27eb62 vs installed v0.21.5) | `OWNER` | needs a fresh G1 re-certification by the Human Policy Owner |
| K-07 | subject baselines are not certified in this mirror | `OWNER` | needs the Acceptance Officer; planners must treat the declared baseline as the planning assumption and the installed version mismatch as an explicit risk |
| K-08 | no independent digest recomputation is possible in a tool-less checker lane | `OWNER` | needs an owner-designated read-tool verification lane |
| K-09 | no tamper-evident commitment binds oracle time to dispatch time | `OWNER` | file mtimes are only an ordering witness; a hash-chain is new machinery the owner must choose |
| K-10 | the mandated checker arm was absent from the sealed lane pool, so checks ran provider-direct with no pool ledger | `OWNER` | route-registry change is owner-gated; each affected run is disclosed in its receipt |
| K-11 | long prompts passed as a single argv element produced no artifact on the PLAN lane | `PARTIAL` | rule recorded in `LANE-INVOCATION-NOTES.md`; a long-prompt run by file is the confirming test and has not been executed |
| K-12 | carried-forward findings from earlier rounds were never triaged individually | `RESOLVED` | this ledger; each row names its artifact or its remaining gap |

Nothing here is an acceptance. Presence of a row in this table is not a pass.
