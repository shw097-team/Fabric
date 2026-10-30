# FAR — the loop existed; the driver I wrote did not use it, and the clock was paused

Run `FAR-HANDOFF-V1-LOOP-REUSE-AND-CLOCK-20261031` · 2026-10-31 · Fabric contract / SBL entry / HG-KSEOS control plane

## 1. Why "the first loop-authored implementation" is late rather than new

Measured, not remembered:

| Fact | Evidence |
|---|---|
| `--lane EXECUTE` existed in the lane runtime since **2026-10-21** | `git log -S"--lane EXECUTE" -- scripts` → `051d574 FAR-CLOSURE-20261021-R3: land the lane runtime` |
| The lane runtime itself is 8+ commits deep (route, policy, guard, preflight, toolchain) | `scripts/hgk-lane-*.py`, `hgk-lane-dispatch.py` 189,795 B |
| `continuation_driver.py` is **one day old** | `git log -- scripts/continuation_driver.py` → first commit `42016f7 continuation: move the loop out of the turn and into a clock` |
| That driver dispatched only PLAN and VERIFY | `plan_prompt` + `verify_prompt`, no `execute_prompt`; 0 hits for `--lane EXECUTE` in `C:/wg/queue` |

So the three-lane **mechanism** was never missing. What was missing was that **my** continuation graph — written yesterday as if
the lane runtime did not already have an EXECUTE arm — carried two of the mandate's three lanes. The first
loop-authored implementation therefore appeared when I wired the third edge (01:01), not when the capability appeared
(2026-10-21).

B1 and SKELETON_SPINE did not have "a loop" either: a scan of 137 executable files in those trees found no scheduler,
queue or driver — their content is documents plus the delivery's own readers. What B1 *did* have, and what I failed to
reuse, is the lane runtime and an admission module (next section).

## 2. Rebuild audit: what existed and was rebuilt anyway

| Thing | Already existed | What I built | Verdict |
|---|---|---|---|
| Lane dispatch | `b1_closure_20261028/code/hgk-lane-dispatch.py`, in HG-KSEOS and evolved | — | **reused, correct** |
| Lane routing registry | `b1_closure_20261028/code/lane-routing-registry.yaml` | — | **reused, correct** |
| Native admission | `b1_closure_20261028/code/native_admission.py` (22,646 B, `HGK-B1-ASCII-C14N/1`, OS-protected owner config, no local key creation, no second DB) | `scripts/issue_grant.py` (241 lines, Ed25519 + nonce ledger + admission) | **DUPLICATE — should have been reused** |
| Kanban for tracking | Hermes `kanban_db_dispatch.py` (133 KB) present in the delivery's reader copy | `work_queue.py` tables | partial duplicate (justified: the registry is the canonical state, but I should have said so instead of quietly building a second one) |
| Skeleton/B1 delivery content | promoted as `b1_closure_20261028/` + `SKELETON_SPINE_r2_revision2.zip` | nothing (good) | **no duplication** |

The duplication that matters is `native_admission.py` → `issue_grant.py`. The B1 module was written for exactly this
problem ("no local key creation, no caller-asserted trust") and I re-derived a narrower version of it. Ruling OD-AB1
below records what to do about it.

## 3. "The wrong place": inventory, promotion, closure

The wrong place is the documentation tree
`...\SBL_PIPD\FHS-MSC\` — not a git repository, invisible to every test, reviewer and repo reader.

Inventory (SHA-256 per file in `archive/WRONG_PLACE_INVENTORY_20261031.json` of the delivery repo):

| Tree | Files | Bytes | Classification |
|---|---|---|---|
| `B1/` | 141 | 17.6 MB | 26 PROMOTED_CODE · 89 ARCHIVE_DOC · 26 DISCARD_ARTEFACT |
| `FHS-MSC_PIPD-LS-PKG/SKELETON_SPINE/` | 291 | — | 136 ARCHIVE_CODE · 144 ARCHIVE_DOC · 11 DISCARD_ARTEFACT |
| `..._HANDOFF-PATCH-v1/` | 1984 | 936 MB | **primary source — read-only, never closed** |

Promotion is already in the delivery repo: `b1_closure_20261028/` (30 files incl. lane dispatch, registry, native
admission, owner ruling) and `deliveries/SKELETON_SPINE_r2_revision2.zip` + manifest.

Closure, two layers, both measured:

```
HG-KSEOS/config/closed_paths.yaml            <- the decision, with promoted_to and the undo command
closed_paths_gate.py check <path>            -> CLOSED_PATH, exit 3 (called before every dispatch)
icacls <tree> /deny %USERNAME%:(OI)(CI)(WD,AD)
  write probe -> PermissionError [Errno 13]  <- refused, not "please don't"
```

`CLOSED.md` sits at the tree root and states what is promoted where and how to lift the closure (as a decision, not a
step).

## 4. The clock: 15 minutes was the wrong instrument, and it was not even running

Two separate defects:

1. **Cadence.** One EXECUTE run takes 15-30 min on this host (measured: 900 s cut a run mid-file; attempt 2 needed
   1800 s). A 15-minute timer that *decides when work may start* adds up to 15 min of latency per unit and serialises
   independent units. Six units → hours of pure waiting.
2. **It was paused.** The cron job `2d9fbc9715e7` was in state `paused` since **00:24:11**, while three turns described
   "the 15-minute loop". Pausing was silent, and nothing printed it.

The delivery also forbids the shape: `11_WORKPACKAGES_AND_DAG.md` — "依賴原服務，不創第二 Scheduler";
`REPAIR_CLOSURE_REPORT.md` — "未造第二 Queue、Scheduler、Issuer、Checker 或 Canonical Writer". A timer that decides
when work may start *is* a second scheduler by any reading.

Replacement, measured at 01:21:30 — three lanes in flight at once:

```
STATUS: RUNNING — WP-FHS-20 EXECUTE pid 2900, WP-FHS-11 EXECUTE pid 18268
supervisor: holds no queue, no cadence policy, no ordering
  readiness  <- work_queue.py next --wp   (the DAG projection)
  dispatch   <- continuation_driver.py    (the lane runtime owner)
  registry   <- acceptances               (the original state store)
  poll 5 s, max 3 in flight, exits when nothing is ready
watchdog (cron, every 3 min): starts the supervisor if dead, then exits -- never decides what runs
```

With parallel readiness-aware dispatch, the six remaining units are no longer one queue behind one timer: independent
pairs run together, and a unit starts within seconds of becoming ready.

## 5. Rulings

| ID | Ruling |
|---|---|
| OD-AB1 | `native_admission.py` is the admission authority; `issue_grant.py` is a bounded adapter until it is replaced by the B1 module. Recorded as a TT, not quietly kept. |
| OD-AB2 | Readiness comes from the DAG projection and dispatch from the lane runtime. Nothing in the loop may hold its own queue or decide its own order. |
| OD-AB3 | The loop's clock is a process that reacts in seconds; cron is only a liveness check (3 min). A paused clock must be visible in STATUS. |
| OD-AB4 | Closed paths are enforced twice: a gate that refuses before dispatch and an ACL that refuses after. Promotion is the only way out. |
| OD-AB5 | A supervisor writes its own pid; a watchdog that writes it too created three supervisors and duplicate dispatches on the same unit (measured 01:32). |

## 6. What this run got wrong while fixing the previous wrong thing

While replacing the clock I introduced, and then caught, a duplicate-supervisor loop: the watchdog wrote the pid file
and the supervisor wrote it too, so each watchdog tick saw a stale pid and spawned another. It produced two EXECUTE
dispatches on WP-FHS-11 at once. Fixed by single ownership of the pid file and by treating a live
`hgk-lane-dispatch` process for the unit as "in flight" regardless of receipt state. Residual risk: a dispatch that
dies between spawn and receipt can be started twice; the receipt's nonce makes the duplicate identifiable, and the
cure is the same as everywhere else in this project — the second dispatch refuses when it finds a live lock for the
unit.
