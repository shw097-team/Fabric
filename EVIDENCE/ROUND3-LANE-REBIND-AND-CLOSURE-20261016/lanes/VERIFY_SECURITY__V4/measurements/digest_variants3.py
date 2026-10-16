"""Try composite-schema digest variants using per-dir digests + counts to hit 76ec42a0f4c8962c."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016")
FROZEN = ROOT / "subject"
DIRS = ("scripts", "src", "tests", "config")

per = {}
cnt = {}
for d in DIRS:
    files = [p for p in sorted((FROZEN / d).rglob("*"))
             if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts]
    h = hashlib.sha256()
    for p in files:
        h.update(p.read_bytes())
    per[d] = h.hexdigest()
    cnt[d] = len(files)

target = "76ec42a0f4c8962c"


def h16(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


cands = {}
cands["dir|count|digest nl"] = h16("".join(f"{d}|{cnt[d]}|{per[d]}\n" for d in DIRS))
cands["dir:count:digest nl"] = h16("".join(f"{d}:{cnt[d]}:{per[d]}\n" for d in DIRS))
cands["dir=count=digest nl"] = h16("".join(f"{d}={cnt[d]}={per[d]}\n" for d in DIRS))
cands["count+digest nl"] = h16("".join(f"{cnt[d]}{per[d]}\n" for d in DIRS))
cands["digest nl"] = h16("".join(per[d] + "\n" for d in DIRS))
cands["digest concat"] = h16("".join(per[d] for d in DIRS))
cands["json each"] = json.dumps({d: {"files": cnt[d], "digest": per[d]} for d in DIRS}, sort_keys=True)
cands["json each digest"] = h16(cands["json each"])
cands["json schema+dirs"] = h16(json.dumps(
    {"schema": "HGK-ROUND3-SUBJECT-DIGEST/1", "counts": cnt, "total": sum(cnt.values()),
     "digest": None}))
cands["count:digest nl"] = h16("".join(f"{cnt[d]}:{per[d]}\n" for d in DIRS))
cands["dir_digest_space"] = h16(" ".join(f"{d} {per[d]}" for d in DIRS))

for k, v in sorted(cands.items()):
    print(("MATCH " if v[:16] == target else "      ") + k, v[:16])
print("target", target)
print("per", json.dumps(per, indent=1))
print("cnt", cnt)
