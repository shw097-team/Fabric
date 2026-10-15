"""HGK typed admission driver for the R6 archive NARROW_REPAIR change set.

Mission: CNV-PIPD-LS-SP-20261015   ChangeSet: NARROW_REPAIR (R6 evidence-archive minimal repair)
Runs the canonical lifecycle controller over the Shared Spine for a NEW project id that carries
this narrow change set on its own, so the R6 project's records are not overwritten:

  start -> intake -> INTENT_BOUND -> REQUIREMENTS_READY -> DESIGN_READY -> plan -> admit_workorders

Read-only apart from the sanctioned lifecycle writes in the Shared Spine. No secrets are read.
Emits HGK_TYPED_ADMISSION_R6R7.json next to this script.
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

HANDOVER = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015")
ATTACH = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
PROJECT_ID = "CNV-R6R7-ARCHIVE-REPAIR-R6ARC2"
TARGET_ROOT = "C:/Projects/Agent_Workspace/Fabric"

GOAL = (
    "依外部獨立驗收報告 EIA-FABRIC-CONVERGENCE-R6-20261015 的三個合併關卡，對既有 PR #3 的 R6 "
    "候選證據包執行最小、就地的發布修補：M1 讓 PACKET_MANIFEST 的 tracked 清單與實際 Git tree 集合等價、"
    "M2 由受信任包外掃描器驗範圍與秘密、M3 備妥 Maintainer 對單一 evidence prefix 的授權紀錄；"
    "並在提交後以外部機制讀回 new head，交付可獨立查驗的 Draft PR（archive 階段結案）。"
)
CONSTRAINTS = [
    "只准變更遠端前綴 EVIDENCE/CNV-PIPD-LS-SP-20261015/**；不得觸碰 main、HG-KSEOS/、FABRIC/、CI、secrets、canonical DB。",
    "不得加入兩個 .pyc；不得刪除或改寫 R6 失敗 receipts；不得對未改過的候選碼重跑 221 或宣稱八 Gate PASS。",
    "Maker 不等於 Checker 不等於 AO 不等於 Owner；本輪不自行核准、不代簽 AO/Release。",
    "非 force push；remote 結果未知時先讀回再決定，不盲重送。",
    "token 不得出現在模型脈絡、argv、URL、log、PR、.git/config 或 evidence；不得執行 PR 內 helper。",
]
NON_GOALS = [
    "重跑 221 live cases 或宣稱 G-A..G-H PASS。",
    "修 M04/M06/M16 產品 validator、修 OS ACL、重認證 Fresh G1。",
    "建立新 CI、第二控制平面、第二 orchestrator 或 RBWI。",
    "deploy／production／promotion；改 sealed Stage-2；改 unadmitted product。",
]


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build_sources() -> list[str]:
    return [
        str(ATTACH / "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md"),
        str(ATTACH / "Fabric × Hermes × HG-KSEOS｜R6 外部驗收後續作指揮薄 PROMPT.md"),
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"),
        str(HANDOVER / "C0_C9_CONTRACT_R6R7.json"),
        str(HANDOVER / "R6R7_COMPILED_OUT" / "thin-prompt.md"),
        str(HANDOVER / "R6R7_COMPILED_OUT" / "compiler-receipt.json"),
        str(HANDOVER / "OWNER_TRUST_LOCK.json"),
        str(HANDOVER / "R6_HANDOVER_STATE_R2.json"),
    ]


def main() -> int:
    sources, present, missing, inv = build_sources(), [], [], []
    for raw in sources:
        p = Path(raw)
        if p.exists() and p.is_file():
            b = p.read_bytes()
            present.append(raw)
            inv.append({"path": raw, "bytes": len(b), "sha256": sha256_bytes(b)})
        else:
            missing.append(raw)

    report = {
        "schema": "CNV-PIPD-LS-SP-20261015/HGK-TYPED-ADMISSION/R6R7",
        "project_id": PROJECT_ID,
        "changeset": "NARROW_REPAIR",
        "sources_present": len(present),
        "sources_missing": missing,
        "source_inventory": inv,
        "steps": [],
        "claim_ceiling": "LOCAL_ORCHESTRATION",
    }
    out = HANDOVER / "HGK_TYPED_ADMISSION_R6R7.json"
    if missing:
        report["verdict"] = "BLOCKED_SOURCE_MISSING"
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"verdict": "BLOCKED_SOURCE_MISSING", "missing": missing}, ensure_ascii=False))
        return 2

    spine = spine_for(Path(ROOT))
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=GOAL, source_paths=present, constraints=CONSTRAINTS,
                         non_goals=NON_GOALS, target_root=TARGET_ROOT)
    try:
        st = lc.status(PROJECT_ID)
        report["steps"].append({"step": "start", "result": "ALREADY_EXISTS", "state": st["state"]})
    except Exception:
        st = lc.start(req, project_id=PROJECT_ID)
        report["steps"].append({"step": "start", "result": "CREATED", "state": st["state"]})

    if lc.status(PROJECT_ID)["state"] == "PROJECT_CREATED":
        env = lc.intake(PROJECT_ID, req)
        report["steps"].append({"step": "intake", "status": env["status"],
                                "source_count": env["source_count"],
                                "blocking_missing": env["blocking_missing"],
                                "conflicts": env["conflicts"]})
        if env["status"] != "READY":
            report["verdict"] = "BLOCKED_INTAKE"
            out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"verdict": "BLOCKED_INTAKE", "blocking_missing": env["blocking_missing"]},
                             ensure_ascii=False))
            return 3

    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R6R7"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R6R7"),
                           ("DESIGN_READY", "DESIGN_READY_R6R7")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            report["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            report["steps"].append({"step": "transition", "to": to_state, "result": f"SKIPPED_FROM_{cur}"})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig,
                      evidence_refs=["C0_C9_CONTRACT_R6R7.json", "R6R7_COMPILED_OUT/thin-prompt.md"])
        report["steps"].append({"step": "transition", "to": to_state, "result": "OK"})

    if lc.status(PROJECT_ID)["state"] == "DESIGN_READY":
        pl = lc.plan(PROJECT_ID)
        report["steps"].append({"step": "plan", "task_count": pl["task_count"],
                                "titles": [s["title"] for s in pl["plan"]],
                                "non_goals_preserved": pl["non_goals_preserved"]})
    if lc.status(PROJECT_ID)["state"] == "PLAN_READY":
        report["steps"].append({"step": "admit_workorders", "result": lc.admit_workorders(PROJECT_ID)})

    report["final_state"] = lc.status(PROJECT_ID)["state"]
    try:
        report["denominator"] = lc.denominator(PROJECT_ID)
    except Exception as exc:  # noqa: BLE001
        report["denominator_error"] = f"{type(exc).__name__}: {exc}"
    report["verdict"] = ("ADMISSION_OK" if report["final_state"] in ("WORKORDERS_ADMITTED", "EXECUTING")
                         else f"ADMISSION_STATE_{report['final_state']}")
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "final_state": report["final_state"],
                      "sources": len(present)}, ensure_ascii=False))
    return 0 if report["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
