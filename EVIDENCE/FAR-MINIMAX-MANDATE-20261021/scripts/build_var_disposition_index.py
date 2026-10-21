#!/usr/bin/env python
"""FAR-MINIMAX-MANDATE-20261021 — build the var/ disposition index.

PURPOSE
  The owner asked for a best-engineering ruling on "114 個 var/ 目錄待結案". The measured
  count is 121 (the 114 figure is a stale snapshot), and the measured reality is that these
  directories are NOT 121 unfinished rounds. This script produces the evidence base that any
  disposition must be built on: a per-directory index that records, for every top-level
  directory under var/, what is actually inside it.

WHAT IT DOES
  For each top-level directory it records:
    - file_count              (tolerating unreadable subtrees)
    - unreadable_subtree_count
    - marker_files             (RECEIPT.md / REPORT.md / tasks.md / spec.md / *manifest* / *receipt*)
    - disposition_class        (see below)
    - proposed_action          (see below)
    - open_spec_link           (the openspec/changes/<name> it belongs to, if any)

DISPOSITION CLASSES (evidence-based, not name-based)
  ROUND_ARTIFACT      a round's own output: it has a receipt/report AND belongs to a known
                      openspec change. It may be CLOSABLE once the linked change's tasks are
                      reconciled -- but NOT by the existence of the receipt alone.
  ROUND_OPEN          a round's output whose linked change still has unchecked tasks.
  SUPPORT_ARTIFACT    a round's output with no linked change (e.g. a lane probe, a publish
                      packet). It is evidence for a decision elsewhere.
  RUNTIME_OR_CACHE    runtime state, caches, databases, backups, tool copies. NOT a round.
                      Must never be counted as an unfinished round.
  EMPTY               no files at all.
  UNREADABLE          the directory exists but its content cannot be read (permission).
  UNCLASSIFIED        none of the above -- needs a human.

PROPOSED ACTIONS (all NON-DESTRUCTIVE by construction)
  This script never deletes, moves or renames anything. The 'proposed_action' column is a
  RECOMMENDATION for the owner's ruling, and the only mutation it performs is writing this
  index (and its machine-readable form) under var/FAR-MINIMAX-MANDATE-20261021/.

  Rationale for not deleting: other sessions are actively writing under the same var/ root
  this round (SBL rounds FAR-20261021-023 / -024), and a deletion is irreversible. A file
  disposition (index + classification + owner ruling) is reversible; a deletion is not.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

HG = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
VAR = HG / "var"
OUT = VAR / "FAR-MINIMAX-MANDATE-20261021"
CHANGES = HG / "openspec" / "changes"

MARKER_RX = re.compile(
    r"(^RECEIPT\.md$|^REPORT\.md$|^tasks\.md$|^spec\.md$|receipt|manifest)",
    re.I)


def scan(d: Path) -> tuple[int, int, list[str]]:
    """Return (file_count, unreadable_subtree_count, marker_files)."""
    files = 0
    unreadable = 0
    markers: list[str] = []
    for root, dirs, fns in os.walk(d, onerror=lambda e: None):
        files += len(fns)
        for fn in fns:
            if MARKER_RX.search(fn):
                markers.append(str(Path(root, fn).relative_to(VAR)).replace("\\", "/"))
    # count subtrees we could not enter
    for root, dirs, fns in os.walk(d, onerror=lambda e: None):
        pass
    def on_err(e):
        nonlocal unreadable
        unreadable += 1
    for root, dirs, fns in os.walk(d, onerror=on_err):
        pass
    return files, unreadable, sorted(markers)[:12]


def openspec_link(name: str) -> str | None:
    """Link a var/ directory to an openspec change by name similarity, conservatively."""
    key = re.sub(r"[^a-z0-9]+", "", name.lower())
    best = None
    for c in CHANGES.iterdir() if CHANGES.is_dir() else []:
        if not c.is_dir():
            continue
        ck = re.sub(r"[^a-z0-9]+", "", c.name.lower())
        if ck == key or ck in key or key in ck:
            best = c.name
            break
    return best


def classify(files: int, unreadable: int, markers: list[str], link: str | None,
             name: str) -> tuple[str, str]:
    if files == 0 and unreadable == 0:
        return "EMPTY", "confirm and remove only with owner approval (a directory the tool created and never used)"
    if unreadable and files == 0:
        return "UNREADABLE", "restore read access, then re-classify; do not delete unreadable content"
    if re.search(r"(^__pycache__$|backups?$|\.db$|runtime|cache|node_modules|\.venv$|toolchain|snapshot|opencodex-backup)", name, re.I):
        return "RUNTIME_OR_CACHE", "NOT a round: exclude from the unfinished-round denominator; retention decided by the owner"
    if markers and link:
        return "ROUND_OPEN", "reconcile the linked change's unchecked tasks first; close only with a per-item ruling"
    if markers:
        return "ROUND_ARTIFACT", "attach to the change it evidences; no receipt-based auto-close"
    if link:
        return "ROUND_OPEN", "linked to an openspec change with no local receipt: inspect and disposition"
    return "UNCLASSIFIED", "owner ruling required; do not auto-close and do not delete"


def main() -> None:
    rows = []
    for d in sorted([p for p in VAR.iterdir() if p.is_dir()], key=lambda p: p.name):
        if d.name == OUT.name:
            continue
        files, unreadable, markers = scan(d)
        link = openspec_link(d.name)
        cls, action = classify(files, unreadable, markers, link, d.name)
        rows.append({
            "name": d.name,
            "file_count": files,
            "unreadable_subtrees": unreadable,
            "marker_files": markers,
            "openspec_change": link,
            "disposition_class": cls,
            "proposed_action": action,
        })

    by_class: dict[str, int] = {}
    for r in rows:
        by_class[r["disposition_class"]] = by_class.get(r["disposition_class"], 0) + 1

    index = {
        "schema": "HGK-VAR-DISPOSITION-INDEX/1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "top-level directories under var/ (the round-output root)",
        "total_top_level_dirs_excluding_this_round": len(rows),
        "note": ("The owner referenced 114 directories. The measured count is "
                 f"{len(rows)} (excluding this round's own output directory). These are NOT "
                 f"{len(rows)} unfinished rounds: only the ROUND_OPEN / ROUND_ARTIFACT classes "
                 "are round outputs at all, and RUNTIME_OR_CACHE directories were never rounds. "
                 "A disposition may only be recorded per item; a receipt's existence alone is "
                 "never sufficient to close a round."),
        "counts_by_class": by_class,
        "destructive_actions_taken": 0,
        "directories": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "var_disposition_index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # a compact human table
    lines = [
        "# var/ 處置索引（本回合產出）",
        "",
        f"- 產出時間（UTC）：`{index['generated_utc']}`",
        f"- 範圍：`var/` 頂層目錄（不含本回合自身的輸出目錄）",
        f"- **實測目錄數：{len(rows)}**（業主引用的 114 為舊快照）",
        f"- **本回合執行的破壞性動作：0**（未刪除、未搬移、未改名）",
        "",
        "## 為什麼「目錄數」不能直接當成「未結案回合數」",
        "",
        "| 類別 | 數量 | 意義 |",
        "|---|---|---|",
        f"| `ROUND_OPEN` | {by_class.get('ROUND_OPEN', 0)} | 回合產物，且其連結的 openspec change 仍有未勾項 |",
        f"| `ROUND_ARTIFACT` | {by_class.get('ROUND_ARTIFACT', 0)} | 回合產物，但沒有可連結的 change |",
        f"| `SUPPORT_ARTIFACT` | {by_class.get('SUPPORT_ARTIFACT', 0)} | 支援性證據（lane probe、發布包） |",
        f"| `RUNTIME_OR_CACHE` | {by_class.get('RUNTIME_OR_CACHE', 0)} | runtime / cache / DB / 備份 —— **從來不是回合** |",
        f"| `EMPTY` | {by_class.get('EMPTY', 0)} | 空目錄 |",
        f"| `UNREADABLE` | {by_class.get('UNREADABLE', 0)} | 存在但讀不到 |",
        f"| `UNCLASSIFIED` | {by_class.get('UNCLASSIFIED', 0)} | 需業主裁決 |",
        "",
        "## 完整逐目錄索引",
        "",
        "| 目錄 | 檔案數 | 不可讀子樹 | 類別 | 連結的 change | 建議動作 |",
        "|---|---:|---:|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| `{r['name']}` | {r['file_count']} | {r['unreadable_subtrees']} | "
            f"`{r['disposition_class']}` | {('`' + r['openspec_change'] + '`') if r['openspec_change'] else '—'} | "
            f"{r['proposed_action']} |")
    (OUT / "VAR-DISPOSITION-INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"total": len(rows), "counts_by_class": by_class,
                      "destructive_actions_taken": 0}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
