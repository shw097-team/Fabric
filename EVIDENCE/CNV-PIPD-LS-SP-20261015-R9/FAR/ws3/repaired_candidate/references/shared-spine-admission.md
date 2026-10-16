# Shared Spine WorkOrder admission (typed API)

Verified against `src/hg_kseos/spine.py` + `src/hg_kseos/lifecycle.py` in HG-KSEOS
(2026-08-12). For a diagnostic/canary task, do NOT run the full `project start` lifecycle
(`admit_workorders` requires state PLAN_READY and auto-creates a full plan). Instead drive
the typed `SharedSpine` API directly — it emits canonical events + rollback pointers and
leaves RP-002 rows untouched.

## Sequence (all through `SharedSpine`)

```python
import json, sys
from pathlib import Path
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
sys.path.insert(0, str(HGK / "src"))
from hg_kseos.spine import SharedSpine

sp = SharedSpine(HGK / "var" / "shared-spine" / "hg-kseos.db")

REQ = "REQ-HGK-A2-DIAG-001"; TS = "TS-HGK-A2-DIAG-001"; WO = "WO-HGK-A2-DIAG-001"

# 1. register requirement (idempotent: UNIQUE/IntegrityError => already exists, continue)
sp.register_requirement(requirement_id=REQ, source_locator="task:<id>:intent",
    wording="...", acceptance_id=f"ACC-{REQ}", oracle="...", threshold="...",
    negative_fixture="...", priority="P0", project_id="HGK-REFERENCE-PROJECT-002")

# 2. freeze requirement: lease -> transition -> release (idempotency key prevents replay dup)
sp.acquire_lease(REQ, "a2-orchestrator", f"TK-{REQ}", ttl_seconds=300)
tr = sp.transition_requirement(REQ, "FROZEN", actor="a2-orchestrator", token=f"TK-{REQ}",
    expected_version=0, evidence_ref=f"EV-{REQ}", idempotency_key=f"FRZ-{REQ}")
sp.release_lease(REQ, "a2-orchestrator", f"TK-{REQ}")
# tr == {"event_id": "EVT-...", "resulting_version": 1, "to_state": "FROZEN"}

# 3. taskspec (state DRAFT; requirement must be FROZEN)
sp.create_taskspec(taskspec_id=TS, requirement_id=REQ, objective="...",
    owner="a2-orchestrator", writable_root=HGK/"var"/"a2"/"wt-a2-diag",
    permissions={"write_scope": "worktree", "network": False},
    tests=["A2 acceptance contract §17"], evidence_plan="raw + independent evidence")

# 4. workorder (writer=codex; taskspec DRAFT -> ADMITTED; requires non-empty writer+base_head)
sp.create_workorder(WO, TS, writer="codex",
    worktree=HGK/"var"/"a2"/"wt-a2-diag", base_head="<current HGK HEAD sha>")
```

## Readback (prove it landed)

```python
with sp.connect() as c:
    wo = c.execute("SELECT workorder_id,writer,state,rollback_pointer FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
    ev = c.execute("SELECT event_id,to_state FROM canonical_events WHERE idempotency_key=?", (f"FRZ-{REQ}",)).fetchone()
```

Expect: workorder `state=CREATED`, `writer=codex`, `rollback_pointer=RB-WO-...`,
requirement `FROZEN v1`, canonical event `EVT-...` to_state FROZEN.

## Result recording (later, when the WorkOrder completes)

`record_workorder_result(wo_id, writer, checker, verdict, evidence_refs)` — requires
`writer != checker` (ERR_WORKORDER_SELF_REVIEW), verdict in {PASS,FAIL}, non-empty
evidence_refs, and workorder state CREATED. **The `writer` arg MUST equal the
workorder's stored writer from `create_workorder`** — passing a different actor name
(e.g. a role alias like `fda-upgrade-orchestrator` when the WO was created with
`hermes-orchestrator`) raises `ERR_WORKORDER_RESULT_STATE` even when the state is
CREATED (verified 2026-08-14: record failed once with a role alias, succeeded with the
exact stored writer). Register evidence first via
`register_evidence(evidence_id, kind, locator, sha256, producer, checker)` (sha must be
64 hex chars). Rollback: `rollback_workorder(wo_id, evidence_ref)` (VERIFIED -> ROLLED_BACK,
inserts rollback_records row).

## Notes

- DB path comes from `config/project.json` -> `canonical_database` (`var/shared-spine/hg-kseos.db`).
- `transition_requirement` checks lease + expected_version; a re-run with version 0 after a
  successful freeze raises ERR_STALE_VERSION — treat as "already done".
- `writable_root.resolve()` is stored — create the dir first (`mkdir(parents=True, exist_ok=True)`).
- SQLite3 is bundled with the HGK repo venv python (3.12.13); do NOT rely on `sqlite3` from
  a system python in the same script unless the repo venv is the interpreter.
- `SharedSpine(db)` REQUIRES a `pathlib.Path`, not a `str` — a bare string raises
  `AttributeError: 'str' object has no attribute 'resolve'` at construction (the ctor calls
  `database.resolve()`). Wrap with `Path(...)`, and run it under the repo venv python.
- Row reads: `sp.connect()` yields `sqlite3.Row` objects that print as
  `<sqlite3.Row object at 0x...>`. Coerce with `dict(row)` (or index positionally) before
  comparing/printing — a raw row silently reads as "no data" in your log.
- **Closure rows may not live in the spine at all.** The SWOF W2 normative closure is delivered
  as an evidence-tree **projection artifact** (`R*_W2_NORMATIVE_CLOSURE_PROJECTION.json` bound
  into the evidence commit), NOT as live `requirements`/`workorders`/`acceptances`/`checkpoints`
  rows — grepping the db for `REQ-HGK-SWOF-W2*` / `CK-W2-*` returns nothing. Reproduce the
  closure from the projection JSON + the recomputable `checkpoints.source_digest`, don't hunt
  the db for rows that were never written there.
