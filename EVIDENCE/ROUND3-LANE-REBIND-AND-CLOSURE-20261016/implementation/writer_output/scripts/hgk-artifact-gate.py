#!/usr/bin/env python
"""hgk-artifact-gate.py — repaired artifact gate checker (CANDIDATE).

Repairs the defect class D23/D24 (a checker that scanned its own output and returned PASS despite
broken citations):

  * The set of scanned inputs is frozen from the manifest BEFORE any read, and the gate's own
    output path plus every registered producer output are excluded by resolved, case-insensitive
    realpath identity — so a previous output file can never re-enter the scan.
  * Findings are semantic-stable: for identical frozen inputs the emitted findings and the input
    digest are byte-identical regardless of any pre-existing output file.
  * `--out` and an input digest are REQUIRED. A missing/empty input denominator, an unreadable
    manifest, a missing artifact, a sha256 mismatch, or an unresolved citation are named blocking
    findings — never a silent PASS.

Everything is CANDIDATE. Read-only except the single `--out` write.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

GATE_SCHEMA = "HGK-ARTIFACT-GATE/1"
MANIFEST_SCHEMA = "HGK-ARTIFACT-MANIFEST/1"


def _norm(path: Path) -> str:
    return os.path.normcase(os.path.realpath(str(path)))


def _sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with Path(path).open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()
    except OSError:
        return None


def _finding(code: str, path: str, detail: str) -> dict[str, str]:
    return {"code": code, "path": path, "detail": detail}


def compute_input_digest(entries: list[tuple[str, str]]) -> str:
    """Digest of the frozen input set: sorted (relpath, sha256) lines."""
    lines = [f"{rel}\t{digest}" for rel, digest in sorted(entries)]
    blob = "\n".join(lines).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def check_artifacts(
    *,
    workspace: Path,
    manifest: Path,
    output: Path,
    producer_outputs: set[Path] | None = None,
    expected_input_digest: str | None = None,
    declared_input_digest: str | None = None,
) -> dict[str, Any]:
    workspace = Path(workspace)
    manifest = Path(manifest)
    output = Path(output)
    producer_outputs = set(producer_outputs or set())

    excluded = {_norm(output)} | {_norm(p) for p in producer_outputs}

    findings: list[dict[str, str]] = []
    inputs_digest_entries: list[tuple[str, str]] = []

    if not manifest.exists():
        findings.append(_finding("ERR_GATE_MANIFEST_MISSING", str(manifest), "manifest not found"))
        return _report(findings, None, excluded)
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append(_finding("ERR_GATE_MANIFEST_UNREADABLE", str(manifest), f"{type(exc).__name__}: {exc}"))
        return _report(findings, None, excluded)

    # ---- freeze + digest the input denominator (excluding output/producer outputs) ------------
    input_specs = data.get("inputs", [])
    if not isinstance(input_specs, list):
        findings.append(_finding("ERR_GATE_MANIFEST_SCHEMA", str(manifest), "inputs must be a list"))
        input_specs = []
    for spec in input_specs:
        rel = spec.get("path") if isinstance(spec, dict) else str(spec)
        if not rel:
            continue
        resolved = (workspace / rel) if not Path(rel).is_absolute() else Path(rel)
        if _norm(resolved) in excluded:
            continue  # never scan our own output or a registered producer output
        digest = _sha256(resolved)
        if digest is None:
            findings.append(_finding("ERR_GATE_INPUT_UNREADABLE", rel, "input file missing or unreadable"))
            continue
        inputs_digest_entries.append((rel, digest))

    if not inputs_digest_entries:
        findings.append(_finding("ERR_GATE_EMPTY_DENOMINATOR", str(manifest),
                                 "no frozen inputs to check after excluding the output"))
        return _report(findings, None, excluded)

    actual_input_digest = compute_input_digest(inputs_digest_entries)
    declared = expected_input_digest or declared_input_digest or data.get("input_digest")
    if declared and declared != actual_input_digest:
        findings.append(_finding("ERR_GATE_INPUT_DIGEST_MISMATCH", str(manifest),
                                 f"declared={declared} actual={actual_input_digest}"))

    # ---- required artifacts -------------------------------------------------------------------
    required = data.get("required", [])
    if not isinstance(required, list) or not required:
        findings.append(_finding("ERR_GATE_EMPTY_DENOMINATOR", str(manifest), "required[] is empty"))
    for item in required:
        rel = item.get("path")
        want = item.get("sha256")
        if not rel:
            findings.append(_finding("ERR_GATE_MANIFEST_SCHEMA", str(manifest), "required item missing path"))
            continue
        resolved = (workspace / rel) if not Path(rel).is_absolute() else Path(rel)
        if not resolved.exists():
            findings.append(_finding("ERR_GATE_ARTIFACT_MISSING", rel, "required artifact not found"))
            continue
        if want:
            got = _sha256(resolved)
            if got != want:
                findings.append(_finding("ERR_GATE_ARTIFACT_SHA256",
                                         rel, f"declared={want} actual={got}"))

    # ---- citations ----------------------------------------------------------------------------
    for citation in data.get("citations", []):
        target = citation.get("ref") or citation.get("path")
        if not target:
            findings.append(_finding("ERR_GATE_MANIFEST_SCHEMA", str(manifest), "citation missing ref"))
            continue
        resolved = (workspace / target) if not Path(target).is_absolute() else Path(target)
        if not resolved.exists():
            findings.append(_finding("ERR_GATE_CITATION_UNRESOLVED", target, "cited path does not exist"))
        elif _norm(resolved) in excluded:
            # A citation pointing at the gate output is itself a defect.
            findings.append(_finding("ERR_GATE_CITATION_SELF", target, "citation points at the gate output"))

    # Deterministic ordering so findings are semantic-stable.
    findings.sort(key=lambda f: (f["code"], f["path"], f["detail"]))
    return _report(findings, actual_input_digest, excluded)


def _report(findings: list[dict[str, str]], input_digest: str | None, excluded: set[str]) -> dict[str, Any]:
    return {
        "schema": GATE_SCHEMA,
        "claim_ceiling": "CANDIDATE_ONLY",
        "status": "PASS" if not findings else "FAIL",
        "input_digest": input_digest,
        "checked_inputs": input_digest is not None,
        "excluded_paths": sorted(excluded),
        "findings": findings,
        "finding_count": len(findings),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hgk-artifact-gate.py", description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True, help="gate receipt output path (REQUIRED)")
    parser.add_argument("--input-digest", default=None, help="expected frozen-input digest (REQUIRED via this or the manifest)")
    parser.add_argument("--producer-output", action="append", default=[], help="additional producer output to exclude")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest_path = Path(args.manifest)
    declared = args.input_digest
    if declared is None and manifest_path.exists():
        try:
            declared = json.loads(manifest_path.read_text(encoding="utf-8")).get("input_digest")
        except Exception:
            declared = None
    if declared is None:
        # Required input digest absent -> blocking usage failure.
        report = {
            "schema": GATE_SCHEMA,
            "claim_ceiling": "CANDIDATE_ONLY",
            "status": "FAIL",
            "input_digest": None,
            "findings": [_finding("ERR_GATE_NO_INPUT_DIGEST", str(manifest_path),
                                  "an input digest is required (--input-digest or manifest.input_digest)")],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 2

    report = check_artifacts(
        workspace=Path(args.workspace),
        manifest=manifest_path,
        output=Path(args.out),
        producer_outputs={Path(p) for p in args.producer_output},
        expected_input_digest=declared,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                      encoding="utf-8", newline="\n")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
