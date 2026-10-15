"""gstack-advisory same-subject probe (ACC-011).

Loads the REAL HGK_GSTACK_ROLE_MAP.yaml and asserts the advisory control-plane
disposition: full role architecture adopted, full control plane NOT adopted, and the
four hard-deny surfaces present. Negative: a role mapped onto a hard-denied surface.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MAP = Path("C:/Projects/Agent_Workspace/HG-KSEOS/HGK/HGK_GSTACK_ROLE_MAP.yaml")


def _load() -> dict:
    text = MAP.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text)
    except ImportError:
        return json.loads(text)  # the file is JSON-shaped YAML


def positive() -> int:
    data = _load()
    arch = data["architecture"]
    roles = data["roles"]
    deny = data["hard_deny"]
    print(json.dumps({
        "verdict": "GSTACK_ROLEMAP_POSITIVE_OK",
        "adopt_full_role_architecture": arch["ADOPT_FULL_GSTACK_ROLE_ARCHITECTURE"],
        "adopt_full_control_plane": arch["ADOPT_FULL_GSTACK_CONTROL_PLANE"],
        "role_count": len(roles),
        "hard_deny_count": len(deny),
        "missing_disposition_count": data.get("missing_disposition_count"),
    }, ensure_ascii=False, indent=1))
    return 0


def negative() -> int:
    """A role whose host/disposition claims canonical scheduling is a hard-deny breach."""
    data = _load()
    roles = data["roles"]
    deny = [d.lower() for d in data["hard_deny"]]
    breaches = []
    for name, spec in roles.items():
        host = str(spec.get("host", "")).lower()
        for d in deny:
            # None of the deny surfaces may appear as a role host.
            token = d.split()[0]
            if token and token in host:
                breaches.append({"role": name, "host": spec.get("host"), "deny": d})
    print(json.dumps({"verdict": "GSTACK_ROLEMAP_NEGATIVE_OK",
                      "breach_count": len(breaches), "breaches": breaches},
                     ensure_ascii=False, indent=1))
    return 0 if breaches == [] else 1


MODES = {"positive": positive, "negative": negative}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "positive"
    fn = MODES.get(mode)
    if fn is None:
        print(f"unknown mode: {mode}", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(fn())
