# -*- coding: utf-8 -*-
"""RP-002 D1 — INDEPENDENT checker: fresh read-only spine re-derivation (maker != checker)."""
import hashlib, json, sqlite3, sys
from pathlib import Path

DB = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db"
D1 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\D1")
PROJECT = "HGK-REFERENCE-PROJECT-002"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 1. 18 requirements FROZEN
frozen = con.execute("SELECT COUNT(*) FROM requirements WHERE project_id=? AND state='FROZEN' AND requirement_id LIKE 'REQ-RP2-%'", (PROJECT,)).fetchone()[0]
check("D1I_FROZEN_18", frozen == 18, f"frozen={frozen}")

# 2. every REQ-RP2-* has a taskspec (no orphans)
orphan_req = con.execute(
    """SELECT COUNT(*) FROM requirements r WHERE r.project_id=? AND r.requirement_id LIKE 'REQ-RP2-%'
       AND NOT EXISTS (SELECT 1 FROM taskspecs t WHERE t.requirement_id=r.requirement_id)""",
    (PROJECT,)).fetchone()[0]
check("D1I_NO_REQ_ORPHAN", orphan_req == 0, f"req_orphan={orphan_req}")

# 3. every taskspec has a workorder
orphan_ts = con.execute(
    """SELECT COUNT(*) FROM taskspecs t WHERE t.taskspec_id LIKE 'TS-RP2-%'
       AND NOT EXISTS (SELECT 1 FROM workorders w WHERE w.taskspec_id=t.taskspec_id)""").fetchone()[0]
check("D1I_NO_TASKSPEC_ORPHAN", orphan_ts == 0, f"taskspec_orphan={orphan_ts}")

# 4. workorders have rollback pointers + base_head
bad_wo = con.execute(
    "SELECT COUNT(*) FROM workorders WHERE workorder_id LIKE 'WO-RP2-%' AND (rollback_pointer IS NULL OR base_head IS NULL OR base_head='')").fetchone()[0]
check("D1I_WO_ROLLBACK_BASEHEAD", bad_wo == 0, f"bad_wo={bad_wo}")

# 5. evidence refs carry real sha (64 hex, not zero-padded)
bad_ev = con.execute(
    "SELECT COUNT(*) FROM evidence_refs WHERE evidence_id LIKE 'EVD1-%' AND (sha256='0'*64 OR length(sha256)!=64)").fetchone()[0]
check("D1I_EVIDENCE_REAL_SHA", bad_ev == 0, f"bad_ev={bad_ev}")

# 6. evidence sha matches on-disk design contract digest
ev = con.execute("SELECT sha256 FROM evidence_refs WHERE evidence_id LIKE 'EVD1-%' LIMIT 1").fetchone()
design_sha = hashlib.sha256((D1 / "RP002_D1_DESIGN_CONTRACT.md").read_bytes()).hexdigest()
check("D1I_EVIDENCE_BINDS_DESIGN", ev is not None and ev["sha256"] == design_sha, f"{ev['sha256'][:16]} vs {design_sha[:16]}")

# 7. design contract + ledger exist and parse
check("D1I_DESIGN_DOC", (D1 / "RP002_D1_DESIGN_CONTRACT.md").stat().st_size > 2000, "design doc present")
ledger = (D1 / "RP002_D1_CONTRACT_LEDGER.tsv").read_text(encoding="utf-8").splitlines()
check("D1I_LEDGER_18", len(ledger) - 1 == 18, f"ledger rows={len(ledger)-1}")

# 8. requirements transition history has FROZEN events with idempotency
evt = con.execute("SELECT COUNT(*) FROM canonical_events WHERE entity_type='requirement' AND to_state='FROZEN' AND idempotency_key LIKE 'd1-freeze-%'").fetchone()[0]
check("D1I_FREEZE_EVENTS", evt == 18, f"freeze events={evt}")
con.close()

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_D1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(D1 / "RP002_D1_INDEPENDENT_CHECKER.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
