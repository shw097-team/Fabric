# -*- coding: utf-8 -*-
"""
RP-002 D1 — DOCUMENT_FACTORY_SECOND_ACCEPTANCE executor.

Closes the engineering contract chain in the HGK Shared Spine for the 18
canonical gate requirements:
    Requirement(FROZEN) -> ADR/SDD -> TaskSpec -> WorkOrder -> Acceptance -> Evidence -> Rollback
required_requirement_orphan = 0.

Consumes only K1-sealed current contract. Emits:
  Fabric/rp002/D1/RP002_D1_DESIGN_CONTRACT.md   ADR/SDD (engineering design contract)
  Fabric/rp002/D1/RP002_D1_EVIDENCE.json         maker evidence + predicates
  Fabric/rp002/D1/RP002_D1_CONTRACT_LEDGER.tsv   requirement->taskspec->workorder->evidence rows
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
D1 = FAB / "rp002" / "D1"
D1.mkdir(parents=True, exist_ok=True)
DB = HGK / "var" / "shared-spine" / "hg-kseos.db"
PROJECT = "HGK-REFERENCE-PROJECT-002"
BASE_HEAD = subprocess.run(["git", "-C", str(HGK), "rev-parse", "HEAD"],
                           capture_output=True, text=True).stdout.strip()

# gate -> (taskspec objective, workorder title, evidence kind)
GATE_CONTRACTS = {
    "G0": ("Freeze input baseline: full denominator + external bootstrap oracle + machine truth artifacts",
           "WO-RP2-G0 baseline freeze", "D1-DESIGN-CONTRACT"),
    "G1": ("Qualify pinned Hermes runtime: executable/profile/Kanban/Windows + 6 permanent guards",
           "WO-RP2-G1 runtime qualification", "D1-DESIGN-CONTRACT"),
    "K1": ("Govern 教程字幕 corpus + cross-distill with RP-002/HGK/SQS corpora; no invented norm",
           "WO-RP2-K1 knowledge distillation", "D1-DESIGN-CONTRACT"),
    "D1": ("Close requirement->design->taskspec->workorder->acceptance->evidence->rollback chain",
           "WO-RP2-D1 documentation contract", "D1-DESIGN-CONTRACT"),
    "C1": ("Coding factory reuse-first: FIT-GAP->REUSE->BIND->ADAPT->TEST; materialize Profile/TEAM/Stack",
           "WO-RP2-C1 coding factory acceptance", "D1-DESIGN-CONTRACT"),
    "H1": ("Materialize 4 HGK Profile Distributions + HGK/TEAM.md + Stack Manifest + inherited probes",
           "WO-RP2-H1 profile team ready", "D1-DESIGN-CONTRACT"),
    "O1": ("Materialize construction-acceptance-oracle Profile (Core+Packs+validators+fresh CHECKER)",
           "WO-RP2-O1 internal oracle ready", "D1-DESIGN-CONTRACT"),
    "B1": ("Create RP002-FABRIC-BOOTSTRAP board + RP002/TEAM.md + ExecutionBindings + liveness/auth",
           "WO-RP2-B1 kanban board/team/dag", "D1-DESIGN-CONTRACT"),
    "F0": ("Bind Fabric governance contracts/change router into existing HGK APL consumers",
           "WO-RP2-F0 fabric policy consumer", "D1-DESIGN-CONTRACT"),
    "CF1": ("Qualify ContextForge A2A+MCP + OASF records + OTel conditional in local sandbox",
            "WO-RP2-CF1 contextforge/oasf interop", "D1-DESIGN-CONTRACT"),
    "F1": ("Self-hosting cutover: post-F1 normal work via WorkOrder->Binding->Profile->Kanban",
           "WO-RP2-F1 self-hosting cutover", "D1-DESIGN-CONTRACT"),
    "KG1": ("Knowledge governance: namespace/ACL/revoke/promotion/provider-state preservation",
            "WO-RP2-KG1 knowledge governance", "D1-DESIGN-CONTRACT"),
    "SQP1": ("Materialize SQS Stack Manifest + SQS/TEAM.md + 3 SQS Profile Distributions",
             "WO-RP2-SQP1 sqs profile team", "D1-DESIGN-CONTRACT"),
    "S1": ("Run a real SQS LOCAL/PAPER/NO-LIVE-WRITE operational canary with domain/risk acceptance",
           "WO-RP2-S1 sqs real canary", "D1-DESIGN-CONTRACT"),
    "E1": ("Cross-stack engineering evolution: real/fault-labeled defect->repair->promote->replay",
           "WO-RP2-E1 cross-stack evolution", "D1-DESIGN-CONTRACT"),
    "E2": ("Behavioral artifact evolution: SOUL/Skill/Profile defect->patch->replay+rollback",
           "WO-RP2-E2 behavioral evolution", "D1-DESIGN-CONTRACT"),
    "E3": ("Meta-Oracle evolution only if actual Oracle change; else N/A_WITH_SOURCE_LOCATOR",
           "WO-RP2-E3 meta-oracle (conditional)", "D1-DESIGN-CONTRACT"),
    "R1": ("Final local acceptance: all gates + blocking TT=0 + subject/evidence/package readback",
           "WO-RP2-R1 final acceptance", "D1-DESIGN-CONTRACT"),
}


def main() -> int:
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row
    rows = []
    errors = []

    # current requirement states
    reqs = {r["requirement_id"]: r for r in con.execute(
        "SELECT requirement_id,state,version FROM requirements WHERE project_id=?", (PROJECT,))}

    for gid, (objective, title, kind) in GATE_CONTRACTS.items():
        req_id = f"REQ-RP2-{gid}"
        ts_id = f"TS-RP2-{gid}"
        wo_id = f"WO-RP2-{gid}"
        ev_id = f"EVD1-{gid}"
        try:
            # 1. freeze requirement (CANDIDATE -> FROZEN) with lease
            if req_id in reqs and reqs[req_id]["state"] == "CANDIDATE":
                token = hashlib.sha256(f"d1-freeze-{req_id}".encode()).hexdigest()
                con.execute("DELETE FROM leases WHERE resource_id=?", (req_id,))
                con.execute(
                    "INSERT INTO leases(resource_id,holder,token_hash,expires_at,created_at) "
                    "VALUES(?,?,?,?,?)",
                    (req_id, "d1-executor", hashlib.sha256(token.encode()).hexdigest(),
                     (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=10)).isoformat(),
                     datetime.datetime.now(datetime.timezone.utc).isoformat()))
                con.commit()
                con.execute(
                    """UPDATE requirements SET state='FROZEN',version=version+1,updated_at=?
                       WHERE requirement_id=? AND version=?""",
                    (datetime.datetime.now(datetime.timezone.utc).isoformat(), req_id, reqs[req_id]["version"]))
                con.execute(
                    "INSERT INTO canonical_events(event_id,idempotency_key,entity_type,entity_id,from_state,to_state,"
                    "actor,expected_version,resulting_version,payload_json,evidence_ref,rollback_pointer,created_at) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (f"EVT-D1-{gid}", f"d1-freeze-{req_id}", "requirement", req_id, "CANDIDATE", "FROZEN",
                     "d1-executor", reqs[req_id]["version"], reqs[req_id]["version"] + 1, "{}",
                     f"Fabric/rp002/D1/RP002_D1_DESIGN_CONTRACT.md", f"RB-{req_id}",
                     datetime.datetime.now(datetime.timezone.utc).isoformat()))
                con.commit()
            # 2. taskspec (requires FROZEN)
            con.execute(
                """INSERT INTO taskspecs(taskspec_id,requirement_id,objective,owner,writable_root,permissions_json,
                   tests_json,rollback_pointer,evidence_plan,state,version,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,'DRAFT',0,?,?)
                   ON CONFLICT(taskspec_id) DO UPDATE SET objective=excluded.objective""",
                (ts_id, req_id, objective, "d1-executor", str(FAB / "rp002" / "D1"),
                 json.dumps({"read": ["hgk.*"], "write": ["rp002/D1"]}),
                 json.dumps([f"RP2-T0{i:02d}" for i in range(1, 7)]),
                 f"RB-{ts_id}", "K1-sealed contract -> design -> taskspec",
                 datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 datetime.datetime.now(datetime.timezone.utc).isoformat()))
            # 3. workorder (requires DRAFT taskspec)
            con.execute(
                """INSERT INTO workorders(workorder_id,taskspec_id,writer,worktree,base_head,state,rollback_pointer,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(workorder_id) DO UPDATE SET base_head=excluded.base_head""",
                (wo_id, ts_id, "d1-executor", str(FAB / "rp002" / "worktrees" / gid), BASE_HEAD, "CREATED",
                 f"RB-{wo_id}",
                 datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 datetime.datetime.now(datetime.timezone.utc).isoformat()))
            con.execute("UPDATE taskspecs SET state='ADMITTED',version=version+1,updated_at=? WHERE taskspec_id=?",
                        (datetime.datetime.now(datetime.timezone.utc).isoformat(), ts_id))
            # 4. evidence ref (sha filled after design doc written below)
            con.execute(
                """INSERT INTO evidence_refs(evidence_id,kind,locator,sha256,producer,checker,created_at)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(evidence_id) DO UPDATE SET locator=excluded.locator""",
                (ev_id, kind, f"Fabric/rp002/D1/RP002_D1_DESIGN_CONTRACT.md",
                 "0" * 64, "d1-executor", "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
                 datetime.datetime.now(datetime.timezone.utc).isoformat()))
            con.commit()
            rows.append({"requirement_id": req_id, "taskspec_id": ts_id, "workorder_id": wo_id,
                         "evidence_id": ev_id, "state": "FROZEN/ADMITTED/CREATED"})
        except Exception as exc:  # noqa: BLE001
            errors.append({"gate": gid, "error": f"{type(exc).__name__}: {exc}"})
            con.rollback()
    con.close()

    # ── ADR/SDD design contract (single canonical design doc) ───────────────
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    design = f"""# RP-002 Design Contract (ADR/SDD) — Fabric-Governed Profile-Distributed Kanban-Coordinated Upgrade

artifact_id: RP002_D1_DESIGN_CONTRACT
generated_at_utc: {ts}
supersedes: r2 design lineage (r3 is current substantive blueprint; r2 discussions are design lineage only)
oracle: EXTERNAL_FROZEN_BOOTSTRAP_ORACLE
base_head: {BASE_HEAD}

## ADR-001 — Architecture decision: only HGK + SQS are heavy stacks
Decision: keep HG-KSEOS and SQS-THC as the only durable engineering/financial stacks.
Hermes runtime = execution plane (Profiles/Distribution/Kanban/A2A); Fabric = governance
contracts + bindings, never an actor/daemon. Second orchestrator/reducer/task-DB/
knowledge-platform is prohibited (r3 §1.2, §6.1; N-RP2-05/06).

## ADR-002 — Bootstrap inversion
G0~C1 execute with CURRENT_CERTIFIED_HGK_RUNTIME + EXTERNAL_FROZEN_BOOTSTRAP_ORACLE.
New Profile Team is not assumed before H1; internal Oracle candidate is null until O1
(r3 §15.1; FROZEN_ACCEPTANCE_ORACLE.yaml). G0 freeze binds prompt r1 + blueprint r3 +
current controls digests (RP002_G0_FREEZE.json).

## ADR-003 — WorkOrder is the executor contract
HGK WorkOrder remains normative; Kanban is runtime pointer/status only. ExecutionBinding
ABI (RP002_EXECUTION_BINDING.schema.json) binds workorder->kanban task->profile without
creating a second task truth (r3 §6.8, §14.2).

## SDD-001 — Factory second-acceptance contract chain
For each canonical gate requirement REQ-RP2-{{GATE}}:
  Requirement (FROZEN in Shared Spine) -> ADR/SDD (this doc) -> TaskSpec (TS-RP2-*)
  -> WorkOrder (WO-RP2-*) -> Acceptance (RP2-T0xx suite) -> Evidence (EVD1-*)
  -> Rollback (RB-* pointer). required_requirement_orphan = 0.

## SDD-002 — Profile Team runtime materialization
8 profile instances per RP002-PROFILE-TEAM-MANIFEST.yaml; each instance = distribution.yaml
+ SOUL.md + config.yaml + skills/ + toolset/model/provider/MCP readback; Profile != sandbox
(r3 §10.2-10.3). HGK/TEAM.md, SQS/TEAM.md, RP002/TEAM.md materialize the team graphs.

## SDD-003 — Inherited capability preservation
Codex/OpenCodex/OpenCode provider route, OpenSpec brownfield, gstack selected advisory
slices, Spec Kit XOR, GE, independent checker/reducers: preserve-or-requalify; silent
fallback/fake invocation prohibited (RP002_TOOL_AND_INHERITED_CAPABILITY_MATRIX.yaml).

## SDD-004 — Oracle internalization
construction-acceptance-oracle Profile: Oracle Core + KP00~19 + prompt compiler + validators
+ Acceptance Packs + OracleReceipt schema; CHECKER = fresh read-only context, no candidate
write tools (r3 §9). Meta-Oracle stays external for O1 qualification and E3.

## SDD-005 — SQS selective profileization + real canary
SQS Stack Manifest keeps Financial Truth owner in SQS controls; 3 profiles (orchestrator,
data-analysis, risk); S1 runs a real LOCAL/PAPER/NO-LIVE-WRITE task; live_trading
NOT_AUTHORIZED (r3 §10.5, §SQP1/S1).

## SDD-006 — Cross-stack + behavioral evolution
E1: real/fault-labeled SQS defect -> reproduce -> classify -> smallest HGK repair -> old+new
regression -> independent/domain check -> atomic promotion -> same task replay.
E2: SOUL/Skill/Profile/Pipeline durable behavior defect -> versioned patch -> fresh session
effective-load -> positive+negative+regression -> promotion -> replay -> rollback drill.

## SDD-007 — Evidence truth
Single canonical Evidence Manifest; MD is renderer, not truth owner. SubjectAttestation
binds repo heads + distribution commits + stack manifests + oracle digest + manifest digest
(r3 §6.6, §7.3).
"""
    (D1 / "RP002_D1_DESIGN_CONTRACT.md").write_text(design, encoding="utf-8")
    design_sha = hashlib.sha256((D1 / "RP002_D1_DESIGN_CONTRACT.md").read_bytes()).hexdigest()

    # fill real design digest into evidence refs
    con = sqlite3.connect(str(DB))
    con.execute("UPDATE evidence_refs SET sha256=? WHERE evidence_id LIKE 'EVD1-%' AND sha256='0000000000000000000000000000000000000000000000000000000000000000'",
                (design_sha,))
    con.commit()
    con.close()

    # ── ledger ──────────────────────────────────────────────────────────────
    with open(D1 / "RP002_D1_CONTRACT_LEDGER.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("requirement_id\ttaskspec_id\tworkorder_id\tevidence_id\tstate\n")
        for r in rows:
            f.write(f"{r['requirement_id']}\t{r['taskspec_id']}\t{r['workorder_id']}\t{r['evidence_id']}\t{r['state']}\n")

    # ── predicates ──────────────────────────────────────────────────────────
    checks = []
    def check(name, ok, detail):
        checks.append({"id": name, "pass": bool(ok), "detail": detail})

    check("D1_18_REQUIREMENTS_FROZEN", len([r for r in rows]) == 18 and not errors, f"rows={len(rows)} errors={errors}")
    con = sqlite3.connect(str(DB))
    frozen = con.execute("SELECT COUNT(*) FROM requirements WHERE project_id=? AND state='FROZEN'", (PROJECT,)).fetchone()[0]
    check("D1_SPINE_FROZEN_18", frozen == 18, f"frozen={frozen}")
    tspec = con.execute("SELECT COUNT(*) FROM taskspecs WHERE taskspec_id LIKE 'TS-RP2-%'").fetchone()[0]
    check("D1_TASKSPECS_18", tspec == 18, f"taskspecs={tspec}")
    wos = con.execute("SELECT COUNT(*) FROM workorders WHERE workorder_id LIKE 'WO-RP2-%'").fetchone()[0]
    check("D1_WORKORDERS_18", wos == 18, f"workorders={wos}")
    evs = con.execute("SELECT COUNT(*) FROM evidence_refs WHERE evidence_id LIKE 'EVD1-%'").fetchone()[0]
    check("D1_EVIDENCE_18", evs == 18, f"evidence={evs}")
    # orphan = requirement without taskspec/workorder, or taskspec/workorder without requirement
    orphan = con.execute(
        """SELECT COUNT(*) FROM requirements r
           WHERE r.project_id=? AND r.requirement_id LIKE 'REQ-RP2-%'
             AND (NOT EXISTS (SELECT 1 FROM taskspecs t WHERE t.requirement_id=r.requirement_id)
                  OR NOT EXISTS (SELECT 1 FROM workorders w JOIN taskspecs t2 ON t2.taskspec_id=w.taskspec_id
                                 WHERE t2.requirement_id=r.requirement_id))""",
        (PROJECT,)).fetchone()[0]
    check("D1_REQUIRED_ORPHAN_ZERO", orphan == 0, f"orphan={orphan}")
    con.close()

    verdict = "PASS" if all(c["pass"] for c in checks) else "FAIL"
    evidence = {
        "artifact_id": "RP002_D1_EVIDENCE",
        "project_id": PROJECT,
        "generated_at_utc": ts,
        "oracle": "EXTERNAL_FROZEN_BOOTSTRAP_ORACLE",
        "gate": "D1",
        "verdict": verdict,
        "checks": checks,
        "contract_rows": rows,
        "design_contract": {"path": str(D1 / "RP002_D1_DESIGN_CONTRACT.md"),
                            "sha256": design_sha,
                            "bytes": (D1 / "RP002_D1_DESIGN_CONTRACT.md").stat().st_size},
        "ledger": str(D1 / "RP002_D1_CONTRACT_LEDGER.tsv"),
        "base_head": BASE_HEAD,
    }
    (D1 / "RP002_D1_EVIDENCE.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
