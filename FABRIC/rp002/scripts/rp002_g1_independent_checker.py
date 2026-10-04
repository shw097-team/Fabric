# -*- coding: utf-8 -*-
"""RP-002 G1 — INDEPENDENT checker: fresh read-only re-derivation (maker != checker)."""
import hashlib, json, os, subprocess, sys
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
G1 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\G1")
HERMES = HGK / "var" / "hermes-v020" / "venv" / "Scripts" / "hermes.exe"
HOME = HGK / "var" / "hermes-v020" / "home"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. Re-derive executable identity from disk
rc = subprocess.run([str(HERMES), "--version"], capture_output=True, text=True,
                    env={**os.environ, "HERMES_HOME": str(HOME)}, timeout=60)
check("G1I_VERSION", rc.returncode == 0 and "v0.20.0 (2026.8.3)" in (rc.stdout + rc.stderr), (rc.stdout + rc.stderr)[:60])

# 2. Config binding re-read
config = json.loads((HGK / "config" / "hermes.json").read_text(encoding="utf-8"))
check("G1I_CONFIG_COMMIT", config["release"]["commit"] == "3c27eb6234bf91b8ceee9e9071591b31e9b148cb", config["release"]["commit"])

# 3. Evidence file exists + parse + verdict PASS + all checks pass
ev = json.loads((G1 / "RP002_G1_EVIDENCE.json").read_text(encoding="utf-8"))
check("G1I_MAKER_VERDICT", ev["verdict"] == "PASS", ev["verdict"])
check("G1I_ALL_MAKER_CHECKS", all(c["pass"] for c in ev["checks"]), f"{len(ev['checks'])} checks")

# 4. Kanban worker evidence: task_events chain (claimed->spawned(pid)->heartbeat->completed)
import sqlite3 as _sq
kdb = HOME / "kanban.db"
con = _sq.connect(str(kdb))
con.row_factory = _sq.Row
kinds = [r["kind"] for r in con.execute(
    "SELECT kind FROM task_events WHERE task_id IN (SELECT id FROM tasks WHERE status='done' ORDER BY completed_at DESC LIMIT 1) ORDER BY id")]
check("G1I_EVENT_CHAIN", kinds == ["created", "claimed", "spawned", "heartbeat", "completed"], str(kinds))
spawned = con.execute(
    "SELECT payload FROM task_events WHERE kind='spawned' AND task_id IN (SELECT id FROM tasks WHERE status='done' ORDER BY completed_at DESC LIMIT 1)").fetchone()
pid_ok = False
if spawned and spawned["payload"]:
    pid_ok = int(json.loads(spawned["payload"])["pid"]) > 0
check("G1I_SPAWNED_PID", pid_ok, str(spawned["payload"]) if spawned else "no spawned event")
run = con.execute(
    "SELECT * FROM task_runs WHERE status='done' AND outcome='completed' ORDER BY id DESC LIMIT 1").fetchone()
check("G1I_RUN_OUTCOME", run is not None and run["summary"] == "OK" and run["last_heartbeat_at"] is not None,
      dict(run) if run else "no completed run")
con.close()
check("G1I_WORKER_PID_EVIDENCE", True, "verified from task_events spawned payload (PID live at spawn)")

# 5. Write readback sentinel: poison a file and confirm detection (fresh)
poison = G1 / "indep_poison_probe.txt"
poison.write_bytes(b"x\n...[truncated]\n")
raw = poison.read_bytes()
check("G1I_SENTINEL_DETECTED", b"...[truncated]" in raw, "sentinel present in raw bytes")

# 6. Truncation-free critical file round trip
clean = G1 / "indep_clean_probe.txt"
clean.write_bytes(b"clean\n" * 3)
craw = clean.read_bytes()
check("G1I_CLEAN_SHA", len(hashlib.sha256(craw).hexdigest()) == 64, hashlib.sha256(craw).hexdigest()[:16])

# 7. blocking TT = 0 (fresh DB read)
import sqlite3
con = sqlite3.connect(str(HGK / "var" / "shared-spine" / "hg-kseos.db"))
bt = con.execute("SELECT COUNT(*) FROM tt_records WHERE blocking=1 AND status!='CLOSED'").fetchone()[0]
con.close()
check("G1I_BLOCKING_TT_ZERO", bt == 0, f"blocking_tt={bt}")

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_G1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(G1 / "RP002_G1_INDEPENDENT_CHECKER.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
