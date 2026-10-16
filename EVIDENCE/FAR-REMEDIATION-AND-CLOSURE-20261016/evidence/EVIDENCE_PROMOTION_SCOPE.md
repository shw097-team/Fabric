# Evidence promotion scope

**Result: four-file promotion overlay identified; whole-tree exactness is blocked by access-denied directories.**

Frozen candidate: `C:\Projects\Agent_Workspace\HG-KSEOS\var\LANE-RELIABILITY-CLOSURE-20261016\candidate`. Canonical: `C:\Projects\Agent_Workspace\HG-KSEOS`.

## Measured scope

- All **200 candidate files** match the frozen manifest individually by SHA-256.
- Candidate comparison: **5 modified**, **1 candidate-only**, **194 identical**.
- Full-root walk enumerated **243,465 canonical files** and **243,266 canonical-only files** after exclusions.
- Classified **243,272 known file differences**: **4 PROMOTE**, **242,920 DO_NOT_PROMOTE**, **348 NEEDS_OWNER_DECISION**. Every file is individually listed in the JSON.

## PROMOTE (proposed overlay, not authorization)

| Relative path | Canonical exists | Current candidate SHA-256 |
|---|---|---|
| `scripts/hgk-governed-runtime-controller.py` | yes | `5b744de7c4e30240ae92421c2e7220efa5dfca02d88d85f2264bc921ad849412` |
| `scripts/runtime_role_binding_assert.py` | yes | `6fa7ed6b6ea983e154a6a2a0b70a250baa6bbc65742a2a82425ce9a2f5fcacd2` |
| `tests/test_governed_runtime_controller.py` | yes | `fdf1dbc251eee5e78d9c5db91f2a0ebf18c30c2daa43a66f62b3cde5bf26d521` |
| `tests/test_lane_effort_enforcement.py` | no (new file) | `18742bf07b4055ae44733829d9817787a12d3c9140536689c574223e5356e333` |

## Do not blindly mirror the snapshot

- Two additional modified files were independently detected: `config/model-lane-assignment.json` and `config/lane-routing-registry.yaml`. Both candidate versions are revision/epoch **19**, while canonical is **20**. Copying them would remove newer plane-binding/history data and restore a stale binary-pin expectation. Classified NEEDS_OWNER_DECISION; **retain canonical unless an owner explicitly authorizes rollback**.
- Another **346 canonical-only product/control/spec/support files** require owner authorization **only if deletion is proposed**. Snapshot absence does not establish intentional deletion. Retaining them requires no new decision.
- **242,920 canonical-only environment/runtime/worktree/evidence/generated/scratch files** are DO_NOT_PROMOTE; retain them. No deletion or copying occurred.

## Dependency/self-consistency check

**Yes for the four-file overlay, with existing canonical files retained.** No promoted test requires an unpromoted, missing module. This is static dependency consistency, **not acceptance or proof all canonical policy gates are green**.

Checked candidate import/reference lines:

- `tests/test_governed_runtime_controller.py:23`: `CONTROLLER = ROOT / "scripts" / "hgk-governed-runtime-controller.py"` — controller is in PROMOTE.
- `tests/test_governed_runtime_controller.py:29–31`: `sys.path.insert(0, str(ROOT / "src"))`; `from hg_kseos import role_binding`; `from hg_kseos.spine import SharedSpine` — both modules already exist canonically and hash-identically match candidate.
- `tests/test_lane_effort_enforcement.py:27–28`: `ASSERT = ROOT / "scripts" / "runtime_role_binding_assert.py"`; `TOOLCHAIN = ROOT / "config" / "hermes-codex-lane.json"` — assertion script is in PROMOTE; toolchain config is already identical.
- `scripts/runtime_role_binding_assert.py:39,175`: imports `hg_kseos.role_binding` and invokes `scripts/hgk-lane-toolchain.py`; both canonical dependencies are already identical.
- `scripts/hgk-governed-runtime-controller.py:94,242`: imports `SharedSpine` and `hg_kseos.role_binding`; existing canonical source and schema match candidate.

All four promotion files compile in memory. The tests' sibling `TEST_RESULTS` directory and pinned interpreter exist. Tests were **not executed** because they write scratch/SQLite fixtures outside the two-file write allowlist. JSON contains exact dependency hashes and source lines.

## Limitations and exclusions

- **757 canonical directories remained access-denied after a read-only retry**, all under prior round `var/` trees; their descendant file inventories are unknown. Three reparse-directory boundaries were recorded, not followed. Therefore an EXACT whole-tree difference **cannot honestly be certified**. The JSON explicitly preserves every blocked path and marks enumeration incomplete.
- Excluded `__pycache__`, `*.pyc`, `.pytest_cache`, this source round's `TEST_RESULTS` trees, the nested candidate storage subtree, and these two output files. Included `.git`, `.venv`, `.hgk`, prior round data, and worktrees in the discoverable canonical inventory.
- Canonical-only file hashes are not claimed: path absence, not byte modification, defines those entries. Classification uses explicit namespaces; product/control omissions include content excerpts. Common-file differences use SHA-256.
- The live canonical walk is not an atomic filesystem snapshot. No permission changes, deletion, promotion, product/config edit, or acceptance-state changes were made. Only these two evidence files were written.
