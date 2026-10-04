#!/usr/bin/env python3
"""Deterministic intake, report, and Skill-tree checks for challenge-review."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

VERDICTS = {
    "PASS_CHALLENGE",
    "PARTIAL_CHALLENGE",
    "FAIL_CHALLENGE",
    "TEMP_CLOSED_CHALLENGE",
}
CLASSIFICATIONS = {
    "CONFIRMED_DEFECT",
    "EVIDENCE_GAP",
    "ORACLE_DISAGREEMENT",
    "NON_BLOCKING_OBSERVATION",
    "OUT_OF_SCOPE",
}
BLOCKING_FIELDS = {
    "acceptance_id",
    "evidence_id",
    "earliest_owner",
    "smallest_repair",
    "focused_retest",
    "affected_regression",
}
FINDING_REQUIRED_FIELDS = {
    "finding_id",
    "classification",
    "severity",
    "candidate_digest",
    "acceptance_id",
    "evidence_id",
    "source_locator",
    "observed",
    "expected",
    "impact",
    "earliest_owner",
    "smallest_repair",
    "focused_retest",
    "affected_regression",
    "status",
}
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
FINDING_STATUSES = {"OPEN", "TEMP_CLOSED", "ROUTED", "NON_BLOCKING"}
ALLOWED_CLAIM_CEILINGS = {
    "SKILL_CANDIDATE_QUALIFIED",
    "PARTIAL_LOCAL_CHALLENGE",
    "TEMP_CLOSED_LOCAL_CHALLENGE",
    "FAIL_LOCAL_CHALLENGE",
}
VERDICT_CLAIM_CEILING = {
    "PASS_CHALLENGE": "SKILL_CANDIDATE_QUALIFIED",
    "PARTIAL_CHALLENGE": "PARTIAL_LOCAL_CHALLENGE",
    "TEMP_CLOSED_CHALLENGE": "TEMP_CLOSED_LOCAL_CHALLENGE",
    "FAIL_CHALLENGE": "FAIL_LOCAL_CHALLENGE",
}
EDGE_KINDS = {"TEST", "RUNTIME", "PACKAGE", "STATE", "NORMATIVE", "ORACLE", "RECOVERY", "DOMAIN"}
EDGE_STATUSES = {"SUPPORTED", "CONTRADICTED", "MISSING", "UNVERIFIED"}
HANDOFFS = {"CONTINUE", "RESUME_SMALLEST_REPAIR", "META_ORACLE", "DOMAIN_OWNER", "HITL", "TERMINAL"}
REPORT_TOP_LEVEL_FIELDS = {
    "verdict",
    "subject",
    "findings",
    "claim_ceiling",
    "evidence_edges",
    "handoff",
    "rendered_report_pointer",
    "rendered_report_digest",
}
FORBIDDEN_CLAIM_TOKENS = {"RP002_PASS", "PRODUCTION_AUTHORIZED", "FABRIC_EXTERNAL_ACCEPTANCE_COMPLETE"}
TRIGGER_EXPECTATIONS = {
    "T-TRIGGER-001": ("direct_positive", True),
    "T-TRIGGER-002": ("indirect_positive", True),
    "T-TRIGGER-003": ("incomplete_input", True),
    "T-TRIGGER-004": ("oracle_disagreement", True),
    "T-TRIGGER-005": ("rp003_reuse", True),
    "T-TRIGGER-006": ("ordinary_code_review", False),
    "T-TRIGGER-007": ("maker_repair", False),
    "T-TRIGGER-008": ("release_execution", False),
    "T-TRIGGER-009": ("domain_authority", False),
    "T-TRIGGER-010": ("general_explanation", False),
    "T-TRIGGER-011": ("role_drift_request", True),
    "T-TRIGGER-012": ("evidence_negative", True),
}
TRIGGER_PROMPT_SHA256 = {
    "T-TRIGGER-001": "8db3409bd25b487ea6208e94191c7ac7b590ceb7830835ffe19dc93e1bdd3631",
    "T-TRIGGER-002": "dd0ad59433b322609f9abd03824aa253433212679c266472e5290db201352f5c",
    "T-TRIGGER-003": "d3f51d2a20c9f39a7a02113cdd69573d3d44dde36b0df87e42c5f944fb982e39",
    "T-TRIGGER-004": "056fb55600ff26b4fae8cfc2fb87ab1f4cae19674272fc56f735a24cfaf7e3bf",
    "T-TRIGGER-005": "1ea1c68b6dd002a437005d49bbaeea201aa1644cfd2dad1bc210876df9530c58",
    "T-TRIGGER-006": "67a0b481ff2bcac7d9c5a174949262d1b8f3b1be08c3a10121c3b2c0228c2c9f",
    "T-TRIGGER-007": "77a98f08ff77ebabfc4b45c551686fa6b12b74ac365e76ed8859a6c9e9f040f2",
    "T-TRIGGER-008": "d7695558e92a7cc7e94a934f901da9e41c210e77187db07f5ac585b67dee4e63",
    "T-TRIGGER-009": "197f1224d3e96aad3a3c2f7dc1f0a24981f622058eb1a175f5a0a46facb274f1",
    "T-TRIGGER-010": "b3f545a079bf226b56cf8443641975e1d719394e518a2de4634f7b20d627e721",
    "T-TRIGGER-011": "027944489a9055d62b5dd3d579ec342516ef3ff7c8c6e83cd8d4a46ecb3c3aa9",
    "T-TRIGGER-012": "9952c24f9a9d6056d7c040d36f049bc3d8b9143e9a0e08311a399370e356bc74",
}
FINDING_ALLOWED_FIELDS = FINDING_REQUIRED_FIELDS | {"blocking"}
EDGE_BASE_FIELDS = {
    "evidence_id",
    "acceptance_id",
    "artifact_digest",
    "kind",
    "required",
    "status",
    "raw",
    "pointer",
}
TEST_EDGE_FIELDS = EDGE_BASE_FIELDS | {
    "command",
    "environment",
    "denominator",
    "passed",
    "failed",
    "errors",
    "exit_status",
}
REQUIRED_REFERENCES = {
    "evidence-intake.md",
    "gate-calibration.md",
    "finding-contract.md",
    "rp002-profile.md",
    "security-permissions.md",
    "adjudication-resume.md",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_sha256(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


class DuplicateJsonKey(ValueError):
    pass


def strict_json_loads(text: str) -> object:
    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateJsonKey(key)
            result[key] = value
        return result

    return json.loads(text, object_pairs_hook=unique_object)


def sha256_path(path: Path) -> str:
    """Hash a regular file or a symlink-free directory tree deterministically."""
    if path.is_symlink():
        raise ValueError("symlink subject is not allowed")
    if path.is_file():
        return sha256_file(path)
    if not path.is_dir():
        raise ValueError("subject is not a regular file or directory")
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*"), key=lambda value: value.relative_to(path).as_posix()):
        if item.is_symlink():
            raise ValueError(f"symlink in subject tree: {item.relative_to(path).as_posix()}")
        if item.is_file():
            rel = item.relative_to(path).as_posix().encode("utf-8")
            digest.update(len(rel).to_bytes(8, "big"))
            digest.update(rel)
            digest.update(bytes.fromhex(sha256_file(item)))
    return digest.hexdigest()


def resolve_pointer(bundle_root: Path, pointer: object, *, require_file: bool = False) -> tuple[Path | None, str | None]:
    if not isinstance(pointer, str) or not pointer.strip():
        return None, "required non-empty relative path"
    if "\\" in pointer or pointer.startswith("/") or re.match(r"^[A-Za-z]:", pointer):
        return None, "must be a relative canonical path"
    pure = PurePosixPath(pointer)
    if any(part in {"", ".", ".."} for part in pure.parts) or pure.as_posix() != pointer:
        return None, "must be a relative canonical path"
    root = bundle_root.resolve()
    unresolved = root.joinpath(*pure.parts)
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            return None, "symlink component is not allowed"
    resolved = unresolved.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        return None, "escapes bundle root"
    if not resolved.exists():
        return None, "path does not exist"
    if require_file and not resolved.is_file():
        return None, "must point to a regular file"
    return resolved, None


def compare_distribution_to_candidate(candidate: Path, distribution: Path, prefix: object = "") -> list[str]:
    errors: list[str] = []
    if not isinstance(prefix, str) or (
        prefix
        and (
            prefix.startswith("/")
            or "\\" in prefix
            or PurePosixPath(prefix).as_posix() != prefix
            or ".." in PurePosixPath(prefix).parts
        )
    ):
        return ["intake.distribution_prefix: must be a canonical relative path"]
    if candidate.is_file():
        if sha256_file(candidate) != sha256_file(distribution):
            errors.append("intake.distribution_pointer: distribution bytes do not equal frozen file candidate")
        return errors
    if not candidate.is_dir() or not zipfile.is_zipfile(distribution):
        return ["intake.distribution_pointer: directory candidate requires an exact ZIP distribution"]
    try:
        validator_path = Path(__file__).with_name("validate_package.py")
        spec = importlib.util.spec_from_file_location("challenge_review_package_validator", validator_path)
        if spec is None or spec.loader is None:
            return ["intake.distribution_pointer: package validator unavailable"]
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        package_errors = module.validate_archive(distribution, candidate, prefix)
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile):
        return ["intake.distribution_pointer: package validation failed closed"]
    errors.extend(f"intake.distribution_pointer: {error}" for error in package_errors)
    return errors


def render_canonical_markdown(data: dict) -> str:
    subject = json.dumps(data.get("subject", {}), sort_keys=True, separators=(",", ":"))
    findings = json.dumps(data.get("findings", []), sort_keys=True, separators=(",", ":"))
    edges = json.dumps(data.get("evidence_edges", []), sort_keys=True, separators=(",", ":"))
    return (
        "# External Challenge Report\n\n"
        f"- Verdict: `{data.get('verdict', '')}`\n"
        f"- Claim ceiling: `{data.get('claim_ceiling', '')}`\n"
        f"- Handoff: `{data.get('handoff', '')}`\n\n"
        "## Subject\n\n"
        f"```json\n{subject}\n```\n\n"
        "## Findings\n\n"
        f"```json\n{findings}\n```\n\n"
        "## Evidence edges\n\n"
        f"```json\n{edges}\n```\n"
    )


def validate_intake(data: dict, bundle_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    root = (bundle_root or Path.cwd()).resolve()
    for field in ("project", "task", "candidate_version"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"intake.{field}: required non-empty string")
    for field in ("candidate_digest", "evidence_manifest_digest"):
        if not is_sha256(data.get(field)):
            errors.append(f"intake.{field}: required lowercase SHA-256")
    candidate_path, candidate_path_error = resolve_pointer(root, data.get("candidate_pointer"))
    if candidate_path_error:
        errors.append(f"intake.candidate_pointer: {candidate_path_error}")
    elif candidate_path is not None:
        try:
            actual = sha256_path(candidate_path)
        except (OSError, ValueError) as exc:
            errors.append(f"intake.candidate_pointer: unreadable bound subject ({exc})")
        else:
            if actual != data.get("candidate_digest"):
                errors.append("intake.candidate_digest: does not match frozen candidate bytes")

    version_path, version_path_error = resolve_pointer(
        root, data.get("candidate_version_pointer"), require_file=True
    )
    version_field = data.get("candidate_version_field")
    if version_path_error:
        errors.append(f"intake.candidate_version_pointer: {version_path_error}")
    elif not isinstance(version_field, str) or not version_field.strip():
        errors.append("intake.candidate_version_field: required top-level JSON field")
    elif version_path is not None:
        try:
            version_document = strict_json_loads(version_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKey):
            errors.append("intake.candidate_version_pointer: metadata must be unique-key JSON")
        else:
            if not isinstance(version_document, dict) or version_document.get(version_field) != data.get("candidate_version"):
                errors.append("intake.candidate_version: does not match bound metadata bytes")
    if candidate_path is not None and candidate_path.is_dir():
        plugin_metadata = candidate_path / ".codex-plugin" / "plugin.json"
        if plugin_metadata.is_file():
            try:
                plugin_document = strict_json_loads(plugin_metadata.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKey):
                errors.append("intake.candidate_version: embedded plugin metadata is invalid")
            else:
                if not isinstance(plugin_document, dict) or plugin_document.get("version") != data.get("candidate_version"):
                    errors.append("intake.candidate_version: does not match embedded plugin manifest")

    manifest_path, manifest_path_error = resolve_pointer(
        root, data.get("evidence_manifest_pointer"), require_file=True
    )
    manifest_data: dict | None = None
    if manifest_path_error:
        errors.append(f"intake.evidence_manifest_pointer: {manifest_path_error}")
    elif manifest_path is not None:
        if sha256_file(manifest_path) != data.get("evidence_manifest_digest"):
            errors.append("intake.evidence_manifest_digest: does not match manifest bytes")
        try:
            parsed_manifest = strict_json_loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKey):
            errors.append("intake.evidence_manifest_pointer: manifest must be unique-key canonical JSON")
        else:
            if isinstance(parsed_manifest, dict):
                manifest_data = parsed_manifest
            else:
                errors.append("intake.evidence_manifest_pointer: manifest top level must be object")

    distribution_pointer = data.get("distribution_pointer")
    distribution_digest = data.get("distribution_digest")
    if distribution_pointer is not None or distribution_digest is not None:
        if not is_sha256(distribution_digest):
            errors.append("intake.distribution_digest: required lowercase SHA-256 when distribution is bound")
        distribution_path, distribution_error = resolve_pointer(root, distribution_pointer, require_file=True)
        if distribution_error:
            errors.append(f"intake.distribution_pointer: {distribution_error}")
        elif distribution_path is not None:
            if sha256_file(distribution_path) != distribution_digest:
                errors.append("intake.distribution_digest: does not match distribution bytes")
            if candidate_path is not None:
                errors.extend(
                    compare_distribution_to_candidate(
                        candidate_path, distribution_path, data.get("distribution_prefix", "")
                    )
                )

    if not isinstance(data.get("requested_gates"), list) or not data["requested_gates"]:
        errors.append("intake.requested_gates: required non-empty list")
    required_acceptance_ids = data.get("required_acceptance_ids")
    if (
        not isinstance(required_acceptance_ids, list)
        or not required_acceptance_ids
        or any(not isinstance(value, str) or not value for value in required_acceptance_ids)
        or len(required_acceptance_ids) != len(set(required_acceptance_ids))
    ):
        errors.append("intake.required_acceptance_ids: required unique non-empty string list")
    evidence = data.get("evidence")
    evidence_by_id: dict[str, dict] = {}
    if not isinstance(evidence, list) or not evidence:
        errors.append("intake.evidence: required non-empty list")
    else:
        seen: set[str] = set()
        for index, row in enumerate(evidence):
            if not isinstance(row, dict):
                errors.append(f"intake.evidence[{index}]: required object")
                continue
            evidence_id = row.get("evidence_id")
            if not isinstance(evidence_id, str) or not evidence_id:
                errors.append(f"intake.evidence[{index}].evidence_id: required")
            elif evidence_id in seen:
                errors.append(f"intake.evidence[{index}].evidence_id: duplicate")
            else:
                seen.add(evidence_id)
                evidence_by_id[evidence_id] = row
            if row.get("class") not in {
                "NORMATIVE",
                "STATE",
                "RAW_EVIDENCE",
                "SUMMARY_CLAIM",
                "SUPPORT",
                "UNVERIFIED",
            }:
                errors.append(f"intake.evidence[{index}].class: unsupported")
            if row.get("kind") not in EDGE_KINDS:
                errors.append(f"intake.evidence[{index}].kind: unsupported")
            if not is_sha256(row.get("subject_digest")):
                errors.append(f"intake.evidence[{index}].subject_digest: required SHA-256")
            elif row.get("class") == "RAW_EVIDENCE" and row["subject_digest"] != data.get("candidate_digest"):
                errors.append(f"intake.evidence[{index}].subject_digest: raw evidence subject mismatch")
            if not is_sha256(row.get("artifact_digest")):
                errors.append(f"intake.evidence[{index}].artifact_digest: required SHA-256")
            artifact_path, artifact_error = resolve_pointer(root, row.get("pointer"), require_file=True)
            if artifact_error:
                errors.append(f"intake.evidence[{index}].pointer: {artifact_error}")
            elif artifact_path is not None and sha256_file(artifact_path) != row.get("artifact_digest"):
                errors.append(f"intake.evidence[{index}].artifact_digest: does not match pointed bytes")

    if manifest_data is not None:
        if manifest_data.get("candidate_digest") != data.get("candidate_digest"):
            errors.append("intake.evidence_manifest: candidate digest mismatch")
        if manifest_data.get("candidate_version") != data.get("candidate_version"):
            errors.append("intake.evidence_manifest: candidate version mismatch")
        if manifest_data.get("required_acceptance_ids") != data.get("required_acceptance_ids"):
            errors.append("intake.evidence_manifest: required acceptance IDs mismatch")
        manifest_rows = manifest_data.get("evidence")
        if not isinstance(manifest_rows, list):
            errors.append("intake.evidence_manifest: evidence list required")
        else:
            manifest_ids = [
                row.get("evidence_id")
                for row in manifest_rows
                if isinstance(row, dict) and isinstance(row.get("evidence_id"), str)
            ]
            if len(manifest_ids) != len(manifest_rows):
                errors.append("intake.evidence_manifest: every evidence row requires an evidence ID")
            if len(manifest_ids) != len(set(manifest_ids)):
                errors.append("intake.evidence_manifest: duplicate evidence ID")
            manifest_by_id = {
                row["evidence_id"]: row
                for row in manifest_rows
                if isinstance(row, dict) and isinstance(row.get("evidence_id"), str)
            }
            if set(manifest_by_id) != set(evidence_by_id):
                errors.append("intake.evidence_manifest: evidence ID set mismatch")
            if len(manifest_rows) != len(evidence):
                errors.append("intake.evidence_manifest: evidence row cardinality mismatch")
            for evidence_id, row in evidence_by_id.items():
                manifest_row = manifest_by_id.get(evidence_id)
                if manifest_row is not None:
                    for field in ("class", "kind", "subject_digest", "artifact_digest", "pointer"):
                        if manifest_row.get(field) != row.get(field):
                            errors.append(f"intake.evidence_manifest: {evidence_id}.{field} mismatch")
    return errors


def validate_report(data: dict, intake: dict | None = None, bundle_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    root = (bundle_root or Path.cwd()).resolve()
    if set(data) != REPORT_TOP_LEVEL_FIELDS:
        missing = sorted(REPORT_TOP_LEVEL_FIELDS - set(data))
        extra = sorted(set(data) - REPORT_TOP_LEVEL_FIELDS)
        if missing:
            errors.append("report.schema: missing top-level fields " + ", ".join(missing))
        if extra:
            errors.append("report.schema: unknown top-level fields " + ", ".join(extra))
    serialized_report = json.dumps(data, sort_keys=True)
    for token in sorted(FORBIDDEN_CLAIM_TOKENS):
        if token in serialized_report:
            errors.append(f"report.claim_ceiling: forbidden escalated token {token}")
    if intake is None:
        errors.append("report.intake: canonical intake is required")
    else:
        errors.extend(f"report.{error}" for error in validate_intake(intake, bundle_root))
    verdict = data.get("verdict")
    if verdict not in VERDICTS:
        errors.append("report.verdict: unsupported")
    subject = data.get("subject")
    if not isinstance(subject, dict):
        errors.append("report.subject: required object")
        subject = {}
    expected_subject_fields = {"candidate_version", "candidate_digest", "evidence_manifest_digest"}
    if intake and ("distribution_digest" in intake or "distribution_pointer" in intake):
        expected_subject_fields.add("distribution_digest")
    if set(subject) != expected_subject_fields:
        errors.append("report.subject: fields do not match bound subject schema")
    for field in ("candidate_version", "candidate_digest", "evidence_manifest_digest"):
        if field == "candidate_version":
            if not isinstance(subject.get(field), str) or not subject[field].strip():
                errors.append("report.subject.candidate_version: required non-empty string")
        elif not is_sha256(subject.get(field)):
            errors.append(f"report.subject.{field}: required lowercase SHA-256")
        if intake and subject.get(field) != intake.get(field):
            errors.append(f"report.subject.{field}: does not match intake")
    if intake and ("distribution_digest" in intake or "distribution_pointer" in intake):
        if subject.get("distribution_digest") != intake.get("distribution_digest"):
            errors.append("report.subject.distribution_digest: does not match intake")
    claim_ceiling = data.get("claim_ceiling")
    if claim_ceiling not in ALLOWED_CLAIM_CEILINGS:
        errors.append("report.claim_ceiling: unsupported or escalated")
    elif verdict in VERDICT_CLAIM_CEILING and claim_ceiling != VERDICT_CLAIM_CEILING[verdict]:
        errors.append("report.claim_ceiling: inconsistent with verdict")
    handoff = data.get("handoff")
    if handoff not in HANDOFFS:
        errors.append("report.handoff: unsupported")
    if verdict == "FAIL_CHALLENGE" and handoff != "RESUME_SMALLEST_REPAIR":
        errors.append("report.handoff: FAIL requires RESUME_SMALLEST_REPAIR")
    if verdict == "PARTIAL_CHALLENGE" and handoff not in {"CONTINUE", "META_ORACLE", "DOMAIN_OWNER", "HITL"}:
        errors.append("report.handoff: inconsistent with PARTIAL")
    if verdict == "TEMP_CLOSED_CHALLENGE" and handoff not in {"META_ORACLE", "DOMAIN_OWNER", "HITL", "TERMINAL"}:
        errors.append("report.handoff: inconsistent with TEMP_CLOSED")

    rendered_path, rendered_error = resolve_pointer(root, data.get("rendered_report_pointer"), require_file=True)
    rendered_text = ""
    if rendered_error:
        errors.append(f"report.rendered_report_pointer: {rendered_error}")
    elif rendered_path is not None:
        if not is_sha256(data.get("rendered_report_digest")):
            errors.append("report.rendered_report_digest: required lowercase SHA-256")
        elif sha256_file(rendered_path) != data.get("rendered_report_digest"):
            errors.append("report.rendered_report_digest: does not match rendered report bytes")
        try:
            rendered_text = rendered_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append("report.rendered_report_pointer: rendered report must be UTF-8")
    if rendered_text:
        if rendered_text != render_canonical_markdown(data):
            errors.append("report.rendered_report_pointer: content is not the exact canonical rendering")

    findings = data.get("findings", [])
    if not isinstance(findings, list):
        errors.append("report.findings: required list")
        findings = []
    finding_ids: set[str] = set()
    evidence_by_id: dict[str, dict] = {}
    required_acceptance_ids: set[str] = set()
    if intake:
        evidence_by_id = {
            row["evidence_id"]: row
            for row in intake.get("evidence", [])
            if isinstance(row, dict) and isinstance(row.get("evidence_id"), str)
        }
        required_acceptance_ids = set(intake.get("required_acceptance_ids", []))
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            errors.append(f"report.findings[{index}]: required object")
            continue
        if set(finding) != FINDING_ALLOWED_FIELDS:
            errors.append(f"report.findings[{index}]: fields do not match closed finding schema")
        if finding.get("classification") not in CLASSIFICATIONS:
            errors.append(f"report.findings[{index}].classification: unsupported")
        if finding.get("severity") not in SEVERITIES:
            errors.append(f"report.findings[{index}].severity: unsupported")
        for field in sorted(FINDING_REQUIRED_FIELDS):
            if not isinstance(finding.get(field), str) or not finding[field].strip():
                errors.append(f"report.findings[{index}].{field}: required")
        finding_id = finding.get("finding_id")
        if isinstance(finding_id, str):
            if finding_id in finding_ids:
                errors.append(f"report.findings[{index}].finding_id: duplicate")
            finding_ids.add(finding_id)
        if finding.get("status") not in FINDING_STATUSES:
            errors.append(f"report.findings[{index}].status: unsupported")
        if not isinstance(finding.get("blocking"), bool):
            errors.append(f"report.findings[{index}].blocking: required boolean")
        if finding.get("candidate_digest") != subject.get("candidate_digest"):
            errors.append(f"report.findings[{index}].candidate_digest: subject mismatch")
        acceptance_id = finding.get("acceptance_id")
        if acceptance_id != "NOT_APPLICABLE" and acceptance_id not in required_acceptance_ids:
            errors.append(f"report.findings[{index}].acceptance_id: unknown intake acceptance")
        if finding.get("blocking") is True and acceptance_id not in required_acceptance_ids:
            errors.append(f"report.findings[{index}].acceptance_id: blocking finding requires intake acceptance")
        evidence_id = finding.get("evidence_id")
        if evidence_id == "MISSING":
            if finding.get("classification") != "EVIDENCE_GAP":
                errors.append(f"report.findings[{index}].evidence_id: MISSING allowed only for EVIDENCE_GAP")
        elif evidence_id not in evidence_by_id:
            errors.append(f"report.findings[{index}].evidence_id: unknown intake evidence")
        source_locator = finding.get("source_locator")
        if isinstance(source_locator, str) and "#" in source_locator:
            authority_id, predicate_id = source_locator.split("#", 1)
            authority_row = evidence_by_id.get(authority_id)
            if authority_row is None or authority_row.get("class") != "NORMATIVE":
                errors.append(f"report.findings[{index}].source_locator: authority is not intake NORMATIVE evidence")
            if acceptance_id != "NOT_APPLICABLE" and predicate_id != acceptance_id:
                errors.append(f"report.findings[{index}].source_locator: predicate does not match acceptance")
        else:
            errors.append(f"report.findings[{index}].source_locator: expected AUTHORITY_EVIDENCE_ID#ACCEPTANCE_ID")
        if finding.get("severity") in {"CRITICAL", "HIGH"} and finding.get("blocking") is not True:
            errors.append(f"report.findings[{index}].blocking: required for CRITICAL/HIGH")
        if finding.get("classification") in {"NON_BLOCKING_OBSERVATION", "OUT_OF_SCOPE"} and finding.get("blocking") is True:
            errors.append(f"report.findings[{index}].blocking: non-blocking taxonomy cannot block")
        if finding.get("classification") in {"NON_BLOCKING_OBSERVATION", "OUT_OF_SCOPE"}:
            if finding.get("status") != "NON_BLOCKING":
                errors.append(f"report.findings[{index}].status: non-blocking taxonomy requires NON_BLOCKING")
        elif finding.get("status") == "NON_BLOCKING":
            errors.append(f"report.findings[{index}].status: NON_BLOCKING conflicts with classification")
        if finding.get("classification") == "CONFIRMED_DEFECT" and finding.get("blocking") is not True:
            errors.append(f"report.findings[{index}].blocking: CONFIRMED_DEFECT must block")
        if finding.get("classification") == "CONFIRMED_DEFECT" and finding.get("status") not in {"OPEN", "ROUTED"}:
            errors.append(f"report.findings[{index}].status: CONFIRMED_DEFECT requires OPEN or ROUTED")
        if finding.get("blocking") is True:
            for field in sorted(BLOCKING_FIELDS):
                if not isinstance(finding.get(field), str) or not finding[field].strip():
                    errors.append(f"report.findings[{index}].{field}: required for blocking finding")
        if finding.get("classification") == "CONFIRMED_DEFECT":
            row = evidence_by_id.get(finding.get("evidence_id"))
            if row is None or row.get("class") != "RAW_EVIDENCE" or row.get("subject_digest") != subject.get("candidate_digest"):
                errors.append(f"report.findings[{index}]: CONFIRMED_DEFECT requires subject-bound RAW_EVIDENCE")

    edges = data.get("evidence_edges", [])
    if not isinstance(edges, list):
        errors.append("report.evidence_edges: required list")
        edges = []
    covered_acceptance_ids: set[str] = set()
    seen_edges: set[tuple[object, object, object]] = set()
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"report.evidence_edges[{index}]: required object")
            continue
        allowed_edge_fields = TEST_EDGE_FIELDS if edge.get("kind") == "TEST" else EDGE_BASE_FIELDS
        if set(edge) != allowed_edge_fields:
            errors.append(f"report.evidence_edges[{index}]: fields do not match closed edge schema")
        edge_identity = (edge.get("acceptance_id"), edge.get("evidence_id"), edge.get("kind"))
        if edge_identity in seen_edges:
            errors.append(f"report.evidence_edges[{index}]: duplicate acceptance/evidence/kind edge")
        seen_edges.add(edge_identity)
        acceptance_id = edge.get("acceptance_id")
        if acceptance_id not in required_acceptance_ids:
            errors.append(f"report.evidence_edges[{index}].acceptance_id: unknown intake acceptance")
        evidence_id = edge.get("evidence_id")
        row = evidence_by_id.get(evidence_id)
        if row is None:
            errors.append(f"report.evidence_edges[{index}].evidence_id: unknown intake evidence")
        if type(edge.get("required")) is not bool:
            errors.append(f"report.evidence_edges[{index}].required: required boolean")
        if not is_sha256(edge.get("artifact_digest")):
            errors.append(f"report.evidence_edges[{index}].artifact_digest: required SHA-256")
        if row is not None:
            if edge.get("required") is True and row.get("class") != "RAW_EVIDENCE":
                errors.append(f"report.evidence_edges[{index}]: required intake evidence is not RAW_EVIDENCE")
            if row.get("subject_digest") != subject.get("candidate_digest"):
                errors.append(f"report.evidence_edges[{index}]: intake evidence subject mismatch")
            if edge.get("artifact_digest") != row.get("artifact_digest"):
                errors.append(f"report.evidence_edges[{index}].artifact_digest: does not match intake")
            if edge.get("pointer") != row.get("pointer"):
                errors.append(f"report.evidence_edges[{index}].pointer: does not match intake")
        if edge.get("status") not in EDGE_STATUSES:
            errors.append(f"report.evidence_edges[{index}].status: unsupported")
        if type(edge.get("raw")) is not bool:
            errors.append(f"report.evidence_edges[{index}].raw: required boolean")
        if not isinstance(edge.get("pointer"), str) or not edge["pointer"].strip():
            errors.append(f"report.evidence_edges[{index}].pointer: required")
        if edge.get("kind") not in EDGE_KINDS:
            errors.append(f"report.evidence_edges[{index}].kind: unsupported")
        if row is not None and edge.get("kind") != row.get("kind"):
            errors.append(f"report.evidence_edges[{index}].kind: does not match intake")
        if edge.get("kind") == "TEST" and edge.get("required") is True:
            counts = [edge.get(name) for name in ("passed", "failed", "errors")]
            if not isinstance(edge.get("command"), str) or not edge["command"].strip():
                errors.append(f"report.evidence_edges[{index}].command: non-empty string required")
            if not isinstance(edge.get("environment"), str) or not edge["environment"].strip():
                errors.append(f"report.evidence_edges[{index}].environment: non-empty string required")
            if type(edge.get("denominator")) is not int or edge["denominator"] <= 0:
                errors.append(f"report.evidence_edges[{index}].denominator: positive integer required")
            if any(type(value) is not int or value < 0 for value in counts):
                errors.append(f"report.evidence_edges[{index}]: TEST requires nonnegative passed/failed/errors")
            elif type(edge.get("denominator")) is int and sum(counts) != edge["denominator"]:
                errors.append(f"report.evidence_edges[{index}]: TEST counts do not equal denominator")
            if type(edge.get("exit_status")) is not int:
                errors.append(f"report.evidence_edges[{index}].exit_status: integer required")
            if edge.get("status") == "SUPPORTED" and (
                edge.get("passed") != edge.get("denominator")
                or edge.get("failed") != 0
                or edge.get("errors") != 0
                or edge.get("exit_status") != 0
            ):
                errors.append(f"report.evidence_edges[{index}]: SUPPORTED TEST is not objectively green")
            if edge.get("status") == "CONTRADICTED" and not (
                type(edge.get("failed")) is int
                and type(edge.get("errors")) is int
                and type(edge.get("exit_status")) is int
                and (edge["failed"] > 0 or edge["errors"] > 0 or edge["exit_status"] != 0)
            ):
                errors.append(f"report.evidence_edges[{index}]: CONTRADICTED TEST has no objective failure")
        if verdict == "PASS_CHALLENGE" and edge.get("required") is True:
            if isinstance(acceptance_id, str):
                covered_acceptance_ids.add(acceptance_id)
            if edge.get("status") != "SUPPORTED":
                errors.append(f"report.evidence_edges[{index}]: required edge not supported")
            if edge.get("raw") is not True:
                errors.append(f"report.evidence_edges[{index}]: required edge is not raw evidence")
    if verdict == "PASS_CHALLENGE":
        if not edges:
            errors.append("report.evidence_edges: PASS requires evidence edges")
        if any(f.get("blocking") is True for f in findings if isinstance(f, dict)):
            errors.append("report.verdict: PASS cannot contain blocking finding")
        if any(
            f.get("classification") not in {"NON_BLOCKING_OBSERVATION", "OUT_OF_SCOPE"}
            for f in findings
            if isinstance(f, dict)
        ):
            errors.append("report.verdict: PASS contains contradictory finding taxonomy")
        missing_acceptance = sorted(required_acceptance_ids - covered_acceptance_ids)
        if missing_acceptance:
            errors.append("report.evidence_edges: missing required acceptance coverage " + ", ".join(missing_acceptance))
    blocking_findings = [row for row in findings if isinstance(row, dict) and row.get("blocking") is True]
    if verdict == "FAIL_CHALLENGE" and not any(
        row.get("classification") == "CONFIRMED_DEFECT" for row in blocking_findings
    ):
        errors.append("report.verdict: FAIL requires a blocking CONFIRMED_DEFECT")
    if verdict == "PARTIAL_CHALLENGE" and blocking_findings:
        errors.append("report.verdict: PARTIAL cannot contain blocking finding")
    if verdict == "FAIL_CHALLENGE":
        for index, finding in enumerate(findings):
            if isinstance(finding, dict) and finding.get("classification") == "CONFIRMED_DEFECT" and finding.get("blocking") is True:
                if not any(
                    isinstance(edge, dict)
                    and edge.get("acceptance_id") == finding.get("acceptance_id")
                    and edge.get("evidence_id") == finding.get("evidence_id")
                    and edge.get("status") == "CONTRADICTED"
                    and edge.get("raw") is True
                    for edge in edges
                ):
                    errors.append(f"report.findings[{index}]: blocking defect requires contradicted raw evidence edge")
    unresolved_edges = [
        edge for edge in edges if isinstance(edge, dict) and edge.get("status") in {"CONTRADICTED", "MISSING", "UNVERIFIED"}
    ]
    unresolved_findings = [
        finding
        for finding in findings
        if isinstance(finding, dict) and finding.get("classification") in {"EVIDENCE_GAP", "ORACLE_DISAGREEMENT", "CONFIRMED_DEFECT"}
    ]
    if verdict == "PARTIAL_CHALLENGE" and not unresolved_edges and not unresolved_findings:
        errors.append("report.verdict: PARTIAL requires an unresolved or contradicted edge/finding")
    if verdict == "TEMP_CLOSED_CHALLENGE" and not any(
        isinstance(finding, dict)
        and finding.get("classification") in {"EVIDENCE_GAP", "ORACLE_DISAGREEMENT"}
        and finding.get("status") == "TEMP_CLOSED"
        for finding in findings
    ):
        errors.append("report.verdict: TEMP_CLOSED requires a TEMP_CLOSED evidence/disagreement finding")
    return errors


def load_json_document(path: Path) -> tuple[dict | None, list[str]]:
    try:
        data = strict_json_loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKey) as exc:
        return None, [f"{path.name}: expected canonical JSON sidecar ({type(exc).__name__})"]
    if not isinstance(data, dict):
        return None, [f"{path.name}: top level must be an object"]
    return data, []


def validate_trigger_cases(root: Path, description: str) -> list[str]:
    errors: list[str] = []
    eval_path = root / "evals" / "trigger_cases.jsonl"
    agent_path = root / "agents" / "openai.yaml"
    try:
        rows = [strict_json_loads(line) for line in eval_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKey) as exc:
        return [f"trigger evals: parse failure {type(exc).__name__}"]
    ids = [row.get("id") for row in rows if isinstance(row, dict)]
    if len(rows) < 10 or len(ids) != len(set(ids)):
        errors.append("trigger evals: require at least 10 unique cases")
    if not any(row.get("should_trigger") is True for row in rows) or not any(
        row.get("should_trigger") is False for row in rows
    ):
        errors.append("trigger evals: require positive and negative controls")
    if set(ids) != set(TRIGGER_EXPECTATIONS):
        errors.append("trigger evals: required immutable fixture ID set mismatch")
    if "Use" not in description or "Do not use" not in description:
        errors.append("SKILL.md description: must state positive and negative trigger scope")
    agent = agent_path.read_text(encoding="utf-8") if agent_path.is_file() else ""
    implicit_enabled = "allow_implicit_invocation: true" in agent
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("prompt"), str) or not isinstance(row.get("should_trigger"), bool):
            errors.append("trigger evals: malformed row")
            continue
        expected = TRIGGER_EXPECTATIONS.get(row.get("id"))
        if expected is not None and (row.get("class"), row.get("should_trigger")) != expected:
            errors.append(f"trigger evals: {row.get('id')} class/label drift")
        prompt_digest = hashlib.sha256(row["prompt"].encode("utf-8")).hexdigest()
        if row.get("id") in TRIGGER_PROMPT_SHA256 and prompt_digest != TRIGGER_PROMPT_SHA256[row["id"]]:
            errors.append(f"trigger evals: {row.get('id')} prompt semantic fixture drift")
        explicitly_named = "challenge-review" in row["prompt"] or "Fabric External Independent Challenge Reviewer" in row["prompt"]
        if row["should_trigger"] and not explicitly_named and not implicit_enabled:
            errors.append(f"trigger evals: {row.get('id')} expects implicit trigger while policy disables it")
    return errors


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return {}, ["SKILL.md: missing or unclosed frontmatter"]
    raw, body = text[4:].split("\n---\n", 1)
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            errors.append("SKILL.md: malformed frontmatter line")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    if set(fields) != {"name", "description"}:
        errors.append("SKILL.md: frontmatter must contain only name and description")
    if not body.strip():
        errors.append("SKILL.md: body is empty")
    return fields, errors


def validate_skill_root(root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        return ["SKILL.md: missing"]
    text = skill_md.read_text(encoding="utf-8")
    fields, frontmatter_errors = parse_frontmatter(text)
    errors.extend(frontmatter_errors)
    if fields.get("name") != "challenge-review":
        errors.append("SKILL.md: technical name must be challenge-review")
    if len(fields.get("description", "")) > 1024:
        errors.append("SKILL.md: description exceeds 1024 characters")
    errors.extend(validate_trigger_cases(root, fields.get("description", "")))
    negative_clause = re.compile(r"^(?:[-*]\s*)?(?:do not|never|must not|cannot|refuse to|without)\b")
    authority_patterns = (
        r"\bact as (?:a |the )?maker\b",
        r"\b(?:patch|modify|rewrite) (?:the |this )?(?:candidate|repair|code|release)\b",
        r"\b(?:commit|merge|deploy) (?:the |this )?(?:candidate|repair|change|changes|code|release)\b",
        r"\bapprove (?:the |this )?(?:candidate|release|production|domain)\b",
        r"\b(?:change|edit|modify|rewrite) (?:the )?(?:acceptance|evaluator|oracle)\b",
    )
    for line_number, line in enumerate(text.splitlines(), 1):
        clauses = [part.strip().lower() for part in re.split(r"[;,]|(?<=[.!?])\s+", line) if part.strip()]
        for clause in clauses:
            if not any(re.search(pattern, clause) for pattern in authority_patterns):
                continue
            if negative_clause.search(clause) or "read-only" in clause:
                continue
            errors.append(f"SKILL.md:{line_number}: affirmative maker/repair/release authority")
            break
    references = root / "references"
    present = {p.name for p in references.glob("*.md")} if references.is_dir() else set()
    missing = sorted(REQUIRED_REFERENCES - present)
    if missing:
        errors.append("references: missing " + ", ".join(missing))
    for name in REQUIRED_REFERENCES:
        if f"references/{name}" not in text:
            errors.append(f"SKILL.md: does not route to references/{name}")
    required_paths = [
        root / "assets" / "EXTERNAL_CHALLENGE_REPORT.template.md",
        root / "agents" / "openai.yaml",
        root / "evals" / "trigger_cases.jsonl",
        root / "scripts" / "verify_review_bundle.py",
    ]
    for path in required_paths:
        if not path.is_file():
            errors.append(f"missing path: {path.relative_to(root)}")
    agent_path = root / "agents" / "openai.yaml"
    if agent_path.is_file():
        agent = agent_path.read_text(encoding="utf-8")
        for token in (
            "interface:",
            "display_name:",
            "short_description:",
            "default_prompt:",
            "$challenge-review",
            "policy:",
            "allow_implicit_invocation: true",
        ):
            if token not in agent:
                errors.append(f"agents/openai.yaml: missing {token}")
    if len(text.splitlines()) >= 500:
        errors.append("SKILL.md: must remain under 500 lines")
    return errors


def self_test() -> dict:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        candidate = root / "candidate.bin"
        candidate_metadata = root / "candidate-metadata.json"
        raw_log = root / "raw.log"
        authority = root / "authority.md"
        manifest_path = root / "evidence-manifest.json"
        rendered_path = root / "EXTERNAL_CHALLENGE_REPORT.md"
        candidate.write_bytes(b"frozen-candidate")
        candidate_metadata.write_text('{"version":"1"}\n', encoding="utf-8")
        raw_log.write_text("1 test passed\n", encoding="utf-8")
        authority.write_text("# A-1\nFrozen acceptance.\n", encoding="utf-8")
        digest = sha256_file(candidate)
        artifact_digest = sha256_file(raw_log)
        authority_digest = sha256_file(authority)
        manifest_data = {
            "candidate_version": "1",
            "candidate_digest": digest,
            "required_acceptance_ids": ["A-1"],
            "evidence": [
                {
                    "evidence_id": "EV-1",
                    "class": "RAW_EVIDENCE",
                    "kind": "TEST",
                    "subject_digest": digest,
                    "artifact_digest": artifact_digest,
                    "pointer": "raw.log",
                },
                {
                    "evidence_id": "AUTH-1",
                    "class": "NORMATIVE",
                    "kind": "NORMATIVE",
                    "subject_digest": digest,
                    "artifact_digest": authority_digest,
                    "pointer": "authority.md",
                }
            ],
        }
        manifest_path.write_text(json.dumps(manifest_data, sort_keys=True) + "\n", encoding="utf-8")
        manifest_digest = sha256_file(manifest_path)
        intake = {
            "project": "fixture",
            "task": "R1",
            "candidate_version": "1",
            "candidate_pointer": "candidate.bin",
            "candidate_version_pointer": "candidate-metadata.json",
            "candidate_version_field": "version",
            "candidate_digest": digest,
            "evidence_manifest_pointer": "evidence-manifest.json",
            "evidence_manifest_digest": manifest_digest,
            "requested_gates": ["R1"],
            "required_acceptance_ids": ["A-1"],
            "evidence": manifest_data["evidence"],
        }
        report = {
            "verdict": "PASS_CHALLENGE",
            "subject": {
                "candidate_version": "1",
                "candidate_digest": digest,
                "evidence_manifest_digest": manifest_digest,
            },
            "findings": [],
            "claim_ceiling": "SKILL_CANDIDATE_QUALIFIED",
            "handoff": "CONTINUE",
            "rendered_report_pointer": "EXTERNAL_CHALLENGE_REPORT.md",
            "rendered_report_digest": "",
            "evidence_edges": [
                {
                    "evidence_id": "EV-1",
                    "acceptance_id": "A-1",
                    "artifact_digest": artifact_digest,
                    "kind": "TEST",
                    "required": True,
                    "status": "SUPPORTED",
                    "raw": True,
                    "pointer": "raw.log",
                    "command": "python fixture.py",
                    "environment": "self-test",
                    "denominator": 1,
                    "passed": 1,
                    "failed": 0,
                    "errors": 0,
                    "exit_status": 0,
                }
            ],
        }
        rendered_path.write_text(render_canonical_markdown(report), encoding="utf-8")
        report["rendered_report_digest"] = sha256_file(rendered_path)
        errors.extend(validate_intake(intake, root))
        errors.extend(validate_report(report, intake, root))
        negative = json.loads(json.dumps(report))
        negative["evidence_edges"][0]["pointer"] = ""
        if not validate_report(negative, intake, root):
            errors.append("self-test: missing raw log pointer was not rejected")
        mismatch = json.loads(json.dumps(report))
        mismatch["subject"]["candidate_digest"] = "c" * 64
        if not validate_report(mismatch, intake, root):
            errors.append("self-test: subject mismatch was not rejected")
        forged = json.loads(json.dumps(intake))
        forged["candidate_digest"] = "c" * 64
        if not validate_intake(forged, root):
            errors.append("self-test: forged candidate digest was not rejected")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--intake", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--bundle-root", type=Path)
    args = parser.parse_args()
    output: dict[str, object] = {}
    errors: list[str] = []
    intake: dict | None = None
    bundle_root = args.bundle_root.resolve() if args.bundle_root else (args.intake.parent.resolve() if args.intake else Path.cwd())
    if args.self_test:
        output["self_test"] = self_test()
        errors.extend(output["self_test"]["errors"])
    if args.intake:
        intake, parse_errors = load_json_document(args.intake)
        output["intake_errors"] = parse_errors + (validate_intake(intake, bundle_root) if intake is not None else [])
        errors.extend(output["intake_errors"])
    if args.report:
        report, parse_errors = load_json_document(args.report)
        output["report_errors"] = parse_errors + (
            validate_report(report, intake, bundle_root) if report is not None else []
        )
        errors.extend(output["report_errors"])
    if args.skill_root:
        output["skill_errors"] = validate_skill_root(args.skill_root)
        output["skill_sha256"] = sha256_file(args.skill_root / "SKILL.md") if (args.skill_root / "SKILL.md").is_file() else None
        errors.extend(output["skill_errors"])
    output["status"] = "PASS" if not errors else "FAIL"
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
