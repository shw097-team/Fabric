import json, os, re, base64, hashlib

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
with open(ROOT + "/PHYSICAL_SOURCE_READBACK_MANIFEST.json", encoding="utf-8") as f:
    src_manifest = json.load(f)
missing = src_manifest["missing"]
hash_to_pin = {m["sha256"]: m["filename"] for m in missing}

# Recycle bin scan by bytes
hits = {}
recycle = r"C:\$Recycle.Bin"
if os.path.isdir(recycle):
    for base, dirs, files in os.walk(recycle, onerror=lambda e: None):
        for fn in files:
            p = os.path.join(base, fn)
            try:
                st = os.path.getsize(p)
            except OSError:
                continue
            if st in set(m["bytes"] for m in missing):
                h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                if h in hash_to_pin:
                    hits.setdefault(hash_to_pin[h], []).append(p)
print("RECYCLE_HITS", json.dumps(hits))

# Deep scan everywhere on disk for these exact sizes+hashes
hits2 = {}
scanned = 0
suspects = 0
for d in ["C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes", "C:/Projects", "C:/Users/user/AppData/Roaming"]:
    if os.path.isdir(d):
        for base, dirs, files in os.walk(d, onerror=lambda e: None):
            dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "__pycache__")]
            for fn in files:
                p = os.path.join(base, fn)
                scanned += 1
                try:
                    st = os.path.getsize(p)
                except OSError:
                    continue
                if st in set(m["bytes"] for m in missing):
                    suspects += 1
                    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                    if h in hash_to_pin:
                        hits2.setdefault(hash_to_pin[h], []).append(p)
print("DEEP_SCANNED", scanned, "suspects", suspects, "HITS", json.dumps(hits2))
