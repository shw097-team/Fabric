# Independent SECURITY review — tag 2, narrowed scope, read-only, fresh context

You are a fresh Codex CLI checker lane on the frozen subject. Your previous attempt on this work order ended its turn WITHOUT emitting the transport token after 12 read commands, so this brief is deliberately narrow and starts with a rule that overrides everything else.

RULE ZERO — finish your turn. Never end a turn without the final transport token line. If you cannot finish every case, emit the JSON verdict with the unfinished cases marked NOT_RUN (stating why), then the token. An unfinished but token-bearing answer is useful; a token-less answer is discarded and wasted.

RULE ONE — do NOT plan, do NOT probe permissions, do NOT investigate whether you can write. You are in a read-only lane and that is EXPECTED. The harness scripts print their report to stdout and print their own note when a write is refused. Just run them and record exit codes.

RULE TWO — do not re-read large files you already have context for, and do not print whole files. Work with digests, greps and short excerpts. Your previous attempt consumed 645k input tokens before concluding anything; that budget is gone.

Do this, in this order, and nothing else:
1. Compute the frozen subject digest yourself from evidence/subject_manifest.json (sha256 of the "sha path" lines joined by newline) and compare it with 9b68418bcbfd230d43d6525752a09d156b37b31fb214eacaf3b5c77b616936cb. Record match or mismatch.
2. Run these read-only harness scripts and record exit code plus the verdict line each prints:
   evidence/convergence_check.py
   evidence/check_topic_batch.py avr topic_batch_1.json
   evidence/check_topic_batch.py hgk topic_batch_1.json
   evidence/check_topic_batch.py hgk topic_batch_2.json
3. Four attack cases, each with a real command and the observed result:
   a. WRITE CONFINEMENT — evidence/qualification_receipt.json claims the Codex native sandbox confines writes to the admitted root and refuses outside-root, subprocess, pre-existing junction and sibling-root writes. Try to falsify it: attempt a write outside the admitted root from your lane and report the observed refusal. If the read-only lane makes this untestable here, say so and name the lane mode that would test it.
   b. APPLY VALIDATOR PATH HANDLING — in candidates/apply/guarded_apply.py, probe relative paths, parent traversal, an absolute prefix, a target that is a directory, and a case-folded collision. Report a typed refusal per case, or NOT_RUN with the reason.
   c. AUTHORITY ESCAPE — search (Select-String, bounded to the files you were given) for any place where an advisory review, a maker self-report, a transport receipt, a checkpoint, or a router final_authority value is treated as canonical acceptance, or where a scope/binding/review gate can be self-granted. Report exact locators, or state plainly that you found none in the files searched and name the files searched.
   d. OBSERVER NEUTRALITY — read evidence/observe_dispatch.py and confirm it does not weaken a gate, does not change byte handling, does not alter the canonical dispatcher, and cannot let a partial run be scored as a pass. Report any way it could.
4. Cases you deliberately do not cover (supply-chain provenance of evidence/offline-test-deps, credential-value inspection, rollback TOCTOU depth) are to be listed as NOT_RUN with the reason, not silently dropped.

Then emit ONE strict JSON object with: verdict, subject_manifest_sha256, cases, findings, commands, quotation_check, carry_forward, coverage, claim_ceiling. verdict ∈ {PASS_ADVISORY, PARTIAL_ADVISORY, FAIL_ADVISORY, INCONCLUSIVE}. Cases carry case_id, status (PASS/FAIL/NOT_RUN/INCONCLUSIVE), evidence_refs, observation. Findings carry id, severity, source_locator, counterexample, maker_repair_required. A blocker or major finding forces a non-PASS verdict.

Carry forward as unverified, never as done: only reference batches 1-2 are consolidated (AVR 7 files, HGK 9 files) and the candidate reference-file counts went UP (27->30, 119->122); nothing was applied to the canonical tree; the live adversarial-verification-rounds skill has already moved past the round baseline via a ledger-attributed curator patch at 05:49:46Z, so byte-exactness holds against the frozen generation only; symlink cases are host-limited (WinError 1314).

State in your output that this is an advisory independent rederivation, not canonical acceptance.
