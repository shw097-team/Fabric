# VERIFIER BRIEF — independent adversarial check of the R7-0 acceleration artifacts

You are the **independent checker** on the VERIFY/SECURITY lane (Codex CLI, `opencode-go/glm-5.3-flash`).
Your subject is the work produced in the last hour by the orchestrator and three parallel subagents. Be adversarial:
your job is to falsify, not to agree. Claim ceiling: **LOCAL / candidate-only**; your verdict is a candidate for the
Owner — never an acceptance, approval or merge authorisation.

## Write-root rules (a violation voids your own verdict)
- Write **only** under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7/R7_VERIFIER_SWARM/` (create it).
- Never create, modify or delete anything under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/**`
  (contains the guarded subject `R6_DELIVERY/`; reads only) or under any product tree
  (`C:/Projects/Agent_Workspace/PIPD/**`, `C:/Projects/wt-pipd-r7/**`, `C:/Projects/wt-cnv-r7/**` — reads only).
  Copy anything you need to run into your own root first.

## Inspect and try to falsify
1. **WS1 product-side publication (option A, nothing applied).** Remote: `shw097-team/PIPD-LS-SP`, branch
   `evidence/cnv-r7-0-validator-hardening-20261015`, head `eae636d8668027887977a797b20e63899465ad8d`, 16 blobs
   under `evidence/cnv-r7-0/`. Claims to test: (a) the head hash and blob count; (b) **no path under `src/` was
   touched** on that branch; (c) the base-binding claim — that the candidate files' *pre-change* ancestors are
   exactly the blobs of commit `a503efe` while `main` is `dba4b19456777d3b597fdf71480f6423dd974243`; (d) the
   rebase claim — that applying `evidence/cnv-r7-0/delta/validate.py.delta.patch` and `cli.py.delta.patch` to a
   `main` checkout fails while `pipeline.py.delta.patch` applies (re-measure it in your own scratch clone/copy; do
   NOT mutate any existing worktree).
2. **WS3 openspec proposal.** `C:/Projects/Agent_Workspace/HG-KSEOS/openspec/changes/hgk-lane-brief-and-guard-hardening-20261015/`
   (5 files). Claims: it validates strict, it covers all nine findings TF-01..TF-09 by id, each task names file +
   acceptance evidence + applicability (`NOW` / `BLOCKED-owner`), and it contains a NON-CLAIMS section. Re-run the
   validation yourself (`npx openspec validate <id> --type change --strict`) and check the coverage by parsing the
   files — not by reading the author's summary. Report any finding that is missing, mis-scoped or silently widened.
3. **WS4 GSTACK readback.** `WS4_GSTACK_ROLEMAP_READBACK.json` + `WS4_GSTACK_RECEIPT.md`. Its four load-bearing
   claims: (a) only 7 of 19 role-map entries have a role-keyed ACTIVE-SELECTED method, the evidence living in
   `HG-KSEOS/src/hg_kseos/named_methods.py` rather than `config/`; (b) the three gap classes and their members;
   (c) the live routes (VERIFY_SECURITY `openai-codex/gpt-6.1-sol` medium with GLM→DS fallbacks and
   `admission_status: UNPROVEN`; PLAN `opencode-go/glm-5.3-flash`; EXECUTE `opencode-go/deepseek-v4.1-flash`);
   (d) SoD: owner-recorded deviations `SOD006-C2`/`SOD006-C3` exist and the delegation model equals the VERIFY
   arm-B identity, so model/provider independence does not exist. Re-derive each from the live files.
4. **WS5 self-check harness — adversarially.** `selfcheck/round_selfcheck.py` (25,480 B) claims 6/6 PASS.
   **Do not accept a green run as verification of anything but the harness itself.** Read the source and answer:
   (i) can any check pass vacuously (hardcoded expectation, swallowed exception, a PASS printed without comparing
   live bytes, a network result accepted without hashing it)? (ii) do its guard circuits actually refuse a write
   outside the handover root and a git *write* verb — test both from your own root; (iii) does any code path emit
   an acceptance-like claim? Then re-run it and compare the raw output with `selfcheck/SELFCHECK_OUTPUT.txt`
   (say explicitly whether your re-run is byte-identical, equivalent, or different).
5. **Round invariants still holding.** Fabric `main` still `b8ff81043e47e4b652522be34444bf52fcf4d65e` with the R6
   prefix at 581 blobs and `PACKET_MANIFEST.json` sha256
   `27ba42f7cb32d9f490d8897ef0205b0b70cd13bb2b7bc6344e717e5bffbd118b`; Fabric branch
   `evidence/cnv-pipd-ls-sp-20261015-r7` head `7d610e5821b6eddd3969cd537f05efe81fdd54b6` with 212 blobs. Also
   restate the unresolved blocker: the R7-0 patch's base is `a503efe`, so the mutation result (M04/M06/M16 REJECT)
   is unmeasured on any `main`-based rebase.

## Output (write ALL of these, nowhere else)
`…/CNV-PIPD-LS-SP-20261015-R7/R7_VERIFIER_SWARM/`
- `R7_VERIFIER_SWARM_VERDICT.json` — schema `CNV-PIPD-LS-SP-20261015-R7/VERIFIER-SWARM-VERDICT/1`; one row per
  checked claim with `id`, `claim`, `method`, `evidence_path` (your own file), `verdict`
  (`CONFIRMED`, `CHALLENGED`, `UNVERIFIABLE`), `note`; plus `harness_assessment` (the WS5 adversarial answers),
  `unverifiable_claims`, `boundary_violations`, `first_fail`, `overall_verdict` (`PENDING_OWNER` or
  `CHALLENGED`), `claim_ceiling`.
- `R7_VERIFIER_SWARM_RECEIPT.md` — what you ran, exact commands, exit codes, your re-run comparison, and every
  place you disagree.
- `RAW/` — raw stdout/stderr of each command.

## Hard constraints
- No git write command, nothing sent to any outside host, no credential material read or printed (a token file
  exists at `C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt`; you may read it into a variable for
  GitHub API reads and must never print it, put it in argv/URL, or write it anywhere).
- Do not run the 221 acceptance cases; do not claim any Gate PASS; do not upgrade any verdict.
- If a required condition cannot be met, stop and record it as a blocker with the raw error.
