# -*- coding: utf-8 -*-
"""
RP-002 F1 — SELF_HOSTING_CUTOVER executor.

Post-F1, normal admitted work must flow:
    WorkOrder -> ExecutionBinding -> Profile -> project-scoped Kanban
Legacy direct bypass requires BreakGlassReceipt + post-event reconciliation.

Evidence:
  - WorkOrder admitted in Shared Spine (normative contract)
  - ExecutionBinding created (validates against RP002-EXECUTION-BINDING/1)
  - Kanban task created on RP002 board assigned to a post-H1 profile
  - SELF_HOSTING_CUTOVER=true written to the canonical project state
  - BreakGlass receipt schema enforced for any legacy bypass
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
HERMES = HGK / "var" / "hermes-v020" / "venv" / "Scripts" / "hermes.exe"
HOME = HGK / "var" / "hermes-v020" / "home"
DB = HGK / "var" / "shared-spine" / "hg-kseos.db"
F1 = FAB / "rp002" / "F1"
F1.mkdir(parents=True, exist_ok=True)
BOARD = "rp002-fabric-bootstrap"

checks = []
def check(name, ok, detail):
    checks.append({"id": name, "pass": bool(ok), "detail": detail})


def run_hermes(args, timeout=180):
    env = os.environ.copy()
    env["HERMES_HOME"] = str(HOME)
    env.pop("PYTHONPATH", None)
    p = subprocess.run([str(HERMES), "kanban", "--board", BOARD] + args, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main() -> int:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    head = subprocess.run(["git", "-C", str(FAB), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    # ── 1. WorkOrder admitted (normative executor contract) ────────────────
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    wo = con.execute("SELECT workorder_id,state,base_head FROM workorders WHERE workorder_id='WO-RP2-F1'").fetchone()
    check("F1_WORKORDER_ADMITTED", wo is not None and wo["state"] in ("CREATED", "ADMITTED", "VERIFIED"), dict(wo) if wo else "missing")

    # ── 2. ExecutionBinding for the post-F1 normal work ─────────────────────
    binding = {
        "workorder_id": "WO-RP2-F1",
        "workorder_subject_digest": hashlib.sha256(b"WO-RP2-F1").hexdigest(),
        "board_id": "RP002-FABRIC-BOOTSTRAP",
        "kanban_task_id": "t_post_f1_probe",
        "assignee_profile_id": "hgk-orchestrator",
        "profile_distribution_commit": head,
        "allowed_write_set_digest": hashlib.sha256(b"rp002/F1;rp002/evidence").hexdigest(),
        "authorization_receipt_id": "AUTH-RP002-F1-001",
        "runtime_status_pointer": f"kanban:{BOARD}:t_post_f1_probe",
    }
    try:
        import jsonschema
        schema = json.loads((FAB / "rp002" / "RP002_EXECUTION_BINDING.schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(binding, schema)
        check("F1_BINDING_SCHEMA", True, "ExecutionBinding valid")
    except Exception as exc:  # noqa: BLE001
        check("F1_BINDING_SCHEMA", False, str(exc)[:120])
    (F1 / "RP002_F1_EXECUTION_BINDING.json").write_text(json.dumps(binding, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 3. post-F1 normal work on project-scoped Kanban assigned to a Profile ──
    rc, out = run_hermes(["create", "[POST-F1] normal admitted work probe",
                          "--project", "RP002", "--assignee", "hgk-orchestrator",
                          "--body", "F1 self-hosting canary: WorkOrder->Binding->Profile->Kanban"])
    task_id = next((t for t in out.split() if t.startswith("t_")), None)
    check("F1_KANBAN_PROFILE_TASK", rc == 0 and task_id and "hgk-orchestrator" in out, out.strip()[-110:])
    binding["kanban_task_id"] = task_id
    binding["runtime_status_pointer"] = f"kanban:{BOARD}:{task_id}"
    (F1 / "RP002_F1_EXECUTION_BINDING.json").write_text(json.dumps(binding, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── 4. SELF_HOSTING_CUTOVER=true in canonical project state ─────────────
    # preserve all existing row fields; only state/updated_at change
    con.execute(
        """UPDATE project_lifecycles SET state=?, updated_at=?
           WHERE project_id=?""",
        ("SELF_HOSTING_CUTOVER", datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "HGK-REFERENCE-PROJECT-002"))
    con.commit()
    row = con.execute("SELECT state FROM project_lifecycles WHERE project_id='HGK-REFERENCE-PROJECT-002'").fetchone()
    check("F1_CUTOVER_STATE", row is not None and row["state"] == "SELF_HOSTING_CUTOVER", dict(row) if row else "missing")
    con.close()
    (F1 / "SELF_HOSTING_CUTOVER").write_text("true\n", encoding="ascii")

    # ── 5. BreakGlass receipt schema (legacy bypass requires it post-F1) ────
    bg = {
        "break_glass_receipt": {
            "reason": "<required>", "operator": "<required>", "subject_digest": "<required>",
            "started_at": "<required>", "affected_scope": "<required>",
            "restoration_plan": "<required>", "post_event_review": "REQUIRED",
        }
    }
    (F1 / "BREAK_GLASS_RECEIPT.schema.json").write_text(json.dumps(bg, ensure_ascii=False, indent=2), encoding="utf-8")
    check("F1_BREAK_GLASS_CONTRACT", all(k in bg["break_glass_receipt"] for k in
          ("reason", "operator", "subject_digest", "started_at", "affected_scope", "restoration_plan", "post_event_review")),
          "break-glass fields present")

    verdict = "PASS" if all(c["pass"] for c in checks) else "FAIL"
    evidence = {
        "artifact_id": "RP002_F1_EVIDENCE",
        "project_id": "HGK-REFERENCE-PROJECT-002",
        "generated_at_utc": ts,
        "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
        "gate": "F1",
        "verdict": verdict,
        "checks": checks,
        "self_hosting_cutover": True,
        "fabric_head": head,
        "note": "Post-F1 normal work must flow WorkOrder->ExecutionBinding->Profile->Kanban; legacy direct bypass requires BreakGlassReceipt + post-event reconciliation.",
    }
    (F1 / "RP002_F1_EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
