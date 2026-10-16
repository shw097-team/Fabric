# R9-0 INDEPENDENT VERIFIER BRIEF — re-derive, do not restate

Mission `CNV-PIPD-LS-SP-20261015` · ChangeSet `R9-0-FAR-RESIDUAL-CLOSURE` · HGK project `CNV-R9-FARCLOSURE`
Role: **Independent Acceptance Officer / VERIFY / SECURITY** (checker). Claim ceiling: your verdict is **LOCAL / candidate-only**; it is not an AO acceptance, not a Gate PASS, not a release decision.

FIRST LINE OF YOUR FIRST MESSAGE and LAST LINE OF YOUR FINAL MESSAGE must both be exactly:
`R9V-CHECKER-NONCE-5c1d84`

## Rules of this turn
- **Write ONLY under** `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/R9_VERIFY/`. Never write
  into the round's evidence roots (`WS_A/`, `WS_B/`, `WS_B2/`, `FAR/`), never into any skill tree, never into
  `_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/`, and never run a git write command or send anything outside.
- **Do NOT read the round's own report/synthesis files** (`R9_MISSION_PLAN.md`, `R9_LEDGER.json`,
  `R9_SYNTHESIS*`, `SELF_EVOLUTION_R9*`, any `*_RECEIPT.md`). Re-derive each claim below from the artifacts
  themselves. If you cannot re-derive a claim, say so with a typed code — a restatement of the round's prose is
  worth nothing here.
- Native `C:/...` paths only when calling native tools. Interpreter:
  `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.

## Claims to re-derive (report PASS / FAIL / UNVERIFIABLE per item, with the raw output you produced)

1. **The validator adaptation is real, bounded and non-weakening.** In `C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt`
   (base commit `dba4b19456777d3b597fdf71480f6423dd974243`): (a) confirm only `src/pipd_ls_sp/validate.py` carries
   the round's two new guards — the frozen-context derivation and the `risk_guard` mapping guard — and quote the
   lines; (b) run the two named tests (`test_real_trace_link_is_legal_beside_its_endpoints`, `test_cli_smoke_runs`)
   and require both to pass; (c) run the mutation probes `M04`, `M06`, `M16` (through the round's runner under
   `_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/RUNNERS/probe_mutations.py`, or re-derive the mutation yourself) and
   require `observed=REJECT` for each. A pass WITHOUT the three refusals is a FAIL — that would mean the hardening
   was relaxed rather than adapted.
2. **The successor candidate's gate result.** Run the round's harness
   (`_handover/CNV-PIPD-LS-SP-20261015-R8/ws_a_skill_slim_regression.py`) with
   `--subject C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/CANDIDATE_V2`
   `--live C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/software-development/hgk-governed-execution`
   `--out <your root>/harness_v2_yourrun.json`. Report every check's verdict and the C6 counts. Also state what
   the harness's own recorded `subject_live` field says versus the `--live` value you passed — and whether that is
   a defect in the harness or in this round's reading of it.
3. **The canonical skill tree state.** Report, from the LIVE tree (not from any round record): whether the apply
   happened at all, the byte size and sha256 of `SKILL.md`, the number of files under `references/`, and whether
   the reference `product-branch-write-set-gates.md` is present with sha256 `e59968d8fb23f18a…`. If a receipt in
   `WS_B2/` claims an apply, check the tree against that claim and report any disagreement.
4. **The package and the record corrections.** Recompute the PKG digest
   (`…/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md`) and state whether it equals the owner's
   approved `96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f`. Then check, in the PKG's own bytes:
   that it contains no 100000/100,000 size cap; and that `ACC-RQ06` names AVR/10-piece and HGK/6-piece
   reconstruction. Quote what you find, including anything that contradicts the round's reading.
5. **The registry claim.** Run the repo's own drift check (`HG-KSEOS`, `PYTHONPATH=src`, its venv python:
   `lane_policy.check_drift(registry=load_registry())` — the keyword is required) and report the result. Then state
   the canonical top-level route for `PLAN` and for `VERIFY_SECURITY`, and whether either agrees with the
   2026-10-16 mandate (PLAN and VERIFY/SECURITY = GPT 6.1 SOL-MEDIUM via OpenAI OAuth).
6. **The FAR artifact set.** In `Fabric/FABRIC/fabric-autonomous-research/runs/FAR-20261016-012-r9-residual-closure/`:
   inventory the artifacts, and verify that every `evidence_ref` named in `ClaimLedger.tsv` resolves to a record
   that exists in the set or to an addressable path. Report any dangling reference.
7. **The lane attribution.** Read the dispatch receipt(s) under
   `_handover/CNV-PIPD-LS-SP-20261015/lane_runs/` and report, per attempt: `rank`, `provider`, `model`, `exit`,
   `seconds`, `nonce_present`, and the receipt's `code`. State which arm served each turn, and whether any turn
   was served by an arm other than the one this round's dispatcher pinned.

## Output

Write `R9_VERIFY/R9_VERDICT.json`: one row per claim above with `claim_id`, `verdict`
(`CONFIRMED` / `REFUTED` / `UNVERIFIABLE`), `how_you_derived_it` (command + the essential raw output),
`disagreement` (a typed note when your measurement differs from the round's), and a final
`overall` plus `claim_ceiling`. Also write `R9_VERIFY/R9_VERDICT.md` (the same content in prose) and
`R9_VERIFY/R9V_DONE` containing only your nonce.

Then answer in your final message: per-claim verdicts, every disagreement with its raw evidence, and your nonce.
