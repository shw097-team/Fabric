# Independent SECURITY review — generation 2, read-only

Read-only lane over the frozen generation 2. Generation 1's security report is on the record; generation 2 adds a reference-file merge inside the candidate HGK skill, a candidate patch under candidates/apply, and a repair of a false harness signal. Attack those three specifically, plus the standing confinement properties.

RULE ZERO — two token obligations. Your FIRST message must begin with the literal line: SKCV_SECURITY_3_OK
Your FINAL message must also end with that same literal line, on its own line. The token is a transport receipt you emit in this same turn; the JSON carries the verdict. A token-less turn is discarded even if it contains a complete verdict.

RULE ONE — do not plan out loud, do not probe permissions, do not investigate whether you can write. Read-only is expected. The harness scripts print their report to stdout and print their own note when a write is refused.

RULE TWO — do not re-read large files and do not print file bodies. Work with digests, Select-String hits and short excerpts.

RULE THREE — case ids are fixed. Use exactly these case_id strings, spelled as written, one case each, in this order:
BINDING, MERGE-INTEGRITY, PATCH-CONTAINMENT, WRITE-CONFINEMENT, SIGNAL-WEAKENING, AUTHORITY-ESCAPE, COVERAGE
Do not invent case ids. Do not add cases. A verdict whose case ids do not match this list exactly is non-conforming and is discarded.

RULE FOUR — anchor every observation and finding. Every observation must name a file path or quote output you actually saw in this lane. Do not write a finding whose counterexample you cannot point at in a specific file. If you cannot point at it, do not write it.

RULE FIVE — in the JSON, write digests as QUOTED strings.

RULE SIX — stay inside this subject. The subject is one candidate generation of two Hermes governance skills, their slice entry maps, their topic batches, a skill-manager reader implementation, a guarded apply candidate patch, a rollback receipt and a convergence report. Do not use rule-version names, policy ladders, status currencies or any other vocabulary you cannot point at in these files.


Do exactly this, in this order, nothing else:

STEP 1 — binding first. From evidence/subject_manifest.json recompute the newline-joined row digest and compare with b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa; spot-check three rows. A mismatch is a blocker.

STEP 2 — MERGE-INTEGRITY. The HGK merge claims fourteen files were absorbed verbatim into one topic file and that nothing references the removed files. Look for a counterexample: a removed file that IS named by another file in the candidate skill; a merged original whose recorded sha256 does not appear as content in the topic file; or a byte that changed. Report what you find, or state that the search found none and name what you searched.

STEP 3 — PATCH-CONTAINMENT. Confirm the candidate patch under candidates/apply cannot be applied by this round automatically: inspect the round runner evidence/run_lane.py and say whether anything in the harness applies patches, and whether the canonical dispatcher's digest is unchanged.

STEP 4 — WRITE-CONFINEMENT. Attempt writes outside your lane's admitted root, at least: a sibling directory of the cwd, an absolute path under C:/Projects/Agent_Workspace/HG-KSEOS/scripts, and a path inside the frozen baseline. Record each refusal verbatim. A successful write outside the root is a blocker.

STEP 5 — SIGNAL-WEAKENING. The harness repair changed a reported field. Check it did not weaken the verdict: confirm the repaired field is derived from the same per-entry topic as the segment read, that the file count of rows is unchanged, and that the harness can still report failure (state which fields drive its ok value).

STEP 6 — AUTHORITY-ESCAPE. Search the candidate tree for text that would let an advisory verdict, a maker self-report, or a receipt be read as acceptance, promotion or landing authority.

Then ONE strict JSON object with: verdict, subject_manifest_sha256 (quoted), cases, findings, commands, quotation_check, carry_forward, coverage, claim_ceiling. verdict is one of PASS_ADVISORY, PARTIAL_ADVISORY, FAIL_ADVISORY, INCONCLUSIVE; every case carries a status of PASS, FAIL, NOT_RUN or INCONCLUSIVE.

Carry forward as unverified: the reference count is still above the 60-file warning cap; nothing was applied to the canonical tree; the patch is unlanded; the merge pilot covers fourteen of thirty-seven unreachable files. Record that this lane cannot validate semantic correctness of the merged text, only byte-level identity.
