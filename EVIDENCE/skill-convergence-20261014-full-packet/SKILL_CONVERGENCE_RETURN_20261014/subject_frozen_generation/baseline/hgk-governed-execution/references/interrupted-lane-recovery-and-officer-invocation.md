# Interrupted lane recovery, fixture-alignment remedy, CODEX CLI officer invocation

## 1. A lane killed by a host/backend interruption

Symptoms of a background `-Action Write` lane that died mid-run (not still working):
- `maker/launcher-receipt.log` is **0 bytes** (it is written only on normal return), AND
- the expected final deliverable (`maker/RESULT.json`) is absent, AND
- no `codex.exe` in `tasklist`.
A parent log that is merely silent is NOT a stall - check for real artefacts and codex PIDs first.

Consequence: the **sealed front door on :10100 dies with the backend**. Verify with
`curl -s http://127.0.0.1:10100/healthz` (expect `{"status":"ok","sanctioned_pair":"..."}`).
The upstream relay on :10101 survives.

Recovery: re-dispatch the SAME lane idempotently. Put an explicit header in the prompt -
"A PREVIOUS RUN OF THIS SAME LANE WAS INTERRUPTED. Work already on disk: <paths>. Do not start
over." - and make STEP 1 "verify what exists against the spec, repair only if it deviates".
The launcher restarts the front door itself; do not hand-roll the env (CODEX_HOME,
OPENCODEX_HOME, OPENAI_BASE_URL are pinned by `scripts/start-hgk-hermes.ps1` and it refuses a
wrong CODEX_HOME with `ERR_WRONG_CODEX_HOME_INJECTED`).

## 2. Fixture-alignment when a strengthened invariant breaks existing tests

When a new invariant makes canonical tests fail because their fixtures register evidence that is
not real (constant sha256, `TEST_LOG` kinds, placeholder producer/checker, non-existent locator),
the honest remedy is to **align the fixtures**, not to scope the invariant down. Prove it, do not
assert it, by running BOTH against the same candidate shadow:
- unaligned baseline -> must still FAIL (reproduce the blocker verbatim), and
- aligned -> must pass with a documented count.
A fixture-only diff that removes only the old seed constants, changes no assertion and no test
count, and cannot have passed the strengthened primitive honestly is an HONEST_FIX. The officer
must re-derive that verdict itself (diff + re-run), never read the writer's report.
Residual limit to disclose always: aligning fixtures makes them honest, it does NOT enforce
independence (free-text producer/checker, nullable subject_digest).

## 3. Running a CODEX CLI Independent Acceptance Officer

The launcher has no checker action (`Verify|StartOpenCodex|Probe|Hermes|Write`), so send the
officer through `-Action Write` and let the ROLE live in the prompt; it guarantees the front
door, CODEX_HOME and the sanctioned model token.
Pass the prompt as a FILE, not inline - officer prose always contains apostrophes, which break a
single-quoted PowerShell string:

```
pwsh -NoProfile -ExecutionPolicy Bypass -Command "& { \$p = Get-Content -Raw '<abs>/OFFICER_PROMPT.md'; & '<abs>/scripts/start-hgk-hermes.ps1' -Action Write -ModelChain <model> -Prompt \$p }" > <log> 2>&1
```

Make the officer fail-closed and demand re-derivation from disk: rebuild the shadow package
itself, re-run every suite, recompute every sha256, re-diff aligned-vs-baseline, re-read git
state, query the live db read-only (`sqlite3` URI `?mode=ro`). When the checker model is the same
family as the writer, the prompt must state that model diversity is ABSENT and that separation is
PROCESS-only.

## 4. Read-only proof for an officer run

Do not rely on a sandbox flag alone: freeze sha256 of every maker artefact BEFORE the officer runs
(`verify/SUBJECT_DIGESTS.json`), then re-verify after. Zero drift + canonical guard 7/7 unchanged
is the proof the officer wrote only its verdict file. For an inherited dirty baseline, record each
git-modified path with its mtime and assert `mtime <= round_start` - a digest alone cannot
distinguish "modified earlier" from "modified by this round".
