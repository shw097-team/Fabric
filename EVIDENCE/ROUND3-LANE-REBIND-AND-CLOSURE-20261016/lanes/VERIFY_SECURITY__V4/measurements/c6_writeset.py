import hashlib, os

R = r"C:\Projects\Agent_Workspace\HG-KSEOS"
O = os.path.join(R, "var", "ROUND3-LANE-REBIND-AND-CLOSURE-20261016")
CAND = os.path.join(O, "candidate")
SUBJ = os.path.join(O, "lanes", "VERIFY_SECURITY", "V4", "work", "subject")
SKIP_DIRS = {"__pycache__", ".pytest_cache", "TEST_RESULTS"}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def collect(root):
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".pyc"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root).replace("\\", "/")
            out[rel] = sha(p)
    return out

for label, a, b in [("candidate_vs_subject", CAND, SUBJ),
                    ("canonical_vs_subject", R, SUBJ)]:
    A = collect(a)
    B = collect(b)
    keys = set(A) | set(B)
    diff = sorted(k for k in keys if A.get(k) != B.get(k))
    print(f"=== {label}: {len(diff)} differing files (A={len(A)} B={len(B)})")
    for k in diff:
        print("   DIFF", k)
