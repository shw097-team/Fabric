# -*- coding: utf-8 -*-
"""
RP-002 G0 — deterministic full material-source denominator builder (Windows-native, offline).

Produces:
  RP002_INPUT_DENOMINATOR.jsonl            one JSON object per material file
  RP002_INPUT_DENOMINATOR.sha256           sha256 of the jsonl (canonical artifact hash)
  RP002_SOURCE_CLASSIFICATION.tsv          per-file authority/classification projection
  RP002_DENOMINATOR_SUMMARY.json           counts + excluded-family aggregate identities

Policy (explicit, fail-closed):
  INCLUDE  : every file under the four declared roots EXCEPT the exclusion families below.
  EXCLUDE  : .git internals (identity recorded separately via git HEAD/status)
             __pycache__ / *.pyc / .venv / node_modules
             vendored toolchain dirs (hermes-v020 repo+venv, hermes-disposable,
             opencodex-backup, codex-relay)  -> identity pinned by config/hermes.json commit
             HGK var/workbench (derived wiki/compiler output), var/backups, var/rollback-proof
             SQS 技術資料庫/台股價格歷史資料 (raw market data; aggregate identity only)
             Fabric rp002/** and Fabric evidence/** (RP-002 OUTPUT tree, not input)
  Aggregate identity for excluded families: tree hash over sorted (relpath, bytes) rows.

Classification families (source_family):
  PROMPT/BLUEPRINT/CONTROL/CODE/TEST/TOOL/SCRIPT/EVIDENCE/DOCS/DATA/CORPUS/RUNTIME/VENDOR/DERIVED
Authority rank:
  A0 user prompt / A1 blueprint+discussions / A2 HGK controls / A3 SQS controls /
  A4 admitted runtime contracts / A5 local readback+raw evidence / SUPPORT external corpus
Disposition: INCLUDE / EXCLUDED_VENDOR / EXCLUDED_DERIVED / EXCLUDED_RAW_DATA / EXCLUDED_GIT / EXCLUDED_OUTPUT
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOTS = {
    "HGK": r"C:\Projects\Agent_Workspace\HG-KSEOS",
    "SQS": r"C:\Projects\Agent_Workspace\SQS-THC",
    "FABRIC": r"C:\Projects\Agent_Workspace\Fabric",
    "CORPUS": r"C:\Projects\Agent_Workspace\教程字幕",
}
# Windows long-path support: operate on \\?\ extended absolute paths internally,
# but emit clean relative paths in artifacts.
def ext(p: str) -> str:
    ap = os.path.abspath(p)
    if ap.startswith("\\\\?\\"):
        return ap
    return "\\\\?\\" + ap.replace("/", "\\")
OUT_DIR = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\G0")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSONL = OUT_DIR / "RP002_INPUT_DENOMINATOR.jsonl"
SHAFILE = OUT_DIR / "RP002_INPUT_DENOMINATOR.sha256"
TSV = OUT_DIR / "RP002_SOURCE_CLASSIFICATION.tsv"
SUMMARY = OUT_DIR / "RP002_DENOMINATOR_SUMMARY.json"

EXCLUDED_DIR_NAMES = {".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDED_EXT = {".pyc", ".pyo"}
# vendored / derived / raw-data exclusion: (root, relative_dir_prefix) -> reason
EXCLUDED_PREFIXES = {
    ("HGK", "var/hermes-v020/repo"): "VENDOR_hermes_source_pinned_by_config_commit",
    ("HGK", "var/hermes-v020/venv"): "VENDOR_python_venv",
    ("HGK", "var/hermes-disposable"): "VENDOR_disposable_qual_home",
    ("HGK", "var/opencodex-backup"): "VENDOR_tool_install_backup",
    ("HGK", "var/codex-relay"): "VENDOR_runtime_relay",
    ("HGK", "var/workbench"): "DERIVED_llm_wiki_compiler_output",
    ("HGK", "var/backups"): "DERIVED_sqlite_backups",
    ("HGK", "var/rollback-proof"): "DERIVED_rollback_drill_output",
    ("SQS", "技術資料庫/台股價格歷史資料"): "RAW_DATA_market_price_history",
    ("FABRIC", "rp002"): "OUTPUT_rp002_tree",
    ("FABRIC", "evidence"): "OUTPUT_evidence_tree",
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(root_name: str, rel: str) -> dict:
    rel_l = rel.lower()
    fam = "DOCS"
    if rel_l.endswith((".py", ".js", ".ts", ".tsx", ".json", ".yaml", ".yml", ".toml", ".sql")):
        fam = "CODE"
    elif rel_l.endswith((".md", ".txt", ".rst")):
        fam = "DOCS"
    elif rel_l.endswith((".csv", ".jsonl", ".tsv", ".parquet", ".db", ".sqlite")):
        fam = "DATA"
    elif rel_l.endswith((".ps1", ".sh", ".bat", ".cmd")):
        fam = "SCRIPT"
    elif rel_l.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif", ".ico", ".pdf", ".docx", ".xlsx", ".pptx", ".zip")):
        fam = "ASSET"
    if root_name == "CORPUS":
        fam = "CORPUS"
    if root_name == "FABRIC" and "/RP-002_DOC/" in "/" + rel.replace("\\", "/") + "/":
        fam = "BLUEPRINT"
    if "/control/" in "/" + rel.replace("\\", "/") + "/":
        fam = "CONTROL"
    if rel_l.startswith(("test", "/test", "tests/")) or "/tests/" in "/" + rel_l:
        fam = "TEST"
    if "/evidence/" in "/" + rel.replace("\\", "/") + "/" or "/evidence" == "/" + rel.replace("\\", "/")[: -len(rel) + len(rel)]:
        fam = "EVIDENCE"
    if root_name == "HGK" and rel_l.startswith(("var/", "tools/", "scripts/", "src/", "registries/")):
        fam = {"var/": "RUNTIME", "tools/": "TOOL", "scripts/": "SCRIPT", "src/": "CODE", "registries/": "CONTROL"}[rel_l.split("/")[0] + "/"]
    if root_name == "SQS" and rel_l.startswith(("src/", "scripts/", "adapters/", "contracts/", "schemas/")):
        fam = "CODE"
    if root_name == "SQS" and rel_l.startswith(("requirements/", "docs/", "SSOT/", "risk/", "research/")):
        fam = "CONTROL" if rel_l.startswith(("requirements/", "SSOT/")) else "DOCS"

    rank = "SUPPORT"
    if root_name == "CORPUS":
        rank = "SUPPORT"
    elif root_name == "FABRIC":
        if fam == "BLUEPRINT":
            rank = "A1"
        elif rel_l.startswith("oracle/"):
            rank = "A1"
        else:
            rank = "A5"
    elif root_name == "HGK":
        if rel_l.startswith(("control/", "registries/", "requirements/", "source-freeze/")):
            rank = "A2"
        elif rel_l.startswith(("config/", "AGENTS.md", "pyproject.toml")):
            rank = "A4"
        elif rel_l.startswith(("evidence/", "var/", "release/", "worktrees/")):
            rank = "A5"
        else:
            rank = "A5"
    elif root_name == "SQS":
        if rel_l.startswith(("requirements/", "SSOT/", "contracts/")):
            rank = "A3"
        elif rel_l.startswith(("docs/", "risk/", "research/", "schemas/")):
            rank = "A3"
        else:
            rank = "A5"
    return {"family": fam, "rank": rank}


def tree_rows_of_excluded(root: Path, rel_prefix: str):
    """Deterministic (relpath, bytes) rows for an excluded subtree (no content read)."""
    base = root / rel_prefix
    rows = []
    if base.is_dir():
        for dirpath, dirnames, filenames in os_walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIR_NAMES]
            dp = Path(dirpath)
            for fn in filenames:
                p = dp / fn
                if p.suffix.lower() in EXCLUDED_EXT:
                    continue
                rows.append((p.relative_to(root).as_posix(), p.stat().st_size))
    elif base.is_file():
        rows.append((rel_prefix, base.stat().st_size))
    return rows


def walk(root_name: str, root: Path):
    """Yield (root_name, rel, abs_path) for included files; collect excluded aggregates."""
    excluded_agg = {}
    prefix_map = {r: reason for (rn, r), reason in EXCLUDED_PREFIXES.items() if rn == root_name}
    for dirpath, dirnames, filenames in os_walk(root):
        dp = Path(dirpath)
        rel_dir = dp.relative_to(root).as_posix()
        # prune excluded dirs
        keep = []
        for d in dirnames:
            if d in EXCLUDED_DIR_NAMES:
                continue
            rel_child = f"{rel_dir}/{d}" if rel_dir != "." else d
            if rel_child in prefix_map:
                excluded_agg.setdefault(prefix_map[rel_child], []).extend(
                    tree_rows_of_excluded(root, rel_child))
                continue
            keep.append(d)
        dirnames[:] = keep
        for fn in filenames:
            if Path(fn).suffix.lower() in EXCLUDED_EXT:
                continue
            rel = f"{rel_dir}/{fn}" if rel_dir != "." else fn
            if any(rel.startswith(pref + "/") or rel == pref for pref in prefix_map):
                continue
            yield root_name, rel, dp / fn
    for reason, rows in excluded_agg.items():
        yield ("__EXCLUDED__", reason, rows)


def main() -> int:
    import os
    global os_walk
    os_walk = os.walk
    all_rows = []
    excluded_rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = []
        for root_name, root in ROOTS.items():
            for item in walk(root_name, Path(ext(root))):
                if item[0] == "__EXCLUDED__":
                    excluded_rows.append(item)
                else:
                    futs.append(ex.executor_submit if False else ex.submit(process_file, *item))
        for fut in as_completed(futs):
            all_rows.append(fut.result())

    all_rows.sort(key=lambda r: (r["root"], r["path"]))
    with open(JSONL, "w", encoding="utf-8", newline="\n") as f:
        for row in all_rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    digest = sha256_file(JSONL)
    SHAFILE.write_text(digest + "\n", encoding="ascii")

    with open(TSV, "w", encoding="utf-8", newline="\n") as f:
        f.write("path\tbytes\tsha256\troot\tsource_family\tauthority_rank\tdisposition\tlocator_status\n")
        for row in all_rows:
            f.write(f"{row['path']}\t{row['bytes']}\t{row['sha256']}\t{row['root']}\t"
                    f"{row['family']}\t{row['rank']}\tINCLUDE\tOK\n")

    # excluded aggregate identities
    agg = []
    for _marker, reason, rows in excluded_rows:
        h = hashlib.sha256()
        cnt = 0
        tot = 0
        for rel, b in rows:
            h.update(f"{rel}\t{b}\n".encode("utf-8"))
            cnt += 1
            tot += b
        agg.append({"family_reason": reason, "file_count": cnt, "bytes_total": tot,
                    "tree_identity": h.hexdigest(),
                    "sample_paths": [r for r, _ in sorted(rows)[:3]]})
    summary = {
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "roots": {k: str(v) for k, v in ROOTS.items()},
        "included_file_count": len(all_rows),
        "included_bytes_total": sum(r["bytes"] for r in all_rows),
        "denominator_jsonl": str(JSONL),
        "denominator_jsonl_sha256": digest,
        "classification_tsv": str(TSV),
        "excluded_families": agg,
        "policy": "INCLUDE all material source under 4 roots except .git/__pycache__/.venv/node_modules/*.pyc, "
                  "vendored toolchains (pinned by config commit), derived wiki/backup dirs, raw market data, "
                  "and Fabric rp002/**+evidence/** output trees (recorded as aggregate identities).",
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def process_file(root_name: str, rel: str, p: Path) -> dict:
    st = p.stat()
    cl = classify(root_name, rel)
    return {
        "root": root_name,
        "path": rel,
        "bytes": st.st_size,
        "mtime_utc": st.st_mtime_ns,
        "sha256": sha256_file(p),
        "family": cl["family"],
        "rank": cl["rank"],
    }


if __name__ == "__main__":
    sys.exit(main())
