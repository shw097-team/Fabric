"""HGK typed admission for ChangeSet R9-0 (FAR-informed residual / gap / owner-decision closure).

Mission: CNV-PIPD-LS-SP-20261015   ChangeSet: R9-0-FAR-RESIDUAL-CLOSURE
New project id (own requirement/taskspec/workorder lineage); R6/R7/R8 projects untouched.
Run from a git repository working directory (the controller reads git HEAD from the ambient cwd).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
sys.path.insert(0, ROOT + "/src")
from hg_kseos.cli import spine_for  # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController, ProjectRequest  # noqa: E402

R9 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9")
R8 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8")
R7 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7")
FAR = Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs")
FARG = Path("C:/Projects/Agent_Workspace/Fabric/FABRIC/fabric-autonomous-research")
ATTACH = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
# attempt 2: the last dash segment must be UNIQUE - plan() derives spec ids as TS-<last segment>-NN,
# and attempt 1 ("...CLOSURE") collided with the R8 project's TS-CLOSURE-01..04 (see R9_FINDINGS.json).
PROJECT_ID = "CNV-R9-FARCLOSURE"
TARGET_ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"

GOAL = (
    "\u4f9d\u300aFabric_HG-KSEOS_Convergence_PIPD-LS-PKG\u300bv2.0.0\u3001\u300aFabric_HG-KSEOS_Convergence_\u6307\u63ee\u8584PROMPT\u3001"
    "EIA-FABRIC-CONVERGENCE-R6-20261015 finding register \u8207 FAR R0\u2013R8 \u751f\u547d\u9031\u671f\uff0c\u5c0d\u5168\u90e8\u300c\u6b98\u7559\u9805\u76ee\u3001\u7f3a\u53e3\u3001"
    "\u5f85 OWNER \u6c7a\u7b56\u9805\u76ee\u300d\u505a\u4e00\u8f2a\u53d7\u6cbb\u7406\u7814\u7a76\uff08FAR run 012\uff09\u4e26\u64da\u5176\u6700\u4f73\u5de5\u7a0b\u88c1\u6c7a\u76f4\u63a5\u57f7\u884c\uff1a"
    "(a) \u95dc\u9589 BLK-R8-WS2-MAIN-DIVERGENCE\uff08\u786c\u5316\u6b04\u5728 main \u65b0\u7248\u5951\u7d04\u4e0b\u7684 2 \u500b\u5931\u6557 + derive_frozen_context \u5d29\u6f70\u8def\u5f91\uff09\uff1b"
    "(b) \u4fee\u5fa9 hgk-governed-execution \u7626\u8eab\u5019\u9078\u7684 2 \u8655\u771f\u5be6\u5167\u5bb9\u907a\u5931\u4e26\u91cd\u8dd1 C1\u2013C6\uff0c\u5171\u7b49\u5b89\u5168\u5247\u8d70 guarded apply\uff1b"
    "(c) \u5c0d R8-F6\uff08lane control plane \u81ea\u76f8\u77db\u76fe / \u4e0d\u7b26\u547d\u4ee4\uff09\u8207 TF-06\uff08arm \u5c65\u7d04\u7121\u6cd5\u8b49\u660e\uff09\u7522\u51fa owner-ready \u4e00\u52d5\u4f5c\u88c1\u6c7a\u8a18\u9304\uff1b"
    "(d) \u89e3\u6790 R8-F7\uff08PKG RQ06 \u7684 10/6 slice \u5207\u5206\u5b9a\u7fa9\uff09\u4e26\u66f4\u65b0 PKG \u5c0d\u9f4a\u6620\u5c04\uff1b"
    "(e) \u767c\u4f48 R9 evidence packet \u81f3 Fabric repo \u4f9b\u5916\u90e8\u9a57\u6536\u5b98\u3002"
)
CONSTRAINTS = [
    "\u4e0d\u5f97\u6539\u5beb\u5df2\u5408\u4f75\u7684 EVIDENCE/CNV-PIPD-LS-SP-20261015/**\u3001-R7/**\u3001-R8/** \u65e2\u6709\u63d0\u4ea4\u3002",
    "\u4e0d\u5f97\u81ea\u9a57\u6536\u3001\u4e0d\u5f97\u81ea\u6211\u6649\u5347\u88c1\u6c7a\uff1bmaker \u2260 checker \u2260 AO\u3002",
    "\u4e0d\u5f97\u5ba3\u7a31\u4efb\u4f55 Gate PASS\u3001\u4e0d\u5f97\u57f7\u884c 221 cases\u3001\u4e0d\u5f97\u5ba3\u7a31 Product/Production\u3002",
    "\u4e0d\u5f97\u5efa\u7acb\u7b2c\u4e8c\u63a7\u5236\u5e73\u9762\u3001\u7b2c\u4e8c DB \u6216\u9577\u99d0 CI\u3002",
    "\u6191\u8b49\u4e00\u5f8b\u4e0d\u5f97\u9032\u5165 argv\uff0fURL\uff0flog\uff0fartifact\u3002",
    "canonical \u5beb\u5165\uff08Hermes skills \u6a39\u3001HG-KSEOS \u63a7\u5236\u9762\uff09\u9808\u8d70 guarded apply\uff1apre-image \u5099\u4efd\u3001receipt\u3001rollback\u3002",
    "\u63a7\u5236\u5e73\u9762\uff08lane registry / dispatcher\uff09\u8b8a\u66f4\u53ea\u767c\u51fa owner-ready \u88c1\u6c7a\u8a18\u9304\uff0c\u4e0d\u81ea\u6e05\u3002",
]
NON_GOALS = [
    "Fresh G1 \u91cd\u8a8d\u8a3c\u3001DOC-05 effect admission\u3001Owner/AO/Release \u6388\u6b0a\uff08\u4eba\u529b\u9580\u6aee\uff09\u3002",
    "24 AUD \u5168\u91cf\u9589\u5408\u8207 8 Gates \u5168\u6578 PASS\u3002",
    "\u91cd\u5beb\u63a7\u5236\u5e73\u9762\u3001Stage-2/Stage-3 \u91cd\u5efa\u3001\u4efb\u4f55 production/live/trade \u884c\u70ba\u3002",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    R9.mkdir(parents=True, exist_ok=True)
    srcs = [
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"),
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_\u6307\u63ee\u8584PROMPT.md"),
        str(ATTACH / "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md"),
        str(Path(ROOT) / "AGENTS.md"),
        str(R8 / "R8_LEDGER.json"),
        str(R8 / "R8_SYNTHESIS.md"),
        str(R8 / "PKG_ALIGNMENT_R8.json"),
        str(R8 / "R8_PUBLICATION_VERIFICATION.json"),
        str(R8 / "R8_VERIFY" / "R8_VERIFY_VERDICT.json"),
        str(R8 / "R8_VERIFY" / "WS_B_3_ATTRIBUTION_ERRATA.json"),
        str(R7 / "CHECKPOINT_STATE_20261016.json"),
        str(FAR / "FAR-20261016-011-r5r3-preview4-live-subject" / "OpenQuestionLedger.tsv"),
        str(FAR / "FAR-20261016-011-r5r3-preview4-live-subject" / "ResearchHandoff.yaml"),
        str(FAR / "FAR-20261015-010-r6r7-closure-and-r7-slice" / "OpenQuestionLedger.tsv"),
        str(FARG / "governance" / "FAR_CAPABILITY_MATRIX.yaml"),
        str(FARG / "research-product" / "RESEARCH_ARTIFACT_CONTRACTS.yaml"),
    ]
    present, missing, inv = [], [], []
    for s in srcs:
        p = Path(s)
        if p.is_file():
            present.append(s)
            inv.append({"path": s, "bytes": p.stat().st_size, "sha256": sha(p)})
        else:
            missing.append(s)
    out = R9 / "HGK_TYPED_ADMISSION_R9.json"
    rep = {"schema": "CNV-PIPD-LS-SP-20261015-R9/HGK-TYPED-ADMISSION/1", "project_id": PROJECT_ID,
           "changeset": "R9-0-FAR-RESIDUAL-CLOSURE", "sources_present": len(present),
           "sources_missing": missing, "source_inventory": inv, "steps": []}
    if missing:
        rep["verdict"] = "BLOCKED_SOURCE_MISSING"
        out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"verdict": rep["verdict"], "missing": missing}, ensure_ascii=False))
        return 2
    spine = spine_for(Path(ROOT))
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=GOAL, source_paths=present, constraints=CONSTRAINTS,
                         non_goals=NON_GOALS, target_root=TARGET_ROOT)
    try:
        st = lc.status(PROJECT_ID)
        rep["steps"].append({"step": "start", "result": "ALREADY_EXISTS", "state": st["state"]})
    except Exception:
        st = lc.start(req, project_id=PROJECT_ID)
        rep["steps"].append({"step": "start", "result": "CREATED", "state": st["state"]})
    if lc.status(PROJECT_ID)["state"] == "PROJECT_CREATED":
        env = lc.intake(PROJECT_ID, req)
        rep["steps"].append({"step": "intake", "status": env["status"], "source_count": env["source_count"],
                             "blocking_missing": env["blocking_missing"], "conflicts": env["conflicts"]})
        if env["status"] != "READY":
            rep["verdict"] = "BLOCKED_INTAKE"
            out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"verdict": "BLOCKED_INTAKE", "detail": env}, ensure_ascii=False))
            return 3
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R9"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R9"),
                           ("DESIGN_READY", "DESIGN_READY_R9")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": f"SKIPPED_FROM_{cur}"})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig, evidence_refs=["PKG:v2.0.0", "EIA:R6", "FAR:run-012"])
        rep["steps"].append({"step": "transition", "to": to_state, "result": "OK"})
    if lc.status(PROJECT_ID)["state"] == "DESIGN_READY":
        pl = lc.plan(PROJECT_ID)
        rep["steps"].append({"step": "plan", "task_count": pl["task_count"],
                             "titles": [s["title"] for s in pl["plan"]]})
    if lc.status(PROJECT_ID)["state"] == "PLAN_READY":
        rep["steps"].append({"step": "admit_workorders", "result": lc.admit_workorders(PROJECT_ID)})
    rep["final_state"] = lc.status(PROJECT_ID)["state"]
    try:
        rep["denominator"] = lc.denominator(PROJECT_ID)
    except Exception as exc:  # noqa: BLE001
        rep["denominator_error"] = f"{type(exc).__name__}: {exc}"
    rep["verdict"] = ("ADMISSION_OK" if rep["final_state"] in ("WORKORDERS_ADMITTED", "EXECUTING")
                      else "ADMISSION_STATE_" + rep["final_state"])
    if rep.get("denominator"):
        ck = lc.checkpoint(PROJECT_ID)
        rep["checkpoint"] = ck.get("checkpoint_id") if isinstance(ck, dict) else str(ck)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": rep["verdict"], "final_state": rep["final_state"],
                      "sources_present": rep["sources_present"], "sources_missing": rep["sources_missing"],
                      "steps_tail": rep["steps"][-3:]}, ensure_ascii=False, indent=1))
    return 0 if rep["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
