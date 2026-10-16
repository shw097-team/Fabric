#!/usr/bin/env python
"""Repair the FAR-20261019 pack prefix: the first push landed under a lower-case `evidence/` root while
the repository's convention (and the previous round's pack) is upper-case `EVIDENCE/`.

One commit: the same 61 blobs re-added under the correct prefix, and the 61 lower-case paths deleted in the
same tree (the Git Trees API deletes a path by giving it sha:null). Then the branch ref is moved and every
file is re-verified by git blob id. Additive in the sense that matters: no other path in the tree is
touched, and `main` is not involved.
"""
import base64, hashlib, json, datetime, urllib.request, urllib.error
from pathlib import Path

TOK = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt").read_text(encoding="utf-8").strip()
REPO = "shw097-team/Fabric"
BRANCH = "evidence/far-019-owner-auth-closure"
OLD_PREFIX = "evidence/FAR-20261019-owner-authorized-closure"
NEW_PREFIX = "EVIDENCE/FAR-20261019-owner-authorized-closure"
ROUND = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")


def api(method, path, body=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=(json.dumps(body).encode() if body is not None else None),
                                 headers={"Authorization": "Bearer " + TOK,
                                          "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "far-019-fix"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


st, ref = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
tip = ref["object"]["sha"]
st, cm = api("GET", f"/repos/{REPO}/git/commits/{tip}")
base_tree = cm["tree"]["sha"]
st, tr = api("GET", f"/repos/{REPO}/git/trees/{tip}?recursive=1")
old_paths = [e["path"] for e in tr["tree"] if e.get("type") == "blob" and e["path"].startswith(OLD_PREFIX + "/")]
print("lower-case blobs to remove:", len(old_paths))

entry = [{"path": p, "mode": "100644", "type": "blob", "sha": None} for p in old_paths]
for f in sorted(ROUND.rglob("*")):
    if not f.is_file():
        continue
    rel = f.relative_to(ROUND).as_posix()
    if {"attempts", "__pycache__"} & set(f.parts) or f.suffix.lower() in {".db", ".pyc", ".log"} \
            or f.name in {"PUBLISH_RECEIPT_019.json", "REMOTE_READBACK_VERIFY_019.json"}:
        continue
    if rel.startswith("lane/") or rel.endswith(".md"):
        continue  # receipts stage owns these
    b = f.read_bytes()
    entry.append({"path": f"{NEW_PREFIX}/{rel}", "mode": "100644", "type": "blob",
                  "content": b.decode("utf-8", errors="surrogateescape")})
st, tree = api("POST", f"/repos/{REPO}/git/trees", {"base_tree": base_tree, "tree": entry})
print("tree:", st, tree.get("sha", tree.get("error", ""))[:50])
st, commit = api("POST", f"/repos/{REPO}/git/commits",
                 {"message": "FAR-20261019: move the pack to the repository's EVIDENCE/ convention "
                             "(the first push used a lower-case evidence/ root); no other path touched",
                  "tree": tree["sha"], "parents": [tip]})
print("commit:", st, commit.get("sha", commit.get("error", ""))[:50])
st, r2 = api("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False})
print("ref:", st)

st, chk = api("GET", f"/repos/{REPO}/git/trees/{commit['sha']}?recursive=1")
remote = {e["path"]: e["sha"] for e in chk["tree"] if e.get("type") == "blob"}
still_old = [p for p in remote if p.startswith(OLD_PREFIX + "/")]


def blob_id(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


match = miss = 0
for f in sorted(ROUND.rglob("*")):
    if not f.is_file():
        continue
    rel = f.relative_to(ROUND).as_posix()
    if {"attempts", "__pycache__"} & set(f.parts) or f.suffix.lower() in {".db", ".pyc", ".log"} \
            or f.name in {"PUBLISH_RECEIPT_019.json", "REMOTE_READBACK_VERIFY_019.json"}:
        continue
    if rel.startswith("lane/") or rel.endswith(".md"):
        continue
    p = f"{NEW_PREFIX}/{rel}"
    if remote.get(p) == blob_id(f.read_bytes()):
        match += 1
    else:
        miss += 1
print(f"readback under new prefix: {match} match, {miss} mismatch, {len(still_old)} stale lower-case paths")
out = {"schema": "FAR-20261019/PREFIX-REPAIR/1", "branch": BRANCH,
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "old_prefix": OLD_PREFIX, "new_prefix": NEW_PREFIX, "removed_lowercase_blobs": len(old_paths),
       "commit": commit.get("sha"), "matches": match, "mismatches": miss,
       "stale_paths_remaining": len(still_old),
       "verdict": "PASS" if miss == 0 and not still_old else "FAIL"}
(ROUND / "PREFIX_REPAIR_019.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("verdict:", out["verdict"])
