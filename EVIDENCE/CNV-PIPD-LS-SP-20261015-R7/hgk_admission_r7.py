"""HGK typed admission for ChangeSet R7-0 (R7-02 validator hardening + R7-03 checker isolation).

Mission: CNV-PIPD-LS-SP-20261015   ChangeSet: R7-0-VALIDATOR-AND-CHECKER-ISOLATION
New project id (own requirement/taskspec/workorder lineage); the R6 and R6R7 projects are left untouched.
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

FAR_RUN = Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261015-010-r6r7-closure-and-r7-slice")
H7 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7")
ATTACH = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
PROJECT_ID = "CNV-R7-VALIDATOR-HARDEN-R7VH"
TARGET_ROOT = "C:/Projects/Agent_Workspace/PIPD"

GOAL = (
    "依外部審查 EIA-R6-04/EIA-R6-03 與 FAR run FAR-20261015-010 的裁決，執行有界 R7-0："
    "(a) 硬化 PIPD bound validator，使 M04（ProfileBinding ASSURED→LITE）、M06（domain oracle expected 被改）、"
    "M16（trace atom digest 失配）三類 tamper 皆為確定性 REJECT，且原本已偵測的 7 個維持 REJECT、"
    "8 個 NOT_RUN 維持 NOT_RUN；(b) 提供 checker 寫入根隔離與 write-denial fixture，"
    "無法以 OS 層達成時須誠實記 ACL_UNENFORCEABLE。"
)
CONSTRAINTS = [
    "只准修改 PIPD 產品 validator 及其呼叫面，以及 R7 handover 證據；不得改寫已合併的 EVIDENCE/CNV-PIPD-LS-SP-20261015/**。",
    "不得 git commit／push；不得觸碰 HG-KSEOS spine、config 或 WorkOrder 狀態。",
    "maker ≠ checker ≠ AO：writer 不得為自身產出 verdict。",
    "不得執行 221 cases、不得宣稱任何 Gate PASS、不得升級任何裁決。",
    "憑證一律不得進入 argv／URL／log／artifact。",
]
NON_GOALS = [
    "R7-01/04/05/06/07/08/09 各項（本輪僅立 TaskSpec 不執行）。",
    "Fresh G1 重認證、DOC-05 effect admission、AO／Release（人力閘門）。",
    "建立第二控制平面、第二 DB 或常駐 CI。",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    srcs = [str(H7 / "WRITER_BRIEF_R7.md"),
            str(FAR_RUN / "ResearchSynthesis.md"),
            str(FAR_RUN / "CandidateResearch.yaml"),
            str(FAR_RUN / "ProposedEvolution.yaml"),
            str(FAR_RUN / "ClaimLedger.tsv"),
            str(FAR_RUN / "ResearchRunReceipt.json"),
            str(ATTACH / "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md"),
            str(Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/MUTATIONS_18.json"))]
    present, missing, inv = [], [], []
    for s in srcs:
        p = Path(s)
        (present if p.is_file() else missing).append(s)
        if p.is_file():
            inv.append({"path": s, "bytes": p.stat().st_size, "sha256": sha(p)})
    out = H7 / "HGK_TYPED_ADMISSION_R7.json"
    rep = {"schema": "CNV-PIPD-LS-SP-20261015-R7/HGK-TYPED-ADMISSION/1", "project_id": PROJECT_ID,
           "changeset": "R7-0-VALIDATOR-AND-CHECKER-ISOLATION", "sources_present": len(present),
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
            print(json.dumps({"verdict": "BLOCKED_INTAKE"}, ensure_ascii=False))
            return 3
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R7"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R7"),
                           ("DESIGN_READY", "DESIGN_READY_R7")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": f"SKIPPED_FROM_{cur}"})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig, evidence_refs=["FAR_RUN:" + FAR_RUN.name])
        rep["steps"].append({"step": "transition", "to": to_state, "result": "OK"})
    if lc.status(PROJECT_ID)["state"] == "DESIGN_READY":
        pl = lc.plan(PROJECT_ID)
        rep["steps"].append({"step": "plan", "task_count": pl["task_count"], "titles": [s["title"] for s in pl["plan"]]})
    if lc.status(PROJECT_ID)["state"] == "PLAN_READY":
        rep["steps"].append({"step": "admit_workorders", "result": lc.admit_workorders(PROJECT_ID)})
    rep["final_state"] = lc.status(PROJECT_ID)["state"]
    try:
        rep["denominator"] = lc.denominator(PROJECT_ID)
    except Exception as exc:  # noqa: BLE001
        rep["denominator_error"] = f"{type(exc).__name__}: {exc}"
    rep["verdict"] = "ADMISSION_OK" if rep["final_state"] in ("WORKORDERS_ADMITTED", "EXECUTING") else "ADMISSION_STATE_" + rep["final_state"]
    if rep.get("denominator"):
        ck = lc.checkpoint(PROJECT_ID)
        rep["checkpoint"] = ck.get("checkpoint_id") if isinstance(ck, dict) else str(ck)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": rep["verdict"], "final_state": rep["final_state"],
                      "workorders": (rep["steps"][-1]["result"] or {}).get("workorders")}, ensure_ascii=False))
    return 0 if rep["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
