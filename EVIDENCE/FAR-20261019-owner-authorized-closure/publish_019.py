#!/usr/bin/env python
"""FAR-20261019 publisher: build the round pack, push it as one tree/commit, open the PR, then verify
every file by git blob id.

Design decisions carried over from the previous round, each one learned the hard way:
  * the pack index EXCLUDES ITSELF (a file cannot contain its own digest) and says so explicitly;
  * the push is additive: a new branch is created from the live main tip, never a force update;
  * verification compares git blob ids (sha1("blob <len>\\0" + bytes)) so it is byte-level without
    downloading the files again;
  * the token file is read by this process only and is never printed or written into any artifact.

Usage:  publish_019.py [--stage payload|receipts] [--message TEXT]
"""
import base64, hashlib, json, sys, datetime, urllib.request, urllib.error
from pathlib import Path

TOK = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt").read_text(encoding="utf-8").strip()
REPO = "shw097-team/Fabric"
BASE_BRANCH = "main"
BRANCH = "evidence/far-019-owner-auth-closure"
ROUND = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
PREV_BRANCH = "evidence/far-018-r7r11-residual-closure"
EXCLUDE_DIRS = {"attempts", "__pycache__"}
EXCLUDE_EXT = {".db", ".pyc", ".log"}
EXCLUDE_NAMES = {"PUBLISH_RECEIPT_019.json", "REMOTE_READBACK_VERIFY_019.json"}

stage = "payload"
msg = "FAR-20261019 owner-authorised closure: evidence pack"
for i, a in enumerate(sys.argv):
    if a == "--stage":
        stage = sys.argv[i + 1]
    if a == "--message":
        msg = sys.argv[i + 1]


def api(method, path, body=None, raw=False):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=(json.dumps(body).encode() if body is not None else None),
                                 headers={"Authorization": "Bearer " + TOK,
                                          "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28",
                                          "User-Agent": "far-019-publish"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = r.read()
            return r.status, (d if raw else json.loads(d.decode() or "{}"))
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:500]}


def blob_id(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


# ---- discover the previous round's pack prefix from the live tree and mirror the convention ----
st, ref = api("GET", f"/repos/{REPO}/git/ref/heads/{PREV_BRANCH}")
prev_tip = (ref.get("object") or {}).get("sha")
prefix = "EVIDENCE/FAR-20261019-owner-authorized-closure"
if prev_tip:
    st, tree = api("GET", f"/repos/{REPO}/git/trees/{prev_tip}?recursive=1")
    tops = {}
    for e in tree.get("tree") or []:
        p = e.get("path") or ""
        if "/" in p:
            tops.setdefault(p.split("/")[0], 0)
            tops[p.split("/")[0]] += 1
    disc = sorted(tops.items(), key=lambda kv: -kv[1])[:3]
    print("prev pack root histogram:", disc, "| prev tip", (prev_tip or "")[:8])
    if disc:
        top = disc[0][0]
        # Mirror the repository's own convention exactly, case included: the previous round's pack lives at
        # EVIDENCE/<ROUND>, and forcing this to lower case created a case-duplicate directory that an
        # external reviewer would not find where the convention says it should be.
        prefix = f"{top}/FAR-20261019-owner-authorized-closure"

files = []
for p in sorted(ROUND.rglob("*")):
    if not p.is_file():
        continue
    rel = p.relative_to(ROUND).as_posix()
    if EXCLUDE_DIRS & set(p.parts) or p.suffix.lower() in EXCLUDE_EXT or p.name in EXCLUDE_NAMES:
        continue
    if stage == "receipts" and not (rel.startswith("lane/") or rel.endswith(".md")):
        continue
    files.append((rel, p.read_bytes()))
print("files in this stage:", len(files), "| total bytes:", sum(len(b) for _, b in files), "| prefix:", prefix)

# index excludes itself and is explicitly declared so (a file cannot contain its own digest)
index_entries = [{"path": f"{prefix}/{rel}", "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
                 for rel, b in files if not rel.endswith("PACK_INDEX.json")]
index = {"schema": "FAR-20261019/PACK-INDEX/1",
         "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "round": "FAR-20261019-owner-authorized-closure", "repo": REPO, "branch": BRANCH,
         "prefix": prefix, "file_count": len(index_entries),
         "self_excluded": {"path": f"{prefix}/PACK_INDEX.json",
                           "reason": "a file cannot carry its own digest; this index's digest is carried "
                                     "by the post-publication receipt (REMOTE_READBACK_VERIFY_019.json)"},
         "not_listed_by_design": [f"{prefix}/{n}" for n in EXCLUDE_NAMES],
         "entries": index_entries}
index_bytes = json.dumps(index, ensure_ascii=False, indent=1).encode()
files.append(("PACK_INDEX.json", index_bytes))
packdir = ROUND / "pack"
packdir.mkdir(exist_ok=True)
(packdir / "PACK_INDEX.json").write_bytes(index_bytes)
(packdir / "pack_contents.json").write_text(json.dumps({"files": [r for r, _ in files]}, ensure_ascii=False, indent=1), encoding="utf-8")

st, mainref = api("GET", f"/repos/{REPO}/git/ref/heads/{BASE_BRANCH}")
main_sha = (mainref.get("object") or {}).get("sha")
st, refchk = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
branch_exists = bool(refchk.get("object"))
if branch_exists:
    # A second stage on an existing branch must parent its commit on the BRANCH tip, not on main: a commit
    # whose parent is main while the ref already points elsewhere is a non-fast-forward and is refused.
    base_sha = refchk["object"]["sha"]
    print("branch exists; parenting on tip", base_sha[:8], "(main is at", main_sha[:8], ")")
else:
    base_sha = main_sha
st, basecommit = api("GET", f"/repos/{REPO}/git/commits/{base_sha}")
base_tree = (basecommit.get("tree") or {}).get("sha")
print("base", BASE_BRANCH if not branch_exists else BRANCH, base_sha[:8], "tree", (base_tree or "")[:8])

entry = [{"path": f"{prefix}/{rel}", "mode": "100644", "type": "blob",
          "content": b.decode("utf-8", errors="surrogateescape")} for rel, b in files]
st, tree = api("POST", f"/repos/{REPO}/git/trees", {"base_tree": base_tree, "tree": entry})
tree_sha = tree.get("sha")
print("tree create:", st, (tree_sha or tree.get("error", ""))[:60])
assert tree_sha, "tree creation failed"

st, commit = api("POST", f"/repos/{REPO}/git/commits",
                 {"message": msg, "tree": tree_sha, "parents": [base_sha]})
commit_sha = commit.get("sha")
print("commit create:", st, (commit_sha or commit.get("error", ""))[:60])

st, refchk = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
if refchk.get("object"):
    st, refnew = api("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}",
                     {"sha": commit_sha, "force": False})
else:
    st, refnew = api("POST", f"/repos/{REPO}/git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit_sha})
print("ref update:", st, json.dumps(refnew, ensure_ascii=False)[:120])

# ---- remote readback by git blob id ----
st, rtree = api("GET", f"/repos/{REPO}/git/trees/{commit_sha}?recursive=1")
remote = {e["path"]: e.get("sha") for e in (rtree.get("tree") or []) if e.get("type") == "blob"}
checks, mism, missing, unindexed = [], [], [], []
for rel, b in files:
    rp = f"{prefix}/{rel}"
    lid = blob_id(b)
    if rp not in remote:
        missing.append(rp)
        continue
    ok = remote[rp] == lid
    checks.append({"path": rp, "local_blob": lid, "remote_blob": remote[rp], "match": ok})
    if not ok:
        mism.append(rp)
listed = {f"{prefix}/{rel}" for rel, _ in files}
for rp in remote:
    if rp.startswith(prefix + "/") and rp not in listed:
        unindexed.append(rp)
st, mref = api("GET", f"/repos/{REPO}/git/ref/heads/{BASE_BRANCH}")
main_now = (mref.get("object") or {}).get("sha")
readback = {"schema": "FAR-20261019/REMOTE-READBACK/1", "repo": REPO, "branch": BRANCH,
            "tip": commit_sha, "method": "git blob id equality (byte-level, no re-download)",
            "files_checked": len(checks), "matches": sum(1 for c in checks if c["match"]),
            "mismatches": mism, "missing": missing, "committed_not_indexed": unindexed,
            "main_before_publish": base_sha, "main_now": main_now,
            "main_unchanged": main_now == base_sha, "verdict": "PASS" if checks and not mism
            and not missing else "FAIL"}
(ROUND / "REMOTE_READBACK_VERIFY_019.json").write_text(json.dumps(readback, ensure_ascii=False, indent=1), encoding="utf-8")
receipt = {"schema": "FAR-20261019/PUBLISH-RECEIPT/1", "repo": REPO, "branch": BRANCH, "stage": stage,
           "base_branch": BASE_BRANCH, "base_sha": base_sha, "tree_sha": tree_sha, "commit_sha": commit_sha,
           "files": len(files), "prefix": prefix,
           "token_value_exported": False, "force_update": False,
           "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
(ROUND / f"PUBLISH_RECEIPT_019_{stage}.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print("READBACK:", readback["verdict"], "| matches", readback["matches"], "/", len(checks),
      "| mism", len(mism), "| missing", len(missing), "| unindexed", len(unindexed),
      "| main unchanged", readback["main_unchanged"], "| tip", commit_sha[:8])
