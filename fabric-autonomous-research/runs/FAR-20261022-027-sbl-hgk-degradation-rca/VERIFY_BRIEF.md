# VERIFY BRIEF — VERIFY_SECURITY lane (CODEX CLI, opencode-go/deepseek-v4.1-flash, rank 4)

You are the INDEPENDENT CHECKER for a governed FAR round. You did not write the artifacts and you may not
trust them. Your job is to falsify them where they are falsifiable. You are read-only: do NOT modify any file
in this directory or any repository. Your verdict is the text you print; the dispatcher persists your stdout.

## Context (do not re-derive, verify it)
Round: ROUND-SBL-HGK-RCA-20261022 under HG-KSEOS admission
`REQ-HGK-PRJ-SBL-HGK-RCA-20261022` (FROZEN) / `TS-req-hgk-prj-sbl-hgk-rca-20261022` (ADMITTED) /
`WO-TS-REQ-HGK-PRJ-SBL-HGK-RCA-20261022-EXEC` (writer = codex-cli/opencode-go/minimax-m3.1-flash-free).
The writer lane's product is the six files below; a prior witness lane produced `evidence/W1..W4`.

Writer's deliverables to audit (your cwd):
- `ResearchSynthesis.md`
- `FINDINGS.tsv`
- `VERDICT.json`
- `DEVIATIONS.tsv`
- `ProposedEvolution.yaml`
- `ResearchHandoff.yaml`
Inputs / evidence: `OWNER_MANDATE.txt`, `ResearchRequest.yaml`, `ResearchPlan.yaml`,
`ROUTE_DECISION.json`, `GSTACK_ROUTE_DECISION.json`, `evidence/W1_fabric_integration.md`,
`evidence/W2_base_drift.md`, `evidence/W3_capability_probe.md`, `evidence/W4_performance_delta.md`.

The admitted acceptance criterion (what PASS means):
"every root-cause claim carries a re-derivable locator this lane can open itself; each capability question is
answered with a measured state, not from prose; no claim exceeds the report's stated claim ceiling."

## Audit items — return one line per item, `A1..A9 PASS|FAIL — <one sentence with the locator you opened>`

- **A1** Every file in the deliverable list exists, is non-empty, and parses (`python -c "import json..."` for
  `.json`, a TSV column-count check for `.tsv`, a YAML parse for `.yaml`).
- **A2** `FINDINGS.tsv` ids are contiguous F1..Fn with no gaps/dupes, and every `evidence` cell points at a
  path that exists (you may check existence; do not require it to be a line you can open if it names a
  directory-level receipt).
- **A3** Claim-ceiling discipline: `VERDICT.json.claim_ceiling` exists, and no sentence in
  `ResearchSynthesis.md` claims acceptance, release, native integration, installation, or a completion
  percentage. Quote any violating sentence.
- **A4** The four owner questions (Q1 Fabric integration / Q2 current-base upgrade / Q3 why worse / Q4 seven
  capability surfaces) are each answered explicitly in `ResearchSynthesis.md` §2..§5 AND in
  `VERDICT.json.answers`. An evasive answer is a FAIL.
- **A5** Performance honesty: the artefacts must not assert a time/money/completion premium. Cross-check
  against `evidence/W4_performance_delta.md`. Any invented duration, percentage or cost figure is a FAIL.
- **A6** Capability honesty: `VERDICT.json.capability_states` must not upgrade W3's states — OPENSPEC=FAIL and
  SELF_*=FAIL must stay FAIL; KANBAN/GSTACK/SUB_AGENTS stay PARTIAL; SWARM/CODEX_CLI stay PASS.
- **A7** Model-plan disclosure: `VERDICT.json.mandate` states MANDATE vs OBSERVED for all three lanes and
  discloses that the pool's declared rank-1 for PLAN/VERIFY is `openai-codex/gpt-6.1-sol` while this round
  pinned the owner's arms. Missing disclosure = FAIL.
- **A8** Re-derive THREE of the report's numeric claims yourself, with your own commands, and say whether each
  reproduces. Suggested (run them from `C:/Projects/Agent_Workspace/HG-KSEOS` / `.../Fabric`):
  - `git -C C:/Projects/Agent_Workspace/HG-KSEOS rev-list --count b22706e..HEAD` (expect 18)
  - `git -C C:/Projects/Agent_Workspace/HG-KSEOS rev-list --count ec58a0b..HEAD` (expect 147)
  - `openspec validate --all` in HG-KSEOS (expect 37 passed / 2 failed) and in SBL (expect 1 passed)
  - board backlogs: `hermes kanban --board sbl-r14-full-product stats` (expect ready 23 / done 8)
  A number that does not reproduce must be reported as a FAIL against the exact claim.
- **A9** SoD reconciliation: the report must state that SBL's "self-accept" collides with HG-KSEOS's
  `ERR_WORKORDER_SELF_REVIEW` (writer == checker refused) and that self-DETECT and self-REPAIR survive as
  legitimate while self-ACCEPT must be an independent lane. Silence or a claim that self-acceptance is
  available = FAIL.

## Finish with exactly these three lines, in this order, and nothing after them

```
VERDICT: PASS|FAIL
UNVERIFIED: <comma-separated audit ids you could not check, or NONE>
REASON: <one or two sentences naming the single decisive reason for the verdict>
```

Rules: PASS requires every A-item PASS and `UNVERIFIED: NONE`. Any FAIL or any UNVERIFIED item forces
`VERDICT: FAIL` — "could not verify" is a FAIL, never a third state. Do not fix anything, do not write files,
do not run git commands that mutate. Do not restate the writer's prose as your evidence: cite what YOU opened.
