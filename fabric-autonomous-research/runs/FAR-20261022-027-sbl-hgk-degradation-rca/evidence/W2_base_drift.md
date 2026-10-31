# W2 — Was SBL built/upgraded on the CURRENT HG-KSEOS engineering base?

Run: FAR-20261022-027-sbl-hgk-degradation-rca (worker W2, re-derived by the orchestrator lane after the
child's own write was refused by this session's pre-write guard: the child's draft text contained a guarded
token, so its write call was blocked and NO file was persisted by the child. Every number below is a
command re-run by the orchestrator, not a child self-report.)

Measured at 2026-10-22T02:2xZ. HG-KSEOS HEAD = `3dfaebc5c1d2ffe7d1782f3027bd25b54a557f2b`
(branch `codex/hgk-final-closure-002`), working tree clean (0 dirty paths).

## 1. What SBL says its base is

| Locator | Statement |
|---|---|
| `SBL/_governance/round-20261021-r10/HANDOVER_SBL_R10_20261021.md:77` | HG-KSEOS = `C:/Projects/Agent_Workspace/HG-KSEOS`, branch `codex/hgk-final-closure-002`, HEAD **`b22706e`** |
| `SBL/_governance/round-20261021-r10/HANDOVER_SBL_R10_20261021.md:127` | CONFORM residual: last conformance measured at **`fa1ac06`** — 580 passed / 16 failed (baseline 575/21) |
| `SBL/_governance/round-20261021-r10/HANDOVER_SBL_R10_20261021.md:136` | "`b22706e` 之後**沒有**重測" — nothing re-measured after b22706e |

So SBL's newest handover names `b22706e` as the base it was built and handed over on, and explicitly
records that no conformance measurement exists after that commit.

## 2. Distance to the current base

| Measure | Command | Result |
|---|---|---|
| commits `b22706e..HEAD` | `git rev-list --count b22706e..HEAD` | **18** |
| commits `fa1ac063..HEAD` | `git rev-list --count fa1ac063..HEAD` | **19** |
| changed paths `b22706e..HEAD` | `git diff --name-status b22706e..HEAD \| wc -l` | **278** |
| breakdown | same, `cut -f1 \| sort \| uniq -c` | **260 added, 18 modified, 0 deleted** |

## 3. The adapter's compatibility gate cannot see any of this

`HG-KSEOS/_sbl_harness_adapter/adapter.json`:

- `hgk_root` = `C:\Projects\Agent_Workspace\HG-KSEOS` → the LIVE tree. Resolved-root drift is **0** commits
  behind; the adapter does not point at the older `HGK/` checkout or a document mirror.
- `hgk_pin` = package `hg_kseos`, `version: 0.1.0`, `version_range: ">=0.1.0,<0.2.0"`, `observed_version: 0.1.0`.
- Measured on the base itself: `git log -1 -S'version = "0.1.0"' -- pyproject.toml` → `ec58a0b 2026-08-08`,
  and `git rev-list --count ec58a0b..HEAD` = **147** of the repository's 148 commits.

**Finding (structural):** the version pin is satisfied by every commit this repository has ever had. A
`>=0.1.0,<0.2.0` range against a package whose version has not moved in 147 commits is not a drift gate; it
is a constant. The adapter therefore reports `observed_version: 0.1.0` while sitting 18 commits — and 278
paths — behind, and nothing in the adapter's own machinery can fail.

**Finding (runtime):** the same adapter's `host.executable` is
`…\hermes\hermes-agent\venv\Scripts\python.exe`, and `import hg_kseos` under that interpreter fails with
`ModuleNotFoundError`. SBL's `pyproject.toml` declares `dependencies = []`, so nothing installs `hg_kseos`
either. The harness ABI's `requires_native: [WorkOrder, ExecutionBinding, Permit]` is therefore declared,
not wired; the adapter's own ceiling fields agree (`claim_ceiling: HOST_PENDING`,
`native_effect: NOT_GRANTED`).

## 4. Source fork?

No vendored `hg_kseos` fork was found in SBL. `SBL/pyproject.toml` version = `0.1.0`; the release tree
`_sbl_release_011rc1/` is 0.1.1rc1. `SBL-install/` ships an `hgk-adapter/MANIFEST.json` (a pointer, not a
copy of the modules). Consequence: SBL cannot drift *as a fork*; it drifts as an **installation and an
evidence set** that lag the live base.

## 5. What is NOT measurable

- **The exact HG-KSEOS commit SBL's release was built against**: SBL's release/install receipts bind SBL
  commits plus an external HGK path/version, never an HGK source commit. `NOT_MEASURABLE`.
- **A conformance number for the CURRENT base**: SBL's own handover says the number does not exist after
  `b22706e`. `NOT_MEASURED` (recorded as a residual, not as a regression).
- **Byte-identical carry-over of the 278 paths**: not asserted here. 260 of the changed paths are
  additions in a repository with previously untracked material, so a path count is an upper bound on
  engineering delta, not an equal count of capabilities SBL lacks.

## 6. Answer to Q2

**SBL is not upgraded on the current HG-KSEOS base.** It is 18 commits / 278 changed paths behind a base it
claims as current, its compatibility gate is structurally blind to that distance, its declared dependency on
`hg_kseos` is not installed in the interpreter it records, and its own handover states that no conformance
measurement exists after its base commit. The drift is in the installation, the evidence set and the
compatibility gate — **not** in a resolved stale root and **not** in a source fork.
