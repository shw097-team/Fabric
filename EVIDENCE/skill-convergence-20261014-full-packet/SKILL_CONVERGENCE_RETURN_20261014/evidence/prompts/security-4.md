# Independent SECURITY review — generation 2, bounded, read-only

Read-only lane over the frozen generation 2 of the subject. Two earlier attempts on the security work order are on the record: one ended its turn without the transport token, and one burned its whole budget building elaborate probes and produced no verdict at all. This brief is deliberately small. Answer the five questions below with reads and at most three write attempts, then emit the verdict.

RULE ZERO — two token obligations. Your FIRST message must begin with the literal line: SKCV_SECURITY_4_OK
Your FINAL message must also end with that same literal line, on its own line.

RULE ONE — economy. Budget yourself at about twenty-five commands total. Do not build a test harness, do not
write more than one small temporary script, do not enumerate directories recursively, and do not investigate
your own permissions beyond the three write attempts asked for in case 3. If you are running long, emit the JSON
with the unfinished cases marked NOT_RUN and the reason, then the token.

RULE TWO — no planning narration and no probing whether you can write. Read-only is expected and a refusal is the
expected result, not a problem to solve.

RULE THREE — case ids are fixed, exactly these, in this order:
BINDING, MERGE-INTEGRITY, CONFINEMENT, PATCH-CONTAINMENT, AUTHORITY-ESCAPE, COVERAGE

RULE FOUR — anchor every observation and finding to a file path or to output you actually saw. Do not write a
finding whose counterexample you cannot point at. Do not use vocabulary that does not occur in this subject.

RULE FIVE — write digests as quoted strings in the JSON.

Do exactly this:

CASE BINDING — from `evidence/subject_manifest.json`, recompute sha256 over the newline-joined `<sha256> <path>` row
lines with NO trailing separator and compare with
`b050a0256e57f5e6958956874d3f4c4d63ac38c7cbe46489990183a16b48e8fa`. Spot-check three rows by hashing the named
files. A mismatch is a blocker.

CASE MERGE-INTEGRITY — the candidate HGK skill absorbed fourteen small reference files into one topic file
(`skill/references/topics/lane-bootstrap-and-guard-notes.md`) and removed the originals, and the claim is that
nothing referenced them. Look for a counterexample: (a) is any one of the removed files named by another file in
the candidate skill; (b) does any removed file's baseline content fail to appear exactly once inside the topic
file; (c) did `skill/SKILL.md` change. Read `candidates/hgk/remediation_result.json` for the declared list. Report
what you searched and what you found; "I searched X and found none" is a complete answer.

CASE CONFINEMENT — make at most three write attempts outside your admitted root, one each: a sibling path of the
cwd, a path under `C:/Projects/Agent_Workspace/HG-KSEOS/scripts/`, and a path inside `baseline/`. Record each
refusal verbatim. A successful write outside the root is a blocker.

CASE PATCH-CONTAINMENT — inspect `candidates/apply/patch/` and `evidence/run_lane.py`. Answer: does anything in this
round apply patches to the canonical tree automatically, and is the canonical dispatcher
(`C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py`) byte-identical to the digest its own lane
recorded before it started? Quote the digest you compute.

CASE AUTHORITY-ESCAPE — search for text in the candidate tree and in the round's evidence that would let an
advisory verdict, a maker self-report, or a dispatch receipt be read as acceptance, promotion or landing
authority. Name what you searched and what you found, or state that the search found none and name the files you
searched.

CASE COVERAGE — what you did not verify and why, including that this lane cannot validate the semantic quality of
merged text, only byte identity, and that symlink-based negative tests are unavailable on this host (WinError 1314).

Then ONE strict JSON object with: verdict, subject_manifest_sha256 (quoted), cases, findings, commands,
quotation_check, carry_forward, coverage, claim_ceiling. verdict is one of PASS_ADVISORY, PARTIAL_ADVISORY,
FAIL_ADVISORY, INCONCLUSIVE.

Carry forward as unverified: the HGK reference population is still above the linter's 60-file warning (95 files);
the timeout-capture patch is unlanded; nothing was applied to the canonical tree and nothing was promoted; and the
record already carries twelve timed-out lane dispatches, two nonce-less dispatches, one contaminated verdict, one
false-signal harness field and one budget-exhausted security attempt, none of which your verdict repairs.

State in your output that this is advisory and not canonical acceptance.
