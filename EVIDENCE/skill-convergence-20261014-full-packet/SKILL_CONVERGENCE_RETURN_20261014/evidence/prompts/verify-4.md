# Independent Acceptance Officer / VERIFY — tag 4, fixed case ids, anchored evidence, read-only, fresh context

Read-only lane over a frozen subject. Two earlier attempts on this work order are on the record: tag 2 produced a complete verdict but ended its turn without the transport token, and tag 3 emitted the token but its verdict body drifted into vocabulary belonging to another task, invented case ids, and contained a finding whose counterexample is not in this subject. This brief adds four rules aimed exactly at those defects. Follow them literally.

RULE ZERO — two token obligations. Your FIRST message must begin with the literal line: SKCV_VERIFY_4_OK
Your FINAL message must also end with that same literal line, on its own line. The token is a transport receipt you emit in this same turn; the JSON carries the verdict.

RULE ONE — do not plan out loud, do not probe permissions, do not investigate whether you can write. Read-only is expected. The harness scripts print their report to stdout and print their own note when a write is refused.

RULE TWO — do not re-read large files and do not print file bodies. Work with digests, Select-String hits and short excerpts.

RULE THREE — case ids are fixed. Use exactly these case_id strings, spelled as written, one case each, in this order:
SUBJECT-BINDING, HARNESS-CONVERGENCE, HARNESS-AVR-BATCH1, HARNESS-HGK-BATCH1, HARNESS-HGK-BATCH2, RECONSTRUCTION-AVR, RECONSTRUCTION-HGK, RECONSTRUCTION-MUTATIONS, C1-EXTRACTION, C2-THEMES, C3-CONSUMER, C4-ROLLBACK, C5-POLICY, COVERAGE
Do not invent case ids. Do not add cases. A verdict whose case ids do not match this list exactly is non-conforming and is discarded.

RULE FOUR — anchor every observation and finding. Every observation must name a file path or quote output you actually saw in this lane. Do not write a finding whose counterexample you cannot point at in a specific file. If you cannot point at it, do not write it.

RULE FIVE — in the JSON, write the manifest digest as a QUOTED string. The previous attempt emitted a bare value and the object could not be parsed.

RULE SIX — stay inside this subject. This subject contains exactly: two Hermes governance skills (adversarial-verification-rounds, hgk-governed-execution), their slice entry maps, their topic batches, a skill-manager reader implementation, a rollback receipt and a convergence report. There is nothing else. Do not use rule-version names, policy ladders, status currencies or any other vocabulary you cannot point at in these files. If a phrase occurs to you that does not appear in the subject, drop it.

Do exactly this, in this order, nothing else:

STEP 1 — SUBJECT-BINDING. From evidence/subject_manifest.json compute sha256 over the newline-joined "<sha256> <path>" row lines with NO trailing separator, and compare with 9b68418bcbfd230d43d6525752a09d156b37b31fb214eacaf3b5c77b616936cb. Quote the exact command and its output. Then spot-check five rows by hashing the named files on disk and comparing digests and byte sizes. A mismatch is a blocker.

STEP 2 — the four harness cases. Re-run each of these read-only scripts and record its exit code and the verdict line it prints:
  HARNESS-CONVERGENCE: evidence/convergence_check.py
  HARNESS-AVR-BATCH1: evidence/check_topic_batch.py avr topic_batch_1.json
  HARNESS-HGK-BATCH1: evidence/check_topic_batch.py hgk topic_batch_1.json
  HARNESS-HGK-BATCH2: evidence/check_topic_batch.py hgk topic_batch_2.json

STEP 3 — RECONSTRUCTION. The claim is that each entry's original SKILL.md is reconstructable byte-exactly from the frozen slice map plus the main file and topic payloads. For both candidates (candidates/avr against baseline/adversarial-verification-rounds/SKILL.md, and candidates/hgk against baseline/hgk-governed-execution/SKILL.md), using candidates/<role>/entry_map.json, concatenate the source ranges in source order and compare with the baseline file's bytes. Record the byte count, the sha256 of both, and the equality. Then run three mutations — RECONSTRUCTION-MUTATIONS — and report whether the map-driven reconstruction detects each: (a) drop one slice, (b) swap the first two slices, (c) flip one byte inside one slice's destination range.

STEP 4 — one line each, anchored:
  C1-EXTRACTION: does the evidence support "the two entries were extracted losslessly"? (entry maps and STEP 3)
  C2-THEMES: does it support "theme references were consolidated losslessly"? (candidates/*/topic_batch_*.json and STEP 2)
  C3-CONSUMER: does candidates/consumer/tools/skill_manager_tool.py and candidates/consumer/phase3_result.json support "the existing consumer was reused rather than duplicated"?
  C4-ROLLBACK: does verification/round-harness/rollback_receipt.json support "a rollback point exists and was exercised"?
  C5-POLICY: does verification/round-harness/convergence_report.json support "no policy, cap or threshold was changed"?
  Answer agree, overstate, or under-specify, with the artifact you read.

STEP 5 — COVERAGE: list what you did not verify and why, including host limits (symlink creation is refused with WinError 1314; the candidate tests need pytest from the user site-packages on PYTHONPATH).

Then emit ONE strict JSON object with: verdict, subject_manifest_sha256 (quoted string), cases, findings, commands, quotation_check, carry_forward, coverage, claim_ceiling. verdict ∈ {PASS_ADVISORY, PARTIAL_ADVISORY, FAIL_ADVISORY, INCONCLUSIVE}. PASS requires no case NOT_RUN or INCONCLUSIVE and no open blocker or major.

Carry forward as unverified, never as done: only batches 1-2 of the reference themes are consolidated (AVR 7 files in 1 topic, HGK 9 files in 2 topics) and the candidate reference-file counts went UP (AVR 27->30, HGK 119->122); nothing was applied to the canonical tree; the live adversarial-verification-rounds skill has already moved past the round baseline via a ledger-attributed curator patch at 05:49:46Z, so byte-exactness holds against the frozen generation only. Preserve every earlier failure record: this round has eleven timed-out lane dispatches, one nonce-less dispatch, and one contaminated verdict on the record, and they are not repaired by your verdict.

State in your output that this is an advisory independent rederivation, not canonical acceptance.
