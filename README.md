# Fabric — Integrated Governance Mirror

> **Fabric + FAR + the desktop-effect plane + HG-KSEOS** — integrated under one governance
> contract, mirrored for external acceptance.

## 1. Governance contract of this integration

This repository mirrors the subjects **as one governed system**, under the following binding:

```
在 current Fabric 治理契約下，
以 HG-KSEOS 作為唯一控制平面 (sole control plane)，
並將 current canonical Hermes 綁定為其受治理的 Runtime／Orchestration Plane
(governed runtime / orchestration plane).
```

| Layer | Role | What it may NOT do |
|---|---|---|
| **Fabric** | Governance contract / policy owner of the system | not a runtime; does not execute work |
| **HG-KSEOS** (SharedSpine) | **Sole control plane**: WorkOrder / ExecutionBinding are the single source of truth; admission; router; reducer | must not bypass its own domain API from consumers |
| **Hermes** (canonical) | **Governed Runtime / Orchestration Plane**: admission execution, Kanban, swarm, heartbeat, R0-R8 execution | must not self-set itself as task truth or release authority |
| **FAR** | Autonomous-research **method layer** (governed research product) | not final acceptance; does not land meta-apply |
| **Desktop-effect plane** | Governed desktop adapter with a zero-mouse hard route | never auto-invoked without a registered authorization route |

## 2. Directory map

| Path | Subject | Notes |
|---|---|---|
| `FABRIC/` | Fabric governance | contract, policy, tooling |
| `HG-KSEOS/` | HG-KSEOS control plane | curated: `src/ tests/ docs/ schemas/ scripts/ config/ requirements/ tools/` |
| `FAR/` | FAR research deliverables | research request/plan, integrated findings, root-cause, challenge, proposed evolution |
| `DESKTOP/` | Desktop-effect plane | *pending authorization-token refresh — see Sec.5* |
| `INTEGRATION/` | This integration | manifest, binding statement, acceptance entry point |

**Deliberately excluded** (not part of the acceptance surface): `var/` (working data, SQLite DBs),
`worktrees/`, `evidence/` raw stores, `.venv/`, and any `API KEY/` directory. These are runtime
state or secrets, not governance artifacts.

## 3. What an external acceptance officer can verify here

1. **The binding is real, not prose** - HG-KSEOS is a single control plane: check
   `HG-KSEOS/src/hg_kseos/spine.py` for the canonical transition API and the `TRANSITIONS`
   table; consumers call it rather than issuing SQL.
2. **The ordering-oracle defect class is closed** -
   `HG-KSEOS/src/hg_kseos/{lifecycle,knowledge,evidence_graph}.py` order by the implicit `rowid`
   (monotonic insertion order), never by wall-clock `created_at`.
   Guard: `HG-KSEOS/tests/test_ordering_oracle.py`.
3. **The acceptance-integrity controls** -
   `FAR/far-swof-kseos-rca-001/impl/acceptance_integrity_checks.py` + its 22-test suite, plus the
   inventory record that grounded them.
4. **The FAR research chain** - request -> plan -> integrated findings -> root cause -> challenge
   -> proposed evolution -> Gate-1 receipt, all in `FAR/`.

## 4. Claim ceiling of this mirror

`MIRROR_OF_GOVERNED_ARTIFACTS_FOR_EXTERNAL_ACCEPTANCE_ONLY`

- This repository does **not** claim external acceptance, merge, release, production, or any
  live-world effect.
- Neither SWOF W2 (external `PASS_CHALLENGE`) nor W3 dispatch is claimed here.
- Credentials, tokens and connection strings are **never** mirrored.

## 5. Desktop-effect plane slice

The desktop-effect plane artifact tree is mirrored at `DESKTOP/` (adapter, routing/preflight
guards, capability matrix, asset registry, verified action-class receipts, documentation).

Curation: third-party vendored material (a downloaded distribution archive and its extraction,
~133 MB) is **excluded** - it is not a governance artifact. The scripts that operate on it are
kept.

## 6. Provenance

Mirrored from the local governed workspace `C:\Projects\Agent_Workspace` at the state where:
- HG-KSEOS commits `c0cb5cb` (canonical acceptance resolver) and `c12412e` (ordering oracle) are HEAD.
- FAR Gate 1 = `CONFIRMS_USEFUL`; Gate 2 = authorized; controls C1-C8 implemented with an
  independent-checker PASS.
