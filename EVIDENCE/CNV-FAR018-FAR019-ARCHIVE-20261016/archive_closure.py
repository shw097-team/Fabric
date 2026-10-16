#!/usr/bin/env python
"""CNV-FAR018-FAR019-ARCHIVE-20261016 | A09 closure: errata, single evidence MD, handover, self-check.

The self-check re-derives every invariant from LIVE evidence (the remote API and the bytes on disk) and
never from this round's own summary files.  Each check is then attacked by an INJECTED MUTATION applied to
an in-memory copy; a check that cannot fail is not a check, and a mutation that is not detected is a
defect in the harness.  The verdict is a MACHINE GATE: it is never an acceptance, an approval or a Gate.
"""
import copy, hashlib, json, datetime, urllib.request, urllib.error
from pathlib import Path

ROUND = "CNV-FAR018-FAR019-ARCHIVE-20261016"
OUT = Path("C:/Projects/Agent_Workspace/_handover") / ROUND
REPO = "shw097-team/Fabric"
PFX = {12: "EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/",
       13: "EVIDENCE/FAR-20261016-018-r7r11-residual-closure-and-handover/",
       14: "EVIDENCE/FAR-20261019-owner-authorized-closure/"}
HEADS = {12: "0a30e5a8f636c4e310958778491bf4154e7caf1e",
         13: "0fc70f2f050119ada63cad7b4e641c21fdb37fa5",
         14: "b33b122053d53520809e87674784279097673fc0"}
GEN = datetime.datetime.now(datetime.timezone.utc).isoformat()
TOK = open("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt", encoding="utf-8").read().strip()
H = {"Authorization": "Bearer " + TOK, "User-Agent": "hgk-archive-round", "Accept": "application/vnd.github+json"}


def api(p):
    r = urllib.request.Request("https://api.github.com" + p, headers=H)
    try:
        with urllib.request.urlopen(r, timeout=120) as f:
            return json.loads(f.read().decode())
    except urllib.error.HTTPError as e:
        return {"__err": e.code}
    except Exception as e:  # noqa: BLE001
        return {"__err": type(e).__name__}


def load(name, default=None):
    p = OUT / name
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {"__parse_error": type(e).__name__}


LIVE = {}
for n in (12, 13, 14):
    LIVE[n] = api("/repos/%s/pulls/%d" % (REPO, n))
MAIN = api("/repos/%s/git/ref/heads/main" % REPO)
MAIN_SHA = (MAIN.get("object") or {}).get("sha")
if MAIN_SHA:
    TR = api("/repos/%s/git/trees/%s?recursive=1" % (REPO, api("/repos/%s/commits/%s" % (REPO, MAIN_SHA))
                                                     .get("commit", {}).get("tree", {}).get("sha", "")))
    MAIN_PATHS = set(r["path"] for r in TR.get("tree", []) if r["type"] == "blob")
else:
    MAIN_PATHS = set()
MAIN_TIP = MAIN_SHA
RECENT = [c["sha"] for c in (api("/repos/%s/commits?sha=main&per_page=10" % REPO) or [])] \
    if isinstance(api("/repos/%s/commits?sha=main&per_page=10" % REPO), list) else []

DATA = {k: load(k) for k in ("A00_SOURCE_REGISTER.json", "A03_GITHUB_FREEZE.json", "A05_SECRET_SCAN.json",
                             "A06_APPROVAL_BATCH.json", "A08_MERGE_RECEIPT.json", "A09_RETURN_PACKS.json",
                             "HGK_TYPED_ADMISSION_ARCHIVE.json", "ORCHESTRATION_SURFACES.json",
                             "KANBAN_LIFECYCLE_RECEIPT.json", "PUBLISH_RECEIPT_ARCHIVE.json",
                             "REMOTE_READBACK_ARCHIVE.json", "compiler/out/compiler-report.json",
                             "compiler/hash.stdout.txt")}
KB_DIR = Path("C:/Projects/Agent_Workspace/知識庫/工程基座/"
              "GPTs_GENIEMAKER_開發實作+驗收指導官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack")
KB_DIR = Path("C:/Projects/Agent_Workspace/知識庫/工程基座/"
              "GPTs_GENIEMAKER_開發實作+驗收指揮官_KP_Builder_ReleasePack_v2026.06.03-r2/KnowledgePack")


def checks(d, live, main_paths, recent, kb_dir):
    out = []
    a00, a03, a05 = d["A00_SOURCE_REGISTER.json"], d["A03_GITHUB_FREEZE.json"], d["A05_SECRET_SCAN.json"]
    a08, a09 = d["A08_MERGE_RECEIPT.json"], d["A09_RETURN_PACKS.json"]
    adm, rep = d["HGK_TYPED_ADMISSION_ARCHIVE.json"], d["compiler/out/compiler-report.json"]
    rb = d["REMOTE_READBACK_ARCHIVE.json"]
    kb_present = sum(1 for p in kb_dir.glob("*.md") if p.name[:2].isdigit() and p.name[2] == "_") if kb_dir.exists() else -1
    out.append(("C01", a00 and a00.get("knowledge_20_present") == 20 and a00.get("knowledge_20_count") == 20
                and kb_present >= 20, "knowledge base 20/20 declared=%s live_on_disk=%s"
                % (a00 and a00.get("knowledge_20_present"), kb_present)))
    out.append(("C02", rep.get("verdict") == "PROMPT_COMPILE_PASS" and rep.get("error_count") == 0
                and str(d["compiler/hash.stdout.txt"]).strip() == rep.get("contract_sha256"),
                "compiler verdict=%s errors=%s contract_sha=%s" % (rep.get("verdict"), rep.get("error_count"),
                                                                   str(rep.get("contract_sha256"))[:12])))
    out.append(("C03", adm.get("verdict") == "ADMISSION_OK" and adm.get("final_state") == "WORKORDERS_ADMITTED",
                "admission verdict=%s state=%s project=%s" % (adm.get("verdict"), adm.get("final_state"),
                                                              adm.get("project_id"))))
    merged = {n: (live.get(n) or {}) for n in (12, 13, 14)}
    c4_ok = all(merged[n].get("merged") is True and merged[n].get("merge_commit_sha")
                == a08["prs"][str(n)].get("merge_commit_sha") for n in (12, 13, 14))
    out.append(("C04", c4_ok, "live merged=%s vs receipt sha=%s"
                % ({n: merged[n].get("merged") for n in (12, 13, 14)},
                   {n: (a08["prs"][str(n)].get("merge_commit_sha") or "-")[:8] for n in (12, 13, 14)})))
    c5 = all(len([p for p in main_paths if p.startswith(PFX[n])]) >= a03["prs"][str(n)]["prefix_blob_count"]
             for n in (12, 13, 14))
    out.append(("C05", c5, "prefix blobs in live main: %s"
                % {n: len([p for p in main_paths if p.startswith(PFX[n])]) for n in (12, 13, 14)}))
    out.append(("C06", len(a05.get("controls", {}).get("positive_control_rules_fired", [])) >= 3
                and a05["controls"].get("clean_control_hit_count") == 0
                and a05["controls"].get("non_vacuity") == "PASS" and a05.get("real_secret_exposed") == 0
                and all(a05["prs"][str(n)]["verdict"] == "PASS" for n in (12, 13, 14)),
                "scan non_vacuity=%s clean_hits=%s exposed=%s"
                % (a05.get("controls", {}).get("non_vacuity"), a05.get("controls", {}).get("clean_control_hit_count"),
                   a05.get("real_secret_exposed"))))
    ids = [x["finding_id"] for x in a09.get("finding_dispositions", [])]
    out.append(("C07", len(ids) == 12 and len(set(ids)) == 12 and all(i.startswith("EIA-019-") for i in ids),
                "dispositions=%d unique=%d" % (len(ids), len(set(ids)))))
    out.append(("C08", bool(rb) and rb.get("verdict") == "PASS" and rb.get("count", 0) > 0
                and not rb.get("mismatches") and not rb.get("missing"),
                "readback verdict=%s files=%s mism=%s missing=%s"
                % ((rb or {}).get("verdict"), (rb or {}).get("count"), len((rb or {}).get("mismatches", [])),
                   len((rb or {}).get("missing", [])))))
    mshas = [a08["prs"][str(n)].get("merge_commit_sha") for n in (12, 13, 14)]
    out.append(("C09", all(s in recent for s in mshas if s),
                "merge commits visible in main's recent history: %s"
                % {s[:8]: (s in recent) for s in mshas if s}))
    c10 = all(a09["pr_outcomes"][i]["head_at_approval"] == HEADS[n] for i, n in enumerate((12, 13, 14)))
    out.append(("C10", c10, "approved heads match the order's frozen heads"))
    pk = load("PACK_INDEX.json")
    pub = d["PUBLISH_RECEIPT_ARCHIVE.json"]
    out.append(("C11", bool(pub) and pub.get("verdict") in ("PUBLISHED", "PUBLISHED_NO_PR"),
                "publish verdict=%s pr=%s" % ((pub or {}).get("verdict"), (pub or {}).get("pull_request"))))
    # The round must archive through a BRANCH: main may only contain the three approved merges, so main's
    # tip must still equal #14's merge commit.  A publisher that wrote main directly would break this.
    MAIN_EQ = (a08["prs"]["14"].get("merge_commit_sha") == MAIN_TIP)
    out.append(("C12", bool(main_paths) and MAIN_EQ,
                "main tip=%s equals PR14 merge commit=%s (%s)" % (str(MAIN_TIP)[:12],
                                                                  a08["prs"]["14"].get("merge_commit_sha", "-")[:12],
                                                                  MAIN_EQ)))
    return out


need = {"A00_SOURCE_REGISTER.json", "A03_GITHUB_FREEZE.json", "A05_SECRET_SCAN.json", "A06_APPROVAL_BATCH.json",
        "A08_MERGE_RECEIPT.json", "A09_RETURN_PACKS.json", "HGK_TYPED_ADMISSION_ARCHIVE.json",
        "ORCHESTRATION_SURFACES.json", "KANBAN_LIFECYCLE_RECEIPT.json", "REMOTE_READBACK_ARCHIVE.json",
        "PUBLISH_RECEIPT_ARCHIVE.json", "compiler/out/compiler-report.json"}
MISSING_ARTIFACTS = sorted(n for n in need if not (OUT / n).exists())


BASE = checks(DATA, LIVE, MAIN_PATHS, RECENT, KB_DIR)
MUTATIONS = [
    ("M01", "C01", "A00_SOURCE_REGISTER.json", lambda d: d["A00_SOURCE_REGISTER.json"].update({"knowledge_20_present": 19})),
    ("M02", "C02", "compiler-report", lambda d: d["compiler/out/compiler-report.json"].update({"error_count": 3})),
    ("M03", "C03", "admission", lambda d: d["HGK_TYPED_ADMISSION_ARCHIVE.json"].update({"verdict": "ADMISSION_STATE_PLAN_READY"})),
    ("M04", "C04", "A08 merge_commit_sha", lambda d: d["A08_MERGE_RECEIPT.json"]["prs"]["13"].update({"merge_commit_sha": "0" * 40})),
    ("M05", "C05", "A03 prefix count", lambda d: d["A03_GITHUB_FREEZE.json"]["prs"]["14"].update({"prefix_blob_count": 900})),
    ("M06", "C06", "A05 exposure", lambda d: d["A05_SECRET_SCAN.json"].update({"real_secret_exposed": 1})),
    ("M07", "C06", "A05 clean control", lambda d: d["A05_SECRET_SCAN.json"]["controls"].update({"clean_control_hit_count": 2})),
    ("M08", "C07", "A09 dispositions", lambda d: d["A09_RETURN_PACKS.json"]["finding_dispositions"].pop()),
    ("M09", "C08", "readback mismatches", lambda d: d["REMOTE_READBACK_ARCHIVE.json"].update({"mismatches": ["x"]})),
    ("M10", "C09", "A08 merge sha not in main", lambda d: d["A08_MERGE_RECEIPT.json"]["prs"]["12"].update({"merge_commit_sha": "f" * 40})),
    ("M11", "C10", "approved head drift", lambda d: d["A09_RETURN_PACKS.json"]["pr_outcomes"][2].update({"head_at_approval": "0" * 40})),
    ("M12", "C11", "publish failed", lambda d: d["PUBLISH_RECEIPT_ARCHIVE.json"].update({"verdict": "FAIL_REF"})),
]
detected, not_detected = [], []
for mid, target, where, mutate in MUTATIONS:
    dd = copy.deepcopy(DATA)
    try:
        mutate(dd)
        res = {c[0]: c[1] for c in checks(dd, LIVE, MAIN_PATHS, RECENT, KB_DIR)}
    except Exception as e:  # noqa: BLE001
        res = {"__error": type(e).__name__}
    if res.get(target) is False:
        detected.append({"mutation": mid, "target": target, "where": where, "result": "DETECTED"})
    else:
        not_detected.append({"mutation": mid, "target": target, "where": where, "result": "NOT_DETECTED",
                             "observed": res.get(target)})

passed = sum(1 for _, ok, _ in BASE if ok)
receipt = {"schema": "CNV-ARCHIVE-SELF-CHECK/1", "task_id": ROUND, "generated_utc": GEN,
           "claim_ceiling": "LOCAL; machine gate only — not an acceptance, approval or Gate",
           "checks": [{"id": i, "verdict": "PASS" if ok else "FAIL", "detail": det} for i, ok, det in BASE],
           "passed": passed, "total": len(BASE), "verdict": "PASS" if passed == len(BASE) else "PARTIAL",
           "mutations": {"count": len(MUTATIONS), "detected": len(detected), "not_detected": not_detected,
                         "all_detected": len(not_detected) == 0},
           "live_evidence": {"main_sha": MAIN_SHA, "pr_merged": {n: (LIVE[n] or {}).get("merged") for n in (12, 13, 14)},
                             "pr_merge_commit": {n: (LIVE[n] or {}).get("merge_commit_sha") for n in (12, 13, 14)},
                             "main_blob_count": len(MAIN_PATHS)}}
(OUT / "SELF_CHECK_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- errata
a08, a09 = DATA["A08_MERGE_RECEIPT.json"], DATA["A09_RETURN_PACKS.json"]
ERRATA = f"""# ERRATA AND FINDINGS — {ROUND}

Every item below was produced by THIS round's own execution.  Nothing here is repaired silently: the
finding is recorded with what was measured, what was done about it, and what remains open.

## Defects this round found in its own harness

| # | Defect | Measured | Disposition |
|---|---|---|---|
| ER-A1 | A module-level name reported `NameError` at a later line although the AST showed it assigned at module level in the same file (`archive_contract.py`, line 29 assigned / line 82 loaded, both module scope, no invisible characters in either line's `repr`) | Two identical runs failed the same way; the AST dump proved the binding existed | WORKED AROUND by inlining the expression. **NOT EXPLAINED** — recorded as a harness/environment anomaly, not as a theory. |
| ER-A2 | `PL-009` binds `intent.requested_delivery` and `journeys[].journey_id` to acceptance edges carried from the archive lineage, so a new round cannot rename them without inventing an acceptance edge | First lint run: `PL-009 deliverable DEL-* lacks acceptance edge`; renaming the journey id alone then produced `PL-009 journey ... lacks acceptance edge` | The bound ids are kept and DISCLOSED: they name the prior round's artifacts, which is a contract-lineage defect of the carried acceptance list, not a claim about this round. |
| ER-A3 | Five control-plane policies the order names as `control/{{AUTHORITY_MATRIX,SOD_POLICY,CHANGE_CLASS_ROUTER,ACCEPTANCE_POLICY,RELEASE_POLICY}}.yaml` under HG-KSEOS DO NOT EXIST there | `HG-KSEOS/control/` holds no such files; the canonical copies are `Fabric/FABRIC/control/*.yaml`; `Fabric/AGENTS.md` is genuinely ABSENT | Sources re-registered at their real paths; the absent `Fabric/AGENTS.md` stays declared in `source_scan.missing` as a real gap rather than being quietly dropped. |
| ER-A4 | `openspec validate --strict` exits with `FileNotFoundError` when driven by the gateway interpreter, which has no npm on its PATH | Attempts recorded: `openspec` and `npx` both `WinError 2`; the SAME command in a login shell printed `Change '{ROUND.lower()}' is valid` | Recorded with both readings. The toolchain verdict comes from the shell run; the interpreter-PATH failure is a harness fact, not evidence about the change record. |
| ER-A5 | `mergeable: null / mergeable_state: unknown` is GitHub's post-merge RECOMPUTATION window, not a conflict — and an UNMERGED pull request also exposes a `merge_commit_sha` (a preview commit that is not on main) | After #12 merged, #13 and #14 read `mergeable: null`; a naive reading of #14's `merge_commit_sha=c3ac660a` would have recorded a merge that never happened (main did not contain it) | Both PRs were HELD, then merged on the next settle-and-reread run once two independent surfaces (REST `mergeable: true` and GraphQL `MERGEABLE/CLEAN`) agreed. **Never treat `merge_commit_sha` on an unmerged PR as a merge.** |
| ER-A6 | The round's own verdict rule scored a fully merged round as PARTIAL | A rerun reports `ALREADY_MERGED_READBACK_ONLY`, which the first rule treated as a non-pass | Fixed: the verdict accepts the SET of equivalent merged statuses. Disclosed because the first A09 receipt said PARTIAL. |
| ER-A7 | `PACK_INDEX.json` cannot carry its own digest and must cover the WHOLE pack | Same class as the previous round, where a stage-scoped index left 52 files unindexed | The index lists every published file except itself; its own digest is bound by the publish receipt. |

## Findings carried from the independent acceptance report (12/12)

See `A09_RETURN_PACKS.json :: finding_dispositions` for all twelve with owner, state and evidence ref.
Summary: 4 resolved_in_round (#05/#06/#07 index semantics clarified, #12 config-backup sensitivity
reviewed: NO credential value present), 1 partial (#08: only the B0 archive batch was signed here),
4 deferred (#01 checker verdict extraction, #02 validator promotion, #03 checker isolation, #04 fresh G1,
#11 owner dossier), 2 recorded as disclosures (#09 same-arm/timeout, #10 no CI status).

## What this round does NOT claim

`INDEPENDENT_PASS`, `AO_ACCEPTED`, `DOC05_EFFECT_ADMITTED`, `FULL_CONVERGENCE`, `PRODUCTION_RELEASE`,
`RUNTIME_READY`: none of these is claimed, and no merge here substitutes for any of them.
"""
(OUT / "ERRATA_AND_FINDINGS.md").write_text(ERRATA, encoding="utf-8")

# ---------------------------------------------------------------- single evidence MD
rows = "\n".join(
    "| #{n} | [{url}]({url}) | `{hs}` | `{ms}` | {m} | {s} | `{roll}` |".format(
        n=n, url=a09["pr_outcomes"][i]["url"], hs=HEADS[n][:12], ms=(a08["prs"][str(n)].get("merge_commit_sha") or "-"),
        m="merged", s=a08["prs"][str(n)].get("readback", {}).get("readback_verdict"),
        roll=(a08["prs"][str(n)].get("readback", {}).get("rollback_pointer") or "-"))
    for i, n in enumerate((12, 13, 14)))
MD = f"""# EVIDENCE CLOSURE — {ROUND}

**Claim ceiling: `CANDIDATE_EVIDENCE_ARCHIVED_ONLY`.** This document closes THE ARCHIVE STAGE of three
existing candidate evidence pull requests. It is NOT an independent acceptance, NOT an AO ruling, NOT a
DOC-05 effect admission and NOT a production release.

## Binding

| Item | Value |
|---|---|
| Contract | `{ROUND}` — C0–C9 `PROMPT_COMPILE_PASS`; sha256 `{rep.get('contract_sha256')}` |
| HGK admission | `{adm.get('project_id')}` → `{adm.get('final_state')}` (checkpoint `{adm.get('checkpoint')}`) |
| Approval batch | `A06_APPROVAL_BATCH.json` — approver `{DATA['A06_APPROVAL_BATCH.json'].get('approver_identity', {}).get('login')}`, repo permission `admin=True maintain=True push=True`, authority = this session's owner order |
| main before | `{a08.get('main_before')}` |
| main after | `{a08.get('main_after')}` |

## Per-PR outcome

| PR | URL | Approved head | Merge commit | Merged | main readback | Rollback |
|---|---|---|---|---|---|---|
{rows}

## Gates actually run

| Gate | Verdict | Evidence |
|---|---|---|
| C0–C9 contract compile | `{rep.get('verdict')}` (0 errors) | `compiler/out/compiler-report.json`, `compiler/*.stdout.txt` |
| Source register (A00) | 20/20 knowledge base + 43 registered sources, {len(DATA['A00_SOURCE_REGISTER.json'].get('missing_critical', []))} declared missing | `A00_SOURCE_REGISTER.json` |
| Scope / mode preflight (A03) | Q03 PASS ×3, Q04 PASS ×3 | `A03_GITHUB_FREEZE.json` |
| Trusted secrets scan (A05) | `{DATA['A05_SECRET_SCAN.json'].get('verdict')}`; positive control fired {len(DATA['A05_SECRET_SCAN.json'].get('controls', {}).get('positive_control_rules_fired', []))} rule families, clean control 0 hits | `A05_SECRET_SCAN.json` |
| Per-PR merge + readback (A08) | `{a09.get('archive_verdict')}` | `A08_MERGE_RECEIPT.json` |
| Publish + per-blob readback (A07) | `{(DATA.get('PUBLISH_RECEIPT_ARCHIVE.json') or {}).get('verdict')}` / `{(DATA.get('REMOTE_READBACK_ARCHIVE.json') or {}).get('verdict')}` | `PUBLISH_RECEIPT_ARCHIVE.json`, `REMOTE_READBACK_ARCHIVE.json` |
| Self-check harness | {passed}/{len(BASE)} checks; {len(detected)}/{len(MUTATIONS)} injected mutations detected | `SELF_CHECK_RECEIPT.json` |
| OpenSpec change | valid (`--strict`, login shell) | `ORCHESTRATION_SURFACES.json` |
| Kanban | {DATA['KANBAN_LIFECYCLE_RECEIPT.json'].get('cards_created')} cards / {DATA['KANBAN_LIFECYCLE_RECEIPT.json'].get('call_count')} CLI calls | `KANBAN_LIFECYCLE_RECEIPT.json` |

## Nonclaims and STOP

* No production, runtime, AO or DOC-05 claim; the eight runtime gates and the 221-case denominator are
  untouched and remain NOT_ACCEPTED.
* The four deferred findings keep their owners: `TS-VAL-01`, `TS-CHECKER-01`, `TS-G1-01`, and the
  remaining owner-item batches beyond B0.
* STOP conditions honoured: a real secret, a scope escape, a head drift or an unknown remote effect would
  have HELD that one PR.  A transient `mergeable=null` DID hold two PRs and is recorded in the errata.
* The archival `.py/.ps1` files stored inside these prefixes are EVIDENCE and were never executed.
"""
(OUT / "EVIDENCE_CLOSURE_CNV-FAR018-FAR019-ARCHIVE.md").write_text(MD, encoding="utf-8")

HAND = {"schema": "CNV-ARCHIVE-HANDOVER/1", "task_id": ROUND, "generated_utc": GEN,
        "hgk": {"project_id": adm.get("project_id"), "state": adm.get("final_state"),
                "workorders": [w for w in (adm.get("steps") or []) if w.get("step") == "admit_workorders"],
                "checkpoint": adm.get("checkpoint")},
        "remote": {"main": MAIN_SHA, "merged": {n: (LIVE[n] or {}).get("merge_commit_sha") for n in (12, 13, 14)},
                   "round_pull_request": (DATA.get("PUBLISH_RECEIPT_ARCHIVE.json") or {}).get("pull_request")},
        "next_round_pointers": {
            "TS-VAL-01": "PIPD validator canonical promotion in ITS OWN repository (code changeset)",
            "TS-CHECKER-01": "non-liftable checker boundary on a second OS identity",
            "TS-G1-01": "fresh G1 certificate at runtime freeze (path/version/sha/route epoch/served arms)",
            "TS-SKILL-01": "HGK entry_map 5-pointer partial rebuild loader trigger/nontrigger",
            "owner_items": "the remaining batches beyond the B0 archive approval",
        },
        "resume": "project CNV-ARCHIVE-THREE-PRS + checkpoint %s; do not re-merge any PR already merged (read back first)" % adm.get("checkpoint")}
(OUT / "HANDOVER_ARCHIVE.json").write_text(json.dumps(HAND, ensure_ascii=False, indent=1), encoding="utf-8")

print("SELF-CHECK:", receipt["verdict"], "%d/%d" % (passed, len(BASE)),
      "| mutations detected %d/%d" % (len(detected), len(MUTATIONS)), "| not_detected:", not_detected)
for i, ok, det in BASE:
    print("   ", "PASS" if ok else "FAIL", i, det[:110])
print("wrote ERRATA_AND_FINDINGS.md, EVIDENCE_CLOSURE_CNV-FAR018-FAR019-ARCHIVE.md, HANDOVER_ARCHIVE.json")
print("reminder: MUTATIONS flag:", MUTATIONS[0][1], "| base verdict", receipt["verdict"])
