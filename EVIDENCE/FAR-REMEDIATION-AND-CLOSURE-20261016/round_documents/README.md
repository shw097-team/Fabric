# FAR-REMEDIATION-AND-CLOSURE-20261016

Round 2 of session `20261016_104922_d455e7`, following `LANE-RELIABILITY-CLOSURE-20261016`.
HG-KSEOS is the control plane; the canonical Hermes is its governed Runtime/Orchestration plane.

**Claim ceiling: CANDIDATE_ONLY.** Everything here was measured on this host by this session. Applying a
ruling is not accepting it. `hgk_canonical_acceptance: NOT_PERFORMED`.

## What this round was asked to do, and what it did

The owner order: study every residual, gap, owner-decision item, session-closure item and publication item
with FAR; rule the best option on low friction / high necessity / no over-engineering; **execute that
ruling**; then close, hand over and publish the implementation and evidence to `github.com/shw097-team/Fabric`.

The ruling is `FAR_RULING.md` (items R1–R7). Its execution is recorded in the receipts named below, and
each decisive number was re-derived from a receipt or raw log rather than transcribed.

## Delivered

| Item | What happened | Evidence |
|---|---|---|
| **R1 — PLAN route row rebind** | `routes[].PLAN` moved from `opencode-go/glm-5.3-flash` to `openai-codex/gpt-6.1-sol` (medium, OAuth) under the owner order of 2026-10-16; the arm order is now `gpt-6.1-sol` → `glm-5.3-flash` → `deepseek-v4.1-flash`, the exact order the conformance test asserts; the stale `QUOTA_429` marker is kept as dated history; `admission_status: UNPROVEN → ADMITTED` **on measurement**. Registry `epoch` 20 → 21. | `R1_R3_APPLY_RECEIPT.json`, `R1_R3_COMPLETION_RECEIPT.json` |
| **R2 — promotion** | The four product files the previous round verified were promoted from the frozen candidate. Each is byte-identical to the candidate digest, the orchestrator re-ran the oracle itself (6 + 16 tests, OK), and nothing round-local was promoted. The candidate's two **config** files are stale (revision 19 vs canonical 21) and were deliberately NOT promoted. | `R2_PROMOTION_RECEIPT.json` |
| **R3 — SoD reclassification** | `declared_conflicts[SOD006-C2]` moved `OPEN_OWNER_ORDERED → OWNER_ORDERED_IN_FORCE`, with the surviving independence written into the same record: process, lane, evidence-path, and the no-self-acceptance rule remain; maker/checker **model** independence is absent **by owner order**. | same receipts, `FAR_RULING.md` R3 |
| **R7 — a defect class named and detected** | The site file simultaneously declared VERIFY_SECURITY's default arm as `gpt-6.1-sol` (lane chain) and `glm-5.3-flash` (three sod prose fields) — **with `check_drift` at zero fatal findings**. A detector for the class was written and demonstrated against both states: 3 contradictions before, 0 after. | `FINDINGS_R7_CROSS_FIELD_DECLARATION.md`, `check_declaration_agreement.py` |
| **E11 reclassified** | "5 E11 cases" is really **4 E11 guard cases + 1 C2 case**, and the underlying first cause is an **uncaught `OSError` on relay/usage metadata probes** at `scripts/hgk-lane-dispatch.py:862-873` and `:1134-1135`: the promised refusal receipt is replaced by a crash. On this host the unmodified module passes 136/136. | `evidence/EVIDENCE_E11_PRECONDITION.md` |
| **Regression isolation** | The whole tree was run twice — once with the pre-change config pair restored from its backups, once with the post-change pair. Pre: 527 tests, 8 failures + 2 errors. Post: 527 tests, 7 failures + 2 errors. **Diff: exactly one name removed (`test_registry_and_projection_shape`), none added.** CALIBRATION, added
after the independent checker re-ran both states itself: the absolute counts above are
**environment-specific and were NOT independently reproduced** (its restricted reference tree ran 540 tests
with 29 failures + 17 errors, and it names the missing dependencies). What DID reproduce is the **paired
delta — one removal, zero additions** (its own pair: 47 → 46). The isolation claim is a DELTA claim; the
absolute counts are this host's. | `evidence/WHOLE_TREE_PRE.txt`, `evidence/WHOLE_TREE_POST.txt` |

**F1 is closed.** The canonical conformance gate that was RED on exactly one assertion is now green, and the
lane guard admits the policy source again.

## Not delivered — stated plainly

**R5, the `--turn-shape edit_only` flag in `scripts/hgk-lane-dispatch.py`: NOT delivered, after TWO
attempts.** The bounded writer did not return within its window either time. The first attempt's failure was
diagnosed to this round's own brief — the output path was ambiguous under the sandbox cwd, so the writer
spent its whole window probing directory names for a writable location (12 tiny probe files, CPU pinned at
0). The brief was corrected and re-dispatched; the corrected attempt moved its probes into the right
directory but STILL never landed the change, and its scope (four edits plus a new test file in a
2,275-line module) is the remaining explanation — against a single-hunk edit-only turn on the same lane that
landed in 74 s in the previous round. Both attempts are recorded with measured termination evidence and the
item is handed over open. See `lanes/EXECUTE/R5/TERMINATION.json` and `lanes/EXECUTE/R5b/TERMINATION.json`.

## The independent verdict — three claims agreed, three disputed, one not verifiable

`lanes/VERIFY_SECURITY/V3c/work/CHECKER_VERDICT.json` (CODEX CLI, `openai-codex/gpt-6.1-sol`): **C1 AGREE,
C5 AGREE, C7 AGREE, C2 DISAGREE, C3 DISAGREE, C6 DISAGREE, C4 UNCERTAIN.** The checker re-derived every
decisive number itself and was forbidden to read this round's conclusions. Its findings are in
`FINDINGS_V3C_INDEPENDENT_VERDICT.md`; the two that matter most are handed over **OPEN**:

- **The manifest hashed ITSELF** (`F-IND-1`, my defect, fixed): the sole mismatching item was
  `FROZEN_MANIFEST.json`, whose recorded digest could only ever be the previous revision's bytes. Both it
  and `GATE_REPORT.json` are now excluded from the frozen item set, with the reason declared in the
  manifest's own `excluded` field, and revision 1 is retained as
  `frozen/FROZEN_MANIFEST.rev1.SUPERSEDED.json`.
- **A third cross-field contradiction** (`F-IND-2`, OPEN): `/sod/plan_lane` and
  `/sod/verify_security_selection` say an arm is *never* auto-selected while the registry declares
  `automatic_selection=true` for exactly those arms. Same class as R7, different axis — my detector reads
  only the default-arm claims, so this is also correction **SC-7**.
- **The R2 promotion path lacked pre-write typed admission** (`F-IND-3`, OPEN): byte-exactness is verified
  by independent recomputation, but the path that put the files there was not the governed one. The claim
  ceiling for R2 is quoted SPLIT, never as one word.

A first checker turn (`V3b`) **refused to adjudicate anything** because frozen revision 1 no longer verified;
that refusal is preserved as evidence (`evidence/CHECKER_V3B_REFUSAL_IS_EVIDENCE.md`) and is the reason the
defect is on the record at all. `ROUND_CLOSURE.json` carries both turns, marking the refusal as a refusal.

## Self-reported defects (this round's own)

**Seven**, all in `FINDINGS_SELF_CORRECTIONS.md`: an incomplete first application that the existing
lane-guard suite caught; an applied-then-rolled-back attempt whose spine rows survived the rollback; a
promotion that ran before its WorkOrder existed; a detector whose first parser returned a false negative on
the very line it exists to catch (a claim made from that run was withdrawn); a **premature freeze** that the
independent checker and my own gate independently identified; a **brief that conflated two different
objects**; and the detector's **scope gap** above. Four of the seven were found by someone or something
other than my own review.

## Where to look

| If you want to judge… | read |
|---|---|
| the ruling and its reasoning | `FAR_RULING.md` |
| what was enumerated, mechanically | `RESIDUAL_INVENTORY.json` (22 items: 9 residual, 3 gap, 3 owner-decision, 6 closure, 1 publication) |
| the machine-readable closure | `ROUND_CLOSURE.json` (16 detections, 15 honest residuals, 7 self-corrections, and BOTH checker turns with the refusal labelled as a refusal) |
| the independent verdict and what it disputed | `FINDINGS_V3C_INDEPENDENT_VERDICT.md`, `lanes/VERIFY_SECURITY/V3c/work/CHECKER_VERDICT.json` |
| the checker turn that REFUSED to adjudicate | `evidence/CHECKER_V3B_REFUSAL_IS_EVIDENCE.md` |
| the four mechanisms | `KANBAN_SWARM_GRAPH.json` (KANBAN board + SWARM DAG ids), `openspec/` (validates `--strict`), GSTACK as a named-method readback |
| the PLAN plane's evidence | `PLAN_LANE_AVAILABILITY.json`, `GSTACK_READBACK.json` |
| what changed in the product | `implementation/` — before/after files **and** unified diffs |
| what the writer actually produced | `implementation/writer_output/` |
| everything the checker saw | `CHECKER_BRIEF.md`, `lanes/VERIFY_SECURITY__*/` |
| the proposals for the next round | `RETROSPECTIVE.md`, `SELF_EVOLUTION.md` |

## Reproduction

Interpreter: `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`, always with `-B`.

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS
# the canonical gate that was RED and is now green
python -B -m unittest tests.test_lane_policy tests.test_lane_guard -v
# drift must be empty
python -B -c "import sys;sys.path.insert(0,'src');from hg_kseos.lane_policy import check_drift;print(check_drift())"
# the R7 class, against the preserved pre-change snapshot and the current file
python -B var/FAR-REMEDIATION-AND-CLOSURE-20261016/check_declaration_agreement.py \
        config/model-lane-assignment.json.bak-far-remediation-20261016
python -B var/FAR-REMEDIATION-AND-CLOSURE-20261016/check_declaration_agreement.py \
        config/model-lane-assignment.json
# the whole tree, both states, is recorded as two raw logs rather than one summary claim
```

## For the external engineer planning the next upgrade

The round's priced proposals are P1–P6 in `RETROSPECTIVE.md`, ordered by value per unit of change. The two
highest-value ones are both in `lane_policy`: a **cross-field declaration sweep** (closes R7 permanently)
and a **coupled-pin sweep** (site digest, site revision, registry epoch), so that a half-applied declaration
change fails at the gate instead of at dispatch time. P4 carries the only security-adjacent work and should
be reviewed by a human: two typed metadata-refusal catches must fail closed.

Three items the independent checker added, in priority order for the next round:

1. **The `automatic_selection` axis** (`F-IND-2`): the cross-field sweep above must read the
   `automatic_selection` flags, not only the default-arm claims, or it will keep missing this class. Three
   low-friction options are priced in `FINDINGS_V3C_INDEPENDENT_VERDICT.md`.
2. **Pre-write typed admission for promotions** (`F-IND-3`): `ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC`
   arrived AFTER the files were copied. A promotion path should refuse to copy anything until the WorkOrder
   exists, and should require an atomic pre/post whole-tree inventory, because a post-change `git status`
   cannot prove nothing else changed.
3. **Freeze-last and no self-reference** (`F-IND-1`): a freeze manifest must not include itself, nor any
   artifact the tool that verifies it rewrites; and it must be taken after the last derived document has
   settled. Both rules are now encoded here and were each learned from a real, refused verification.
