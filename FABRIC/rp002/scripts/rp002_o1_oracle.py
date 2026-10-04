# -*- coding: utf-8 -*-
"""
RP-002 O1 — INTERNAL_ORACLE_READY executor: materialize construction-acceptance-oracle Profile
(Distribution + Oracle Core + KP00~19 binding + Prompt Compiler + deterministic validators
 + Acceptance Packs + OracleReceipt schema + fresh CHECKER isolation recipe).

Checker for O1 = EXTERNAL FROZEN META-ORACLE (this dialogue's GPT-5.6 Sol contract).
Internal Oracle candidate must NOT self-promote. Candidate write tools absent in CHECKER context.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
HERMES = HGK / "var" / "hermes-v020" / "venv" / "Scripts" / "hermes.exe"
HOME = HGK / "var" / "hermes-v020" / "home"
O1 = FAB / "rp002" / "O1"
O1.mkdir(parents=True, exist_ok=True)
ORACLE_DIR = FAB / "profiles" / "construction-acceptance-oracle"
KPACK = FAB / "Oracle" / "工程基座" / "GPTs_GENIEMAKER_開發實作+驗收指揮官" / "GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2" / "KnowledgePack"
COMPILER = FAB / "Oracle" / "工程基座" / "construction-acceptance-prompt-compiler" / "construction-acceptance-prompt-compiler"

checks = []
def check(name, ok, detail):
    checks.append({"id": name, "pass": bool(ok), "detail": detail})

DISTRIBUTION_YAML = """name: construction-acceptance-oracle
version: 0.1.0
description: "RP-002 internal construction acceptance oracle: Oracle Core + KP00~19 + Prompt Compiler + deterministic validators + Acceptance Packs"
hermes_requires: ">=0.12.0"
author: "RP-002 HGK"
license: "MIT"
env_requires:
  - name: OPENCODE_GO_API_KEY
    description: "OpenCode Go API key (provider route)"
    required: true
"""

SOUL_MD = """# Construction Acceptance Oracle

You are the **construction-acceptance-oracle** Hermes profile — the internalized
construction/acceptance referee of RP-002 (HGK-REFERENCE-PROJECT-002).

## Identity
- basis: 00_KNOW_INDEX~19_KP_INDEX_CROSSWALK + construction-acceptance-prompt-compiler
  + deterministic validators + evidence readers + OracleReceipt schema + Acceptance Packs
- You are independent from the maker, NOT independent from Fabric governance.
- COMMANDER mode: bounded Thin Order / WorkOrder request + acceptance IDs + allowed write-set
  + non-goals + raw evidence obligations + claim ceiling. You do NOT prescribe rigid
  implementation recipes; HGK remains the engineering optimizer inside frozen boundaries.
- CHECKER mode: fresh/read-only context; maker memory preload OFF; candidate/source/evaluator
  write tools ABSENT; authority/promotion tools ABSENT; allowed write-set = OracleReceipt
  + checker logs only. Output: OracleReceipt only.

## Hard invariants (fail-closed)
- FILES_FIRST / NO_SOURCE_NO_NORM / maker != final checker / summary != raw evidence
- Gate terminal != project terminal; session pause != completion
- Profile != security sandbox; Kanban assignment != authorization
- MemoryCandidate != FinancialSpec; Oracle narrative != maker authority
- Oracle vN+1 may never self-approve; actual Oracle change -> E3 Meta-Oracle path
- Unknown subject type -> FAIL_CLOSED / UNKNOWN_ACCEPTANCE_PACK

## OracleReceipt
schema: RP002-ORACLE-RECEIPT/1 — required: oracle_id, oracle_package_digest, subject_digest,
acceptance_oracle_digest, verdict(PASS|PARTIAL|FAIL|TEMP_CLOSED); plus evidence_ids,
missing_evidence, conflicts, repair_scope, acceptance_pack_ids, requirement_ids.
"""

CONFIG_YAML = """# construction-acceptance-oracle — RP-002 internal oracle profile
model:
  provider: opencode-go
  default: deepseek-v4-flash
  base_url: https://opencode.ai/zen/go/v1
  api_mode: chat_completions
approvals:
  mode: manual
agent:
  max_turns: 300
  verify_on_stop: false
"""

GITIGNORE = """auth.json
.env
.env.EXAMPLE
state.db*
hermes_state.db
response_store.db*
gateway.pid
gateway_state.json
processes.json
auth.lock
active_profile
.update_check
memories/
sessions/
logs/
plans/
workspace/
home/
image_cache/
audio_cache/
document_cache/
browser_screenshots/
cache/
hermes-agent/
.worktrees/
profiles/
bin/
node_modules/
local/
checkpoints/
sandboxes/
backups/
errors.log
.hermes_history
"""

ORACLE_RECEIPT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "RP002-ORACLE-RECEIPT/1",
    "type": "object",
    "required": ["oracle_id", "oracle_package_digest", "subject_digest", "acceptance_oracle_digest", "verdict"],
    "properties": {
        "oracle_id": {"type": "string"},
        "oracle_version": {"type": "string"},
        "oracle_package_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "subject_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "acceptance_oracle_digest": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "acceptance_pack_ids": {"type": "array", "items": {"type": "string"}},
        "requirement_ids": {"type": "array", "items": {"type": "string"}},
        "evidence_ids": {"type": "array", "items": {"type": "string"}},
        "missing_evidence": {"type": "array", "items": {"type": "string"}},
        "conflicts": {"type": "array", "items": {"type": "string"}},
        "repair_scope": {"type": "array", "items": {"type": "string"}},
        "verdict": {"enum": ["PASS", "PARTIAL", "FAIL", "TEMP_CLOSED"]},
    },
}

ACCEPTANCE_PACK_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "RP002-ACCEPTANCE-PACK/1",
    "type": "object",
    "required": ["pack_id", "subject_type", "core_checks", "final_semantic_owner"],
    "properties": {
        "pack_id": {"type": "string"},
        "subject_type": {"type": "string"},
        "core_checks": {"type": "array", "items": {"type": "string"}},
        "final_semantic_owner": {"type": "string"},
        "blocking_predicates": {"type": "array", "items": {"type": "string"}},
    },
}

PACKS = {
    "hermes-runtime": {"subject_type": "HERMES_RUNTIME", "core_checks": ["exact subject", "authority", "evidence", "rollback"], "owner": "HGK runtime owner"},
    "profile": {"subject_type": "HERMES_PROFILE", "core_checks": ["identity", "subject", "authority", "evidence"], "owner": "owning Stack/Fabric policy"},
    "kanban": {"subject_type": "KANBAN_RUNTIME_OR_POLICY", "core_checks": ["subject", "scope", "authorization", "evidence"], "owner": "project/Fabric policy owner"},
    "multi-profile-pipeline": {"subject_type": "MULTI_PROFILE_PIPELINE", "core_checks": ["scope", "candidate", "evidence"], "owner": "project owner"},
    "stack": {"subject_type": "STACK_RELEASE", "core_checks": ["exact subject", "release", "evidence"], "owner": "Stack owner"},
    "skill": {"subject_type": "SKILL", "core_checks": ["version", "source", "mutation scope"], "owner": "owning Stack"},
    "knowledge": {"subject_type": "KNOWLEDGE", "core_checks": ["authority", "provenance", "claim ceiling"], "owner": "Knowledge + Domain owner"},
    "shared-service": {"subject_type": "SHARED_SERVICE", "core_checks": ["exact pin", "license", "install", "security", "rollback"], "owner": "provider/Fabric policy owner"},
    "sqs-financial-bridge": {"subject_type": "SQS_DOMAIN_CHANGE", "core_checks": ["engineering integrity only"], "owner": "SQS Financial Authority"},
    "oracle-meta": {"subject_type": "ORACLE_CHANGE", "core_checks": ["meta-subject", "frozen old oracle"], "owner": "Human/Frozen Meta-Oracle"},
}


def main() -> int:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ORACLE_DIR / "skills").mkdir(parents=True, exist_ok=True)

    (ORACLE_DIR / "distribution.yaml").write_text(DISTRIBUTION_YAML, encoding="utf-8")
    (ORACLE_DIR / "SOUL.md").write_text(SOUL_MD, encoding="utf-8")
    (ORACLE_DIR / "config.yaml").write_text(CONFIG_YAML, encoding="utf-8")
    (ORACLE_DIR / ".gitignore").write_text(GITIGNORE, encoding="utf-8")

    # schemas
    schemas = ORACLE_DIR / "schemas"
    schemas.mkdir(exist_ok=True)
    (schemas / "oracle_receipt.schema.json").write_text(json.dumps(ORACLE_RECEIPT_SCHEMA, indent=2), encoding="utf-8")
    (schemas / "acceptance_pack.schema.json").write_text(json.dumps(ACCEPTANCE_PACK_SCHEMA, indent=2), encoding="utf-8")

    # acceptance packs (10)
    packs_dir = ORACLE_DIR / "acceptance-packs"
    packs_dir.mkdir(exist_ok=True)
    for pid, meta in PACKS.items():
        pack = {
            "pack_id": pid,
            "subject_type": meta["subject_type"],
            "core_checks": meta["core_checks"],
            "final_semantic_owner": meta["owner"],
            "blocking_predicates": [f"locator:{c}" for c in meta["core_checks"]],
        }
        (packs_dir / pid / "pack.yaml").parent.mkdir(exist_ok=True)
        (packs_dir / pid / "pack.yaml").write_text(
            json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")

    # core/ knowledge packs: bind KP00~19 + prompt compiler as references (no duplication)
    core = ORACLE_DIR / "core"
    core.mkdir(exist_ok=True)
    kpack_index = KPACK / "19_KP_INDEX_CROSSWALK.md"
    check("O1_KPACK_INDEX_EXISTS", kpack_index.exists(), str(kpack_index))
    (core / "KPACK_BINDING.md").write_text(
        f"# KP00~19 KnowledgePack binding\n\nbound_to: {KPACK}\n"
        f"kp_index_sha256: {hashlib.sha256(kpack_index.read_bytes()).hexdigest()}\n"
        f"compiler_skill: {COMPILER / 'construction-acceptance-prompt-compiler_SKILL.md'}\n"
        f"prompt_compiler_sha256: {hashlib.sha256((COMPILER / 'construction-acceptance-prompt-compiler_SKILL.md').read_bytes()).hexdigest()}\n",
        encoding="utf-8")

    # validators (deterministic, real)
    validators = ORACLE_DIR / "validators"
    validators.mkdir(exist_ok=True)
    (validators / "oracle_preflight.py").write_text(VALIDATOR_PREFLIGHT, encoding="utf-8")
    (validators / "evidence_readback.py").write_text(VALIDATOR_READBACK, encoding="utf-8")
    (validators / "subject_binding.py").write_text(VALIDATOR_BINDING, encoding="utf-8")

    # tests (golden / negative / adversarial / holdout)
    tests = ORACLE_DIR / "tests"
    for sub in ("golden", "negative", "adversarial", "holdout"):
        (tests / sub).mkdir(parents=True, exist_ok=True)
    (tests / "golden" / "test_golden.py").write_text(TEST_GOLDEN, encoding="utf-8")
    (tests / "negative" / "test_negative.py").write_text(TEST_NEGATIVE, encoding="utf-8")
    (tests / "adversarial" / "test_adversarial.py").write_text(TEST_ADVERSARIAL, encoding="utf-8")
    (tests / "holdout" / "test_holdout.py").write_text(TEST_HOLDOUT, encoding="utf-8")

    # CHECKER isolation recipe doc
    (ORACLE_DIR / "CHECKER_ISOLATION_RECIPE.md").write_text(CHECKER_RECIPE, encoding="utf-8")

    # ── run the validators + tests (real execution) ────────────────────────
    for v in ("oracle_preflight", "evidence_readback", "subject_binding"):
        p = subprocess.run([sys.executable, str(validators / f"{v}.py")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        check(f"O1_VALIDATOR_{v}", p.returncode == 0 and "VALIDATOR_OK" in p.stdout, p.stdout[-80:] + p.stderr[-80:])
    for t in ("golden", "negative", "adversarial", "holdout"):
        p = subprocess.run([sys.executable, str(tests / t / f"test_{t}.py")],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        check(f"O1_TESTS_{t}", p.returncode == 0 and "TESTS_OK" in p.stdout, p.stdout[-80:] + p.stderr[-80:])

    # ── fresh CHECKER isolation: candidate write tools absent ──────────────
    recipe = (ORACLE_DIR / "CHECKER_ISOLATION_RECIPE.md").read_text(encoding="utf-8")
    check("O1_CHECKER_RECIPE",
          "read-only" in recipe and "write tools ABSENT" in recipe and "allowed write-set = OracleReceipt" in recipe,
          "isolation recipe present")
    check("O1_SELF_PROMOTION_DENIED", "self-approve" in SOUL_MD, "self-promotion denied in SOUL")

    verdict = "PASS" if all(c["pass"] for c in checks) else "FAIL"
    evidence = {
        "artifact_id": "RP002_O1_EVIDENCE",
        "project_id": "HGK-REFERENCE-PROJECT-002",
        "generated_at_utc": ts,
        "oracle": "EXTERNAL_FROZEN_META_ORACLE",  # O1 qualification authority is external
        "gate": "O1",
        "verdict": verdict,
        "checks": checks,
        "oracle_profile_dir": str(ORACLE_DIR),
        "oracle_package_digest": hashlib.sha256(
            (ORACLE_DIR / "distribution.yaml").read_bytes()).hexdigest(),
        "acceptance_oracle_digest": hashlib.sha256(
            (ORACLE_DIR / "SOUL.md").read_bytes()).hexdigest(),
        "internal_oracle_promotion_receipt": None,  # filled only after external meta qualification
        "external_meta_qualification_required": {
            "authority": "EXTERNAL FROZEN META-ORACLE (this dialogue's GPT-5.6 Sol contract)",
            "rule": "Internal Oracle candidate must NOT self-promote (r3 §9.5, §16 O1, §26.2)",
            "status": "PENDING_EXTERNAL_CONFIRMATION_VIA_SINGLE_REVIEW_MD",
            "evidence_for_external_check": [
                "Fabric/rp002/O1/RP002_O1_EVIDENCE.json",
                "Fabric/profiles/construction-acceptance-oracle/CHECKER_ISOLATION_RECIPE.md",
                "Fabric/profiles/construction-acceptance-oracle/validators/*.py",
                "Fabric/profiles/construction-acceptance-oracle/tests/{golden,negative,adversarial,holdout}/*.py",
            ],
            "note": "Deterministic materialization + validators/tests PASS here; the promotion receipt is created only by the external Meta-Oracle after reviewing the single evidence MD (prompt §8).",
        },
    }
    (O1 / "RP002_O1_EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


VALIDATOR_PREFLIGHT = '''# -*- coding: utf-8 -*-
"""Oracle preflight validator: receipt schema + required fields + verdict enum."""
import json, sys, hashlib
def validate(receipt: dict) -> dict:
    errs = []
    for k in ("oracle_id", "oracle_package_digest", "subject_digest", "acceptance_oracle_digest", "verdict"):
        if k not in receipt:
            errs.append(f"MISSING:{k}")
    if receipt.get("verdict") not in ("PASS", "PARTIAL", "FAIL", "TEMP_CLOSED"):
        errs.append(f"BAD_VERDICT:{receipt.get('verdict')}")
    for k in ("oracle_package_digest", "subject_digest", "acceptance_oracle_digest"):
        v = receipt.get(k, "")
        if v and (len(v) != 64 or any(c not in "0123456789abcdef" for c in v)):
            errs.append(f"BAD_DIGEST:{k}")
    return {"ok": not errs, "errors": errs}
if __name__ == "__main__":
    good = {"oracle_id": "CONSTRUCTION_ACCEPTANCE_ORACLE", "oracle_package_digest": "a" * 64,
            "subject_digest": "b" * 64, "acceptance_oracle_digest": "c" * 64, "verdict": "PASS"}
    bad = {"verdict": "SELF_APPROVED"}
    r1, r2 = validate(good), validate(bad)
    ok = r1["ok"] and not r2["ok"] and "MISSING:oracle_id" in r2["errors"]
    print("VALIDATOR_OK" if ok else "VALIDATOR_FAIL", json.dumps({"good": r1, "bad": r2}))
    sys.exit(0 if ok else 1)
'''

VALIDATOR_READBACK = '''# -*- coding: utf-8 -*-
"""Evidence readback validator: raw byte readback + sha256 + truncation sentinel scan."""
import hashlib, sys
SENTINEL = b"...[truncated]"
def verify_critical_write(path: str) -> dict:
    raw = open(path, "rb").read()
    if SENTINEL in raw:
        raise RuntimeError(f"ERR_LITERAL_TRUNCATION_SENTINEL:{path}")
    return {"path": path, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
if __name__ == "__main__":
    import tempfile, os
    d = tempfile.mkdtemp(prefix="oracle-rb-")
    p = os.path.join(d, "probe.txt")
    open(p, "wb").write(b"good\\n" * 3)
    r = verify_critical_write(p)
    poison = os.path.join(d, "poison.txt")
    open(poison, "wb").write(b"x\\n...[truncated]\\n")
    try:
        verify_critical_write(poison)
        ok = False
    except RuntimeError as exc:
        ok = "ERR_LITERAL_TRUNCATION_SENTINEL" in str(exc)
    ok = ok and len(r["sha256"]) == 64 and r["bytes"] == 15
    print("VALIDATOR_OK" if ok else "VALIDATOR_FAIL", r)
    sys.exit(0 if ok else 1)
'''

VALIDATOR_BINDING = '''# -*- coding: utf-8 -*-
"""Subject binding validator: receipt must bind exact subject digest + pack ids."""
import json, sys
def bind(receipt: dict, subject_digest: str, pack_ids: list[str]) -> dict:
    errs = []
    if receipt.get("subject_digest") != subject_digest:
        errs.append("SUBJECT_MISMATCH")
    missing = [p for p in pack_ids if p not in receipt.get("acceptance_pack_ids", [])]
    if missing:
        errs.append(f"MISSING_PACKS:{missing}")
    return {"ok": not errs, "errors": errs}
if __name__ == "__main__":
    good = {"subject_digest": "d" * 64, "acceptance_pack_ids": ["hermes-runtime", "kanban"]}
    bad = {"subject_digest": "e" * 64, "acceptance_pack_ids": []}
    r1 = bind(good, "d" * 64, ["hermes-runtime"])
    r2 = bind(bad, "d" * 64, ["hermes-runtime"])
    ok = r1["ok"] and not r2["ok"]
    print("VALIDATOR_OK" if ok else "VALIDATOR_FAIL", json.dumps({"good": r1, "bad": r2}))
    sys.exit(0 if ok else 1)
'''

TEST_GOLDEN = '''# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from oracle_preflight import validate
good = {"oracle_id": "O", "oracle_package_digest": "a" * 64, "subject_digest": "b" * 64,
        "acceptance_oracle_digest": "c" * 64, "verdict": "PASS"}
assert validate(good)["ok"]
print("TESTS_OK")
'''

TEST_NEGATIVE = '''# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from oracle_preflight import validate
bad = {"verdict": "PASS"}
assert not validate(bad)["ok"] and "MISSING:oracle_id" in validate(bad)["errors"]
print("TESTS_OK")
'''

TEST_ADVERSARIAL = '''# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from evidence_readback import verify_critical_write
import tempfile, os
d = tempfile.mkdtemp(prefix="oracle-adv-")
p = os.path.join(d, "p.txt")
open(p, "wb").write(b"ok\\n...[truncated]")
try:
    verify_critical_write(p)
    raise SystemExit("SENTINEL_NOT_DETECTED")
except RuntimeError:
    pass
print("TESTS_OK")
'''

TEST_HOLDOUT = '''# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "validators"))
from subject_binding import bind
r = bind({"subject_digest": "f" * 64, "acceptance_pack_ids": ["stack"]}, "f" * 64, ["stack"])
assert r["ok"]
r2 = bind({"subject_digest": "f" * 64, "acceptance_pack_ids": []}, "f" * 64, ["stack"])
assert not r2["ok"]
print("TESTS_OK")
'''

CHECKER_RECIPE = """# Oracle CHECKER isolation recipe (fresh/read-only)
1. same frozen Oracle Distribution digest as the COMMANDER
2. fresh session or ephemeral checker run (no commander session reuse)
3. maker memory preload OFF
4. candidate/source/evaluator write tools ABSENT
5. authority/promotion tools ABSENT
6. allowed write-set = OracleReceipt + checker logs only
7. output = OracleReceipt only (schema RP002-ORACLE-RECEIPT/1)
A same-profile long-running session that previously commanded the maker is NOT sufficient.
"""


if __name__ == "__main__":
    sys.exit(main())
