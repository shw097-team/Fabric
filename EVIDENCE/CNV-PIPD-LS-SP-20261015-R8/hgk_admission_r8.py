"""HGK typed admission for ChangeSet R8-0 (skill-slim regression+apply, stale-baseline closure, EIA closure).

Mission: CNV-PIPD-LS-SP-20261015   ChangeSet: R8-0-SKILL-SLIM-REGRESSION-AND-EIA-CLOSURE
New project id (own requirement/taskspec/workorder lineage); R6/R6R7/R7VH projects are left untouched.
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

H8 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8")
H7 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R7")
SKCV = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014")
ATTACH = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
PROJECT_ID = "CNV-R8-SKILL-SLIM-EIA-CLOSURE"
TARGET_ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"

GOAL = (
    "依《Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG》v2.0.0、《Fabric_HG-KSEOS_Convergence_指揮薄PROMPT》與外部驗收報告"
    "EIA-FABRIC-CONVERGENCE-R6-20261015 的 finding register，執行有界 R8-0："
    "(a) 對前回合 SKILL-CONVERGENCE-20261014 產出的『瘦身技能候選』做回歸檢測（容量上限、references 覆蓋、"
    "loader 可載入性、內容無損負例、既有 consumer 複用）並在受治理 guarded apply 下落套用；"
    "(b) 關閉 BLK-R7-WS1-STALE-BASELINE：把 R7-0 validator 硬化在 main 上重建，並在該樹重測 18 變異"
    "（M04/M06/M16 必 REJECT、既有 7 detected 維持、8 NOT_RUN 之適用性逐項判定）；"
    "(c) 產生 checker 寫入根的 OS 層 denial 證據（對應 EIA-R6-03）；"
    "(d) 逐筆對 EIA-R6-01..09 以其反例重測現況並出具 disposition；"
    "(e) 發布 R8 evidence packet 至 Fabric repo 供外部驗收官再次驗收。"
)
CONSTRAINTS = [
    "不得改寫已合併的 EVIDENCE/CNV-PIPD-LS-SP-20261015/**（byte-bound）與 EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/** 既有提交。",
    "不得自驗收、不得自我晉升裁決；maker ≠ checker ≠ AO。",
    "不得宣稱任何 Gate PASS、不得執行 221 cases、不得宣稱 Product/Production。",
    "不得建立第二控制平面、第二 DB 或長駐 CI。",
    "憑證一律不得進入 argv／URL／log／artifact；只以本機非 LLM credential helper 路徑使用。",
    "canonical 寫入（HG-KSEOS 控制面、Hermes skills 樹）須走 guarded apply：pre-image 備份、receipt、rollback，且不得就地覆蓋無備份。",
]
NON_GOALS = [
    "Fresh G1 重認證、DOC-05 effect admission、Owner/AO/Release 授權（人力閘門）。",
    "24 AUD 全量閉合與 8 Gates 全數 PASS（需授權與 runtime effect，本輪只做可及之最小項目）。",
    "重寫控制平面、重建 Stage-2/Stage-3、任何 production/live/trade 行為。",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    H8.mkdir(parents=True, exist_ok=True)
    srcs = [
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"),
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_指揮薄PROMPT.md"),
        str(ATTACH / "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md"),
        str(HG := Path("C:/Projects/Agent_Workspace/HG-KSEOS/AGENTS.md")),
        str(SKCV / "evidence/postfreeze/SESSION_CLOSURE.md"),
        str(SKCV / "_CHECKPOINT_RESUME.md"),
        str(SKCV / "candidates/avr/skill/SKILL.md"),
        str(SKCV / "candidates/apply/patch/lane-dispatch-timeout-capture.patch"),
        str(SKCV / "candidates/hgk/phase2_result.json"),
    ]
    present, missing, inv = [], [], []
    for s in srcs:
        p = Path(s)
        if p.is_file():
            present.append(s)
            inv.append({"path": s, "bytes": p.stat().st_size, "sha256": sha(p)})
        else:
            missing.append(s)
    out = H8 / "HGK_TYPED_ADMISSION_R8.json"
    rep = {"schema": "CNV-PIPD-LS-SP-20261015-R8/HGK-TYPED-ADMISSION/1", "project_id": PROJECT_ID,
           "changeset": "R8-0-SKILL-SLIM-REGRESSION-AND-EIA-CLOSURE", "sources_present": len(present),
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
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R8"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R8"),
                           ("DESIGN_READY", "DESIGN_READY_R8")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": f"SKIPPED_FROM_{cur}"})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig, evidence_refs=["PKG:v2.0.0", "EIA:R6"])
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
                      "workorders": (rep["steps"][-1].get("result") or {}) if rep["steps"] else None},
                     ensure_ascii=False))
    return 0 if rep["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
