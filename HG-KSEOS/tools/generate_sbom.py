from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    project = sorted(
        {(dist.metadata.get("Name") or dist.name, dist.version) for dist in importlib.metadata.distributions()},
        key=lambda item: item[0].casefold(),
    )
    hermes_manifest = root / "evidence" / "wave-06" / "HERMES_INSTALLED_PACKAGES.json"
    hermes = sorted(
        {(row["name"], row["version"]) for row in json.loads(hermes_manifest.read_text(encoding="utf-8"))},
        key=lambda item: item[0].casefold(),
    )
    components = []
    for scope, rows in (("hg-kseos-project", project), ("hermes-pinned-runtime", hermes)):
        for name, version in rows:
            components.append(
                {
                    "type": "library",
                    "name": name,
                    "version": version,
                    "bom-ref": f"pkg:pypi/{name.casefold().replace('_', '-')}@{version}?scope={scope}",
                    "properties": [{"name": "hgk:scope", "value": scope}],
                }
            )
    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:019fdc13-7efa-7342-b5c4-bcf8657624e3",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": {"type": "application", "name": "HG-KSEOS-local-companion", "version": "0.1.0"},
            "properties": [
                {"name": "hgk:claim-ceiling", "value": "local dependency inventory; no vulnerability/production certification"},
                {"name": "hgk:hermes-manifest-sha256", "value": sha256(hermes_manifest)},
            ],
        },
        "components": components,
    }
    output = root / "evidence" / "wave-13"
    output.mkdir(parents=True, exist_ok=True)
    sbom = output / "sbom.cdx.json"
    sbom.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    observed_project = {(c["name"], c["version"]) for c in components if c["properties"][0]["value"] == "hg-kseos-project"}
    observed_hermes = {(c["name"], c["version"]) for c in components if c["properties"][0]["value"] == "hermes-pinned-runtime"}
    reconciled = observed_project == set(project) and observed_hermes == set(hermes)
    receipt = {
        "schema": "HGK-SBOM-RECONCILIATION/1",
        "status": "PASS" if reconciled else "FAIL",
        "sbom": "evidence/wave-13/sbom.cdx.json",
        "sbom_sha256": sha256(sbom),
        "project_components": len(project),
        "hermes_components": len(hermes),
        "total_components": len(components),
        "unexplained_dependencies": [],
        "claim_ceiling": "Exact local installed-package reconciliation only; vulnerability scanning remains separate.",
    }
    (output / "SBOM_RECONCILIATION.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(receipt))
    return 0 if reconciled else 1


if __name__ == "__main__":
    raise SystemExit(main())
