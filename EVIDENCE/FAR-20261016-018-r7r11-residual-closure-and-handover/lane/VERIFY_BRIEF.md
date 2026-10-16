# VERIFY BRIEF — FAR-20261016-018 (independent checker, cross-model, re-derivation)

You are the independent verification lane. Your job is to **falsify** this round's claims, not to agree with
them. Report DISAGREE wherever your own re-derivation differs, and report UNVERIFIABLE rather than PASS when
you cannot actually run something.

NONCE: your FIRST line of output must be exactly `CNVEA-FAR018-VERIFY-NONCE-2b6e44` and your LAST line must
repeat it.

## You must not write to the subject

The artifacts you verify are guarded. Do not modify, move, delete or create anything under
`C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover/` outside
`lane/`, and do not modify anything under
`C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/`.
You may write throwaway files only under a temp dir you create yourself (use `$TMPDIR`), and you must remove
them before you finish. If you must run the writer's harness, run it with its own temp root so it cannot
touch the guarded tree.

Python: `C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe` (use `-B`). Windows; your shell is
bash (git-bash) — pass native `C:/...` paths to native programs.

## Claims to re-derive (each needs a verdict, a raw command, and the raw output)

**V1 — residual register counts.** From `W1_RESIDUAL_UNIVERSE.json`, independently recompute: total items,
the per-kind counts, the per-authority counts, and the count of items whose authority is
`agent-executable-now`. Compare to the file's own `counts` object AND to the numbers asserted in
`FAR_RULING.md` §0. Report any mismatch, including a mismatch between the file and the ruling.

**V2 — the isolation harness is not vacuous, and its cleanup is real.** Read
`writer/checker_isolation_probe.py`. Then (a) run it with `--self-test` and confirm the mutated case is
detected (it must report failure for the mutation); (b) run a normal invocation and inspect the receipt it
prints — confirm it contains the three booleans, the raw stderr of the denied attempt, and an explicit limit
statement that the denying identity can lift its own ACE; (c) independently confirm the deny actually blocks:
after the harness finishes, assert that no probe directory and no deny ACE it created still exists (or that
it cleaned up in its `finally`). Quote evidence. If the harness could pass with the deny step skipped, that
is a FAIL — say so.

**V3 — the de-vacuumed check can actually fail.** Read `writer/self_check_v2.py`. Run it, then run its
negative-control mode. Confirm the verdict it computes CHANGES between the unmodified input and the
disclosure-stripped input. A check whose result cannot change is vacuous: report FAIL.

**V4 — the reconstructed index is honest about being partial.** Independently recompute, with your own code,
the sha256 of `bytes[offset:offset+length]` for every `SKCV-POINTER` target recorded in
`writer/entry_map.json`, resolved against the skill dir
`.../LocalCache/Local/hermes/skills/software-development/hgk-governed-execution`. Report the match count.
Then confirm the artifact declares its coverage as PARTIAL and names what it does not cover. Finally, verify
the verifier can fail: perturb a recorded digest and confirm the tool aborts.

**V5 — the vacuity finding about the PREVIOUS round is true.** Open
`C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/self_check.py`. Locate the S8b
check. Confirm or refute, by quoting the source lines, that its success argument is a literal `True` and
that a computed variable near it is never used. This is a claim that a previous round's green was partly
vacuous — treat it adversarially in both directions: if the code actually computes its verdict, say so.

**V6 — claim ceiling.** Search every JSON and Markdown artifact in the round dir (excluding `lane/attempts/`)
for verdict-bearing strings. Report any string that asserts or implies: closure of `R7-03`/`EIA-20261016-02`,
an immutable checker boundary, validator acceptance, runtime certification, convergence, production, or an
external acceptance. Also confirm the three fields `full_convergence_verdict`, `production_verdict` and
`canonical_AO_acceptance` are present in the ruling's artifacts and carry their non-achieved values.

**V7 — the guard false-positive claim.** In `W2_DEFECT_DOSSIER.json`, D0 asserts that a guarded write was
refused with a specific error and that the orchestrator then persisted the file from the lane's transcript.
Check what you can from artifacts: does the dossier contain a raw error string for that refusal, and does
the narrative correctly distinguish "the lane measured it" from "the orchestrator persisted it"? Report what
you cannot verify.

## Output

Print a single JSON object as your final output (after the closing nonce line is not required to be JSON):
`{"verdicts":[{"id":"V1","verdict":"AGREE|DISAGREE|UNVERIFIABLE","claim":"","how_re_derived":"","raw":""}],
"overall":"AGREE|DISAGREE|PARTIAL","disagreements":[],"could_not_verify":[]}`
Rules: an item you could not run is UNVERIFIABLE, never AGREE. Your verdict is about the round's artifacts,
not about the underlying engineering problems. Do not claim the round is externally accepted.
