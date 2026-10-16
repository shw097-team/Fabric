"""HGK typed admission for ChangeSet R11-0 (complete SESSION closure + handover so a NEW session can continue).

Mission: CNV-PIPD-LS-SP-20261015   ChangeSet: R11-0-SESSION-HANDOVER
Own project id (own requirement/taskspec/workorder lineage); R6..R10 projects untouched.
The last dash segment is UNIQUE by construction: plan() derives taskspec ids as TS-<last segment>-NN.
Successor of hgk_admission_r10.py; the predecessor is left byte-unchanged.
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

R11 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R11")
R10 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R10")
R9 = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9")
FAB = Path("C:/Projects/Agent_Workspace/Fabric")
FAR = FAB / "fabric-autonomous-research" / "runs"
ATTACH = Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/attachments")
OPENSPEC = Path(ROOT) / "openspec" / "changes"

PROJECT_ID = "CNV-R11-HANDOVER"
TARGET_ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"

GOAL = (
    "依《Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG》v2.0.0 唯一權威錨點，對本 SESSION 做完整結案與移交，"
    "使用戶可開新 SESSION 續作未完任務：(a) 以 FAR 研究「本 SESSION 結案／移交相關事項」，提出低阻力、"
    "高可行、高工程必要性、不過度工程化、對齊 PKG 的裁決並直接執行；(b) 產出單一入口的狀態交接"
    "（resume 用），列出全部未竟治理紀錄與其可量測狀態、owner、單一動作續作路徑與阻擋項；"
    "(c) 保留受守護主體與既有 R6..R10 封包零回退；(d) 將本 SESSION 實作與證據推送 Fabric 供外部驗收官驗收。"
)

CONSTRAINTS = [
    "不得改寫已合併／已發布的 EVIDENCE/CNV-PIPD-LS-SP-20261015/**、-R7/**、-R8/**、-R9/**、-R10/** 既有提交。",
    "不得自我驗收、不得自我晉升裁決；maker ≠ checker ≠ AO；本輪命令將 checker 與 EXECUTE 指向同一 arm，"
    "模型軸獨立性 ABSENT，須如實記錄。",
    "不得宣稱任何 Gate PASS、不得執行 221 cases、不得宣稱 Product/Production 或任何上市決定。",
    "不得建立第二控制平面、第二 DB 或長駐 CI；不得自改 canonical lane registry（僅發出 owner-ready 決策紀錄）。",
    "憑證一律不得進入 argv／URL／log／artifact；不得讀取或列印憑證值。",
    "同儕在飛回合為唯讀；不得切換、清理或覆寫其 checkout 與未追蹤產物。",
    "受守護主體 _handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/ 全程 hands-off（本輪寫入根一律在主體外）。",
]
NON_GOALS = [
    "Fresh G1 重認證、DOC-05 effect admission、Owner/AO/Release 授權（人力門檻）。",
    "221 cases、8 Gates 全數 PASS、AUD 全量閉合。",
    "重寫控制平面、Stage-2/3 重建、任何 production/live/trade 行為。",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    R11.mkdir(parents=True, exist_ok=True)
    srcs = [
        str(ATTACH / "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md"),
        str(ATTACH / "Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md"),
        str(Path(ROOT) / "AGENTS.md"),
        str(R10 / "HANDOVER_R10.md"),
        str(R10 / "SESSION_LEDGER_R10.json"),
        str(R10 / "R10_CHANGE_RECORD_ADJUDICATION.json"),
        str(R10 / "SELF_EVOLUTION_R10.json"),
        str(R10 / "R10_OWNER_READY_LANE_REBIND.json"),
        str(R10 / "R10_VERIFY" / "R10_VERDICT.json"),
        str(R10 / "R10_VERIFY" / "R10_VERDICT_ADJUDICATION.json"),
        str(R9 / "R9_LEDGER.json"),
        str(R9 / "R9_VERIFY" / "R9_VERDICT_ADJUDICATION.json"),
        str(FAR / "FAR-20261016-015-r10-session-closure" / "ResearchRunReceipt.json"),
        str(FAR / "FAR-20261016-015-r10-session-closure" / "OpenQuestionLedger.tsv"),
        str(OPENSPEC / "hgk-far-remediation-20261016" / "tasks.md"),
        str(OPENSPEC / "skill-mainfile-cap-remediation" / "tasks.md"),
        str(OPENSPEC / "hgk-r10-session-closure-20261016" / "tasks.md"),
        str(OPENSPEC / "hgk-lane-reliability-closure-20261016" / "tasks.md"),
    ]
    present, missing, inv = [], [], []
    for s in srcs:
        p = Path(s)
        if p.is_file():
            present.append(s)
            inv.append({"path": s, "bytes": p.stat().st_size, "sha256": sha(p)})
        else:
            missing.append(s)
    out = R11 / "HGK_TYPED_ADMISSION_R11.json"
    rep = {"schema": "CNV-PIPD-LS-SP-20261015-R11/HGK-TYPED-ADMISSION/1", "project_id": PROJECT_ID,
           "changeset": "R11-0-SESSION-HANDOVER", "sources_present": len(present),
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
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_R11"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_R11"),
                           ("DESIGN_READY", "DESIGN_READY_R11")):
        cur = lc.status(PROJECT_ID)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": "SKIPPED_FROM_" + cur})
            break
        lc.transition(PROJECT_ID, to_state, trigger=trig, evidence_refs=["PKG:v2.0.0", "EIA:R6", "FAR:run-015"])
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
