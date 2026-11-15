#!/usr/bin/env python
"""CNV-FAR018-FAR019-ARCHIVE-20261016 | A07 remote publisher + per-blob readback.

Publishes THIS round's return pack to its own new EVIDENCE prefix on a DEDICATED branch and opens a pull
request.  main is never written directly (the order forbids it) — the archive of this round's own
evidence follows the same shape the three archived rounds did: branch + pull request, reviewable.

Discipline carried from the previous round's measured failures:
  * PACK_INDEX.json excludes its own digest (a file cannot carry its own hash) and covers the WHOLE pack,
    payload and receipts alike, because a stage-scoped index left 52 files unindexed last time.
  * Readback is per blob: sha1(b"blob %d\\0" % len + bytes) recomputed locally and compared against the
    remote tree, not against this script's own claims.
  * The credential is read by this process only and is never printed or written.
"""
import base64, hashlib, json, datetime, urllib.request, urllib.error
from pathlib import Path

ROUND = "CNV-FAR018-FAR019-ARCHIVE-20261016"
OUT = Path("C:/Projects/Agent_Workspace/_handover") / ROUND
PREFIX = "EVIDENCE/%s/" % ROUND
BRANCH = "evidence/cnv-far018-far019-archive"
REPO = "shw097-team/Fabric"
TOK = open("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt", encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "User-Agent": "hgk-archive-round", "Accept": "application/vnd.github+json"}
MODE = "--apply" in __import__("sys").argv
GEN = datetime.datetime.now(datetime.timezone.utc).isoformat()
SKIP = {".db", ".sqlite", ".pyc"}
EXCLUDE_NAMES = {"REMOTE_READBACK_ARCHIVE.json", "PUBLISH_RECEIPT_ARCHIVE.json", "PACK_INDEX.json"}


def api(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.github.com" + path, headers=H, method=method, data=data)
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=180) as f:
            return f.status, json.loads(f.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {"raw": "unparseable"}


def git_blob_sha(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


# ---- the publication set: this round's own records, whole-tree, minus derived receipts
files = {}
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.suffix not in SKIP and p.name not in EXCLUDE_NAMES:
        files[PREFIX + p.name] = p.read_bytes()
for p in sorted((OUT / "compiler").rglob("*")):
    if p.is_file() and "out" in p.parts and p.suffix in (".json", ".md"):
        files[PREFIX + "compiler/out/" + p.name] = p.read_bytes()
for p in sorted((OUT / "logger").rglob("*")) if (OUT / "logger").exists() else []:
    if p.is_file():
        files[PREFIX + "logger/" + p.name] = p.read_bytes()

index = {"schema": "CNV-ARCHIVE-PACK-INDEX/1", "round": ROUND, "generated_utc": GEN,
         "prefix": PREFIX, "self_excluded": ["PACK_INDEX.json"],
         "note": "PACK_INDEX.json cannot carry its own digest; its digest is bound by the publish receipt.",
         "file_count": len(files),
         "files": [{"path": k[len(PREFIX):], "bytes": len(v), "sha256": hashlib.sha256(v).hexdigest()}
                   for k, v in sorted(files.items())]}
files[PREFIX + "PACK_INDEX.json"] = json.dumps(index, ensure_ascii=False, indent=1).encode()

st, main = api("/repos/%s/git/ref/heads/main" % REPO)
main_sha = (main.get("object") or {}).get("sha")
# Multi-stage pack: a later stage must parent to the BRANCH TIP and use THAT tree as base_tree.
# Parent to main with main's tree and the commit silently DROPS the previous stage's files — the exact
# data-loss shape measured in the previous round (a stage-2 commit deleted the round's own .md files).
st_ref0, ref0 = api("/repos/%s/git/ref/heads/%s" % (REPO, BRANCH))
PARENT = (ref0.get("object") or {}).get("sha") if st_ref0 == 200 else main_sha
st, cmeta = api("/repos/%s/commits/%s" % (REPO, PARENT))
base_tree = (cmeta.get("commit") or {}).get("tree", {}).get("sha")

REC = {"schema": "CNV-ARCHIVE-PUBLISH-RECEIPT/1", "task_id": ROUND, "generated_utc": GEN,
       "mode": "APPLY" if MODE else "DRY_RUN", "repo": REPO, "prefix": PREFIX, "branch": BRANCH,
       "base_main_sha": main_sha, "parent": PARENT, "base_tree_sha": base_tree,
       "parent_policy": "branch tip when the branch exists (multi-stage pack), else main",
       "files": len(files),
       "token": {"read_by": "this publisher process only", "printed": False}, "steps": []}
print("publication set:", len(files), "files,", sum(len(v) for v in files.values()), "bytes")

if not MODE:
    REC["verdict"] = "DRY_RUN"
    (OUT / "PUBLISH_RECEIPT_ARCHIVE.json").write_text(json.dumps(REC, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in sorted(files):
        print("   would publish", k)
    raise SystemExit(0)

tree_entries = []
for path, blob in sorted(files.items()):
    stb, rb = api("/repos/%s/git/blobs" % REPO, "POST",
                  {"content": base64.b64encode(blob).decode(), "encoding": "base64"})
    if stb not in (200, 201):
        REC["steps"].append({"step": "blob", "path": path, "status": stb, "body": rb})
        REC["verdict"] = "FAIL_BLOB"
        (OUT / "PUBLISH_RECEIPT_ARCHIVE.json").write_text(json.dumps(REC, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")
        print("blob failed", path, stb, str(rb)[:160])
        raise SystemExit(5)
    tree_entries.append({"path": path, "mode": "100644", "type": "blob", "sha": rb["sha"]})
step_tree = None
for attempt, base in enumerate([base_tree, None], 1):
    body = {"tree": tree_entries}
    if base:
        body["base_tree"] = base
    stt, rt = api("/repos/%s/git/trees" % REPO, "POST", body)
    step_tree = {"attempt": attempt, "status": stt, "body": rt if stt not in (200, 201) else {"sha": rt.get("sha")}}
    if stt in (200, 201):
        break
REC["steps"].append({"step": "tree", **step_tree})
if stt not in (200, 201):
    REC["verdict"] = "FAIL_TREE"
    (OUT / "PUBLISH_RECEIPT_ARCHIVE.json").write_text(json.dumps(REC, ensure_ascii=False, indent=1), encoding="utf-8")
    raise SystemExit(5)

stc, rc = api("/repos/%s/git/commits" % REPO, "POST",
              {"message": ("FAR-018/FAR-019 archive round: candidate evidence return pack\n\n"
                           "Three existing candidate evidence PRs (#12/#13/#14) merged at their approved exact "
                           "heads and read back; this commit archives this round's own records and receipts."),
               "tree": rt["sha"], "parents": [PARENT]})
REC["steps"].append({"step": "commit", "status": stc, "sha": rc.get("sha")})
if stc not in (200, 201):
    REC["verdict"] = "FAIL_COMMIT"
    (OUT / "PUBLISH_RECEIPT_ARCHIVE.json").write_text(json.dumps(REC, ensure_ascii=False, indent=1), encoding="utf-8")
    raise SystemExit(5)

st_ref, existing = api("/repos/%s/git/ref/heads/%s" % (REPO, BRANCH))
if st_ref == 200:
    stp, rp = api("/repos/%s/git/refs/heads/%s" % (REPO, BRANCH), "PATCH",
                  {"sha": rc["sha"], "force": False})
else:
    stp, rp = api("/repos/%s/git/refs" % REPO, "POST", {"ref": "refs/heads/%s" % BRANCH, "sha": rc["sha"]})
REC["steps"].append({"step": "ref", "status": stp, "response": rp if stp not in (200, 201) else {"ref": BRANCH}})
if stp not in (200, 201):
    REC["verdict"] = "FAIL_REF"
    (OUT / "PUBLISH_RECEIPT_ARCHIVE.json").write_text(json.dumps(REC, ensure_ascii=False, indent=1), encoding="utf-8")
    raise SystemExit(5)

st_pr, pr = api("/repos/%s/pulls" % REPO, "POST",
                {"title": "FAR-018 / FAR-019 archive round: candidate evidence return pack (3 PRs merged)",
                 "head": BRANCH, "base": "main", "body":
                 "Evidence-only return pack for round CNV-FAR018-FAR019-ARCHIVE-20261016.\n\n"
                 "- PR #12 merged at 0a30e5a8 -> 6c25bbe8 (33 blobs read back)\n"
                 "- PR #13 merged at 0fc70f2f -> 603cb0cb (55 blobs read back)\n"
                 "- PR #14 merged at b33b1220 -> bcd91043 (83 blobs read back)\n"
                 "- trusted scoped secrets scan PASS with positive + clean controls; no secret bytes\n"
                 "- claim ceiling: CANDIDATE_EVIDENCE_ARCHIVED_ONLY. No AO, no production, no runtime promotion.\n"})
REC["steps"].append({"step": "pull_request", "status": st_pr, "url": (pr or {}).get("html_url")})
REC["branch_commit"] = rc.get("sha")
REC["pull_request"] = pr.get("html_url")
REC["pull_request_number"] = pr.get("number")
REC["verdict"] = "PUBLISHED" if st_pr in (200, 201) else "PUBLISHED_NO_PR"

# ---- per-blob readback against the REMOTE tree (never against this script's own claims)
readback = {"schema": "CNV-ARCHIVE-REMOTE-READBACK/1", "generated_utc": GEN, "branch": BRANCH,
            "commit": rc.get("sha"), "files": [], "mismatches": [], "missing": []}
str_, rtree = api("/repos/%s/git/trees/%s?recursive=1" % (REPO, rt["sha"]))
remote = {r["path"]: r["sha"] for r in rtree.get("tree", []) if r["type"] == "blob"}
for path, blob in sorted(files.items()):
    local = git_blob_sha(blob)
    got = remote.get(path)
    row = {"path": path[len(PREFIX):], "local_git_blob_sha1": local, "remote_git_blob_sha1": got,
           "match": local == got}
    readback["files"].append(row)
    if got is None:
        readback["missing"].append(path)
    elif local != got:
        readback["mismatches"].append(path)
readback["count"] = len(readback["files"])
readback["verdict"] = "PASS" if not readback["mismatches"] and not readback["missing"] else "FAIL"
readback["main_unchanged_by_publish"] = api("/repos/%s/git/ref/heads/main" % REPO)[1].get("object", {}).get("sha")

(OUT / "PUBLISH_RECEIPT_ARCHIVE.json").write_text(json.dumps(REC, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "REMOTE_READBACK_ARCHIVE.json").write_text(json.dumps(readback, ensure_ascii=False, indent=1), encoding="utf-8")
print("publish:", REC["verdict"], "| PR", REC.get("pull_request"), "| branch commit", (rc.get("sha") or "")[:12])
print("readback:", readback["verdict"], "| files", readback["count"], "| mismatches", len(readback["mismatches"]),
      "| missing", len(readback["missing"]), "| main", readback["main_unchanged_by_publish"])
