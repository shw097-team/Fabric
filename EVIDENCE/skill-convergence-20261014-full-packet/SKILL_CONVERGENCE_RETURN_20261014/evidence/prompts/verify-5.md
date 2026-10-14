# Independent Acceptance Officer / VERIFY — generation 2, fixed case ids, anchored evidence, read-only

Read-only lane over the frozen generation 2 of the subject. Generation 1 was frozen at digest 9b68418bcbfd230d43d6525752a09d156b37fb31fb214eacaf3b5c77b616936cb and two GLM checker lanes reported on it. Generation 2 exists because the round applied three bounded remediations after those reports: the HGK reference-sprawl pilot merge, the timeout-capture candidate patch preparation, and a repair of a false signal inside the harness. Your job is to re-derive generation 2 independently.

RULE ZERO — two token obligations. Your FIRST message must begin with the literal line: SKCV_VERIFY_5_OK
Your FINAL message must also end with that same literal line, on its own line. The token is a transport receipt you emit in this same turn; the JSON carries the verdict. A token-less turn is discarded even if it contains a complete verdict.

RULE ONE — do not plan out loud, do not probe permissions, do not investigate whether you can write. Read-only is expected. The harness scripts print their report to stdout and print their own note when a write is refused.

RULE TWO — do not re-read large files and do not print file bodies. Work with digests, Select-String hits and short excerpts.

RULE THREE — case ids are fixed. Use exactly these case_id strings, spelled as written, one case each, in this order:
SUBJECT-BINDING, HARNESS-CONVERGENCE, HARNESS-AVR-BATCH1, HARNESS-HGK-BATCH1, HARNESS-HGK-BATCH2, STUB-SIGNAL-REPAIR, REMEDIATION-HGK-SPRAWL, REMEDIATION-APPLY-PATCH, RECONSTRUCTION-AVR, RECONSTRUCTION-HGK, RECONSTRUCTION-MUTATIONS, C1-EXTRACTION, C2-THEMES, C3-CONSUMER, C4-ROLLBACK, C5-POLICY, COVERAGE
Do not invent case ids. Do not add cases. A verdict whose case ids do not match this list exactly is non-conforming and is discarded.

RULE FOUR — anchor every observation and finding. Every observation must name a file path or quote output you actually saw in this lane. Do not write a finding whose counterexample you cannot point at in a specific file. If you cannot point at it, do not write it.

RULE FIVE — in the JSON, write digests as QUOTED strings.

RULE SIX — stay inside this subject. The subject is one candidate generation of two Hermes governance skills, their slice entry maps, their topic batches, a skill-manager reader implementation, a guarded apply candidate patch, a rollback receipt and a convergence report. Do not use rule-version names, policy ladders, status currencies or any other vocabulary you cannot point at in these files.


Do exactly this, in this order, nothing else:

STEP 1 — SUBJECT-BINDING. From evidence/subject_manifest.json compute sha256 over the newline-joined "<sha256> <path>" row lines with NO trailing separator and compare with b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa. Quote the exact command and its output. Spot-check five rows by hashing the named files on disk. A mismatch is a blocker.

STEP 2 — the four harness cases. Re-run each and record its exit code and verdict line:
  HARNESS-CONVERGENCE: evidence/convergence_check.py
  HARNESS-AVR-BATCH1: evidence/check_topic_batch.py avr topic_batch_1.json
  HARNESS-HGK-BATCH1: evidence/check_topic_batch.py hgk topic_batch_1.json
  HARNESS-HGK-BATCH2: evidence/check_topic_batch.py hgk topic_batch_2.json

STEP 3 — STUB-SIGNAL-REPAIR. Generation 1's harness reported `stub_points_at_topic: false` for every row because it read the batch-level topic, which is absent in the AVR batch shape. The repair reads the same per-entry topic the segment is read from. Confirm from the STEP 2 output that every row now reports true, state how many rows that is, and confirm the harness's headline verdict still depends only on the three substantive fields (segment_matches_claim, baseline_equals_segment, stub_exists) by reading the file.

STEP 4 — REMEDIATION-HGK-SPRAWL. The candidate HGK skill merged fourteen unreachable, small reference files into one new topic file with no stubs. Verify from the candidate tree and from candidates/hgk/remediation_result.json: the reference count before and after, that each merged original is gone as a file, that each original's recorded sha256 still appears as content inside the new topic file, and that skill/SKILL.md was not modified (compare its recorded before and after digests).

STEP 5 — REMEDIATION-APPLY-PATCH. Verify that candidates/apply/patch exists with a unified diff and a reproduction script, that the canonical dispatcher at C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py still has the sha256 the lane recorded before it started, and that the diff's context lines match that canonical file's current content — you cannot apply it in a read-only lane, so check consistency instead of application.

STEP 6 — RECONSTRUCTION. Using candidates/<role>/entry_map.json for both candidates (candidates/avr against baseline/adversarial-verification-rounds/SKILL.md, candidates/hgk against baseline/hgk-governed-execution/SKILL.md), concatenate the source ranges in source order and compare with the baseline bytes: record byte counts and sha256 of both. Then run the three mutations and report whether the map-driven reconstruction detects each: drop a slice, swap the first two, flip one byte.

STEP 7 — one line each, anchored: C1-EXTRACTION, C2-THEMES, C3-CONSUMER, C4-ROLLBACK, C5-POLICY — answer agree, overstate or under-specify, with the artifact you read.

STEP 8 — COVERAGE: what you did not verify and why, including host limits (symlink creation refused with WinError 1314; the candidate tests need pytest from the user site-packages on PYTHONPATH).

Then ONE strict JSON object with: verdict, subject_manifest_sha256 (quoted), cases, findings, commands, quotation_check, carry_forward, coverage, claim_ceiling.

Carry forward as unverified, never as done: the HGK reference population is still above the linter's 60-file warning (it moved from 108 to about 95, so roughly 34 further merges would be needed); only theme batches 1 and 2 are consolidated; nothing has been applied to the canonical tree and nothing has been promoted; the timeout-capture patch is a candidate only; the live adversarial-verification-rounds skill has already drifted past the round baseline through a ledger-attributed curator patch, so byte-exactness holds against the frozen generation only. Preserve every earlier failure record: eleven timed-out lane dispatches, one nonce-less dispatch, one contaminated verdict, and one false-signal harness field are on the record and none of them is repaired by your verdict.

State in your output that this is an advisory independent rederivation, not canonical acceptance.
