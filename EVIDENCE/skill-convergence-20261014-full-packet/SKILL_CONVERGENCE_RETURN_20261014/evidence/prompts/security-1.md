# Independent SECURITY review — frozen subject, read-only, fresh context

You are a fresh Codex CLI checker lane (opencode-go/glm-5.3-flash), READ-ONLY. You are NOT the maker and NOT the PLAN author. Do not modify any subject byte, candidate, baseline, manifest or canonical tree. A mutation during your review invalidates it.

Subject: C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014. Read evidence/subject_manifest.json, evidence/verification_contract.json, evidence/qualification_receipt.json, evidence/execution_bindings.json and evidence/gstack_route_receipt.json first, then attack — do not trust any summary in this brief.

Attack surface you must actually exercise, with real commands and observed results:
1. The writer-qualification claim. It says the Codex native sandbox confines writes to the admitted root and refuses outside-root, subprocess, pre-existing junction and sibling-root writes. Try to falsify it: enumerate every mode and flag the tooling accepts, then attempt a write that the claim says is refused. Report any acceptance path that returns success over a target the claim proved nothing about, and label it ADDITIVELY rather than assuming the default path is the only path.
2. Path handling in the apply validator: relative paths, absolute prefixes, parent traversal, junction and symlink components, unicode and case-folded path collisions, an identifier used as a path component, and a target that is a directory. Report a typed refusal per case, and name any case the host cannot supply.
3. The pre-image and rollback logic: is there a window between digest check and write (TOCTOU)? Can a partial failure leave a target un-restored? Can rollback restore the wrong generation, or overwrite unrelated drift? Test with fixtures only.
4. Authority escape: search the candidate code and the evidence records for any place where an advisory review, a maker self-report, a transport receipt, a checkpoint, or a router final_authority value is treated as canonical acceptance, or where a scope/binding/review gate can be self-granted or widened. Report the exact locator.
5. Credential and secret posture: confirm no credential value, token, key or connection string was recorded in the round. Report the credential-posture verdict as recorded, and state plainly that INCONCLUSIVE is not a pass.
6. Supply chain and environment: the round copied existing host libraries into evidence/offline-test-deps to run tests offline. Verify nothing was installed globally, nothing was fetched from the network into that directory, and the copies are digests of pre-existing host files. Report provenance you could not establish.
7. The diagnostic observer that patches subprocess.run to keep partial capture on timeout: confirm it does not weaken any gate, does not change byte handling, does not alter the canonical dispatcher, and would not let a partial run be scored as a pass. Report any way it could.

Emit ONE strict JSON object with: verdict, subject_manifest_sha256, cases, findings, commands, quotation_check, carry_forward, coverage, claim_ceiling. Verdict is one of PASS_ADVISORY, PARTIAL_ADVISORY, FAIL_ADVISORY, INCONCLUSIVE. Cases carry case_id, status (PASS/FAIL/NOT_RUN/INCONCLUSIVE), evidence_refs, observation. Findings carry id, severity, source_locator, counterexample, maker_repair_required. A blocker or major finding forces a non-PASS verdict. Do not fix anything; report with a repair instruction. State that this is an advisory security rederivation, not canonical acceptance. End with the transport token line given in the dispatch prompt.

## FROZEN SUBJECT BINDING (verify this exact binding)
tree_digest = 9b68418bcbfd230d43d6525752a09d156b37b31fb214eacaf3b5c77b616936cb over 374 files, recorded in evidence/subject_manifest.json together with its inclusion and exclusion rules. Recompute the digest yourself from that file's rows (sha256 of "{sha} {path}" lines joined by newline) and report any mismatch as a blocker, not a footnote. The manifest is the subject; anything outside it is not under review.

## HARNESS SCRIPTS YOU MUST RE-RUN YOURSELF (report exit code and verdict)
- evidence/convergence_check.py
- evidence/check_topic_batch.py avr topic_batch_1.json
- evidence/check_topic_batch.py hgk topic_batch_1.json
- evidence/check_topic_batch.py hgk topic_batch_2.json
- evidence/rollback_drill.py
- evidence/status_check.py
A read-only lane cannot write their report files; that is expected, they print their report to stdout and say so themselves. Do not treat "could not write" as a product failure, and do not treat their printed verdict as your verdict: state where you agree and where you differ.

## ENVIRONMENT FACTS TO RECORD RATHER THAN MISREPORT
- Symlink creation is refused on this host (OSError WinError 1314). Symlink and junction cases are therefore NOT exercisable here; record them NOT_RUN / host-limited, and say which test they belong to.
- The candidate tests need pytest from C:/Users/user/AppData/Roaming/Python/Python311/site-packages on PYTHONPATH; the qualified venv ships no pytest. With that set, tests/tools/ gives 102 passed, 3 skipped (symlink), 1 failed (the same symlink privilege test, which also fails on the unpatched live runtime).

## OPEN ITEMS YOU MUST CARRY FORWARD, NEVER ASSUME VERIFIED
- Only batches 1-2 of the reference themes are consolidated: AVR 7 references in 1 topic, HGK 9 references in 2 topics. Most of HGK's ~114 references and AVR's remaining themes are untouched, so no sprawl-reduction claim is available.
- The candidate reference-file count went UP, not down (AVR 27->30, HGK 119->122) because topic files and remainder files were added.
- No canonical apply, no promotion, no guarded-apply write path, no rollback over drifted bytes has been exercised.
- No independent acceptance exists yet: this lane is the first.
- The live AVR skill has already moved past the round baseline (a curator patch to references/verifier-lane-handover.md, ledger-attributed at 05:49:46Z). Byte-exactness is claimed against the FROZEN baseline generation, not against today's live tree; judge it that way and say so.
- The round's own amply disclosed self-defects: an earlier harness run reported pytest exit 1 because PYTHONPATH was unset; a rollback-drill revision briefly compared the restored tree against the wrong baseline variable. Both were fixed and are recorded rather than deleted. Treat them as records of the harness, not as product failures.

Final literal transport token (not an acceptance): SKCV_SECURITY_1_OK
