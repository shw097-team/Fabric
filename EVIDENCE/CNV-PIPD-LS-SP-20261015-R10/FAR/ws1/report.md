# WS1 adjudication report - two stale open change records vs freshly measured reality

Worker: read-only research agent. Nothing was manufactured to close a row; every verdict cites a measured artifact or command recorded in raw_measurements.json (81 measurement records).

## Counts

| verdict | all rows |
|---|---|
| DONE_MEASURED | 24 |
| OPEN_OWNER | 9 |
| SUPERSEDED | 1 |
| NOT_OWED | 2 |

Per change (36 adjudicated rows):

- hgk-far-remediation-20261016 (25 rows): 20 DONE_MEASURED, 3 OPEN_OWNER, 2 NOT_OWED, 0 SUPERSEDED.
- skill-mainfile-cap-remediation (11 rows T1..T11): 4 DONE_MEASURED, 6 OPEN_OWNER, 1 SUPERSEDED, 0 NOT_OWED.

## Change 1 - hgk-far-remediation-20261016

Rows 5-11 (registry rebind) - all six DONE_MEASURED. The live config/lane-routing-registry.yaml (sha256 38f0436b9bde0599a1c3d5b8b928950450f570548380a90079ca06ff0aba38d2, mtime 2026-10-16 12:36) reads, measured straight from the file: routes[].PLAN.provider=openai-codex (row 6), model=gpt-6.1-sol, reasoning_effort=medium, selection_authority=owner-order-20261016-plan-model-rebind-gpt61-sol, admission_status=ADMITTED with an admission_evidence naming the 2026-10-16 serving probes (row 8); epoch: 21 with a provenance comment recording why (row 10); source_of_routes.revision=21 and sha256=e7be2dea36874f169... equal to the live config/model-lane-assignment.json digest - measured, wholesale consistency preserved. The concrete backup at config/lane-routing-registry.yaml.bak-far-remediation-20261016 sha256 a0d811c48f6063b0... equals the FROZEN_MANIFEST.json config.before entry (row 5). Stale usable_now QUOTA_429_2026-10-15 lives in model-lane-assignment.json (as a retained dated note, not in the registry current value; row 7). declared_conflicts[SOD006-C2] status=OWNER_ORDERED_IN_FORCE (row 9). check_drift() live call returned n=0 findings, exit 0 (row 11). Conformance test tests/test_lane_policy.py - 3 passed, 90 subtests passed, exit 0.

Rows 1-4 (round orchestration) - 1, 2, 3 DONE_MEASURED from the round dir var/FAR-REMEDIATION-AND-CLOSURE-20261016/ (admission.json, KANBAN_SWARM_GRAPH.json, R1_R3_COMPLETION_RECEIPT.json, etc.). Row 4 (validate --strict by the project CLI) was NOT measured: no openspec CLI probe succeeded in this workstream tooling, so NOT_OWED/unverified.

Rows 16-19 (R5 turn shape) - rows 16, 17, 18 OPEN_OWNER; row 19 NOT_OWED (dependent on them). Measured: grep of turn_shape / turn-shape / edit_only in scripts/hgk-lane-dispatch.py returns 0 hits, and the round own ROUND_CLOSURE.json detection D13 says NOT_DELIVERED (canonical_mutations.R5_dispatcher_turn_shape = "NOT LANDED"). No --turn-shape flag exists.

Rows 12-15 (R2 promotion) - all four DONE_MEASURED against var/FAR-REMEDIATION-AND-CLOSURE-20261016/R2_PROMOTION_RECEIPT.json. The PROMOTE set is exactly 4 files; the 3 pre-existing ones have canonical_sha256_before and a .bak-far-remediation-20261016 backup (4th file is new, canonical_sha256_before: null in the receipt - consistent with new file not needing a backup). All 4 live digests re-measured today equal the receipt candidate digests - byte for byte. The receipt itself records workorder_note: InvariantViolation: ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC, remedied late (the independent checker flagged this too) - admitted as a residual, not a closure failure.

Rows 20-25 (verification / closure / publication) - all six DONE_MEASURED as record-presence + digest checks: detection list D01..D16 exists in ROUND_CLOSURE.json (statuses measured row by row; D13 = NOT_DELIVERED which flows into rows 16-19 being open), CHECKER_VERDICT.json (C1..C7 with real DISAGREEs and one UNCERTAIN) submitted by lane VERIFY_SECURITY/V3c (the independent-checker mechanism, not a self-check), ROUND_CLOSURE.json + README + RESIDUAL_INVENTORY present (row 23), PUBLICATION_RECEIPT / REMOTE_READBACK present with sha_match: true, commit b4595e66f9f6ccc81432372cbc701009a4929ab2, PR #8 open (row 24), and SELF_EVOLUTION.md present (row 25).

Rows the worker is unable to independently re-verify beyond artifact presence are limited to: row 1 Spine side-effect (re-admission), row 4 strict CLI (not measured), row 24 full remote tree read-back (receipt digest checked internally, remote not re-fetched by this worker), and the whole-tree canonical-vs-candidate check for row 15 (the round own incomplete enumeration is carried over as-is; this worker re-verified only the 4-file PROMOTE set).

## Change 2 - skill-mainfile-cap-remediation (T1..T11)

Live measured target: the skill lives at C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/hgk-governed-execution/.

- SKILL.md raw bytes = 21026, raw-text len() = 19918, LF-normalized = 19658, sha256 = 60a4d9b3c79fc9e72cd82d587fc8a0c3d2513ac4a2b74ecb3040fb587450d960.
- references/ has 115 entries including a nested topics/ directory (4 files) plus 112 regular files on disk, among them references/adversarial-verification-rounds.md and the change own support-files-index.md.
- The change premise (99,996/100,000, 4-char headroom) is SUPERSEDED: the live main file is 19,658 LF-chars, 80,342 characters of headroom (80.3 percent of the cap). That premise described a pre-SKCV-extraction (2026-10-14) image; the superseding work is the SKCV-20261014 extraction, which moved bytes into references/topics/construction-wave-and-remaining-procedures.md and left its own sandbox entry_map.json (schema SKCV-ENTRY-MAP/1, 6 slices) - this worker re-verified all 6 slices byte-match their recorded sha256 at their recorded live offsets.
- The governing cap constant is MAX_SKILL_CONTENT_CHARS = 100_000 (characters), not bytes, in hermes-agent/tools/skill_manager_tool.py:111 (_validate_content_size at :192; patch path reads target.read_text with encoding utf-8 at :488 and validates new_content at :499). A separate MAX_SKILL_FILE_BYTES = 1_048_576 bytes (:112) is the supporting-file cap. There is NO separate regrowth or ceiling declaration for a future over-cap round - grep for regrowth/ceiling in skill modules returned no hits, and the only repeat-check mechanism is skill_guard.py own size > 100_000 BLOCK (a split-reminder, not a round-crossing gate).
- scripts/skill_guard.py skill_dir post re-measured TODAY: exit 0, PASS, size=19658B refs=7 sections=5.
- 0 dangling references/ pointers in the live SKILL.md as-written. support-files-index.md names 39 of the 112 disk reference files (73 NOT listed), and references/topics/ is entirely absent from the index - T6 is unmet in the strict sense.
- The adversarial-verification-rounds POINTER is absent from both SKILL.md and support-files-index.md (the underlying references/adversarial-verification-rounds.md exists on disk) - T7 unmet.
- No cold-start canary receipt, no future-round ceiling declaration, and no independent checker receipt exist for this change as written (T9, T10, T11 unmet).

### Is the split remedy still necessary given measured headroom?

No, not as an urgency matter. The change Why (4-char headroom, every append blocked) is falsified by measurement: 80,342 LF-normalized chars of headroom exist today. The mechanical split already happened in a different shape (SKCV-20261014, proven by byte-matching slices). What remains genuinely owed is pointer/completeness work, not a further split: the main-file entry_map.json pointer names a file that is not in the live skill dir, support-files-index.md omits 73 reference files, and the adversarial-verification-rounds pointer is missing. Rows T2 (pre-registered manifest for THIS change split), T6, T7, T9, T10 and T11 stay OPEN_OWNER pending an owner ruling on whether SKCV-20261014 landing counts as the replacement remedy for T2-T5 mechanics.

## What this worker could NOT measure (and why)

- openspec validate --strict for change 1 row 4: no openspec CLI invocation was available in this workstream tooling; the row is NOT scored DONE for that reason (scored NOT_OWED/unverified).
- Live re-fetch of the published remote packet (row 24 read the remote back by digest): the local receipt chain (PUBLICATION_RECEIPT.json / REMOTE_READBACK.json) was measured, but no live HTTPS fetch was performed by this worker (networked access out of scope for a read-only worker).
- Whole-var/ tree canonical-vs-candidate diff for row 15: the round own fractional record (access-denied on 757 directories) is carried forward, not re-measured.
- T1 pre-flight baseline as literally written (a pre at the 100k-blocked state) - the measured file is today 19,658-char state, so the row original baseline no longer exists; this is what makes T4 SUPERSEDED rather than DONE.
- The hook scripts in the skills tree were NOT invoked; measurement stayed at file/read-back level.

## Deliverables produced

- raw_measurements.json - 81 measurement records (each with command, raw output, note).
- adjudication.tsv - 36 rows.
- report.md - this file.

Nothing was written outside C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10/FAR/ws1/.
No git write command and no external host contact.
