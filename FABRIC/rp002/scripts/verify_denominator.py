# -*- coding: utf-8 -*-
"""RP-002 G0 — denominator readback verification (deterministic, offline)."""
import hashlib, json, os, sys

JSONL = r"C:\Projects\Agent_Workspace\Fabric\rp002\G0\RP002_INPUT_DENOMINATOR.jsonl"
SHAFILE = r"C:\Projects\Agent_Workspace\Fabric\rp002\G0\RP002_INPUT_DENOMINATOR.sha256"
TSV = r"C:\Projects\Agent_Workspace\Fabric\rp002\G0\RP002_SOURCE_CLASSIFICATION.tsv"

raw = open(JSONL, "rb").read()
digest = hashlib.sha256(raw).hexdigest()
declared = open(SHAFILE).read().strip()
print("JSONL_BYTES", len(raw))
print("JSONL_SHA256", digest)
print("DECLARED_SHA256", declared)
print("SHA_MATCH", digest == declared)

rows = []
for line in raw.decode("utf-8").splitlines():
    rows.append(json.loads(line))
print("JSONL_ROWS", len(rows))
print("ROWS_UNIQUE_PATHS", len({r["path"] for r in rows}))
print("ROWS_UNIQUE_PATH_ROOT", len({(r["root"], r["path"]) for r in rows}))

# TSV parity
tsv_lines = open(TSV, encoding="utf-8").read().splitlines()
print("TSV_ROWS", len(tsv_lines) - 1)
print("TSV_HEADER", tsv_lines[0])
bad = [l for l in tsv_lines[1:] if len(l.split("\t")) != 8]
print("TSV_BAD_COLUMN_ROWS", len(bad))

# spot-check: longest-path corpus files present + hashed
corpus_rows = [r for r in rows if r["root"] == "CORPUS"]
print("CORPUS_ROWS", len(corpus_rows))
longest = sorted(corpus_rows, key=lambda r: -len(r["path"]))[:3]
for r in longest:
    print("LONGEST", len(r["path"]), r["sha256"][:16], r["path"][-80:])

# verify a sample of hashes against disk (extended path)
import random
random.seed(42)
sample = random.sample(rows, 25)
mismatch = 0
base = {
    "HGK": r"C:\Projects\Agent_Workspace\HG-KSEOS",
    "SQS": r"C:\Projects\Agent_Workspace\SQS-THC",
    "FABRIC": r"C:\Projects\Agent_Workspace\Fabric",
    "CORPUS": r"C:\Projects\Agent_Workspace\教程字幕",
}
for r in sample:
    p = "\\\\?\\" + os.path.join(base[r["root"]], r["path"].replace("/", "\\"))
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h != r["sha256"]:
        mismatch += 1
        print("MISMATCH", r["path"])
print("SAMPLE_MISMATCH", mismatch, "/25")
print("VERDICT", "PASS" if (digest == declared and len(rows) == len({(r['root'], r['path']) for r in rows}) and mismatch == 0 and not bad) else "FAIL")
