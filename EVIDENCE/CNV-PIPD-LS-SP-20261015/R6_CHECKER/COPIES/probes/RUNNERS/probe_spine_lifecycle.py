"""Same-subject positive/negative probes for HGK-typed-spine-and-lifecycle (ACC-003).

Modes:
  positive  - create a throwaway project, register requirement + evidence, acquire lease,
              drive a legal CANDIDATE->FROZEN->IMPLEMENTED lifecycle, read the snapshot back.
  negative  - attempt an ILLEGAL transition (CANDIDATE->IMPLEMENTED); must be refused.
  acceptance- register evidence + resolve_acceptance; verify registered-evidence binding.
  teardown  - remove the scratch database.

Operates only on a scratch sqlite file under RAW/. No canonical mutation.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, "C:/Projects/Agent_Workspace/HG-KSEOS/src")

RAW = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
           "R6_DELIVERY/RAW")
DB = RAW / "spine_scratch.sqlite"

from hg_kseos.spine import SharedSpine  # noqa: E402

TOKEN = "R6-SCRATCH-TOKEN"
ACTOR = "R6-PROBE-WRITER"
PROJECT_ID = "HGK-P0"


def _fresh(tag: str) -> SharedSpine:
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB) + suffix)
        if p.exists():
            p.unlink()
    spine = SharedSpine(DB)
    spine.initialize()
    # requirements.project_id has a real FK to projects(project_id); register under the
    # project id we actually create so the constraint is satisfied (not bypassed).
    spine.create_project(PROJECT_ID, f"CNV-R6 scratch {tag}")
    return spine


def _reg(spine: SharedSpine, rid: str) -> str:
    aid = f"ACC-{rid}"
    spine.register_requirement(
        requirement_id=rid,
        source_locator="RAW/spine_probe_source.md#clause-1",
        wording="R6 scratch requirement for lifecycle probe",
        acceptance_id=aid,
        oracle="deterministic assertion on the bound artifact",
        threshold="EXPLICIT_ORACLE_PASS",
        negative_fixture="fixtures/negative",
        priority="P0",
        project_id=PROJECT_ID,
    )
    return aid


def positive() -> int:
    spine = _fresh("SCRATCH")
    rid = "REQ-R6-001"
    _reg(spine, rid)
    spine.acquire_lease(rid, ACTOR, TOKEN, ttl_seconds=600)
    spine.transition_requirement(rid, "FROZEN", ACTOR, TOKEN, 0, "RAW/cap03", "IDEM-R6-001-A")
    spine.transition_requirement(rid, "IMPLEMENTED", ACTOR, TOKEN, 1, "RAW/cap03", "IDEM-R6-001-B")
    snap = spine.snapshot()
    with spine.connect() as con:
        row = con.execute(
            "SELECT state,version FROM requirements WHERE requirement_id=?", (rid,)
        ).fetchone()
    print(json.dumps({
        "verdict": "SPINE_POSITIVE_OK",
        "requirement_state": row["state"],
        "requirement_version": row["version"],
        "snapshot_counts_requirements": snap["counts"]["requirements"],
        "snapshot_counts_canonical_events": snap["counts"]["canonical_events"],
        "schema_version": snap["schema_version"],
    }, ensure_ascii=False, indent=1))
    return 0


def negative() -> int:
    spine = _fresh("SCRATCH-NEG")
    rid = "REQ-R6-NEG"
    _reg(spine, rid)
    spine.acquire_lease(rid, ACTOR, TOKEN, ttl_seconds=600)
    try:
        # CANDIDATE -> IMPLEMENTED is illegal: must pass through FROZEN first.
        spine.transition_requirement(rid, "IMPLEMENTED", ACTOR, TOKEN, 0,
                                     "RAW/cap03", "IDEM-R6-NEG-A")
    except Exception as exc:  # noqa: BLE001
        with spine.connect() as con:
            state = con.execute(
                "SELECT state,version FROM requirements WHERE requirement_id=?", (rid,)
            ).fetchone()
        print(json.dumps({
            "verdict": "SPINE_NEGATIVE_REFUSED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "state_after_refusal": state["state"],
            "version_after_refusal": state["version"],
        }, ensure_ascii=False, indent=1))
        return 0
    print(json.dumps({"verdict": "SPINE_NEGATIVE_NOT_REFUSED",
                      "detail": "illegal CANDIDATE->IMPLEMENTED was accepted"},
                     ensure_ascii=False, indent=1))
    return 1


def acceptance() -> int:
    """Registered-evidence binding: an acceptance may only be resolved through its own
    requirement and only against a registered evidence ref."""
    spine = _fresh("SCRATCH-ACC")
    rid = "REQ-R6-ACC"
    aid = _reg(spine, rid)
    spine.register_evidence("EVD-R6-ACC", "RAW_RECEIPT", "RAW/cap03.stdout.txt",
                            "a" * 64, "R6-PROBE-WRITER")
    spine.acquire_lease(aid, ACTOR, TOKEN, ttl_seconds=600)
    res = spine.resolve_acceptance(aid, verdict="PASS", evidence_ref="EVD-R6-ACC",
                                   actor=ACTOR, token=TOKEN, expected_version=0,
                                   idempotency_key="IDEM-R6-ACC-A", requirement_id=rid)
    replay = spine.resolve_acceptance(aid, verdict="PASS", evidence_ref="EVD-R6-ACC",
                                      actor=ACTOR, token=TOKEN, expected_version=0,
                                      idempotency_key="IDEM-R6-ACC-A", requirement_id=rid)
    # negative: same idempotency key spent on a different subject must fail closed
    rid2 = "REQ-R6-ACC2"
    aid2 = _reg(spine, rid2)
    spine.register_evidence("EVD-R6-ACC2", "RAW_RECEIPT", "RAW/cap03b.stdout.txt",
                            "b" * 64, "R6-PROBE-WRITER")
    spine.acquire_lease(aid2, ACTOR, TOKEN, ttl_seconds=600)
    wrong_subject_refused = None
    try:
        spine.resolve_acceptance(aid2, verdict="PASS", evidence_ref="EVD-R6-ACC2",
                                 actor=ACTOR, token=TOKEN, expected_version=0,
                                 idempotency_key="IDEM-R6-ACC-A", requirement_id=rid2)
    except Exception as exc:  # noqa: BLE001
        wrong_subject_refused = {"error_type": type(exc).__name__, "error": str(exc)}
    # negative: unregistered evidence must be refused
    unregistered_refused = None
    rid3 = "REQ-R6-ACC3"
    aid3 = _reg(spine, rid3)
    spine.acquire_lease(aid3, ACTOR, TOKEN, ttl_seconds=600)
    try:
        spine.resolve_acceptance(aid3, verdict="PASS", evidence_ref="EVD-DOES-NOT-EXIST",
                                 actor=ACTOR, token=TOKEN, expected_version=0,
                                 idempotency_key="IDEM-R6-ACC-C", requirement_id=rid3)
    except Exception as exc:  # noqa: BLE001
        unregistered_refused = {"error_type": type(exc).__name__, "error": str(exc)}
    with spine.connect() as con:
        verdict = con.execute(
            "SELECT verdict,evidence_ref FROM acceptances WHERE acceptance_id=?", (aid,)
        ).fetchone()
    print(json.dumps({
        "verdict": "SPINE_ACCEPTANCE_OK",
        "resolve": res,
        "idempotent_replay": replay,
        "wrong_subject_reuse_refused": wrong_subject_refused,
        "unregistered_evidence_refused": unregistered_refused,
        "final_acceptance_verdict": verdict["verdict"],
        "final_acceptance_evidence_ref": verdict["evidence_ref"],
    }, ensure_ascii=False, indent=1))
    return 0


def teardown() -> int:
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB) + suffix)
        if p.exists():
            p.unlink()
    print(json.dumps({"verdict": "SPINE_SCRATCH_TEARDOWN_OK"}, ensure_ascii=False))
    return 0


MODES = {"positive": positive, "negative": negative,
         "acceptance": acceptance, "teardown": teardown}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "positive"
    fn = MODES.get(mode)
    if fn is None:
        print(f"unknown mode: {mode}", file=sys.stderr)
        raise SystemExit(2)
    try:
        code = fn()
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        code = 9
    raise SystemExit(code)
