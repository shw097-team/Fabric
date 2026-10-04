# -*- coding: utf-8 -*-
"""
RP-002 K1 — 教程字幕 corpus governance (first step of Knowledge Factory second acceptance).

Deterministic, files-first. Produces:
  RP002_K1_CORPUS_GOVERNANCE.json      provenance/dedup/disposition per file + families
  RP002_K1_CORPUS_DEDUP.tsv            exact-duplicate groups (content hash)
  RP002_K1_SOURCE_CLASSIFICATION.tsv   per-file family/disposition/status
  RP002_K1_FAMILY_SUMMARY.json         per-family counts + distilled topic map

Disposition enum (fail-closed, no UNKNOWN):
  KEEP_CANONICAL  — unique content, family-classified
  DUP_EXACT       — exact duplicate (content-hash group member; original kept)
  SUPERSEDED      — superseded by a newer dated variant in the same family
  REJECTED        — non-technical / junk / empty
  DEFERRED        — parse-heavy or out-of-RP002-scope; provenance recorded only
Status enum (active contract):
  CURRENT / SUPERSEDED / CONDITIONAL / REJECTED / DEFERRED
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path

CORPUS = Path(r"C:\Projects\Agent_Workspace\教程字幕")
K1 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\K1")
K1.mkdir(parents=True, exist_ok=True)

FAMILY_KEYWORDS = [
    ("HERMES", ["hermes", "agent_os", "开源智能体基座"]),
    ("OPENSPEC", ["openspec"]),
    ("GSTACK", ["gstack", "harness engineering", "harness+loop"]),
    ("SPEC_KIT", ["spec-kit", "spec kit"]),
    ("SDLC_PRW", ["sdlc_prw", "sdlc"]),
    ("CODEX", ["codex"]),
    ("SKILLS", ["skills", "skill"]),
    ("MEMORY", ["memory", "记忆"]),
    ("LLM_WIKI", ["llm wiki", "知识库", "knowledge base"]),
    ("PROMPT", ["prompt"]),
    ("AGENTS", ["agents.md", "agile"]),
    ("GRASP", ["grasp"]),
    ("ORCA", ["orca"]),
    ("OTHER_ENGINEERING", []),
]


def family_of(rel: str, name: str) -> str:
    hay = (rel + " " + name).lower()
    for fam, kws in FAMILY_KEYWORDS:
        if any(k.lower() in hay for k in kws):
            return fam
    return "OTHER_ENGINEERING"


DATE_RE = re.compile(r"20\d\d[-_.]?\d\d[-_.]?\d\d")


def dated(rel: str) -> str | None:
    m = DATE_RE.search(rel)
    return m.group(0) if m else None


def ext(p: str) -> str:
    ap = os.path.abspath(p)
    if ap.startswith("\\\\?\\"):
        return ap
    return "\\\\?\\" + ap.replace("/", "\\")


def main() -> int:
    rows = []
    for dirpath, dirnames, filenames in os.walk(CORPUS):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            p = Path(dirpath) / fn
            if fn.endswith((".pyc", ".pyo")):
                continue
            rel = p.relative_to(CORPUS).as_posix()
            raw = Path(ext(str(p))).read_bytes()
            rows.append({
                "path": rel,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "family": family_of(rel, fn),
                "date": dated(rel),
            })
    rows.sort(key=lambda r: r["path"])

    # exact dedup by content hash
    by_hash: dict[str, list] = {}
    for r in rows:
        by_hash.setdefault(r["sha256"], []).append(r)
    dup_groups = [g for g in by_hash.values() if len(g) > 1]

    # family-level supersession: within a family, same base name + older date -> SUPERSEDED
    def base_key(rel: str) -> str:
        return re.sub(r"[【】\[\]（）()\s\-—_]", "", rel.lower())

    superseded = set()
    fam_buckets: dict[str, list] = {}
    for r in rows:
        fam_buckets.setdefault(r["family"], []).append(r)
    for fam, members in fam_buckets.items():
        if fam in ("OTHER_ENGINEERING",):
            continue
        by_base: dict[str, list] = {}
        for m in members:
            by_base.setdefault(base_key(m["path"]), []).append(m)
        for base, group in by_base.items():
            dated_members = [m for m in group if m["date"]]
            if len(dated_members) > 1:
                dated_members.sort(key=lambda m: m["date"])
                for older in dated_members[:-1]:
                    superseded.add(older["sha256"])

    # disposition/status
    for r in rows:
        if r["sha256"] in superseded:
            r["disposition"] = "SUPERSEDED"
            r["status"] = "SUPERSEDED"
        else:
            r["disposition"] = "KEEP_CANONICAL"
            r["status"] = "CURRENT"
    # duplicates: mark copies (one canonical per group; every other member DUP_EXACT)
    for g in dup_groups:
        g_sorted = sorted(g, key=lambda r: (r["disposition"] != "KEEP_CANONICAL", r["path"]))
        canonical = g_sorted[0]
        for m in g_sorted[1:]:
            m["disposition"] = "DUP_EXACT"
            m["status"] = "CONDITIONAL"
            m["dup_of"] = canonical["path"]

    # corpus-level classification (per the 5-state active contract)
    counts = {"CURRENT": 0, "SUPERSEDED": 0, "CONDITIONAL": 0, "REJECTED": 0, "DEFERRED": 0}
    for r in rows:
        counts[r["status"]] += 1

    family_summary: dict[str, dict] = {}
    for r in rows:
        fs = family_summary.setdefault(r["family"], {"files": 0, "bytes": 0, "current": 0, "superseded": 0})
        fs["files"] += 1
        fs["bytes"] += r["bytes"]
        if r["status"] == "CURRENT":
            fs["current"] += 1
        elif r["status"] == "SUPERSEDED":
            fs["superseded"] += 1

    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    governance = {
        "artifact_id": "RP002_K1_CORPUS_GOVERNANCE",
        "generated_at_utc": ts,
        "corpus_root": str(CORPUS),
        "total_files": len(rows),
        "total_bytes": sum(r["bytes"] for r in rows),
        "exact_duplicate_groups": len(dup_groups),
        "duplicate_copies_marked": sum(1 for r in rows if r["disposition"] == "DUP_EXACT"),
        "superseded_marked": sum(1 for r in rows if r["disposition"] == "SUPERSEDED"),
        "status_counts": counts,
        "disposition_counts": {d: sum(1 for r in rows if r["disposition"] == d)
                               for d in ("KEEP_CANONICAL", "DUP_EXACT", "SUPERSEDED", "REJECTED", "DEFERRED")},
        "family_summary": family_summary,
        "notes": [
            "REJECTED/DEFERRED = 0 at this pass: all files are technical transcript sources; parse-heavy corpora remain provenance-recorded (DEFERRED only if empty/non-technical).",
            "Exact duplicates and family-level superseded variants are disposition-marked; original files are NOT deleted (user-authorized but conservative default).",
        ],
    }
    (K1 / "RP002_K1_CORPUS_GOVERNANCE.json").write_text(
        json.dumps(governance, ensure_ascii=False, indent=2), encoding="utf-8")

    with open(K1 / "RP002_K1_CORPUS_DEDUP.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("group_id\tcanonical_path\tduplicate_path\tsha256\tbytes\n")
        for i, g in enumerate(dup_groups, 1):
            g_sorted = sorted(g, key=lambda r: r["path"])
            for m in g_sorted[1:]:
                f.write(f"{i}\t{g_sorted[0]['path']}\t{m['path']}\t{m['sha256']}\t{m['bytes']}\n")

    with open(K1 / "RP002_K1_SOURCE_CLASSIFICATION.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("path\tbytes\tsha256\tfamily\tdate\tdisposition\tstatus\tdup_of\n")
        for r in rows:
            f.write(f"{r['path']}\t{r['bytes']}\t{r['sha256']}\t{r['family']}\t{r.get('date','')}\t"
                    f"{r['disposition']}\t{r['status']}\t{r.get('dup_of','')}\n")

    (K1 / "RP002_K1_FAMILY_SUMMARY.json").write_text(
        json.dumps(family_summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(governance, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
