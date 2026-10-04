# -*- coding: utf-8 -*-
"""RP-002 F1 — INDEPENDENT checker (fresh read-only; maker != checker)."""
import json, sqlite3, subprocess, sys
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
F1 = FAB / "rp002" / "F1"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

ev = json.loads((F1 / "RP002_F1_EVIDENCE.json").read_text(encoding="utf-8"))
check("F1I_MAKER_PASS", ev["verdict"] == "PASS" and all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# cutover flag + state in spine (fresh read)
check("F1I_CUTOVER_FLAG", (F1 / "SELF_HOSTING_CUTOVER").read_text().strip() == "true", "flag file")
con = sqlite3.connect(str(HGK / "var" / "shared-spine" / "hg-kseos.db"))
row = con.execute("SELECT state FROM project_lifecycles WHERE project_id='HGK-REFERENCE-PROJECT-002'").fetchone()
con.close()
check("F1I_SPINE_STATE", row and row[0] == "SELF_HOSTING_CUTOVER", str(row))

# binding validates + has real kanban task id
try:
    import jsonschema
    schema = json.loads((FAB / "rp002" / "RP002_EXECUTION_BINDING.schema.json").read_text(encoding="utf-8"))
    binding = json.loads((F1 / "RP002_F1_EXECUTION_BINDING.json").read_text(encoding="utf-8"))
    jsonschema.validate(binding, schema)
    check("F1I_BINDING", binding["kanban_task_id"].startswith("t_"), binding["kanban_task_id"])
except Exception as exc:  # noqa: BLE001
    check("F1I_BINDING", False, str(exc)[:100])

# workorder admitted in spine
con = sqlite3.connect(str(HGK / "var" / "shared-spine" / "hg-kseos.db"))
wo = con.execute("SELECT state FROM workorders WHERE workorder_id='WO-RP2-F1'").fetchone()
con.close()
check("F1I_WORKORDER", wo is not None and wo[0] in ("CREATED", "ADMITTED", "VERIFIED"), str(wo))

# break-glass contract present
bg = json.loads((F1 / "BREAK_GLASS_RECEIPT.schema.json").read_text(encoding="utf-8"))
check("F1I_BREAK_GLASS", "post_event_review" in bg["break_glass_receipt"], "break-glass schema")

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_F1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(F1 / "RP002_F1_INDEPENDENT_CHECKER.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
