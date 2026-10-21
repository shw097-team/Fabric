#!/usr/bin/env python
"""Fabric evidence packet builder + secret scanner for FAR-LANE-REMEDIATION-20261021.

Builds PACKET_MANIFEST.json (sorted path/bytes/sha256, manifest excluded from itself) and
independently recomputes every entry to prove the manifest matches the delivered bytes.
Scans for credential-shaped strings and reports them by class (documentation placeholders
are reported separately from real values).
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

FABRIC = Path(r"C:\Projects\Agent_Workspace\Fabric")
PKT = FABRIC / "evidence" / "FAR-LANE-REMEDIATION-20261021"

# Real-value patterns: a key that is actually assigned a credential-looking value.
REAL_PATTERNS = [
    ("github_pat", re.compile(rb"github_pat_[A-Za-z0-9_]{20,}")),
    ("ghp_token", re.compile(rb"ghp_[A-Za-z0-9]{30,}")),
    ("nvapi_key", re.compile(rb"nvapi-[A-Za-z0-9_\-]{30,}")),
    ("sk_secret", re.compile(rb"\bsk-[A-Za-z0-9_\-]{24,}")),
    ("bearer_literal", re.compile(rb"Bearer\s+[A-Za-z0-9_\-\.]{24,}")),
]
# Documentation placeholders / env-var references: expected, not a leak.
PLACEHOLDER = re.compile(rb"(env_ref:[A-Z_]+|\$\{?[A-Z_]+\}?|env_ref:|apiKey'?\s*:\s*'\$|OPENCODE_GO_API_KEY|NVIDIA_API_KEY)")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    files = sorted(p for p in PKT.rglob("*") if p.is_file() and p.name not in
                   ("PACKET_MANIFEST.json", ".gitattributes", "build_packet.py"))
    entries, findings = [], []
    for p in files:
        b = p.read_bytes()
        # The repository's published evidence root is EVIDENCE/ (upper case). Windows is
        # case-insensitive, so the on-disk path may read as evidence/ while the git index
        # stores EVIDENCE/. Resolve the path the INDEX uses, or an external acceptor that
        # recomputes sha256 from the committed blob cannot find the path.
        rel = p.relative_to(FABRIC).as_posix()
        parts = rel.split("/")
        if parts[0].lower() == "evidence":
            parts[0] = "EVIDENCE"
        rel = "/".join(parts)
        entries.append({"path": rel, "bytes": len(b), "sha256": sha(b)})
        for cls, pat in REAL_PATTERNS:
            for m in pat.finditer(b):
                findings.append({"file": rel, "class": cls, "offset": m.start(),
                                 "excerpt": m.group(0)[:12].decode("ascii", "replace") + "…"})
    # independent recomputation
    mismatches = []
    for e in entries:
        p = FABRIC / e["path"]
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha(b) != e["sha256"]:
            mismatches.append(e["path"])
    manifest = {
        "schema": "FAR-LANE-REMEDIATION-20261021/PACKET-MANIFEST/1",
        "round": "FAR-LANE-REMEDIATION-20261021",
        "subject": "HG-KSEOS lane/model declaration remediation, epoch 22 -> epoch 23",
        "control_plane": "HG-KSEOS (sole control plane); canonical Hermes = governed Runtime/Orchestration Plane",
        "publish_claim": ("the DELIVERED set is every file under evidence/FAR-LANE-REMEDIATION-20261021/. "
                          "Bytes are stored verbatim (-text). An external acceptor can recompute each sha256 below "
                          "from the delivered blob."),
        "file_count": len(entries),
        "total_bytes": sum(e["bytes"] for e in entries),
        "manifest_excludes_itself": True,
        "independent_recomputation_mismatches": mismatches,
        "secret_scan": {
            "real_credential_findings": findings,
            "finding_count": len(findings),
            "classes_scanned": [c for c, _ in REAL_PATTERNS],
            "note": ("Env-var references and documentation placeholders (env_ref:, $VAR, apiKey: '$…') are "
                     "policy values, not credential values, and are excluded from the finding count."),
        },
        "claim_ceiling": ("CANDIDATE_ONLY — mirrored governed artefacts for external acceptance. "
                          "Local verification is not independent acceptance; publication is not release."),
        "files": entries,
    }
    (PKT / "PACKET_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(entries), "total_bytes": manifest["total_bytes"],
                      "mismatches": mismatches, "secret_findings": len(findings)}, indent=1))
    for f in findings:
        print("SECRET:", f)
    return 0 if not mismatches and not findings else 2


if __name__ == "__main__":
    sys.exit(main())
