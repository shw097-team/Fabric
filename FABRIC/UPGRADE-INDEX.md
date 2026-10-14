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
