# CHECKPOINT — HG-KSEOS FAR remediation, closure and publication

Round: `FAR-REMEDIATION-AND-CLOSURE-20261016` · Session: `20261016_104922_d455e7` · Written: 2026-10-16 (UTC+8)
Round dir: `var/FAR-REMEDIATION-AND-CLOSURE-20261016/` · Publication: `shw097-team/Fabric`, branch
`pub/far-remediation-and-closure-20261016`, **PR #8** (open, NOT merged), packet
`EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/`

## 1. What this round was asked to do

Under the current Fabric contract: HG-KSEOS is the sole control plane, canonical Hermes is its governed
Runtime/Orchestration plane. After HGK admission: use **FAR** over every residual, gap, owner-decision item,
session-closure item and publication item; rule the best option on low friction / high necessity / no
over-engineering; **execute the ruling** (owner-authorised); then close, hand over and publish the
implementation and evidence to `github.com/shw097-team/Fabric` for external engineers. KANBAN + SWARM +
GSTACK + OPENSPEC enabled; multi-sub-agent fan-out; self-detect / self-repair / self-verify to completion;
then a governed self-study / self-learning / self-iteration / self-evolution pass.

## 2. What was actually proven, and how

| claim | evidence |
|---|---|
| **F1 closed** — `routes[].PLAN` rebound to the owner-mandated arm `openai-codex/gpt-6.1-sol` (medium, OAuth), arm order `gpt-6.1-sol → glm-5.3-flash → deepseek-v4.1-flash` | conformance case exit 0 (was the ONLY red assertion); `check_drift` 0 fatal; registry `epoch` 20 → 21; **independently reproduced by the checker** (C1 AGREE) |
| **R2 promoted 4 files, byte-exact** | canonical/candidate/reference-copy hashes recomputed by the checker and they agree; all 200 frozen-candidate entries match (C3: byte-exactness confirmed) |
| **R7 class is real** | checker ran the detector itself on both states: 3 contradictions pre-change, 0 post-change (C5 AGREE) |
| **R5 NOT delivered** | no turn-shape flag in either the canonical or the reference dispatcher; the round claims no otherwise (C7 AGREE) |
| **Regression isolation** | paired DELTA reproduces: exactly one named test removed (`test_registry_and_projection_shape`), none added (the checker's own pair: 47 → 46) |

## 3. What changed in the canonical tree

- `config/lane-routing-registry.yaml` (`a0d811c4…` → `109bcf8a…`) and `config/model-lane-assignment.json`
  (`d41f8f8b…` → `21513be1…`): R1 rebind, R3 SoD reclassification to `OWNER_ORDERED_IN_FORCE`, `epoch` 21,
  coupled `source_of_routes{revision,sha256}` re-pinned, PLAN fallbacks ordered `[GLM, DeepSeek]` exactly as
  the conformance case asserts. Before/after copies preserved.
- **Four product files promoted** (byte-identical to the frozen candidate) — see `R2_PROMOTION_RECEIPT.json`.
- Everything else in the round is candidate-only or round-local.

## 4. Claim ceiling — split, do not collapse

**CANDIDATE_ONLY. `hgk_canonical_acceptance: NOT_PERFORMED`.** Nothing is accepted, approved, merged or
reviewed by any external party. Two of the round's own claims are **capped by the independent checker** and
must be quoted in the split form:

- **R2**: `bytes VERIFIED` / `pre-write typed admission ABSENT` / `canonical writer NOT the mandated writer`
  / `exclusive pre/post tree inventory NOT TAKEN`. (`F-IND-3`, DISAGREE, open.)
- **Regression isolation**: the DELTA is verified; the **absolute counts are environment-specific and were
  NOT independently reproduced**. (C4 UNCERTAIN — a reproduction limitation, not evidence of new defects.)

## 5. Open residuals (do not smooth these)

1. **`F-IND-2` — a third cross-field contradiction, NOT repaired**: `/sod/plan_lane` and
   `/sod/verify_security_selection` say an arm is *never* auto-selected while `config/lane-routing-registry.yaml:297`
   declares `automatic_selection=true` for exactly those arms (and VERIFY arm C pairs an operator-selectable
   role with `automatic_selection=true`). Same class as R7, on an axis my detector does not read →
   correction **SC-7**. Three low-friction options are priced in `FINDINGS_V3C_INDEPENDENT_VERDICT.md`.
2. **`F-IND-3` — the R2 promotion path was not the governed one** (files copied before `create_workorder`,
   which then returned `ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC`; recorded writer was the PLAN/orchestrator).
3. **R5 not delivered after two attempts** — the first wedged on MY brief's path ambiguity (probe loop),
   the corrected one still did not land it; scope (4 edits + a new test file in a 2,275-line module) is the
   remaining explanation. Decompose into 2–3 edit-only turns rather than re-running the same shape.
4. **The R7 class is still not detected by the product** — `check_declaration_agreement.py` is a round
   artifact; three remediations priced, none applied.
5. **E11 stays open (MIXED)**: the real defect is two uncaught metadata `OSError`s at
   `scripts/hgk-lane-dispatch.py:862-873` and `:1134-1135`; nothing repaired.
6. **PLAN and VERIFY/SECURITY share a model by owner order** (`SOD006-C2`, now `OWNER_ORDERED_IN_FORCE`):
   maker/checker MODEL independence absent by order; process, lane, evidence-path and the
   no-self-acceptance rule remain.
7. 15 residuals in total are enumerated machine-readably in `ROUND_CLOSURE.json`.

## 6. Self-corrections (nine, and four were found by something other than me)

`FINDINGS_SELF_CORRECTIONS.md` + `ROUND_CLOSURE.json.corrections`: SC-1 (incomplete first application the
existing guard caught; its numerical description was itself imprecise — fixed), SC-2 (rollback left spine
rows), SC-3 (promotion ran before its WorkOrder), SC-4 (detector parser false negative; claim withdrawn),
**SC-5** (frozen subject taken too early — found by the checker AND by my own gate), **SC-6** (the checker
brief conflated the frozen manifest with the reference tree), **SC-7** (detector scope gap — found by the
checker), **SC-8** (the gate's own G4 check could never fail for the reason it was written: a greedy class
plus a negative lookahead backtracks; replaced with a direct assertion), **SC-9** (the first packet build
flattened 244 scratch files; the rule is now a structural depth limit).

## 7. Next session's first moves

1. **Read `FINDINGS_V3C_INDEPENDENT_VERDICT.md` first** — it contains the three DISAGREE verdicts and the
   two open findings; everything else in the packet should be read through it.
2. `F-IND-2` and `F-IND-3` are the two things an owner should decide. Neither is repair work for an agent
   without a WorkOrder.
3. If R5 is still wanted, decompose it; do not re-run the same brief shape.
4. Do **not** merge PR #8: merging is the owner's decision, and this round explicitly did not take it.

## 8. Reproduction

```
R=C:/Projects/Agent_Workspace/HG-KSEOS; PY=C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe
$PY -B $R/var/FAR-REMEDIATION-AND-CLOSURE-20261016/make_closure_round2.py   # regenerate the closure from disk
$PY -B $R/var/FAR-REMEDIATION-AND-CLOSURE-20261016/gate_round2.py           # must print GATE_PASS
$PY -B $R/var/FAR-REMEDIATION-AND-CLOSURE-20261016/publish_packet_round2.py
$PY -B $R/var/FAR-REMEDIATION-AND-CLOSURE-20261016/verify_remote.py 8       # remote readback, digests only
```
Freeze discipline learned the hard way: **freeze LAST, immediately before the manifest is consumed**, keep
every revision (`frozen/FROZEN_MANIFEST.rev*.SUPERSEDED.json`), and never let the manifest include itself or
any artifact the tool that verifies it rewrites. Environment notes that cost time: MSYS rewrites native
`//FLAG` arguments; native git needs `C:/…` paths; `npx`/`openspec` need a real shell; the Hermes CLI needs
`PYTHONPATH` + the hermes-agent venv interpreter.
