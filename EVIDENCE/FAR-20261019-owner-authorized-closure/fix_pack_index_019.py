#!/usr/bin/env python
"""Recompute PACK_INDEX.json over the WHOLE pack (payload + receipts) and commit only that one file.

The receipts stage rebuilt the index from its own 17 files, which left the 52 payload files unlisted; a
reader opening the index would have seen an incomplete pack. The index must describe the pack, not the
stage that happened to write it.
"""
import hashlib, json, datetime, urllib.request, urllib.error
from pathlib import Path

TOK = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt").read_text(encoding="utf-8").strip()
REPO = "shw097-team/Fabric"
BRANCH = "evidence/far-019-owner-auth-closure"
PREFIX = "EVIDENCE/FAR-20261019-owner-authorized-closure"
ROUND = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")


def api(method, path, body=None):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=(json.dumps(body).encode() if body is not None else None),
                                 headers={"Authorization": "Bearer " + TOK,
                                          "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "far-019-idx"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


st, ref = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
tip = ref["object"]["sha"]
st, tr = api("GET", f"/repos/{REPO}/git/trees/{tip}?recursive=1")
blobs = {e["path"]: e["sha"] for e in tr["tree"] if e.get("type") == "blob" and e["path"].startswith(PREFIX + "/")}
self_path = f"{PREFIX}/PACK_INDEX.json"
entries = []
for p, sha in sorted(blobs.items()):
    if p == self_path:
        continue
    entries.append({"path": p, "git_blob_id": sha})
index = {"schema": "FAR-20261019/PACK-INDEX/1",
         "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "round": "FAR-20261019-owner-authorized-closure", "repo": REPO, "branch": BRANCH, "prefix": PREFIX,
         "note": "second revision: the first index was built from the receipts stage alone and left the "
                 "payload files unlisted; this one is built by reading the branch tree itself, so it "
                 "describes the pack as it actually is",
         "file_count": len(entries),
         "self_excluded": {"path": self_path,
                           "reason": "a file cannot carry its own digest; its digest is carried by the "
                                     "post-publication receipt"},
         "not_listed_by_design": [f"{PREFIX}/PUBLISH_RECEIPT_019_payload.json",
                                  f"{PREFIX}/PUBLISH_RECEIPT_019_receipts.json",
                                  f"{PREFIX}/REMOTE_READBACK_VERIFY_019.json"],
         "entries": entries}
b = json.dumps(index, ensure_ascii=False, indent=1).encode()
st, cm = api("GET", f"/repos/{REPO}/git/commits/{tip}")
st, tree = api("POST", f"/repos/{REPO}/git/trees",
               {"base_tree": cm["tree"]["sha"],
                "tree": [{"path": self_path, "mode": "100644", "type": "blob",
                          "content": b.decode("utf-8", errors="surrogateescape")}]})
st, commit = api("POST", f"/repos/{REPO}/git/commits",
                 {"message": "FAR-20261019: rebuild PACK_INDEX.json over the whole pack (the receipts-stage "
                             "index listed only the receipts files)", "tree": tree["sha"], "parents": [tip]})
st, r2 = api("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False})
st, chk = api("GET", f"/repos/{REPO}/git/trees/{commit['sha']}?recursive=1")
now = {e["path"]: e["sha"] for e in chk["tree"] if e.get("type") == "blob" and e["path"].startswith(PREFIX + "/")}
listed = {e["path"] for e in entries} | set(index["not_listed_by_design"]) | {self_path}
unindexed = sorted(p for p in now if p not in listed)
st, mref = api("GET", f"/repos/{REPO}/git/ref/heads/main")
out = {"schema": "FAR-20261019/PACK-INDEX-REBUILD/1", "tip": commit.get("sha"),
       "files_in_pack": len(now), "indexed": len(entries), "unindexed_after": unindexed,
       "main": mref["object"]["sha"],
       "verdict": "PASS" if not unindexed else "FAIL"}
(ROUND / "PACK_INDEX_REBUILD_019.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("tip:", (commit.get("sha") or "")[:8], "| files:", len(now), "| indexed:", len(entries),
      "| unindexed:", len(unindexed), "| main:", mref["object"]["sha"][:8], "| verdict:", out["verdict"])
