# -*- coding: utf-8 -*-
"""FDA WorkOrder admission via typed SharedSpine API.
REQ-FDA-001 -> TS-FDA-001 -> WO-FDA-001 (writer=codex).
Idempotent: existing rows are detected and reported, not recreated.
"""
import json, sys
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
sys.path.insert(0, str(HGK / "src"))
from hg_kseos.spine import SharedSpine

sp = SharedSpine(HGK / "var" / "shared-spine" / "hg-kseos.db")

REQ = "REQ-FDA-001"; TS = "TS-FDA-001"; WO = "WO-FDA-001"
ACTOR = "fda-orchestrator"

def step(name, fn):
    try:
        r = fn()
        print(f"[{name}] OK -> {r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)[:200]}")
        return r
    except Exception as e:
        msg = str(e)
        if "UNIQUE" in msg or "IntegrityError" in msg or "exists" in msg.lower() or "ERR_STALE_VERSION" in msg or "already" in msg.lower():
            print(f"[{name}] ALREADY_EXISTS (idempotent continue): {msg[:120]}")
            return None
        print(f"[{name}] ERROR: {msg[:300]}")
        raise

# 1. requirement
step("register_requirement", lambda: sp.register_requirement(
    requirement_id=REQ,
    source_locator="attachments/fabric-desktop-automation_藍圖_v2026.08.13-r2.md",
    wording="Implement fabric-desktop-automation blueprint r2: FDA shared-infra team artifact, capability matrix, cua/ufo2 profiles, deterministic router + one-writer lease + idempotency, XQ PAPER fixture qualification, security/SoD negative suite, interop dispositions, single evidence MD for external acceptance.",
    acceptance_id="ACC-FDA-001",
    oracle="FABRIC_BLUEPRINT_R2 + current RP-002 machine truth",
    threshold="PROMPT_COMPILE_PASS + C0..C7 predicates per blueprint 6.8",
    negative_fixture="third heavy stack / second scheduler / schema fork / live write = FAIL",
    priority="P0",
    project_id="HGK-REFERENCE-PROJECT-002"))

# 2. freeze requirement (lease -> transition -> release)
tok = f"TK-{REQ}"
try:
    step("acquire_lease", lambda: sp.acquire_lease(REQ, ACTOR, tok, ttl_seconds=300))
except Exception as e:
    print("lease acquire note:", str(e)[:120])
step("transition_freeze", lambda: sp.transition_requirement(
    REQ, "FROZEN", actor=ACTOR, token=tok, expected_version=0,
    evidence_ref="EV-FDA-COMPILER", idempotency_key=f"FRZ-{REQ}"))
try:
    step("release_lease", lambda: sp.release_lease(REQ, ACTOR, tok))
except Exception as e:
    print("lease release note:", str(e)[:120])

# 3. taskspec (writable root = var/fda)
wt = HGK / "var" / "fda" / "wt-fda"
wt.mkdir(parents=True, exist_ok=True)
step("create_taskspec", lambda: sp.create_taskspec(
    taskspec_id=TS, requirement_id=REQ,
    objective="Materialize FDA team/profile/matrix/router/lease/idempotency artifacts under Fabric; qualify Cua/UFO2/XQ PAPER; freeze evidence MD.",
    owner=ACTOR, writable_root=wt,
    permissions={"write_scope": "worktree", "network": False},
    tests=["blueprint 6.7 FDA-T001..T041 applicable edges"],
    evidence_plan="raw receipts + independent checker + evidence MD"))

# 4. workorder (writer=codex)
try:
    import subprocess
    head = subprocess.run(["git", "-C", str(HGK), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
except Exception:
    head = "22e21f0340501caf4ff0dbd67663faf49f521b03"
step("create_workorder", lambda: sp.create_workorder(
    WO, TS, writer="codex", worktree=wt, base_head=head))

# readback
with sp.connect() as c:
    wo_row = c.execute("SELECT workorder_id, writer, state, rollback_pointer FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
    req_row = c.execute("SELECT requirement_id, state, version FROM requirements WHERE requirement_id=?", (REQ,)).fetchone()
    ev_row = c.execute("SELECT event_id, to_state FROM canonical_events WHERE idempotency_key=?", (f"FRZ-{REQ}",)).fetchone()
print("READBACK WO:", wo_row)
print("READBACK REQ:", req_row)
print("READBACK EVT:", ev_row)
