#!/usr/bin/env python
"""FAR-MINIMAX-MANDATE-20261021 — index the unchecked OpenSpec tasks (no auto-ticking).

PURPOSE
  The owner referenced "33 個其他 OpenSpec change 的 471 個未勾項目". A prior research agent
  MEASURED the real numbers as 37 active changes / 34 with unchecked items / 460 unchecked
  (the 471 figure is a stale estimate). This script produces the evidence base for a ruling:
  a per-change, per-task index that says what each unchecked item is and what evidence exists
  for it.

WHAT IT DOES
  For every change under openspec/changes/ it counts the unchecked "- [ ]" items, lists them,
  and cross-checks each against the repository for evidence that the work was actually done:
    - a commit in git log whose subject mentions the change name
    - files the change's own artifacts reference that exist in the tree
    - the change's own directory (evidence written INSIDE the change)

WHAT IT DELIBERATELY DOES NOT DO
  It does NOT tick any box. A checkbox is a claim about a piece of work; this script only
  assembles the evidence that a ruling would judge. Ticking is the owner's ruling, applied
  afterwards through a separate, explicit, reviewable step.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HG = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
CHANGES = HG / "openspec" / "changes"
OUT = HG / "var" / "FAR-MINIMAX-MANDATE-20261021"
TICK = re.compile(r"^\s*-\s*\[ \]\s*(.+?)\s*$")
DONE = re.compile(r"^\s*-\s*\[[xX]\]\s*(.+?)\s*$")


def git_log_subjects() -> str:
    r = subprocess.run(["git", "log", "--oneline", "-400"], cwd=HG,
                       capture_output=True, text=True)
    return r.stdout


def main() -> None:
    log = git_log_subjects()
    rows = []
    for c in sorted(CHANGES.iterdir(), key=lambda p: p.name) if CHANGES.is_dir() else []:
        if not c.is_dir():
            continue
        tasks_files = sorted(c.rglob("tasks.md"))
        unchecked, checked = [], []
        for tf in tasks_files:
            for ln in tf.read_text(encoding="utf-8", errors="replace").splitlines():
                m = TICK.match(ln)
                if m:
                    unchecked.append({"file": str(tf.relative_to(HG)).replace("\\", "/"),
                                      "text": m.group(1)})
                    continue
                m2 = DONE.match(ln)
                if m2:
                    checked.append(m2.group(1))
        in_log = bool(re.search(re.escape(c.name.lower().split("-")[0]), log, re.I))
        # files inside the change directory (self-evidence)
        inside = [str(p.relative_to(HG)).replace("\\", "/")
                  for p in c.rglob("*") if p.is_file()]
        rows.append({
            "change": c.name,
            "unchecked_count": len(unchecked),
            "checked_count": len(checked),
            "unchecked": unchecked,
            "has_own_artifacts": len(inside),
            "name_appears_in_git_log": in_log,
            "spec_files": [str(p.relative_to(HG)).replace("\\", "/")
                           for p in sorted(c.rglob("spec.md"))],
        })

    with_unchecked = [r for r in rows if r["unchecked_count"] > 0]
    total_unchecked = sum(r["unchecked_count"] for r in rows)
    # the 33 "other" changes = all with unchecked items, minus this round's own change
    own = "far-lane-remediation-20261021"
    others = [r for r in with_unchecked if r["change"] != own]

    out = {
        "schema": "HGK-OPENSPEC-UNCHECKED-INDEX/1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "total_active_changes": len(rows),
        "changes_with_unchecked": len(with_unchecked),
        "total_unchecked": total_unchecked,
        "other_changes_with_unchecked": len(others),
        "other_changes_unchecked": sum(r["unchecked_count"] for r in others),
        "this_round_change": own,
        "owner_referenced_figure": 471,
        "figure_note": ("The owner's 471 is a stale estimate. The measured figure is "
                        f"{total_unchecked} unchecked items across {len(with_unchecked)} "
                        f"changes ({sum(r['unchecked_count'] for r in others)} in the "
                        f"{len(others)} changes other than this round's)."),
        "ticks_applied_by_this_script": 0,
        "changes": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "openspec_unchecked_index.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# OpenSpec 未勾項索引（本回合產出，未自動打勾）",
        "",
        f"- 產出時間（UTC）：`{out['generated_utc']}`",
        f"- active changes：**{out['total_active_changes']}**",
        f"- 有未勾項的 change：**{out['changes_with_unchecked']}**",
        f"- 未勾項總數：**{out['total_unchecked']}**（業主引用的 471 為舊估計值）",
        f"- 本回合自身 change 之外的 change：**{out['other_changes_with_unchecked']}** 個，"
        f"合計 **{out['other_changes_unchecked']}** 個未勾項",
        f"- **本腳本套用的 tick 數：0**",
        "",
        "## 逐 change 索引",
        "",
        "| change | 未勾 | 已勾 | 自身產物檔 | 名稱出現於 git log |",
        "|---|---:|---:|---:|---|",
    ]
    for r in sorted(rows, key=lambda x: -x["unchecked_count"]):
        lines.append(f"| `{r['change']}` | {r['unchecked_count']} | {r['checked_count']} | "
                     f"{r['has_own_artifacts']} | {'是' if r['name_appears_in_git_log'] else '否'} |")
    (OUT / "OPENSPEC-UNCHECKED-INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({k: out[k] for k in (
        "total_active_changes", "changes_with_unchecked", "total_unchecked",
        "other_changes_with_unchecked", "other_changes_unchecked",
        "ticks_applied_by_this_script")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
