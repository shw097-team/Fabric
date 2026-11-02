# Fabric — Integrated Governance Mirror & FHS Engineering Entry Host

> **Fabric + FAR + the desktop-effect plane + HG-KSEOS** — integrated under one governance contract,
> mirrored so that an **external engineer can plan a complete upgrade** of the subjects from this
> repository alone.

## FHS Engineering Entry — Start Here

This repository also **hosts** the FHS Engineering Entry: one non-authoritative navigation index for
cross-repository engineering work across the four FHS repositories. Hosting is not authority.

| repository | what it owns | entry |
|---|---|---|
| **Fabric** (this repository) | governance contract / policy mirror | [`INTEGRATION/README.md`](INTEGRATION/README.md) |
| **HG-KSEOS** | sole native control plane: typed lifecycle, admission, evidence ledger | [HG-KSEOS](https://github.com/shw097-team/HG-KSEOS) |
| **SBL** | product surface (TPM skill pack) | [SBL](https://github.com/shw097-team/SBL) |
| **PIPD-LS-SP** | compiler / CLI / U04 until a separately ratified cutover | [PIPD-LS-SP](https://github.com/shw097-team/PIPD-LS-SP) |

- **Read first:** [`INTEGRATION/FHS/README.md`](INTEGRATION/FHS/README.md) — six task classes, the
  original reader for each, and the next action.
- **Route map:** [`INTEGRATION/FHS/repository-map.json`](INTEGRATION/FHS/repository-map.json) —
  machine-readable routes, `source_state=PROPOSED_NOT_OWNER_RATIFIED`.
- **Deployment record and owner decisions:**
  [`INTEGRATION/FHS/DEPLOYMENT-AND-OWNER-DECISIONS.md`](INTEGRATION/FHS/DEPLOYMENT-AND-OWNER-DECISIONS.md).
- **Next step for a cross-repository task:** name the task class, read the original reader it points
  to, then open a separately scoped change in the affected repository. A shared ChangeSet ID is not
  an HGK WorkID.

**Host ≠ Authority.** The entry is `NAVIGATION_ONLY / effect_permission=NONE`. It signs no permit,
work order or grant; it is not a queue, a policy writer, a compiler or a protected checker.
HG-KSEOS remains the only native control plane, and every route's authority stays with its original
domain.

## 1. Governance contract of this integration

```
在 current Fabric 治理契約下，
以 HG-KSEOS 作為唯一控制平面 (sole control plane)，
並將 current canonical Hermes 綁定為其受治理的 Runtime／Orchestration Plane
(governed runtime / orchestration plane).
```

| Layer | Role | What it may NOT do |
|---|---|---|
| **Fabric** | governance contract / policy owner of the system | not a runtime; does not execute work |
| **HG-KSEOS** | **sole control plane**: typed lifecycle, admission, evidence ledger | may not self-accept; may not accept on a subject's behalf |
| **canonical Hermes** | governed Runtime / Orchestration Plane under HG-KSEOS | is not a controlling authority; routing changes are owner-gated |
| **FAR** | research product: contracts, routing, retrieval | does not own governance |
| **desktop-effect plane** | documented desktop procedures, guards, skills | no live-world effect is claimed here |

## 2. Start here — planning an upgrade from outside

| If you want to … | read |
|---|---|
| know what may be planned against | [`INTEGRATION/UPGRADE-SCOPE.md`](INTEGRATION/UPGRADE-SCOPE.md) |
| follow the ordered procedure | [`INTEGRATION/UPGRADE-PLANNING-GUIDE.md`](INTEGRATION/UPGRADE-PLANNING-GUIDE.md) |
| map this mirror onto the four subjects | [`INTEGRATION/SOURCE-PROJECTION.md`](INTEGRATION/SOURCE-PROJECTION.md) |
| see cross-subject dependencies and who may change what | [`INTEGRATION/DEPENDENCY-AND-CONTRACT-MATRIX.md`](INTEGRATION/DEPENDENCY-AND-CONTRACT-MATRIX.md) |
| know the tests and the rollback for a change | [`INTEGRATION/VALIDATION-AND-ROLLBACK.md`](INTEGRATION/VALIDATION-AND-ROLLBACK.md) |
| know what is **not** claimed | [`INTEGRATION/NON-CLAIMS.md`](INTEGRATION/NON-CLAIMS.md) |
| see what this publication contains and excludes | [`INTEGRATION/MANIFEST.json`](INTEGRATION/MANIFEST.json) |
| read the hygiene record and the independent verdict | [`EVIDENCE/repo-hygiene-20261013/`](EVIDENCE/repo-hygiene-20261013) |
| read the current round's closure record and its independent check | [`EVIDENCE/SKILL-CONVERGENCE-20261014/`](EVIDENCE/SKILL-CONVERGENCE-20261014) |

**Capability test.** An external engineer must be able to produce the upgrade scope, the dependency
and contract map, the validation plan, the rollback plan and the non-claim list — from this
repository alone, without any private workspace path. The `INTEGRATION/` set exists to make that
test passable.

## 3. Repository layout

| folder | contents |
|---|---|
| `HG-KSEOS/` | control plane: contracts, typed lifecycle, evidence, requirements |
| `FABRIC/` | governance contract, research and automation trees, methods and skills |
| `FAR/` | research-product contracts, routing and retrieval |
| `DESKTOP/` | desktop-effect plane: documentation, guards and skills (runtime state is a named, bounded exception — see the manifest) |
| `INTEGRATION/` | the readiness set described in section 2, plus the mirror manifest and the FHS navigation entry |
| `EVIDENCE/` | assessment, hygiene and independent-check records |

## 4. Ground rules for contributors and planners

1. **Do not read this repository as an authority.** It is a projection; `HG-KSEOS` is the control plane.
2. **A gate that is not named is not passed.** Presence, digests, file counts and model votes are not passes.
3. **Owner-class decisions stay with the owner**: licence choice, bulk-binary disposition, remote
   linkage, subject baseline re-certification and acceptance are recorded as open, never resolved here.
4. **Never publish credentials or machine-local state.** The root `.gitignore` encodes the publish control.
5. **Changes arrive as a reviewed change-set**, on a branch, with an approval list, then merge.

## 5. Status of the subjects

`NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`

Published 2026-10-13T11:50:38.128148+00:00 (the readiness set). A second publication is recorded: **2026-10-14, change-set
`docs/skill-convergence-20261014`** — it carries the candidate-only convergence round's closure record and its independent
check under [`EVIDENCE/SKILL-CONVERGENCE-20261014/`](EVIDENCE/SKILL-CONVERGENCE-20261014), brings the `FABRIC/` front page up
to the local revision, adds the round's rows to [`INTEGRATION/KNOWN-FINDINGS.md`](INTEGRATION/KNOWN-FINDINGS.md), and changes
no contract. Each publication is preserved in history and records its own scope, its hygiene result and its open owner
decisions.

The FHS navigation entry under `INTEGRATION/FHS/` is a third, separate addition: it is
`GITHUB_NAV_DEPLOYED` and changes no contract, no manifest subject and no owner decision. See
[`INTEGRATION/FHS/DEPLOYMENT-AND-OWNER-DECISIONS.md`](INTEGRATION/FHS/DEPLOYMENT-AND-OWNER-DECISIONS.md).


## B1 closure 2026-10-28

`b1_closure_20261028/` is the evidence index for the FHS-MSC B1 bootstrap-repair round (PKG_00~08) on the Fabric side.

- `b1_closure_20261028/EVIDENCE_INDEX.md` — question → file#line → the command that reproduces it
- `b1_closure_20261028/MANIFEST.json` — per-file bytes + sha256 (the packet is verifiable offline)
- `b1_closure_20261028/HANDOVER.md` — ten-point orientation for an external reviewer

Claim ceiling (measured, not asserted): `mission_complete true` under `b1_closure_20261028/evidence/GATES.json`
means the gate conjunction passed, no residual blocker remained, and every blocking declaration was
owner-ruled. It does **not** mean release (`release: NOT_RUN`), promotion, or third-party acceptance.
Databases, raw lane output, the owner key envelope and credentials are excluded by design.
