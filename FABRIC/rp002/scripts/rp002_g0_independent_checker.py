# -*- coding: utf-8 -*-
"""RP-002 G0 — INDEPENDENT checker (fresh read-only re-derivation; maker != checker)."""
import hashlib, json, os, sqlite3, subprocess, sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
G0 = FAB / "rp002" / "G0"
DB = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. Recompute denominator sha from raw bytes
den_jsonl = G0 / "RP002_INPUT_DENOMINATOR.jsonl"
den_sha = sha(den_jsonl)
check("IND_DEN_SHA_REMATH", den_sha == (G0 / "RP002_INPUT_DENOMINATOR.sha256").read_text().strip(), den_sha)

# 2. Denominator rows are parseable JSON, unique by (root,path)
rows = [json.loads(l) for l in den_jsonl.read_text(encoding="utf-8").splitlines()]
check("IND_DEN_ROWS_PARSE", len(rows) == 30372, len(rows))
check("IND_DEN_UNIQUE", len({(r["root"], r["path"]) for r in rows}) == len(rows), "unique (root,path)")

# 3. Freeze record: parse + sha match + internal oracle null
freeze = json.loads((G0 / "RP002_G0_FREEZE.json").read_text(encoding="utf-8"))
check("IND_FREEZE_SHA", sha(G0 / "RP002_G0_FREEZE.json") == (G0 / "RP002_G0_FREEZE.sha256").read_text().strip(), "freeze sha")
check("IND_ORACLE_NULL", freeze["internal_oracle_candidate"]["distribution_commit"] is None, "internal oracle null pre-O1")

# 4. Git heads re-derived from disk
h = subprocess.run(["git", "-C", r"C:\Projects\Agent_Workspace\HG-KSEOS", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
check("IND_HGK_HEAD", h == freeze["current_identities"]["hgk_head"], h)
s = subprocess.run(["git", "-C", r"C:\Projects\Agent_Workspace\SQS-THC", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
check("IND_SQS_HEAD", s == freeze["current_identities"]["sqs_head"], s)

# 5. Oracle contract digests re-derived from source files
prompt = r"C:\Users\user\AppData\Local\hermes\attachments\RP-002_HGK_HERMES_UltraThin_Master_Construction_Acceptance_Prompt_r1_2026-08-11.md"
bp = r"C:\Projects\Agent_Workspace\Fabric\RP-002_DOC\RP-002_藍圖_Fabric-Governed_Profile-Distributed_Kanban-Coordinated_2026-08-11_r3.md"
check("IND_PROMPT_R1_DIGEST", sha(prompt) == "c3f34ca28a6bc8c8b7255c721173ff00e694366eb3b15891d15b3b97f5453c70", sha(prompt))
check("IND_BLUEPRINT_R3_DIGEST", sha(bp) == "6900e451e578bdcbb9b6e4fa5792277ef11a8389ae9b7fced94254d89d00f147", sha(bp))

# 6. Gate requirements present in spine (18 rows for project)
con = sqlite3.connect(DB)
n = con.execute("SELECT COUNT(*) FROM requirements WHERE project_id=? AND requirement_id LIKE 'REQ-RP2-%'", ("HGK-REFERENCE-PROJECT-002",)).fetchone()[0]
check("IND_SPINE_GATE_REQS", n == 18, f"REQ-RP2-* rows={n}")
con.close()

# 7. Machine-truth artifacts exist and are non-empty
for a in ["RP002_GATE_CATALOG.yaml", "RP002_EXECUTION_GRAPH.yaml", "FROZEN_ACCEPTANCE_ORACLE.yaml",
          "RP002_PROFILE_TEAM_MANIFEST.yaml", "RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml",
          "RP002_CHANGE_CLASS_ROUTER.yaml", "RP002_EXECUTION_BINDING.schema.json", "RP002_PROMOTION_TRANSACTION.yaml"]:
    p = FAB / "rp002" / a
    check(f"IND_ARTIFACT_{a.split('.')[0]}", p.exists() and p.stat().st_size > 50, str(p))

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_G0_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
       "verdict": verdict, "checks": results}
(G0 / "RP002_G0_INDEPENDENT_CHECKER.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
