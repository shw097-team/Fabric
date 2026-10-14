# Independent Acceptance Officer / VERIFY — tag 3, token-first, narrowed, read-only, fresh context

Read-only lane over a frozen subject. Your previous attempt on this work order ran out of its execution budget after ten minutes without producing a verdict, so this brief is deliberately narrow and bounded.

RULE ZERO — two token obligations, and they are transport obligations, not the verdict.
  ZEROa: your FIRST message must begin with the literal line: SKCV_VERIFY_3_OK
  ZEROb: your FINAL message must also end with that same literal line, on its own line.
  Why both: the previous attempt on this work order produced a complete, well-formed verdict and then ran out of turn before the trailing token, so the transport gate marked it ERR_NO_ARM_EMITTED_NONCE and the round is required to treat the content as inadmissible. The token is emitted by you, in this same turn, either way — putting it first does not weaken what it proves. The JSON is what carries the verdict, and the round harness re-derives every number independently regardless.
  If you run out of budget, emit SKCV_VERIFY_3_OK first, then the JSON with the unfinished cases marked NOT_RUN and why. A token-bearing partial verdict is useful; a token-less answer is discarded even if it is complete.

RULE ONE — do NOT plan out loud, do NOT probe permissions, do NOT investigate whether you can write. Read-only is expected. The harness scripts print their report to stdout and print their own note when a write is refused.

RULE TWO — do not re-read large files and do not print file bodies. Work with digests, Select-String hits and short excerpts. Your previous attempt spent ten minutes and produced nothing; budget for conclusions, not for reading.

Do exactly this, in this order, nothing else:

STEP 1 — subject binding. From evidence/subject_manifest.json compute sha256 over the newline-joined "<sha256> <path>" lines and compare with 9b68418bcbfd230d43d6525752a09d156b37b31fb214eacaf3b5c77b616936cb. Also spot-check five rows by hashing the files on disk. Record match or mismatch; a mismatch is a blocker.

STEP 2 — re-run these four read-only harness scripts and record each exit code plus the verdict line it prints:
  evidence/convergence_check.py
  evidence/check_topic_batch.py avr topic_batch_1.json
  evidence/check_topic_batch.py hgk topic_batch_1.json
  evidence/check_topic_batch.py hgk topic_batch_2.json

STEP 3 — falsify the round's strongest claim. The claim is: each entry's original SKILL.md is reconstructable byte-exactly from the frozen slice map plus the generated main file and topic payloads. For BOTH candidates (candidates/avr with baseline/adversarial-verification-rounds, candidates/hgk with baseline/hgk-governed-execution), using candidates/<role>/entry_map.json, concatenate the source ranges in source order and compare with the baseline SKILL.md bytes. Then attempt three mutations and report whether the map-driven reconstruction detects each: (a) drop one slice, (b) swap the order of two slices, (c) flip one byte inside one slice's destination range. Report the commands and the observed results.

STEP 4 — claim-versus-evidence for these five headline claims (quote the claim, quote the artifact, then say agree / overstate / under-specify):
  C1 "the two entries were extracted losslessly" — evidence: the entry maps and STEP 3.
  C2 "theme references were consolidated losslessly" — evidence: candidates/*/topic_batch_*.json and the batch checks.
  C3 "the existing consumer was reused rather than duplicated" — evidence: candidates/consumer/tools/skill_manager_tool.py (reader _consult_skill_lint) and candidates/consumer/phase3_result.json.
  C4 "a rollback point exists and was exercised" — evidence: verification/round-harness/rollback_receipt.json.
  C5 "no policy, cap or threshold was changed" — evidence: the policy constants compared against the live runtime in verification/round-harness/convergence_report.json.

STEP 5 — coverage and limits. List what you did not verify and why, including host limits (symlink creation refused with WinError 1314; the candidate tests need pytest from the user site-packages on PYTHONPATH).

Then emit ONE strict JSON object with: verdict, subject_manifest_sha256, cases, findings, commands, quotation_check, carry_forward, coverage, claim_ceiling. verdict ∈ {PASS_ADVISORY, PARTIAL_ADVISORY, FAIL_ADVISORY, INCONCLUSIVE}. Cases carry case_id, status (PASS/FAIL/NOT_RUN/INCONCLUSIVE), evidence_refs, observation. Findings carry id, severity, source_locator, counterexample, maker_repair_required. PASS requires no required case NOT_RUN/INCONCLUSIVE and no open blocker or major.

Carry forward as unverified, never as done: only batches 1-2 of the reference themes are consolidated (AVR 7 files in 1 topic, HGK 9 files in 2 topics) and the candidate reference-file counts went UP (AVR 27->30, HGK 119->122); nothing was applied to the canonical tree; the live adversarial-verification-rounds skill has already moved past the round baseline via a ledger-attributed curator patch at 05:49:46Z, so byte-exactness holds against the frozen generation only. Preserve every earlier failure record: this round has eleven timed-out lane dispatches and one nonce-less dispatch on the record, and they are not repaired by your verdict.

State in your output that this is an advisory independent rederivation, not canonical acceptance.
