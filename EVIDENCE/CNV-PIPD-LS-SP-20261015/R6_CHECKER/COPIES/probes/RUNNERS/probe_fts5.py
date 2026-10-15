"""FAR-SQLite-FTS5 same-subject probe (ACC-013).

Creates a scratch sqlite database, builds an FTS5 virtual table, inserts rows, runs a
MATCH query (positive) and a malformed MATCH query (negative). Scratch file lives under
RAW/. No canonical DB is touched.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

RAW = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/"
           "R6_DELIVERY/RAW")
DB = RAW / "fts5_scratch.sqlite"


def _fresh() -> sqlite3.Connection:
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("CREATE VIRTUAL TABLE docs USING fts5(title, body)")
    con.executemany(
        "INSERT INTO docs(title, body) VALUES (?, ?)",
        [("alpha", "the intake binds every normative claim to a source locator"),
         ("beta", "the compiler refuses an unbound normative claim"),
         ("gamma", "typed refusal instead of untyped traceback")])
    con.commit()
    return con


def positive() -> int:
    con = _fresh()
    rows = con.execute(
        "SELECT title, bm25(docs) AS rank FROM docs WHERE docs MATCH ? ORDER BY rank",
        ("normative",)).fetchall()
    print(json.dumps({"verdict": "FTS5_POSITIVE_OK", "sqlite_version": sqlite3.sqlite_version,
                      "match_term": "normative", "hit_count": len(rows),
                      "hits": [r[0] for r in rows]}, ensure_ascii=False, indent=1))
    con.close()
    return 0


def negative() -> int:
    con = _fresh()
    try:
        con.execute("SELECT title FROM docs WHERE docs MATCH ?", ("AND AND AND",)).fetchall()
    except sqlite3.OperationalError as exc:
        print(json.dumps({"verdict": "FTS5_NEGATIVE_REFUSED",
                          "error_type": type(exc).__name__, "error": str(exc)},
                         ensure_ascii=False, indent=1))
        con.close()
        return 0
    print(json.dumps({"verdict": "FAIL", "probe": "fts5-negative",
                      "detail": "malformed MATCH term was accepted"}))
    con.close()
    return 1


def teardown() -> int:
    for suffix in ("", "-wal", "-shm"):
        p = Path(str(DB) + suffix)
        if p.exists():
            p.unlink()
    print(json.dumps({"verdict": "FTS5_SCRATCH_TEARDOWN_OK"}, ensure_ascii=False))
    return 0


MODES = {"positive": positive, "negative": negative, "teardown": teardown}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "positive"
    fn = MODES.get(mode)
    if fn is None:
        print(f"unknown mode: {mode}", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(fn())
