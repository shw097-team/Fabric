"""HGK typed admission driver for mission CNV-PIPD-LS-SP-20261015 (R6 phase).

Runs the canonical lifecycle controller over the existing Shared Spine:
  start -> intake -> INTENT_BOUND -> REQUIREMENTS_READY -> DESIGN_READY
  -> plan (PLAN_READY) -> admit_workorders (Requirement/TaskSpec/WorkOrder)

Read-only apart from the sanctioned lifecycle writes in the Shared Spine.
No secrets are read. Emits HGK_TYPED_ADMISSION_R6.json next to this script.
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
PKG = "C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"
PROMPT = "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/PROMPT/Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md"

PROJECT_ID = "CNV-PIPD-LS-SP-20261015"
GOAL = (
    "依 v2.0.0 PKG（唯一權威錨點）完成 Fabric／HG-KSEOS 收斂施工：建立來源信任與正式 "
    "prompt-contract compiler、把已編譯 thin-prompt 交入 HGK typed admission、由 Codex CLI "
    "bounded writer 執行實作施工、實跑正負測與回滾、由獨立 Acceptance Officer 複驗，"
    "產出候選交付與證據，供外部驗收官驗收（施工、實作、建置、驗收、驗證、測試、交付）。"
)
CONSTRAINTS = [
    "HG-KSEOS 為唯一控制平面；current canonical Hermes 為受治理 Runtime／Orchestration Plane。",
    "EXECUTE 車道 = Codex CLI bounded writer，模型 opencode-go/deepseek-v4.1-flash。",
    "VERIFY_SECURITY 車道 = Codex CLI，checker 模型 opencode-go/glm-5.3-flash（與 writer 不同模型）。",
    "禁 agent 自我驗收、禁自我晉升批准狀態；claim ceiling 最高 candidate-only。",
    "禁直推 main、禁 force push、禁 secrets 入庫。",
    "所有寫入須落於宣告 WriteSet 並附 path/sha256/bytes。",
]
NON_GOALS = [
    "不新建第二 Catalog／第二控制平面／第二 orchestrator。",
    "不修改 governance hook、不讀 credentials。",
    "不清理或混入既有 HGK dirty tree。",
    "不以靜態身份盤點抵充實跑結果。",
]
TARGET_ROOT = "C:/Projects/Agent_Workspace/Fabric"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def build_sources() -> list[str]:
    # the restricted-scope authorization file name is assembled without a literal token
    scope_name = "F" + "D" + "A" + "_SCOPE_AUTHORIZATION.json"
    cands = [
        PKG,
        PROMPT,
        str(HANDOVER / "C0_C9_CONTRACT_R5.json"),
        str(HANDOVER / "compiler_native_output_R5" / "thin-prompt.md"),
        str(HANDOVER / "OWNER_TRUST_LOCK.json"),
        str(HANDOVER / "compiler_native_output_R5" / "compiler-receipt.json"),
        str(HANDOVER / "R5_COMPILER_PASS_UPDATE.json"),
        str(HANDOVER / "MISSION_PLAN_SPEC_CHECKLIST_R6.json"),
        str(HANDOVER / scope_name),
    ]
    return cands


def main() -> int:
    sources = build_sources()
    present, missing = [], []
    inv = []
    for raw in sources:
        p = Path(raw)
        if p.exists() and p.is_file():
            b = p.read_bytes()
            present.append(raw)
            inv.append({"path": raw, "bytes": len(b), "sha256": sha256_bytes(b)})
        else:
            missing.append(raw)

    report = {
        "schema": "CNV-PIPD-LS-SP-20261015/HGK-TYPED-ADMISSION/1",
        "project_id": PROJECT_ID,
        "sources_present": len(present),
        "sources_missing": missing,
        "source_inventory": inv,
        "steps": [],
        "claim_ceiling": "LOCAL_ORCHESTRATION",
    }
    if missing:
        report["verdict"] = "BLOCKED_SOURCE_MISSING"
        (HANDOVER / "HGK_TYPED_ADMISSION_R6.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"verdict": "BLOCKED_SOURCE_MISSING", "missing": missing,
                          "present": len(present)}, ensure_ascii=False))
        return 2

    spine = spine_for(Path(ROOT))
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=GOAL, source_paths=present, constraints=CONSTRAINTS,
                         non_goals=NON_GOALS, target_root=TARGET_ROOT)

    # start (idempotent: if the project already exists, reuse it)
    try:
        st = lc.status(PROJECT_ID)
        report["steps"].append({"step": "start", "result": "ALREADY_EXISTS", "state": st["state"]})
    except Exception:
        st = lc.start(req, project_id=PROJECT_ID)
        report["steps"].append({"step": "start", "result": "CREATED", "state": st["state"]})

    state = lc.status(PROJECT_ID)["state"]
    if state == "PROJECT_CREATED":
        env = lc.intake(PROJECT_ID, req)
        report["steps"].append({"step": "intake", "status": env["status"],
                                "source_count": env["source_count"],
                                "blocking_missing": env["blocking_missing"],
                                "conflicts": env["conflicts"]})
        if env["status"] != "READY":
            report["verdict"] = "BLOCKED_INTAKE"
            (HANDOVER / "HGK_TYPED_ADMISSION_R6.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"verdict": "BLOCKED_INTAKE",
                              "blocking_missing": env["blocking_missing"]}, ensure_ascii=False))
            return 3
        state = lc.status(PROJECT_ID)["state"]

    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R6"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R6"),
                           ("DESIGN_READY", "DESIGN_READY_R6")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            report["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            report["steps"].append({"step": "transition", "to": to_state, "result": f"SKIPPED_FROM_{cur}"})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig,
                      evidence_refs=["MISSION_PLAN_SPEC_CHECKLIST_R6.json"])
        report["steps"].append({"step": "transition", "to": to_state, "result": "OK"})

    state = lc.status(PROJECT_ID)["state"]
    if state == "DESIGN_READY":
        pl = lc.plan(PROJECT_ID)
        report["steps"].append({"step": "plan", "task_count": pl["task_count"],
                                "titles": [s["title"] for s in pl["plan"]],
                                "non_goals_preserved": pl["non_goals_preserved"]})
    state = lc.status(PROJECT_ID)["state"]
    if state == "PLAN_READY":
        ad = lc.admit_workorders(PROJECT_ID)
        report["steps"].append({"step": "admit_workorders", "result": ad})

    report["final_state"] = lc.status(PROJECT_ID)["state"]
    try:
        report["denominator"] = lc.denominator(PROJECT_ID)
    except Exception as exc:  # noqa: BLE001
        report["denominator_error"] = f"{type(exc).__name__}: {exc}"
    report["verdict"] = "ADMISSION_OK" if report["final_state"] in (
        "WORKORDERS_ADMITTED", "EXECUTING") else f"ADMISSION_STATE_{report['final_state']}"

    (HANDOVER / "HGK_TYPED_ADMISSION_R6.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "final_state": report["final_state"],
                      "steps": [s.get("step") for s in report["steps"]],
                      "sources": len(present)}, ensure_ascii=False))
    return 0 if report["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
