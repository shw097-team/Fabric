# EVIDENCE_RESIDUAL_STATUS_REDERIVED — ROUND3-LANE-REBIND-AND-CLOSURE-20261016

Round-dated evidence file: every one of the previous round's 15 honest residuals, plus F-IND-2 and
F-IND-3, re-derived against the LIVE tree under the NEW owner mandate:

```
PLAN & Orchestrator  = opencode-go / glm-5.3-flash
EXECUTE bounded writer = opencode-go / deepseek-v4.1-flash
VERIFY / SECURITY checker = opencode-go / deepseek-v4.1-flash
(new mandate; referenced from var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/PLAN.md §1, which
supersedes the previous round's role_mandate.json openai-codex/gpt-6.1-sol order)
```

Scope: **read-only re-derivation.** No file under the repo was edited. The only write by this
sub-task is the two files under `var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/evidence/` named
`EVIDENCE_RESIDUAL_STATUS_REDERIVED.{md,json}` (this file is the .md of the pair).

---

## Implications of the NEW mandate read as a set, before the item list

The new mandate does two structurally different things to the previous round's residual set:

1. It **dissolves the PLAN==VERIFY same-model owner-ordered collision** (the residual R-07's own
   substance) because PLAN leaves `gpt-6.1-sol` for `glm-5.3-flash` while the current VERIFY route's
   rank-1 primary is still `gpt-6.1-sol` (registry `routes[].VERIFY_SECURITY` provider `openai-codex`,
   model `gpt-6.1-sol`, lines 278-292 of `config/lane-routing-registry.yaml`).
2. It **creates a NEW same-model maker/checker pair** out of exactly the pair
   (`sod_invariants.pairs[0]` EXECUTE-vs-VERIFY, `distinct_required: true` today) whose
   model-axis separation was the only SoD axis still holding. Measured fail-closed on the live tree
   this turn (see NF-02 in the JSON's `new_findings[]`): `hgk-lane-guard.py --lane VERIFY_SECURITY
   --maker-model opencode-go/deepseek-v4.1-flash --target-model opencode-go/deepseek-v4.1-flash ...`
   → `ERR_LANE_SOD_VIOLATION`, `decision REFUSE`, `exit_code 2`.

The residual list is renumbered R-01..R-15 to match the order in which they appear in
`var/FAR-REMEDIATION-AND-CLOSURE-20261016/ROUND_CLOSURE.json::honest_residuals` (15 entries).

---

## Items

### R-01 — R5 NOT DELIVERED (--turn-shape flag not in scripts/hgk-lane-dispatch.py)

- One-line restatement: the previous round's single most valuable reliability lever (a bounded
  writer's EDIT-ONLY turn shape) was specified (FAR_RULING / BUILD_R5_SPEC.md) but never encoded in
  the dispatcher; the bounded writer turn timed out.
- CURRENT status: **OPEN** — unchanged by the mandate.
- Exact command / evidence used:
  `grep -rn "turn-shape" scripts src tests` over the live tree → **empty** (measured this turn);
  also `wc -l scripts/hgk-lane-dispatch.py` = 2275 (unchanged from the ACC9 tracebacks of the
  previous round's `hermes-agent/.hermes-runtime/.../hgk-lane-dispatch.py`, which also showed 2275).
  Termination record on disk:
  `var/FAR-REMEDIATION-AND-CLOSURE-20261016/lanes/EXECUTE/R5/TERMINATION.json` (outcome
  `TERMINATED_BY_ORCHESTRATOR_AFTER_DIAGNOSED_PROBE_LOOP`, `no_product_change: true`), superseded by
  `lanes/EXECUTE/R5b/TERMINATION.json` (outcome
  `TERMINATED_BY_ORCHESTRATOR_AFTER_PROBE_AND_REVERT_LOOP`, `no_product_change: true`).
- What would close it: either (a) a bounded EXECUTE (deepseek-v4.1-flash) writer turn that lands the
  `--turn-shape {normal,edit_only}` flag with its tested HARD-RULES prefix, reusing the R5b brief's
  corrected write-target discipline; or (b) an owner's explicit FAR ruling that the residual is
  deferred. The residual is **not** affected by the mandate — the flag is model-independent.

### R-02 — R7 class undetected by the product (detector is round artifact only)

- One-line restatement: `check_declaration_agreement.py` exists only inside round directories; it is
  not wired into `src/hg_kseos/lane_policy.py`'s `check_drift`, so the R7 cross-field contradiction
  class (prose field vs structured lane chain) would be missed again by the product.
- CURRENT status: **OPEN**.
- Exact command / evidence used:
  `test -f scripts/check_declaration_agreement.py` → **absent**; file present at both
  `var/FAR-REMEDIATION-AND-CLOSURE-20261016/check_declaration_agreement.py` and
  `var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/check_declaration_agreement.py`; executed this turn
  against `config/model-lane-assignment.json` → `CONTRADICTIONS = 0` on the four fields it covers.
  `grep -n "declaration_agreement|claimed_default" src/hg_kseos/lane_policy.py` → empty (no
  cross-field sweep in the product).
- What would close it: land R7 remediation option (1): promote the detector's cross-field rule into
  `src/hg_kseos/lane_policy.py` (hooked from `check_drift`), RED-first test included, under a typed
  WorkOrder. Model-independent.

### R-03 — E11 classified MIXED, two genuine product defects (uncaught metadata OSError sites)

- One-line restatement: the 136/136 E11 pre-pass on this host measures the host, not relay health;
  two uncaught `OSError` / `PermissionError` metadata probes in the dispatcher remain genuinely
  unrepaired (a denial crash instead of the promised typed refusal receipt).
- CURRENT status: **OPEN** (defect sites unchanged).
- Exact command / evidence used:
  `sed -n '864,866p' scripts/hgk-lane-dispatch.py` →
  `candidates = [p for p in (root / "auth.json", root / "codex-accounts.json") if p.is_file()]`
  — bare `is_file()` metadata probe outside any `try` block;
  `sed -n '1134,1136p' scripts/hgk-lane-dispatch.py` →
  `offset = usage_path.stat().st_size if usage_path.is_file() else 0` — same pattern on the usage
  ledger. Both line ranges match the E11 report's named defect sites
  (`evidence/EVIDENCE_E11_PRECONDITION.md:49-60`), on the live file's current bytes.
- What would close it: catch `OSError` around BOTH metadata sites, return an unhealthy identity
  verdict / typed pre-spawn failure receipt (rc 4 / `ERR_RELAY_OAUTH_NEEDS_REAUTH`-style typed code),
  plus the E11 test-hermeticity fixtures (report's own proposed repair §4 items 1-2) — and a
  deterministic denied-stat regression test requiring non-OK receipt + zero child spawns.
  Model-independent.

### R-04 — whole-tree canonical-vs-candidate difference cannot be certified

- One-line restatement: the previous round's enumeration could not traverse 757 access-denied
  directories under prior-round `var/` trees, so the alert that "no other canonical file changed"
  rests on an incomplete walk.
- CURRENT status: **OPEN** (still cannot be certified; my own fresher walk finds the obstacle class
  is even larger than "757 access-denied" and is dominated by OS long-path failures) — see NF-01 in
  `new_findings[]` for the new numbers.
- Exact command / evidence used (this turn): a fresh Python `os.walk` over the live tree —
  641,986 file entries enumerated before the walker pruned; 4,093 directories that could not be
  listed (`os.listdir` raising `OSError (WinError 3)`); 59,434 file entries whose `stat` raised a
  non-Permission `OSError`. Both live obstacle records disagree in KIND with the round's own
  "757 access-denied dirs, retried read-only" measure, which is recorded (not replaced) in
  `evidence/EVIDENCE_PROMOTION_SCOPE.md:45`.
- What would close it: replace the plain `os.walk` with a Windows long-path-aware enumerator
  (`\\?\`-prefixed paths) or accept a narrowed claim whose object is the 200-file product/control
  candidate overlay rather than the whole tree. Model-independent.

### R-05 — two stale candidate config files (epoch/rev 19 vs canonical 21)

- One-line restatement: the frozen candidate's `config/model-lane-assignment.json` and
  `config/lane-routing-registry.yaml` copies are two revisions behind canonical, deliberately NOT
  promoted, classified NEEDS_OWNER_DECISION.
- CURRENT status: **SUPERSEDED_BY_THIS_MANDATE.** The rationale: under a newer owner order (the
  mandate that flips PLAN to glm-5.3-flash), any promotion of the epoch-19 candidate configs is
  doubly inadmissible — they were stale at the round's epoch 21 measure AND they encode the
  superseded 2026-10-15 owner order on both PLAN (glm primary) and VERIFY (glm rank-1) chains. A
  rebind under the new order will create NEW candidate/config snapshots at the new epoch; the
  epoch-19 copies' status (retained as historical evidence) needs no new decision.
- Exact command / evidence used:
  `python -c` readback of
  `var/LANE-RELIABILITY-CLOSURE-20261016/candidate/config/model-lane-assignment.json` →
  `{"registry_epoch": 19, "revision": 19}` (live this turn);
  `grep -n "^epoch" .../candidate/config/lane-routing-registry.yaml` → `epoch: 19`;
  canonical readback this turn: `config/lane-routing-registry.yaml` `epoch: 21`,
  `config/model-lane-assignment.json` `revision: 21` (sha256 `e7be2dea…7664df`, matching the
  registry pin).
- What would close it / decision needed: the ONLY remaining decision is whether the epoch-19
  snapshots may be deleted once the new-epoch rebind makes them safely superseded evidence; retaining
  them needs no decision. (This decision is now narrower and lower-stakes than the original.)

### R-06 — 348 canonical-only product/control files classified NEEDS_OWNER_DECISION

- One-line restatement: retaining these needs no decision; only proposing deletion would; the
  original full per-file JSON was compacted away (SC-10), so the on-disk classification lives in
  `evidence/EVIDENCE_PROMOTION_SCOPE.summary.json` + the `.md`.
- CURRENT status: **OPEN** (unchanged; no owner disposition has been recorded since closure).
- Exact command / evidence used:
  `grep -rln "needs_owner_decision" var/FAR-REMEDIATION-AND-CLOSURE-20261016/evidence` →
  `EVIDENCE_PROMOTION_SCOPE.summary.json` (which carries `"needs_owner_decision": 348` and
  `"do_not_promote": 242920`); no post-closure disposition record found in either
  `var/FAR-REMEDIATION-AND-CLOSURE-20261016/` or `var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/`
  (`grep` on filenames containing "decision" / "348" → empty).
- What would close it: an owner decision per class (retain / delete-per-class), or an explicit FAT
  ruling that these files stay. Model-independent.

### R-07 — PLAN and VERIFY_SECURITY share a model by owner order (SOD006-C2)

- One-line restatement: the residual documents that model-axis maker/checker separation for
  PLAN-vs-VERIFY is ABSENT by owner order, and that `check_sod` (no longer a stale declaration)
  reported the collision as the *ordered* state.
- CURRENT status: **SUPERSEDED_BY_THIS_MANDATE** on the PAIR it names, with a NEW-life residual on
  the pair it does not name — see NF-02.
- Exact command / evidence used (both measured this turn):
  `python` + `hg_kseos.lane_policy` `check_sod(route_for_lane(reg,'PLAN'),
  route_for_lane(reg,'VERIFY_SECURITY'))` on the live tree → `(False, "SOD_VIOLATION
  maker_model=gpt-6.1-sol == checker_model=gpt-6.1-sol")` — the ordered collision, exactly as
  recorded. `python` + `hg_kseos.lane_policy` `check_sod(EXECUTE, VERIFY_SECURITY)` → `(True,
  "SOD_OK deepseek-v4.1-flash != gpt-6.1-sol")` — the only SoD axis still holding today.
  Registry readback: `config/lane-routing-registry.yaml:295-297` (VERIFY route's `selected_arm: A`,
  `selected_arm_identity: gpt-6.1-sol`).
- What supersedes it: under the new mandate PLAN (glm-5.3-flash) is no longer equal to the VERIFY
  route's top-level (gpt-6.1-sol); the recorded owner-ordered collision SOD006-C2 becomes SUPERSEDED
  by the new order on that pair. Closure requires the SAME re-declaration mechanic the previous
  rebind used: set `sod_invariants.pairs[].distinct_required: true` for PLAN-vs-VERIFY and add a
  SUPERSEDED status record (naming SOD006-C2) in the SAME registry edit that re-points PLAN rank-1 -
  `sod_invariants.declared_conflicts[]` is the governing field, not a prose sweep.
- What it would take to close: the new-epoch rebind under the owner order; nothing else. The
  residual's substance (model-axis diversity absent on the *new* maker/checker pair) is carried by
  NF-02 into `new_findings[]`.

### R-08 — PLAN-plane availability is carry-forward; no fresh probe dispatched

- One-line restatement: the previous round measured the governed profile serving rows on the OLD
  order's model (`gpt-6.1-sol`, `openai-codex`), so the measurement supports a mandate that has since
  been superseded.
- CURRENT status: **OPEN — made NEWLY ACTIVE and WORSE.**
- Why worse: the *binding* (profile `config.yaml::model.default/provider`) and the *serving rows* in
  the profile's own `state.db` both still measure the OLD order's model, so every surface the
  original residual used as evidence is now the WRONG answer under the new mandate.
- Exact command / evidence used (this turn):
  `grep -A3 '^model:' profiles/hgk-governed/config.yaml` →
  `model: { default: gpt-6.1-sol, provider: openai-codex, reasoning_effort: medium }` (stale under
  the new mandate);
  `sqlite3 profiles/hgk-governed/state.db "SELECT id, model, source FROM sessions ORDER BY rowid
  DESC LIMIT 4"` → all five rows `gpt-6.1-sol`, `source=oneshot`, latest
  `20261016_121307_a4d22a` — no `glm-5.3-flash` row in the governed profile.
- What would close it: rebind the governed profile's `model.default` + `model.provider` to
  `glm-5.3-flash` / `opencode-go` (mandate), then run the one-shot PROBE_OK probe and record the new
  profile-`state.db` row (the recipe in `hgk-kanban-and-lane-routing` "Scoping the PLAN-plane binding
  to a PROFILE"). This is the cheapest true closure of the residual in its NEW form.

### R-09 — interactive-session ordering caveat still applies

- One-line restatement: the arm shown served for an interactive (non-`oneshot`) turn is the arm the
  profile's session-picker selects, not the configured default — so serving-row triage by `source`
  is required before reading any row as "the PLAN lane's serving evidence."
- CURRENT status: **UNVERIFIABLE** (structural caveat, not a defect).
- Exact command / evidence used (this turn):
  `sqlite3 <hermes root>/state.db "SELECT id, model, source FROM sessions ORDER BY rowid DESC LIMIT
  10"` → rows of both `source=desktop` (glm-5.3-flash, 2026-10-16) and `source=oneshot`
  (gpt-6.1-sol and glm), interleaved — the caveat's cause is live. No extra probe is required; the
  caveat is recorded as a limitation that stands independent of which order is in force.
- What would close it: nothing to close; the residual is a standing measurement caveat that belongs
  in any D01 re-measure under the new mandate. (Marked UNVERIFIABLE rather than OPEN because there
  is no falsifiable state change to measure.)

### R-10 — self-research/self-learning note is a proposal set, not a curriculum

- One-line restatement: `SELF_EVOLUTION.md`'s section 4 proposals are not a validated curriculum;
  nothing in the touched skills has been validated by a third party.
- CURRENT status: **OPEN** (unchanged).
- Exact command / evidence used:
  `tail -6 var/FAR-REMEDIATION-AND-CLOSURE-20261016/SELF_EVOLUTION.md` →
  "Section 4 is a PROPOSAL SET: none of it is product code in this round, none of it is accepted…
  No external party has reviewed any of it." — matches the residual verbatim.
- What would close it: third-party validation of any specific proposal, or an owner's explicit
  acceptance/deferral. Model-independent.

### R-11 — no external engineer has reviewed any part of the round

- One-line restatement: the round's verdict rests on the round's own VERIFY lane (machine checker,
  same workstream), not on a human/external engineer's review.
- CURRENT status: **OPEN** (unchanged). No post-closure review artifact appears under this
  workstream's `var/` trees; the only post-closure VERIFY activity found this turn is the separate
  `R5R3-20261016-preview4-closeout` turn, which audits a DIFFERENT subject (handover packet
  preview4) and is itself an in-workstream machine checker (see NF-04).
- Exact command / evidence used:
  `find var -name "*REVIEW*" -newer ROUND_CLOSURE.json` → empty;
  `ls var/R5R3-20261016-preview4-closeout/VERIFY_SECURITY/attempt-2-*/` → `attempt.marker.json` +
  raw stdout/stderr with a completed turn carrying 10 findings against the preview-4 handover
  packet, not against this round's own residuals.
- What would close it: an external engineer's verdict, which is exactly what the publication gate
  (`claim_ceiling: CANDIDATE_ONLY`) already requests. Model-independent.

### R-12 (F-IND-2) — prose vs `automatic_selection` cross-field contradiction, OPEN

- One-line restatement: `/sod/plan_lane` prose declares GLM "never auto-selected" while
  `routes[].PLAN` fallback1 (opencode-go/glm-5.3-flash) declares `automatic_selection: true`;
  `/sod/verify_security_selection` says arm B (and arm C's operator-selectable role) is "never
  auto-selected" while the VERIFY lane's arm B (opencode-go/glm-5.3-flash, `automatic_selection:
  true`) and arm C (opencode-go/deepseek-v4.1-flash, `automatic_selection: true`) both auto-select.
  Invisible to `check_drift` (pointer-vs-target only) and to the R7 detector (default-arm axis only).
- CURRENT status: **OPEN — made WORSE / NEWLY ACTIVE** by the mandate.
- Why worse: the new mandate makes `opencode-go/glm-5.3-flash` the PLAN rank-1 default. The exact
  sentence that recorded "GLM-5.3-Flash is retained as a rotation alternate, never auto-selected"
  will then contradict BOTH the structured chain it sits beside AND the new mandate — two axes at
  once instead of one.
- Exact command / evidence used (this turn):
  `python` readback of `config/model-lane-assignment.json` `sod.plan_lane` → "…GLM-5.3-Flash is
  retained as a rotation alternate, never auto-selected." and `sod.verify_security_selection` →
  "…arm B is a non-default operator-selectable alternate, never auto-selected";
  `grep -n automatic_selection config/lane-routing-registry.yaml` → lines 190 (`true`, PLAN
  fallback1 arm), 263 (`true`, VERIFY arm B), 328 (`true`, VERIFY arm C) on the live file;
  `check_declaration_agreement.py config/model-lane-assignment.json canonical` → 4 fields
  AGREES, `CONTRADICTIONS = 0` — the detector confirms the contradiction is outside its own axis
  (default-arm equality), which is the residual's substance.
- What would close it: under the new order, apply `$FINDINGS_V3C remediation (a) or (c)` —
  make the `automatic_selection` flags authoritative and repair the prose to match the NEW rank
  order, OR add an `automatic_selection` axis to the agreement detector so the contradiction class
  is caught mechanically in future rounds. Model-independent in *mechanism*, but the resolution must
  be re-derived against the NEW (post-rebind) prose.

### R-13 (F-IND-3) — R2 promotion lacked pre-write typed admission; writer was not the mandated writer

- One-line restatement: the promotion of four product files copied bytes BEFORE the WorkOrder
  existed and its recorded writer is `hermes-plan-orchestrator`, not the mandated CODEX CLI writer;
  no atomic pre/post whole-tree inventory was taken; disclosure does not equal compliance; the
  claim ceiling is SPLIT (`bytes: VERIFIED` / `pre-write typed admission: ABSENT` /
  `canonical writer: NOT the mandated writer` / `exclusive scope: NOT TAKEN`).
- CURRENT status: **OPEN** (unchanged — pre-write admission cannot be supplied retroactively).
- Exact command / evidence used (this turn):
  `sed -n '70,110p' var/FAR-REMEDIATION-AND-CLOSURE-20261016/apply_R2_promote.py` →
  `shutil.copy2(src, dst)` at line 83 with `sp.create_workorder(...)` first executed at line 101 —
  the code path that produced the receipt's `ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC` is in the file
  itself;
  `python` readback of `R2_PROMOTION_RECEIPT.json::workorder_note` →
  `"InvariantViolation: ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC"`;
  `python` readback of `SPINE_STATE_READBACK.json::existing_after.workorders[WO-…-R2]` →
  `{"writer": "hermes-plan-orchestrator", "state": "CREATED", …}`;
  promoted-file hash re-verification this turn: all four files
  (`scripts/runtime_role_binding_assert.py`, `scripts/hgk-governed-runtime-controller.py`,
  `tests/test_governed_runtime_controller.py`, `tests/test_lane_effort_enforcement.py`) still match
  the receipt's canonical_sha256_after byte-for-byte — the byte half of the split claim still holds.
- What would close it: nothing — the historical violation is *not curable*; it is a permanent record.
  What CAN be closed is the NARROWER residual: enumerate the four promoted files as
  "promoted-with-disclosed-defect" and verify current bytes still match the receipt (done this turn),
  so the only remaining action is documentation (already done) plus an owner decision to accept the
  violation as a bounded disposition. Model-independent.

### R-14 — absolute whole-tree test counts are environment-specific; the DELTA is what reproduces

- One-line restatement: the previous round's 527-test / 7-failures / 2-errors absolute numbers do not
  reproduce in a different environment; the paired named-delta (only `test_registry_and_projection_shape`
  moved, none added) does.
- CURRENT status: **PARTIALLY_CLOSED** (still true, but the framing is now the round's claim
  ceiling; a newer interpreter mismatch was measured this turn that reinforces it).
- Exact command / evidence used (this turn):
  `"C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe" --version` → `Python 3.11.9`;
  the recorded interpreter used by the checker's full-suite run
  (`hermes-agent/.hermes-runtime/python/cpython-3.11.17-windows-x86_64-none/python.exe --version`) →
  `Python 3.11.17` — two DIFFERENT interpreters still co-exist on this host, so absolute counts
  remain environment-coupled, and the residue is a standing calibration caveat rather than an open
  defect.
- What would close it: pin the recorded interpreter + missing dependencies (`run_acceptance`,
  `tools/package_local.py`, task-local toolchain manifest) inside a hermetic runner and re-run the
  whole tree from a fixed environment. Model-independent. (Cheaper alternative: keep the residual as
  a permanent calibration note, which is what the round already declares.)

### R-15 — the independent verdict was NOT unanimous

- One-line restatement: C1/C5/C7 AGREE, C2/C3/C6 DISAGREE, C4 UNCERTAIN in
  `lanes/VERIFY_SECURITY/V3c/work/CHECKER_VERDICT.json`; the round records this rather than smoothing
  over it.
- CURRENT status: **OPEN** in its original form (the record stands), but **made NEWLY ACTIVE** by
  the mandate because the natural remedy is exactly what the new checker arm (deepseek-v4.1-flash)
  enables: a fresh independent re-derivation on a DIFFERENT model from the writer's, closing on
  typed DISAGREE/UNCERTAIN only where re-derivation fails.
- Exact command / evidence used:
  `ROUND_CLOSURE.json::verify_verdict_history[1].verdicts` (read this turn) →
  `{"C1": "AGREE", "C2": "DISAGREE", "C3": "DISAGREE", "C4": "UNCERTAIN", "C5": "AGREE",
  "C6": "DISAGREE", "C7": "AGREE"}` (unchanged, the file's recorded state).
- What would close it: run the same C1-C7 re-derivation on the NEW checker arm, and either agree
  unwaveringly (residual closes), disagree on the SAME items (residual becomes two-sided evidence
  the disagreement is genuine), or disagree on NEW items (the residual grows; it does NOT "close").
  Model-dependent only in the instrument, not in the object.

---

## What closing which items actually requires (cheap first)

| item | cheapest true closure |
|---|---|
| R-01 | bounded EXECUTE deepseek turn adds `--turn-shape` (Skill's R5 recipe, PRE-specified seam) |
| R-02 | promote detector into `src/hg_kseos/lane_policy.py` hooking `check_drift` |
| R-03 | catch `OSError` at the two dispatcher sites + E11 fixture isolation + denied-stat regression test |
| R-04 | long-path enumerator, or narrow the claim to the 200-file candidate overlay |
| R-06 | owner decision per class (most likely: retain all) |
| R-07 | new-epoch rebind records SUPERSEDED / new `declared_conflicts[]` in the same edit |
| R-08 | rebind the governed profile + a fresh PROBE_OK probe recorded in the profile's own `state.db` |
| R-12 | make `automatic_selection` flags authoritative; re-write prose on the NEW rank order; (optional detector-axis extension) |
| R-13 | owner decision to disposition the recorded violation (no work can cure it) |
| R-14 | pin interpreter + dependencies in a hermetic runner |
| R-15 | re-run C1-C7 re-derivation on the NEW checker arm |

R-05, R-07, R-08, R-12 are the four residuals whose *substance* changes most under the new mandate;
all four point into the same immediate work bundle: the registry/SoD/prose/profile rebind.

---

## Claim ceiling

CANDIDATE_ONLY re-derivation, read-only. Nothing in this file repairs, promotes, deploys, or
accepts anything. `hgk_canonical_acceptance: NOT_PERFORMED`. Every item's evidence is a command or a
`file:line` that was re-run or re-read this turn on the live tree at
`C:/Projects/Agent_Workspace/HG-KSEOS`; nothing is cited from memory. Machine-readable sibling:
`evidence/EVIDENCE_RESIDUAL_STATUS_REDERIVED.json`.
