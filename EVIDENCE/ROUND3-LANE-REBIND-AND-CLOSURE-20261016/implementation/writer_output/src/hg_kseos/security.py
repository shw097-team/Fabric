from __future__ import annotations

import os
import re
from pathlib import Path

from .errors import AdmissionDenied


WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
INJECTION_PATTERNS = (
    re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions", re.I),
    re.compile(r"system\s+message\s*:", re.I),
    re.compile(r"developer\s+message\s*:", re.I),
    re.compile(r"(?:exfiltrate|reveal|print)\s+(?:the\s+)?(?:secret|token|api\s*key)", re.I),
    re.compile(r"disable\s+(?:the\s+)?(?:sandbox|security|validation)", re.I),
)
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(?:api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{16,}"),
)
PII_PATTERNS = (
    re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    re.compile(r"(?<!\d)(?:\+?886[- ]?)?0?9\d{2}[- ]?\d{3}[- ]?\d{3}(?!\d)"),
)


def ensure_within(path: Path, allowed_root: Path, *, must_exist: bool = False) -> Path:
    root = allowed_root.resolve(strict=True)
    candidate = path.resolve(strict=must_exist)
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise AdmissionDenied(f"ERR_PATH_OUTSIDE_SCOPE: {candidate}") from exc
    for part in candidate.relative_to(root).parts:
        stem = part.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED or part.endswith((" ", ".")):
            raise AdmissionDenied(f"ERR_WINDOWS_RESERVED_PATH: {part}")
    current = root
    for part in candidate.relative_to(root).parts:
        current = current / part
        if current.exists() and (current.is_symlink() or _is_reparse_point(current)):
            raise AdmissionDenied(f"ERR_REPARSE_POINT: {current}")
    return candidate


def _is_reparse_point(path: Path) -> bool:
    stat = path.lstat()
    return bool(getattr(stat, "st_file_attributes", 0) & 0x400)


def sanitation_findings(text: str) -> list[str]:
    findings = [f"PROMPT_INJECTION:{pattern.pattern}" for pattern in INJECTION_PATTERNS if pattern.search(text)]
    findings.extend(f"SECRET_PATTERN:{pattern.pattern}" for pattern in SECRET_PATTERNS if pattern.search(text))
    return findings


def redact_secrets(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


def contains_pii(text: str) -> bool:
    return any(pattern.search(text) for pattern in PII_PATTERNS)


def verify_artifact_pin(actual_sha256: str, expected_sha256: str) -> None:
    if not re.fullmatch(r"[0-9a-fA-F]{64}", actual_sha256) or actual_sha256.casefold() != expected_sha256.casefold():
        raise AdmissionDenied("ERR_SUPPLY_CHAIN_PIN_MISMATCH")


def network_is_disabled() -> bool:
    return os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED") == "1"
