# -*- coding: utf-8 -*-
"""WO-SKCV-20261014-HGK phase 2 maker: consolidate skill/references into owned topics.

PARTIAL_TOPIC_ONLY. Moves the COMPLETE original bytes of every Markdown reference
file into at most 8 visible topic files (envelope + verbatim segment), leaves a
visible compatibility stub at each absorbed original path, and records every
original file (sha256 + destination + coverage verdict) in consolidation_map.json.

Rerun-safe: refuses if a prior consolidation is present. Never touches SKILL.md
bytes, skill/scripts/skill_guard.py, the 100k cap, the 24k body advisory, the
60-reference warning threshold, mutation locks, or any policy. Executable/JSON
assets are RETAINED as real files (not hidden, not absorbed).
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = "skill/references"
TOPICS = REF + "/topics"
CONSTRUCTION = REF + "/topics/construction-wave-and-remaining-procedures.md"
NAMED_INPUT = "skill/references/topic-source-remainder.md"
MAIN = "skill/SKILL.md"
STUB_MARK = "Original bytes preserved, not rewritten."
ENV_RE = re.compile(r'<!-- SKCV-SEG path="([^"]+)" offset=(\d+) len=(\d+) seq=(\d+) sha256=([0-9a-f]{64}) -->')

THEMES = [
    ("topic-governance-admission-and-authority.md",
     "Governance admission, authority determination, shared-core changesets and method contracts",
     ["bundle-specification-discipline.md", "candidate-apply-gates.md",
      "capc-contract-building.md", "construction-acceptance-prompt-compiler.md",
      "corpus-freeze-and-digest-reconciliation.md",
      "fabric-rule-to-code-gap-and-invariant-spoof.md", "false-green-verification-traps.md",
      "governance-knowledge-map.md", "governance-ordering-and-binding-proof.md",
      "landing-authored-suites.md", "method-finalization-contract.md",
      "negative-pnl-method-change-contract.md", "proportional-runtime-config-closure.md",
      "shared-core-change-set-authorization.md", "shared-core-primitive-changeset.md",
      "shared-infra-team-implementation.md", "shared-spine-admission.md",
      "spine-lifecycle-closeout.md",
      "strategy-backtest-correctness-and-method-finalization.md",
      "hgk-ssot-authority-determination.md", "hgk-spine-knowledge-facilities.md"]),
    ("topic-verification-lanes-and-checkers.md",
     "Independent verification lanes, checker authorship and model-lane routing",
     ["a-verdict-experimentspec-contract-verification.md", "acceptance-verification-lane.md",
      "adversarial-verification-rounds.md", "conflicting-challenge-report-adjudication.md",
      "equal-rank-external-conflict-adjudication.md", "focused-hardening-rereview.md",
      "guard-false-positives.md", "harness-and-evidence-defects.md",
      "independent-verifier-lane-pitfalls.md",
      "interrupted-lane-recovery-and-officer-invocation.md", "lane-model-routing-verified.md",
      "model-lane-routing-and-codex-execute-route.md",
      "oneshot-lane-liveness-and-model-proof.md", "plan-model-fallback.md",
      "python-security-review-probes.md", "repair-round-equality-and-closure.md",
      "self-verifying-probe-authoring.md", "validator-authoring-lessons.md",
      "verify-lane-must-be-pinned-oneshot.md", "verifying-lane-declaration-changes.md",
      "delegation-marker-env-leak.md", "hermes-provider-fallback-routing.md",
      "hermes-provider-routing-failover.md"]),
    ("topic-evidence-closure-and-review-packaging.md",
     "External-challenge evidence closure, single-MD packaging and post-acceptance hygiene",
     ["acceptance-mirror-publication.md", "evidence-integrity-lessons.md",
      "external-acceptance-single-md-closure.md", "external-challenge-evidence-closure-far.md",
      "external-challenge-review-closure.md", "external-evidence-closure.md",
      "external-provider-tool-enablement.md", "external-publication-mirror.md",
      "external-rereview-normalization-rebind.md", "external-review-evidence-packaging.md",
      "external-single-md-mandatory-route.md", "external-submission-gates.md",
      "final-closure-resume.md", "final-evidence-reseal-binding.md",
      "gate-blockage-far-research.md", "github-acceptance-bridge.md",
      "order-completion-audit.md", "post-acceptance-subject-hygiene.md",
      "publication-credential-and-handover.md",
      "step-10-external-provider-tool-enablement.md",
      "step-6d-evidence-closure-pipeline.md", "step-evidence-only-contract-a.md"]),
    ("topic-fda-desktop-automation.md",
     "FDA/XQ desktop automation, guardrails, route registry and runtime notes",
     ["fda-authorization-gate.md", "fda-authorization-guardrail-design.md",
      "fda-desktop-automation-cua.md", "fda-folder-reorganization.md",
      "fda-guardrail-implementation-2026-08-15.md", "fda-guardrail-operations.md",
      "fda-guardrail-research-2026-08-15.md", "fda-guardrail-runtime-notes.md",
      "fda-invocation-route-inventory.md", "fda-route-registration.md",
      "fda-upgrade-research-2026-08-14.md", "step-9-fda-cua-operations.md",
      "xq-community-automation-solution.md", "xq-radar-paper-runtime.md",
      "browser-account-automation-under-guard.md"]),
    ("topic-codex-lane-and-workspace.md",
     "Codex sealed lane, workspace-write posture, dispose/cwd locks and lane recovery",
     ["codex-canary-powershell.md", "codex-lane-log-liveness-markers.md",
      "codex-sealed-lane-windows.md", "codex-workspace-write.md",
      "artefact-disposal-and-cwd-locks.md", "opencodex-human-home-hijack-restore.md",
      "spartoi-reopen-preopen-execution.md"]),
    ("topic-step-procedures-and-pitfalls.md",
     "Extracted entry step procedures, support-file index, oversized-skill handling and pitfalls",
     ["oversized-skill-handling-route.md", "oversized-skill-split-notes.md",
      "step-pitfalls-checklist.md", "step-verify-only-lane.md", "support-files-index.md"]),
    ("topic-domain-research-and-recovery.md",
     "Domain research (SQS/Taiwan/T0), cross-session integrity, memory and pre-design discussion",
     ["cross-session-integrity.md", "daytrading-t0-axis-authoritative-chain.md",
      "fsdt-stack-doc-series-research.md", "hermes-memory-full-handling.md",
      "oss-landscape-research.md", "predesign-design-discussion.md",
      "rbwi-4plus1-pack-execution.md", "sqs-data-plane-verification.md",
      "sqs-thc-knowledge-base-research.md", "taiwan-daily-ohlcv-acquisition.md",
      "taiwan-isin-venue-master.md"]),
]

CONSTRUCTION_OWNER = "topic-step-procedures-and-pitfalls.md"


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def relpath(p):
    return os.path.relpath(p, HERE).replace("\\", "/")


def read_bytes(rel):
    with open(os.path.join(HERE, rel), "rb") as fh:
        return fh.read()


def envelope(path, offset, length, seq, digest):
    return ('<!-- SKCV-SEG path="%s" offset=%012d len=%012d seq=%03d sha256=%s -->\n'
            % (path, offset, length, seq, digest))


def stub_text(topic):
    return (
        "# Compatibility stub\n\n"
        "Absorbed into `references/topics/%s`.\n"
        "Original bytes preserved, not rewritten.\n"
        "\n"
        "This stub is compatibility only; it does not reduce the physical reference count.\n"
        % topic)


def build_topics(originals):
    topics, seg_index = {}, {}
    for topic, _desc, members in THEMES:
        member_paths = [REF + "/" + m for m in members]
        if topic == CONSTRUCTION_OWNER:
            member_paths.append(CONSTRUCTION)
        body = bytearray()
        check = []
        for seq, rel in enumerate(member_paths):
            if rel not in originals:
                raise SystemExit("missing member for theme %s: %s" % (topic, rel))
            data = originals[rel]
            digest = sha256(data)
            off = len(body) + len(envelope(rel, 0, 0, 0, "0" * 64))
            body += envelope(rel, off, len(data), seq, digest).encode("ascii")
            body += data
            body += b"\n"
            check.append({"seq": seq, "original_path": rel, "offset": off,
                          "len": len(data), "sha256": digest})
        topics[TOPICS + "/" + topic] = bytes(body)
        seg_index[TOPICS + "/" + topic] = check
    return topics, seg_index


def main():
    if not os.path.exists(os.path.join(HERE, CONSTRUCTION)):
        print("REFUSED: phase-1 topic artifact missing: %s" % CONSTRUCTION)
        return 2
    # rerun guard
    if os.path.exists(os.path.join(HERE, "consolidation_map.json")):
        print("REFUSED: consolidation_map.json already present (rerun not allowed here)")
        return 3
    for d, _dirs, files in os.walk(os.path.join(HERE, TOPICS)):
        for f in files:
            if f.startswith("topic-"):
                print("REFUSED: topic file already present: %s" % f)
                return 3

    main_before = read_bytes(MAIN)
    entry_map_before = read_bytes("entry_map.json")

    # snapshot every original reference file BEFORE any write
    originals = {}
    for d, _dirs, files in os.walk(os.path.join(HERE, REF)):
        for f in files:
            p = os.path.join(d, f)
            rel = relpath(p)
            originals[rel] = read_bytes(rel)

    absorbed = {}
    for topic, _d, members in THEMES:
        for m in members:
            absorbed[REF + "/" + m] = TOPICS + "/" + topic
    absorbed[CONSTRUCTION] = TOPICS + "/" + CONSTRUCTION_OWNER
    retained = sorted(p for p in originals if p not in absorbed)

    topics, seg_index = build_topics(originals)

    os.makedirs(os.path.join(HERE, TOPICS), exist_ok=True)
    for topic_rel, data in topics.items():
        with open(os.path.join(HERE, topic_rel), "wb") as fh:
            fh.write(data)

    for orig, topic in absorbed.items():
        with open(os.path.join(HERE, orig), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(stub_text(os.path.basename(topic)))

    files = []
    for p in sorted(originals):
        data = originals[p]
        rec = {"original_path": p, "sha256": sha256(data), "bytes": len(data)}
        if p in absorbed:
            topic = absorbed[p]
            s = {x["original_path"]: x for x in seg_index[topic]}[p]
            rec["coverage"] = "ABSORBED_VERBATIM"
            rec["destination"] = {"type": "stub", "stub_path": p, "topic": topic,
                                  "offset": s["offset"], "len": s["len"],
                                  "sha256": s["sha256"], "seq": s["seq"]}
        else:
            rec["coverage"] = "RETAINED_REAL_FILE"
            rec["destination"] = {"type": "real", "path": p}
        files.append(rec)

    counts = {"original_reference_files": len(originals),
              "absorbed_md_files": len(absorbed),
              "retained_real_files": len(retained),
              "topic_files": len(topics),
              "files_under_topics_dir": len(topics) + 1}  # + construction-wave stub

    cmap = {"schema": "SKCV-CONSOLIDATION-MAP/1", "task": "WO-SKCV-20261014-HGK",
            "phase": "PARTIAL_TOPIC_ONLY",
            "path_convention": "repo-root-relative, forward slashes",
            "envelope_format": '<!-- SKCV-SEG path="<rel>" offset=<12d> len=<12d> seq=<3d> sha256=<hex> -->',
            "topics": seg_index, "files": files, "retained_real_files": retained,
            "counts": counts,
            "physical_alias_count_debt": "OPEN - stubs are real files; topic ownership does "
                                         "not reduce the physical reference count."}
    with open(os.path.join(HERE, "consolidation_map.json"), "w", encoding="utf-8") as fh:
        json.dump(cmap, fh, indent=2, sort_keys=True)

    missing = []
    if not os.path.exists(os.path.join(HERE, NAMED_INPUT)):
        missing.append({"named_input": NAMED_INPUT, "status": "NOT_FOUND",
                        "verdict": "INCONCLUSIVE",
                        "note": "phase-1 wrote topics/construction-wave-and-remaining-procedures.md "
                                "in this candidate; the literal named path does not exist, so it "
                                "is refused rather than fabricated."})
    orphans = [{"topic": t, "reason": "no stub references this topic"}
               for t in sorted(topics)
               if not [p for p in absorbed if absorbed[p] == t]]
    report = {"schema": "SKCV-MISSING-ORPHAN-REPORT/1", "task": "WO-SKCV-20261014-HGK",
              "phase": "PARTIAL_TOPIC_ONLY", "missing_named_inputs": missing,
              "orphan_topics": orphans, "dangling_links": [],
              "refusal_first_verdict": "INCONCLUSIVE" if missing else "OK",
              "notes": ["Absorbed Markdown originals are replaced by visible compatibility "
                        "stubs; executable/JSON assets are retained as real files.",
                        "physical alias-count debt is OPEN; topic ownership is an engineering "
                        "improvement, not a warning suppression."]}
    with open(os.path.join(HERE, "missing_orphan_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)

    em = json.loads(entry_map_before.decode("utf-8"))
    if not os.path.exists(os.path.join(HERE, "entry_map.phase1.json")):
        with open(os.path.join(HERE, "entry_map.phase1.json"), "wb") as fh:
            fh.write(entry_map_before)
    cw_seg = {x["original_path"]: x for x in seg_index[TOPICS + "/" + CONSTRUCTION_OWNER]}[CONSTRUCTION]
    moved = []
    for sl in em["slices"]:
        if sl["dest"]["file"] == CONSTRUCTION:
            old = dict(sl["dest"])
            sl["dest"]["file"] = TOPICS + "/" + CONSTRUCTION_OWNER
            sl["dest"]["start"] = cw_seg["offset"] + old["start"]
            sl["dest"]["end"] = cw_seg["offset"] + old["end"]
            sl["dest"]["len"] = old["len"]
            moved.append({"slice_id": sl["slice_id"], "from": old, "to": dict(sl["dest"])})
    em.setdefault("artifacts", {})["reference"] = TOPICS + "/" + CONSTRUCTION_OWNER
    em["phase2_layout"] = {"schema": "SKCV-ENTRY-MAP-PHASE2-LAYOUT/1",
                           "absorbed_into_topic": TOPICS + "/" + CONSTRUCTION_OWNER,
                           "segment_offset": cw_seg["offset"], "moved_slices": moved,
                           "note": "dest.file/dest offsets updated so entry_map stays consistent; "
                                   "original phase-1 bytes archived at entry_map.phase1.json."}
    with open(os.path.join(HERE, "entry_map.json"), "w", encoding="utf-8") as fh:
        json.dump(em, fh, indent=2, sort_keys=True)

    main_after = read_bytes(MAIN)
    check = {"main_sha_before": sha256(main_before), "main_sha_after": sha256(main_after),
             "main_unchanged": sha256(main_before) == sha256(main_after),
             "entry_map_phase1_sha256": sha256(entry_map_before),
             "counts": counts, "moved_slices": len(moved)}
    with open(os.path.join(HERE, "phase2_layout.json"), "w", encoding="utf-8") as fh:
        json.dump(check, fh, indent=2, sort_keys=True)
    print("counts=%s moved_slices=%d main_unchanged=%s"
          % (counts, len(moved), check["main_unchanged"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
