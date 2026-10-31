# Executable plan — R1…R7 (what runs next, in order)

Every step is a command, has a pass condition that is a measurement, and fails closed. Nothing here is
approved by prose: a step is done when its receipt says so.

## R1 — transport up (idempotent)

```bash
cd /c/Projects/Agent_Workspace/HG-KSEOS
python scripts/relay_daemon.py status          # expect verdict RELAY_OK
python scripts/relay_daemon.py start           # only if RELAY_DOWN; prints health + console:"none"
curl -s -m 5 http://127.0.0.1:10101/healthz    # expect {"status":"ok",...}
```

Pass: `RELAY_OK`. Note: `10102` is the Codex Desktop router and is **not** this relay — never treat its
listener as ours.

## R2 — one work package, one brief, EXECUTE measured

```bash
python scripts/continuation_driver.py --once --wp WP-FHS-17
```

Pass: a receipt whose attempt has `exit 0`, `nonce_present true`, `usage_receipt_ok true`, `rank 1`,
`asked == served`, **`console_window_events_delta == 0`**.
Fail-closed: if `delta > 0`, do not re-run blindly — read `console_window_owners`, and treat the owner
executable as a spawn site defect (FAR-028 F6). If `delta` is `null`, the watcher was not running:
`python scripts/window_watch.py --start` and re-measure.

## R3 — independent VERIFY on the same package

```bash
python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY \
  --prompt <verify brief> --nonce <nonce> \
  --relay-base http://127.0.0.1:10101/v1 --relay-home C:/Users/user/.opencodex \
  --usage C:/Users/user/.opencodex/usage.jsonl --codex-home C:/Users/user/.codex \
  --allow-human-home-transport --identity-source codex-rollout --cwd C:/wg/queue \
  --timeout 900 --sandbox read-only \
  --require-arm opencode-go/mimo-v2.6-flash --json-out <verify receipt>
```

Pass: `ok true`, `used_rank 1`, `provider opencode-go`, `model mimo-v2.6-flash`, delta 0.

## R4 — round closure with F3 blocking

```bash
python scripts/round_close_gate.py --round <round-id> \
  --lane-receipt "EXECUTE=<execute receipt>" \
  --lane-receipt "VERIFY_SECURITY=<verify receipt>"
```

Pass: `ROUND_MAY_CLOSE` with an empty `problems`. Three refusal classes are load-bearing here:
`blocking_tt_open`, `ERR_CONSOLE_WINDOW_EMITTED`, `ERR_CONSOLE_WINDOW_UNMEASURED`.

## R5 — the same shape for the other two packages

WP-FHS-11, then WP-FHS-20, each as **one package per brief** (the 1500 s wall is a brief-width fact, not a
lane-capacity fact). Per-unit locks mean they may run in parallel, but each still needs its own R3 + R4.

## R6 — registry and panels

```bash
python scripts/lane_policy_reconcile.py --check     # expect CONSISTENT
python -m pytest tests/test_lane_policy.py tests/test_console_window_gate.py -q
python scripts/console_guard_gate.py --all          # expect ok == checked, hides_one_level_only == []
```

Then the four governed surfaces (KANBAN board, SWARM independent lanes, GSTACK route evidence, OPENSPEC
brownfield route evidence) each with raw evidence and an independent checker result.

## R7 — ship

`git add` → commit → push HG-KSEOS, Fabric, and the queue repo; update `HANDOFF-20261031-LANE-OPS.md` with
the round state, the open TT, and the next command to run.

## Stop conditions (do not burn a round on these)

1. `RELAY_DOWN` after a `start` → transport defect, not a lane defect: read `relay_daemon.py status` procs.
2. `delta null` twice in a row → the watcher is down; fix the instrument before measuring again.
3. `ERR_REQUIRED_ARM_NOT_SERVED` with `exit 0` + nonce + usage → identity resolution, not the arm.
4. `silent_substitution` where `provider` matches the asked id's prefix → the comparator, not the lane.
