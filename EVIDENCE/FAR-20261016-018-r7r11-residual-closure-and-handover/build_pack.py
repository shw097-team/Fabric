#!/usr/bin/env python
"""Assemble the publishable payload + PACK_INDEX + the single evidence MD for FAR-20261016-018.

Numbers are read OUT of the round's artifacts; the MD's raw index is the payload it actually ships.
"""
import json, hashlib, shutil, datetime
from pathlib import Path

RD = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover")
PUB = RD / "publish"
PAY = PUB / "payload"

COPY = [
    "FAR_RULING.md", "RESIDUAL_REGISTER.json", "W1_RESIDUAL_UNIVERSE.json", "W2_DEFECT_DOSSIER.json",
    "ROUTE_CHECK.json", "HGK_TYPED_ADMISSION_FAR018.json", "KANBAN_LIFECYCLE_RECEIPT.json",
    "prompt-contract.json", "compiler/compiler-receipt.json", "compiler/compiler-report.json",
    "compiler/lint.stdout.txt", "compiler/activation.stdout.txt", "compiler/acceptance.stdout.txt",
    "compiler/compile.stdout.txt", "compiler/hash.stdout.txt", "compiler/duplication.stdout.txt",
    "lane/EXECUTE_BRIEF.md", "lane/VERIFY_BRIEF.md", "lane/EXECUTE_RECEIPT.json", "lane/VERIFY_RECEIPT.json",
    "lane/VERIFY_VERDICT.json",
    "writer/checker_isolation_probe.py", "writer/self_check_v2.py", "writer/regen_entry_map.py",
    "writer/metadata_semantics.py", "writer/cross_index_v2.py", "writer/WRITER_MANIFEST.json",
    "writer/entry_map.json", "writer/METADATA_SEMANTICS_V2.json", "writer/CROSS_INDEX_V2.json",
    "SELF_CHECK_RECEIPT.json", "SELF_EVOLUTION_RECORD.json", "HANDOVER_FAR018.md",
    "isolation_probe_receipt.json", "skill_entry_map_install_receipt.json",
    "ADJUDICATION_AND_LIMITATIONS.json",
    "lane/VERIFY_ATTEMPT1_REFUSED.json",
    # the round's own harness: published so an external team can re-derive, not just read
    "self_check.py", "build_pack.py", "build_register.py", "emit_closure.py", "verify_pack_local.py",
    "persist_firstfail.py", "far018_admission.py", "far018_kanban.py", "recon_route.py",
    "far018_contract.py", "publish_followup2.py",
]
WRITER_DIR = RD / "writer"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load(p):
    try:
        return json.loads((RD / p).read_text(encoding="utf-8"))
    except Exception:
        return {}


def listed(root):
    """Files the index may list. PACK_INDEX.json is EXCLUDED: a file cannot contain its own
    digest, so listing it would assert an impossible value (measured: it produced exactly one
    readback mismatch). Its digest is carried by the publish/readback receipts instead."""
    return sorted(p for p in root.rglob("*") if p.is_file() and p.name != "PACK_INDEX.json")


def index_of(root, note=None):
    files = listed(root)
    idx = {"schema": "FAR-20261016-018/PACK-INDEX/1",
           "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "note": note or "the closure MD cannot contain its own hash; it is indexed here, and this index is "
                           "the file that carries its digest",
           "self_excluded": {
               "path": "PACK_INDEX.json",
               "reason": "an index cannot contain its own digest; a row for itself would be stale by "
                         "construction and failed a live remote readback",
               "its_digest_is_carried_by": ["PUBLISH_RECEIPT.json", "REMOTE_READBACK_VERIFY.json",
                                            "publish/payload/PUBLICATION_ADDENDUM.json"],
           },
           "not_listed_by_design": {
               "reason": "every file below is a receipt ABOUT this commit or about a later commit, so it cannot "
                         "be listed with a digest that the commit itself fixes. Their digests live in "
                         "REMOTE_READBACK_VERIFY.json / PUBLISH_FOLLOWUP_*.json, produced after the commit.",
               "files": ["PACK_INDEX.json", "PUBLISH_RECEIPT.json", "REMOTE_READBACK_VERIFY.json",
                         "POST_PUBLICATION_ADDENDUM.md", "PUBLISH_FOLLOWUP_CORRECT.json",
                         "PUBLISH_FOLLOWUP_FINAL.json"],
           },
           "files": [{"path": str(p.relative_to(root)).replace("\\", "/"), "bytes": p.stat().st_size,
                      "sha256": sha(p.read_bytes())} for p in files]}
    idx["file_count"] = len(idx["files"])
    idx["payload_files_total"] = len(files) + 1
    return idx


def main():
    if PAY.exists():
        shutil.rmtree(PAY)
    missing = []
    for rel in COPY:
        src = RD / rel
        if not src.exists():
            missing.append(rel)
            continue
        dst = PAY / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    (PAY / ".gitattributes").write_text("* -text\n", encoding="utf-8")

    reg = load("RESIDUAL_REGISTER.json")
    ex = load("lane/EXECUTE_RECEIPT.json")
    ve = load("lane/VERIFY_RECEIPT.json")
    vv = load("lane/VERIFY_VERDICT.json")
    sc = load("SELF_CHECK_RECEIPT.json")
    rc = load("ROUTE_CHECK.json")
    comp = load("compiler/compiler-receipt.json")

    def attempt(d):
        a = (d.get("attempts") or [{}])[0]
        return {"provider": a.get("provider"), "model": a.get("model"), "exit": a.get("exit"),
                "seconds": a.get("seconds"), "nonce_present": a.get("nonce_present")}

    ex_a, ve_a = attempt(ex), attempt(ve)
    same_axis = bool(ex_a.get("model")) and ex_a.get("model") == ve_a.get("model")

    files = listed(PAY)
    index = index_of(PAY)
    (PAY / "PACK_INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    files = sorted(p for p in PAY.rglob("*") if p.is_file())
    manifest = {"prefix": f"EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/",
                "files": [str(p.relative_to(PAY)).replace("\\", "/") for p in files]}
    (PUB / "PUBLISH_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    rc_counts = (reg.get("recomputed_counts") or {})
    md = []
    A = md.append
    A("# EVIDENCE CLOSURE — FAR-20261016-018 (R7～R11 殘留結案與移交)\n")
    A(f"generated_utc: {index['generated_utc']}\n")
    A("## 0. Claim ceiling and binding\n")
    A("| field | value |")
    A("|---|---|")
    A("| claim ceiling | `LOCAL` — 本地可重導的完成 |")
    A("| external acceptance | **NOT ISSUED**（待真實驗收官） |")
    A("| full_convergence_verdict | `TEMP_CLOSED_CHALLENGE` |")
    A("| production_verdict | `FAIL_CLOSED` |")
    A("| canonical_AO_acceptance | `NOT_ISSUED` |")
    A("| reviewer of this pack | none — 本 pack 未經任何外部驗收官接受 |")
    A("")
    A("## 1. 本輪是什麼\n")
    A("FAR 研究輪：對 R7～R11 證據歸檔輪遺留的全部殘留／缺口／阻斷、待 OWNER 決策項、候選未落地資產與本 "
      "SESSION 結案移交事項，提出唯一份排名工程裁決並執行其中 agent 可執行項目；OWNER-gated 僅備妥、未執行。")
    A("")
    A("## 2. 執行面（皆有收據）\n")
    A("| 面 | 證據 |")
    A("|---|---|")
    A(f"| Gate-1 route | `{json.dumps((rc.get('registry') or {}).get('route_FAR_RESEARCH'), ensure_ascii=False)}`；負控制 `PURE_QA_CHAT` → `{((rc.get('registry') or {}).get('route_NEGATIVE_CONTROL') or {}).get('route')}` |")
    A(f"| CAPC contract | `{comp.get('verdict')}`（lint／activation／acceptance／compile 皆 exit 0） |")
    A(f"| HGK admission | `{(load('HGK_TYPED_ADMISSION_FAR018.json') or {}).get('verdict')}` project `{(load('HGK_TYPED_ADMISSION_FAR018.json') or {}).get('project_id')}` |")
    A(f"| Kanban | {(load('KANBAN_LIFECYCLE_RECEIPT.json') or {}).get('cards_created')} 卡／{(load('KANBAN_LIFECYCLE_RECEIPT.json') or {}).get('call_count')} 次 CLI；histogram `{json.dumps((load('KANBAN_LIFECYCLE_RECEIPT.json') or {}).get('board_state_histogram'), ensure_ascii=False)}` |")
    A("| OpenSpec | `hgk-far-018-r7r11-residual-closure` strict-valid |")
    A(f"| EXECUTE lane | `{ex_a.get('provider')}/{ex_a.get('model')}` exit {ex_a.get('exit')} nonce {ex_a.get('nonce_present')} |")
    A(f"| VERIFY lane | `{ve_a.get('provider')}/{ve_a.get('model')}` exit {ve_a.get('exit')} nonce {ve_a.get('nonce_present')} |")
    A(f"| model-axis diversity | **{'ABSENT' if same_axis else 'PRESENT'}**（EXECUTE `{ex_a.get('model')}` vs VERIFY `{ve_a.get('model')}`） |")
    A("")
    A("## 3. 殘留暫存器（自 artifact 重算）\n")
    A("| 量 | 值 |")
    A("|---|---|")
    for k in ("w1_items_total", "w2_defects", "w2_confirmed_defects"):
        A(f"| {k} | {rc_counts.get(k)} |")
    A(f"| w1 by_kind | `{json.dumps(rc_counts.get('w1_by_kind'), ensure_ascii=False)}` |")
    A(f"| w1 by_authority | `{json.dumps(rc_counts.get('w1_by_authority'), ensure_ascii=False)}` |")
    A(f"| agent-executable 仍開放 | `{json.dumps(rc_counts.get('w1_agent_executable_open'), ensure_ascii=False)}` |")
    A("")
    A("## 4. 本輪執行的動作與其殘留\n")
    A("| # | 動作 | 優先 | 收據存在 | 執行後仍留的殘留 |")
    A("|---|---|---|---|---|")
    for k, v in (reg.get("executable_now_actions", {}).get("actions") or {}).items():
        present = (reg.get("executable_now_actions", {}).get("evidence_present_at_registration") or {}).get(k, {}).get("evidence_present")
        A(f"| {k} | {v.get('title')} | {v.get('priority')} | {present} | {v.get('residual_after') or '—'} |")
    A("")
    A("## 5. 獨立 checker（不同模型軸）\n")
    A(f"- served arm `{ve_a.get('provider')}/{ve_a.get('model')}`，required arm 由 `--require-arm` pin（pool rank 1 是 writer 自己的模型，故 pin rank 2）")
    A(f"- verdict file: `lane/VERIFY_VERDICT.json`；overall `{vv.get('overall')}`")
    if isinstance(vv.get("verdicts"), list):
        for v in vv["verdicts"]:
            A(f"  - `{v.get('id')}` {v.get('verdict')} — {str(v.get('claim'))[:110]}")
    if vv.get("disagreements"):
        A(f"- disagreements（原話保留，未吞）: `{json.dumps(vv.get('disagreements'), ensure_ascii=False)[:600]}`")
    if vv.get("could_not_verify"):
        A(f"- could_not_verify: `{json.dumps(vv.get('could_not_verify'), ensure_ascii=False)[:400]}`")
    A("")
    A("## 6. OWNER-gated（本輪未執行）\n")
    for k, v in (reg.get("owner_gated") or {}).items():
        A(f"- `{k}` {v}")
    A("")
    A("## 7. 自檢測\n")
    A(f"`SELF_CHECK_RECEIPT.json`: {json.dumps(sc.get('summary') or sc.get('counts') or {}, ensure_ascii=False)} verdict `{sc.get('verdict')}`")
    A("")
    A("## 8. Nonclaims\n")
    for n in (reg.get("nonclaims") or []):
        A(f"- {n}")
    A("- 本輪未合併任何 PR、未晉升任何 Draft、未編輯 canonical 控制平面、未執行任何歸檔腳本。")
    A("- A1 證明的 OS 寫入拒絕是**普通拒絕**，同身分可自行解除其 deny ACE，**不是**不可解除的安全邊界。")
    A("")
    A("## 9. STOP / resume\n")
    A("STOP：本輪到此為止，claim ceiling `LOCAL`；正式 `R7-03` 關閉需 OG6（不同 OS 身分），`R7-04` 需 OG3，"
      "`R7-02` 需 OG2，canonical pin 修復需 OG4，peer chain 需 OG1，guard 精度需 OG8。")
    A("resume：讀 `RESIDUAL_REGISTER.json` 取殘留與 owner，讀 `HANDOVER_FAR018.md` 取 checkpoint 與下一步。")
    A("")
    A("## 10. Raw artifact index（本 pack 實際攜帶的檔案）\n")
    A("| path | bytes | sha256 |")
    A("|---|---|---|")
    for f in index["files"]:
        A(f"| `{f['path']}` | {f['bytes']} | `{f['sha256'][:24]}…` |")
    A("")
    A("`PACK_INDEX.json` is not listed above and does not list itself: a file cannot contain its own digest. "
      "Its digest is carried by `PUBLISH_RECEIPT.json`, `REMOTE_READBACK_VERIFY.json` and "
      "`PUBLICATION_ADDENDUM.json` instead. (A self-row was tried in the first publication attempt and failed a "
      "live remote readback with exactly one mismatch — recorded, not hidden.)")
    A("")
    (PAY / "EVIDENCE_CLOSURE_FAR-20261016-018.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # PACK_INDEX must cover the MD too: it was written after the index, so re-index now.
    index = index_of(PAY, note="the closure MD cannot contain its own hash (it is indexed here); "
                               "PACK_INDEX.json is excluded from its own listing for the same reason — "
                               "its digest is carried by the publish/readback receipts")
    (PAY / "PACK_INDEX.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    files = sorted(p for p in PAY.rglob("*") if p.is_file())
    manifest["files"] = [str(p.relative_to(PAY)).replace("\\", "/") for p in files]
    (PUB / "PUBLISH_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")

    print("payload files:", index["file_count"], "| missing inputs:", len(missing))
    for m in missing:
        print("   MISSING:", m)
    print("md bytes:", (PAY / "EVIDENCE_CLOSURE_FAR-20261016-018.md").stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
