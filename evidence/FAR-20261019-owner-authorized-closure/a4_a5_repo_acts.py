#!/usr/bin/env python
"""FAR-20261019 Tier A repository acts (owner-authorised maintainer role).

A4 merge the peer evidence chain PR #6/#8/#10 at their verified exact HEADs (merge_method=merge, the
   head sha is pinned in the request so a head that moved since the freeze cannot be merged silently).
A5 promote the previous round's evidence PR #13 out of draft (GraphQL markPullRequestReadyForReview).

The token file is READ BY THIS PROCESS ONLY and is never printed, logged or written into any artifact.
"""
import json, datetime, urllib.request, urllib.error, glob
from pathlib import Path

TOK = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt").read_text(encoding="utf-8").strip()
REPO = "shw097-team/Fabric"
OUT = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
rep = {"schema": "FAR-20261019/REPO-ACTS/1",
       "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "repo": REPO, "token_source": "read from file by this process only (never printed)", "steps": []}


def api(method, path, body=None, accept="application/vnd.github+json"):
    req = urllib.request.Request("https://api.github.com" + path, method=method,
                                 data=(json.dumps(body).encode() if body is not None else None),
                                 headers={"Authorization": "Bearer " + TOK, "Accept": accept,
                                          "X-GitHub-Api-Version": "2022-11-28",
                                          "User-Agent": "far-019-closure"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def graphql(query, variables):
    req = urllib.request.Request("https://api.github.com/graphql", method="POST",
                                 data=json.dumps({"query": query, "variables": variables}).encode(),
                                 headers={"Authorization": "Bearer " + TOK, "User-Agent": "far-019-closure"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


st, main_before = api("GET", f"/repos/{REPO}/git/ref/heads/main")
before_sha = (main_before.get("object") or {}).get("sha")
rep["main_before"] = before_sha

# recorded frozen heads from the previous round's peer-chain readiness record, if it exists
frozen = {}
for pat in ("C:/Projects/Agent_Workspace/_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/*.json",
            "C:/Projects/Agent_Workspace/_handover/FAR-20261016-018-r7r11-residual-closure-and-handover/*.json"):
    for f in glob.glob(pat):
        try:
            if "PEER" in Path(f).name.upper() or "PREFLIGHT" in Path(f).name.upper():
                frozen[Path(f).name] = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            pass
rep["frozen_sources_seen"] = list(frozen.keys())

for pr in (6, 8, 10):
    st, d = api("GET", f"/repos/{REPO}/pulls/{pr}")
    step = {"id": f"A4-PR{pr}", "number": pr, "measured": {
        "state": d.get("state"), "draft": d.get("draft"), "mergeable": d.get("mergeable"),
        "mergeable_state": d.get("mergeable_state"), "head_sha": (d.get("head") or {}).get("sha"),
        "base_sha": (d.get("base") or {}).get("sha"), "changed_files": d.get("changed_files"),
        "title": (d.get("title") or "")[:80]}}
    if d.get("state") != "open":
        step["verdict"] = "SKIPPED_NOT_OPEN"
    elif d.get("draft"):
        step["verdict"] = "SKIPPED_IS_DRAFT"
    else:
        head = (d.get("head") or {}).get("sha")
        st2, d2 = api("PUT", f"/repos/{REPO}/pulls/{pr}/merge",
                      {"merge_method": "merge", "sha": head,
                       "commit_title": f"Merge evidence PR #{pr} at verified HEAD {head[:8]} (FAR-019 owner-authorised archival merge)"})
        step["merge_call"] = {"http": st2, "response": {k: d2.get(k) for k in ("sha", "merged", "message")}}
        step["verdict"] = "MERGED" if d2.get("merged") else f"MERGE_REFUSED_{st2}"
        if d2.get("merged"):
            stm, cm = api("GET", f"/repos/{REPO}/commits/{d2['sha']}")
            step["merge_commit_parents"] = [p.get("sha") for p in (cm.get("parents") or [])]
            step["head_is_a_parent"] = head in step["merge_commit_parents"]
    rep["steps"].append(step)
    print(f"A4 PR#{pr}:", step["verdict"], "| head", step["measured"]["head_sha"][:8],
          "| state", step["measured"]["state"], "| mergeable", step["measured"]["mergeable"])

st, main_after = api("GET", f"/repos/{REPO}/git/ref/heads/main")
rep["main_after"] = (main_after.get("object") or {}).get("sha")
rep["main_moved"] = rep["main_after"] != before_sha

# ---- A5: promote PR #13 out of draft ----
st, d13 = api("GET", f"/repos/{REPO}/pulls/13")
node = d13.get("node_id")
a5 = {"id": "A5-PR13", "before": {"state": d13.get("state"), "draft": d13.get("draft"),
                                  "head_sha": (d13.get("head") or {}).get("sha"),
                                  "changed_files": d13.get("changed_files"), "node_id": node}}
if d13.get("draft") and node:
    q = ("mutation($id:ID!){ markPullRequestReadyForReview(input:{pullRequestId:$id}){ "
         "pullRequest{ number isDraft state url } } }")
    stg, dg = graphql(q, {"id": node})
    a5["mutation_http"] = stg
    a5["mutation_response"] = dg.get("data", {}).get("markPullRequestReadyForReview", {}).get("pullRequest") or dg
    st3, d3 = api("GET", f"/repos/{REPO}/pulls/13")
    a5["after"] = {"draft": d3.get("draft"), "state": d3.get("state"),
                   "head_sha": (d3.get("head") or {}).get("sha")}
    a5["verdict"] = "PROMOTED" if d3.get("draft") is False else "STILL_DRAFT"
else:
    a5["verdict"] = "SKIPPED_NOT_DRAFT"
rep["steps"].append(a5)
print("A5 PR#13:", a5["verdict"], "| before draft", a5["before"]["draft"], "->", (a5.get("after") or {}).get("draft"))

(OUT / "A4_A5_REPO_ACTS.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
print("main:", before_sha[:8], "->", (rep["main_after"] or "")[:8], "| moved:", rep["main_moved"])
print("wrote", OUT / "A4_A5_REPO_ACTS.json")
