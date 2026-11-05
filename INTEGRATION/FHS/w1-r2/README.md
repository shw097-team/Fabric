# FHS W1 r2 — navigation pointer (Fabric side)

**NAVIGATION_ONLY · NOT OWNER RATIFIED · NOT AN ISSUER · NOT A COMPILER · NOT A CHECKER.**

**ChangeSet:** `FHS-W1-R2-PREIMPL-20261105`
**Source:** W1 r2 author final, body `e40df2999fbffdb96a32a2e35cddce228abdd82080d5a5bedd415dfc938669ce`, source manifest `06628b6b4c6ba1b0d4d9b31b795141aaf51ade4c7df8304d1af093a229227f60`, ZIP `ce1e27ea948212b4312bf4243d9a6760d39b913e94bb5cc27fd871f378182e8e`

Claim ceiling of this change: **candidate evidence only**. It is not an acceptance, not a release, and it
carries no canonical or native standing.

This directory adds a **pointer**, not a route and not a permission. `INTEGRATION/MANIFEST.json` is
untouched, the four Mirror Subjects stay four, and `effect_permission` remains `NONE`.

| neighbouring repository | pointer |
|---|---|
| SBL (canonical PIPD, product/TPM) | `evidence/fhs-w1-r2-20261105/` |
| HG-KSEOS (native issuer/control) | `evidence/fhs-w1-r2-20261105/` |

`repository-delta.json` records the delta: route change `NONE`, manifest change `NONE`, no Mirror Subject
added, and the open holds (WP19 CI ACK, E26 -> WP14, typed receiver ACK, HGK permit, protected checker,
publisher).

## Why this is safe to merge

- it adds no `task_class`, no route target, and no state to `repository-map.json`;
- it publishes no raw world data, no credential and no local path;
- `fhs-nav-static` (validate_entry + unit tests) is untouched by an additive subdirectory.
