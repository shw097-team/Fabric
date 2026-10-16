"""More digest-algorithm variants to reproduce 76ec42a0f4c8962c."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016")
FROZEN = ROOT / "subject"
DIRS = ("scripts", "src", "tests", "config")

FILES = []
for d in DIRS:
    for p in sorted((FROZEN / d).rglob("*")):
        if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts:
            FILES.append(p)

target = "76ec42a0f4c8962c"


def h16(chunks):
    h = hashlib.sha256()
    for c in chunks:
        h.update(c if isinstance(c, bytes) else c.encode("utf-8"))
    return h.hexdigest()


variants = {}
for prefix in ("", "subject/"):
    rels = [prefix + str(p.relative_to(FROZEN)).replace("\\", "/") for p in FILES]
    shas = [hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES]
    variants[f"rel_sha_nl_prefix={prefix!r}"] = h16([r + ":" + s + "\n" for r, s in zip(rels, shas)])
    variants[f"sha_rel_nl_prefix={prefix!r}"] = h16([s + ":" + r + "\n" for r, s in zip(rels, shas)])
    # byte-concat of each file's content, in dir+relpath order
    variants[f"bytes_prefix={prefix!r}"] = h16([p.read_bytes() for p in FILES])
    # per-dir: dir-level sha of "rel:sha\n" then combine
per = {}
for d in DIRS:
    files = [p for p in sorted((FROZEN / d).rglob("*"))
             if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts]
    per[d] = h16([str(p.relative_to(FROZEN)).replace("\\", "/") + ":"
                  + hashlib.sha256(p.read_bytes()).hexdigest() + "\n" for p in files])
variants["perdir_pathsha_then_concat"] = h16([per[d] for d in DIRS])
variants["perdir_pathsha_join|"] = h16(["|".join(per[d] for d in DIRS)])

for k, v in sorted(variants.items()):
    print(("MATCH " if v[:16] == target else "      ") + k, v[:16], "...", v[-8:])
print("target", target)
