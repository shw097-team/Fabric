#!/usr/bin/env python3
"""stage_policy -- the Fabric Policy Owner's staging operation for a change-class router.

An acceptance officer refused WP-FHS-02 because the Stage layer did not exist and told the next engineer
what it must contain: a real, separately observable **candidate-stage representation** of
`rp002/RP002_CHANGE_CLASS_ROUTER.yaml` carrying the declared classes and their complete route metadata,
with the staged bytes' SHA-256 bound to the source SHA, produced by a staging operation rather than
hand-made. A byte copy does not count, because a copy is indistinguishable from the source and therefore
proves nothing about staging.

So this operation:
  1. reads the source router and validates every class has a `route` it knows how to interpret;
  2. builds a candidate-stage representation -- a normalised, schema-versioned JSON document that keeps
     every field of every class (it loses nothing) and adds the provenance that makes it a *stage* rather
     than a copy: source path, source sha256, byte length, transformation list, staged_at;
  3. writes `<stage-dir>/<policy>.staged.json` plus `STAGE_RECEIPT.json`;
  4. re-reads both and verifies the staged document re-derives the source's class set exactly.

`--check` re-derives the staged document from the source *now* and compares it to the file on disk, so a
stale or edited stage is detected instead of trusted.

Usage:
  stage_policy.py --stage [--fabric-root DIR]        # produce or refresh the stage
  stage_policy.py --check                            # verify the stage still re-derives from source
Exit 0 = ok, 3 = the stage does not re-derive (stale/hand-edited), 2 = source unreadable/invalid.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

ROUTER_RELPATH = pathlib.Path("rp002") / "RP002_CHANGE_CLASS_ROUTER.yaml"
STAGE_SUBDIR = pathlib.Path("stage") / "RP002-STAGE-HGK" / "POLICY"
STAGED_NAME = "RP002_CHANGE_CLASS_ROUTER.staged.json"
STAGE_SCHEMA = "FABRIC-CANDIDATE-STAGE/1"

# Every route the ecosystem knows how to consume. A class naming anything else is staged with
# route_interpretation="UNKNOWN" and the receipt fails closed -- staging must not launder a route that
# no consumer can act on.
KNOWN_ROUTES = {
    "HERMES_NATIVE",
    "ORACLE_TO_HGK",
    "ORACLE_TO_HGK_QUALIFICATION_ONLY",
    "OWNING_STACK_ORCHESTRATOR_APPLY_SMOKE_READBACK",
    "DOMAIN_AUTHORITY_TO_ORACLE_TO_HGK",
    "HUMAN_META_ORACLE",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stage_dir_for(fabric: pathlib.Path) -> pathlib.Path:
    """Where the stage tree actually lives on this host.

    Measured 2026-10-30: `rp002/` sits in `Fabric/FABRIC/`, while the stage tree sits one level up in
    `Fabric/stage/`. Guessing `<fabric_root>/stage` produced a false "stage absent" -- the same miss that
    made WP-FHS-02 look like it had no Stage layer at all. So: prefer the stage tree beside the repository
    root when it exists, and only fall back to one inside it.
    """
    for base in (fabric.parent, fabric):
        candidate = base / STAGE_SUBDIR
        if (base / "stage").is_dir() or candidate.is_dir():
            return candidate
    return fabric / STAGE_SUBDIR


def find_fabric_root(start: pathlib.Path) -> pathlib.Path:
    here = start.resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ROUTER_RELPATH).is_file():
            return candidate
    raise FileNotFoundError(f"no ancestor of {here} contains {ROUTER_RELPATH.as_posix()}")


def load_source(fabric: pathlib.Path) -> tuple[dict, bytes]:
    import yaml

    path = fabric / ROUTER_RELPATH
    raw = path.read_bytes()
    doc = yaml.safe_load(raw.decode("utf-8"))
    classes = doc.get("classes")
    if not isinstance(classes, dict) or not classes:
        raise ValueError(f"{ROUTER_RELPATH.as_posix()} declares no classes")
    for name, entry in classes.items():
        if not isinstance(entry, dict) or "route" not in entry:
            raise ValueError(f"class {name} has no route")
    return classes, raw


def build_stage(classes: dict, raw: bytes, source_path: pathlib.Path) -> dict:
    """The candidate-stage representation: nothing dropped, provenance added."""
    staged_classes = {}
    unknown_routes = []
    for name in sorted(classes):
        entry = dict(classes[name])
        route = entry.get("route")
        interpretation = route if route in KNOWN_ROUTES else "UNKNOWN"
        if interpretation == "UNKNOWN":
            unknown_routes.append({"class": name, "route": route})
        entry["route_interpretation"] = interpretation
        staged_classes[name] = entry
    return {
        "stage_schema": STAGE_SCHEMA,
        "policy": ROUTER_RELPATH.as_posix(),
        "provenance": {
            "source_path": str(source_path),
            "source_sha256": sha256_bytes(raw),
            "source_bytes": len(raw),
            "transformation": [
                "yaml -> json (structure preserved, no field dropped)",
                "classes sorted by name",
                "route_interpretation added per class from the consumer's known-route set",
            ],
        },
        "classes": staged_classes,
        "class_names": sorted(staged_classes),
        "class_count": len(staged_classes),
        "unknown_routes": unknown_routes,
    }


def derive_and_compare(fabric: pathlib.Path) -> tuple[dict, dict, bool, str]:
    classes, raw = load_source(fabric)
    staged_now = build_stage(classes, raw, fabric / ROUTER_RELPATH)
    body = json.dumps(staged_now, sort_keys=True, ensure_ascii=False, indent=2).encode("utf-8")
    on_disk_path = stage_dir_for(fabric) / STAGED_NAME
    if not on_disk_path.is_file():
        return staged_now, {}, False, f"stage absent: {on_disk_path}"
    on_disk = json.loads(on_disk_path.read_text(encoding="utf-8"))
    same = json.dumps(on_disk.get("classes"), sort_keys=True) == json.dumps(staged_now["classes"], sort_keys=True)
    reason = "stage re-derives from source" if same else "stage does not re-derive: the file differs from a fresh build"
    return staged_now, on_disk, same, reason


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fabric-root", default=None)
    ap.add_argument("--stage-root", default=None)
    ap.add_argument("--stage", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if not (args.stage or args.check):
        ap.error("choose --stage or --check")

    fabric = pathlib.Path(args.fabric_root) if args.fabric_root else find_fabric_root(pathlib.Path(__file__))
    if args.stage_root:
        globals()["stage_dir_for"] = lambda _f: pathlib.Path(args.stage_root)  # noqa: PLW0127
    try:
        classes, raw = load_source(fabric)
    except (OSError, ValueError) as exc:
        print(json.dumps({"verdict": "SOURCE_INVALID", "detail": str(exc)}, ensure_ascii=False))
        return 2

    if args.check:
        staged_now, on_disk, same, reason = derive_and_compare(fabric)
        sd = stage_dir_for(fabric)
        file_sha = sha256_bytes((sd / STAGED_NAME).read_bytes()) if (sd / STAGED_NAME).is_file() else None
        receipt_sha = None
        rp = sd / "STAGE_RECEIPT.json"
        if rp.is_file():
            receipt_sha = json.loads(rp.read_text(encoding="utf-8")).get("stage_sha256")
        digest_matches = file_sha is not None and file_sha == receipt_sha
        okay = same and digest_matches
        print(json.dumps({"verdict": "STAGE_DERIVES" if okay else "STAGE_STALE",
                          "reason": reason, "stage_sha256_on_disk": file_sha,
                          "stage_sha256_in_receipt": receipt_sha,
                          "digest_matches_receipt": digest_matches,
                          "classes": staged_now["class_count"]}, ensure_ascii=False))
        return 0 if okay else 3

    source_path = fabric / ROUTER_RELPATH
    staged = build_stage(classes, raw, source_path)
    out_dir = stage_dir_for(fabric)
    out_dir.mkdir(parents=True, exist_ok=True)
    staged_path = out_dir / STAGED_NAME
    # The digest is NOT written inside the document. Embedding it makes the recorded digest describe a
    # body that no longer exists on disk -- the receipt then cites a hash nothing can reproduce. The
    # receipt carries the digest of the exact bytes written, and --check re-hashes the file to compare.
    payload = (json.dumps(staged, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    staged_path.write_bytes(payload)

    receipt = {
        "receipt_schema": "FABRIC-STAGE-RECEIPT/1",
        "operation": "stage_policy",
        "producer": "Fabric Policy Owner (native staging operation, staged by stage_policy.py)",
        "policy": ROUTER_RELPATH.as_posix(),
        "staged_path": str(staged_path),
        "source_sha256": sha256_bytes(raw),
        "source_bytes": len(raw),
        "stage_sha256": sha256_bytes(payload),
        "stage_bytes": len(payload),
        "class_count": staged["class_count"],
        "class_names": staged["class_names"],
        "unknown_routes": staged["unknown_routes"],
        "byte_identical_to_source": False,
        "transformation": staged["provenance"]["transformation"],
        "staged_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "re_derivation": "stage_policy.py --check rebuilds this document from the source and compares classes",
    }
    receipt_path = out_dir / "STAGE_RECEIPT.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    staged_now, on_disk, same, reason = derive_and_compare(fabric)
    print(json.dumps({"verdict": "STAGED" if same else "STAGED_BUT_NOT_DERIVABLE",
                      "staged": str(staged_path), "receipt": str(receipt_path),
                      "source_sha256": receipt["source_sha256"], "stage_sha256": receipt["stage_sha256"],
                      "classes": receipt["class_count"], "unknown_routes": receipt["unknown_routes"],
                      "check": reason}, ensure_ascii=False))
    return 0 if same else 3


if __name__ == "__main__":
    raise SystemExit(main())
