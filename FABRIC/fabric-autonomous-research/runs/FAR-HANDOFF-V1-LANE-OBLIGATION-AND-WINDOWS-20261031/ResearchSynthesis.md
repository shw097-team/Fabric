# FAR — lane obligation and the console-window root cause

Run: `FAR-HANDOFF-V1-LANE-OBLIGATION-AND-WINDOWS-20261031`
Written: 2026-10-31 08:33:40 (UTC+08:00)
Author of this file: the interactive session, whose pinned arm is `opencode-go/deepseek-v4.1-flash` — the **EXECUTE**
arm. PLAN (`openai-codex/gpt-6.1-sol`) was dispatched for this run at 08:18:09 (`NONCE-FAR-LANEOBL-20261031081809`) and
was still running when this synthesis was written; the VERIFY sitting has not been held yet.

**Therefore this document is not yet valid research by its own gate.** `scripts/far_lane_gate.py` (written today)
answers `INVALID_RESEARCH` for it until `PLAN_RECEIPT.json` and `VERIFY_RECEIPT.json` land in the run directory. That
verdict is printed on purpose: it is the same defect the report is about.

---

## Q1 — why the FAR work never used the three lanes

### What was measured

| Fact | Number | Source |
|---|---|---|
| Lane receipts in `C:\wg\queue` (every dispatch the loop ever made) | EXECUTE 18 · VERIFY_SECURITY 8 · **PLAN 2** | receipt scan, 2026-10-31 |
| PLAN receipts, ever | 2 (`WP-FHS-11` 22:57, `WP-FHS-20` 23:44 on 10-30) — both after the owner asked three times | same |
| FAR run directories from this session | 8 | `fabric-autonomous-research/runs` |
| FAR runs carrying a PLAN receipt | **0** | same |
| FAR runs carrying any lane receipt | 1 of 8 | same |

### Root cause (structural, not personal)

A FAR run was admitted by **directory existence**: `runs/<name>/` with a `ResearchSynthesis.md` inside read as a
finished study to every reader, including me. Nothing in the artefact's own rule named who had to produce it, so the
cheapest producer won — the session, which is the EXECUTE arm. The mandate's lane clause was enforced only where a
*work package* claimed a lane (`lane_evidence_gate.py`, `round_close_gate.py`); research claimed nothing, so it was
checked by nothing.

Second order, and this is the part that made it recur: the session model **is** the EXECUTE arm. So an in-session
report is not "PLAN work done badly" — it is EXECUTE work with a research-shaped filename, and no field in the
artefact could contradict that. The failure was invisible because PLAN leaves prose, and prose has no receipt.

The loop had a matching blind spot: `continuation_driver.py` dispatches PLAN only when a work package has *no brief*.
Research runs arrive pre-briefed (by the session), so the driver never saw them as units of work at all.

### Ruling R-1 — a research run must carry its lanes

- **Rule.** `runs/<name>/` is `VALID_RESEARCH` only with a `PLAN_RECEIPT.json` (lane PLAN, served
  `openai-codex/gpt-6.1-sol`, nonce echoed, `lane_evidence_gate` exit 0) **and** a `VERIFY_RECEIPT.json` (lane
  VERIFY_SECURITY, same pinned arm), **and** a synthesis that cites both files by name.
- **Enforced by** `scripts/far_lane_gate.py` (exit 3 `INVALID_RESEARCH`), meant to run before any FAR finding is
  transcribed into the registry or quoted in a round-close.
- **Why this layer.** A rule in a prompt is advice; a rule in the artefact's admission check is a wall. The run
  directory is the only place both the producer and the reader must pass through.

### Ruling R-2 — a lane receipt must survive the turn that made it

The four failed PLAN attempts today each refused **before spawn**, and each refusal was a real gate: `RELAY_DOWN`
(the relay had died and nothing noticed), `ERR_DURABLE_GATE_NO_GO` (subject not committed), and
`ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT` (the harness wrote its receipt inside the guard root). Those are the gates
working. The defect is that a refused dispatch leaves *no* durable trace in the research run, so the owner sees a
report with no lanes and no reason. Ruling: a refused dispatch writes its refusal into the run directory as
`LANE_REFUSED-<lane>.json` with the code and the fix, so "no receipt" always has a cause on disk.

---

## Q2 — why console windows keep appearing, worse each time, sometimes in a loop

### What was measured

1. `scripts/console_guard_gate.py` parses each entry point with `ast` and requires the console guard to be an
   **executed module-level node**. Before today **7 files failed**, including the two that matter most:
   `hgk-lane-dispatch.py` and `ops_status.py` (also `stall_monitor.py`, `review_lock.py`, and three more).
2. In those files the guard sat **inside the module docstring** — `try: import winproc; winproc.install()` inserted
   above the docstring body. Text in a docstring never runs.
3. So `winproc.install()` never executed in the dispatcher, and every `codex.exe` / `powershell.exe` child it started
   allocated a **new console**. On Windows 11 a new console is a Windows Terminal window on the desktop.
4. Window-event log: 46 events in the 02:00 hour and 30 in the 07:00 hour, all `powershell.exe`, `cmd.exe`,
   `WindowsTerminal.exe` — i.e. bursts during dispatch, not at idle.
5. Three independent launchers existed for the single 10101 relay: the Startup-folder
   `ocx-relay-start.cmd` (`start "" /min ocx.cmd start --port 10101`, run at logon through a console host → the
   "opencodex proxy running on http://localhost:10101" window), the scheduled task
   `HGK-OpenCodex-Sealed-10101` (`Hidden: true`, launched via `wscript` → genuinely windowless), and
   `relay_daemon.py`.
6. `detach.py` (written today to escape the Hermes job object) first wrapped every launch in `cmd /c … >> log`;
   `Win32_Process.Create` starts `cmd.exe` **with** a console → 10 `cmd.exe` + 20 Windows Terminal windows in three
   minutes.

### Root cause

**Both previous fixes verified that the file contained the guard, not that the process ran it.** The check was
`grep creationflags` / `grep winproc` — both passed while the statement was dead text. And each fix introduced a new
launch path (cron → `pythonw` wrapper; then `detach` → `cmd /c`), so the window source moved rather than disappeared.
The recurrence mechanism is therefore: *a hiding measure applied at the call site, verified by reading the source,
while a second launcher existed outside the code path being read.*

### Ruling R-3 — the guard is proven by execution, not by presence

`console_guard_gate.py` is the enforcement: AST-level, module-body-only, exit 3 `CONSOLE_GUARD_NOT_EXECUTED`. A file
that carries the guard as a docstring string fails. This is the check that would have caught both earlier "fixes".

### Ruling R-4 — one service, one launcher; and the launcher must be consoleless

- The Startup `.cmd` is archived (`var/autostart-archive/`, with `WHY.md`); the scheduled task (hidden, `wscript`) and
  `relay_daemon.py` (CREATE_NO_WINDOW) remain.
- `detach.py` launches `pythonw.exe` directly; it never wraps in `cmd /c`.
- Any new autostart must be a `.vbs`/`wscript` or `pythonw` entry. A `.cmd`/`.bat` in Startup is a visible console by
  construction, no matter what flags the process inside uses.

### Measurement after the repair

```
17 lane processes live during a tick · 0 console-window events in 75 s
relay health 200 · visible_windows [] · relay procs: node/bun, main_window 0
```

### Falsifiers

- Q1: if a run directory with no lane receipts can pass `far_lane_gate.py`, the diagnosis is wrong. Measured today:
  it exits 3 with `INVALID_RESEARCH`.
- Q2: if a dispatch from the repaired tree produces a console window event, the diagnosis is incomplete. The 75-second
  measurement above is the counter-test; re-run it after any change to a launcher.

---

## What I would not do

- No second scheduler, no second issuer, no second queue: the FAR gate is a check, not a runner.
- No "always dispatch PLAN for everything": a research run needs PLAN + VERIFY, not a lane ceremony for a question
  that a single receipt can answer.
- No removal of the dispatch gates that refused four attempts today. They refused for real reasons; the missing piece
  was recording the refusal where the reader looks.
