#!/usr/bin/env python3
"""Read-only registry readback for WP-FHS-17.

Reproduce:
    python tools/registry_readback.py --out evidence/registry-before.json
    python tools/registry_readback.py --out evidence/registry-after.json

Opens the original SharedSpine database with `mode=ro&immutable=1` (the plain
read-only open fails while the service holds the WAL; this observes the main
database file only, which is stated in the output, not hidden). It writes
NOTHING to the database.

Besides the WP rows it answers one question the officer's REAL_CURRENT_NEED
finding turns on: does any admitted CurrentNeed / SourceSelectionID /
OriginalDisposition object exist anywhere in the original registry? The answer
is recorded as a machine-checkable search over every text column, not an
assertion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import time
from pathlib import Path

DB = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db")
URI = f"file:{DB.as_posix()}?mode=ro&immutable=1"
NEEDLES = ["CurrentNeed", "Current Need", "current_need",
           "SourceSelectionID", "Source Selection", "OriginalDisposition",
           "Original Disposition"]


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(cur: sqlite3.Cursor, sql: str, args: tuple = ()) -> list[dict]:
    return [dict(r) for r in cur.execute(sql, args)]


def need_search(cur: sqlite3.Cursor) -> dict:
    tables = [r[0] for r in cur.execute(
        "select name from sqlite_master where type='table' order by 1")]
    counts = {n: 0 for n in NEEDLES}
    examples = {n: [] for n in NEEDLES}
    prose_tables = {"candidates", "knowledge_docs", "source_units", "memory_records"}
    # FTS shadow tables are byte mirrors of knowledge_docs.body, not objects.
    def is_prose(t: str) -> bool:
        return t in prose_tables or t.startswith("knowledge_fts")

    non_prose_hits = []
    for t in tables:
        try:
            cols = [r[1] for r in cur.execute(f'pragma table_info("{t}")')]
        except sqlite3.Error:
            continue
        for col in cols:
            try:
                found = cur.execute(
                    f'select rowid, "{col}" from "{t}" where typeof("{col}")=\'text\''
                ).fetchall()
            except sqlite3.Error:
                continue
            for rid, val in found:
                if not val:
                    continue
                for n in NEEDLES:
                    if n in val:
                        counts[n] += 1
                        if is_prose(t):
                            if len(examples[n]) < 3:
                                examples[n].append({"table": t, "column": col,
                                                    "rowid": rid, "excerpt": val[:160]})
                        else:
                            non_prose_hits.append({"needle": n, "table": t,
                                                   "column": col, "rowid": rid,
                                                   "excerpt": val[:160]})
    structural = {
        "tables_with_need_column": [],
        "tables_with_selection_column": [],
        "tables_with_disposition_column": [],
    }
    for t in tables:
        try:
            cols = [r[1].lower() for r in cur.execute(f'pragma table_info("{t}")')]
        except sqlite3.Error:
            continue
        if any("need" in c for c in cols):
            structural["tables_with_need_column"].append(t)
        if any("selection" in c for c in cols):
            structural["tables_with_selection_column"].append(t)
        if any("disposition" in c for c in cols):
            structural["tables_with_disposition_column"].append(t)
    # The decisive question is not "does the string appear in some document body"
    # but "is there an OBJECT (table/column) that could hold an admitted
    # CurrentNeed / SourceSelectionID / OriginalDisposition". Column names are
    # matched strictly; `provider_bindings.disposition` is the provider enum
    # dimension (DEFER/REJECT/...), not a need's OriginalDisposition.
    strict = ("currentneed", "current_need", "need", "sourceselection",
              "source_selection", "originaldisposition", "original_disposition")
    object_columns = []
    for t in tables:
        try:
            cols = [r[1] for r in cur.execute(f'pragma table_info("{t}")')]
        except sqlite3.Error:
            continue
        for c in cols:
            low = c.lower().replace("-", "_")
            if any(s in low for s in strict):
                object_columns.append({"table": t, "column": c})
    try:
        provider_dispositions = [r[0] for r in cur.execute(
            "select distinct disposition from provider_bindings order by 1")]
    except sqlite3.Error:
        provider_dispositions = []
    absent = not object_columns and not non_prose_hits
    return {
        "needles": NEEDLES,
        "text_hits": counts,
        "examples": examples,
        "structural_columns": structural,
        "object_model": {
            "tables_inspected": len(tables),
            "columns_named_like_a_need_or_selection": object_columns,
            "prose_only_text_hits": bool(counts["Source Selection"] or counts["CurrentNeed"]),
            "prose_tables": sorted(prose_tables),
            "prose_table_rule": "candidates|knowledge_docs|source_units|memory_records|knowledge_fts*",
            "non_prose_text_hits": non_prose_hits,
            "provider_bindings_disposition_values": provider_dispositions,
            "note": ("provider_bindings.disposition is the provider enum dimension; it is "
                     "not an OriginalDisposition for a need and is excluded from the "
                     "object-model match."),
        },
        "conclusion": ("ABSENT_AS_OBJECT_MODEL: no table or column can hold an admitted "
                       "CurrentNeed / SourceSelectionID / OriginalDisposition; every text "
                       "hit is inside a free-text document body"
                       if absent else "PRESENT_OR_PARTIAL: see object_model / non_prose_text_hits"),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    conn = sqlite3.connect(URI, uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    out = {
        "command": "python tools/registry_readback.py --out " + a.out,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "db": {
            "path": str(DB),
            "sha256": sha_file(DB),
            "bytes": DB.stat().st_size,
            "mtime": DB.stat().st_mtime,
            "open_mode": "sqlite3 mode=ro&immutable=1 (main db file only; not a transactional live/WAL snapshot)",
        },
        "requirement": rows(cur, "select * from requirements where requirement_id='R18-WP-FHS-17'"),
        "acceptance": rows(cur, "select * from acceptances where acceptance_id in "
                                "('ACC-WP-FHS-17','ACC-WP-FHS-17-V3') "
                                "or acceptance_id like 'ACC-WP-FHS-17-%' order by acceptance_id"),
        "upstream_acceptance": rows(cur, "select * from acceptances where acceptance_id in "
                                        "('ACC-WP-FHS-00','ACC-WP-FHS-02','ACC-WP-FHS-03',"
                                        "'ACC-WP-FHS-02-V2','ACC-WP-FHS-03-V2') "
                                        "order by acceptance_id"),
        "work_queue": rows(cur, "select * from work_queue where wp_id in "
                                "('WP-FHS-00','WP-FHS-02','WP-FHS-03','WP-FHS-06','WP-FHS-17','WP-FHS-13') "
                                "order by wp_id"),
        "taskspecs": rows(cur, "select * from taskspecs where requirement_id='R18-WP-FHS-17' "
                               "or taskspec_id like '%FHS-17%' order by taskspec_id"),
        "native_admission": {
            "lease_rows_total": cur.execute("select count(*) from native_admission_leases").fetchone()[0],
            "nonce_rows_total": cur.execute("select count(*) from native_admission_nonces").fetchone()[0],
            "leases_naming_wp17": rows(cur, "select * from native_admission_leases "
                                            "where resource_id like '%FHS-17%'"),
            "nonces_bound_to_wp17_subject": rows(
                cur, "select * from native_admission_nonces where subject_sha256 like '%FHS%'"),
            "note": ("native_admission_nonces stores (nonce, subject_sha256) only; it has no "
                     "WP-FHS-17 row and no grant payload column, so it cannot admit this operation"),
        },
        "provider_bindings": rows(cur, "select * from provider_bindings "
                                       "where provider_id like '%FHS%' or slot like '%FHS%' "
                                       "order by provider_id, slot"),
        "current_need_search": need_search(cur),
        "notes": [
            "Read-only: no INSERT/UPDATE/DELETE is issued.",
            "ACC-WP-FHS-17-V3 is an owner-ruling text row, not an independent officer oracle.",
            "WAL is not read; a concurrent writer between before/after is not excluded.",
        ],
    }
    p = Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(p), "db_sha256": out["db"]["sha256"],
                      "wp17_state": [r["state"] for r in out["work_queue"] if r["wp_id"] == "WP-FHS-17"],
                      "current_need": out["current_need_search"]["conclusion"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
