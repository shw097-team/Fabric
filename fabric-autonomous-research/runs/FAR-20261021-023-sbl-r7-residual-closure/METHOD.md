# METHOD — FAR-20261021-023-sbl-r7-residual-closure

Route: `NATIVE_WITH_SELECTED_ARIS` (`FAR_ROUTE_NATIVE_ARIS`), swarm `DEFAULT_ON`, 3 read-only research
lanes, 0 canonical parallel writers. Challenger: `aris` / `research-review`.
Captured: 2026-10-21T05:45:50.426368+00:00

## 1. Why this route
`FAR_CAPABILITY_MATRIX.yaml` maps `task_class = RESEARCH_LITERATURE_REPO` to `NATIVE_WITH_SELECTED_ARIS`:
the question is a decision over a local governed corpus plus two git repositories, with a challenger
review required. The source classes exercised were OFFICIAL_DOC, LOCAL_GOVERNED_CORPUS, GIT_REPOSITORY
and EXPERIMENT_INPUT.

## 2. The swarm split
| Lane | Sub-question | Method | Output |
|---|---|---|---|
| W0 | the complete R6 residual set | programmatic marker extraction over the R6 round tree + a read of the R6 execution status | 16 items, one bucket each |
| W1 | the unmerged candidate branches | per-branch merge-base / ahead-behind / diff --stat / `merge-tree --write-tree` / patch-equivalence / CI check-runs | 49 branch rulings |
| W2 | the legal path for R6-TS06-A | live GitHub API reads + a scratch build + an isolated clean-venv lifecycle | the PR #2 fact set and a 9-step plan |

Workers were read-only. The orchestrator re-derived every decisive fact itself rather than accepting a
worker's summary: the merge-tree probe, the three lane probes, the two-build reproduction, and the
contract acceptance-binding cross-join were all re-measured by the orchestrator.

## 3. Orchestrator re-derivations (the decisive measurements)
1. **Lane availability.** Dispatched all three lanes with `--require-arm` and a nonce carried in the
   prompt. Result: PLAN `openai-codex/gpt-6.1-sol`, EXECUTE `opencode-go/deepseek-v4.1-flash`,
   VERIFY_SECURITY `openai-codex/gpt-6.1-sol`; each `ok=true`, `nonce_present=true`, usage HTTP 200.
   The interactive session model is a different plane and was never treated as a lane binding.
2. **PR #2 mergeability.** `git merge-base origin/main candidate/c3-20261021-v2` = `bedc119...` =
   `origin/main`; ahead/behind = 6/0; `git merge-tree --write-tree` exits 0. Main is an ancestor, so the
   merge is a fast-forward with no conflict.
3. **The reproducibility diagnosis.** `git cat-file blob` on the shipped text files → CRLF=0 in the
   objects; the working tree → CRLF; `core.autocrlf=true`; no `.gitattributes`. The wheel diff between
   two builds of the same commit had 7 differing members, all equal after LF normalisation, and 39
   differing member timestamps.
4. **The fix.** `tools/build_reproducible.py --commit a6bcdd0 --verify` twice: the identical wheel
   sha256 `a161162fa4173460ad9041a9bc83afc31a52b6fc0539f4655f74de3b1147ecf6` and the identical sdist
   sha256 `b147f674ffb2356123b63b6e95d6ad572a91f7364db56e859e562495fdd4a927`.
5. **No product regression.** The candidate suite moved 194 → 200 (`200 passed, 2 skipped`).
6. **Contract binding.** Cross-joining `runtime_readiness[].acceptance_ids` against
   `acceptance[].subject_id` found 4 mismatches, while all 34 acceptance ids do have their own entry.

## 4. Decision rule
A residual enters `executable_this_round` only when (a) the missing thing is our own input, (b) the fix
is a product-side change that improves the delivered artifact, and (c) it needs no Human/Native gate.
Exactly one item qualified. A residual enters `one_action_owner` when a single human act closes it and
that act can be written as one mechanical step. Everything else is `not_closable_this_round`, named
with the specific authority that is missing.

## 5. Challenger review
The `aris` challenger review is in `ResearchSynthesis.md` §4: it asks whether the reproducibility claim
over-reaches, whether closing the wheel item hides a product defect, whether the denominator is honest,
whether the ruling over-reaches into the human gate, and whether the checker is independent. Each
question is answered with the measurement that settles it.

## 6. Reproducing this run
    # the residual inventory
    python SBL/_governance/round-20261021-r7/30_RESIDUAL/.. (the file is a static inventory)
    # the reproduction
    python tools/build_reproducible.py --commit a6bcdd0 --outdir <dir> --verify
    # the lane probes
    python HG-KSEOS/scripts/hgk-lane-dispatch.py --lane PLAN --prompt "<brief including the nonce>" \
        --nonce <token> --require-arm openai-codex/gpt-6.1-sol --json-out <receipt>


## M9 — Classify a lane exit before classifying the candidate
A dispatch that ends `exit=1` is not a FAIL until the cause is classified. The R7 round produced all
three shapes in one day:

  * `ERR_SLOT_POOL_MALFORMED` — the artifact the resolver reads was corrupt (merge-conflict markers in
    a JSON pool). Cause: a concurrent writer. Classification: **environment**, and a governance incident
    in its own right, because a governance artifact that does not parse cannot govern anything.
  * `ERR_LANE_REQUIRED_ARM_ABSENT` — the required arm was not in the pool. Classification: **declaration
    gap**; the fix is the pool, not the retry.
  * `ERR_NO_ARM_EMITTED_NONCE` with a valid usage receipt — the provider failed the turn. Classification:
    **incomplete round**. Preserve the bytes, count nothing, re-run.

The rule: a receipt is classified by its cause, and only a cause in the *product* may become a product
verdict. Everything else becomes a recorded deviation, a re-run, or a control-plane defect to file.

## M10 — Measure the canonical artifact, never a bounded stand-in
A lane probe against a hand-built pool proves the ARM is reachable. It does not prove the BINDING is
what the next dispatch will use. The R7 rebind was measured twice:

  * against a bounded probe pool → proved `opencode-go/minimax-m3.1-flash-free` was serviceable;
  * against the CANONICAL `config/lane-route-slots.candidate.json` → proved the pool file itself now
    selects that arm at rank 1 for PLAN and VERIFY_SECURITY.

Only the second measurement is a binding proof. The gap between the two is where a governance system
fails: a declaration that was measured in a laboratory and never in production is a wish.

## M11 — A conflict between two variants of a binding is a question, not a merge
When two in-flight variants of the same binding disagree, the correct action is to ask the owner which
one governs, then restore that one over the working tree and DROP the other — never merge them, never
pick silently. The R7 case: a concurrent process had rebound the EXECUTE lane to the same model as
PLAN and VERIFY, while the owner had named only two of the three lanes. The variants differed on exactly
one field, and that field was a model identity for the code-writing lane. It was asked, answered, and
recorded.
