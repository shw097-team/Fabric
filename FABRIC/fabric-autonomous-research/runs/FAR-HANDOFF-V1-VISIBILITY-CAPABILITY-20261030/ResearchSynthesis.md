# FAR synthesis — visibility that cannot lie, and three blocks that are not one block

Run `FAR-HANDOFF-V1-VISIBILITY-CAPABILITY-20261030` · 2026-10-30 · governance: Fabric / SBL / HG-KSEOS

## 0. What was actually measured before any reasoning

| Time | Measurement | How |
|---|---|---|
| 23:44:08 | WP-FHS-20 PLAN dispatched, pid 7284 | driver log |
| 23:48:16 | pid 7284 + child codex 6224 alive | `Get-CimInstance Win32_Process` |
| 23:50:23 | `brief.md` 20,657 B, first line `NONCE-ECHO: …234408` | file stat |
| 23:50:2x | receipt `ok:true`, rank 1, `gpt-6.1-sol`, **323.72 s**, `nonce_present:true` | `WP-FHS-20-plan-20261030234408.json` |
| 23:52:06 | `STATUS.json` still lists pid 7284 **as live, 8.0 min** | `C:/wg/queue/STATUS.json` |
| 23:59:41 | no dispatcher alive; only two stale `codex.exe` from 17:29 | process scan |

**The report was true when written and false fifteen minutes later, and nothing in the system marks the difference.**

## 1. Q1 — is it a lie?

No, and that does not help. The failure is structural: **a projection with no freshness contract**.

* Liveness is sampled *at the moment the status file is written* and never expires. A status file is a claim about
  a moving system that carries no expiry, so it can only become wrong, never self-correct.
* The todo mirror is written at the same instant and inherits the same age. The owner reads at 23:59 and sees what
  was true at 23:52.
* Two unrelated fields are rendered as one word. The queue's `blocked` means *DAG dependency unsatisfied*; the run's
  `running` means *a process exists now*. The goal list showed the first and the chat said the second, and both were
  rendered as if they answered "is anything happening".
* This is the third member of one family already diagnosed twice on this host: `wmic` missing → "no dispatch"
  (a broken probe reported as a fact), `text=True` on cp950 → "nothing running" (a decode error swallowed as idle),
  now a status file with no age → "still running" (a stale sample reported as now).

**Ruling OD-Z1 — a projection must carry its own expiry.** Every receipt gains `started_at`, `ended_at`, `exit`.
`STATUS.json` gains `as_of` and `stale_after_seconds`; any consumer that reads it older than that must print
`STALE (as of HH:MM)` and never "running". `todo_list` states the same `as of HH:MM` line, re-derived each turn.
A projection that cannot be told apart from a lie is a defect even when every sample in it was honest.

## 2. Q2 — the windows

Root cause, stated as a Windows rule: **a process with no console gives every console-program it launches a brand
new console, and a new console is a visible window.** A headless driver is therefore not enough; each child must be
told `CREATE_NO_WINDOW` or the tree is visibly noisy.

Measured sources on this host, in order of how often they fired:

| Source | Spawns | Status |
|---|---|---|
| My own matrix probe at 23:47 (`cmd /c hermes --version`, `cmd /c codex --version`) | **96 in one minute** | fixed: `winproc.install()` |
| `hgk-lane-dispatch.py` → `codex.exe` per attempt (and per fallback attempt) | several per sitting | fixed: `winproc.install()` |
| Ad-hoc `powershell -NoProfile …` from probes | every probe | fixed: `CREATE_NO_WINDOW` |
| Cron: Hermes starts `hgk_continuation.py` with **`python.exe`** | 1 per 15 min | mitigated: the wrapper re-execs itself under `pythonw.exe` |

The 96-in-a-minute burst is the one the owner saw: a matrix probe is a legitimate, high-fan-out operation, and it ran
from an interpreter that had not installed the wrapper. **Any high-fan-out probe must be hidden by construction, not
by remembering.**

**Ruling OD-Z2 — console-hiding is a property of the entry point, not of the call site.** Every headless entry
installs `winproc` before its first spawn, and `winproc` counts what it hid so the receipt can state
`children_hidden: N`. Verification never depends on the owner watching the screen: `MainWindowHandle == 0` on a live
child is the check.

Residual, stated rather than hidden: the scheduler's own first `python.exe` (~50 ms before the re-exec) and the app's
own terminal pane are not mine to flag off.

## 3. Q3 — the three blocks are not one block

I offered the owner a choice between "provide capability" and "lower the standard". That framing was wrong, and it
was wrong in a specific way: **I collapsed three different missing things into one and then made the standard the
variable.**

| Block | What is actually missing | Cost of the honest fix | Cost of the shortcut I proposed |
|---|---|---|---|
| WP-17 → 13 | a **native grant** for `install_occupant` | route the grant through the owner-key envelope (`WIN-*`, scope `permit_sign, admission_bundle_sign`) that already exists; one owner unlock | call a conformance seam "production" |
| WP-20 → 10 | two host CLIs **installed** | `npm` user-scope install of Claude Code; DeepSeek harness via `opencode`; no admin, no policy change | count NoFit as evidence |
| WP-11 | **nine lifecycle cells** built | same shape as the WP-17 installer: install/load/invoke/nontrigger/remove per host | declare the matrix incomplete-but-passed |

None of the three needs the acceptance standard to move. Two of the three need a capability this machine does not
have **yet**; one needs an engineering artefact. The shortcut only looks cheaper because it hides the cost inside a
word ("seam", "NoFit") where the owner cannot see it.

**Ruling OD-Z3 — acquire capability, do not redefine sufficiency.** Ranked by the owner's own priority order
(delivery alignment > native E2E closed loop > unattended automation > necessity > minimal governance > low friction):

1. **Capability acquisition, unattended, no admin**: install the two missing host CLIs user-scope and re-run the
   matrix. 96 NoFit become 96 RAW with no standard touched. This is the highest-value move and it is pure execution.
2. **Grant routing through the existing native path**: the owner envelope is the production issuer on this host; the
   only irreducible owner action is unlocking the key. Everything downstream — bundle, WriteSet, receipt — is mine.
3. **WP-11's nine cells**: build them; they are the same pattern as the occupant installer that the AO already
   accepted structurally.
4. **Never**: PASS by substitution, NoFit read as evidence, or a seam described as an anchor.

## 4. What was executed in this run, not only recommended

| Item | State |
|---|---|
| `winproc.py` + installed at every headless entry | done, `MainWindowHandle == 0` measured |
| cron wrapper re-exec under `pythonw.exe` | done, `driver.log` grows while no window exists |
| `occupant_install.py` (WP-17 lifecycle, negatives, rollback) | done, AO-accepted except for grant assurance |
| `host_matrix.py` (192 cells parsed from the delivery, foreign-evidence refusal) | done, 96 RAW / 96 NoFit / 0 foreign |
| `PRE_ATTEMPT` receipt before spawn | done, third silent death now visible |
| `STATUS.json` `as_of` / `stale_after` / `ended_at` | **this run** (see §5) |
| capability acquisition (claude-code, opencode) | attempted; see `ResearchHandoff.yaml` for the measured result |

## 5. Freshness contract, as implemented

    STATUS.json  { as_of, stale_after_seconds, live:[{pid, started, minutes, alive}], finished:[{wp, ended_at, exit}] }
    consumer     age > stale_after → print "STALE (as of …)", never "running"
    todo_list    one line, always "as of HH:MM:SS"

The point is not more fields. The point is that **the projection is allowed to expire on its own**, so a quiet
system reads as quiet instead of reading as busy.

## 6. Open questions the owner owns

`OD-Z4` — if a host CLI cannot be installed on this machine at all (licence, no network), the cells stay
`NOT_RUN` with that reason, and WP-20 stays FAIL. That is the honest end state, and it is not a pass.
`OD-Z5` — the owner envelope unlock is the single action I cannot take for the owner; every other step of the
grant chain is automated.
