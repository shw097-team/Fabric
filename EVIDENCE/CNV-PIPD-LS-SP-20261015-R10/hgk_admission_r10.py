"""HGK typed admission for ChangeSet R10-0 (session closure / handover, residual + unlanded-candidate closure).

Mission: CNV-PIPD-LS-SP-20261015   ChangeSet: R10-0-SESSION-CLOSURE
Own project id (own requirement/taskspec/workorder lineage); R6/R7/R8/R9 projects untouched.
The last dash segment is UNIQUE by construction: plan() derives taskspec ids as TS-<last segment>-NN.
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

R10 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10")
R9 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9")
R8 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8")
FAB = Path("C:/Projects/Agent_Workspace/Fabric")
FAR = FAB / "fabric-autonomous-research" / "runs"
ATTACH = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
OPENSPEC = Path(ROOT) / "openspec" / "changes"

PROJECT_ID = "CNV-R10-SESSCLOSE"
TARGET_ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"

GOAL = (
    "\u4f9d\u300aFabric_HG-KSEOS_Convergence_PIPD-LS-PKG\u300bv2.0.0 \u552f\u4e00\u6b0a\u5a01\u9c8e\u9ede\u8207 EIA "
    "R6 \u5831\u544a\uff0c\u5c0d\u5168\u90e8\u300c\u6b98\u7559\u9805\u76ee\u3001\u7f3a\u53e3\u3001\u5f85 OWNER \u6c7a\u7b56\u9805\u76ee\u3001"
    "\u5019\u9078\u672a\u843d\u5730\u5be6\u7528\u7684 SKILLS\u3001\u672c SESSION \u7d50\u6848\u8207\u79fb\u4ea4\u76f8\u95dc\u4e8b\u9805\u300d"
    "\u505a\u4e00\u8f2a FAR \u53d7\u6cbb\u7406\u7814\u7a76\u4e26\u76f4\u63a5\u57f7\u884c\u5176\u6700\u4f73\u5de5\u7a0b\u88c1\u6c7a\uff1a"
    "(a) \u5c07\u300chgk-far-remediation-20261016\u300d\u8207\u300cskill-mainfile-cap-remediation\u300d\u5169\u4efd"
    "\u9673\u820a\u8b8a\u66f4\u8a18\u9304\u9010\u5217\u5c0d\u7167\u5df2\u6e2c\u5f97\u73fe\u5be6\u88c1\u6c7a\uff08done / superseded / open\uff09\uff0c"
    "\u4e0d\u88fd\u9020\u6578\u91cf\u3001\u4e0d\u70ba\u6e05\u6848\u800c\u88dc\u4ef6\uff1b"
    "(b) \u4fee\u5fa9\u672c\u56de\u5408\u81ea\u6709\u5de5\u5177\u93c8\u7684\u5169\u500b\u5be6\u6e2c\u7f3a\u9677\uff08\u6309\u89d2\u8272\u8986\u5beb\u6536\u64da\u8def\u5f91\u3001"
    "nonce \u6aa2\u6e2c\u672a\u8b80\u8eca\u9053\u81ea\u6709\u4ef6\uff09\u4e26\u9644\u6e2c\u8a66\uff1b"
    "(c) \u7522\u51fa\u672c SESSION \u7684\u7d50\u6848\uff0f\u79fb\u4ea4\u5305\uff08checkpoint\u3001session ledger\u3001"
    "\u4e0b\u4e00\u8f2a residual worklist\uff09\uff1b"
    "(d) \u5c07\u5be6\u4f5c\u8207\u8b49\u64da\u63a8\u9001 Fabric \u4f9b\u5916\u90e8\u9a57\u6536\u5b98\u9a57\u6536\u3002"
)

CONSTRAINTS = [
    "\u4e0d\u5f97\u6539\u5beb\u5df2\u5408\u4f75\u7684 EVIDENCE/CNV-PIPD-LS-SP-20261015/**\u3001-R7/**\u3001-R8/**\u3001-R9/** \u65e2\u6709\u63d0\u4ea4\u3002",
    "\u4e0d\u5f97\u81ea\u9a57\u6536\u3001\u4e0d\u5f97\u81ea\u6211\u6649\u5347\u88c1\u51b3\uff1bmaker \u2260 checker \u2260 AO\uff1b"
    "\u672c\u8f2a\u547d\u4ee4\u5c07 checker \u8207 EXECUTE \u6307\u5411\u540c\u4e00 arm\uff0c\u6a21\u578b\u8ef8\u7368\u7acb\u6027 ABSENT\uff0c\u9808\u5982\u5be6\u8a18\u9304\u3002",
    "\u4e0d\u5f97\u5ba3\u7a31\u4efb\u4f55 Gate PASS\u3001\u4e0d\u5f97\u57f7\u884c 221 cases\u3001\u4e0d\u5f97\u5ba3\u7a31 Product/Production \u6216\u4efb\u4f55\u4e0a\u5e02\u6c7a\u5b9a\u3002",
    "\u4e0d\u5f97\u5efa\u7acb\u7b2c\u4e8c\u63a7\u5236\u5e73\u9762\u3001\u7b2c\u4e8c DB \u6216\u9577\u99d0 CI\uff1b\u4e0d\u5f97\u81ea\u6539 canonical lane registry\u3002",
    "\u6191\u8b49\u4e00\u5f8b\u4e0d\u5f97\u9032\u5165 argv\uff0fURL\uff0flog\uff0fartifact\uff1b\u4e0d\u5f97\u8b80\u53d6\u6216\u5217\u5370\u6191\u8b49\u503c\u3002",
    "\u540c\u5115\u5728\u98db\u56de\u5408\uff08pub/lane-reliability-closure-20261016\u3001evidence/FAR-REMEDIATION-AND-CLOSURE-20261016\uff09"
    "\u70ba\u552f\u8b80\uff1b\u4e0d\u5f97\u5207\u63db\u3001\u6e05\u7406\u6216\u8986\u5beb\u5176 checkout \u8207\u672a\u8ffd\u8e64\u7522\u7269\u3002",
    "\u63a7\u5236\u5e73\u9762\uff08lane registry\uff09\u8b8a\u66f4\u53ea\u767c\u51fa owner-ready \u88c1\u6c7a\u8a18\u9304\uff0c\u4e0d\u81ea\u6e05\u3002",
]
NON_GOALS = [
    "Fresh G1 \u91cd\u8a8d\u8a3c\u3001DOC-05 effect admission\u3001Owner/AO/Release \u6388\u6b0a\uff08\u4eba\u529b\u9580\u6aae\uff09\u3002",
    "221 cases\u30018 Gates\u5168\u6578 PASS\u3001AUD \u5168\u91cf\u9589\u5408\u3002",
    "\u91cd\u5beb\u63a7\u5236\u5e73\u9762\u3001Stage-2/3 \u91cd\u5efa\u3001\u4efb\u4f55 production/live/trade \u884c\u70ba\u3002",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    R10.mkdir(parents=True, exist_ok=True)
    srcs = [
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"),
        str(ATTACH / "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md"),
        str(Path(ROOT) / "AGENTS.md"),
        str(R9 / "R9_LEDGER.json"),
        str(R9 / "R9_SYNTHESIS.md"),
        str(R9 / "SELF_EVOLUTION_R9.json"),
        str(R9 / "R9_VERIFY" / "R9_VERDICT.json"),
        str(R9 / "R9_VERIFY" / "R9_VERDICT_ADJUDICATION.json"),
        str(R9 / "R9_PUBLICATION_VERIFICATION.json"),
        str(R9 / "R9_LATE_NOTIFICATION_RECONCILIATION.json"),
        str(R9 / "R9_M2_SCAN_LADDER.json"),
        str(R8 / "R8_LEDGER.json"),
        str(OPENSPEC / "hgk-far-remediation-20261016" / "tasks.md"),
        str(OPENSPEC / "skill-mainfile-cap-remediation" / "tasks.md"),
        str(OPENSPEC / "hgk-lane-reliability-closure-20261016" / "tasks.md"),
        str(OPENSPEC / "hgk-r9-far-residual-closure-20261016" / "tasks.md"),
        str(FAB / "evidence" / "FAR-REMEDIATION-AND-CLOSURE-20261016" / "PACKET_MANIFEST.json"),
        str(FAR / "FAR-20261016-012-r9-residual-closure" / "OpenQuestionLedger.tsv"),
    ]
    present, missing, inv = [], [], []
    for s in srcs:
        p = Path(s)
        if p.is_file():
            present.append(s)
            inv.append({"path": s, "bytes": p.stat().st_size, "sha256": sha(p)})
        else:
            missing.append(s)
    out = R10 / "HGK_TYPED_ADMISSION_R10.json"
    rep = {"schema": "CNV-PIPD-LS-SP-20261015-R10/HGK-TYPED-ADMISSION/1", "project_id": PROJECT_ID,
           "changeset": "R10-0-SESSION-CLOSURE", "sources_present": len(present),
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
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R10"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R10"),
                           ("DESIGN_READY", "DESIGN_READY_R10")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": "SKIPPED_FROM_" + cur})
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
        rep["denominator_error"] = type(exc).__name__ + ": " + str(exc)
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
