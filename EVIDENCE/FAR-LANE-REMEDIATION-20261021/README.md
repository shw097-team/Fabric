# FAR-LANE-REMEDIATION-20261021 — publication summary for external acceptance

**Repository:** `shw097-team/Fabric` (branch `pub/far-lane-remediation-20261021`)
**Subject:** HG-KSEOS lane/model declaration remediation — registry epoch 22 → 24
**Control plane:** HG-KSEOS (sole control plane); canonical Hermes = governed Runtime/Orchestration Plane
**Claim ceiling:** `CANDIDATE_ONLY` — mirrored governed artefacts for external acceptance. Local
verification is not independent acceptance; publication is not release.

## What an external engineer can verify from this repository alone

1. **The route contract itself** — `implementation/lane-routing-registry.yaml`,
   `implementation/model-lane-assignment.json`, `implementation/lane-route-slots.candidate.json`,
   `implementation/hermes-codex-lane.json` are the exact bytes that the governance registry
   projects. Their digests are in `PACKET_MANIFEST.json`.
2. **The change that produced them** — `implementation/IMPLEMENTATION_DIFF.patch` (the
   `AGENTS.md` + owner-chain-oracle diff of the epoch-23 alignment), `IMPLEMENTATION_DIFFSTAT.txt`,
   and the two apply scripts (`apply_far_remediation.py`, `apply_closure.py`) with their receipts
   (`evidence/apply_receipt.json`, `evidence/apply_receipt.json` for the closure round).
3. **The lane receipts that prove which arm actually served** — `lane_receipts/` holds the raw
   dispatcher receipts: the EXECUTE turn served by `opencode-go/minimax-m3.1-flash-free`
   (`required_arm == served_arm`), the earlier `opencode-go/deepseek-v4.1-flash` turn, the
   `openai-codex/gpt-6.1-sol` VERIFY turn, and the AO attempt that did **not** complete.
4. **The self-check gate** — `implementation/selfcheck_epoch24.py` and
   `evidence/selfcheck_receipt.json` (GATE_PASS 20/20, re-runnable; prints its own claim ceiling).
5. **The research that drove the closure** — `research/RESEARCH_GAPS.md` (11 gaps classified A/B/C),
   `research/RESEARCH_CANDIDATES.md` (candidate-merge adjudication), `research/RESEARCH_DOCUPGRADE.md`
   (file-level upgrade list with line numbers).
6. **The diagnosis that started it** — `round_documents/FAR_LANE_VERSION_MIX_REPORT.md` and
   `evidence/EVIDENCE_DIGEST.md` (the cross-surface contradiction table and the mechanism analysis).
7. **The round-2 closure** — `implementation/apply_transport_fix.py` +
   `evidence/apply_receipt_r2.json` (the transport-vocabulary repair and its conformance test),
   `implementation/hgk-lane-dispatch.py` (the dispatcher, including the Windows-usable scratch root
   that lets a checker lane execute a test suite), `IMPLEMENTATION_DIFF_R2.patch` /
   `IMPLEMENTATION_DIFFSTAT_R2.txt` (the epoch-24 diff), and `lane_receipts/EXECUTE_transport.json`
   + `lane_receipts/VERIFY_acceptance.json` (the two lane receipts that carry the repair).

## Current declared route (epoch 24)

| Lane | Rank-1 provider/model | Engine | Transport id | Fallbacks |
|---|---|---|---|---|
| PLAN | `openai-codex/gpt-6.1-sol` (medium, OAuth) | hermes | `gpt-6.1-sol` (BARE) | `opencode-go/glm-5.3-flash`, `opencode-go/deepseek-v4.1-flash` |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` | codex-cli | `opencode-go/deepseek-v4.1-flash` | `openai-codex/gpt-6-luna` (bare `gpt-6-luna`), `nvidia/deepseek-ai/deepseek-v4.1-flash` |
| VERIFY_SECURITY | `openai-codex/gpt-6.1-sol` (medium, OAuth) | codex-cli | `gpt-6.1-sol` (BARE) | `opencode-go/glm-5.3-flash`, `opencode-go/deepseek-v4.1-flash` |

### Round 3 (`FAR-CLOSURE-20261021-R3`) — the published contract was not reproducible from the repository

An independent read of the round-2 output found a defect that no local gate could see: this round
committed `tests/test_lane_policy.py` and `scripts/hgk-lane-dispatch.py`, and **both import
`hg_kseos.lane_policy` / `lane_admission` / `lane_route_resolver` / `role_binding` — none of which
were tracked in git**. A clean detached worktree at the round's own HEAD could not import them:

```
clean checkout: ImportError: cannot import name 'lane_policy' from 'hg_kseos'
pytest tests/test_lane_policy.py -> ERROR during collection (1 error)
```

So the tracked tree carried the **tests** and the **dispatcher** while the modules they depend on
lived only in the working copy. A lane that cannot be rebuilt from a clean checkout is a lane that
cannot be handed over.

**Fixed** in commit `051d574` (HG-KSEOS): the measured closure — four runtime modules
(`src/hg_kseos/lane_policy.py`, `lane_admission.py`, `lane_route_resolver.py`, `role_binding.py`),
four lane scripts (`scripts/hgk-lane-guard.py`, `runtime_role_binding_assert.py`,
`hgk-exec-model-frontdoor.py`, `hgk-artifact-gate.py`) and one test
(`tests/test_lane_dispatch_ao_guard.py`) — is now tracked. The closure was **re-derived**, not
guessed: every local import of every candidate was resolved against `git ls-files` first, so no
candidate pulls in an untracked dependency; no candidate carries a credential-shaped literal; no
candidate hardcodes a machine-absolute path.

**Verification, by the independent AO lane, from the committed bytes only**
(`lane_receipts/AO_landing2.json` — the checker extracted the tree with `git archive HEAD` and
worked inside it, so nothing from the working copy could leak in):

| claim | result |
|---|---|
| all nine files present in the extracted HEAD tree | PASS (none missing) |
| `from hg_kseos import lane_policy, lane_admission, lane_route_resolver, role_binding` | `IMPORTS_OK`, exit 0 |
| `pytest tests/test_lane_policy.py -q` in the extracted tree | exit 0, `5 passed, 90 subtests passed` |
| `config/` present in the extracted tree; registry `epoch: 24` | PASS |
| epoch / drift read from the extracted tree | `EPOCH 24`, drift non-empty (see below) |
| the suite is self-contained from committed bytes | PASS — only an external venv+pytest is needed |

The AO lane also disclosed, without being asked, that the drift it read in the **extracted** tree is
non-empty (three `PROJECTION_DEBT` warnings about `config/hermes.json`) whereas the main working
tree reads `[]`. That difference is real and is **not** repaired here: the committed
`config/hermes.json` still describes the `var/hermes-v020` isolated home and the old model name
`deepseek-v4-flash`, and the corrected version exists only as an **uncommitted** working-tree edit
left by an earlier session. Committing it would land an unreviewed, out-of-scope rewrite (it also
repoints `executable` at the `hermes.exe` trampoline) — so it is recorded as an open item below
rather than silently shipped. See ledger row `K-27`.

### The transport vocabulary is a second, per-provider vocabulary — read this before trusting a lane

A pool entry carries **two** identities, and they are not the same thing:

- `provider` / `model` — the **governance identity**: what the lane is *declared* to be.
  This is what the receipt gate compares against, and it is what `check_drift()` checks.
- `transport_model` — the **transport vocabulary**: the string actually handed to the Codex-CLI
  transport. This vocabulary is **per-provider**:
  - `openai-codex` **REQUIRES the bare id** (`gpt-6.1-sol`).
  - `nvidia` **REQUIRES** `<provider>/<model>`.
  - `opencode-go` accepts bare or qualified.

Measured on the live relay (`127.0.0.1:10101`, 2026-10-21):

| requested id | result |
|---|---|
| `gpt-6.1-sol` | **200** |
| `openai/gpt-6.1-sol` | **200** |
| `openai-codex/gpt-6.1-sol` | **400** `Model is unavailable` |
| `openai-codex/gpt-5.6-sol` | **400** `Model is unavailable` |
| `gpt-6.1-sol-high` | **400** `not supported when using Codex with a ChatGPT account` |

A qualified `openai-codex/<model>` is routed by the relay to the **default provider**, which does not
serve it. The lane was therefore *correctly declared but structurally un-runnable* — which is the
mechanism behind "gpt-6.1-sol sometimes works": it worked whenever the id reached the backend bare,
and failed whenever a provider-qualified spelling was used. `transport_vocabulary` in
`implementation/lane-route-slots.candidate.json` records this rule and its evidence, and
`tests/test_lane_policy.py::TestOpenaiTransportVocabulary` now fails if any `openai-codex` entry
carries a qualified transport id.

`opencode-go/minimax-m3.1-flash-free` is carried as a **PROBE** arm on EXECUTE (rank 4,
`automatic_selection: false`): the Codex-CLI lane was measured serving it
(`required_arm == served_arm`, nonce present, usage receipt OK), but it is **not** a policy default.

**Independence:** PLAN and VERIFY_SECURITY share `gpt-6.1-sol` **by owner order** — declared as
`SOD006-C4 OPEN_OWNER_ORDERED`. Model-axis independence is **absent** for that pair; only process
separation is claimed. EXECUTE (`deepseek-v4.1-flash`) vs VERIFY (`gpt-6.1-sol`) remain model-distinct.

## What is NOT claimed

- **An independent re-derivation WAS obtained** for this change-set, and it PASSED: the AO lane
  (`openai-codex/gpt-6.1-sol` over the Codex-CLI transport) re-derived 10/10 claims on its own and
  returned `VERDICT: PASS` (`lane_receipts/VERIFY_acceptance.json`). It ran with the sandbox escalated
  from `read-only` to `workspace-write` under an explicit authorisation, with a digest guard over
  `config/`, `tests/`, `src/`, `openspec/`, `AGENTS.md` and `README.md`: the guard reported
  **520/520 governed files unchanged, verdict CLEAN**. The AO's own receipt states that a pass
  "is not an acceptance of any subject" — that ceiling is carried forward here unchanged.
  The earlier failing attempts are retained verbatim in `lane_receipts/AO_verdict2.json` and
  `lane_receipts/VERIFY_final.json`, so the before/after of the transport-vocabulary repair is
  visible rather than overwritten.
- **Model-axis independence between PLAN and VERIFY_SECURITY is absent.** Both are
  `openai-codex/gpt-6.1-sol` **by owner order**, declared as `SOD006-C4 OPEN_OWNER_ORDERED`; only
  process separation is claimed. EXECUTE (`deepseek-v4.1-flash`) and VERIFY (`gpt-6.1-sol`) remain
  model-distinct. Closing the PLAN/VERIFY gap is an owner decision, not an engineering task.
- **The relay's own model catalogue is a stale snapshot.** The ChatGPT OAuth backend listed 9 models
  including `gpt-6.1-sol` and `gpt-6-sol`; the relay's catalogue holds 92 entries with no 6.x, and its
  `models_cache.json` records `fetched_at = 2000-01-01`. The lane works today because the bare id is
  forwarded verbatim — not because the catalogue is current. A catalogue refresh is an open item.
- **The openai-codex upstream's availability is not under local control.** Its own quota showed 31%
  weekly used with an unexpired credential while requests failed with `Model is unavailable`; the
  transport-vocabulary repair is what made the arm usable, but the upstream's catalogue and
  availability remain outside the local contract.
- **The committed `config/hermes.json` is stale** — it still names the `var/hermes-v020` isolated
  home and `deepseek-v4-flash`, so the COMMITTED tree carries three `PROJECTION_DEBT` warnings that
  the working tree does not. The corrected binding exists only as an uncommitted edit from an
  earlier session and was deliberately NOT landed here (it is an out-of-scope rewrite that also
  repoints `executable` at the `hermes.exe` trampoline). Ledger row `K-27`.
- **Two lane tools are still untracked**: `scripts/hgk-lane-guard.py` and
  `scripts/runtime_role_binding_assert.py` were landed, but the wider `var/` candidate population
  (300+ untracked entries) is untouched. Landing it is a per-item disposition job, not a bulk
  `git add`. Ledger row `K-28`.
- **Other work from earlier sessions remains uncommitted** in the HG-KSEOS working tree
  (`src/hg_kseos/knowledge.py`, `src/hg_kseos/spine.py`, `scripts/hermes-core.ps1`,
  `source-freeze/TT_LEDGER.csv`, `tests/test_task014_named_method_closure.py`,
  `docs/HG-KSEOS使用說明文檔.md`, `config/project.json`). It was left alone deliberately: it belongs
  to a different task and was not verified in this round.
- No canonical acceptance, no release, no production authorisation.
- The mirrored `var/` trees, the spine database, the credential stores and every machine-local
  runtime path are **not** published here.
