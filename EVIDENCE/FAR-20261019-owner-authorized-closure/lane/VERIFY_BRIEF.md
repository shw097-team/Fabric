# VERIFY brief — FAR-20261019 independent verification

Lane: VERIFY_SECURITY, dispatched to the CODEX CLI on `opencode-go/deepseek-v4.1-flash`
(`--force-rank 1 --require-arm opencode-go/deepseek-v4.1-flash`), by **owner order** given mid-round:
the GPT quota was about to run out, so the owner moved this lane off `openai-codex/gpt-6.1-sol`.
Nonce: `CNVEA-FAR019-VERIFY-NONCE-4c8ba1`
Echo the nonce verbatim on its own line prefixed `NONCE-ECHO:` — the receipt is only accepted when the arm
emits it.

## Read this before you start: you are NOT on a different model axis

This round's EXECUTE writer is also `opencode-go/deepseek-v4.1-flash`. By owner order the two lanes now
share one model, so **model-axis independence between maker and checker is absent and must not be claimed
anywhere**. What you still have — and what your verdict therefore rests on — is **process independence**
(you are a separate spawn), **lane independence** (a different lane with its own receipt) and
**evidence-path independence** (you verify from the raw state, not from the writer's receipts). Your value
is in executing each check yourself and being willing to say `DISAGREE` or `UNVERIFIABLE`. A verdict that
merely repeats the maker's claims is worth nothing, and this is the round where that risk is highest.

## Your job

Verify the round's executed actions **independently**: run the command yourself, read the raw output, and
report a verdict. Do not trust the round's receipts; they are the subject, not the evidence.

For each item: `AGREE` / `DISAGREE` / `UNVERIFIABLE`, with the exact command you ran and its raw output.
**If a check cannot be executed from where you are, return `UNVERIFIABLE` and say why — a soft agreement is
worth less than an honest `UNVERIFIABLE`.** Do not fix anything; you are a checker, not a writer.

1. **V1 — the canonical pin.** Read `HG-KSEOS/config/hermes-codex-lane.json`, extract the declared
   executable, and check the declared path exists on disk. Report the declared value and the live binary's
   version/size/sha256. Also confirm the only difference from the retained backup
   (`config-hermes-codex-lane.pre-A1.json`) is that one value.
2. **V2 — the peer merges.** For PRs 6, 8 and 10 in `shw097-team/Fabric`, fetch each PR's state and each
   merge commit's parent list, and confirm the merged head equals the PR's own head and that `main`'s tip
   advanced by exactly those three merges. Report the tip before and after.
3. **V3 — the promoted PR.** Fetch PR #13 and report its draft flag, state and head sha.
4. **V4 — the register.** From `RC1_OPEN_ITEM_UNIVERSE.json`, **recompute** the counts in code (totals, open,
   by authority, by severity) and compare with the file's own `counts` block. Report any disagreement.
5. **V5 — the writer's artifacts.** For each file the EXECUTE lane wrote under `writer/`, run its self test
   yourself and report the raw verdict and return code. Specifically judge whether each test can FAIL:
   identify any test that would pass even if its subject were corrupted, and say so. If a test is vacuous,
   that is a **finding**, not a pass.
6. **V6 (do this LAST, it is the least important) — the closure self-check.** Run the round's self-check and report which injected mutations it
   detected. Then pick ONE of its checks, mutate the underlying input yourself in a temporary copy, and
   report whether the check's predicate actually changes verdict.
7. **V7 — non-claims.** Confirm from the artifacts that the round claims `LOCAL` only and issues no
   acceptance, release or production claim. Quote the line.

DELIVERY OF YOUR REPORT: you run in a READ-ONLY sandbox, so you must NOT try to write a file. Instead PRINT each item as one JSON object on its own line to stdout, formatted `VERIFY-ITEM: {"item": ..., "verdict": ..., "command": ..., "raw_output": ..., "reason": ...}`, immediately after you finish that item, and print a final line `VERIFY-OVERALL: {"overall": ..., "could_not_verify": [...]}`. The harness captures stdout, so printing as you go is what makes your work survive. (The previous instruction named a file path at `lane/VERIFY_REPORT.json`; that path is written by the harness from your stdout, not by you.)
with schema `FAR-20261019/VERIFY-REPORT/1`, one object per item: `{item, verdict, command, raw_output,
reason}` plus an `overall` field and an explicit `could_not_verify` list.


## Failure-mode instruction (added after the EXECUTE lane hit the harness timeout)

The EXECUTE lane on this same relay was still working when it hit the 1500s harness timeout, so its
artifacts exist but its own completion receipt is a TIMEOUT. You must not repeat that failure: **write
your report file after EACH item, overwriting it with the verdicts you have reached so far.** A partial
report left on disk is worth more than a perfect report that never lands. If you notice you are running
long, stop adding depth and make sure the file is current.

## Standing rules

- Read-only with respect to every canonical artifact, every repo, and the previous round's directory. Write
  only your one report file.
- Never re-run a publishing or merging operation to "check" it. Verify by reading state.
- Your verdict is advisory evidence for an external acceptancer; you cannot issue acceptance.
