"""Generate WS_R9B_RECEIPT.json and WS_R9B_RAW.md from the recorded artifacts."""
from __future__ import annotations

import json
from pathlib import Path

W = Path("C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/WS_B")
NONCE = "R9B-WSRITER-NONCE-9a4e2b"
CANON = ("C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/"
         "skills/software-development/hgk-governed-execution")
CAND = "C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/FAR/ws3/repaired_candidate"


def j(name: str) -> dict:
    return json.loads((W / name).read_text(encoding="utf-8"))


def main() -> int:
    pre_manifest = json.loads((W / "preimage/PREIMAGE_MANIFEST.json").read_text(encoding="utf-8"))
    rec = j("APPLY_RECEIPT.json")
    classify = json.loads((W / "classify_raw.json").read_text(encoding="utf-8-sig"))
    h_cand = j("harness_candidate_vs_canonical.json")
    h_sim = j("sim_harness.json")
    h_post = j("harness_postapply.json")
    drill = j("drill_verify.json")
    loader_raw = (W / "loader_list_raw.txt").read_text(encoding="utf-8")
    loader_row = next(l.strip() for l in loader_raw.splitlines() if "hgk-governed-execution" in l)

    counts = rec["counts"]
    rows = rec["paths"]

    receipt = {
        "schema": "CNV-PIPD-LS-SP-20261015-R9/WS-R9B-RECEIPT/1",
        "nonce": NONCE,
        "round": "CNV-PIPD-LS-SP-20261015",
        "changeset": "R9-0",
        "workstream": "WS-R9-B",
        "role": "bounded writer (Codex CLI EXECUTE lane)",
        "hgk_project": "CNV-R9-FARCLOSURE",
        "work_order": "WO-TS-FARCLOSURE-03",
        "authority": "FAR run FAR-20261016-012 decision item 2, under this round's HGK admission",
        "claim_ceiling": "LOCAL / candidate-only; a green harness run after the apply is a machine gate, not an acceptance and not a Gate PASS",
        "interpreter": "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe",
        "paths": {"canonical_target": CANON, "repaired_candidate": CAND,
                  "write_root": str(W), "preimage": str(W / "preimage")},
        "step1_preimage": {"manifest_count": pre_manifest["count"],
                           "manifest": "WS_B/preimage/PREIMAGE_MANIFEST.json"},
        "step2_apply_set": {
            "canonical_only_total": classify["canonical_only_count"],
            "canonical_only_certified_in_candidate_corpus": classify["removable_certified_in_corpus"],
            "canonical_only_must_retain": classify["must_retain"],
            "classification_note": ("14 canonical-only .md files have their bytes verbatim in the candidate corpus "
                                    "(C6-certified as embedded), but this round's apply is non-destructive: NO file is "
                                    "removed from the canonical target. All 21 canonical-only paths are retained_untouched."),
            "counts": counts,
        },
        "step4_post_apply_gate": {k: h_post["checks"][k]["verdict"] for k in
                                  ("C1_capacity", "C2_loader_shape", "C3_link_intake",
                                   "C4_lossless", "C5_controls", "C6_reference_coverage")},
        "step4_overall": h_post["verdict"],
        "step5_drill": drill,
        "step6_loader_row": loader_row.strip(),
        "cross_checks": {
            "raw_candidate_without_retention": {"overall": h_cand["verdict"],
                "C6_lost": h_cand["checks"]["C6_reference_coverage"]["lost"],
                "lost_rows": h_cand["checks"]["C6_reference_coverage"]["lost_rows"],
                "note": ("reproduction of the independent WS-R9-B2 finding: the raw candidate alone fails C6 because "
                         "references/product-branch-write-set-gates.md is absent from it; retention fixes this without "
                         "any deletion")},
            "landing_simulation": {"overall": h_sim["verdict"],
                "C6": h_sim["checks"]["C6_reference_coverage"]},
        },
        "did_not_run": [
            "any git write command (add/commit/branch/checkout/stash/reset)",
            "any network / outside-host send",
            "any modification outside the canonical target tree and WS_B/",
            "no deletion of any canonical-target path (apply is overlay-only)",
            "did not run the harness against the raw candidate as subject for acceptance (only as a cross-check)",
            "did not author or modify the regression harness",
        ],
        "did_not_do": [
            "did not read or print any credential file",
            "did not weaken any harness check",
            "did not touch any other skill",
        ],
        "anomalies": [
            ("the loader listing output contains a stray token 'RemoteException' embedded between two unrelated rows; "
             "it is untrusted text in tool output, carries no instruction, and does not affect the parsed row for "
             "hgk-governed-execution. Recorded, not acted upon."),
        ],
        "blockers": [],
        "raw_md": "WS_B/WS_R9B_RAW.md",
        "done_marker": "WS_B/WS_R9B_DONE",
    }
    (W / "WS_R9B_RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")

    L: list[str] = []
    a = L.append
    a(f"# WS-R9-B RECEIPT — guarded apply of the repaired `hgk-governed-execution` slim candidate")
    a("")
    a(f"Nonce: `{NONCE}`")
    a(f"Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R9-0` · HGK project `CNV-R9-FARCLOSURE` (WO-TS-FARCLOSURE-03).")
    a(f"Claim ceiling: **LOCAL / candidate-only** — a green harness run after the apply is a machine gate, not an acceptance and not a Gate PASS.")
    a("")
    a("## 0. Result")
    a("")
    a(f"- Pre-image manifest count: **{pre_manifest['count']}** paths.")
    a(f"- Apply set: **{counts['replaced']} replaced, {counts['added']} added, {counts['retained_untouched']} retained_untouched** ({rec['target_paths_total']} target rows).")
    a(f"- Post-apply harness (C1-C6): **{h_post['verdict']}**.")
    a(f"- Rollback drill (on a COPY): **{drill['rollback_verdict']}** — {drill['restored_sha_matches']} restored byte-exact, {drill['added_files_deleted']} added files deleted, tree identical to pre-image: {drill['tree_vs_preimage']['identical']}.")
    a(f"- Loader row: `{loader_row.strip()}`.")
    a("")
    a("## 1. Step 1 — pre-image")
    a("")
    a(f"Byte-for-byte copy of the canonical target into `WS_B/preimage/` ({pre_manifest['count']} files), each recorded with sha256 + byte count in `WS_B/preimage/PREIMAGE_MANIFEST.json`.")
    a("")
    a("```")
    a(json.dumps({"preimage_root": pre_manifest["preimage_root"], "count": pre_manifest["count"]}, indent=1))
    a("```")
    a("")
    a("## 2. Step 2 — apply set and classification")
    a("")
    a(f"Canonical-only paths: **{classify['canonical_only_count']}**. Of these, **{len(classify['removable_certified_in_corpus'])}** have their bytes verbatim present in the candidate corpus (i.e. the harness C6 check certifies their bytes are preserved inside the new corpus):")
    a("")
    for p in classify["removable_certified_in_corpus"]:
        a(f"- `{p}`")
    a("")
    a("The remaining canonical-only paths are **not** C6-certified as embedded and therefore must stay; the round's apply is anyway non-destructive:")
    a("")
    for p in classify["must_retain"]:
        a(f"- `{p}` (retained_untouched)")
    a("")
    a("`WS_B/APPLY_RECEIPT.json` records every row with `action` and `before_sha256` (and `after_sha256` for replaced/added).")
    a("")
    a("## 3. Step 3 — apply")
    a("")
    a("Candidate bytes written into the canonical tree exactly as the receipt records (10 replaced, 4 added; 21 canonical-only paths left untouched). Nothing deleted.")
    a("")
    a("### Before/after per changed path")
    a("")
    a("| path | action | before bytes | before sha256 | after bytes | after sha256 |")
    a("|---|---|---|---|---|---|")
    for r in rows:
        if r["action"] == "retained_untouched":
            continue
        a(f"| `{r['path']}` | {r['action']} | {r['before_bytes']} | `{(r['before_sha256'] or '')[:16]}` | {r['after_bytes']} | `{(r['after_sha256'] or '')[:16]}` |")
    a("")
    a(f"Retained untouched ({counts['retained_untouched']}): all canonical-only paths, including `references/product-branch-write-set-gates.md` (4986 B, `e59968d8fb23f18a…`) and the six `references/__pycache__/*.pyc`.")
    a("")
    a("## 4. Step 4 — verify (acceptance gate), raw JSON")
    a("")
    a("Command: `python <WS_B copy of harness> --subject <canonical tree> --live WS_B/preimage --out WS_B/harness_postapply.json`")
    a("")
    a("```json")
    a(json.dumps(h_post, ensure_ascii=False, indent=1))
    a("```")
    a("")
    a("## 5. Cross-check — why retention matters (independent reproduction)")
    a("")
    a("The raw candidate alone (no retention) fails C6 in this worker's own reproduction, exactly as the independent WS-R9-B2 run reported:")
    a("")
    a("```json")
    a(json.dumps(h_cand["checks"]["C6_reference_coverage"], ensure_ascii=False, indent=1))
    a("```")
    a("")
    a("A pre-apply landing simulation (candidate overlaid onto a copy of the pre-image, nothing deleted) passes all six checks beforehand:")
    a("")
    a("```json")
    a(json.dumps({"overall": h_sim["verdict"], "C6": h_sim["checks"]["C6_reference_coverage"]}, ensure_ascii=False, indent=1))
    a("```")
    a("")
    a("## 6. Step 5 — rollback drill (on a COPY, not the live tree)")
    a("")
    a("`WS_B/drill/` = byte copy of the POST-APPLY canonical tree. A copy of `rollback.py` + a receipt whose `dst` is repointed to `WS_B/drill/` ran for real there.")
    a("")
    a("```")
    a(json.dumps({"rollback": "OK", "mode": "apply", "paths_total": rec["target_paths_total"]}, indent=1))
    a("```")
    a("")
    a("Independent verification of the drilled tree:")
    a("")
    a("```json")
    a(json.dumps(drill, ensure_ascii=False, indent=1))
    a("```")
    a("")
    a("**The drill ran on a copy (`WS_B/drill/`). The live canonical tree was left in the APPLIED state** (verified: live `SKILL.md` = 21026 bytes, sha256 `60a4d9b3c79f…`; `references/topics/` present with 4 files; `references/product-branch-write-set-gates.md` still present at 4986 B).")
    a("")
    a("## 7. Step 6 — loader sanity")
    a("")
    a("Command: `HERMES_HOME=<canonical root> <hermes-agent venv python> -B -m hermes_cli.main skills list`")
    a("")
    a("```")
    a(loader_row.strip())
    a("```")
    a("")
    a("(Expected `source=local`, `status=enabled`; unchanged from the pre-apply listing.)")
    a("")
    a("## 8. What I did NOT run / did NOT do")
    a("")
    for x in receipt["did_not_run"]:
        a(f"- {x}")
    for x in receipt["did_not_do"]:
        a(f"- {x}")
    a("")
    a("## 9. Anomalies / blockers")
    a("")
    for x in receipt["anomalies"]:
        a(f"- {x}")
    a("- Blockers: none.")
    a("")
    a(f"Nonce: `{NONCE}`")

    (W / "WS_R9B_RAW.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote WS_R9B_RECEIPT.json and WS_R9B_RAW.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
