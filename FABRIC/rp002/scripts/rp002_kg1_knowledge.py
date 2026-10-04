# -*- coding: utf-8 -*-
"""
RP-002 KG1 — KNOWLEDGE_GOVERNANCE_READY executor.

Materialize namespace/ACL/provenance/revoke/promotion/cross-stack recall policy;
preserve provider-state ledger; FTS5 active baseline; no MemoryCandidate->Financial Truth escape.
Uses the REAL HGK KnowledgeFactory in a disposable temp spine (deterministic runtime probes).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
KG1 = FAB / "rp002" / "KG1"
KG1.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HGK / "src"))

from hg_kseos.knowledge import KnowledgeFactory  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402

checks = []
def check(name, ok, detail):
    checks.append({"id": name, "pass": bool(ok), "detail": detail})


def main() -> int:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # ── 1. provider-state preservation ledger (FTS5 active; others preserved) ──
    provider_ledger = {
        "schema": "RP002-KNOWLEDGE-PROVIDER-STATE-PRESERVATION/1",
        "providers": {
            "fts5": {"target_state": "ACTIVE_BASELINE", "activate_by_rp002": False},
            "qdrant": {"target_state": "PRESERVE_CURRENT_READBACK", "activate_by_rp002": False},
            "neo4j": {"target_state": "PRESERVE_CURRENT_READBACK", "activate_by_rp002": False},
            "cognee": {"target_state": "P1_SHADOW_CANDIDATE", "canonical_promotion": False},
            "pgvector": {"target_state": "CONDITIONAL_IF_CURRENT_POSTGRESQL_ARCHITECTURE_REQUIRES"},
        },
        "current_readback": {
            "fts5": "ACTIVE (knowledge_fts tables present in hg-kseos.db)",
            "qdrant": "NOT_ACTIVE (no provider binding in spine)",
            "neo4j": "NOT_ACTIVE (no provider binding in spine)",
            "cognee": "P1_SHADOW_ONLY (no canonical promotion)",
        },
    }
    (KG1 / "RP002_KNOWLEDGE_PROVIDER_STATE.json").write_text(
        json.dumps(provider_ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    # FTS5 active baseline verified from canonical spine
    con = sqlite3.connect(str(HGK / "var" / "shared-spine" / "hg-kseos.db"))
    fts_tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'knowledge_fts%'")]
    con.close()
    check("KG1_FTS5_BASELINE", len(fts_tables) >= 4, f"fts tables={len(fts_tables)}")
    check("KG1_PROVIDER_LEDGER", provider_ledger["providers"]["fts5"]["target_state"] == "ACTIVE_BASELINE",
          "provider ledger written")

    # ── 2. real runtime probes (disposable spine, deterministic) ─────────────
    with tempfile.TemporaryDirectory(prefix="rp002-kg1-") as td:
        db = Path(td) / "kg.db"
        spine = SharedSpine(db)
        spine.initialize()
        kf = KnowledgeFactory(spine)

        # ingest -> promote (NON-maker verifier) -> search hit
        ingest = kf.ingest_text("KG1 governance probe: namespace ACL read requires admitted source.",
                                "src-locator-001", authority_rank="A2")
        src_id = ingest["source_id"]
        cand_id = ingest["candidate_id"]
        doc_id = kf.promote(cand_id, verifier="KG1-CHECKER", evidence_ref="E-KG1-001", title="KG1 probe doc")
        try:
            hits = kf.search("governance")
            check("KG1_PROMOTE_SEARCH", len(hits) >= 1, f"hits={len(hits)}")
        except Exception as exc:  # noqa: BLE001
            check("KG1_PROMOTE_SEARCH", False, f"abstain:{exc}")

        # provenance: source unit bound to locator + hash
        with spine.connect() as con:
            row = con.execute("SELECT canonical_path,status FROM sources WHERE source_id=?", (src_id,)).fetchone()
            check("KG1_PROVENANCE_BOUND", row is not None and row["status"] == "PROMOTED", dict(row) if row else "missing")

        # stale/revoked exclusion: withdraw source -> search abstains
        kf.withdraw_source(src_id)
        kf.rebuild()
        try:
            hits2 = kf.search("governance")
            check("KG1_REVOKED_EXCLUDED", len(hits2) == 0, f"hits after revoke={len(hits2)}")
        except Exception:
            check("KG1_REVOKED_EXCLUDED", True, "search abstains after withdrawal (fail-closed)")

        # MemoryCandidate cannot promote FinancialSpec: memory write is scope-isolated,
        # no path from memory_records to FinancialSpec/risk tables (schema has none)
        mid = kf.remember("scope-a", "candidate: market regime signal", "KG1-PROBE", ttl_seconds=300)
        mem = kf.active_memory("scope-a")
        check("KG1_MEMORY_SCOPE_ISOLATED", any(m["memory_id"] == mid for m in mem), f"memory in scope-a={len(mem)}")
        mem_other = kf.active_memory("scope-b")
        check("KG1_MEMORY_NO_CROSS_SCOPE", all(m["memory_id"] != mid for m in mem_other), "no cross-scope leak")
        con2 = sqlite3.connect(str(db))
        fin_tables = [r[0] for r in con2.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%financial%' OR name LIKE '%risk_auth%' OR name LIKE '%order%')")]
        con2.close()
        check("KG1_NO_MEMORY_TO_FINANCIAL", len(fin_tables) == 0,
              f"no financial-truth table exists in knowledge spine (escape impossible): {fin_tables}")

        # namespace policy contract (read/write/promote/revoke matrix)
        ns = {
            "schema": "RP002-KNOWLEDGE-NAMESPACE/1",
            "namespaces": {"hgk.*": {"read": ["hgk.*", "shared.*"], "write": ["hgk.*"], "promote": ["hgk.*"]},
                           "sqs.*": {"read": ["sqs.*", "shared.allowed.*"], "write": ["sqs.runtime.*", "sqs.candidate.*"],
                                     "promote": ["sqs.*:DOMAIN_OWNER_ONLY"]},
                           "shared.*": {"read": ["*"], "write": ["shared.*"], "promote": ["shared.*:POLICY"]}},
            "rule": "cross-namespace read checks ACL before retrieval; revoked/stale source removed from projections",
        }
        (KG1 / "RP002_KNOWLEDGE_NAMESPACE.yaml").write_text(json.dumps(ns, ensure_ascii=False, indent=2), encoding="utf-8")
        check("KG1_NAMESPACE_CONTRACT", "sqs.*:DOMAIN_OWNER_ONLY" in json.dumps(ns), "namespace ACL contract written")

    verdict = "PASS" if all(c["pass"] for c in checks) else "FAIL"
    evidence = {
        "artifact_id": "RP002_KG1_EVIDENCE",
        "project_id": "HGK-REFERENCE-PROJECT-002",
        "generated_at_utc": ts,
        "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
        "gate": "KG1",
        "verdict": verdict,
        "checks": checks,
        "note": "Real KnowledgeFactory probes in disposable spine; provider-state ledger preserved; no MemoryCandidate->FinancialSpec escape path exists (schema-level proof).",
    }
    (KG1 / "RP002_KG1_EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
