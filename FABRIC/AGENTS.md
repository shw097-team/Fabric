# AGENTS.md — Fabric (agent-operating projection)

Version: 2026-10-10.1  (adds: AO lane independence — spawn-前 fail-closed 身分閘門、required＝served、非變異守衛、確定性負測；advisory 綁定規則不變)
Scope: this repository (`Fabric\`) and all descendants unless a nearer AGENTS.md narrows execution details.

> Status: operational projection for agents working inside the Fabric repository. This file is NOT a new
> authority source, NOT a policy, and NOT a gate. Normative truth lives in the Master/Stage contracts and
> current machine truth: `rp002\RP002_STAGE_CROSSWALK.yaml` (master sha256 `3bc4ad6c…`), the frozen
> contracts under `control\` / `contracts\` / `assurance\`, and the sealed Stage artifacts under
> `stage\RP002-STAGE-HGK\`. Stage-2 is **externally accepted**
> (`stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`, `PASS_CHALLENGE` / `GRANTED`);
> next gate `SQP1` is NOT_AUTHORIZED. This docs task does NOT execute Stage-3 / SQP1 and does NOT claim
> production / live / remote.

## Identity

- **Fabric** = governance / assurance / interop / knowledge **contract surface** (policy + schema +
  assurance packs + profile + knowledge governance rules). It is NOT an OS, daemon, second scheduler,
  second task DB, second reducer, second HGK, second knowledge platform, or a substitute for
  Hermes / Codex.
- **HG-KSEOS** = the sole governance / normative **control plane** (WorkOrder admission, SharedSpine,
  reducers, acceptance, release). Fabric never becomes a second control plane.
- **Hermes** = **runtime / orchestrator** (Kanban, /goal, checkpoint, tool recovery, compression,
  approvals), governed-bound by HGK (`..\HG-KSEOS\config\hermes.json`, `HGK-HERMES-BINDING/2`,
  v0.20.0 @ `3c27eb62`).
- **Codex** = **bounded tracked writer** for admitted WorkOrders (`writer=codex`), never a product root
  or authority.
- **Acceptance Officer** = **independent verifier** (VERIFY_ONLY), default L2 checker after O1; cannot
  write or repair candidates, cannot promote or release.

## Mandatory reading order (before any Fabric work)

1. Fabric README/index — if present; otherwise `Fabric\IDEA.md` (stub) + this file +
   `rp002\RP002_GATE_CATALOG.yaml` as the machine gate index.
2. Master / Stage contracts — `rp002\RP002_STAGE_CROSSWALK.yaml`, `rp002\RP002_EXECUTION_GRAPH.yaml`,
   `rp002\MASTER_REF.yaml`, `stage\RP002-STAGE-FABRIC\MASTER_REF.yaml`.
3. Machine truth — `rp002\CHECKPOINT.json` (historical) and current stage state:
   `stage\RP002-STAGE-HGK\STAGE-2-SEAL-REPAIRED.yaml`,
   `stage\RP002-STAGE-HGK\STAGE2_TO_STAGE3_HANDOFF_REPAIRED.yaml`,
   `stage\RP002-STAGE-HGK\EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`,
   `stage\RP002-STAGE-HGK\RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`.
4. Policy / contracts / assurance / schemas — `control\*`, `contracts\*`, `assurance\*`
   (incl. `assurance\acceptance-packs\`), `profiles\*\README.runtime-contract.md`.
5. Current Stage seal / handoff / evidence — gate receipts under
   `stage\RP002-STAGE-HGK\<GATE>\*_RECEIPT*.yaml|json` and
   `evidence\review\RP002_STAGE-2_KG1_EVIDENCE_FOR_EXTERNAL_REVIEW.md` +
   `evidence\review\RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json`.
6. HGK AGENTS.md — `..\HG-KSEOS\AGENTS.md` (control-plane rules take precedence for HGK-side work).
7. Current WorkOrder / ExecutionBinding — `stage\RP002-STAGE-HGK\B1\B1_EXECUTION_BINDING.json`
   (schema `RP002-EXECUTION-BINDING/2`) and the WorkOrder it binds (`WO-RP2-STAGE2-001` /
   `WO-RP2-S2R-001`).

## Operating rules

- **FILES_FIRST** — read actual files (contracts, receipts, evidence) before acting; never trust
  memory, summaries, or another doc over the files.
- **NO_SOURCE_NO_NORM** — no normative claim (Requirement / ADR / WorkOrder / gate state) without a
  source-bound artifact (SharedSpine EVT, frozen requirement, receipt).
- **NO_SOURCE_NO_CLAIM** — no PASS / status claim without raw evidence refs; file existence, hashes
  alone, row counts, and LLM votes are not substantive PASS.
- **One writer per worktree** — a given admitted writable root has exactly one active writer at a time;
  parallel work must go through HGK admission into separate worktrees / lanes.
- **WorkOrder normative task truth** — the WorkOrder (not Kanban cards, not chat, not this file) is the
  normative task truth; Kanban state is coordination state only.
- **Kanban coordination state ≠ authority** — boards/cards may be stale; treat drift as a
  smallest-repair candidate, never as license to skip gates.
- **ROLE ≠ PROFILE ≠ WORKER** — no permanent profile per role; identity, capability contract, and
  active worker claim are distinct.
- **Maker cannot self-accept** — writer / orchestrator / commander can never be the final checker;
  officer VERIFY_ONLY cannot repair the candidate it checks.
- **Acceptance Officer cannot repair candidate** — defects are reported back to the maker; recheck is
  a fresh independent session.
- **Policy presence ≠ policy consumption** — consumption requires the traced chain (policy digest →
  consumer → decision → evidence), per `stage\RP002-STAGE-HGK\F0\F0_POLICY_CONSUMER_TRACE.json`.
- **Derived knowledge ≠ authority** — Obsidian / LLM Wiki / RAG / KG output and agent-produced notes
  are candidates; only approved namespaces (`hgk.approved.*`) are consumption-grade, and promotion
  needs owner / gate.
- **BreakGlass explicit + audited** — any legacy bypass is `BREAK_GLASS_ONLY` per
  `control\BREAK_GLASS_POLICY.yaml`, recorded in evidence; Stage-2 seal shows
  `open_breakglass_count: 0`.
- **TT/CR carried forward** — open technical debt / change requests carry forward to the next
  gate / stage; never silently dropped.
- **Critical writes readback/hash** — after writing any critical artifact, read it back and record its
  hash; receipts / seals are immutable once sealed.

## Hermes execution chain

```text
Admitted WorkOrder → ExecutionBinding (BIND-RP2-S2-001) → Profile dispatch (hgk-orchestrator)
→ Hermes Kanban board (RP002-FABRIC-BOOTSTRAP, task claim + heartbeat)
→ Codex bounded writer (writer=codex) → tests/evidence
→ Acceptance Officer VERIFY_ONLY (fresh session, 8 packs) → reducers → release
```

Hermes runtime state ≠ HGK normative state; `/goal done` ≠ HGK PASS. Evidence:
`..\HG-KSEOS\evidence\review\HG-KSEOS_HERMES_V020_*.json` and
`stage\RP002-STAGE-HGK\B1\B1_WORKER.log`.

## AO lane independence (round `FAR-AO-INDEPENDENCE-20261010`, 2026-10-10)

- **What it is**: the AO / VERIFY / SECURITY dispatch surface (`HG-KSEOS/scripts/hgk-lane-dispatch.py`)
  can now be *proven* independent in an unattended window, instead of only looking independent.
- **Four behaviours**: (1) a **pre-spawn** identity/health gate — an unhealthy arm is refused
  (`exit 4` / `ERR_RELAY_OAUTH_NEEDS_REAUTH`) and **never** silently swapped for another arm;
  (2) `--require-arm` means the named arm must **SERVE** the turn, else `exit 3` /
  `ERR_REQUIRED_ARM_NOT_SERVED` (pin the rank too when a specific model is required);
  (3) a non-mutation guard whose root must resolve (`ERR_GUARD_ROOT_MISSING`, 0 attempts) and whose
  `removed`/`changed` **voids the turn's own verdict**; (4) the turn's raw bytes are persisted and
  independently re-derivable.
- **Measured**: unattended `openai-codex/gpt-6.1-sol` — `required_arm == served_arm`, `exit 0`,
  `usage 200`, no interactive window (`HG-KSEOS/evidence/FAR-AO-INDEPENDENCE-20261010/`).
- **Binding rule is UNCHANGED**: a checker/AO verdict remains **advisory** — never an OracleReceipt,
  never a canonical acceptance status, and no Fabric contract may consume it as either. The round's
  `ACC-AO-INDEP-012 = PASS` is valid because an **independent checker lane** produced the verdict and
  it was recorded through the **typed spine API** with a canonical event — not because a verdict was
  advisory-but-convenient.
- **Honest status**: **process-only independence** (all three lanes run one model, per the owner's
  D-3 ruling) → model diversity must never be claimed; the guard is **detection, not prevention**;
  the dedicated pool-account item is **NOT APPLICABLE** (the owner holds one account).

## Hard prohibitions

- No Fabric OS — no daemon, no second scheduler, no second task DB, no second reducer, no second HGK,
  no knowledge platform substitution.
- No authority elevation of this file — AGENTS.md / docs never create gates, policies, or authority.
- No invented gates — only the vocabulary in `rp002\RP002_GATE_CATALOG.yaml` executes; historical
  names (`KBN1`, `FG1`) do not execute.
- No PASS from file presence — a policy/contract file existing is not consumption; a receipt existing
  is not a fresh PASS.
- No secrets — never read/write credentials into Fabric evidence/docs; secret policy is env-var
  `REFERENCE_ONLY` (ContextForge: `__REPLACE_ME__` rejected fail-closed).
- No Stage-3 execution from this docs task — SQP1 and Stage-3 are NOT authorized and NOT executed by
  this task.

## Evidence quick map

- Stage root: `stage\RP002-STAGE-HGK\` — seal (`STAGE-2-SEAL-REPAIRED.yaml`), handoff
  (`STAGE2_TO_STAGE3_HANDOFF_REPAIRED.yaml`), external acceptance
  (`EXTERNAL_ACCEPTANCE_RECEIPT_STAGE2.yaml`), finding closure (`S2R_FINDING_CLOSURE.yaml`),
  superseded artifacts (`SUPERSEDED_ARTIFACTS.yaml`), resume checkpoint
  (`RESUME_CHECKPOINT_STAGE3_ENTRY.yaml`).
- Gate receipts: `stage\RP002-STAGE-HGK\<K1|D1|C1|H1|O1|B1|F0|CF1|F1|KG1>\*_RECEIPT*.yaml|json`.
- Review evidence: `evidence\review\RP002_STAGE-2_KG1_EVIDENCE_FOR_EXTERNAL_REVIEW.md` and
  `evidence\review\RP002_STAGE-2_EXTERNAL_BUNDLE_HASHES.json` (mirror byte-identical, `104d4cf2`).
- Policy consumption trace: `stage\RP002-STAGE-HGK\F0\F0_POLICY_CONSUMER_TRACE.json`.
- Interop lineage: `stage\RP002-STAGE-HGK\CF1\*` (ContextForge 1.0.7 @ `4092d336`, registration
  `CF-REG-RP2-S2-001`, OASF `oasf-record/1`) and `stage\RP002-STAGE-HGK\F1\` (transaction
  `TX-RP2-S2-F1-002-REPAIRED`).
- Knowledge governance: `stage\RP002-STAGE-HGK\KG1\KG1_NAMESPACE_MODEL.json`,
  `KG1_PROVIDER_LEDGER.json`, `KG1_RUNTIME_EVIDENCE.json`, `KG1_RUNTIME.db`.
- Independent checker upgrade (round `HGK-CHU-20261009`, candidate): mirror
  `evidence\review\checker-upgrade-20261009\HGK-CHU-20261009_CHECKER_UPGRADE_EVIDENCE.md`
  (byte-identical to the HG-KSEOS source) and the round summary
  `HG-KSEOS\evidence\checker-upgrade-20261009\IMPLEMENTATION_SUMMARY.md`. What it binds: a checker
  lane's verdict is **advisory only** — never an OracleReceipt, never a canonical acceptance status, and
  no Fabric contract may consume it as one. Honest status: cutover gate `TEMP_CLOSED/UNVERIFIED`;
  `hgk_canonical_acceptance: NOT_PERFORMED`.

When in doubt: read the file, then read the receipt that binds it, then the seal that binds the
receipt. Do not claim anything the chain does not show.
