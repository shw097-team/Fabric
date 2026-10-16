#!/usr/bin/env python3
"""Admit the HG-KSEOS control-plane obligation to install the credential broker.

This is the CONTROL-PLANE admission for the broker's durable install. It is
deliberately NOT run by the PIPD R10 product round: per FAR-PIPD-R8-DISPATCH-004
§4 option B, an edit to HG-KSEOS control-plane tooling "needs its own admission,
and must not ride along inside a PIPD round". This file is the ready-to-run
candidate for that separate admission.

Typed SharedSpine / ProjectLifecycleController API only (no raw SQL), same shape
as .hgk/rounds/R9-.../hgk_r9_admission.py and R10/.../hgk_r10_admission.py.

`admit_requirement` only succeeds while the target project is in
EXECUTING / PLAN_READY / WORKORDERS_ADMITTED (lifecycle.py:566). Two routes:

  (A) MINIMAL -- reuse an existing HG-KSEOS control-plane project already in an
      admissible state, e.g. HGK-CHU-20261009 (EXECUTING; it already carries the
      credential obligations REQ-CHU-R2-04-CREDENTIAL-SCRUB and
      REQ-CHU-R2-05-BRIDGE-CONFIG). One typed call, no new lifecycle:

        python hgk_cred_admission.py \
          --hgk-root C:/Projects/Agent_Workspace/HG-KSEOS \
          --project-id HGK-CHU-20261009 \
          --out <control-plane-round>/admission

  (B) OWN ROUND -- create a dedicated control-plane lifecycle project first (a
      new project starts at PROJECT_CREATED, which is NOT admissible, so it must
      be driven along the main path to PLAN_READY):

        hgk project start --project-id HGK-CREDBROKER-20261011 \
            --goal "Install the GitHub credential broker as a standing, non-activated HG-KSEOS control-plane artefact"
        # advance PROJECT_CREATED->SOURCE_DISCOVERY->..->PLAN_READY (see --help),
        then run this script with --project-id HGK-CREDBROKER-20261011.

This script performs ONLY the admission (Requirement freeze -> TaskSpec ->
WorkOrder). It does NOT install the files and does NOT wire/activate anything.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ONE obligation. Close criterion is a machine-checkable oracle so the later
# EXECUTE lane cannot pass on file-existence alone (AGENTS.md: file existence is
# not substantive PASS): files present at the pinned path with matching sha256,
# offline verify PASS, and NO activation reference anywhere in the config tree.
OBLIGATIONS = [
    ("REQ-HGK-CREDBROKER-001", "P0", "CREDENTIAL-BROKER",
     "Install the R9-designed GitHub credential broker (cred_broker.py, cred_preflight.py, "
     "selftest.py) as a STANDING, NON-ACTIVATED control-plane artefact at scripts/cred/ so long "
     "unattended write lanes do not depend on ephemeral agent scratch. Acceptance oracle: (1) the "
     "three modules are present under scripts/cred/ with the sha256 pinned in INSTALL_MANIFEST.json; "
     "(2) verify_offline.py returns PASS_OFFLINE_T5_UNPROVEN or PASS and selftest.py returns 5/5 on "
     "DUMMY credentials; (3) NO lane-routing-registry.yaml, model-lane-assignment.json, dispatcher "
     "or other config references the installed path (non-activated); (4) no secret value appears in "
     "any artefact. This obligation covers INSTALL only; wiring the broker into a live lane is a "
     "separate, later admitted change."),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hgk-root", required=True, type=Path)
    ap.add_argument("--project-id", required=True,
                    help="an HG-KSEOS control-plane project in an admissible state")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--checkpoint", action="store_true")
    ap.add_argument("--evidence", nargs="*", default=[])
    args = ap.parse_args()

    sys.path.insert(0, str(args.hgk_root / "src"))
    from hg_kseos.spine import SharedSpine
    from hg_kseos.lifecycle import ProjectLifecycleController

    spine = SharedSpine(args.hgk_root / "var/shared-spine/hg-kseos.db",
                        args.hgk_root / "src/hg_kseos/schema.sql")
    lc = ProjectLifecycleController(spine)
    args.out.mkdir(parents=True, exist_ok=True)

    try:
        status_before = lc.status(args.project_id)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": f"project not admissible: {type(exc).__name__}: {exc}",
                          "project_id": args.project_id}, ensure_ascii=False))
        return 2

    result: dict = {"step": "admit_requirement", "project_id": args.project_id,
                    "status_before": status_before, "admitted": [], "errors": []}
    for rid, priority, owner, wording in OBLIGATIONS:
        try:
            admitted = lc.admit_requirement(args.project_id, rid, wording,
                                            owner=owner, priority=priority)
            result["admitted"].append(admitted)
        except Exception as exc:  # noqa: BLE001 - record, never hide
            result["errors"].append({"requirement_id": rid, "error": f"{type(exc).__name__}: {exc}"})
    if args.checkpoint:
        result["checkpoint"] = lc.checkpoint(args.project_id, evidence_refs=args.evidence)
    result["status_after"] = lc.status(args.project_id)
    (args.out / "hgk_cred_admission.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1, default=str), encoding="utf-8", newline="")
    print(json.dumps({"step": result["step"], "errors": result["errors"]}, ensure_ascii=False))
    print(json.dumps(result["admitted"], ensure_ascii=False, default=str)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
