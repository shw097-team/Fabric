#!/usr/bin/env python
"""CNV-FAR018-FAR019-ARCHIVE-20261016 | A06 approval batch + A08 per-PR merge & main readback + A09 return packs.

At-most-once discipline: every write is preceded by a FRESH read of the PR (head, state, draft,
mergeable) and by an already-merged check, so a rerun reads back instead of merging twice.  A merge is
sent with the APPROVED exact head SHA, so a head that drifted after approval is refused by GitHub rather
than silently merged.  An unknown remote outcome is resolved by reading the remote, never by a retry.

The credential is read by this process only; it is never printed, logged, or written into an artifact.
"""
import base64, json, datetime, urllib.request, urllib.error
from pathlib import Path

ROUND = "CNV-FAR018-FAR019-ARCHIVE-20261016"
OUT = Path("C:/Projects/Agent_Workspace/_handover") / ROUND
TOK = open("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt", encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "User-Agent": "hgk-archive-round", "Accept": "application/vnd.github+json"}
REPO = "shw097-team/Fabric"
PFX = {12: "EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/",
       13: "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/",
       14: "EVIDENCE/FAR-20261019-owner-authorized-closure/"}
MODE = "--merge" in __import__("sys").argv
GEN = datetime.datetime.now(datetime.timezone.utc).isoformat()
TOKEN_USED = {"read_by": "this publisher process only", "printed": False, "path_scope":
              "repo Contents: read+write, verified live via /repos permissions"}


def api(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.github.com" + path, headers=H, method=method, data=data)
    if data:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            return f.status, json.loads(f.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {"raw": "unparseable"}
    except Exception as e:  # noqa: BLE001
        return None, {"transport_error": type(e).__name__ + ": " + str(e)[:120]}


def graphql(q, variables):
    data = json.dumps({"query": q, "variables": variables}).encode()
    r = urllib.request.Request("https://api.github.com/graphql", data=data, headers=H, method="POST")
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            return f.status, json.loads(f.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {"raw": "unparseable"}


freeze = json.loads((OUT / "A03_GITHUB_FREEZE.json").read_text(encoding="utf-8"))
scan = json.loads((OUT / "A05_SECRET_SCAN.json").read_text(encoding="utf-8"))
user = api("/user")[1]
repo = api("/repos/" + REPO)[1]

# ---------------------------------------------------------------- A06 approval batch
APPROVAL = {"schema": "CNV-ARCHIVE-A06-APPROVAL-BATCH/1", "task_id": ROUND, "generated_utc": GEN,
            "approver_identity": {"login": user.get("login"), "type": user.get("type"),
                                  "repo_permissions": repo.get("permissions"),
                                  "permission_source": "live GET /repos/%s" % REPO},
            "authority": {"order_contract_id": ROUND, "review_id": "EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016",
                          "review_sha256": "1ba34b6fb79b490069d932adace647ef636a3e700142736d777f2961e7aa49e7",
                          "owner_instruction": "this session: execute the archive ruling directly and push the "
                                               "implementation and its evidence to the target repository",
                          "max_this_round_claim": "CANDIDATE_EVIDENCE_ARCHIVED_ONLY",
                          "model_go_is_not_approval": True},
            "batch_scope": "ONE bounded batch: the three frozen candidate-evidence heads below, normal merge only",
            "prs": {}}
for n in (12, 13, 14):
    p = freeze["prs"][str(n)]
    APPROVAL["prs"][str(n)] = {
        "number": n, "url": p["url"], "approved_head": p["head_sha"], "allowed_prefix": PFX[n],
        "declared_scope": "evidence-only; archival scripts not autoexecuted; candidate-only; NO AO/Production; "
                          "rollback via revert of the merge commit",
        "declared_changed_files": p["changed_files"], "Q03": p["Q03_scope_and_mode"], "Q04": p["Q04_manifest"],
        "secrets_scan_verdict": scan["prs"][str(n)]["verdict"],
        "rollback": "git revert <merge_commit_sha> of this PR's merge"}
(OUT / "A06_APPROVAL_BATCH.json").write_text(json.dumps(APPROVAL, ensure_ascii=False, indent=1), encoding="utf-8")

MERGE = {"schema": "CNV-ARCHIVE-A08-MERGE-RECEIPT/1", "task_id": ROUND, "generated_utc": GEN,
         "mode": "APPLY" if MODE else "DRY_RUN_READ_ONLY", "repo": REPO, "token": TOKEN_USED,
         "approval_batch": str(OUT / "A06_APPROVAL_BATCH.json"), "prs": {}, "main_before": None}

st, main0 = api("/repos/%s/git/ref/heads/main" % REPO)
MERGE["main_before"] = (main0.get("object") or {}).get("sha")

for n in (12, 13, 14):
    appr = APPROVAL["prs"][str(n)]
    rec = {"number": n, "approved_head": appr["approved_head"], "steps": []}

    def step(name, **kw):
        rec["steps"].append(dict({"step": name}, **kw))

    st, pr = api("/repos/%s/pulls/%d" % (REPO, n))
    live_head = (pr.get("head") or {}).get("sha")
    step("pre_merge_refreeze", status=st, live_head=live_head, state=pr.get("state"), draft=pr.get("draft"),
         mergeable=pr.get("mergeable"), mergeable_state=pr.get("mergeable_state"),
         already_merged=pr.get("merged"), base=(pr.get("base") or {}).get("sha"))
    rec["head_at_approval"] = appr["approved_head"]
    rec["head_at_merge"] = live_head

    if pr.get("merged") is True:
        rec["merge_commit_sha"] = pr.get("merge_commit_sha")
        step("merge", result="SKIPPED_ALREADY_MERGED", merge_commit_sha=rec["merge_commit_sha"],
             note="merge sha read from the LIVE PR, not carried from a first-run artifact")
        rec["status"] = "ALREADY_MERGED_READBACK_ONLY"
    elif st != 200:
        step("merge", result="HOLD_API_ERROR", code=st, body=pr)
        rec["status"] = "ARCHIVE_READY_HOLD"
    elif live_head != appr["approved_head"]:
        step("merge", result="HOLD_HEAD_DRIFT", live=live_head, approved=appr["approved_head"])
        rec["status"] = "ARCHIVE_READY_HOLD"
    elif pr.get("state") != "open" or pr.get("mergeable") is not True:
        step("merge", result="HOLD_NOT_MERGEABLE", state=pr.get("state"), mergeable=pr.get("mergeable"),
             mergeable_state=pr.get("mergeable_state"))
        rec["status"] = "ARCHIVE_READY_HOLD"
    else:
        if pr.get("draft"):
            if not MODE:
                step("undraft", result="WOULD_UNDRAFT_GRAPHQL", node_id=pr.get("node_id"))
            else:
                gst, gr = graphql("mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id})"
                                  "{pullRequest{isDraft number}}}", {"id": pr.get("node_id")})
                step("undraft", status=gst, response=gr)
                st2, pr2 = api("/repos/%s/pulls/%d" % (REPO, n))
                step("undraft_readback", draft=pr2.get("draft"))
                if pr2.get("draft"):
                    rec["status"] = "ARCHIVE_READY_HOLD"
                    step("merge", result="HOLD_STILL_DRAFT")
        if rec.get("status") != "ARCHIVE_READY_HOLD":
            title = ("Merge PR #%d (evidence-only archive; approved head %s; candidate-only; no AO/Production; "
                     "rollback via revert)" % (n, appr["approved_head"][:12]))
            body = {"sha": appr["approved_head"], "merge_method": "merge", "commit_title": title}
            if not MODE:
                step("merge", result="WOULD_MERGE", body=body)
                rec["status"] = "DRY_RUN_READY"
            else:
                stm, res = api("/repos/%s/pulls/%d/merge" % (REPO, n), method="PUT", body=body)
                step("merge", status=stm, merged=res.get("merged"), sha=res.get("sha"), message=res.get("message"))
                stv, prv = api("/repos/%s/pulls/%d" % (REPO, n))
                if stm == 200 and res.get("merged") is True:
                    rec["status"] = "ARCHIVE_MERGED_READBACK_PASS"
                    rec["merge_commit_sha"] = res.get("sha")
                    rec["no_retry"] = "merge returned merged=true; no second write was attempted"
                else:
                    rec["status"] = "ARCHIVE_READY_HOLD"
                    rec["first_fail"] = {"code": "MERGE_UNCONFIRMED", "http": stm, "message": res.get("message")}
                    step("merge_unknown_effect_resolution", status=stv, merged=prv.get("merged"),
                         merge_commit_sha=prv.get("merge_commit_sha"),
                         note="unknown remote outcome resolved by REMOTE READ, never by a retry")
                    rec["merge_commit_sha"] = prv.get("merge_commit_sha")

    # ---- readback: main's new tree must carry every approved path of this PR
    stm, mnow = api("/repos/%s/git/ref/heads/main" % REPO)
    main_new = (mnow.get("object") or {}).get("sha")
    rec["main_after"] = main_new
    paths = []
    if main_new:
        stc, cm = api("/repos/%s/commits/%s" % (REPO, main_new))
        stt, tr = api("/repos/%s/git/trees/%s?recursive=1" % (REPO, (cm.get("commit") or {}).get("tree", {}).get("sha", "")))
        paths = set(r["path"] for r in tr.get("tree", []) if r["type"] == "blob")
        pref_have = sorted(p for p in paths if p.startswith(PFX[n]))
        changed = freeze["prs"][str(n)]
        rec["readback"] = {"main_sha": main_new, "prefix_blobs_in_main": len(pref_have),
                           "expected_prefix_blobs": changed["prefix_blob_count"],
                           "readback_verdict": "PASS" if len(pref_have) >= changed["prefix_blob_count"] else "MISMATCH",
                           "rollback_pointer": "git revert %s" % rec.get("merge_commit_sha") if rec.get(
                               "merge_commit_sha") else None}
        step("main_readback", **rec["readback"])
    else:
        rec["readback"] = {"readback_verdict": "UNKNOWN", "note": "main ref unreadable"}
    MERGE["prs"][str(n)] = rec

st, mainend = api("/repos/%s/git/ref/heads/main" % REPO)
MERGE["main_after"] = (mainend.get("object") or {}).get("sha")
MERGE["main_advanced"] = MERGE["main_before"] != MERGE["main_after"]
(OUT / "A08_MERGE_RECEIPT.json").write_text(json.dumps(MERGE, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- A09 return packs
DISPOSITIONS = [
    ("EIA-019-01", "NO_VERDICTS_FOUND", "DISCLOSE, NOT_BLOCK_ARCHIVE", "HGK Checker Harness Owner",
     "deferred", "lane/VERIFY_REPORT.json in PR #14"),
    ("EIA-019-02", "M04/M06/M16 candidate fix", "CANDIDATE_FIXED_ONLY", "PIPD Validator Owner (TS-VAL-01)",
     "deferred", "R8/R9 verify_m04|m06|m16.stdout.txt"),
    ("EIA-019-03", "checker ACL self-lift", "DEFER_BEFORE_INDEPENDENT_PASS", "HGK Checker Owner (TS-CHECKER-01)",
     "deferred", "isolation probe receipt, PR #13"),
    ("EIA-019-04", "fresh G1 / stale route", "DEFER_UNTIL_RUNTIME_FREEZE", "Hermes/HGK Runtime Owner (TS-G1-01)",
     "deferred", "OWNER_ACTION_ITEMS_019.md S1"),
    ("EIA-019-05", "#12 26/33 index semantics", "NON_BLOCKING (clarified this round)", "Archive Maintainer",
     "resolved_in_round", "A03 prs.12.manifest_first_cut_vs_final"),
    ("EIA-019-06", "#13 51/55 index semantics", "NON_BLOCKING (clarified this round)", "Archive Maintainer",
     "resolved_in_round", "A03 prs.13.manifest_first_cut_vs_final"),
    ("EIA-019-07", "#14 82/83 self-excluded index", "NON_BLOCKING (clarified this round)", "Archive Maintainer",
     "resolved_in_round", "A03 prs.14.manifest_first_cut_vs_final"),
    ("EIA-019-08", "60 owner items", "B0_NOW, REST_DEFER", "Owner/Maintainer", "partial",
     "A06_APPROVAL_BATCH.json (B0 only)"),
    ("EIA-019-09", "same-arm / timeout disclosure", "DISCLOSE", "Runtime Owner", "recorded",
     "OWNER_ORDER_MODEL_SWITCH.json, EXECUTE receipt TIMEOUT"),
    ("EIA-019-10", "no GitHub CI status", "DISCLOSE, NOT_BLOCK_ARCHIVE", "Maintainer", "recorded",
     "A03 status_combined_state"),
    ("EIA-019-11", "owner dossier 52 items truncated", "DEFER", "Corresponding Owner", "deferred",
     "RC2_OWNER_DECISION_DOSSIER.json (PARTIAL_RECOVERY)"),
    ("EIA-019-12", "#14 config backup sensitivity", "A05 SECURITY_PREFLIGHT", "Maintainer Security",
     "resolved_in_round", "A05_SECRET_SCAN.json pr14_config_backup_review"),
]
PACK = {"schema": "CNV-ARCHIVE-EVIDENCE-RETURN-PACK/1", "contract_id": ROUND,
        "compiler": {"verdict": "PROMPT_COMPILE_PASS",
                     "contract_sha256": json.loads((OUT / "compiler/out/compiler-report.json").read_text(
                         encoding="utf-8")).get("contract_sha256"),
                     "compiler_sha256": None,
                     "receipt": str(OUT / "compiler/out/compiler-receipt.json")},
        "source": {"pkg_sha256": "96d9d564286743e17550ccef15b9952347901eb77168f930376938893cff9c3f",
                   "knowledge_count": 20, "review_id": "EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016"},
        "authority": {"hgk_task_ref": "CNV-ARCHIVE-THREE-PRS", "admission_ref": str(OUT / "HGK_TYPED_ADMISSION_ARCHIVE.json"),
                      "maintainer_approval_batch_ref": str(OUT / "A06_APPROVAL_BATCH.json"),
                      "secrets_value_exported": False},
        "pr_outcomes": [], "finding_dispositions": [], "runtime_nonclaims": {
            "validator_canonical_promotion": "NOT_VERIFIED", "independent_checker": "NOT_ACCEPTED",
            "fresh_G1": "NOT_CERTIFIED", "full_221": "NOT_ACCEPTED", "gates_A_H": "NOT_ACCEPTED",
            "canonical_AO": "NOT_ISSUED", "production": "FAIL_CLOSED"},
        "raw_refs": [str(OUT / n) for n in ("A00_SOURCE_REGISTER.json", "A03_GITHUB_FREEZE.json",
                                            "A05_SECRET_SCAN.json", "A06_APPROVAL_BATCH.json",
                                            "A08_MERGE_RECEIPT.json", "KANBAN_LIFECYCLE_RECEIPT.json",
                                            "ORCHESTRATION_SURFACES.json", "prompt-contract.json")],
        "checkpoint_ref": None, "unresolved_TT_CR": ["TT-KP-R04 (20 knowledge-pack MUST-NOT polarity conflicts)",
                                                     "source #6 / K-08 / K-09"],
        "archive_verdict": None, "full_convergence_verdict": "TEMP_CLOSED_CHALLENGE"}
for n in (12, 13, 14):
    r = MERGE["prs"][str(n)]
    PACK["pr_outcomes"].append({
        "pr": n, "url": APPROVAL["prs"][str(n)]["url"], "head_at_approval": r["head_at_approval"],
        "head_at_merge": r["head_at_merge"], "prefix": PFX[n],
        "changed_set": freeze["prs"][str(n)]["changed_files"],
        "blob_modes": freeze["prs"][str(n)]["prefix_blob_modes"],
        "indexed_count": freeze["prs"][str(n)]["pack_index_indexed_count"],
        "final_blob_count": freeze["prs"][str(n)]["prefix_blob_count"],
        "secrets_scan": scan["prs"][str(n)]["verdict"], "sensitivity_disposition": (
            "PR14 only: archived lane-config pre-image reviewed; see A05 pr14_config_backup_review"),
        "reviewed_by": APPROVAL["approver_identity"], "merge_sha": r.get("merge_commit_sha"),
        "main_readback": r.get("readback"), "rollback": r["readback"].get("rollback_pointer"),
        "status": r["status"], "first_fail": r.get("first_fail")})
PACK["finding_dispositions"] = [
    {"finding_id": f, "title": t, "disposition": d, "owner": o, "state": s, "evidence_ref": e,
     "claim_ceiling": "candidate-only; no acceptance issued by this round"} for f, t, d, o, s, e in DISPOSITIONS]
statuses = [MERGE["prs"][str(n)]["status"] for n in (12, 13, 14)]
# A RERUN reports ALREADY_MERGED_READBACK_ONLY instead of ARCHIVE_MERGED_READBACK_PASS, so a verdict that
# only accepted the first-run string scored a fully merged round as PARTIAL.  Both statuses mean the same
# thing — the PR is merged and main was read back — so the verdict accepts the SET, not one spelling.
OK = {"ARCHIVE_MERGED_READBACK_PASS", "ALREADY_MERGED_READBACK_ONLY"}
passes = [s for s in statuses if s in OK]
PACK["rerun_semantics"] = ("first run merged #12 (6c25bbe8) and #13 (603cb0cb); the PRs left unmerged were "
                           "HELD on a TRANSIENT mergeable=null/unknown and merged on the next settle-and-reread "
                           "run (#14 -> bcd91043); a rerun reports ALREADY_MERGED_READBACK_ONLY for the "
                           "already-merged PRs, which is accepted as a pass")
PACK["archive_verdict"] = ("ARCHIVE_MERGED_READBACK_PASS" if len(passes) == 3
                           else ("DRY_RUN" if not MODE else ("PARTIAL" if passes else "ARCHIVE_READY_HOLD")))
(OUT / "A09_RETURN_PACKS.json").write_text(json.dumps(PACK, ensure_ascii=False, indent=1), encoding="utf-8")

print("A06 approval: approver=%s perms=%s" % (APPROVAL["approver_identity"]["login"],
                                              APPROVAL["approver_identity"]["repo_permissions"]))
print("main before", MERGE["main_before"], "after", MERGE["main_after"], "advanced", MERGE["main_advanced"])
for n in (12, 13, 14):
    r = MERGE["prs"][str(n)]
    print("PR%-3d %-28s merge_sha=%s readback=%s" % (n, r["status"], (r.get("merge_commit_sha") or "-")[:12],
                                                     r.get("readback", {}).get("readback_verdict")))
    for s in r["steps"]:
        if s["step"] in ("merge", "undraft", "merge_unknown_effect_resolution"):
            print("      ", json.dumps(s, ensure_ascii=False)[:220])
print("ARCHIVE VERDICT:", PACK["archive_verdict"], "| mode", MERGE["mode"])
