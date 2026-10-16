# WS3 — measured defect-and-repair spec: dispatch_r6.py / dispatch_r9.py

Scope: two measured defects in the round dispatch wrappers (plus their dispatcher
`C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py` where the defect actually
executes). Nothing in the wrappers or in `lane_runs/` was modified; all writes landed under
`C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10/FAR/ws3/`.

---

## DEFECT 1 — per-role receipt path collision (per-turn overwrite)

### 1.1 Where the path is constructed (exact lines)

**dispatch_r6.py, `main()`, lines 51–61** (the two offending lines are 56–57):

```python
    cmd = [PY, DISP, "--lane", lane, "--prompt", brief, "--brief", str(brief_path),
           *LANE_CONF[lane], *LANE_EXTRA[lane],
           "--max-candidates", "1",
           "--round", round_name, "--attempt", attempt,
           "--output-root", LANE_RUNS,
           "--json-out", f"{LANE_RUNS}/{lane}_dispatch_receipt_attempt{attempt}.json",
           "--attempt-log-dir", f"{LANE_RUNS}/{lane}_logs_attempt{attempt}",
           "--cwd", HANDOVER,
           "--codex-executable", LIVE_CODEX,
           "--timeout", timeout_s,
           "--no-authorization-claim"]
```

dispatch_r9.py carries the identical construction at **lines 58–68, offending lines 63–64**:

```python
           "--json-out", f"{LANE_RUNS}/{lane}_dispatch_receipt_attempt{attempt}.json",
           "--attempt-log-dir", f"{LANE_RUNS}/{lane}_logs_attempt{attempt}",
```

The path depends only on `LANE_RUNS` (constant) + `lane` (argv[1]) + `attempt` (argv[3], defaults
to `"1"`). No round, turn index, or UTC stamp participates, so every turn of the same lane and the
same `attempt` argv writes the SAME file. The wrapper counter-argument "the attempt argv
differentiates turns" does not hold for this round: the measured EXECUTE receipt trail at
`…_attempt1.json` shows **five distinct turns** (five `run_id` values, five distinct stdout byte
counts) all attached to that one path via the shared `.attempts.ndjson` append trail:

| run_id | at_utc (turn end) | stdout_bytes |
|---|---|---|
| 2140-1792049969 | 2026-10-15T08:20:20.760378+00:00 | 3,541,041 |
| 4640-1792119447 | 2026-10-16T03:15:15.265649+00:00 | 563,555 |
| 2480-1792119780 | 2026-10-16T03:28:54.912512+00:00 | 803,905 |
| 5316-1792124385 | 2026-10-16T04:25:50.274623+00:00 | 113,758 |
| 1972-1792124816 | 2026-10-16T04:40:52.352624+00:00 | 322,713 |

The file on disk now (`EXECUTE_dispatch_receipt_attempt1.json`, 7701 bytes, mtime
2026-10-16 12:40:52 +0800) carries only the LAST turn (run_id `1972-1792124816`, narrow-window
R9B writer with stdout 322713 bytes and stderr tail citing apply_patch hunk errors); every earlier
turn's `ok/code/used_rank/used_seconds/attempts[]` record is GONE from the human-side ticket path —
those turns survive only as bare `attempts.`-ndjson rows with no final code attached. The same
shape is visible for `VERIFY_SECURITY_dispatch_receipt_attempt1.json` (3 turns, only
`1188-1792125708` = the R9 checker survives on disk), and for
`VERIFY_SECURITY_dispatch_receipt_attempt2.json` (2 turns, only `21748-1792074089` survives).

The lane-side attempt dirs, which DO encode UTC (`CNV-PIPD-LS-SP-20261015-R6/EXECUTE/attempt-1-<utc-ts>/`),
do not have this defect: the dispatcher's derived output dir helper refuses to reuse an already-
existing dir. The bug is exclusively the dispatcher-side `--json-out` / `--attempt-log-dir`
filenames that ignore that helper's per-turn stamp.

### 1.2 Observable failure

A second turn of the same lane inside one round silently overwrites the first turn's completion
receipt. Any attestation that says "the round produced N receipts" cannot be re-derived from
`lane_runs/*_dispatch_receipt_attempt1.json` — the file count (8 JSON + 7 ndjson) understates the
turn count (14 ranks in the trail), and every overwritten turn's final `ok/code/used_*` read is
unrecoverable from the ticket-path file.

### 1.3 Exact function/lines to change and the minimal repair (before/after)

Change **one line-pair inside `main()`** in both wrapper files; no dispatcher change is required
(and none is proposed for this defect). The repair: derive `json-out`/`attempt-log-dir` from a
per-turn immutable key `turn_id = f"{lane}_turn{turn}_{utc}"` appended to the lane name, and
crucially, snapshot BOTH files into the round root (`HANDOVER`) at the moment `subprocess.run`
returns, so a later turn in the same round cannot erase the evidence of an earlier one.

**BEFORE (dispatch_r6.py lines 56–57; dispatch_r9.py lines 63–64):**

```python
           "--json-out", f"{LANE_RUNS}/{lane}_dispatch_receipt_attempt{attempt}.json",
           "--attempt-log-dir", f"{LANE_RUNS}/{lane}_logs_attempt{attempt}",
```

**AFTER (identical patch applied to both files; drop-in):**

```python
import datetime as _dt                                   # only once, near the existing imports
    TURN_ID = _dt.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") \
              + "_" + str(round_name)                    # round-scoped, UTC-stamped, per-spawn
    json_out  = f"{HANDOVER}/lane_runs/{lane}_turn{TURN_ID}_attempt{attempt}_dispatch_receipt.json"
    trail_dir = f"{HANDOVER}/lane_runs/{lane}_turn{TURN_ID}_attempt{attempt}_logs"
    cmd = [PY, DISP, "--lane", lane, "--prompt", brief, "--brief", str(brief_path),
           *LANE_CONF[lane], *LANE_EXTRA[lane],
           "--max-candidates", "1",
           "--round", round_name, "--attempt", attempt,
           "--output-root", LANE_RUNS,
           "--json-out", json_out,
           "--attempt-log-dir", trail_dir,
           "--cwd", HANDOVER,
           "--codex-executable", LIVE_CODEX,
           "--timeout", timeout_s,
           "--no-authorization-claim"]
```

and immediately **after** the existing `print(f"=== DISPATCHER EXIT {r.returncode} ===")` line in
`main()` (dispatch_r6.py line 70; dispatch_r9.py line 77), add the round-root copy:

```python
    # per-turn round-root snapshot: an earlier turn's receipt must survive a later turn's write
    import shutil
    if Path(json_out).is_file():
        Path(HANDOVER).mkdir(parents=True, exist_ok=True)
        shutil.copy2(json_out, Path(HANDOVER) / Path(json_out).name)
    if Path(trail_dir).is_dir():
        shutil.copytree(trail_dir, Path(HANDOVER) / Path(trail_dir).name, dirs_exist_ok=True)
```

`round_name` already exists in `main()` ("CNV-PIPD-LS-SP-20261015-R6" / "-R9"), so `TURN_ID`
re-using it makes the file name round+lane+turn+UTC unique without adding a new argv; because the
copy happens at the moment `subprocess.run` returns, a later turn writing to a NEW path cannot
touch the snapshot — the old failure mode (one `*_attempt1.json` rewrite erasing the previous
turn's verdict fields) is structurally gone, not merely slowed.

### 1.4 What a TEST must assert

- Two sequential calls of the repaired wrapper for the same lane and the same `attempt` argument
  must produce two DIFFERENT `--json-out` basenames (no shared `"…attempt1.json"` filename), each
  carrying its own `used_rank` / `ok` / `code` / `used_seconds` / `attempts[0].run_id`.
- After the second turn returns, the round-root snapshots of BOTH turns exist under `HANDOVER`,
  neither is empty, and no path under `HANDOVER` was mutated by a turn whose dispatch started after
  it (mtime-ordering assertion).
- The `attempts.ndjson` trail for each turn lives under its own `…_turn<TURN_ID>_…_logs` dir, not a
  shared per-lane file.
- The existing collateral behaviour must NOT regress: the dispatcher still refuses to reuse an
  already-existing derived attempt output dir (`ERR_LANE_OUTPUT_DIR_EXISTS`), so two turns with the
  same TURN_ID still fail loudly instead of silently overwriting (negative control: manually
  pre-create the would-be path for turn 2 and assert the dispatcher, not the wrapper, is the one
  that refuses).

### 1.5 LOCAL fixture possible? YES.

No live lane, no relay, no network is needed:

- Fixture: copy `dispatch_r6.py` → `dispatch_r6_fixture_copy.py` inside a temp scratch dir; stub
  `main()`'s `subprocess.run` (or make `PY`/`DISP` point to a tiny fake script that just writes a
  receipt JSON containing a distinguishing `run_id`) and invoke `main()` twice with the same
  `lane`/`attempt` argv but different fake `run_id`s.
- asserts: (a) two distinct `json_out` Path values; (b) after turn 1 returns and turn 2 returns,
  both round-root snapshots exist and turn 1's snapshot still contains turn 1's `run_id`; (c) with
  the UNPATCHED wrapper the same fixture shows turn 1's file content replaced by turn 2's `run_id`
  (the negative control that demonstrates the defect).
- This is a pure local-file/filesystem exercise.

---

## DEFECT 2 — nonce gate misses a nonce the lane DID emit into its own artifacts

### 2.1 Where the wrapper's receipt path of the nonce gate lives

The gate is NOT in the wrapper; it is in the dispatcher the wrapper calls:
`C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py`. Measured surfaces it reads:

**Run attempt, line 1179–1188** (the only stdout-based nonce carrier):

```python
    nonce_bytes = args.nonce.encode("utf-8")
    nonce_raw = nonce_bytes in out_b
    …
    nonce_ok = nonce_in_agent_message(out_b, args.nonce) and nonce_raw
```

plus the recorded carrier-extraction rule at **line 1266–1267** and the account-oracle at
**lines 447–463** (`nonce_in_agent_message`), which reads only `item.completed`/`agent_message`
JSON carriers inside `stdout` bytes. **No filesystem/artifact-root read participates.**

**Final classification, lines 1033–1062 (`failure_disposition`) and 2124–2139 (`used = att`):**

```python
    answered = [a for a in attempts if a.get("exit") == 0 and a.get("usage_receipt_ok")]
    if answered and not any(a.get("nonce_present") for a in answered):
        return {"code": "ERR_NO_ARM_EMITTED_NONCE", …}
```

and

```python
        if att.get("exit") == 0 and att.get("nonce_present") and att.get("usage_receipt_ok"):
            …
            if _ce is None:
                used = att
                break
```

The receipt that the wrapper's round then consumed (HEAD of
`VERIFY_SECURITY_dispatch_receipt_attempt1.json`, mtime 2026-10-16 12:54:37 +0800) already
carried the hard evidence of the miss:

```json
  "attempts": [ { "rank": 1, "provider": "openai-codex", "model": "gpt-6.1-sol",
                  "nonce_present": false, … } ],
  "used_rank": null, "used_transport_model": null, "used_seconds": null,
  "ok": false, "code": "ERR_NO_ARM_EMITTED_NONCE",
  "nonce_absent_arms": ["openai-codex/gpt-6.1-sol"]
```

while the lane's OWN artifact root had, at that same mtime window, both:

- `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/R9_VERIFY/R9V_DONE`
  (24 bytes, contents `R9V-CHECKER-NONCE-5c1d84\n` — the exact nonce the brief mandated),
- `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/R9_VERIFY/R9_VERDICT.md` /
  `R9_VERDICT.json`, both ending in the same nonce line,

and the lane's stdout at
`…/lane_runs/CNV-PIPD-LS-SP-20261015-R9/VERIFY_SECURITY/attempt-1-20261016T044148Z/attempt-1188-1792125708-1-stdout.txt`
line 4 shows an `item.completed`/`agent_message` carrier whose `text` DOES contain
`R9V-CHECKER-NONCE-5c1d84` — the nonce was emitted on every surface the gate could read and on a
surface it did not read. The manifest record of the known defect is
`…-R9/SELF_EVOLUTION_R9.md` RS-09 / IT-07 / EV-08 (same gate gap, gate = a DONE/nonce file read).

### 2.2 Exactly which surfaces it reads (measured)

1. `stdout` bytes (`out_b`) — the ONLY surface. Two sub-checks: `nonce_bytes in out_b` (raw) and
   `nonce_in_agent_message(out_b, args.nonce)` (a `item.completed`/`agent_message` carrier must be
   the JSON-string `text` that contains the nonce).
2. `stderr` — read, persisted, but NOT searched for the nonce.
3. The lane ARTIFACT ROOT (e.g. `…/R9_VERIFY/…`) — NOT read at all.

### 2.3 Exact place to change and the minimal repair (before/after)

Dispatcher change (single site) plus one wrapper-input change, kept strictly additive:
no meaning of `nonce_present` that was previously false should become true except when a FILE the
lane owns carries it.

**(a) dispatch_r6.py / dispatch_r9.py — pass the lane's artifact root (line 55-ish `--cwd`. use the
new `--nonce-artifact-root` flag; add it beside `--output-root`):**

```python
           "--output-root", LANE_RUNS,
           "--nonce-artifact-root", f"{HANDOVER}/R9_VERIFY",
           "--json-out", json_out,
```

(dispatch_r6.py's value is `f"{HANDOVER}/R6_DELIVERY"`-adjacent; concrete path is per-round; the
point is: one explicit path per lane turn, never inferred from the wrapper's own cwd.)

**(b) `hgk-lane-dispatch.py`, `run_candidate()`, immediately after line 1188
(`carrier_surrogate = carrier_surrogate_count()`), add the artifact-file read:

```python
    # EV-08 repair: when the stdout carrier misses, the lane may still have written a nonce/
    # DONE file at its artifact root (e.g. `R9V_DONE`, `*_DONE`, `*.nonce`). Read that surface
    # BEFORE declaring the arm nonce-absent; a nonce file proves an answering turn completed.
    nonce_artifact_files = []
    if not nonce_ok:
        art_root = getattr(args, "nonce_artifact_root", None)
        if art_root:
            for cand in Path(art_root).glob("**/*DONE*"):           # R9V_DONE / WS_R9B_DONE shape
                try:
                    if args.nonce in cand.read_text(encoding="utf-8", errors="strict"):
                        nonce_artifact_files.append(str(cand))
                except (OSError, UnicodeDecodeError):
                    continue
            for cand in Path(art_root).glob("**/*.nonce"):
                try:
                    if args.nonce in cand.read_text(encoding="utf-8", errors="strict"):
                        nonce_artifact_files.append(str(cand))
                except (OSError, UnicodeDecodeError):
                    continue
        nonce_ok = bool(nonce_artifact_files)
```

(the three lines `nonce_bytes/nonce_raw/nonce_ok` at 1179–1188 stay untouched; only the
`nonce_ok = …` assignment on line 1187 receives an additive fallback above it)

**(c) `hgk-lane-dispatch.py`, `attempt` dict construction at line 1263–1267 — record the
artifact-file evidence (additive, so the trail stays readable):**

```python
            "nonce_source": "item.completed/agent_message",
            "nonce_artifact_files": nonce_artifact_files,
```

**(d) `hgk-lane-dispatch.py`, receipt fields (line 2203–2205) — the fields that must CHANGE on the
receipt** (they must stop being null for a turn whose only nonce miss was the stdout carrier and
whose artifact root carries the file):

```python
        "used_rank": used["rank"] if used else None,
        "used_transport_model": used["transport_model"] if used else None,
        "used_seconds": used["seconds"] if used else None,
        …
        receipt["served_arm"] = f"{used['provider']}/{used['model']}"
```

For the measured R9 checker turn, after the repair they read (from the surviving attempt row,
attempts[0]): `used_rank = 1`, `used_transport_model = "openai-codex/gpt-6.1-sol"`,
`used_seconds = <measured turn age>`, `served_arm = "openai-codex/gpt-6.1-sol"`, `ok = true`,
`code = ""` (the ERR_NO_ARM_EMITTED_NONCE top-level code is NOT emitted; the frozen C1
classification in `failure_disposition` already states explicitly (lines 1043–1046) that the code
is the gate grade, never the attribution — so leaving `nonce_absent_arms` populated while
`used_rank` stays null would be a contradiction, and this repair resolves it by attribute; the
final code emitted instead is the no-op empty string).

### 2.4 What a TEST must assert

- A fixture attempt whose stdout contains NO `item.completed`/`agent_message` nonce carrier but
  whose `--nonce-artifact-root` contains a file (`*_DONE` or `*.nonce`) whose bytes equal the nonce
  → `nonce_present` must be `true`, `nonce_artifact_files` must name the file, and the receipt
  must carry non-null `used_rank` / `used_transport_model` / `used_seconds` / `served_arm`, plus
  `ok: true`.
- Negative controls (must still fail-closed, i.e. the repair is not a general relaxation):
  - `--nonce-artifact-root` unset or nonexistent directory → `nonce_present` stays `false`.
  - a `*_DONE` / `*.nonce` file that does NOT contain the exact nonce → `nonce_present` stays
    `false` (`nonce_artifact_files` stays `[]`), and `ERR_NO_ARM_EMITTED_NONCE` still emits with
    `nonce_absent_arms` listing the arm.
  - a file whose bytes carry a NON-UTF-8 surrogate escape of the nonce → the repair's strict
    `UnicodeDecodeError` skip keeps it `false` (no replace-manufactured U+FFFD ever satisfies a
    nonce; mirrors the H1 constraint already documented at dispatch lines 1172–1178).
- A receipt field-list assertion: `nonce_artifact_files` is the additive surface; `used_rank` /
  `served_arm` become non-null; `nonce_absent_arms` is absent from the top-level receipt in the
  pass case.

### 2.5 LOCAL fixture possible? YES.

No live lane, no relay, no network:

- Fixture: a temp scratch dir shaped as
  `tmp/artifacts/{R9V_DONE, R9V.nonce, decoy_DONE, decoy.nonce, no_nonce_file_dir}/…`,
  each carrying either the exact fixture nonce `R9V-CHECKER-NONCE-fixture` or a decoy/non-matching
  string; drive the patched `hgk-lane-dispatch.py`'s `run_candidate` on a crafted stdout blob
  (`no item.completed agent_message carrier at all`) plus the crafted artifact root; also run the
  unpatched function as the negative control and assert the different `nonce_present` outcome.
- Real-host pytest of the patched module can be added as
  `tests/test_nonce_artifact_surface.py` calling `run_candidate` with a stubbed `subprocess.run`
  that emits a canned stdout and a stubbed lanes artifact root; this is a pure filesystem +
  string-matching exercise and does not need the relay or a real arm.

---

## lane_runs/ current state (measured at 2026-10-16 13:0x +0800, read-only)

Files (top level, JSON + ndjson), size / mtime:

| file | bytes | mtime (+0800) | role / turn it now holds |
|---|---|---|---|
| EXECUTE_dispatch_receipt_attempt1.json | 7,701 | 2026-10-16 12:40:52.373 | EXECUTE turn 5 of 5 (writer, run_id 1972-1792124816, R9B narrow turn; `code=ERR_NO_ARM_EMITTED_NONCE`, `nonce_present=false`) |
| EXECUTE_dispatch_receipt_attempt1.json.attempts.ndjson | 13,415 | 2026-10-16 12:40:52.352 | 5 writer turns appended (see table above) |
| EXECUTE_dispatch_receipt_attempt2.json | 7,681 | 2026-10-15 21:44:43.261 | EXECUTE attempt-2 (TIMEOUT turn, 1 row) |
| EXECUTE_dispatch_receipt_attempt2.json.attempts.ndjson | 2,771 | 2026-10-15 21:44:43.239 | same |
| EXECUTE_dispatch_receipt_attempt3.json | 7,516 | 2026-10-15 21:53:57.119 | EXECUTE attempt-3 (writer turn 1 row) |
| EXECUTE_dispatch_receipt_attempt3.json.attempts.ndjson | 2,599 | 2026-10-15 21:53:57.116 | same |
| VERIFY_SECURITY_dispatch_receipt_attempt1.json | 7,413 | 2026-10-16 12:54:37.321 | VERIFY_SECURITY turn 3 of 3 (checker, run_id 1188-1792125708, R9 checker turn on openai-codex/gpt-6.1-sol; `code=ERR_NO_ARM_EMITTED_NONCE`, `nonce_present=false`) |
| VERIFY_SECURITY_dispatch_receipt_attempt1.json.attempts.ndjson | 8,112 | 2026-10-16 12:54:37.119 | 3 checker turns appended |
| VERIFY_SECURITY_dispatch_receipt_attempt2.json | 7,763 | 2026-10-15 23:16:29.722 | checker attempt-2 TIMEOUT + a 2026-10-15 18:13 row |
| VERIFY_SECURITY_dispatch_receipt_attempt2.json.attempts.ndjson | 5,521 | 2026-10-15 23:16:29.522 | same |
| VERIFY_SECURITY_dispatch_receipt_attempt3.json | 7,326 | 2026-10-15 23:34:30.183 | checker attempt-3 + a 2026-10-15 18:28 row |
| VERIFY_SECURITY_dispatch_receipt_attempt3.json.attempts.ndjson | 5,315 | 2026-10-15 23:34:30.014 | same |
| VERIFY_SECURITY_dispatch_receipt_attempt4.json | 7,526 | 2026-10-16 00:48:58.996 | checker attempt-4 (single row) |
| VERIFY_SECURITY_dispatch_receipt_attempt4.json.attempts.ndjson | 2,740 | 2026-10-16 00:48:58.830 | same |
| VERIFY_SECURITY_dispatch_receipt_attempt5.json | 701 | 2026-10-16 00:53:09.868 | checker attempt-5 — refusal-before-spawn record (`ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED`, NO attempts row) |
| CNV-PIPD-LS-SP-20261015-R6/ | dir | 2026-10-15 16:20:53.119 | lane attempt dirs (EXECUTE / VERIFY_SECURITY sub-trees) |
| CNV-PIPD-LS-SP-20261015-R9/ | dir | 2026-10-16 12:41:48.502 | lane attempt dirs (VERIFY_SECURITY sub-tree only) |

Per-turn attribution (from the `.attempts.ndjson` trails — the only complete history, and the
reason the ticket-path JSONs understate the turn count):

- EXECUTE `…attempt1.json` = 5 writer turns; only the 5th (run_id 1972-1792124816) is described by
  the on-disk JSON. Turns 1–4 survive ONLY as ndjson rows with no `code` field.
- VERIFY_SECURITY `…attempt1.json` = 3 checker turns; only the 3rd (run_id 1188-1792125708) is
  described by the on-disk JSON.
- VERIFY_SECURITY `…attempt2/3.json` = 2 turns each; only the newest of each pair survives at the
  ticket-path JSON.
- The R6/EXECUTE and R6/VERIFY_SECURITY attempt dirs each hold 7–9 per-turn subdirectories
  (`attempt-<n>-<utc-ts>/`), each self-contained via its own `attempt.marker.json` +
  `attempt-*-stdout.txt` / `attempt-*-stderr.txt`, which is why the LANE-side evidence base is
  recoverable even though the TICKET-side (round-side) receipts were overwritten.

---

## What I could NOT determine from source alone

- Whether the copy-into-round-root step of Defect 1 should also carry a stable extension for the
  `.attempts.ndjson` trail (the dispatcher derives that path internally from `--json-out`), i.e.
  whether `receipt_paths.json.snapshot_policy` should copy the trail too. Source alone cannot say
  if `.attempts.ndjson` is versioned; a round-pinned test would have to decide.
- The exact value (or absence) of `round_name`'s trimming at the wrapper for R6 vs R9 — the two
  wrappers already set `"--round", round_name` and the round string participates in the derived
  lane-side dir, so whether the per-turn files should ALSO name the round is a policy call I can
  only recommend (I recommended not, to keep `json_out` basename short), not decide from source.
- Whether `nonce_artifact_root` should be per-lane (EXECUTE's artifact root differs from
  VERIFY_SECURITY's, e.g. `WS_R9B_*_DONE` vs `R9V_DONE`) — the briefs hold the concrete roots;
  mapping each lane to its artifact root is DATA, not source, so the exact per-lane mapping must
  come from the round's briefs (I gave the concrete R9 checker root but not an EXECUTE one).
- Local-fixture |潜伏| risk for Defect 2: whether `*_DONE` vs the lane's own `attempt.marker.json`
  (which also carries the nonce `HGK_LANE_NONCE_OK`) should be in the glob inclusion set. Source
  cannot disambiguate; I excluded `attempt.marker.json` from the repair's glob on purpose because
  it is already read by the C1 phase — but a test must pin that decision.
