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
| K-13 | the local Fabric tree has no remote linkage, so a round's Fabric-side work can be committed and still never reach this mirror | `OWNER` | `EVIDENCE/SKILL-CONVERGENCE-20261014/PUBLICATION-RECORD.md` section C: the round's hygiene work was local-only until this change-set projected it; the remote linkage itself stays the owner's open item (`MANIFEST.json` `pending`) |
| K-14 | a closure text described the Fabric front page as upgraded when it had only been committed | `RESOLVED` | corrected in the publication record; the round section is added by this change-set |
| K-15 | a publication manifest can list a file the commit silently drops, because the host repo's own ignore rules apply | `RESOLVED` | the commit-byte read-back refused to claim reproducibility and the packet was renamed; the rule is recorded in the `remote-repo-publication` skill |
| K-16 | the reference population still exceeds the linter's warning line (94 files against 60) | `PARTIAL` | only a 14-file pilot group was merged this round; the remaining topic groups are unmerged |
| K-17 | the control plane's timeout path discards partial captures | `PARTIAL` | a candidate patch exists (2,621 bytes) and is **not** landed; landing needs its own admission and governed change-set |
| K-18 | this round's lane failures (12 timeouts, 2 nonce-less dispatches, 1 contaminated verdict, 1 empty answer) | `PARTIAL` | none repaired; the timeout class was root-caused and the lane budget raised, and every failure is retained in the round record |
| K-19 | the guarded apply path has only ever run against fixtures | `PARTIAL` | no real write was executed; the subject stays candidate-only |
| K-20 | the round's return packet was first pushed to a repository the owner had not named for it | `RESOLVED` | `EVIDENCE/SKILL-CONVERGENCE-20261014/PUBLICATION-RECORD.md` section A: the packet was republished byte-identically to this repository's branch `evidence/skill-convergence-20261014-full-packet` and the other repository's branch was deleted (its `main` never moved); the deleted tip is recoverable from this branch |

Nothing here is an acceptance. Presence of a row in this table is not a pass.
