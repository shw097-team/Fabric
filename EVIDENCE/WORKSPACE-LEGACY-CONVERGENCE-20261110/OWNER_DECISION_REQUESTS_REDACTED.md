# Owner decision requests (redacted)

Each block is a decision the machine cannot make. No database, registry, receipt or key material is
included; locators are quoted as relative paths only.

## 1. Shared Spine locators (12 items)

| decision | count |
|---|---|
| `RETAIN_HISTORICAL` | 10 |
| `RESTORE_REQUIRED` | 1 |
| `MISSING_HOLD` | 1 |

- `RETAIN_HISTORICAL` — the round is closed and the value is a historical citation; the archive copy is
  sufficient, nothing to restore.
- `RESTORE_REQUIRED` — a still-referenced locator whose file is not in the workspace; restoring or
  re-pointing changes canonical state, so it needs the native owner.
- `MISSING_HOLD` — no copy exists in workspace, first-round archive or the external archive. A same-named
  directory was **not** fabricated.

## 2. PIPD delta (305 rows)

| decision | rows | meaning |
|---|---|---|
| `HISTORICAL_ONLY` | 264 | see disposition table |
| `ALREADY_ABSORBED` | 21 | see disposition table |
| `PORT_TO_SBL` | 10 | see disposition table |
| `ABI_CONFLICT` | 7 | see disposition table |
| `UNIQUE_UNRESOLVED` | 3 | see disposition table |

- `PORT_TO_SBL` rows are the R21 `compile-cc` / `abi.py` / `oracle_compat.py` line. They are **not**
  absorbed by SBL, and they touch the ABI, so they need an SBL-PIPD owner decision before any port.
- `UNIQUE_UNRESOLVED` includes `rescue/r5p-uncommitted-20261016` (no upstream) and the in-repo
  `pipd-ls-sp/` duplicate tree (2,678 files) — potential second writer; untouched.
- The clone itself is **not** retired: 25,985 untracked files and 5 local-only commits remain.

## 3. HGK hot/cold coupling

- `far-lane-sod-003/codex|lanes|receipts` is enumerated by the live `evidence/EVIDENCE_MANIFEST.json`
  completeness set, so splitting it breaks a governed manifest → held.
- `scratch/_acl_refused_53_children`: 53 children return `WinError 5`; contents **unmeasured, not empty**.
- `var/backups/GEN_B_20260808` is cited by `evidence/wave-16/RESTORE_DRILL_REPORT.json`.
