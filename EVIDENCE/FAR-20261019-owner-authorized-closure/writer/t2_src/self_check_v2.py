#!/usr/bin/env python
"""
A2 - self_check_v2.py

The de-vacuumed re-implementation of the previous round's S8b check.

The previous round's `self_check.py` had:
    check("S8b", "...", True, "declared in this receipt ...")
i.e. it passed the literal `True` as the success value, so it could never fail,
and it computed a variable (`sod_declared`) it never used. This file replaces it
with a COMPUTED verdict.

S8b asserts, over the previous round's lane receipts:
    (a) each receipt's arm gate has required_arm == served_arm;
    (b) the pair of arms is stated (both arms non-empty);
    (c) when the two arms are EQUAL, the round must DECLARE that model-axis
        diversity is absent.

MEASURED REALITY / INTERPRETATION (stated plainly, not hidden):
    The two lane receipts carry the arm equality directly (top-level
    `required_arm` == `served_arm` == "opencode-go/deepseek-v4.1-flash"), but
    they do NOT themselves carry any diversity-absence disclosure text. The
    declaration lives in the round's binding disclosure artifacts:
    `SELF_CHECK_RECEIPT.json` (entry S8b) and the published evidence-closure MD.
    So the disclosure search is run over a NAMED set of sources: the receipts'
    own gate text first, then those binding artifacts. If ANY named source
    declares the absence, (c) is satisfied. This is recorded in the receipt as
    `disclosure_source` and `interpretation`.

Modes:
    (default)           compute S8b on the real inputs AND on an in-memory
                        disclosure-stripped copy, emit one JSON receipt, exit
                        non-zero if the check is VACUOUS (verdict does not
                        change when the disclosure is stripped).
    --negative-control  run the stripped copy and print `NEGATIVE_CONTROL=PASS`
                        only when the check returns FAIL as required.

Exit codes: 0 = as required; 1 = vacuous / negative control did not fail; 2 = IO.
"""

import argparse
import copy
import json
import os
import re
import sys

SCHEMA = "FAR018/DE-VACUUMED-S8B/1"
ARCHIVE = ("C:/Projects/Agent_Workspace/_handover/"
           "CNV-EVIDENCE-ARCHIVE-R7R11-20261016")
RECEIPTS = {
    "EXECUTE": ARCHIVE + "/lane/EXECUTE_RECEIPT.json",
    "VERIFY": ARCHIVE + "/lane/VERIFY_RECEIPT.json",
}
# Binding disclosure artifacts for the same round (searched only as a fallback
# after the receipts' own gate text).
DISCLOSURE_ARTIFACTS = {
    "SELF_CHECK_RECEIPT.json": ARCHIVE + "/SELF_CHECK_RECEIPT.json",
    "EVIDENCE_CLOSURE.md": (ARCHIVE + "/publish/payload/"
                            "EVIDENCE_CLOSURE_CNV-EVIDENCE-ARCHIVE-R7R11-20261016.md"),
}

# A declaration that same-arm model-axis diversity is absent. Deliberately
# requires BOTH a diversity/independence token AND an absence phrase.
DECL_RE = re.compile(
    r"(?:diversit|independen)\w*[^\n]{0,80}?(?:absent|by construction|"
    r"not present|not achieved)",
    re.IGNORECASE,
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def arm_of(receipt):
    """Return (required, served) for one receipt.

    `served` is read from the top-level `served_arm`; the previous round's
    identity_gate carries only `required_arm`, so the equality is completed from
    the top-level served field (documented in the receipt).
    """
    gate = receipt.get("identity_gate") or {}
    required = gate.get("required_arm") or receipt.get("required_arm")
    served = receipt.get("served_arm") or gate.get("served_arm")
    return required, served


def gate_text(receipt):
    """The receipts' own gate text, searched first for a disclosure."""
    return json.dumps(receipt.get("identity_gate") or {}, ensure_ascii=False)


def collect_sources(receipts, artifacts):
    """Ordered [(name, text)] disclosure sources: receipts first, then artifacts."""
    sources = []
    for lane, rc in receipts.items():
        sources.append(("lane/{0}_RECEIPT.identity_gate".format(lane), gate_text(rc)))
    for name, text in artifacts.items():
        sources.append((name, text))
    return sources


def strip_disclosure(text):
    """Remove diversity-absence declarations (the negative-control mutation)."""
    return DECL_RE.sub("[disclosure-stripped]", text)


def evaluate(receipts, sources):
    """Compute the S8b verdict. Returns (verdict, detail dict)."""
    per_lane = {}
    arms = []
    gate_ok = True
    stated_ok = True
    for lane, rc in receipts.items():
        req, srv = arm_of(rc)
        eq = bool(req) and bool(srv) and req == srv
        gate_ok = gate_ok and eq
        stated_ok = stated_ok and bool(req) and bool(srv)
        per_lane[lane] = {"required_arm": req, "served_arm": srv,
                          "required_eq_served": eq}
        arms.append(srv or req)

    arms_equal = bool(arms) and all(a == arms[0] for a in arms)

    disclosure_source = None
    if arms_equal:
        for name, text in sources:
            if DECL_RE.search(text or ""):
                disclosure_source = name
                break

    # (c) only bites when the arms are equal; when they differ, an absence
    # declaration is not required.
    c_ok = (not arms_equal) or (disclosure_source is not None)

    verdict = "PASS" if (gate_ok and stated_ok and c_ok) else "FAIL"
    detail = {
        "per_lane": per_lane,
        "arms_stated": stated_ok,
        "arms_stated_pair": arms,
        "gate_required_eq_served": gate_ok,
        "arms_equal": arms_equal,
        "disclosure_required": arms_equal,
        "disclosure_source": disclosure_source,
        "declaration_present": disclosure_source is not None,
    }
    return verdict, detail


def run(strip):
    receipts = {lane: load_json(path) for lane, path in RECEIPTS.items()}
    artifacts = {}
    for name, path in DISCLOSURE_ARTIFACTS.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                artifacts[name] = fh.read()

    sources = collect_sources(receipts, artifacts)
    if strip:
        sources = [(n, strip_disclosure(t)) for n, t in sources]

    verdict, detail = evaluate(receipts, sources)
    return verdict, detail


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="De-vacuumed S8b same-arm disclosure check (FAR-20261016-018 A2).")
    ap.add_argument("--negative-control", action="store_true",
                    help="strip the disclosure in memory and assert the check returns FAIL")
    args = ap.parse_args(argv)

    try:
        base_verdict, base_detail = run(strip=False)
        stripped_verdict, stripped_detail = run(strip=True)
    except FileNotFoundError as exc:
        sys.stderr.write("IO error: {0}\n".format(exc))
        return 2

    verdict_changes = base_verdict != stripped_verdict
    non_vacuous = verdict_changes and base_verdict == "PASS" and stripped_verdict == "FAIL"

    receipt = {
        "schema": SCHEMA,
        "check": "S8b",
        "what": ("same-arm EXECUTE/VERIFY pair must be COMPUTED and, when the arms "
                 "are equal, the round must DECLARE model-axis diversity absent"),
        "inputs": dict(RECEIPTS),
        "disclosure_artifacts_searched": list(DISCLOSURE_ARTIFACTS),
        "unmodified": {"verdict": base_verdict, **base_detail},
        "stripped": {"verdict": stripped_verdict, **stripped_detail},
        "verdict_changes_on_strip": verdict_changes,
        "non_vacuous": non_vacuous,
        "verdict": base_verdict,
        "interpretation": (
            "The lane receipts carry the arm fields but no diversity-absence text; "
            "that declaration lives in the round's SELF_CHECK_RECEIPT.json (S8b) and "
            "the published evidence-closure MD. The disclosure is therefore searched "
            "in the receipts' identity_gate FIRST and those binding artifacts second; "
            "the satisfying source is named in `disclosure_source`. The previous "
            "round's self_check.py passed a literal `True` here, so it could never fail."
        ),
        "claim_ceiling": ("maker/checker-side local recomputation; NOT an independent "
                          "acceptance and NOT a claim that any finding is closed"),
    }
    sys.stdout.write(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    sys.stdout.write("S8B={0}\n".format(base_verdict))

    if args.negative_control:
        ok = stripped_verdict == "FAIL"
        sys.stdout.write("NEGATIVE_CONTROL={0}\n".format("PASS" if ok else "FAIL"))
        return 0 if ok else 1

    # Default: exit non-zero if the check is vacuous.
    if not non_vacuous:
        sys.stderr.write("VACUOUS: verdict did not change PASS->FAIL when stripped\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
