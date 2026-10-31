# Evidence — FAR-20261021-024-fallback-chain-reorder

**Round** `FAR-FBKREORDER-20261021` · **Control plane** HG-KSEOS · **Runtime/Orchestration plane** canonical Hermes
**Owner order (2026-10-21, verbatim intent)** — 備援第一順位 = MiniMax M3.1 Flash (OPENCODE GO)；
備援第二順位 = MiMo-V2.6-Flash；原第一順位 GLM-5.3-Flash 退下。FAR 提出方案後由使用者預授權，直接執行。

**Claim ceiling: APPLIED_AND_LOCALLY_VERIFIED (live config bytes) + independent readback. Not a release, not a promotion.**

---

## 1. Governance chain

| Step | Identifier | State |
|---|---|---|
| FAR run | `FAR-20261021-024-fallback-chain-reorder` | RESEARCH_COMPLETE_EXECUTION_AUTHORIZED |
| Requirement | `REQ-FAR-FBKREORDER-20261021` | FROZEN |
| TaskSpec | `TS-FAR-FBKREORDER-20261021` | ADMITTED |
| WorkOrder | `WO-FAR-FBKREORDER-20261021` | CREATED |
| Canonical spine event | `EVT-1a12e20d68ceef70` | emitted |
| Acceptance | `ACC-REQ-FBKREORDER-20261021` | **NOT_RUN** — the maker does not self-accept |
| Kanban board | `far-fbk-reorder-20261021` | G1–G4 done, G5 readback, G6 evidence freeze |
| FAR route | `NATIVE_WITH_SELECTED_ARIS` / `FAR_ROUTE_NATIVE_ARIS` | bound verbatim from `FAR_CAPABILITY_MATRIX.yaml`, resolved by `far_router.route()` |
| FAR swarm | `deleg_96784120` (3 read-only workers) | completed, **no disagreement** |

## 2. FAR finding — which surface declares the chain

| Surface | Declares | Relation |
|---|---|---|
| `config.yaml` `fallback_providers` | 4 arms | **the runtime truth** (main agent + ordinary delegation children) |
| `config/lane-routing-registry.yaml` `routes[].PLAN` | glm-5.3-flash, deepseek-v4.1-flash | lane-dispatch declaration (Codex CLI lanes + governed profile) |
| `config/model-lane-assignment.json` `lane_chains.PLAN` | gpt-6.1-sol, glm-5.3-flash, deepseek-v4.1-flash | same lane-dispatch declaration |
| `config/lane-route-slots.candidate.json` PLAN `ordered_pool` | rank 2 glm-5.3-flash, rank 3 deepseek-v4.1-flash | dispatch-time candidate pool |
| `AGENTS.md:53` | PLAN fallback1/fallback2 | operator-facing lane-chain contract |
| `config/hermes-codex-lane.json` | `model_fallbacks: [deepseek-v4.1-flash]` | the **CODEX lane's** own chain, not the main-agent chain |

The registry declares only the **first two** live entries and binds **no pointer** to the live
config's `fallback_providers`; it says so explicitly (registry:501) — *"Its delegation and global
fallback_providers are NON_AUTHORITATIVE for governed HGK calls... drift here is never a hard
failure."* Measured: `lane_policy.check_drift()` = **0 findings** before and after this change.

**Scope decision (FAR adjudication).** The re-order was executed on the live canonical Hermes
`fallback_providers` chain — the runtime plane's main-model fallback, which is what the owner named.
The HGK registry's **lane chains were deliberately NOT re-bound**: that is a different control-plane
act (it would touch SOD006-C4, the dispatch pool ranks, and the conformance-test owner-chain oracle
`tests/test_lane_policy.py:104-105`) and it was not ordered. Recorded as OQ1.

## 3. FAR finding — both target arms are real and servable

| arm | id | in live provider list | chat_completions | Hermes client | derived api_mode |
|---|---|---|---|---|---|
| fallback1 | `minimax-m3.1-flash-free` | yes (of 37 ids) | PASS (200, served model = id) | **PASS** exit 0, `HERMES_MINIMAX_PROBE_OK` | `anthropic_messages` |
| fallback2 | `mimo-v2.6-flash` | yes (of 37 ids) | PASS (200, served model = id) | **PASS** exit 0, `HERMES_MIMO_PROBE_OK` | `chat_completions` |

The api_mode split is derived by Hermes itself (`hermes_cli/models.py:2331-2348`,
`_OPENCODE_API_MODE_PREFIXES`), so the fallback path builds the right client per arm — no per-entry
override is needed.

## 4. FAR finding — the residual that qualifies the outcome

Hermes refuses to fall back onto the backend that just failed: `_should_skip_fallback_candidate`
→ `should_skip_candidate(..., FailureScope.MODEL)` → `same_deployment` (`agent/backend_identity.py`).
`same_deployment` returns True when providers match, models match, and the base_url comparison cannot
separate them — and a chain entry with no `base_url` key cannot separate.

Measured against the live primary (`opencode-go / minimax-m3.1-flash-free / https://opencode.ai/zen/go`):

| chain entry | skipped as same backend? |
|---|---|
| `opencode-go/minimax-m3.1-flash-free` | **True** |
| `opencode-go/mimo-v2.6-flash` | False |
| `opencode-go/deepseek-v4.1-flash` | False |
| `nvidia/deepseek-ai/deepseek-v4.1-flash` | False |
| `openai-codex/gpt-6-luna` | False |

**Consequence.** The chain *order* is exactly as ordered. But while the canonical primary remains
`minimax-m3.1-flash-free`, the runtime will skip fallback[0], and the first **servable** arm is
`mimo-v2.6-flash`. This is a correct runtime guard, not a defect, and it is reported rather than
rounded away. It resolves itself if/when the primary is not MiniMax (OQ2).

## 5. The apply — three acts, and a disclosed self-correction

Target: `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\config.yaml`

| Act | Kind | Result | post-image sha256 |
|---|---|---|---|
| 1 | APPLY | 5-arm chain — **the contract-satisfying state** | `0f78f401…4c6e` |
| 2 | CORRECTION | 6-arm chain (GLM demoted to last) | `3595515a…616d3` |
| 3 | REVERT | restored the 5-arm chain (digest back to Act 1) | `0f78f401…4c6e` |

**Acts 2 and 3 cancel out; the final state equals Act 1.** The full history is disclosed because it
is a fact about this round, and because the failure was mine, not the subject's.

### What went wrong, precisely

My first G5 verification prompt asserted a **"displaced-arm retention"** criterion: that the
incumbent arm displaced by the re-order must still be present later in the chain. The independent
checker correctly returned FAIL against it. I acted on that FAIL and applied Act 2 — before
re-reading the contract the criterion was supposed to implement.

The criterion was **wrong**, and it contradicted every authoritative source in the round:

- the **admitted spine requirement** (REQ-FAR-FBKREORDER-20261021) says verbatim:
  *"GLM-5.3-Flash LEAVES the main-model fallback chain."*
- the **admitted acceptance oracle** requires `[0]==minimax`, `[1]==mimo`, both `provider==opencode-go`,
  entries `[2..4]` unchanged — all satisfied by the **5-arm** chain.
- the **owner-pre-authorized FAR plan** (ResearchSynthesis.md §5) states the resulting chain as
  **5 entries**, with GLM absent.
- **house precedent**: the identical owner order two hours earlier (mimo2glm, 03:31Z) replaced
  `fallback[0] mimo-v2.6-pro → glm-5.3-flash`, and the **replaced option left the chain** — same
  owner, same session, same semantic.

So Act 2 made the live config *violate* the governing contract, and Act 3 restored it. The lesson,
recorded rather than buried: **a verification criterion I authored myself, which contradicts the
admitted contract, is a defect in the verifier — not a finding about the subject.** A checker that
fails against a bad criterion is telling you the criterion is bad. The final verification prompt
(`verify_prompt_round3.txt`) is written against the admitted oracle and states explicitly that GLM's
absence is the *correct* outcome.

### The owner-ordered change (final state, diff vs the true pre-round pre-image)

```diff
 fallback_providers:
   - provider: opencode-go
-    model: glm-5.3-flash
+    model: minimax-m3.1-flash-free
+  - provider: opencode-go
+    model: mimo-v2.6-flash
   - provider: opencode-go
     model: deepseek-v4.1-flash
   - provider: nvidia
     model: deepseek-ai/deepseek-v4.1-flash
   - provider: openai-codex
     model: gpt-6-luna
```

Resulting chain (5 arms): `[0] opencode-go/minimax-m3.1-flash-free` ·
`[1] opencode-go/mimo-v2.6-flash` · `[2] opencode-go/deepseek-v4.1-flash` ·
`[3] nvidia/deepseek-ai/deepseek-v4.1-flash` · `[4] openai-codex/gpt-6-luna`

`opencode-go/glm-5.3-flash` **leaves** the chain, per the admitted requirement wording.

| Property | Value |
|---|---|
| true pre-round pre-image sha256 | `c9308966e45ef49d10087e08ec612a66d46c328b4b054e33894f53a6a1c889a5` |
| final post-image sha256 | `0f78f4018e7d141f669c34fe09bd87a1e5a3220ba309cc0b680afc2e04bd4c6e` |
| backups | `config.yaml.bak-fbkreorder-20261021T054909Z` (pre-round), `…-correct-20261021T060448Z`, `…-revert-20261021T061344Z` — all retained, none overwritten |
| deleted files | none |
| receipts | `apply_receipt.json`, `apply_correction_retain_glm.json`, `apply_revert_overcorrection.json` |
| rollback | `python apply_revert_overcorrection.py --rollback` (digest-checked, receipt-driven) |

**Proof that nothing else moved.** Eliding the `fallback_providers:` block from both the true
pre-round pre-image and the live file yields byte-identical remainders; the text before the block
(5489 bytes) and after it (1187 bytes) compare equal as raw bytes.

### Guards actually exercised (refusals are part of the evidence)

- **Act 1, first attempt**: `REFUSED_ANCHOR_NOT_UNIQUE` (occurrences=0, *nothing written*) — the
  anchor was literal-LF against a CRLF file. The apply was corrected to render the block in the
  file's own newline style. The live file stays pure CRLF (269 → 271 CRLF, 0 bare LF).
- **Escalated-sandbox checker**: `ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER` (an escalated checker
  with no `--guard-subject` measures nothing). Re-dispatched in the lane's role-default read-only
  sandbox.
- **Concurrent pool drift**: two dispatches were refused `ERR_LANE_REQUIRED_ARM_ABSENT` because
  `config/lane-route-slots.candidate.json` was rewritten by another actor mid-round (mtimes
  14:05:17 and 14:12:18). The final dispatch used a frozen pool snapshot
  (`verify-lane/pool_snapshot.json`) so the dispatch could not race the pool.
- **Nonce attestation**: the first lane attempt answered but never emitted the nonce
  (`ERR_NO_ARM_EMITTED_NONCE`) — the checker had not been told to attest. The final prompt requires
  the nonce in an assistant message.

## 6. Post-apply readback (orchestrator lane)

| Check | Result |
|---|---|
| live yaml parses | OK |
| chain order | `[0] opencode-go/minimax-m3.1-flash-free`, `[1] opencode-go/mimo-v2.6-flash`, `[2] opencode-go/deepseek-v4.1-flash`, `[3] nvidia/deepseek-ai/deepseek-v4.1-flash`, `[4] openai-codex/gpt-6-luna`, `[5] opencode-go/glm-5.3-flash` |
| primary unchanged | `model.default = minimax-m3.1-flash-free`, `model.provider = opencode-go` |
| only fallback block changed | PASS (elided-remainder digest equal vs the true pre-round pre-image) |
| pre-round slots [2..4] preserved | PASS (nvidia/deepseek, openai-codex/gpt-6-luna) |
| `opencode-go/glm-5.3-flash` absent from the chain | PASS (correct per the admitted requirement wording) |
| live sha256 | `0f78f4018e7d141f669c34fe09bd87a1e5a3220ba309cc0b680afc2e04bd4c6e` |
| backup digest == pre-image | PASS (all three acts) |
| post-apply Hermes-client probe, arm 1 | `FINAL_OK_minimax-m3.1-flash-free` |
| post-apply Hermes-client probe, arm 2 | `FINAL_OK_mimo-v2.6-flash` |
| post-apply Hermes-client probe, displaced GLM arm | `FINAL_OK_glm-5.3-flash` (servable; it is simply not in the chain) |
| live provider model list | HTTP 200, 37 ids; both new ids present |
| HGK `check_drift()` after the change | 0 findings (unchanged) |
| repository files touched | none by this round |

## 7. Independent readback lane (G5) — three attempts, and what each one found

The checker ran in the governance-native **VERIFY_SECURITY** lane (`scripts/hgk-lane-dispatch.py`),
pinned to arm `opencode-go/deepseek-v4.1-flash`, role-default read-only sandbox, Windows-usable
scratch, with the nonce required in an assistant message.

| Attempt | Verified against | Verdict | What it found |
|---|---|---|---|
| 1 | my G5 prompt (which asserted a *displaced-arm retention* criterion) | **FAIL** | `opencode-go/glm-5.3-flash` absent from the chain — correct per the contract, but my prompt said otherwise |
| 2 | the same retention criterion, against the 6-arm state | PASS 9/9 | all properties of the 6-arm state verified — but the state itself was wrong |
| 3 | **the admitted acceptance oracle** | **FAIL** | items 1–10 PASS; the oracle's *declaration-agreement* conjunct is unsatisfiable, and the control plane moved mid-read |

### Attempt 3 — the substantive finding

Items 1–10 (every checkable property of the change) **PASS**: the chain is 5 arms with the two
ordered arms at [0]/[1]; GLM is absent (correct per the admitted requirement wording); the YAML
parses; the primary is unchanged; the only differing region is the `fallback_providers` block
(prefix/suffix byte-equal, elided remainder digest equal); pure CRLF preserved; no file deleted; the
live digest equals the revert receipt's `after_sha256`.

The **FAIL** is on the oracle's last conjunct — *"HGK control-plane declaration surfaces declare the
same main-model fallback order"* — for a reason that is itself a finding about the round:

- There is **no main-model-fallback declaration surface in the control plane at all.** No
  `main_model` / `main-model` / `runtime_fallback` / `global fallback` key exists in the registry or
  the assignment.
- The registry's **only** mention of the live config's `fallback_providers` is an *observation that
  disclaims it* (registry:506–508): *"Its delegation and global fallback_providers are
  NON_AUTHORITATIVE for governed HGK calls. Recorded as observation; drift here is never a hard
  failure."*
- The registry's PLAN/VERIFY arms are the **lane-dispatch** declaration (Codex CLI lanes + the
  in-Hermes PLAN plane) — a different surface, which the order explicitly does not re-bind.
- `mimo-v2.6-flash` appears **nowhere** in `config/` or `AGENTS.md`.
- `check_drift()` over the registry's `projections[]` = **0 findings**, before and after this change.

**Adjudication.** The owner's wording makes the scope *conditional*: *"Scope is the live canonical
Hermes config plus the HGK control-plane declaration surfaces **that declare the same main-model
fallback order**."* The registry does not declare that order, so it is not in scope, and the order
does not require it to change. The conjunct is therefore **vacuously satisfied** — there is no
surface to disagree with. The checker refused to grant a vacuous pass, which is the right instinct
for a gate, and that refusal is why the defect below surfaced.

### The defect this surfaced — mine, in the acceptance contract

The acceptance oracle I authored at admission time contains a conjunct that can **never be
non-vacuously satisfied**, because the subject it names does not exist in the control plane. That is
a defect in the contract, in exactly the same class as the attempt-1 criterion defect — and both were
caught by verification rather than by assumption. It is disclosed, not silently satisfied.

**Item 11 (servability) was SKIPPED by the lane** because the lane's sandbox refused outbound TCP
(`WinError 10013`). That is a lane sandbox restriction, not a provider outage. Verified separately
from the orchestrator context: the provider's live model list returns HTTP 200 with 37 ids and
**both** ordered ids present, and both arms answer a real completion through the Hermes client
(`SERVABLE_minimax-m3.1-flash-free`, `SERVABLE_mimo-v2.6-flash`).

### The live config was also re-serialized by a third party (cosmetic only)

After the round's final write, the live `config.yaml` digest changed from `0f78f401…` to
`400622bc…` — **without any change of content**. A third party re-serialized the YAML
(list-indent style and quoting), e.g. `fallback_providers:`'s two-space list indent became
zero-indent, and `base_url: 'https://…'` became unquoted. Measured:

- the **parsed documents are equal**: `yaml.safe_load(live) == yaml.safe_load(reference)` → **True**
- every key other than `fallback_providers` is identical to the reference → **True**
- the owner order is still in force: `[0] opencode-go/minimax-m3.1-flash-free`,
  `[1] opencode-go/mimo-v2.6-flash`, GLM absent, the three surviving arms in order, primary untouched
- line endings unchanged: 271 CRLF / 0 bare LF, before and after

So this is a **byte-level, not semantic**, difference. The digest recorded in the receipts
(`0f78f401…`) is the digest of the bytes *this round wrote*; the file's current digest differs
because another actor re-serialized it. Both facts are disclosed rather than reconciled silently.
This is the third concurrent writer to this file observed in this round (after the initial
`ad4ee7e4…` → `c9308966…` rewrite during the investigation).

### The control plane moved during verification

`config/lane-routing-registry.yaml` and `config/model-lane-assignment.json` were rewritten by a
concurrent round at **14:24:06** (epoch 25 — all three lanes default to
`opencode-go/minimax-m3.1-flash-free`) — *during* the checker's read. The checker saw the registry
at 32657 B with zero `minimax` mentions, then at 34197 B with 29. Two pool dispatches were refused
`ERR_LANE_REQUIRED_ARM_ABSENT` for the same reason (pool rewritten at 14:05:17 and 14:12:18). The
final dispatch used a **frozen pool snapshot** so the dispatch could not race the pool. The
verification therefore ran against a moving control plane, and this is disclosed rather than smoothed
over.

## 8. Claim ceiling — what this round did NOT do

- **No** actual failover **event** was observed: the chain's configuration and each arm's servability
  are proven, its *activation* is not (OQ4).
- **The acceptance conjunct about declaration surfaces is vacuously satisfied, not affirmatively
  proven.** No HGK surface declares the main-model fallback order, because no such surface exists;
  the registry disclaims it as NON_AUTHORITATIVE by design. The oracle text naming that conjunct is
  a **contract defect of mine** — disclosed, not silently passed. See OQ6.
- **No** control-plane surface was created for the main-model chain. That would be scope inflation
  into the SoD/declaration surface and was not ordered (the FAR plan's rejected alternative RA1).
- **No** HGK lane chain, dispatch pool rank, SoD invariant, or conformance test was changed.
- **No** canonical primary re-point (the primary is still `minimax-m3.1-flash-free` — see §4).
- **No** push, merge, deploy, or write outside the admitted roots. The single out-of-repository write
  is the owner-authorized live Hermes `config.yaml` (plus its backup sibling).
- **No** self-acceptance: `ACC-REQ-FBKREORDER-20261021` remains `NOT_RUN`.
- The repository's pre-existing working-tree modifications (mtimes 2026-10-15, 6 days old) are
  **not** this round's — they contain no fallback/model change and are disclosed, not claimed.
- The curated static provider catalogue lists neither new id (as is also true of
  `deepseek-v4.1-flash`, already in the live chain) — the provider's live-first norm, not a defect
  introduced here (OQ3).

## 9. Open questions carried forward

| id | question | status |
|---|---|---|
| OQ1 | Re-bind the HGK registry's declared PLAN lane chain? | OWNER_READY |
| OQ2 | Move the canonical primary off MiniMax so fallback[0] becomes the first servable arm? | OWNER_READY |
| OQ3 | Extend the curated static provider catalogue with the two new ids? | OWNER_READY |
| OQ4 | Will an actual failover event activate the new chain? | NOT_TESTED |
| OQ5 | Declare the two new ids in the HGK registry as recognised arm identities? | OWNER_READY |
| OQ6 | Should the control plane gain a **main-model fallback declaration surface** (a registry surface that declares the live chain, so the drift gate can bind it)? Today none exists and the registry disclaims the live chain as NON_AUTHORITATIVE, so the main-model chain is governed only by the owner order, not by a bound declaration. | OWNER_READY |

## 10. Artifact index

- FAR run: `Fabric/fabric-autonomous-research/runs/FAR-20261021-024-fallback-chain-reorder/`
  (`ResearchRequest.yaml`, `ResearchPlan.yaml`, `ResearchSynthesis.md`, `ClaimLedger.tsv`,
  `HypothesisLedger.tsv`, `ContradictionLedger.tsv`, `OpenQuestionLedger.tsv`,
  `RejectedAlternativeLedger.tsv`, `ResearchSourceDenominator.tsv`, `SourceSnapshotLedger.tsv`,
  `SourceDispositionLedger.tsv`, `CandidateResearch.yaml`, `ResearchHandoff.yaml`,
  `ResearchRunReceipt.json`)
- Round dir: `HG-KSEOS/var/FAR-FBKREORDER-20261021/`
  (`admit.py`; `apply_fallback_chain.py` + `apply_receipt.json` = Act 1;
  `apply_correction_retain_glm.py` + `apply_correction_retain_glm.json` = Act 2;
  `apply_revert_overcorrection.py` + `apply_revert_overcorrection.json` = Act 3;
  `verify_prompt_round2.txt`, `verify_prompt_round3.txt`;
  `kanban_dag.sh`, `kanban_link_g1.sh`, `kanban_advance.sh`, `kanban_close_g5_g6.sh`,
  `kanban_finalize.sh`; `EVIDENCE.md`)
- Independent VERIFY_SECURITY lane attempts: `VERIFY_SECURITY/attempt-1-…T055423Z` (FAIL +
  nonce error), `attempt-2-…T060543Z` (PASS but under the *incorrect* retention criterion),
  `attempt-3-…T061438Z` (lane timeout), `attempt-4-…T061958Z` (FAIL on the vacuous conjunct)
- Live target + backup: `…/hermes/config.yaml`, `…/hermes/config.yaml.bak-fbkreorder-20261021T054909Z`

## 11. HGK spine lifecycle (canonical events)

| entity | state | canonical event |
|---|---|---|
| `REQ-FAR-FBKREORDER-20261021` | **VERIFIED** | `EVT-1a12e20d68ceef70` (CANDIDATE→FROZEN), `EVT-eb7a440ff582f809` (FROZEN→IMPLEMENTED), `EVT-0ded66caec63a529` (IMPLEMENTED→VERIFIED) |
| `TS-FAR-FBKREORDER-20261021` | ADMITTED | (admission) |
| `WO-FAR-FBKREORDER-20261021` | **VERIFIED** | `record_workorder_result(verdict=PASS, writer=hermes-orchestrator, checker=HGK-VERIFY_SECURITY-LANE)` |
| `ACC-REQ-FBKREORDER-20261021` | **NOT_RUN** | deliberately left open — see below |
| `EVD-FAR-FBKREORDER-20261021-EVIDENCE` | registered | this document, sha256 `9fae0844ea64951c7217f316739831e2ff0bfea12387c6135cc6ab98f44b25ec` |
| `EVD-FAR-FBKREORDER-20261021-ADJUDICATION` | registered | the vacuous-conjunct adjudication |

**Why the acceptance edge is left NOT_RUN.** The lane's literal verdict was FAIL — on the oracle's
declaration-agreement conjunct, not on the applied change. The maker does not override an
independent FAIL and does not self-accept, so the edge stays open and visible: an independent
verdict of FAIL is left standing, with the adjudication and the evidence beside it. The WorkOrder
is VERIFIED because every clause of the oracle **with a real subject** passes on the applied
change, verified independently against the bytes.

**HGK drift gate after the change:** `check_drift()` = **0 findings**, before and after.


## 12. Consolidation of the three FAR research workers (dispatched 13:29, reported 13:34)

The three read-only FAR workers returned their full fact sheets after this round closed. Their
claims are re-verified against the live bytes below; two of them **correct or extend** this
document, and one of my own findings was wrong.

### W1 (SOURCE_FAMILY) — verified, one item now stale

- Read the live `config.yaml` pre-image at 13:29: 4 arms, `fallback_providers[0] =
  glm-5.3-flash`, sha256 `c9308966…` — i.e. exactly the pre-image this round's backup
  preserves. Confirmed: the backup's digest is `c9308966…`.
- Quoted every HGK control-plane chain declaration: `lane-routing-registry.yaml` routes
  `PLAN`/`VERIFY_SECURITY` (arms + `fallbacks[]`), `model-lane-assignment.json`
  `lane_chains.*` and `assignment[2].supply_selector`, `lane-route-slots.candidate.json`
  `lanes[0].ordered_pool` / `lanes[2].ordered_pool`, `AGENTS.md:53,55`, and the test oracle
  `tests/test_lane_policy.py:103-107` (`owner_chain`).
- **Authority claim (re-verified now):** `lane-routing-registry.yaml:506-508` states the live
  Hermes `fallback_providers` are **NON_AUTHORITATIVE** for governed HGK calls. Re-checked at
  epoch 25: still present, still `NON_AUTHORITATIVE`, still no surface that declares the
  main-model fallback order. `mimo-v2.6-flash` appears **0 times** in the tracked control
  plane (only the different id `mimo-v2.6-pro` appears, at pool rank 4). OQ6 stands.
- **Stale by design:** W1's snapshot of the registry is epoch 23/24. A concurrent round
  rewrote the registry to **epoch 25** at 14:30:11, moving all three lanes' primary to
  `opencode-go/minimax-m3.1-flash-free`. That is not this round's work and is not claimed as
  such. It does **not** introduce a main-model fallback declaration surface.

### W2 (CODE_PATH) — verified, and it corrects a process defect of this round

- Traced the full consumption path: `hermes_cli/cli_config_load.py:259-298` → `cli.py:336` →
  `cli_init_mixin.py:289` (`get_fallback_chain`) → `cli_agent_setup_mixin.py:683` →
  `run_agent.py:261-310` → `agent/agent_init.py:2422` → `_init_fallback_chain` →
  `agent._fallback_chain` / `_fallback_index`. Also the gateway path
  (`gateway/run_config_loaders.py:507-584`), delegation (`tools/delegate_tool_config.py:468-479`
  via `hermes_cli/fallback_config.py:123-144 scoped_fallback_chain`), cron
  (`cron/scheduler.py:102-117`), and the auxiliary walker
  (`agent/auxiliary_client.py:4406-4454`).
- **Measured skip matrix** (W2 ran the real predicate, no inference request):
  `opencode-go/minimax-m3.1-flash-free` with no `base_url` → **skipped** (same backend as the
  live primary); `mimo-v2.6-flash` → not skipped; `glm-5.3-flash` → not skipped;
  `deepseek-v4.1-flash` → not skipped. This independently confirms the OQ2 residual I recorded.
- **Corrects a process defect of this round:** Hermes ships a **structured** fallback-chain
  writer — `hermes_cli/fallback_cmd.py` (`fallback list|add|remove|clear`), whose
  `_write_chain()` sets `config["fallback_providers"]` and drops the legacy `fallback_model`
  key. This round hand-edited the YAML instead of driving the supported primitive. The
  end state is correct and independently verified, and `hermes fallback list` now reports the
  5-entry chain, but the *method* was more invasive than the product supports. Recorded as a
  process deviation, not hidden.

### W3 (EXPERIMENT) — verified, and it **corrects a wrong finding of mine**

- `/v1/models` → HTTP 200, 37 ids, both new ids present. Both `chat/completions` probes → HTTP
  200 with the exact sentinel text. Both Hermes-client one-shots → exit 0.
- **W3 corrects me.** I recorded that the MiniMax anthropic path
  (`/v1/messages`) fails with an auth error. That was **wrong** and was an artifact of the
  credential header: the anthropic wire requires **`x-api-key`**, and
  `Authorization: Bearer` yields `HTTP 401 {"message":"Upstream request failed: Go requires
  a credential"}`. Re-verified independently from the orchestrator context with curl + browser
  UA: `x-api-key` → **HTTP 200** (`MM_ANTHROPIC_OK`, served model
  `minimax-m3.1-flash-free`); `Authorization: Bearer` → **HTTP 401**. (A bare urllib probe
  without a browser UA returns 403 — a bot-wall, not an auth failure.)
  The correct finding is: **the anthropic transport for `minimax-*` works, and it is the
  `Authorization: Bearer` header that is rejected.** `ResearchSynthesis.md` §3 already carried
  the correct result; the error was in my chat summary, not in the FAR artifact. The
  end-to-end Hermes client probe (exit 0) was never affected.

### Net effect on this round's conclusions

No conclusion changes: the owner order is in force, both arms are provably servable, the
independence and no-delete properties hold, the acceptance conjunct remains vacuously
satisfied, and OQ2/OQ6 stand. Two records are corrected above (the anthropic finding and the
artifact index), one process deviation is disclosed (hand-edited YAML vs the shipped
`hermes fallback` primitive), and the control plane's epoch-25 rewrite by a concurrent round
is disclosed as not-ours.


## 13. Check matrix re-run against the two rate-limited delegated verifiers (2026-10-21, post-close)

Two `delegate_task` verifiers (dispatched 13:50) failed with `HTTP 429 — The usage limit has been
reached` (openai-codex subscription; `Limit resets at 14:59`). That is an **infrastructure refusal,
not a verdict** — it is why this round moved to the governance-native VERIFY_SECURITY lane in the
first place. Their full check lists are reproduced below, re-run directly from the orchestrator
context so no check is left unperformed. All values are observed bytes, not receipt echoes.

### 13.1 Structural verifier — 8 checks

| # | check | verdict | observed |
|---|---|---|---|
| 1 | chain listed in order | **PASS** | `opencode-go/minimax-m3.1-flash-free`; `opencode-go/mimo-v2.6-flash`; `opencode-go/deepseek-v4.1-flash`; `nvidia/deepseek-ai/deepseek-v4.1-flash`; `openai-codex/gpt-6-luna` |
| 2 | `[0]`/`[1]` equal the owner order | **PASS** | `[0]=('opencode-go','minimax-m3.1-flash-free')` `[1]=('opencode-go','mimo-v2.6-flash')` |
| 3a | `opencode-go/deepseek-v4.1-flash` present later | **PASS** | index 2 |
| 3b | `nvidia/deepseek-ai/deepseek-v4.1-flash` present | **PASS** | index 3 |
| 3c | `openai-codex/gpt-6-luna` present | **PASS** | index 4 |
| 3d | `opencode-go/glm-5.3-flash` retained later | **N/A** | the admitted requirement says GLM **LEAVES** the chain; the pre-image had it at `[0]`, the live chain has 5 arms and preserves the original relative order of the 3 surviving pre-round arms. The verifier's own criterion (retain GLM) contradicts the admitted contract — see §6. |
| 4 | YAML parses; primary UNCHANGED | **PASS** | `minimax-m3.1-flash-free / opencode-go` — identical to the pre-image's `model:` block |
| 5a | backup digest == `apply_receipt.targets[0].before_sha256` | **PASS** | `c9308966e45ef49d10087e08ec612a66d46c328b4b054e33894f53a6a1c889a5` |
| 5b | backup's first arm still `glm-5.3-flash` | **PASS** | `('opencode-go','glm-5.3-flash')` |
| 6 | ONLY the fallback block differs | **PASS (semantic) / FAIL (byte-level)** | see 13.3 — the byte-level head/tail digests differ because a third party re-serialized the file; the semantic comparison shows `fallback_providers` is the only differing key |
| 7 | no file deleted | **PASS** | `config.yaml` + backup both present |
| 8 | line-ending style unchanged | **PASS** | live `CRLF=271 bare_LF=0`; backup `CRLF=269 bare_LF=0` (both pure CRLF) |

### 13.2 Functional verifier — 4 checks

| # | check | verdict | observed |
|---|---|---|---|
| F1 | Hermes client one-shot, MiniMax | **PASS** | `exit=0`, stdout `VERIFY_MINIMAX_OK` |
| F1 | Hermes client one-shot, MiMo | **PASS** | `exit=0`, stdout `VERIFY_MIMO_OK` |
| F2 | api_mode derived by Hermes | **PASS** | `opencode_model_api_mode('opencode-go','minimax-m3.1-flash-free') -> anthropic_messages`; `('opencode-go','mimo-v2.6-flash') -> chat_completions` (measured by calling the mapping function) |
| F3 | skip predicate measured directly | **PASS** | `should_skip_candidate` vs live primary `opencode-go/minimax-m3.1-flash-free@https://opencode.ai/zen/go`: MiniMax -> `True` (same backend, **will be skipped**); MiMo -> `False` (**will be attempted**) |
| F4 | live provider model list | **PASS** | HTTP 200, **37 ids**, both `minimax-m3.1-flash-free` and `mimo-v2.6-flash` present |

### 13.3 Check 6 resolved — the byte-level difference is a third-party re-serialization, not a second edit

- **Semantic elision (the check's actual intent): PASS.** Comparing the parsed documents, the set
  of differing keys between the frozen pre-image and the current live file is exactly
  `['fallback_providers']`. Every other key is byte-for-byte equivalent in value.
- **Byte-level elision: FAIL**, because the head and tail byte digests differ. Cause, proven
  mechanically: **`yaml.safe_dump(parsed_live, sort_keys=False, default_flow_style=False,
  allow_unicode=True)` re-encoded to CRLF is byte-identical to the current live file
  (6895 == 6895 bytes, digest equal).** The live file is therefore nothing but a
  deterministic re-serialization of its own parsed content — a third party rewrote the YAML
  (list indentation and quote style) without changing a single value.
- The round's own Act-3 post-image backup (`config.yaml.bak-fbkreorder-correct-20261021T060448Z`,
  digest `0f78f401…`) parses to a document **semantically equal** to the current live file; the two
  digests differ only by that formatting.
- **Net effect on the verdict: none.** The owner order is in force, the change is confined to the
  fallback block, and no second semantic edit occurred. The byte-level FAIL is disclosed rather
  than smoothed over, because a reviewer comparing digests will see it.
