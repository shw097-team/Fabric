"""Broad brute force over hash fn + serialization to reproduce 76ec42a0f4c8962c."""
import hashlib
import os
from pathlib import Path

COPY = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\lanes\VERIFY_SECURITY\V4\work\subject")
DIRS = ("scripts", "src", "tests", "config")
TARGET = "76ec42a0f4c8962c"


def walk_files(base, order):
    if order == "sorted":
        seq = []
        for d in DIRS:
            seq += [p for p in sorted((base / d).rglob("*"))
                    if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts]
        return seq
    # os.walk order
    seq = []
    for d in DIRS:
        for dp, dns, fns in os.walk(base / d):
            if "__pycache__" in dp:
                continue
            for fn in fns:
                if fn.endswith(".pyc"):
                    continue
                seq.append(Path(dp) / fn)
    return seq


def tryall(name, data):
    for hn, fn in (("sha256", hashlib.sha256), ("sha1", hashlib.sha1),
                   ("md5", hashlib.md5), ("blake2b", hashlib.blake2b),
                   ("blake2s", hashlib.blake2s), ("sha512", hashlib.sha512),
                   ("sha3_256", hashlib.sha3_256)):
        h = fn()
        h.update(data)
        d = h.hexdigest()
        if d[:16] == TARGET or d[-16:] == TARGET:
            print("MATCH", name, hn, d)


for order in ("sorted", "walk"):
    files = walk_files(COPY, order)
    rels = [str(p.relative_to(COPY)).replace("\\", "/") for p in files]
    shas = [hashlib.sha256(p.read_bytes()).hexdigest() for p in files]
    bytes_all = b"".join(p.read_bytes() for p in files)
    tryall(f"{order}:bytes", bytes_all)
    tryall(f"{order}:rel_sha_nl", "".join(r + ":" + s + "\n" for r, s in zip(rels, shas)).encode())
    tryall(f"{order}:sha_rel_nl", "".join(s + ":" + r + "\n" for r, s in zip(rels, shas)).encode())
    tryall(f"{order}:rel_nl_sha", "".join(r + "\n" + s + "\n" for r, s in zip(rels, shas)).encode())
    tryall(f"{order}:sha_concat", "".join(shas).encode())
    tryall(f"{order}:rel_concat", "".join(rels).encode())

# per-dir concat digests combined
per = {}
for d in DIRS:
    files = [p for p in sorted((COPY / d).rglob("*"))
             if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts]
    per[d] = hashlib.sha256(b"".join(p.read_bytes() for p in files)).hexdigest()
tryall("perdir_concat", "".join(per[d] for d in DIRS).encode())
tryall("perdir_nl", "".join(per[d] + "\n" for d in DIRS).encode())
print("done", TARGET)
