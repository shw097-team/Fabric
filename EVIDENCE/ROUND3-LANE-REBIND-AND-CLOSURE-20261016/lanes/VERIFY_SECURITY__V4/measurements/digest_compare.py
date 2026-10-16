"""Compare frozen subject tree vs the lane COPY; and try more digest algorithms."""
import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016")
FROZEN = ROOT / "subject"
COPY = ROOT / "lanes" / "VERIFY_SECURITY" / "V4" / "work" / "subject"
DIRS = ("scripts", "src", "tests", "config")


def relset(base):
    s = {}
    for d in DIRS:
        for p in (base / d).rglob("*"):
            if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts:
                s[str(p.relative_to(base)).replace("\\", "/")] = hashlib.sha256(p.read_bytes()).hexdigest()
    return s


fz = relset(FROZEN)
cp = relset(COPY)
print("frozen files", len(fz), "copy files", len(cp))
print("only_in_frozen", sorted(set(fz) - set(cp)))
print("only_in_copy", sorted(set(cp) - set(fz)))
print("differing", sorted(k for k in set(fz) & set(cp) if fz[k] != cp[k]))


def agg(fileset, style, subset=None):
    keys = sorted(fileset) if subset is None else subset
    h = hashlib.sha256()
    for k in keys:
        if style == "pathsha":
            h.update((k + ":" + fileset[k] + "\n").encode())
        elif style == "pathsha_no_nl":
            h.update((k + ":" + fileset[k]).encode())
        elif style == "path_sha_space":
            h.update((k + " " + fileset[k] + "\n").encode())
        elif style == "sha_path":
            h.update((fileset[k] + " " + k + "\n").encode())
        elif style == "sha_only":
            h.update(fileset[k].encode())
    return h.hexdigest()


target = "76ec42a0f4c8962c"
for name, fs in (("frozen", fz), ("copy", cp)):
    for st in ("pathsha", "pathsha_no_nl", "path_sha_space", "sha_path", "sha_only"):
        g = agg(fs, st)
        print(("MATCH " if g[:16] == target else "      ") + name, st, g[:16])
