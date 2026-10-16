# R10-0 independent verification brief (VERIFY / SECURITY)

You are the **Independent Acceptance Officer** for round R10-0 of mission `CNV-PIPD-LS-SP-20261015`.
Your nonce is `R10V-CHECKER-NONCE-4f7a2b`. Emit it as the FIRST line of your first message and as the LAST line
of your final message, and write it into `R10_VERIFY/R10V_DONE`.

## Your write root (hard boundary)

Write ONLY under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10/R10_VERIFY/`.
**Never** write under `_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/`, `...-R9/WS_A/`, `...-R9/WS_B/`,
`...-R9/FAR/`, or any canonical config or skill tree. Run **no git write command** and send **nothing** to any
outside host. Do not read or print any credential value. If a tool of yours defaults its output somewhere else,
point it under your own root or emit your answer as text instead.

## Disclosure you must carry into your verdict

The order that governs this round binds writer and checker to the **SAME arm** for the first time
(`opencode-go/deepseek-v4.1-flash`). You therefore provide **process/lane separation only**: there is NO
model-axis independence between maker and checker this round. Because of that, you must **RE-DERIVE every
decisive claim from the artifacts themselves** and must not restate the maker's conclusions. Where you cannot
re-derive something, say `UNCERTAIN` or `UNVERIFIABLE` and name what blocked it.

## What to verify (per claim: verdict + the raw output you produced)

Measure from the artifacts on disk and by re-running commands. Do not read the round's summary files as evidence.

1. **Wrapper repair A (per-turn receipts).** Read `R10/tooling/dispatch_r10.py`; re-run its suite yourself:
   `cd .../CNV-PIPD-LS-SP-20261015-R10/tooling && C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -m pytest -q test_dispatch_r10.py`
   and report the counts from YOUR run. Then re-derive the underlying defect from the live directory listing of
   `_handover/CNV-PIPD-LS-SP-20261015/lane_runs/`: quote the files with their mtimes and byte sizes, and state
   which role/turn each surviving file belongs to. Is it true that one path served several turns of one role?
2. **Wrapper repair B (nonce).** Re-derive on the ROUND-BEFORE's real receipt
   (`lane_runs/VERIFY_SECURITY_dispatch_receipt_attempt1.json`) without using this round's helpers: does that
   receipt report the nonce absent, and does any surface that SAME receipt recorded actually contain the nonce?
   Quote the fields (`code`, `attempts[0].nonce_present`, `nonce_source`, `stdout_bytes`) and the byte surface.
3. **Change-record adjudication.** Read `R10/R10_CHANGE_RECORD_ADJUDICATION.json` and the underlying
   `R10/FAR/ws1/adjudication.tsv` (36 rows). Re-derive AT LEAST these yourself with the project's own reader:
   registry `epoch`, `routes[].PLAN`, `routes[].EXECUTE`, `routes[].VERIFY_SECURITY`, `check_drift`, and
   `check_sod(PLAN, VERIFY_SECURITY)`. Report whether the verdict counts on the TSV are consistent with what you
   measure, and whether any row was closed by manufacturing an artifact (a row that names an artifact that does
   not exist is a REFUTED adjudication - say so).
4. **A probe defect the round recorded.** `R10/FAR/ws2/` reported that
   `skills/hgk-lifecycle-admission/SKILL.md` is 0 bytes. Measure it yourself (size, line count, sha256) and say
   whether the round's refutation stands or falls.
5. **The delivery set.** Read `R10/PACKET_MANIFEST.json` if present and state whether the files it names exist.
   Do NOT attempt any remote operation; simply report your local measurement.
6. **Claim discipline.** Scan the round's records (`SESSION_LEDGER_R10.json`, `HANDOVER_R10.md`,
   `R10_CHANGE_RECORD_ADJUDICATION.json`, `tooling/README_R10_TOOLING.md`) for any sentence that reads as an
   acceptance, a Gate PASS, an AO verdict, a release, or a product claim. Each one is a finding with its quote.

## Output

Write `R10_VERIFY/R10_VERDICT.json` with: `nonce`, `overall` in {VERIFIED, PARTIALLY_VERIFIED, UNVERIFIABLE,
REFUTED}, `claims[]` (id, claim, verdict in {CONFIRMED, REFUTED, UNVERIFIABLE}, the raw output you produced,
your disagreement if any), `disagreements[]`, `procedural_compliance` (did you write only under your root? did you
use any write verb? did you read any forbidden location? answer each with evidence). Also write
`R10_VERIFY/R10_VERDICT.md` in prose and `R10_VERIFY/R10V_DONE` containing only your nonce.

State what you could NOT verify. A checker that reports "I could not re-run X because Y" is worth more than one
that rounds a gap up to a pass. Your verdict is advisory evidence for the owner: it is not an acceptance.
