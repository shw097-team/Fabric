# FAR Research Synthesis — FAR-20261021-024-fallback-chain-reorder

**Decision question.** What is the current main-model fallback chain of the canonical Hermes runtime
plane under the HG-KSEOS control plane, which declaration surfaces declare it, and what is the
exact, reversible execution plan to re-order it to fallback1 = MiniMax M3.1 Flash (OPENCODE GO) and
fallback2 = MiMo-V2.6-Flash, so the live runtime chain and the HGK control-plane declaration agree
and every arm in the new chain is proven servable?

**Route (bound, not invented).** `RESEARCH_LITERATURE_REPO` → `NATIVE_WITH_SELECTED_ARIS` /
`FAR_ROUTE_NATIVE_ARIS`, primary `fabric-autoresearch-native`, challenger `aris` (method
`research-review`), methods `research-lit / novelty-check / research-review`. Copied verbatim from
`governance/FAR_CAPABILITY_MATRIX.yaml` and resolved by `far_router.route(...)`.

**Swarm.** 3 parallel read-only workers (`deleg_96784120`): SOURCE_FAMILY (W1), CODE_PATH (W2),
EXPERIMENT (W3). `canonical_parallel_writers: 0`. Merge outcome: **no disagreement** — all three
independently reproduced the orchestrator's own measurements.

**Claim ceiling: CANDIDATE_ONLY.** A research product, not an acceptance.

---

## 1. What the current chain is (measured)

Live canonical Hermes `config.yaml` (sha256 `c9308966e45ef49d10087e08ec612a66d46c328b4b054e33894f53a6a1c889a5`,
mtime 2026-10-21 12:32:39), lines 227–235:

```yaml
fallback_providers:
  - provider: opencode-go
    model: glm-5.3-flash            # <-- the owner-named first-priority arm
  - provider: opencode-go
    model: deepseek-v4.1-flash
  - provider: nvidia
    model: deepseek-ai/deepseek-v4.1-flash
  - provider: openai-codex
    model: gpt-6-luna
```

Live primary (lines 8–13): `model.default: minimax-m3.1-flash-free`, `provider: opencode-go`,
`base_url: https://opencode.ai/zen/go`, `api_mode: anthropic_messages`.

## 2. Which surfaces declare it

| Surface | Declares | Relation to the live chain |
|---|---|---|
| `config.yaml` `fallback_providers` | 4 entries | **the runtime truth** — the main agent's and ordinary delegation children's chain |
| `config/lane-routing-registry.yaml` `routes[].PLAN` (`arms`/`fallbacks`) | glm-5.3-flash, deepseek-v4.1-flash | the **lane-dispatch declaration** for the Codex CLI lanes + the governed profile — a different surface |
| `config/model-lane-assignment.json` `lane_chains.PLAN` | gpt-6.1-sol (primary), glm-5.3-flash, deepseek-v4.1-flash | same lane-dispatch declaration; registry `source_of_routes` target |
| `config/lane-route-slots.candidate.json` PLAN `ordered_pool` | rank 2 glm-5.3-flash (FALLBACK1), rank 3 deepseek-v4.1-flash (FALLBACK2) | dispatch-time candidate pool |
| `AGENTS.md:53` | PLAN fallback1 `opencode-go/glm-5.3-flash`, fallback2 `opencode-go/deepseek-v4.1-flash` | operator-facing lane-chain contract |
| `config/hermes-codex-lane.json` | `model_fallbacks: [deepseek-v4.1-flash]` | the **CODEX lane's** own chain, not the main-agent chain |

The registry declares only the **first two** live entries, in the same order. It binds **no** pointer to
the live config's `fallback_providers`, and says so explicitly (registry:501):

> "Its delegation and global fallback_providers are NON_AUTHORITATIVE for governed HGK calls. Recorded
> as observation; drift here is never a hard failure."

Measured: `lane_policy.check_drift()` on the pristine tree returns **0 findings** (epoch 24). Changing
the live chain therefore does **not** trip the drift gate — the surfaces are independent by design.

## 3. Are the two new arms real and servable? (measured)

Both ids are in the provider's own live model list (37 ids returned from
`GET https://opencode.ai/zen/go/v1/models`).

| arm | id | in live list | chat_completions | anthropic /v1/messages | Hermes client | resolved api_mode |
|---|---|---|---|---|---|---|
| fallback1 | `minimax-m3.1-flash-free` | yes | **PASS** (200, served model = id, `MM31F_PROBE_OK`) | **PASS** with `x-api-key` (200, `MM_ANTHROPIC_OK`); with `Authorization: Bearer` → *"Go requires a credential"* | **PASS** (exit 0, `HERMES_MINIMAX_PROBE_OK`) | `anthropic_messages` |
| fallback2 | `mimo-v2.6-flash` | yes | **PASS** (200, served model = id, `MIMO26F_PROBE_OK`) | NOT_TESTED (not its transport) | **PASS** (exit 0, `HERMES_MIMO_PROBE_OK`) | `chat_completions` |

The api_mode split is derived by Hermes itself (`hermes_cli/models.py:2331-2348`,
`_OPENCODE_API_MODE_PREFIXES`: `minimax-* → anthropic_messages`; `mimo-*`/`glm-*`/`deepseek-*` →
`chat_completions`), so the fallback path builds the right client per arm automatically — no
per-entry `api_mode` override is needed. Context windows resolve without error
(minimax 1,000,000; mimo 1,048,576).

## 4. The finding that qualifies the outcome (residual, disclosed not hidden)

**Hermes refuses to fall back onto the backend that just failed.** `_should_skip_fallback_candidate`
(`agent/chat_completion_helpers.py`) calls `should_skip_candidate(fb_ident, current_ident,
FailureScope.MODEL)` → `same_deployment` (`agent/backend_identity.py`). `same_deployment` returns
**True** when the providers match, the models match, and the base_url comparison cannot separate
them — and a chain entry with no `base_url` key has `base_url = ""` (falsy), so it cannot separate.

Measured against the live primary (`opencode-go / minimax-m3.1-flash-free / https://opencode.ai/zen/go`):

| chain entry | skipped as same backend? |
|---|---|
| `opencode-go/minimax-m3.1-flash-free` | **True** |
| `opencode-go/mimo-v2.6-flash` | False |
| `opencode-go/deepseek-v4.1-flash` | False |
| `nvidia/deepseek-ai/deepseek-v4.1-flash` | False |
| `openai-codex/gpt-6-luna` | False |

**Consequence.** The chain *order* after this change is exactly as the owner ordered it. But while the
canonical primary remains `minimax-m3.1-flash-free`, the runtime will skip fallback[0] and the first
**servable** arm is `mimo-v2.6-flash`. This is a correct runtime guard, not a defect, and it is
reported rather than rounded away. It disappears on its own if/when the primary is not MiniMax.

## 5. Execution plan (the FAR adjudication)

**Scope decision.** Execute the re-order on the **live canonical Hermes `fallback_providers` chain**
— the runtime plane's main-model fallback, which is what the owner named and what the previous round
in this series changed. **Do not re-bind the HGK registry's declared lane chains.** Reasons, all
measured:

1. The registry declares the live config NON_AUTHORITATIVE and binds no pointer to its chain, so the
   two surfaces are independent by design (registry:501; `check_drift()` = 0 findings).
2. The registry's lane chains are the **lane-dispatch** declaration (Codex CLI EXECUTE / VERIFY
   lanes; the in-Hermes PLAN & Orchestrator plane is bound by `profiles/hgk-governed/config.yaml`).
   Re-binding them is a **lane-chain rebind** — a different control-plane act that would touch
   SOD006-C4, the dispatch pool ranks, and the conformance-test owner-chain oracle
   (`tests/test_lane_policy.py:104-105`). It was not ordered. Recorded as OQ1.
3. The VERIFY_SECURITY checker chain is **not** in scope: the order is about the *main-model*
   fallback; re-pointing the checker's identity would change maker/checker separation and is
   explicitly not ordered.

**Target file (the only file outside the repository this round changes):**
`C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\config.yaml`

**The edit** — the `fallback_providers:` block only, by anchored text replacement:

```diff
 fallback_providers:
   - provider: opencode-go
-    model: glm-5.3-flash
+    model: minimax-m3.1-flash-free
   - provider: opencode-go
-    model: deepseek-v4.1-flash
+    model: mimo-v2.6-flash
+  - provider: opencode-go
+    model: deepseek-v4.1-flash
   - provider: nvidia
     model: deepseek-ai/deepseek-v4.1-flash
   - provider: openai-codex
     model: gpt-6-luna
```

Resulting chain (5 entries): `[0] opencode-go/minimax-m3.1-flash-free` ·
`[1] opencode-go/mimo-v2.6-flash` · `[2] opencode-go/deepseek-v4.1-flash` ·
`[3] nvidia/deepseek-ai/deepseek-v4.1-flash` · `[4] openai-codex/gpt-6-luna`.

**Apply mechanism** (`var/FAR-FBKREORDER-20261021/apply_fallback_chain.py`), with the seven
required properties: dry-run by default; **full-digest pre-image guard** (refuses the whole apply if
the live file drifted — necessary, because the file was rewritten twice during this session);
timestamped backup sibling; post-write verification; machine-readable receipt with before/after
digests + authorization reference + `deleted_files: []`; receipt-driven `--rollback`; never delete.
The script asserts that **only** the fallback block changed (round-trip equality on the rest).

**Probes after the apply:** yaml parse + readback of the 5-entry chain; re-probe both new arms
through the Hermes client; confirm `model:` block, `delegation`, `auxiliary` and every other key are
byte-identical to the pre-image.

**Rollback:** `cp <HERMES_HOME>/config.yaml.bak-fbkreorder-<UTC stamp> <HERMES_HOME>/config.yaml`,
or `python apply_fallback_chain.py --rollback` (digest-checked, driven by the receipt).

**Residuals carried out of this round:** OQ1 (registry lane chain), OQ2 (primary still MiniMax → the
skip residual), OQ3 (static catalogue), OQ4 (no observed failover event), OQ5 (registry identity
declaration).

## 6. Claim ceiling and what this run did NOT do

- **Did not** observe an actual failover event; no live log line shows the chain activating.
- **Did not** re-bind any HGK lane chain, pool rank, SoD invariant or conformance test.
- **Did not** change the canonical primary, the delegation block, the auxiliary block, or any other
  Hermes setting.
- **Did not** push, merge, deploy, or touch any repository outside the admitted write roots.
- **Did not** accept its own output: the spine acceptance `ACC-REQ-FAR-FBKREORDER-20261021` stays
  `NOT_RUN`; an independent readback lane (G5) is the verification, not this synthesis.
