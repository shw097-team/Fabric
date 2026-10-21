# Fabric (governance contract) — upgrade index

Folder-local navigation for an external engineer planning an upgrade. Read
[`../INTEGRATION/UPGRADE-PLANNING-GUIDE.md`](../INTEGRATION/UPGRADE-PLANNING-GUIDE.md) first; this file only
tells you what is here and which document to trust first.

## What this folder holds
- the governance contract and policy ownership statements
- the research and desktop-automation trees, their methods and skills
- governance entry: `AGENTS.md`

## Trust order inside this folder
1. `AGENTS.md` (contract)
2. the contracts/ and policy documents it names
3. the subject trees it governs

## Planning notes
- Fabric owns the contract; it does not execute and does not accept.
- Cross-subject edges are mapped in `../INTEGRATION/DEPENDENCY-AND-CONTRACT-MATRIX.md`.

## Global rules that override anything here
- `HG-KSEOS` is the sole control plane; this repository is a projection, not an authority.
- See [`../INTEGRATION/NON-CLAIMS.md`](../INTEGRATION/NON-CLAIMS.md) and
  [`../INTEGRATION/KNOWN-FINDINGS.md`](../INTEGRATION/KNOWN-FINDINGS.md) before relying on anything.
## Round note — `SKILL-CONVERGENCE-20261014`

- **What changed for planners**: a candidate-only convergence round on the canonical Hermes skill entry points
  (lossless extraction, a 14-file topic-merge pilot, reuse of the existing consumers, rollback point and
  convergence invariants). The Fabric-side effect is hygiene plus the front page; **no contract changed**.
- **Read first**: [`../EVIDENCE/SKILL-CONVERGENCE-20261014/README.md`](../EVIDENCE/SKILL-CONVERGENCE-20261014/README.md),
  then its `ROUND-CLOSURE.md`.
- **Ceiling**: the two checks that ran (`VERIFY 6`, `SECURITY 5`) are advisory; this change-set accepts,
  merges, releases and promotes nothing.
- Generated 2026-10-13T12:23:20.088907+00:00; round note added 2026-10-14.
## Round note — `FAR-MINIMAX-MANDATE-20261021`

- **What changed for planners**: the three governed lanes (PLAN, EXECUTE, VERIFY/SECURITY) are now
  bound to **one** model — `opencode-go/minimax-m3.1-flash-free` (MiniMax M3.1 Flash, OPENCODE GO) —
  by owner order 2026-10-21. The control-plane registry advances to **epoch 25**.
- **What this means for the contract**: **model-axis separation between writer and checker is now
  absent** (declared as `SOD006-C5`, `OPEN_OWNER_ORDERED`). The remaining separation is process,
  lane and evidence-path separation plus the no-self-acceptance rule. Correlated blind spots inside
  the shared model family are **not** claimed to be absent. Every previously declared lane arm is
  retained as a reachable fallback, so a later owner order can restore separation without re-deriving
  the pool.
- **Also in this round**: the residual inventory was **measured, not assumed**. The referenced 471
  unchecked OpenSpec items are **460 across 34 changes**; the referenced 114 `var/` directories are
  **120**, and they are not 120 unfinished rounds (83 round artifacts, 3 runtime/cache, 2 empty, 32
  needing a ruling). The TT ledger has exactly **2** rows with `status == "OPEN"`.
- **Read first**: [`../EVIDENCE/FAR-MINIMAX-MANDATE-20261021/README.md`](../EVIDENCE/FAR-MINIMAX-MANDATE-20261021/README.md),
  then its `FAR-RULING-REPORT.md`.
- **Open for the owner**: five FAR rulings are **proposed, not executed** (OpenSpec tick-backfill,
  `var/` disposition, the two TT ledger rows, model-axis independence, delegation plane). They are
  `blocked` on the KANBAN board `far-minimax-mandate-20261021`, not silently applied.
- **Ceiling**: candidate-only. The evidence shows a local measurement and an independent re-derivation
  of the binding; it is not an acceptance, not a release, not a merge and not a promotion.
- **Branch note**: this round publishes on `pub/far-minimax-mandate-20261021`. The earlier branch
  `pub/far-lane-remediation-20261021` was contaminated by another session's commits and is **not**
  the branch to verify against — see `../EVIDENCE/FAR-MINIMAX-MANDATE-20261021/PUBLISH-BRANCH-INCIDENT.md`.
