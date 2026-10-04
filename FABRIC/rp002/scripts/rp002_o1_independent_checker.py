# -*- coding: utf-8 -*-
"""RP-002 O1 — INDEPENDENT checker (fresh read-only re-derivation; maker != checker).

O1 qualification authority = EXTERNAL FROZEN META-ORACLE. This checker re-derives
the deterministic materialization facts; it does NOT self-promote the Oracle.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
ORACLE = FAB / "profiles" / "construction-acceptance-oracle"
O1 = FAB / "rp002" / "O1"

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. distribution files exist
for f in ("distribution.yaml", "SOUL.md", "config.yaml", "CHECKER_ISOLATION_RECIPE.md"):
    check(f"O1I_FILE_{f.replace('.', '_')}", (ORACLE / f).stat().st_size > 200, f)

# 2. schemas parse + required fields
receipt = json.loads((ORACLE / "schemas" / "oracle_receipt.schema.json").read_text(encoding="utf-8"))
check("O1I_RECEIPT_SCHEMA", receipt["$id"] == "RP002-ORACLE-RECEIPT/1" and "verdict" in receipt["properties"]
      and receipt["properties"]["verdict"]["enum"] == ["PASS", "PARTIAL", "FAIL", "TEMP_CLOSED"],
      receipt["$id"])
pack_schema = json.loads((ORACLE / "schemas" / "acceptance_pack.schema.json").read_text(encoding="utf-8"))
check("O1I_PACK_SCHEMA", pack_schema["$id"] == "RP002-ACCEPTANCE-PACK/1", pack_schema["$id"])

# 3. 10 acceptance packs present
packs = sorted(p.name for p in (ORACLE / "acceptance-packs").iterdir() if p.is_dir())
check("O1I_PACKS_10", packs == ["hermes-runtime", "kanban", "knowledge", "multi-profile-pipeline",
                                "oracle-meta", "profile", "shared-service", "skill", "sqs-financial-bridge", "stack"],
      str(packs))

# 4. validators + tests re-run green (fresh subprocess)
for v in ("oracle_preflight", "evidence_readback", "subject_binding"):
    p = subprocess.run([sys.executable, str(ORACLE / "validators" / f"{v}.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    check(f"O1I_VALIDATOR_{v}", p.returncode == 0 and "VALIDATOR_OK" in p.stdout, p.stdout[-60:])
for t in ("golden", "negative", "adversarial", "holdout"):
    p = subprocess.run([sys.executable, str(ORACLE / "tests" / t / f"test_{t}.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    check(f"O1I_TESTS_{t}", p.returncode == 0 and "TESTS_OK" in p.stdout, p.stdout[-60:])

# 5. self-promotion guard: receipt says promotion pending external; candidate cannot self-approve
ev = json.loads((O1 / "RP002_O1_EVIDENCE.json").read_text(encoding="utf-8"))
check("O1I_NO_SELF_PROMOTION",
      ev.get("internal_oracle_promotion_receipt") is None
      and ev["external_meta_qualification_required"]["status"].startswith("PENDING_EXTERNAL"),
      ev.get("external_meta_qualification_required", {}).get("status", "missing"))

# 6. KPACK + compiler binding digests present
binding = (ORACLE / "core" / "KPACK_BINDING.md").read_text(encoding="utf-8")
check("O1I_KPACK_BINDING", "kp_index_sha256" in binding and "prompt_compiler_sha256" in binding, "binding doc")

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_O1_INDEPENDENT_CHECKER", "oracle": "EXTERNAL_FROZEN_META_ORACLE",
       "verdict": verdict, "checks": results,
       "note": "Deterministic materialization verified. Oracle promotion receipt remains with the external Meta-Oracle."}
(O1 / "RP002_O1_INDEPENDENT_CHECKER.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
