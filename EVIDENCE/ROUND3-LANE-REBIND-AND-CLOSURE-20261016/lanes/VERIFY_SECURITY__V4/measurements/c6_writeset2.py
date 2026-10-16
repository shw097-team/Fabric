import hashlib, os, json

R = r"C:\Projects\Agent_Workspace\HG-KSEOS"
O = os.path.join(R, "var", "ROUND3-LANE-REBIND-AND-CLOSURE-20261016")
CAND = os.path.join(O, "candidate")

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

rec = json.load(open(os.path.join(O, "PROMOTION_RECEIPT.json"), encoding="utf-8"))
print("outside_write_set_changes:", rec["outside_write_set_changes"])
print("all_oracle_ok:", rec["all_oracle_ok"])
for f in rec["files"]:
    rel = f["file"]
    cand = os.path.join(CAND, rel.replace("/", os.sep))
    canon = os.path.join(R, rel.replace("/", os.sep))
    bak = os.path.join(R, os.path.dirname(rel), f["backup"])
    print(rel)
    print("  candidate_matches_candidate_sha:",
          sha(cand) == f["candidate_sha256"] if os.path.exists(cand) else "MISSING")
    print("  canonical_after_matches:",
          sha(canon) == f["canonical_sha256_after"])
    print("  backup_before_matches_canonical_before:",
          sha(bak) == f["canonical_sha256_before"] if os.path.exists(bak) else "NO_BACKUP")

# enumerate candidate tree (excl TEST_RESULTS/__pycache__) and compare EVERY file to canonical
SKIP = {"__pycache__", ".pytest_cache", "TEST_RESULTS"}
extra_diff = []
n = 0
for dp, dn, fns in os.walk(CAND):
    dn[:] = [d for d in dn if d not in SKIP]
    for fn in fns:
        if fn.endswith(".pyc"):
            continue
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, CAND).replace("\\", "/")
        n += 1
        if not rel.startswith(("scripts/", "src/", "tests/", "config/")):
            extra_diff.append(rel + " (non-product path present in candidate)")
            continue
        cp = os.path.join(R, rel.replace("/", os.sep))
        if not os.path.exists(cp):
            extra_diff.append(rel + " (absent in canonical)")
        elif sha(cp) != sha(p):
            extra_diff.append(rel + " (sha differs from canonical)")
print("candidate_files_scanned:", n)
print("unexpected_candidate_contents:", extra_diff)
