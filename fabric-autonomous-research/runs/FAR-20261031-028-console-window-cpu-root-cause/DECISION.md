# Decision — FAR-20261031-028

| | |
|---|---|
| decision id | `FAR-028-DECISION-01` |
| round | `FAR-20261031-028-console-window-cpu-root-cause` |
| authority | HG-KSEOS control plane; owner pre-authorised the engineering ruling (see `OWNER_MANDATE.txt`) |
| change class | engineering-base, reversible, code-scoped, no authority change |
| claim ceiling | MEASURED_LOCAL attribution · INCONCLUSIVE reproduction |

## 1. Ruling

1. **The defect is a class, not a task.** Console-subsystem processes started from a context without a console
   get a new console; on a Windows Terminal host that console is a visible window. Any fix scoped to "the task
   that opens the window" is superseded by this ruling.
2. **Adopt F1, F4, F5** (already applied in this round): hidden-console inheritance tree-wide; no top-up of a
   unit whose budget is spent; per-unit locks; orphan launch markers are not spent rounds.
3. **Adopt F2** (liveness proof in `detach`): a launcher may not return `ok` for a child it cannot see alive
   after a bounded interval.
4. **Adopt F3** (window delta recorded per dispatch): every EXECUTE/PLAN/VERIFY receipt carries
   `console_window_events_delta` and the owner pids observed during the dispatch window. Blocking enforcement
   is enabled per round mandate once a full round shows delta = 0 without a false positive from the owner's
   5-minute task.
5. **Adopt F6** (gate extension): `console_guard_gate` reports any spawn site that relies on
   `CREATE_NO_WINDOW` alone as `HIDES_ONE_LEVEL_ONLY`, so the old shape cannot be reintroduced silently.
6. **Not taken here (owner decisions):** F7's `PT5M → PT15M` interval change, and F8 stopping the second Hermes
   instance (`TT-HOST-SECOND-HERMES-001`).

## 2. Authorisation and signature

- The owner's authority envelope is `config/issuer/OWNER_AUTHORIZATION.json` (DPAPI-bound; no passphrase prompt
  is required on this host — verified in this session, so no owner-key envelope window was opened).
- This decision is issued as an **engineering-base** change. It does **not** authorise production, release,
  Stage-3 entry, or any live path.
- Signature recommendation: seal the decision digest with `scripts/issue_grant.py` under the existing issuer
  key, and attach the resulting grant to the round's `EVIDENCE_INDEX.json` before the AO lane reads it.

## 3. Rollout

| step | action | gate |
|---|---|---|
| R1 | F1/F4/F5 (applied) + F2/F3/F6 (this round) committed | `console_guard_gate --all` = 31/31, `lane_policy_reconcile --check` = CONSISTENT |
| R2 | one full round with `console_window_events_delta` recorded on every lane receipt | delta = 0 on ≥ 1 complete round |
| R3 | enable blocking refusal (`ERR_CONSOLE_WINDOW_EMITTED`) for EXECUTE | a round that closes with 0 refusals and 0 false positives |
| R4 | scheduled-task interval review (owner) | owner sign-off |

## 4. Rollback

Every change is a single-file revert: `scripts/winproc.py` (hidden-console inheritance), `scripts/detach.py`
(liveness), `scripts/hgk-lane-dispatch.py` (delta field), `scripts/console_guard_gate.py` (new AST class),
`scripts/continuation_driver.py` (lock key, budget age rule, fan-out halt). `git revert <sha>` restores the
previous behaviour with no state migration; the evidence files are append-only and are never rewritten.

## 5. What the AO lane must check independently

1. `EVIDENCE_INDEX.json` digests match the files (no self-referential entry).
2. §3 numbers reproduce from `evidence/console-window-events.jsonl` alone.
3. The three probe results are reported as **INCONCLUSIVE**, not as a pass, and the report's claim ceiling
   matches them.
4. F1/F4/F5 are present in the tree at the cited lines, and F2/F3/F6 are either applied with a test or listed
   as proposed — a "proposed" item may not be counted as a fix.
