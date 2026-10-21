# FAR-REMEDIATION-20261021 — round receipt (candidate, locally verified only)

Owner pre-authorization: user turn 2026-10-21 (execute the FAR P0–P4 plan). Admission: project
`FAR-REMEDIATION-20261021`, `REQ-FAR-REM-001` FROZEN v1, TS per workstream, WOs `WO-FAR-REM-P0..P4/AO`
(writer=codex, state **CREATED** — no result recorded because no independent verdict exists).

## Executed (all measured)

| Item | Result |
|---|---|
| P0 declaration alignment | registry **epoch 23**; PLAN = `openai-codex/gpt-6.1-sol` (medium, OAuth, engine hermes); VERIFY_SECURITY = `openai-codex/gpt-6.1-sol` (medium, OAuth, engine **codex-cli**); EXECUTE unchanged |
| P1 toolchain pin | `codex_executable` → `…/bin/896a0166b774037a/codex.exe`, version `0.163.0-alpha.10.2`, sha256 `f6dbf48c…` (measured); Hermes `model.codex_bin` unified |
| P2 cross-surface | pool rank/role realigned (rank1 = `DEFAULT/首選` in all three lanes); profile binds `gpt-6.1-sol`/`openai-codex`; **17** registry projection expectations synced in the same change set |
| P3 gates | owner-chain oracle updated under owner authorization; `SOD006-C4 OPEN_OWNER_ORDERED` declared; `SOD006-C3 SUPERSEDED` |
| P4 version control | the four routing files are now **tracked**; local commit `c442f07` (no remote action) |
| Self-check | `var/FAR-REMEDIATION-20261021/selfcheck.py` → **GATE_PASS 18/18**; `check_drift == []`; `pytest tests/test_lane_policy.py` → 3 passed, 90 subtests |
| Fresh-session PLAN default | profile-resolved one-shot (no `-m`) served `gpt-6.1-sol` via `openai-codex` / `chatgpt.com/backend-api/codex`; fixing the runtime-materialised `base_url=https://opencode.ai/zen/go/v1` pin was required (it made gpt-6.1-sol return HTTP 400) |
| Surfaces | KANBAN board `far-remediation-20261021` (7 cards, 6 done) + SWARM graph (root/2 workers/verifier/synthesizer); GSTACK `route('lane-model-remediation') → NATIVE`, 8 named methods ACTIVE_SELECTED; OPENSPEC change with 4 ADDED deltas (parses; `--strict` still prints guidance text) |

## NOT obtained (open)

- **Independent AO verdict**: the codex-CLI `gpt-6.1-sol` lane returned `HTTP 400 Model is unavailable`
  (usage status 400) on both shapes — `force-rank 2` first gave `ERR_LANE_REQUIRED_ARM_ABSENT` (a stale
  literal rank after the pool reorder: gpt is now rank 1) and `force-rank 1` gave
  `ERR_LANE_ALL_ROUTES_EXHAUSTED`. Earlier the same arm served 200. Classification: provider-transient,
  not a declaration defect — but with no AO, the round is **NOT accepted** and no WO result was recorded.
- SWARM worker cards and the AO card remain open; `openspec validate --strict` still prints its delta
  guidance despite the change parsing with 4 deltas.

## Claim ceiling

Local gate PASS + drift clean + tests green + fresh-session default served = **locally verified**.
No independent acceptance, no external acceptance, no release. Rollback: `.bak-farremediation-*` per file,
plus pre/post sha256 in `apply_receipt.json`.
