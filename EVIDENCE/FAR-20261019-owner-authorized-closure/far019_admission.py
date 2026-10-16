"""HGK typed admission for FAR round FAR-20261016-018 (continuation of mission CNV-PIPD-LS-SP-20261015).

Own project id; the previous round's project (CNV-EA-R7R11) and R6..R11 are superseded, never rewritten.
Run from a git working directory (the controller reads git HEAD from the ambient cwd).
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

RD = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
PREV = Path("C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016")
PROJECT_ID = "FAR-019-OWNER-AUTH"
TARGET_ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"

GOAL = (
    "在上位藍圖《Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG》v2.0.0 與外部驗收報告 "
    "EIA-FABRIC-CNV-R7-R11-20261016 之下，以 HG-KSEOS 為唯一控制平面、canonical Hermes 為受治理 Runtime/"
    "Orchestration Plane，執行 FAR 研究輪 FAR-20261016-018：對 R7～R11 證據歸檔輪遺留的全部「殘留／缺口／"
    "阻斷項目、待 OWNER 決策項目、候選未落地實用資產（含 SKILLS）、本 SESSION 結案與移交事項」提出唯一一份"
    "排名工程裁決（低阻力、高可行、高工程必要性、不過度工程化、對齊上位藍圖與驗收報告），並因 OWNER 已預先"
    "授權而直接執行裁決中 agent 可執行之項目，OWNER-gated 項目僅以單一動作形式備妥；證據推送目標 REPO 供外部"
    "驗收官驗收。"
)

CONSTRAINTS = [
    "單一 EVIDENCE_ONLY ChangeSet；僅新增 EVIDENCE/FAR-20261016-018-*/ 前綴，不得改寫任何既有證據。",
    "不得 force push、不得直寫 main、不得重寫已合併歷史、不得合併任何 PR 或晉升 Draft。",
    "不得編輯 canonical 控制平面檔（lane registry／route slots／hermes-codex-lane.json 等）；registry 只讀。",
    "不得執行任何 evidence 內的 .py/.ps1 歸檔腳本；不得以同包自算 hash 假裝 trusted source。",
    "maker ≠ checker：EXECUTE 與 VERIFY_SECURITY 必須不同模型軸，checker 需 --require-arm pin 至非 writer 的 arm。",
    "不得自我驗收、不得自我晉升；僅能宣告 LOCAL 層級完成，外部接受仍待真實驗收官。",
    "憑證值僅由本地 broker 程序讀取，永不進入 argv／URL／log／artifact／prompt。",
    "每個探針必須先被證明能失敗（正控制＋負控制），否則不得宣稱通過。",
    "所有數量必須由磁碟上的 artifact 以腳本導出並可被獨立車道重導；只存在於對話的數字視為不可驗證。",
]

GOAL = GOAL + (" This round is FAR-20261019-owner-authorized-closure and rests on the sole Fabric and "
              "HG-KSEOS owner's authorisation, given in this session, to execute this round's ruling "
              "directly over every residual, blocked, unclosed and owner-decision item.")

NON_GOALS = [
    "full convergence 221 cases／G-A～H、production 晉升、RUNTIME_READY 或任何上市宣告。",
    "R7-02 validator 程式碼跨 REPO 晉升、peer chain #6/#8/#10 合併、PR #12 轉 Ready/Merged。",
    "Fresh G1 owner 認證、DOC-05 effect admission、AO 或 Release Owner 授權。",
    "重新瘦身兩支已瘦身 skills、或把 reference 數量的 soft warning 當硬門檻。",
    "建立第二控制平面、第二 scheduler/reducer/DB 或新的 virtualization/verifier 系統。",
]


def sha(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except Exception:
        return "UNAVAILABLE"


def main() -> int:
    RD.mkdir(parents=True, exist_ok=True)
    srcs, inv, missing = [], [], []
    for label, p in [
        ("SRC-PKG", Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/"
                         "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")),
        ("SRC-EIA-R7R11", Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/"
                               "hermes/attachments/Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md")),
        ("SRC-PREV-RETURN-PACK", PREV / "packet/RETURN_PACK.json"),
        ("SRC-PREV-PREFLIGHT", PREV / "A03_A05_PR_PREFLIGHT.json"),
        ("SRC-PREV-ERRATA", PREV / "ERRATA_AND_ADVISORIES.json"),
        ("SRC-PREV-MERGE-CHAIN", PREV / "MERGE_CHAIN_RECEIPT.json"),
        ("SRC-PREV-SELF-CHECK", PREV / "SELF_CHECK_RECEIPT.json"),
        ("SRC-FAR018-RULING", Path("C:/Projects/Agent_Workspace/_handover/"
            "FAR-20261016-018-r7r11-residual-closure-and-handover/FAR_RULING.md")),
        ("SRC-FAR018-REGISTER", Path("C:/Projects/Agent_Workspace/_handover/"
            "FAR-20261016-018-r7r11-residual-closure-and-handover/RESIDUAL_REGISTER.json")),
        ("SRC-FAR018-ADJUDICATION", Path("C:/Projects/Agent_Workspace/_handover/"
            "FAR-20261016-018-r7r11-residual-closure-and-handover/ADJUDICATION_AND_LIMITATIONS.json")),
        ("SRC-FAR018-LINEAGE", Path("C:/Projects/Agent_Workspace/_handover/"
            "FAR-20261016-018-r7r11-residual-closure-and-handover/HGK_WORKORDER_RESULTS_AND_DELIVERY.json")),
        ("SRC-FAR-CONTRACT", RD / "prompt-contract.json"),
        ("SRC-FAR-DECISION-QUESTION", Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/"
                                           "FAR-20261019-owner-authorized-closure/"
                                           "DECISION_QUESTION.md")),
        ("SRC-FAR-METHOD", Path("C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/"
                                "FAR-20261019-owner-authorized-closure/METHOD.md")),
        ("SRC-SKILL-HGK", Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/"
                               "hermes/skills/software-development/hgk-governed-execution/SKILL.md")),
        ("SRC-LANE-SLOTS", Path(ROOT) / "config/lane-route-slots.candidate.json"),
    ]:
        s = sha(p)
        if s == "UNAVAILABLE":
            missing.append({"id": label, "locator": str(p), "status": "MISSING"})
            continue
        srcs.append(str(p))
        inv.append({"id": label, "path": str(p), "bytes": p.stat().st_size, "sha256": s})

    out = RD / "HGK_TYPED_ADMISSION_FAR018.json"
    rep = {"schema": "FAR-20261016-018/HGK-TYPED-ADMISSION/1", "project_id": PROJECT_ID,
           "changeset": "FAR-20261019-owner-authorized-closure",
           "contract_id": "FAR-20261019-owner-authorized-closure",
           "sources_present": len(srcs), "sources_missing": missing, "source_inventory": inv, "steps": []}
    spine = spine_for(Path(ROOT))
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=GOAL, source_paths=srcs, constraints=CONSTRAINTS,
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
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_FAR018"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_FAR018"),
                           ("DESIGN_READY", "DESIGN_READY_FAR018")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": "SKIPPED_FROM_" + cur})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig,
                      evidence_refs=["PKG:v2.0.0:96d9d564", "EIA:R7R11:20261016", "FAR:RUN-018"])
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
    try:
        ck = lc.checkpoint(PROJECT_ID)
        rep["checkpoint"] = ck.get("checkpoint_id") if isinstance(ck, dict) else str(ck)
    except Exception as exc:  # noqa: BLE001
        rep["checkpoint_error"] = type(exc).__name__ + ": " + str(exc)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": rep["verdict"], "final_state": rep["final_state"], "project_id": PROJECT_ID,
                      "sources_present": rep["sources_present"], "sources_missing": missing,
                      "checkpoint": rep.get("checkpoint"), "steps_tail": rep["steps"][-4:]},
                     ensure_ascii=False, indent=1))
    return 0 if rep["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
