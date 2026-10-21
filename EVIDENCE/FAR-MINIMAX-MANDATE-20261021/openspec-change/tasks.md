# Tasks — FAR MiniMax mandate (epoch 24 → 25)

Owner order (2026-10-21, this turn): PLAN, EXECUTE (Codex CLI) and VERIFY/SECURITY (Codex CLI)
all run on `opencode-go/minimax-m3.1-flash-free` (MiniMax M3.1 Flash, OPENCODE GO).

Ceiling: every item below is a CANDIDATE-ONLY local change. Local green is not an acceptance,
not a release, and not a merge.

## 0. Pre-flight — the model mandate must be usable before anything else

- [x] 0.1 Measure MiniMax on the relay and through the Codex CLI transport for all three lanes
  (receipts `var/FAR-MINIMAX-MANDATE-20261021/probes/{PLAN,EXECUTE,VERIFY}_admit.json`;
  every one reports `ok=true`, `required_arm == served_arm == opencode-go/minimax-m3.1-flash-free`,
  exit 0, and the model actually driving a shell tool)
- [x] 0.2 HGK admission for the three arms — `PLAN=ADMITTED`, `EXECUTE=ADMITTED`,
  `VERIFY_SECURITY=ADMITTED` (receipts `var/FAR-MINIMAX-MANDATE-20261021/admission/`). The
  admission counts a real `command_execution` event, not a self-declared tool count
- [x] 0.3 Record the transport-vocabulary rule that the mandate depends on: `opencode-go` takes
  the provider-qualified id; `openai-codex` takes the bare id; the relay's `/v1/models` catalog
  is a stale snapshot and is NOT the source of truth for either model

## 1. The binding itself (epoch 24 → 25)

- [x] 1.1 `config/lane-route-slots.candidate.json`: MiniMax becomes the rank-1, default,
  automatically-selected arm of PLAN, EXECUTE and VERIFY_SECURITY; every pool's ranks are
  contiguous `1..N`; no prior arm is deleted — each becomes a reachable fallback
  (`var/FAR-MINIMAX-MANDATE-20261021/apply_minimax_binding.py`)
- [x] 1.2 `config/lane-routing-registry.yaml`: epoch 24 → 25; the three routes' provider/model,
  primary arm, canonical identity and selection authority follow the pool
- [x] 1.3 `config/model-lane-assignment.json`: the lane chains, the assignment rows, the VERIFY
  supply selector and the SoD declarations are DERIVED from the pool rather than hand-written,
  so the pool remains the single selection authority
  (`var/FAR-MINIMAX-MANDATE-20261021/apply_assignment_derivation.py`)
- [x] 1.4 The registry's projection bindings are re-derived from the WRITTEN artifact (read back
  from disk), and pointers whose semantic slot moved (the EXECUTE owner-selectable additional
  route, the sorted model-set indices) are re-pointed rather than merely re-valued
- [x] 1.5 Declare `SOD006-C5 OPEN_OWNER_ORDERED` and set the `EXECUTE → VERIFY_SECURITY` pair's
  `distinct_required` to `false` WITH the reason recorded — the model axis is identical across
  all three lanes by owner order; it is declared, not hedged
- [x] 1.6 `check_drift()` returns `[]` — the projection and the artifact agree on every pointer

## 2. The three residual subjects — measured, indexed, NOT closed

The owner's figures were 471 unchecked OpenSpec items, 114 `var/` directories and 2 TT ledger
OPEN rows. Each was re-measured before any ruling could be built on it.

- [x] 2.1 OpenSpec: measured 38 active changes, 34 with unchecked items, **460** unchecked in
  total (the owner's 471 is a stale estimate). Indexed per change and per item, with each
  unchecked item's own evidence (the change's artifact files, whether its name appears in
  `git log`). **Ticks applied by this script: 0**
  (`var/FAR-MINIMAX-MANDATE-20261021/openspec_unchecked_index.json`)
- [x] 2.2 `var/`: measured **120** top-level directories (the owner's 114 is a stale snapshot),
  and established that these are NOT 120 unfinished rounds — 75 are round artifacts with no
  linked change, 8 are round artifacts whose change still has unchecked items, 3 are
  runtime/cache/DB/backup, 2 are empty, 32 need an owner ruling. **Destructive actions taken: 0**
  (`var/FAR-MINIMAX-MANDATE-20261021/var_disposition_index.json`)
- [x] 2.3 TT ledger: verified that exactly **2** rows carry `status == "OPEN"`
  (`HGK-EBC-TT-001`, `HGK-EBC-TT-002`); the third open-ish row carries a different status value
  (`OPEN_NONBLOCKING_FOR_HLPE_BIND`) and is not one of the two
- [x] 2.4 The FAR ruling is written up for the owner's confirmation — the owner's instruction this
  round was "propose the ruling and let the user confirm", so no ruling-dependent mutation was
  performed (`var/FAR-MINIMAX-MANDATE-20261021/FAR-RULING-REPORT.md`)

## 3. Parallel construction — SBL

- [x] 3.1 Identify the two SBL round directories another session is writing under Fabric
  (`fabric-autonomous-research/runs/FAR-20261021-02{3,4}-*`), and record the exclusion rules
  (`var/FAR-MINIMAX-MANDATE-20261021/SBL-EXCLUSION-NOTE.md`)
- [x] 3.2 Execute the exclusion: zero writes to `fabric-autonomous-research/`, zero staging of
  those paths, and both directories deliberately left untracked for the constructing session

## 4. Orchestration surfaces

- [x] 4.1 KANBAN board `far-minimax-mandate-20261021` — 17 cards: 12 done, 5 blocked awaiting
  the owner's ruling (the blocked cards are the ruling-dependent items, not unfinished work)
- [x] 4.2 Two research subagents on the MiniMax arm (`deleg_4d2d40d9` for the OpenSpec
  classification, `deleg_5ff913cf` for the knowledge-base cross-check) plus a third earlier one
  for the `var/` inventory — the delegation plane was temporarily pinned to MiniMax because
  `gpt-6.1-sol` was rate-limited (HTTP 429), and the pin was restored immediately after dispatch
  and confirmed in `state.db`
- [x] 4.3 Independent AO on the MiniMax VERIFY_SECURITY lane re-derives the binding claims from
  the artifacts (receipt `var/FAR-MINIMAX-MANDATE-20261021/probes/AO_minimax_binding.json`)

## 5. Self-detection / self-repair / self-acceptance (added after the first measurement)

The first full-suite run showed the epoch-25 binding had introduced five NEW failures. Two of
them turned out to be a real governance defect, not a test problem.

- [x] 5.0 **Self-detection** — the full suite is compared BEFORE/AFTER in an ISOLATED detached
  worktree; the live working tree is never modified. The first version of that comparison did
  modify the live tree and had to be killed mid-run, leaving a mixed state that was rebuilt from
  the three backups (`var/FAR-MINIMAX-MANDATE-20261021/compare_pytest_isolated.py`)
- [x] 5.1 **The registry's own route rows are re-derived from the pool** (15 fields). `check_drift`
  compares the registry's *projections* against the live sites; it does NOT compare the registry's
  internal route rows against the pool. Before this fix the registry still advertised
  `gpt-6.1-sol` (PLAN, VERIFY_SECURITY) and `deepseek-v4.1-flash` (EXECUTE) while the pool and the
  assignment both said `minimax-m3.1-flash-free` — and `check_drift()` still returned `[]`.
  `admission_status` was `UNPROVEN` for two lanes whose admission had in fact been measured.
  (`var/FAR-MINIMAX-MANDATE-20261021/apply_registry_route_sync.py`; the re-run reports 0 further
  changes, so the sync is idempotent)
- [x] 5.2 **The test oracle is repaired at the root cause** — the stub child's usage row now derives
  its provider/model from the `--model` argument the dispatcher passes it, so the dispatched arm IS
  the reported arm. A stub that hard-codes a model breaks on every future re-binding of the pool
  for a reason that has nothing to do with the behaviour under test. The `owner_chain` oracle in
  `tests/test_lane_policy.py` follows the owner order, which is what that oracle exists to do.
  (`tests/fixtures/stub_lane_child.py`, `tests/test_lane_dispatch_ao_guard.py`)
- [x] 5.3 **`tests/fixtures/` is brought under version control** — 17 tests referenced
  `stub_lane_child.py` while the whole directory was untracked, so a clean checkout could not
  rebuild the test suite. This is the same defect class as the runtime closure fixed earlier this
  round.
- [x] 5.4 **Self-acceptance** — the targeted lane suite is green (`141 passed / 90 subtests`) and
  the isolated full-suite comparison shows no new failure attributable to this round
  (`var/FAR-MINIMAX-MANDATE-20261021/pytest_diff.json`)
- [x] 5.5 **The publish branch is clean** — this round publishes on
  `pub/far-minimax-mandate-20261021` (based on `origin/main`), because the earlier branch
  `pub/far-lane-remediation-20261021` was contaminated by another session's commits
  (`8fdb9f3`, SBL r7 artifacts) and by 177 stray `fabric-autonomous-research/runs/**` files added by
  an over-broad `git add`. No force-push and no history rewrite; the contaminated branch is left
  intact for the owner to rule on
  (`EVIDENCE/FAR-MINIMAX-MANDATE-20261021/PUBLISH-BRANCH-INCIDENT.md`)

## 6. Blocked on the owner's ruling (NOT done)

- [ ] 6.1 Ruling A — tick the cross-verifiable OpenSpec items. Each tick must carry its own
  verification evidence. A batch tick is refused.
- [ ] 6.2 Ruling B — disposition of the 120 `var/` directories. The recommendation is to delete
  nothing except possibly the 3 runtime/cache + 2 empty directories, and that needs explicit
  approval.
- [ ] 6.3 Ruling C — the status of `HGK-EBC-TT-001` (needs a migration change) and
  `HGK-EBC-TT-002` (needs a cross-entity contract decision). TT-002's acceptance sub-scope is
  already repaired, but the ledger row must stay OPEN until the general contract is ruled on.
- [ ] 6.4 Ruling D — whether to restore model-axis separation. `gpt-6.1-sol` is already retained
  as an operator-selectable VERIFY arm, so restoring it needs no new pool re-binding.
- [ ] 6.5 Ruling E — whether the delegation plane stays on MiniMax permanently.
