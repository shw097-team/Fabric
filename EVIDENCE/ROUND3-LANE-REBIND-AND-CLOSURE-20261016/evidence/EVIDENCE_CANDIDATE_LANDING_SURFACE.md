# EVIDENCE: candidate-but-not-landed audit surface (ROUND3-LANE-REBIND-AND-CLOSURE-20261016)

Read-only audit. Nothing edited. Claim ceilings per item; UNKNOWN where not measurable.

## Measured facts

- openspec_changes_non_archive: 23
- openspec_specs_dir: ['ao-lane-independent-verify']
- archive_entries: ['2026-10-10-ao-lane-independent-verify-20261010']
- strict_invalid_changes: ['hgk-plan-plane-rebind-20261015', 'sod-independent-verify-enforcement']
- strict_valid_changes_count: 21
- changes_with_git_tracked_code_refs: {'hgk-checker-upgrade-adapter': 1}
- candidate_or_frozen_dirs_found: 22
- skills_total_in_library: 72
- governed_workstream_skills_round_authored: 16

## Surface 1 — OpenSpec CHANGES never APPLIED / never ARCHIVED (23 folders)

OPENSPEC/specs holds exactly ONE landed spec (ao-lane-independent-verify); archive holds exactly ONE entry (2026-10-10). So ALL 23 non-archive change folders are unapplied and unarchived.

| change | spec_deltas | main-spec exists | strict valid | code/test refs | workstream-20261015/16 | disposition | reason |
|---|---|---|---|---|---|---|---|
| gcm-noninteractive-default-containment | git-credential-noninteractive-default | no | yes | 0 | no | DEFER | valid strict but its scripts/ were partially created (staged) and never exercised as a round item; no corresponding spec, no code refs |
| hermes-incident-2026-10-05-repair | hermes-runtime-binding-integrity, hermes-runtime-incident-integrity | no | yes | 0 | no | DROP | dated incident proposal (2026-10-05) whose repair window has passed; no spec landing, no code refs |
| hgk-checker-upgrade-adapter | independent-checker-execution | no | yes | 1 | no | DEFER | single doc mention in usage guide; adapter proposal never landed as spec |
| hgk-far-remediation-20261016 | lane-governance-gates | no | yes | 0 | yes | LAND | this workstream, 20261016; R1 (PLAN rebind) measured as executed outside the round per r10's reconciliation note - reconcile its 25 task rows then archive; structurally valid |
| hgk-lane-brief-and-guard-hardening-20261015 | lane-brief-and-guard-hardening | no | yes | 0 | yes | DEFER | workstream 20261015; hardening lessons were absorbed into the hgk-kanban skill body; change record itself unreconciled |
| hgk-lane-reliability-closure-20261016 | lane-governance-gates | no | yes | 0 | yes | LAND | this workstream; ChangeSet A applied under WO with receipt; promoted candidate remains CANDIDATE_ONLY, needs application/acceptance step then archive |
| hgk-plan-plane-rebind-20261015 | — | no | NO | 0 | yes | FIX-or-DROP | FAILS strict validation (scenario-less requirements); premise already superseded by later owner rebinds - fix format or close as superseded |
| hgk-r10-session-closure-20261016 | r10-session-closure | no | yes | 0 | yes | LAND | this workstream, currently executing reconciliation round; only valid path to closing the other 20261016 changes |
| hgk-r8-eia-closure-skill-slim-20261016 | r8-eia-closure-and-skill-slim-regression | no | yes | 0 | yes | LAND | this workstream, proposal-only contract gate governing skill-slim/apply-authorization - keep as owner gate |
| hgk-r9-far-residual-closure-20261016 | r9-far-residual-closure | no | yes | 0 | yes | DEFER | this workstream; validator-adaptation candidate EXECUTED-CANDIDATE, acceptance tasks unchecked; continue under R9/R10 |
| hgk-skill-convergence-20261014 | governance-skill-convergence | no | yes | 0 | yes | DEFER | workstream; guarded-apply tooling and patches sit unapplied in var/SKILL-CONVERGENCE-20261014/candidates |
| lane-health-repair-20261011 | lane-dispatch-honest-declarations | no | yes | 0 | no | DEFER | older workstream change; no spec land, no refs |
| lane-mandate-rebinding-and-d01-revocation | lane-mandate-rebinding | no | yes | 0 | no | DEFER | older workstream change; rebind history superseded by 20261015/16 chain rebinds |
| lane-model-chain-rebind-20261015 | lane-model-chain-policy | no | yes | 0 | yes | DEFER | this workstream; full rebind procedure reference exists in hgk-kanban skill; change record itself never reconciled |
| lane-sod-enforcement | lane-sod-enforcement | no | yes | 0 | no | DEFER | proposal names a spec capability never landed; overlapping with sod-independent-verify-enforcement |
| lane-supervisor-windowless-convergence | scheduled-task-console-window | no | yes | 0 | no | DROP | supervisor-window proposal with no corresponding behavior on disk and no refs |
| lane-toolchain-identity-and-failure-classification | lane-toolchain-identity | no | yes | 0 | no | DEFER | only archived change is ao-lane (related); this one unreconciled |
| lane-verify-dual-routing-and-plan-high | lane-verify-dual-routing-and-plan-high | no | yes | 0 | no | DEFER | routing history superseded by later chain rebinds |
| lane-verify-routing-remediation | model-lane-routing | no | yes | 0 | no | DEFER | routing history superseded by later chain rebinds |
| skill-mainfile-cap-remediation | skill-mainfile-cap-governance | no | yes | 0 | yes | DROP | r10 reconciliation measured the governed cap never exceeded, main files far under 100000 bytes; split remedy superseded |
| sod-independent-verify-enforcement | — | no | NO | 0 | no | LAND-or-REPAIR | FAILS strict validation but its S1* candidate (worktrees/hgk-sod-s1star-20261009) is real, unapplied, owner-gated - highest-value unlanded candidate; fix scenario blocks before apply |
| strict-declaration-20261011 | strict-declaration | no | yes | 0 | no | DEFER | older workstream change; unreconciled |
| verification-artifact-contract | verification-artifact-contract | no | yes | 0 | no | DEFER | proposal-only contract change; unreconciled |

## Surface 2 — Candidate artifacts on disk (candidate/ and frozen/ dirs; apply receipt status)

| path | kind | status | markers | recommended |
|---|---|---|---|---|
| `var/LANE-RELIABILITY-CLOSURE-20261016/candidate/**` | full candidate tree (config/scripts/src/tests snapshot + ChangeSets B/C) | candidate-only; ChangeSet A (model-lane-assignment.json + lane-routing-registry.yaml) APPLIED 2026-10-16T03:28Z; candidate copies differ from canonical (post-apply further edits possible) | FROZEN_MANIFEST.json, CHANGESET_A_APPLY_RECEIPT.json, README claim ceiling CANDIDATE_ONLY | None |
| `var/FAR-REMEDIATION-AND-CLOSURE-20261016/candidate/scripts/hgk-lane-dispatch.py` | candidate writer file produced by R1-R3/R5 rounds | NOT_APPLIED多头? diff vs canonical scripts/hgk-lane-dispatch.py: DIFFERS (canonical untracked in git; candidate mtime earlier than canonical) | candidate/ dir, apply_R1_R3*.py receipts | None |
| `var/FAR-REMEDIATION-AND-CLOSURE-20261016/frozen/**` | frozen subject manifests | frozen manifest only - evidence binding | FROZEN_MANIFEST.json | None |
| `var/LANE-ENFORCEMENT-APPLY-20261015/candidate/**` | apply-round candidate set | partially applied per its own receipts (admission_C/D); residual items named in its checkpoint | ACCEPTANCE_MATRIX.json, BUILD_* Specs | None |
| `var/hgk-solution-apply-20261012/candidate/**` | rebinding candidate | APPLIED per APPLIED_REBINDING_RECEIPT.json (20261013T013301Z) | APPLIED_REBINDING_RECEIPT.json | None |
| `var/FAR-LANE-REPAIR-20261014/CANDIDATE/hgk-lane-dispatch.py` | candidate dispatch | DIFFERS from canonical (not applied byte-identical) | CANDIDATE_INJECTION_TEST.json, CANDIDATE_META.json, patch file hgk-lane-dispatch.codex_home_config.patch | None |
| `var/FAR-LANE-ENFORCEMENT-RCA-20261015/frozen/**` | frozen evidence set | frozen manifest (evidence binding only) | MANIFEST.json, FAR_RULING_CANDIDATE.md | None |
| `var/SKILL-CONVERGENCE-20261014/candidates/**` | guarded-apply tooling + patches incl lane-dispatch-timeout-capture.patch | patch NOT applied: var copy differs from canonical; DISPOSITION unknown | apply/patch/*.patch, phase1_result.json | None |
| `worktrees/hgk-sod-s1star-20261009/maker/candidate/**` | S1* lifecycle+spine candidate (sod-independent-verify-enforcement ChangeSet S1*) | NOT_APPLIED to canonical (candidate spine.py/lifecycle.py differ from canonical; tasks.md: 'Apply to canonical tree (owner gate - NOT executed)') | migrations/0001_evidence_subject_digest.py (migration authored, not run) | None |
| `worktrees/hgk-sod-verify-handoff-20261009/maker/candidate/**` | verify-handoff candidate | NOT_APPLIED (unknown, differing bytes) | — | None |
| `worktrees/pipd-r2-core-20261009/maker/candidate/**` | PIPD R2 candidate | UNKNOWN | — | None |
| `config/lane-route-slots.candidate.json` | candidate config (route slots 012) | UNAPPLIED? - sits in config/ untracked in git with .bak chain; applied-ish but never git-tracked | *.bak-rev* | None |
| `var/far-lane-sod-007/resume-20261008/gate-qualification-candidate` | gate qualification candidate | UNKNOWN | — | None |
| `var/far-lane-sod-008-console-window-20261008/candidate-fix` | console-window fix candidate | UNKNOWN | — | None |
| `var/far-iao-lane-skip-20261012/candidate` | IAO lane-skip candidate | UNKNOWN | — | None |
| `var/far-iao-lane-skip-20261012/verify/scratch/simulated_candidate` | simulated candidate (verify scratch) | simulated - not real | — | None |
| `var/FAR-GOV-SKILLS-20261014/candidate` | decision matrix + research synthesis | research artifact, no apply target | — | None |
| `var/rounds/R2-SOD-FIX1-DISPOSITION-20261009/maker/candidate/**` | SOD FIX1 maker candidate | NOT_APPLIED byte-wise | — | None |
| `var/hgk-solution-apply-20261012/execute/candidate-snapshots` | apply snapshots | snapshot | — | None |
| `var/LANE-ENFORCEMENT-APPLY-20261015/probe/probe-link/candidate` | probe artifact | probe | — | None |
| `var/lane-route-001/candidate` | lane-route candidate | UNKNOWN | — | None |
| `scripts/hgk-lane-dispatch.py (untracked canonical-name file)` | canonical dispatcher itself UNTRACKED in git | whole dispatcher was never committed - can't tell applied from candidate by git | .bak-lanerepair / .bak-x2b / .bak-z2 backups | None |

## Surface 3 — Workstream skills unvalidated by anyone other than their author

| skill | last touched | bytes | refs | unvalidated round lessons | reference claims |
|---|---|---|---|---|---|
| software-development/hgk-kanban-and-lane-routing | 2026-10-16 | 88115 | 20 | R10 round's lane-rebind/brief-marker/subject-guard lessons authored 2026-10-16 by the round itself ('a packet that copies whole skill trees is BLOCKED', 'ERR_NO_ARM_EMITTED_NONCE', receipt-per-role ov | SKILL.md references scripts/runtime_role_binding_assert.py and scripts/start-hgk-exec-frontdoor.ps1 which live in the HG |
| hgk-lifecycle-admission | 2026-10-16 | 35739 | 10 | rules 5,16,26 etc carry round-specific measured lessons (PLAN-model mandate, owner-grant scope reading, PLAN_READY stranded project) asserted from single-round observation | — |
| software-development/remote-repo-publication | 2026-10-16 | 44335 | 8 | publishes lab-rat B/anonymous-readback recipes; round-authored | — |
| software-development/hgk-governed-execution | 2026-10-16 | 21026 | 115 | 115 reference files is just above the R8-0 'more than 60 references = WARNING' threshold; whether the hard gate applies is not defined in the change (proposal-only); main file 21026 bytes is far below | — |
| software-development/adversarial-verification-rounds | 2026-10-16 | 23151 | 29 | round-authored | — |
| software-development/lossless-content-consolidation | 2026-10-16 | 10864 | 1 | round-authored | — |
| software-development/canonical-change-landing | 2026-10-15 | 12441 | 0 | round-authored; body cites NO reference files; skill claims rollback+probe discipline but nothing on disk supports it beyond the body itself | no references/ dir or scripts back the body's probes |
| governed-write-admission | 2026-10-15 | 16733 | 4 | round-authored | — |
| software-development/destructive-path-guards | 2026-10-15 | 16402 | 0 | round-authored; 0 reference files; body-only support | — |
| software-development/long-running-worker-supervision | 2026-10-15 | 67824 | 8 | round-authored | — |
| software-development/provider-routing-triage | 2026-10-15 | 30659 | 4 | round-authored | — |
| software-development/governed-stack-audit | 2026-10-15 | 61801 | 12 | round-authored | — |
| software-development/hgk-enforcement-closure | 2026-10-12 | 12956 | 1 | round-authored | — |
| software-development/windows-lane-verification-audit | 2026-10-09 | 5963 | 0 | round-authored | — |
| software-development/inspecting-hermes-desktop-dom | 2026-10-05 | 6250 | 0 | possibly workstream-authored | — |
| software-development/node-inspect-debugger | 2026-10-05 | 11065 | 0 | UNKNOWN authorship | — |

## Unknowns

- **UNKNOWN** 22 of 23 change folders have NO code/test reference searchable in tracked src/tests/scripts/docs/config — verification attempted: grep over git-tracked paths; untracked working-copy files were NOT exhaustively grepped (repo has a large untracked set incl. Fabric/, HGK/, SQS-THC/)
- **UNKNOWN** whether each of the 23 change folders was 'APPLIED' to main specs exactly once and archived per the repo's own workflow — verification attempted: OPENSPEC/specs holds only ao-lane-independent-verify and the archive dir holds exactly one entry - so every other change is unapplied/unarchived, but WHICH round meant to apply the
- **UNKNOWN** var/far-lane-sod-007/gate-qualification-candidate, var/far-lane-sod-008/candidate-fix, var/far-iao-lane-skip-20261012/candidate, var/lane-route-001/candidate, worktrees/pipd-r2-core-20261009 - NO apply receipts found in their trees; whether each was applied outside them (as_changeSet B/A receipts exist elsewhere) is not determinable from disk alone — verification attempted: walked each candidate dir for APPLIED_RECEIPT/APPLY_RECEIPT naming; none found
- **KNOWN_LIMIT** scripts/hgk-lane-dispatch.py (the canonical dispatcher) is untracked in git; 'applied' candidates could not be judged as applied by git alone, only by byte compare vs var/ copies — verification attempted: git ls-files returned empty
- **UNKNOWN** hgk-skill convergence patch lane-dispatch-timeout-capture.patch - whether it entered the canonical dispatcher via one of the .bak-x2b/.bak-z2 edits — verification attempted: candidate copy differs from canonical; no patchbook receipt ties the patch to a dated apply record
- **UNKNOWN** r8's skill-slim gate: 115-references count on hgk-governed-execution - whether the >60 WARNING threshold (proposal text) hardens to a FAIL on apply — verification attempted: proposal-only contract; no implemented validator on main
- **UNKNOWN** whether the R10 reconciliation (r10 change records) has already been run to completion for the 20261016 rounds — verification attempted: r10 tasks.md shows 1.1-1.3 [x] but 2.1-2.3 adjudication rows are [ ] at proposal time; on-disk packet has FINDINGS_V3C_INDEPENDENT_VERDICT sign-off but no closing epoch marker foun