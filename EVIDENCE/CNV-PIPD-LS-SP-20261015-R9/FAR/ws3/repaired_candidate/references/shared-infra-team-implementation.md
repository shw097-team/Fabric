# Shared Infrastructure Profile Team blueprint implementation (FDA/FAR class)

Verified end-to-end 2026-08-13 on fabric-autonomous-research (FAR) r2 — the second
Shared Infrastructure Profile Team landed after fabric-desktop-automation (FDA).
The blueprint defines its own implementation WorkOrders (FAR-WO-001..008) and local
qualification gates (FAR-Q0..Q10 + FAR-R1); the external verifier stays the final gate.

## 1. Admission: one WorkOrder per blueprint batch (not one mega-WO)

- Script (gitignored `var/far/admit_*.py`) drives the typed SharedSpine API for EACH
  blueprint batch: `register_requirement` → lease/`transition_requirement` FROZEN
  (idempotency key `FRZ-<REQ>`) → release → `create_taskspec` → `create_workorder`
  (writer=codex, base_head = current HGK HEAD). 8/8 admitted in one run.
- Readback pitfall: `sqlite3.Row` objects print as `<sqlite3.Row object at ...>` —
  wrap with `tuple(r)` in SELECT loops.
- `record_workorder_result(...)` returns **None** (not a dict) — verify by re-SELECTing
  `workorders.state` (expect VERIFIED), never by calling `.get()` on its return.
- `register_evidence` is UNIQUE on evidence_id. Re-registering the same id after a
  receipt was regenerated raises `IntegrityError` → register a NEW superseding id
  (`EVD-FAR-GATES-R2`) exactly like the PCIV-F01 manifest pattern. Never rewrite the
  old row.

## 2. CAPC contract for NEW_IMPLEMENTATION (the 4-iteration unblock list)

Build the contract with a **generator script** (`var/<task>/capc/gen_contract.py`),
never by hand. See `references/capc-contract-building.md` for the semantic traps and
the appended "full field shapes" section for the exact fields that make lint pass on
the first tries. Pipeline: `lint` → `activation` → `acceptance` (all
PROMPT_COMPILE_PASS) → `duplication --source <sealed prior>` (ratio ≪ threshold) →
`hash` → `compile --out-dir`. Compile PASS is Gate-A3-0 evidence only, not runtime.

## 3. Codex spawns per deliverable batch

- One real spawn per codex-authored deliverable batch (router module, security module),
  each with its own prompt file (English-only, single-quote-only) + `.ps1` launcher
  (`--sandbox danger-full-access --ask-for-approval never`, `--cd` the real repo root).
  Provider receipt readback from `opencodex-hermes/usage.jsonl` (provider/model/status 200).
- **Codex-written tests come back without `tests/__init__.py`** → `unittest discover`
  fails `Start directory is not importable` and `-m unittest tests/test_x.py` resolves
  to a dotted module that can't import. Smallest repair: Hermes adds an empty
  `tests/__init__.py` and records a defect id (FAR-CODEX-TESTPKG-001). Then
  `python -m unittest discover -s tests -t .` works.

## 4. R0–R8 research-product canary

- Materialize §10 artifact contracts as ONE YAML contract file + a generator that
  emits all templates (stays consistent). Then a canary runner writes the run
  directory with REAL data (hash-verified sources, real query ledger, real pins) and
  computes per-artifact digests into `ResearchRunReceipt.json`.
- **Count artifacts from the actual directory**, not from the plan: the maker said 18,
  the independent swarm lane counted 19 (17 required + CandidateKnowledge +
  ProposedEvolution; conditional ledgers correctly absent because R5 was never
  triggered). Record as SWARM-FINDING-xxx ACCEPTED_CORRECTION.
- No experiment run → no `ExperimentResult` file at all (never fabricate).

## 5. ARIS-style method pack pinning

Shallow clone upstream → pin full commit → hash selected SKILL.md files + catalog →
disposition ledger (§17.2 table) → effective-load receipt: frontmatter parse of every
selected SKILL.md + pin-match + catalog count. STRUCTURAL_PASS is load evidence, not
runtime qualification.

## 6. Long-horizon detach/reattach canary (lightweight)

One worker script with a `--resume` flag: fresh run writes `checkpoint.json`
(phase + normative pointer) + progress log and exits (DETACH); a later `--resume` run
reads the checkpoint, continues, writes `ResearchCompletionContract.marker`
(terminal + resumed_from_checkpoint). Evidence = two distinct PIDs + frozen checkpoint
+ marker. Launch the first leg with `terminal(background=true, notify_on_complete=true)`
so the detach completion notification doubles as the lifecycle receipt.

## 7. Governed-evolution canary (CLI + typed controller)

- `hg_kseos evolution signal --project-id <P> --signal-type KNOWLEDGE_GAP ...` then
  `evolution candidate --gap-id <id> --type KnowledgeCandidate ...` (CLI). Then the
  typed chain: `GovernedEvolutionController(sp).qualify(cand_id, tests_pass=True,
  negative_pass=True, security_pass=True, holdout_pass=True, nrtv_pass=True,
  baseline_verified=True, rollback_verified=True, sandbox_path=..., evaluator_self_mutation=False,
  authority_mutation=False)` → `independent_check(cand_id, checker='acceptance-officer',
  raw_evidence_refs=[...])` → `promotion_gate(cand_id, human_approval=None)`.
- **Do NOT parse CLI output for gap/candidate IDs** (the JSON shape is easy to
  mis-parse; "CANDIDATE" was grabbed as the id once). Query the spine directly:
  `SELECT candidate_id FROM improvement_candidates WHERE gap_id=? ORDER BY created_at DESC LIMIT 1`.
- Expected terminal: `PROMOTION_READY_HITL_SOURCE_REQUIRED` (COV-11-06). That IS the
  governed PASS; do not self-promote. Guard candidate creation with an existence check
  so re-runs are idempotent.

## 8. Evidence freeze order (PCIV-F01 class recurrence)

1. Complete ALL mutations first (workorder results, kanban, gates receipt regeneration).
2. Regenerate the artifact index LAST among mutable artifacts (any receipt regeneration
   silently desyncs hashes embedded earlier — gates receipt hash changed after the
   first index generation).
3. Register superseding EVD rows for regenerated receipts (EVD-*-R2).
4. Generate the single evidence MD (read hashes FROM the index — no transcription).
5. Mirror byte-identical to HGK/Fabric/SQS `evidence\review\`, then SHA-256 all four
   locations and require equality. No edits after hashing.

## 9. Kanban & guardrails

- **Duplicate-create trap:** `hermes kanban create --json | tail -3` truncated the id;
  re-running the create made a SECOND task. If you don't see the id, `kanban list`
  FIRST; archive the duplicate (`kanban archive <id>`; there is no delete).
- Board gets switched away mid-task by other sessions — `boards switch <slug>` before
  every heartbeat/complete batch; `unset HERMES_DELEGATED_CHILD_CONTEXT` after any
  delegate_task batch.
- **SOUL.md is a protected agent-instruction filename**: `write_file` refuses it
  (approval prompt timeout = silence is not consent). Do NOT retry/bypass — record
  `NOT_WRITTEN_GUARDED` in evidence and ship the profile with the other three files
  (config.yaml / distribution.yaml / README.runtime-contract.md).
- YAML write_file validation rejects: colon-in-scalar (`uses A2A (current: none)`),
  `#` starting a comment inside a flow sequence (`[#1288 ...]`), and plain text at
  column 0 under a `## heading` comment (parsed as a mapping key). Quote the value or
  indent under a real key.

## 10. First-use dogfood / self-upgrade convention (FAR-20260813-002, challenge-verified)

After a capability lands, **use it to research its own improvements** before promoting:
run the capability's own R0-R8 lifecycle on a real improvement question (e.g. "should
this landing recipe be added to the skill?"), route the task class through its own
router (`RESEARCH_WORKFLOW_OPTIMIZATION -> HGK_GOVERNED_EVOLUTION`, reason
FAR_ROUTE_EVO_LAB), let a fresh-context challenge lane review the candidate, then land
via the governed path with the owner's (user's) authorization. Evidence:
`Fabric/fabric-autonomous-research/canary/FAR-20260813-002/` (incl. DisagreementLedger
DG01 — the challenge lane caught that a proposed duplicate reference already existed;
outcome: merge unique delta here + delete the duplicate draft, never add a second copy).
Future self-upgrade/self-evolution requests follow this same governed process
(WO admission → CAPC → R0-R8 run → challenge lane → HITL gate → patch → verify).

## 11. Q0 crosswalk + team-artifact materialization checklist (challenge lane F1 value fold-in)

- **Q0 first**: hash blueprint + design-intent inputs (verify manifest SHAs match the
  blueprint's input table), fresh-read current machine truth (doctor, spine counts,
  named_methods registry, Hermes binding config), map every FAR logical field to a
  current contract (reuse-first; no new normative schema), dispose CR-* items with
  current-equivalent locators. Evidence: `FAR_Q0_CROSSWALK.md`.
- **Materialization checklist** (the one area no other reference covers):
  - TEAM.md — `schema: <TEAM>/1`, `heavy_stack: false`, `manager_agent: NONE`,
    capability-matrix ref, hard invariants, SoD ceiling (model: FDA/FAR TEAM.md).
  - Capability matrix — the router's canonical input: capability classes →
    provider/method states → decision + reason codes (never ephemeral dicts).
  - ExecutionBinding — RP002-EXECUTION-BINDING/2 parent, child overlay only
    (no fork): normative WO ref, routing topology, delegation/lease/budget/watchdog,
    idempotency, runtime refs.
  - Interop disposition — OASF/ContextForge/MCP/A2A/OpenTelemetry/Qdrant/Neo4j/Obsidian
    each EXPLICIT (no blank rows; current-state-unverified blocks promotion).
  - Profile(s) under `Fabric/profiles/<id>/` — config.yaml / distribution.yaml /
    README.runtime-contract.md (+ SOUL.md unless the protected-file guard refuses it:
    record NOT_WRITTEN_GUARDED, ship with the other three).
  - Research-product contracts + templates — R0-R8 artifact set per blueprint §10
    (one contract YAML + generator emits all templates; 22 templates for FAR).

## 12. Specialists honesty rule (N/A_NOT_SELECTED_WITH_REASON)

Unqualified specialist providers get an honest record, never a fake qualification:
pin the upstream version/full commit (e.g. Prime v0.7.2 = 83a0f9f9…), list the CR
reasons (no host runtime / sandbox substrate absent / target-OS integration unproven),
mark hard-case IDs (Q-PRIME-01..14 style) as NOT_EXERCISED, and let the router keep
them CANDIDATE_DISABLED_UNTIL_QUALIFIED with FAR_BLOCK_PROVIDER_UNQUALIFIED /
FAR_DEGRADE_NATIVE semantics. `N/A_NOT_SELECTED_WITH_REASON` is an accepted
conditional-gate outcome (FAR-Q7); upstream SUPPORT never overrides A0-A4.

## 13. First-use round close-out + micro-pitfalls (FAR-20260813-002, AO-audited)

- **Close-out is NOT optional for follow-up rounds** (invariant 9 in SKILL.md). A
  first-use/dogfood round still needs: (a) fresh-context AO lane
  (`ACCEPTANCE_OFFICER_VERDICT=PASS`, 7/7 checklist items incl. receipt iteration
  fields, ledgers, closure JSON, patched files, spine state), (b) its own single
  evidence MD (`FAR_FIRST_USE_EVIDENCE.md`) mirrored byte-identical to the 3 roots,
  (c) its own artifact index. The user audits with "內部驗收? 單一MD? 結果?" — close
  the loop before being asked.
- **SharedSpine constructor takes a `Path`, not `str`** — `SharedSpine("...")`
  raises `AttributeError: 'str' object has no attribute 'resolve'`; use
  `SharedSpine(Path(r"..."))`.
- **Python f-string expressions cannot contain backslashes** — compute the dict key
  (`obs_key = "…\\…"`) in a variable first, then interpolate `{obs_key}`.
- **Artifact-index regeneration timing (manifest-before-subject recurrence):** the
  index must be regenerated AFTER the last receipt write (e.g. the AO lane receipt)
  and BEFORE the evidence MD; exclude vendor trees (`aris-vendor`) and `__pycache__`
  from the scan or the count explodes (818 vs 97 observed).
- **Evidence MD hash is verified at 4 locations** — source file + the 3 mirror
  roots — all must be byte-identical.
