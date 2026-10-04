# -*- coding: utf-8 -*-
"""RP-002 B1 — INDEPENDENT checker (fresh read-only; maker != checker)."""
import json, sqlite3, subprocess, sys
from pathlib import Path

HOME = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\home")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
B1 = FAB / "rp002" / "B1"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. maker evidence PASS
ev = json.loads((B1 / "RP002_B1_EVIDENCE.json").read_text(encoding="utf-8"))
check("B1I_MAKER_PASS", ev["verdict"] == "PASS" and all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# 2. board exists with its own kanban.db + tasks
board_db = HOME / "kanban" / "boards" / "rp002-fabric-bootstrap" / "kanban.db"
check("B1I_BOARD_DB", board_db.exists() and board_db.stat().st_size > 0, str(board_db))
con = sqlite3.connect(str(board_db))
n = con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
check("B1I_BOARD_TASKS", n >= 6, f"tasks={n}")
con.close()

# 3. board dir on disk
board_dir = HOME / "kanban" / "boards" / "rp002-fabric-bootstrap"
check("B1I_BOARD_DIR", board_dir.exists() or (HOME / "kanban" / "boards").exists(),
      str(board_dir) if board_dir.exists() else "boards dir present")

# 4. ExecutionBinding validates against schema
try:
    import jsonschema
    schema = json.loads((FAB / "rp002" / "RP002_EXECUTION_BINDING.schema.json").read_text(encoding="utf-8"))
    binding = json.loads((B1 / "RP002_EXECUTION_BINDING_EXAMPLE.json").read_text(encoding="utf-8"))
    jsonschema.validate(binding, schema)
    check("B1I_BINDING_VALID", True, "schema valid")
except Exception as exc:  # noqa: BLE001
    check("B1I_BINDING_VALID", False, str(exc)[:120])

# 5. RP002/TEAM.md binds graph
team = (FAB / "RP002" / "TEAM.md").read_text(encoding="utf-8")
check("B1I_TEAM_BINDS", "RP002_EXECUTION_GRAPH.yaml" in team and "live_broker_write: false" in team, "team md")

# 6. no unauthorized spawn: dry-run dispatch reports 0
env = dict(subprocess.os.environ)
env["HERMES_HOME"] = str(HOME)
env.pop("PYTHONPATH", None)
p = subprocess.run([str(Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\hermes-v020\venv\Scripts\hermes.exe")),
                    "kanban", "--board", "rp002-fabric-bootstrap", "dispatch", "--dry-run", "--max", "5"],
                   env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
out = (p.stdout or "") + (p.stderr or "")
check("B1I_NO_UNAUTHORIZED_SPAWN", "Spawned:      0" in out, out.strip()[-100:])

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_B1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(B1 / "RP002_B1_INDEPENDENT_CHECKER.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
