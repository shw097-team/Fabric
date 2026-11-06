#!/usr/bin/env python
"""CNV-FAR018-FAR019-ARCHIVE-20261016 | A03 GitHub freeze + A04 index/manifest semantics.

Read-only.  Re-derives every frozen value from the live remote (never from the order text):
per-PR head/base/state/draft/mergeable, the full changed-file set, the blob modes of the
whole allowed prefix at that HEAD, symlink/submodule/executable checks, the prefix-resident
.gitattributes, and the PACK_INDEX manifest semantics (first-cut vs final blob count, and
whether every indexed path actually resolves at that HEAD).

Q03 = scope/mode verdict.  Q04 = manifest/index verdict.  Both fail closed per PR.
"""
import json, hashlib, base64, datetime, urllib.request, urllib.error
from pathlib import Path

ROUND = "CNV-FAR018-FAR019-ARCHIVE-20261016"
OUT = Path("C:/Projects/Agent_Workspace/_handover") / ROUND
TOK = open("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt", encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "User-Agent": "hgk-archive-round", "Accept": "application/vnd.github+json"}
PFX = {12: "EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/",
       13: "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/",
       14: "EVIDENCE/FAR-20261019-owner-authorized-closure/"}
ORDER_HEAD = {12: "0a30e5a8f636c4e310958778491bf4154e7caf1e",
              13: "0fc70f2f050119ada63cad7b4e641c21fdb37fa5",
              14: "b33b122053d53520809e87674784279097673fc0"}
ORDER_MAIN = "1807680ebf467aaee80b3d628ceb328fab0734df"


def api(p):
    r = urllib.request.Request("https://api.github.com" + p, headers=H)
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        return {"__err": e.code, "body": e.read().decode()[:200]}


def blob_text(sha):
    b = api("/repos/shw097-team/Fabric/git/blobs/" + sha)
    if "__err" in b:
        return None
    return base64.b64decode(b.get("content", "")).decode("utf-8", "replace")


def index_entries(obj):
    """Collect every path-like string under a manifest-shaped object, at any depth."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v.endswith((".json", ".md", ".txt", ".py", ".patch", ".ndjson")):
                found.append(v)
            else:
                found.extend(index_entries(v))
    elif isinstance(obj, list):
        for v in obj:
            found.extend(index_entries(v))
    return found


user = api("/user")
repo = api("/repos/shw097-team/Fabric")
main = api("/repos/shw097-team/Fabric/git/ref/heads/main")
out = {"schema": "CNV-ARCHIVE-A03-GITHUB-FREEZE/1", "task_id": ROUND,
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "auth_identity": {"login": user.get("login"), "type": user.get("type")},
       "repo_permissions": repo.get("permissions"),
       "repo_default_branch": repo.get("default_branch"),
       "main_sha": (main.get("object") or {}).get("sha"),
       "order_declared_main": ORDER_MAIN,
       "main_matches_order": (main.get("object") or {}).get("sha") == ORDER_MAIN,
       "prs": {}, "findings": []}

for n in (12, 13, 14):
    pr = api("/repos/shw097-team/Fabric/pulls/%d" % n)
    head, base = pr["head"]["sha"], pr["base"]["sha"]
    cm = api("/repos/shw097-team/Fabric/commits/" + head)
    tree = api("/repos/shw097-team/Fabric/git/trees/%s?recursive=1" % cm["commit"]["tree"]["sha"])
    rows = tree.get("tree", [])
    pref = [r for r in rows if r["path"].startswith(PFX[n])]
    pref_blobs = [r for r in pref if r["type"] == "blob"]
    modes = {}
    for r in pref_blobs:
        modes[r["mode"]] = modes.get(r["mode"], 0) + 1
    files = api("/repos/shw097-team/Fabric/pulls/%d/files?per_page=100" % n)
    files = files if isinstance(files, list) else []
    names = [f["filename"] for f in files]
    outside = [x for x in names if not x.startswith(PFX[n])]
    risky = [r["path"] for r in rows if r["mode"] in ("120000", "160000")]
    ga = [r for r in pref_blobs if r["path"].endswith(".gitattributes")]
    ga_txt = blob_text(ga[0]["sha"]) if ga else None
    pi = [r for r in pref_blobs if r["path"].endswith("PACK_INDEX.json")]
    pi_txt = blob_text(pi[0]["sha"]) if pi else None
    indexed, resolved, dangling, pi_keys = [], [], [], None
    if pi_txt:
        try:
            pj = json.loads(pi_txt)
            pi_keys = sorted(pj.keys())[:12] if isinstance(pj, dict) else "LIST"
            raw = index_entries(pj)
            base_dir = pi[0]["path"].rsplit("/", 1)[0] + "/"
            paths = set(r["path"] for r in pref_blobs)
            for v in raw:
                cand = v if v.startswith("EVIDENCE/") else base_dir + v.lstrip("./")
                if cand not in indexed:
                    indexed.append(cand)
            for c in indexed:
                (resolved if c in paths else dangling).append(c)
        except Exception as e:
            pi_keys = "PARSE_ERR:" + str(e)[:80]
    ext = {}
    for r in pref_blobs:
        nm = r["path"].rsplit("/", 1)[-1]
        e = nm.rsplit(".", 1)[-1].lower() if "." in nm else "(noext)"
        ext[e] = ext.get(e, 0) + 1
    q03 = ("PASS" if (not outside and not risky and set(modes) <= {"100644"} and head == ORDER_HEAD[n])
           else "FAIL")
    q04 = ("PASS" if (pi_txt and not dangling) else ("FAIL" if pi_txt else "NOT_RUN"))
    out["prs"][str(n)] = {
        "number": n, "url": pr["html_url"], "state": pr["state"], "draft": pr["draft"],
        "mergeable": pr["mergeable"], "mergeable_state": pr["mergeable_state"],
        "head_sha": head, "order_declared_head": ORDER_HEAD[n], "head_matches_order": head == ORDER_HEAD[n],
        "base_sha": base, "commits": pr["commits"], "changed_files": pr["changed_files"],
        "review_comments": pr["review_comments"], "added": pr.get("additions"), "removed": pr.get("deletions"),
        "allowed_prefix": PFX[n], "changed_paths_sample": names[:4],
        "paths_outside_prefix": outside, "repo_symlink_or_submodule_paths": len(risky),
        "prefix_blob_count": len(pref_blobs), "prefix_blob_modes": modes,
        "executable_or_link_blobs": [r["path"] for r in pref_blobs if r["mode"] != "100644"],
        "prefix_gitattributes": ga[0]["path"] if ga else None, "prefix_gitattributes_text": ga_txt,
        "extension_histogram": dict(sorted(ext.items(), key=lambda kv: -kv[1])),
        "pack_index_path": pi[0]["path"] if pi else None,
        "pack_index_keys": pi_keys, "pack_index_indexed_count": len(indexed),
        "pack_index_resolved_count": len(resolved), "pack_index_dangling": dangling[:8],
        "manifest_first_cut_vs_final": "%d indexed / %d final prefix blobs" % (len(indexed), len(pref_blobs)),
        "Q03_scope_and_mode": q03, "Q04_manifest": q04,
        "review_count": api("/repos/shw097-team/Fabric/pulls/%d/reviews" % n).__len__()
        if isinstance(api("/repos/shw097-team/Fabric/pulls/%d/reviews" % n), list) else None,
        "status_combined_state": api("/repos/shw097-team/Fabric/commits/%s/status" % head).get("state"),
    }
    if outside:
        out["findings"].append({"pr": n, "code": "PREFIX_ESCAPE", "paths": outside[:5]})
    if risky:
        out["findings"].append({"pr": n, "code": "SYMLINK_SUBMODULE_HOOK_RISK", "count": len(risky)})
    if head != ORDER_HEAD[n]:
        out["findings"].append({"pr": n, "code": "PR_HEAD_DRIFT", "live": head, "order": ORDER_HEAD[n]})

(OUT / "A03_GITHUB_FREEZE.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for n in (12, 13, 14):
    p = out["prs"][str(n)]
    print("PR%-3d %s draft=%s %s/%s head==order:%s files=%d outside=%d modes=%s Q03=%s Q04=%s [%s]"
          % (n, p["state"], p["draft"], p["mergeable"], p["mergeable_state"], p["head_matches_order"],
             p["changed_files"], len(p["paths_outside_prefix"]), p["prefix_blob_modes"],
             p["Q03_scope_and_mode"], p["Q04_manifest"], p["manifest_first_cut_vs_final"]))
print("main", out["main_sha"], "matches_order", out["main_matches_order"], "| findings", out["findings"])
print("auth", out["auth_identity"], "perms", out["repo_permissions"])
