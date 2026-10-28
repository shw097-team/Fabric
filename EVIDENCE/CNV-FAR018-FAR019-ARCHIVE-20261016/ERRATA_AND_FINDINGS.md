# ERRATA AND FINDINGS — CNV-FAR018-FAR019-ARCHIVE-20261016

Every item below was produced by THIS round's own execution.  Nothing here is repaired silently: the
finding is recorded with what was measured, what was done about it, and what remains open.

## Defects this round found in its own harness

| # | Defect | Measured | Disposition |
|---|---|---|---|
| ER-A1 | A module-level name reported `NameError` at a later line although the AST showed it assigned at module level in the same file (`archive_contract.py`, line 29 assigned / line 82 loaded, both module scope, no invisible characters in either line's `repr`) | Two identical runs failed the same way; the AST dump proved the binding existed | WORKED AROUND by inlining the expression. **NOT EXPLAINED** — recorded as a harness/environment anomaly, not as a theory. |
| ER-A2 | `PL-009` binds `intent.requested_delivery` and `journeys[].journey_id` to acceptance edges carried from the archive lineage, so a new round cannot rename them without inventing an acceptance edge | First lint run: `PL-009 deliverable DEL-* lacks acceptance edge`; renaming the journey id alone then produced `PL-009 journey ... lacks acceptance edge` | The bound ids are kept and DISCLOSED: they name the prior round's artifacts, which is a contract-lineage defect of the carried acceptance list, not a claim about this round. |
| ER-A3 | Five control-plane policies the order names as `control/{AUTHORITY_MATRIX,SOD_POLICY,CHANGE_CLASS_ROUTER,ACCEPTANCE_POLICY,RELEASE_POLICY}.yaml` under HG-KSEOS DO NOT EXIST there | `HG-KSEOS/control/` holds no such files; the canonical copies are `Fabric/FABRIC/control/*.yaml`; `Fabric/AGENTS.md` is genuinely ABSENT | Sources re-registered at their real paths; the absent `Fabric/AGENTS.md` stays declared in `source_scan.missing` as a real gap rather than being quietly dropped. |
| ER-A4 | `openspec validate --strict` exits with `FileNotFoundError` when driven by the gateway interpreter, which has no npm on its PATH | Attempts recorded: `openspec` and `npx` both `WinError 2`; the SAME command in a login shell printed `Change 'cnv-far018-far019-archive-20261016' is valid` | Recorded with both readings. The toolchain verdict comes from the shell run; the interpreter-PATH failure is a harness fact, not evidence about the change record. |
| ER-A5 | `mergeable: null / mergeable_state: unknown` is GitHub's post-merge RECOMPUTATION window, not a conflict — and an UNMERGED pull request also exposes a `merge_commit_sha` (a preview commit that is not on main) | After #12 merged, #13 and #14 read `mergeable: null`; a naive reading of #14's `merge_commit_sha=c3ac660a` would have recorded a merge that never happened (main did not contain it) | Both PRs were HELD, then merged on the next settle-and-reread run once two independent surfaces (REST `mergeable: true` and GraphQL `MERGEABLE/CLEAN`) agreed. **Never treat `merge_commit_sha` on an unmerged PR as a merge.** |
| ER-A6 | The round's own verdict rule scored a fully merged round as PARTIAL | A rerun reports `ALREADY_MERGED_READBACK_ONLY`, which the first rule treated as a non-pass | Fixed: the verdict accepts the SET of equivalent merged statuses. Disclosed because the first A09 receipt said PARTIAL. |
| ER-A7 | `PACK_INDEX.json` cannot carry its own digest and must cover the WHOLE pack | Same class as the previous round, where a stage-scoped index left 52 files unindexed | The index lists every published file except itself; its own digest is bound by the publish receipt. |

## Findings carried from the independent acceptance report (12/12)

See `A09_RETURN_PACKS.json :: finding_dispositions` for all twelve with owner, state and evidence ref.
Summary: 4 resolved_in_round (#05/#06/#07 index semantics clarified, #12 config-backup sensitivity
reviewed: NO credential value present), 1 partial (#08: only the B0 archive batch was signed here),
4 deferred (#01 checker verdict extraction, #02 validator promotion, #03 checker isolation, #04 fresh G1,
#11 owner dossier), 2 recorded as disclosures (#09 same-arm/timeout, #10 no CI status).

## What this round does NOT claim

`INDEPENDENT_PASS`, `AO_ACCEPTED`, `DOC05_EFFECT_ADMITTED`, `FULL_CONVERGENCE`, `PRODUCTION_RELEASE`,
`RUNTIME_READY`: none of these is claimed, and no merge here substitutes for any of them.
