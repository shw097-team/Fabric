# Fabric — Integrated Governance Mirror

> **Fabric + FAR + the desktop-effect plane + HG-KSEOS** — integrated under one governance contract,
> mirrored so that an **external engineer can plan a complete upgrade** of the subjects from this
> repository alone.

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
| `INTEGRATION/` | the readiness set described in section 2, plus the mirror manifest |
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

Published 2026-10-13T11:50:38.128148+00:00. The previous publication is preserved in history; this one records its own scope,
its hygiene result and its open owner decisions.
