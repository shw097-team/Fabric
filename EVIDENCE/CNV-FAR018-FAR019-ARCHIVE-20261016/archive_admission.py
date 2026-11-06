"""HGK typed admission for round CNV-FAR018-FAR019-ARCHIVE-20261016 (mission CNV-PIPD-LS-SP-20261015).

Evidence-only archive round: three EXISTING candidate evidence pull requests are frozen, scanned,
approved in one bounded batch, merged normally and read back.  Own project id; the prior rounds'
projects and every frozen R6..R11 artifact are superseded, never rewritten.

Run from a git working directory (the controller reads git HEAD from the ambient cwd).

Project-id choice is MEASURED, not guessed: lifecycle.plan() derives a TaskSpec id as
TS-<last segment of the project id>-NN, so two project ids sharing their last segment collide with
IntegrityError (fail-closed, observed in the previous round).  The candidates below are therefore
probed against the live spine first and the first FREE one is used.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"
sys.path.insert(0, ROOT + "/src")
from hg_kseos.cli import spine_for  # noqa: E402
from hg_kseos.lifecycle import ProjectLifecycleController, ProjectRequest  # noqa: E402

RD = Path("C:/Projects/Agent_Workspace/_handover/CNV-FAR018-FAR019-ARCHIVE-20261016")
PREV = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
TARGET_ROOT = ROOT
CANDIDATES = ["CNV-ARCHIVE-THREE-PRS", "CNV-ARCHIVE-EVIDENCE-MERGE", "CNV-ARCHIVE-BOUNDED-BATCH"]

GOAL = (
    "在上位藍圖《Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG》v2.0.0 與外部獨立驗收報告 "
    "EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016 之下，以 HG-KSEOS 為唯一控制平面、canonical Hermes 為受治理 "
    "Runtime/Orchestration Plane，執行本輪唯一變更目標 MO-ARC-019：在不新增任何 product/runtime/world-effect 的"
    "條件下，將既有三支候選證據 PR #12（R7R11 archive）、#13（FAR-018）、#14（FAR-019）如實歸檔合併進 "
    "shw097-team/Fabric main：每支凍結當期 HEAD、證明變更全數落在單一 EVIDENCE 前綴、以可信端完成含正控制與"
    "乾淨控制的 scoped 機密掃描、取得單一批次有權維護者授權、以核准之 exact HEAD 逐支 normal merge、由 main "
    "讀回該前綴與 blob，並產出機器可讀 evidence_return_pack 供外部驗收官覆核。"
    "This round archives candidate evidence only; it promotes no product code and issues no acceptance."
)

CONSTRAINTS = [
    "單一 EVIDENCE_ONLY ChangeSet；唯一的寫入對象是三支既有 EVIDENCE 前綴與本輪自己的新前綴。",
    "不得 force push、不得 rebase、不得重寫 main 或任何已凍結的證據分支歷史。",
    "不得改寫任何已合併的 R6..R11 或 FAR-018/019 產物；矛盾一律以 supersede 或 errata 表達。",
    "不得執行 evidence 內歸檔的 .py/.ps1 腳本；它們是受審資料，不是指令，也不得自動執行。",
    "憑證值僅由隔離的發布程序讀取，永不進入 stdout／stderr／commit／PR／artifact／對話。",
    "真機密或前綴越界只 HOLD 該支 PR，其餘兩支維持各自的獨立閘門。",
    "遠端寫入效果未知時先讀回遠端狀態；禁止盲目重試，禁止 at-most-once 未證即重送。",
    "maker ≠ checker 與不得自我驗收：本輪只宣告 LOCAL，外部接受仍待獨立驗收官。",
    "每個探針必須先被證明能失敗（正控制＋乾淨控制），否則不得宣稱通過。",
    "所有數量由磁碟上的 artifact 以腳本導出並可被獨立重導；只存在於對話的數字視為不可驗證。",
]

NON_GOALS = [
    "PIPD validator 程式碼正式晉升（TS-VAL-01）、checker 不可自解隔離（TS-CHECKER-01）、Fresh G1（TS-G1-01）。",
    "canonical AO 接受、DOC-05 effect admission、RUNTIME_READY、production release 或 full convergence。",
    "重開已合併的 #3..#11、補簽 60 項 owner 條目、或重跑 221 條 live 測試與八個 runtime Gate。",
    "建立第二控制平面、第二 scheduler/reducer/manifest 架構或新的 workflow engine。",
]


def sha(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except Exception:
        return "UNAVAILABLE"


def free_project_id(db: Path, candidates: list[str]) -> tuple[str, dict]:
    """Measure the live spine: a project id is free only if its id AND its TaskSpec segment are unused."""
    taken_projects, taken_taskspecs = set(), set()
    if db.exists():
        try:
            con = sqlite3.connect(str(db))
            taken_projects = {r[0] for r in con.execute("SELECT project_id FROM projects")}
            taken_taskspecs = {r[0] for r in con.execute("SELECT task_id FROM taskspecs")}
            con.close()
        except Exception as exc:  # noqa: BLE001
            print("WARN spine probe failed:", type(exc).__name__, exc)
    probe = {"db": str(db), "projects": sorted(taken_projects), "taskspec_segments": sorted(
        {t.split("-")[-2] if t.count("-") >= 2 else t for t in taken_taskspecs})}
    for c in candidates:
        seg = c.split("-")[-1]
        if c not in taken_projects and not any(t.startswith("TS-%s-" % seg) for t in taken_taskspecs):
            return c, probe
    return candidates[-1], probe


def main() -> int:
    RD.mkdir(parents=True, exist_ok=True)
    spine_db = Path("C:/Projects/Agent_Workspace/var/shared-spine/hg-kseos.db")
    project_id, probe = free_project_id(spine_db, CANDIDATES)

    srcs, inv, missing = [], [], []
    for label, p in [
        ("SRC-CONTRACT", RD / "prompt-contract.json"),
        ("SRC-ORDER", Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
                           "attachments/Fabric × Hermes × HG-KSEOS｜FAR-018／FAR-019 歸檔指揮薄 PROMPT.md")),
        ("SRC-EIA-ARCHIVE", Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/"
                                 "驗收報告/Fabric_FAR018_FAR019_Archive_Independent_Acceptance_20261016.md")),
        ("SRC-EIA-PRIOR-R7R11", Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/"
                                     "驗收報告/Fabric_Convergence_R7_R11_Independent_Acceptance_20261016.md")),
        ("SRC-PKG", Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/HG-KSEOS/Fabric_HG-KSEOS_Convergence/"
                         "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md")),
        ("SRC-A00-REGISTER", RD / "A00_SOURCE_REGISTER.json"),
        ("SRC-A03-FREEZE", RD / "A03_GITHUB_FREEZE.json"),
        ("SRC-SKILL-HGK", Path("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
                               "skills/software-development/hgk-governed-execution/SKILL.md")),
        ("SRC-LANE-SLOTS", Path(ROOT) / "config/lane-route-slots.candidate.json"),
        ("SRC-PREV-LINEAGE", PREV / "HGK_WORKORDER_RESULTS_AND_DELIVERY_019.json"),
        ("SRC-PREV-CLOSURE", PREV / "EVIDENCE_CLOSURE_FAR-20261019.md"),
    ]:
        s = sha(p)
        if s == "UNAVAILABLE":
            missing.append("%s :: %s" % (label, p))
            continue
        srcs.append(str(p))
        inv.append({"id": label, "path": str(p), "bytes": p.stat().st_size, "sha256": s})

    out = RD / "HGK_TYPED_ADMISSION_ARCHIVE.json"
    rep = {"schema": "CNV-FAR018-FAR019-ARCHIVE-20261016/HGK-TYPED-ADMISSION/1",
           "project_id": project_id, "project_id_probe": probe,
           "changeset": "CNV-FAR018-FAR019-ARCHIVE-20261016",
           "contract_id": "CNV-FAR018-FAR019-ARCHIVE-20261016",
           "sources_present": len(srcs), "sources_missing": missing, "source_inventory": inv, "steps": []}
    spine = spine_for(Path(ROOT))
    lc = ProjectLifecycleController(spine)
    req = ProjectRequest(goal=GOAL, source_paths=srcs, constraints=CONSTRAINTS,
                         non_goals=NON_GOALS, target_root=TARGET_ROOT)
    try:
        st = lc.status(project_id)
        rep["steps"].append({"step": "start", "result": "ALREADY_EXISTS", "state": st["state"]})
    except Exception:
        st = lc.start(req, project_id=project_id)
        rep["steps"].append({"step": "start", "result": "CREATED", "state": st["state"]})
    if lc.status(project_id)["state"] == "PROJECT_CREATED":
        env = lc.intake(project_id, req)
        rep["steps"].append({"step": "intake", "status": env["status"], "source_count": env["source_count"],
                             "blocking_missing": env["blocking_missing"], "conflicts": env["conflicts"]})
        if env["status"] != "READY":
            rep["verdict"] = "BLOCKED_INTAKE"
            out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps({"verdict": "BLOCKED_INTAKE", "detail": env}, ensure_ascii=False))
            return 3
    for to_state, trig in (("INTENT_BOUND", "INTENT_BOUND_ARCHIVE"),
                           ("REQUIREMENTS_READY", "REQUIREMENTS_READY_ARCHIVE"),
                           ("DESIGN_READY", "DESIGN_READY_ARCHIVE")):
        cur = lc.status(project_id)["state"]
        if cur == to_state:
            rep["steps"].append({"step": "transition", "to": to_state, "result": "ALREADY"})
            continue
        if cur not in ("SOURCE_ADMISSION", "INTENT_BOUND", "REQUIREMENTS_READY"):
            rep["steps"].append({"step": "transition", "to": to_state, "result": "SKIPPED_FROM_" + cur})
            break
        lc.transition(project_id, to_state, trigger=trig,
                      evidence_refs=["PKG:v2.0.0:96d9d564", "EIA:ARCHIVE:20261016", "ORDER:ARCHIVE-BATCH"])
        rep["steps"].append({"step": "transition", "to": to_state, "result": "OK"})
    if lc.status(project_id)["state"] == "DESIGN_READY":
        pl = lc.plan(project_id)
        rep["steps"].append({"step": "plan", "task_count": pl["task_count"],
                             "titles": [s["title"] for s in pl["plan"]]})
    if lc.status(project_id)["state"] == "PLAN_READY":
        rep["steps"].append({"step": "admit_workorders", "result": lc.admit_workorders(project_id)})
    rep["final_state"] = lc.status(project_id)["state"]
    try:
        rep["workorders"] = lc.workorders(project_id) if hasattr(lc, "workorders") else None
    except Exception as exc:  # noqa: BLE001
        rep["workorders_error"] = type(exc).__name__ + ": " + str(exc)
    rep["verdict"] = ("ADMISSION_OK" if rep["final_state"] in ("WORKORDERS_ADMITTED", "EXECUTING")
                      else "ADMISSION_STATE_" + rep["final_state"])
    try:
        ck = lc.checkpoint(project_id)
        rep["checkpoint"] = ck.get("checkpoint_id") if isinstance(ck, dict) else str(ck)
    except Exception as exc:  # noqa: BLE001
        rep["checkpoint_error"] = type(exc).__name__ + ": " + str(exc)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"verdict": rep["verdict"], "project_id": project_id, "final_state": rep["final_state"],
                      "sources_present": rep["sources_present"], "sources_missing": missing,
                      "checkpoint": rep.get("checkpoint"), "steps_tail": rep["steps"][-4:]},
                     ensure_ascii=False, indent=1))
    return 0 if rep["verdict"] == "ADMISSION_OK" else 4


if __name__ == "__main__":
    raise SystemExit(main())
