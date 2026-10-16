"""Brute-force plausible digest algorithms to reproduce the recorded first-16 '76ec42a0f4c8962c'."""
import hashlib
from pathlib import Path

SUB = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS\var\ROUND3-LANE-REBIND-AND-CLOSURE-20261016\lanes\VERIFY_SECURITY\V4\work\subject")
DIRS = ("scripts", "src", "tests", "config")


def files_all():
    out = []
    for d in DIRS:
        for p in sorted((SUB / d).rglob("*")):
            if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts:
                out.append(p)
    return out


FILES = files_all()
REL = [str(p.relative_to(SUB)).replace("\\", "/") for p in FILES]
SHA = [hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES]
BYTES = [p.read_bytes() for p in FILES]


def _h(*parts):
    h = hashlib.sha256()
    for x in parts:
        h.update(x if isinstance(x, bytes) else x.encode("utf-8"))
    return h.hexdigest()[:16]


cands = {}
# merged sorted relpath variants
by_rel = sorted(zip(REL, SHA, BYTES))
cands["rel_sha_nl"] = _h("".join(r + ":" + s + "\n" for r, s, _ in by_rel))
cands["rel_sha_pipe"] = _h("".join(r + "|" + s + "\n" for r, s, _ in by_rel))
cands["relhash_nl"] = _h("".join(r + "\n" + s + "\n" for r, s, _ in by_rel))
cands["sha_only_concat"] = _h("".join(s for _, s, _ in by_rel))
cands["bytes_concat_sorted"] = _h(b"".join(b for _, _, b in by_rel))
# dir-order then relpath order for bytes
cands["bytes_concat_dirorder"] = _h(b"".join(BYTES))
# per-dir digest then combine
per = {}
for d in DIRS:
    h = hashlib.sha256()
    for p in sorted((SUB / d).rglob("*")):
        if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts:
            h.update(p.read_bytes())
    per[d] = h.hexdigest()
cands["perdir_hex_concat"] = _h("".join(per[d] for d in DIRS))
cands["perdir_dir_colon"] = _h("".join(d + ":" + per[d] + "\n" for d in DIRS))
# per-dir path:sha lines then combine
per2 = {}
for d in DIRS:
    h = hashlib.sha256()
    for p in sorted((SUB / d).rglob("*")):
        if p.is_file() and p.suffix != ".pyc" and "__pycache__" not in p.parts:
            rel = str(p.relative_to(SUB)).replace("\\", "/")
            h.update((rel + ":" + hashlib.sha256(p.read_bytes()).hexdigest()).encode())
    per2[d] = h.hexdigest()
cands["perdir_pathsha_concat"] = _h("".join(per2[d] for d in DIRS))

target = "76ec42a0f4c8962c"
for k, v in sorted(cands.items()):
    print(("MATCH " if v == target else "      ") + k, v)
print("target", target)
print("nfiles", len(FILES))
