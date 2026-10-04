# -*- coding: utf-8 -*-
"""RP-002 K1 — INDEPENDENT re-derivation from raw corpus (fresh read-only, maker != checker)."""
import hashlib, json, os, random, sqlite3, sys
from pathlib import Path

CORPUS = Path(r"C:\Projects\Agent_Workspace\教程字幕")
K1 = Path(r"C:\Projects\Agent_Workspace\Fabric\rp002\K1")
DB = r"C:\Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db"

def ext(p):
    ap = os.path.abspath(str(p))
    return ap if ap.startswith("\\\\?\\") else "\\\\?\\" + ap.replace("/", "\\")

results = []
def check(name, ok, detail):
    results.append({"id": name, "pass": bool(ok), "detail": detail})

# 1. Re-walk corpus: count + bytes, compare to governance totals
n = 0
b = 0
for dp, dn, fn in os.walk(CORPUS):
    dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
    for f in fn:
        if f.endswith((".pyc", ".pyo")):
            continue
        p = Path(dp) / f
        n += 1
        b += os.path.getsize(ext(p))
gov = json.loads((K1 / "RP002_K1_CORPUS_GOVERNANCE.json").read_text(encoding="utf-8"))
check("K1I_REWALK_TOTAL", n == gov["total_files"] == 4717, f"walk={n} gov={gov['total_files']}")
check("K1I_REWALK_BYTES", b == gov["total_bytes"], f"walk={b} gov={gov['total_bytes']}")

# 2. Sample-hash 30 files from governance vs disk
rows = (K1 / "RP002_K1_SOURCE_CLASSIFICATION.tsv").read_text(encoding="utf-8").splitlines()[1:]
samples = random.Random(7).sample(rows, 30)
mm = 0
for row in samples:
    parts = row.split("\t")
    rel, sha = parts[0], parts[2]
    p = Path(ext(CORPUS / rel))
    if hashlib.sha256(p.read_bytes()).hexdigest() != sha:
        mm += 1
check("K1I_SAMPLE_HASH_30", mm == 0, f"mismatch={mm}/30")

# 3. Status-state consistency: KEEP_CANONICAL==CURRENT count, DUP==CONDITIONAL count
disp_ok = gov["disposition_counts"]["KEEP_CANONICAL"] == gov["status_counts"]["CURRENT"] == 2992
disp_ok = disp_ok and gov["disposition_counts"]["DUP_EXACT"] == gov["status_counts"]["CONDITIONAL"] == 1694
check("K1I_DISPOSITION_STATUS_CONSISTENT", disp_ok, str(gov["disposition_counts"]))

# 4. Dedup TSV row parity
tsv_rows = len((K1 / "RP002_K1_CORPUS_DEDUP.tsv").read_text(encoding="utf-8").splitlines()) - 1
check("K1I_DEDUP_TSV_PARITY", tsv_rows == gov["disposition_counts"]["DUP_EXACT"] == 1694, f"tsv={tsv_rows}")

# 5. Every distilled norm locator sha256 exists in classification (source-bound, no invented norm)
dist = json.loads((K1 / "RP002_K1_DISTILLATION.json").read_text(encoding="utf-8"))
known = {r.split("\t")[2] for r in rows}
missing = 0
for norm in dist["distilled_norms"]:
    for loc in norm["source_locators"]:
        if loc["sha256"] not in known:
            missing += 1
check("K1I_NORM_LOCATORS_REAL", missing == 0, f"missing={missing}")

# 6. Requirement ledger: 18 REQ-RP2-* in spine
con = sqlite3.connect(DB)
n_req = con.execute("SELECT COUNT(*) FROM requirements WHERE project_id='HGK-REFERENCE-PROJECT-002' AND requirement_id LIKE 'REQ-RP2-%'").fetchone()[0]
con.close()
check("K1I_SPINE_REQS_18", n_req == 18, f"rows={n_req}")

verdict = "PASS" if all(c["pass"] for c in results) else "FAIL"
out = {"artifact_id": "RP002_K1_INDEPENDENT_REDERIVE", "verdict": verdict, "checks": results}
(K1 / "RP002_K1_INDEPENDENT_REDERIVE.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
sys.exit(0 if verdict == "PASS" else 1)
