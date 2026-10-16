"""Generate WS_A/WS_A_RECEIPT.md from the recorded evidence artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A")


def j(name: str) -> dict:
    return json.loads((W / name).read_text(encoding="utf-8"))


def main() -> int:
    rec = j("apply/APPLY_RECEIPT.json")
    s2 = j("s2_repair_result.json")
    s34 = j("s34_stale_refs_result.json")
    s5 = j("s5_loss_proof.json")
    wit = j("baseline_witness.json")
    drill = j("rollback_drill_result.json")
    reg6 = j("logs/step6_default.json")
    reg8 = j("logs/step8_live.json")
    reg8s = j("logs/step8_selflive.json")

    rows = rec["paths"]
    L: list[str] = []
    a = L.append

    a("# WS-A RECEIPT — repair and guarded landing of the slimmed `adversarial-verification-rounds` skill")
    a("")
    a("- Round: `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0`; HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`, WorkOrder lineage `WO-TS-CLOSURE-01..04`.")
    a("- Authority: PKG v2.0.0 G-A (Skills) + EIA-R6-09 + K-16/K-17.")
    a("- **Claim ceiling: LOCAL / candidate-only.** This is a maker receipt — a claim, not an acceptance. No independent verification, no promotion, no canonical acceptance is claimed. The orchestrator's re-run is the evidence.")
    a("")
    a("## 0. Reader's summary")
    a("")
    a(f"- Repaired candidate main file: {s2['after_bytes']} bytes (was {s2['before_bytes']} with {s2['marker_lines_removed']} `SKCV-SLICE` marker lines); cap 100,000. Live SKILL.md before this turn: 101,488 bytes (over cap).")
    a(f"- Landing actions: {rec['counts']['added']} added, {rec['counts']['replaced']} replaced, {rec['counts']['retained_untouched']} retained untouched ({rec['target_paths_total']} target paths).")
    a("- Excluded stale absorption: `references/verifier-lane-handover.md` — the stub recorded `aebb35ea…`; the live file had moved to `2126b82e…`. Carried the current live file verbatim instead of absorbing.")
    a(f"- Step 6 harness on the repaired candidate (against the frozen originals): **{reg6['verdict']}**.")
    a(f"- Step 8 harness on the live tree (with the originals-witness `--live`): **{reg8['verdict']}**.")
    a(f"- Rollback drill: {drill['verdict']} — {drill['pre_turn_files']} files restored byte-for-byte after a 31-file landing.")
    a("")
    a("## 1. What ran (commands, exit codes)")
    a("")
    a("All commands run under `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (pwsh). Nothing was written outside `WS_A/` and the live skill directory.")
    a("")
    a("| # | Command | Exit |")
    a("|---|---|---|")
    a("| 1 | `Copy-Item -Recurse -Force <frozen>/candidates/avr/skill WS_A/repaired_candidate` (30 files) | 0 |")
    a("| 2 | `python WS_A/tools/s2_repair_skill_md.py` | 0 |")
    a("| 3-4 | `python WS_A/tools/s34_stale_refs.py` | 0 |")
    a("| 5 | `python WS_A/tools/s5_loss_proof.py` | 0 |")
    a("| 6 | `python <harness> --subject WS_A/repaired_candidate --out WS_A/logs/step6_default.json` | 0 |")
    a("| 7 | `python WS_A/tools/landing.py --src WS_A/repaired_candidate --dst <live> --preimage WS_A/apply/preimage --receipt WS_A/apply/APPLY_RECEIPT.json` | 0 |")
    a("| 8a | `python <harness> --subject <live> --out WS_A/logs/step8_selflive.json` | 1 |")
    a("| 8b | `python <harness> --subject <live> --live <frozen-baseline> --out WS_A/logs/step8_live.json` | 0 |")
    a("| — | `python WS_A/tools/rollback_drill.py` | 0 |")
    a("")
    a("Exit code is the harness's own `verdict==PASS` gate (0) / otherwise (1).")
    a("")
    a("## 2. Repair (step 2)")
    a("")
    a(f"- Marker lines removed: **{s2['marker_lines_removed']}** (`^=+\\s*SKCV-SLICE`).")
    a(f"- Before: {s2['before_bytes']} bytes, sha256 `{s2['before_sha256']}`.")
    a(f"- After: {s2['after_bytes']} bytes, sha256 `{s2['after_sha256']}`.")
    a(f"- Now starts with `---`: {s2['starts_with_frontmatter']}; frontmatter `name: {s2['frontmatter_name']}`, `version: {s2['frontmatter_version']}`; remaining marker lines: {s2['remaining_marker_lines']}.")
    a("")
    a("## 3. Excluded stale absorption (steps 3-4)")
    a("")
    a("7 absorbed-reference stubs were re-verified against the **current** live bytes:")
    a("")
    a("| reference | recorded sha256 | current live sha256 | result |")
    a("|---|---|---|---|")
    for r in s34["rows"]:
        a(f"| `{r['ref']}` | `{r.get('recorded_sha256','')[:16]}…` | `{r.get('live_sha256','')[:16]}…` | {r['status']} |")
    a("")
    for c in s34["mismatches_handled"]:
        a(f"- **EXCLUDED_STALE_ABSORPTION** `{c['ref']}`: stub recorded `{c['stub_recorded_sha256']}`, "
          f"but the live file is now `{c['carried_live_sha256']}` ({c['carried_live_bytes']} bytes). "
          "The current live file was copied verbatim into the repaired candidate; the stale stub was discarded. "
          "No newer live text was silently overwritten by stale absorbed text.")
    a("")
    a("## 4. Loss proof from bytes (step 5)")
    a("")
    a(f"- (a) current live bytes appear verbatim at the recorded topic offset for every absorbed reference: **{s5['a_offset_verbatim']}**.")
    a(f"- (b) every live `SKILL.md` line longer than 40 bytes survives in (repaired SKILL.md U topic files U carried-live references): **{s5['b_line_survival']}** "
      f"({s5['live_lines_gt40']} lines, {s5['lost_lines']} lost).")
    a(f"- Raw output: `WS_A/s5_loss_proof.txt`, `WS_A/s5_loss_proof.json`. Step verdict: **{s5['verdict']}**.")
    a("")
    a("## 5. Harness results (steps 6 and 8)")
    a("")
    a("The harness file changed at 2026-10-16 11:02 (after this brief was written at 10:56): C4 became marker-based and a `--live` flag was added. This matters for step 8 — see the note below.")
    a("")
    a("| check | step 6 (repaired candidate) | step 8 (live, `--live`=originals witness) | step 8 (live, default `--live`=live) |")
    a("|---|---|---|---|")
    for k in ("C1_capacity", "C2_loader_shape", "C3_link_intake", "C4_lossless", "C5_controls"):
        a(f"| {k} | {reg6['checks'][k]['verdict']} | {reg8['checks'][k]['verdict']} | {reg8s['checks'][k]['verdict']} |")
    a(f"| **overall** | **{reg6['verdict']}** | **{reg8['verdict']}** | **{reg8s['verdict']}** |")
    a("")
    a("**Why step 8 needs the originals-witness.** C4 compares each absorbed stub's recorded sha against `LIVE/references/<name>`. After landing, the live tree's own `references/<name>` slots *are* the stubs, so the default self-referential invocation (`--live` unset = live tree) cannot pass by construction — there is no residual copy of the originals left in that path. The updated harness's `--live` flag exists exactly to point C4 at the tree the stubs absorbed from. The frozen baseline `HG-KSEOS/var/SKILL-CONVERGENCE-20261014/baseline/adversarial-verification-rounds` is that originals witness.")
    a("")
    a(f"- Originals-witness check: baseline sha256 == the recorded stub sha for all {len(wit['rows'])} absorbed references: **{wit['verdict']}**.")
    a("- Raw JSON: `WS_A/logs/step6_default.json`, `WS_A/logs/step8_live.json`, `WS_A/logs/step8_selflive.json`, `WS_A/sim/reg2.json`, `WS_A/sim/regression_postland_baseline.json`.")
    a("")
    a("## 6. Guarded landing (step 7)")
    a("")
    a(f"Target live dir: `{rec['dst']}`")
    a("")
    a(f"- Pre-image: byte copy of **every pre-existing target path** in `WS_A/apply/preimage/` + `WS_A/apply/preimage/PREIMAGE_MANIFEST.json`.")
    a("- Policy: add files the candidate has and the live tree lacks; replace files whose bytes differ; **never delete** a live file the candidate lacks.")
    a("")
    a("### Before/after per path")
    a("")
    a("| path | action | before bytes | before sha256 | after bytes | after sha256 |")
    a("|---|---|---|---|---|---|")
    for r in rows:
        bs = (r["before_sha256"] or "")[:16]
        as_ = (r["after_sha256"] or "")[:16]
        a(f"| `{r['path']}` | {r['action']} | {r['before_bytes']} | `{bs}` | {r['after_bytes']} | `{as_}` |")
    a("")
    a(f"Tree-level counts: added={rec['counts']['added']}, replaced={rec['counts']['replaced']}, retained_untouched={rec['counts']['retained_untouched']} "
      f"(target paths {rec['target_paths_total']}; candidate files {rec['src_files_total']}; live files before {rec['dst_files_total']}).")
    a("")
    a("- Rollback: `WS_A/apply/rollback.py` (restores every pre-image byte-for-byte, deletes every added file). Drill: **{0}**.".format(drill["verdict"]))
    a("")
    a("## 7. Honest gaps / limits")
    a("")
    a("- **Maker claim only.** No independent checker has run; nothing is accepted, approved, promoted, or canonical-verified.")
    a("- **The harness file changed mid-turn** (mtime 11:02, after the 10:56 brief). I ran the current version. Its C4 is marker-based and it adds `--live`; a caller following the brief literally (`--subject <live>` with no `--live`) will see C4 FAIL by construction after landing, because the live absorbed-reference slots become the stubs. The pass requires `--live` = the originals witness.")
    a("- **`references/verifier-lane-handover.md` is not the frozen-round bytes.** It is the current live file (`2126b82e…`, 29,708 bytes), carried verbatim. The frozen round's recorded target (`aebb35ea…`, 26,549 bytes) is not present in the landed tree. This is the honest handling of a tree that moved after the freeze.")
    a("- **`references/topics/*` and `topic-source-remainder.md` are the frozen round's absorbed text**, landed verbatim. The absorbed stubs are tiny pointer files; the harness treats any file carrying an `absorbed ->` marker as a stub regardless of size.")
    a("- **Live-tree drift is possible after this turn** (the runtime curator can advance it); byte-exactness holds at the moment of this receipt only.")
    a("- I did not read, copy, or print any credential material, and made no git writes and no external network calls.")
    a("")
    a("## 8. Artifacts in `WS_A/`")
    a("")
    a("- `repaired_candidate/` — repaired candidate tree (30 files).")
    a("- `apply/APPLY_RECEIPT.json`, `apply/preimage/` (+`PREIMAGE_MANIFEST.json`), `apply/rollback.py`.")
    a("- `logs/step6_default.json`, `logs/step8_live.json`, `logs/step8_selflive.json`, `logs/step5.txt`.")
    a("- `s2_repair_result.json`, `s34_stale_refs_result.json`, `s5_loss_proof.{txt,json}`, `baseline_witness.json`, `rollback_drill_result.json`.")
    a("- `live_preimage_snapshot.txt`, `live_postimage_snapshot.txt`.")
    a("- `tools/` — the scripts above; `sim/` — post-landing simulations and the rollback drill.")
    a("")

    (W / "WS_A_RECEIPT.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
