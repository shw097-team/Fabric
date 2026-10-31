# FAR-20261031-031 — self-research, self-learning and evolution record for this round

Round: `FHS-MSC-PIPD-LS-PKG-ALL-PASS-20261031` · subject: `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`
Predecessor study: `Fabric/fabric-autonomous-research/runs/FAR-20261031-031-FHS-MSC-ALL-PASS/`

This is the governed retrospection the round requires: what was learned, what changed because of it, and what a
future round must not have to rediscover.

## 1. The three findings that changed the round

### 1.1 A refusal that names an object is still a claim — check whether the object exists

The prior round recorded six work packages as `HOST_OP` failures with
`REFUSAL-20261030-NO-HOST-CAPABILITY`. This round measured the chain instead of reading the refusal:
the Issuer key was present and DPAPI-bound, `issue_grant.py` signed a grant that the receiver's own gate accepted
(14/14 binding checks), and the install ran to `FUNCTIONALLY_QUALIFIED`. The absent object was never "host
capability"; it was a `str`/`Path` mismatch and a hard-coded `"PARK"` string.

**Rule learned:** before accepting any refusal, execute the named service once and record its actual answer.
`REFUSAL-*` receipts are inputs to an investigation, never a finding on their own.

### 1.2 The same round can carry two opposite conclusions about the same lane

`P5C_LANE_VERIFY_BLOCKED` and this round's measurements are both "true" if you only look at the receipt code:
`ERR_LANE_ALL_ROUTES_EXHAUSTED` appears in both. The difference is a flag. Two dispatches, same lane, same arm,
one exhausted and one `ok: true`, differ only in `--identity-source`.

**Rule learned:** a lane verdict must quote the identity source, the rank, the served arm and the nonce echo, or
it is not a lane verdict. `hgk-lane-durability` now carries this as its transport section.

### 1.3 A declaration and its projection can disagree while every test is green

Three declarations contradicted the binding this round put in force, and each was invisible:

| Declaration | Said | Reality | What caught it |
|---|---|---|---|
| `transport_model` on the VERIFY route | `opencode-go/mimo-v2.6-flash` | provider/model = `openai-codex/gpt-6.1-sol` | `test_openai_codex_transport_models_are_bare` |
| `sod_invariants.pairs[PLAN,VERIFY]` | `distinct_required: true` | both bound to gpt-6.1-sol | the SoD sweep, once the pair was read from data |
| `--identity-source` default | `relay-usage` | cannot resolve an OAuth-direct turn on this host | the same two dispatches above |

**Rule learned:** when an owner order changes a binding, the round must update *every* declaration that
described the old binding — the route, the projection oracle, the SoD pairs, the tests — and prove it with a
check that can say NO. A reconciler that "preserves per-arm metadata by rank slot" will happily re-create a
declaration that sends one arm while naming another.

## 2. What was promoted into the control plane this round

| Object | Before | After | Evidence |
|---|---|---|---|
| `WP-FHS-10` | `FAIL` (`NO-HOST-CAPABILITY`) | `PASS` by re-binding existing signed B1 evidence | `EVT-32277089ea9c024b`, `ACC-WP-FHS-10-V1` |
| `WP-FHS-17` | `NOT_RUN` (officer: `INCONCLUSIVE`) | measured chain, verdict from the VERIFY lane | `evidence/install.json`, `evidence/load.json`, `evidence/negatives/*` |
| lane policy | epoch 39 (VERIFY = MiMo) | epoch 40 (VERIFY = gpt-6.1-sol medium, MiMo fallback 1) | registry + assignment rev 41 + slot pool rev 36 |
| dispatcher default | `relay-usage` | `codex-rollout`, with `ERR_IDENTITY_SOURCE_NO_USAGE_ROW` as an additive diagnostic | `tests/test_lane_identity_source_default.py` |
| scoreboards | four answers, no ages | `scripts/scoreboard_consistency.py` (authority = `work_queue`) | `DIVERGENT` on this delivery, by design |

## 3. What this round deliberately did **not** do

- It did not promote `EXECUTED_BOUNDED_LOCAL` to native admission. The bounded receiver is not the original
  Host Installer/Loader/Registry and `EVIDENCE_GAP.md` still names the gap.
- It did not change the acceptance standard. `PASS` on WP-17 is the VERIFY lane's verdict over an oracle that was
  registered and hashed **before** the check; the maker (this session) did not write the officer's claim set.
- It did not force `candidate/r18` onto `main`. The two histories are unrelated (267 ahead / 83 behind, no merge
  base); the round published a main-based review branch instead and left the lineage decision named.
- It did not substitute `UNKNOWN` for `FAIL` anywhere: `WP-FHS-11/12/13/20` remain non-PASS.

## 4. Residual risk, stated plainly

1. **Shared-model correlation.** PLAN and VERIFY both run `gpt-6.1-sol` under epoch 40. `SOD006-C8` declares this
   as an owner-ordered deviation, so the collision is legal, but a blind spot shared by the planner and the
   checker is no longer detectable by identity comparison. Only process/lane/evidence-path independence remains.
2. **One session produced both the fix and the verdict.** The officer is a separate sealed process with a fresh
   context and a different lane, but it was dispatched by the same session that made the fixes. That is process
   independence, not human independence.
3. **The queue driver is halted.** `continuation_driver.py` stopped WP-17 after eleven EXECUTE receipts
   (`halted_repeat`, 19:17:08) and nothing restarted it. Unattended operation therefore depends on this round's
   fixes being present in the tree the driver dispatches into — which is true for `/c/wg/queue/WP-FHS-17` and not
   yet true for a fresh checkout.
4. **The delivery copy in the knowledge base is lossy.** 415 of 909 manifest rows are missing from the extracted
   copy (398 paths ≥260 chars, 17 rows under a renamed top directory). The bytes are intact in `C:\wg\pkg`
   (909/909 re-verified); the copy is not.

## 5. Recurrence controls added (so the same defect cannot return silently)

| Control | What it refuses |
|---|---|
| `tests/test_lane_identity_source_default.py` | a dispatcher whose default identity source cannot resolve an OAuth turn; a getattr fallback that disagrees with the declared default; any weakening of the frozen failure vocabulary |
| `lane_policy_reconcile.transport_for()` | a stale `transport_model` on a route or arm — the token is derived from the provider, not remembered |
| `sod_declaration_exemption()` + `SOD006-C8` | a same-model lane pair that is not declared; and a declared pair whose collision is not real |
| `scripts/scoreboard_consistency.py` | a projection that contradicts `work_queue`, or one older than its own `stale_after_seconds` |
| `scripts/acceptance_rebind.py` | silently rewriting a terminal verdict: a re-binding is a NEW `-V<n>` row, and the superseded row stays visible |
| `build_evidence.py` F4/F6/F7 | reading a stale receipt as this run's verdict; typing a disposition instead of deriving it |

## 6. What the next round should do first

1. Re-run `python tools/build_evidence.py` in `C:/wg/queue/WP-FHS-17` and compare the printed summary against
   `evidence/install.json` — the fixes are in the tree, so a regression shows up as a diff, not as a debate.
2. Read `scripts/scoreboard_consistency.py --json` before quoting any count. If it says `DIVERGENT`, fix the
   projection, never the authority.
3. For the remaining `HOST_OP` packages (`WP-11/12/13/20`), issue the grant the same way
   (`issue_grant.py admit` → `issue` → `verify`) and require the receiver's own gate to accept it — do not
   accept `PARK_GRANT_MISSING` as an answer again.
4. Native admission is still the real ceiling. It needs the original Host Installer/Registry path, not a
   better bounded receiver.
