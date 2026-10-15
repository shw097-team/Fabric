import hashlib, json, os

hash_to_pin = {}
with open("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/PHYSICAL_SOURCE_READBACK_MANIFEST.json", encoding="utf-8") as f:
    src_manifest = json.load(f)
for m in src_manifest["missing"]:
    hash_to_pin[m["sha256"]] = m["filename"]
sizes = set(m["bytes"] for m in src_manifest["missing"])

def sha(p):
    h = hashlib.sha256()
    try:
        with open(p, "rb") as f:
            for ch in iter(lambda: f.read(1 << 20), b""):
                h.update(ch)
    except OSError:
        return None
    return h.hexdigest()

hits = {}
scanned = 0
for d in ["C:/Users/user/OneDrive", "C:/Users/user/Documents", "C:/Users/user/Desktop", "C:/Users/user/Downloads", "C:/Projects/Agent_Workspace/_handover"]:
    if os.path.isdir(d):
        for base, dirs, files in os.walk(d, onerror=lambda e: None):
            dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "__pycache__")]
            for fn in files:
                p = os.path.join(base, fn)
                scanned += 1
                try:
                    if os.path.getsize(p) in sizes:
                        h = sha(p)
                        if h and h in hash_to_pin:
                            hits.setdefault(hash_to_pin[h], []).append(p)
                except OSError:
                    pass

print("SCANNED", scanned)
print("USERDIR_HITS", json.dumps(hits))
