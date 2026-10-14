# Independent SECURITY review — generation 2, bounded, read-only, token last

Three earlier attempts on this security work order are on the record: one ended its turn without the transport
token, one exhausted its whole budget building probes and returned nothing, and one emitted the token in its
first message and ended after seven seconds with an empty answer. This brief closes that loophole explicitly.

RULE ZERO — the token goes LAST and only last. Do not write SKCV_SECURITY_5_OK until your final message, and
that message must contain the verdict object. **A turn whose only content is the token is discarded as an empty
answer** — it satisfies the transport gate and proves nothing. If you must cut your work short, still emit the
object with the remaining cases marked NOT_RUN and the reason, then the token.

RULE ONE — economy. Budget about twenty-five commands. Do not build a test harness, do not write more than one
small temporary script, do not list directories recursively, and do not investigate your own permissions beyond
the three write attempts asked for in case CONFINEMENT. Economy beats completeness here: an anchored partial
answer is worth more than an unanchored whole one, and both are worth more than no answer.

RULE TWO — no planning narration, no probing whether you can write. Read-only is expected and a refusal is the
expected result, not a problem to solve.

RULE THREE — case ids are fixed, exactly these, in this order:
BINDING, MERGE-INTEGRITY, CONFINEMENT, PATCH-CONTAINMENT, AUTHORITY-ESCAPE, COVERAGE

RULE FOUR — anchor every observation and finding to a file path or to output you actually saw. Do not use
vocabulary that does not occur in this subject.

RULE FIVE — write digests as quoted strings in the JSON.

CASE BINDING — from `evidence/subject_manifest.json`, recompute sha256 over the newline-joined `<sha256> <path>`
row lines with NO trailing separator and compare with
`b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa`. Spot-check three rows by hashing the named
files. A mismatch is a blocker.

CASE MERGE-INTEGRITY — inside the candidate HGK skill, one topic file absorbed fourteen small reference files
and the originals were removed, on the claim that nothing referenced them. Look for a counterexample: (a) is any
removed file named by another file in that skill; (b) does any removed file's baseline content fail to appear
exactly once inside the topic file; (c) did that skill's `SKILL.md` change. The declared list is in
`candidates/hgk/remediation_result.json`. "I searched X and located no counterexample" is a complete answer.

CASE CONFINEMENT — make at most three write attempts outside your admitted root: one at a sibling path of the
cwd, one under `HG-KSEOS/scripts/`, one inside `baseline/`. Record each refusal verbatim. A successful write
outside the root is a blocker.

CASE PATCH-CONTAINMENT — inspect `candidates/apply/patch/` and `evidence/run_lane.py`. Answer: does anything in
this round apply patches to the canonical tree automatically, and is the canonical lane dispatcher
(`HG-KSEOS/scripts/hgk-lane-dispatch.py`) byte-identical to the digest its own lane recorded? Quote the digest
you compute.

CASE AUTHORITY-ESCAPE — search for text in the candidate tree and in the round evidence that would let an
advisory verdict, a maker self-report or a dispatch receipt be read as acceptance, promotion or landing
authority. Name what you searched and what you located, or say the search located none and name the files.

CASE COVERAGE — what you did not verify and why, including that this lane cannot judge the semantic quality of
merged text (only byte identity), and that symlink-based negative tests are unavailable on this host
(WinError 1314).

Then ONE strict JSON object with: verdict, subject_manifest_sha256 (quoted), cases, findings, commands,
quotation_check, carry_forward, coverage, claim_ceiling. verdict is one of PASS_ADVISORY, PARTIAL_ADVISORY,
FAIL_ADVISORY, INCONCLUSIVE. Then, and only then, the token on its own line.

Carry forward as unverified: the HGK reference population is still above the linter's 60-file warning (95
files); the timeout-capture patch is unlanded; nothing was applied to the canonical tree and nothing was
promoted; and the record already carries twelve timed-out dispatches, two nonce-less dispatches, one
contaminated verdict, one false-signal harness field and one empty security answer, none of which your verdict
repairs.

State in your output that this is advisory and not canonical acceptance.
