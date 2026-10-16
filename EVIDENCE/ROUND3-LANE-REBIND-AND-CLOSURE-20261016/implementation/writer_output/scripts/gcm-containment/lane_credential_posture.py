#!/usr/bin/env python3
"""L3 lane gate: the GCM credential-posture control, consumed by the lane
launcher (``scripts/lane_launcher.sh``).

Round ``HGK-GCM-APPLY-20261013`` (X2). This is the one thing that *consumes* the
posture preflight: ``credential_preflight.py`` can only be a control if something
acts on its verdict, and this module is that something.

It reuses the CANONICAL classifier in ``credential_preflight.py`` (``read_effective``
 + ``classify``) -- there is no second, weaker inline check -- and applies the
launcher's ASYMMETRIC policy:

  PASS          the effective resolution provably does not reach a prompt-capable
                helper. -> ``CONTINUE`` (silent), exit 0.
  FAIL          a POSITIVE violation: the effective resolution still reaches a
                prompt-capable interactive helper. -> ``BLOCK``, exit 89, with a
                typed message naming the offending helper and its origin file.
  INCONCLUSIVE  the detector could not reach a verdict (git missing, config
                unreadable/unparsable). -> ``WARN_CONTINUE``: a typed warning on
                stderr, exit 0. Deliberately NOT fail-closed on the detector (see
                the trade-off in the launcher header): a detector bug must not
                become a lane outage.

Side-effect free: reads only the EFFECTIVE resolution through git; never a
candidate file's bytes, never a credential value, no network, no writes.

Deterministic test seam (model-free, no live host): ``--test-global`` points git's
global scope at a scratch file and ``--git`` overrides the git executable, so every
posture case can be driven without provoking a real credential request.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

PASS = "PASS"
FAIL = "FAIL"
INCONCLUSIVE = "INCONCLUSIVE"

CONTINUE = "CONTINUE"
WARN_CONTINUE = "WARN_CONTINUE"
BLOCK = "BLOCK"

#: Free code chosen for the new refusal. Reserved in lane_launcher.sh today:
#: 64 usage, 90 toolchain, 91 toolchain-mismatch, 92 model refused/declaration,
#: 93 inconclusive, 94 log containment, 95 scratch containment, 98 identity
#: mismatch, 99 cleanup, 130/143 traps; the preflight owns 95/96/97. 89 is the
#: nearest unused neighbour below the 90-band and collides with nothing.
EXIT_BLOCK = 89

ERR_PROMPTABLE = "ERR_LANE_CREDENTIAL_POSTURE_PROMPTABLE"
WARN_INCONCLUSIVE = "WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE"

#: The second prompt surface the launcher must close on the lane environment.
REQUIRED_ENV = {"GIT_TERMINAL_PROMPT": "0"}


def _load_preflight():
    """Import the canonical ``credential_preflight.py`` that sits beside us."""
    here = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "hgk_gcm_credential_preflight", here / "credential_preflight.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(git: str | None = None, test_global: str | None = None) -> dict:
    """Decide the launcher policy. Never raises: any detector fault -> INCONCLUSIVE."""
    doc: dict = {
        "schema": "HGK-GCM-LANE-POSTURE-GATE/1",
        "round": "HGK-GCM-APPLY-20261013",
        "verdict": INCONCLUSIVE,
        "decision": WARN_CONTINUE,
        "typed_code": WARN_INCONCLUSIVE,
        "helper": None,
        "origin": None,
        "reason": "detector did not run",
        "required_lane_env": dict(REQUIRED_ENV),
    }
    try:
        module = _load_preflight()
        if git is None:
            import shutil

            git = shutil.which("git")
        doc["git"] = git
        if git is None:
            doc["reason"] = "git executable not found on PATH"
            return doc
        overrides = {}
        if test_global:
            overrides["GIT_CONFIG_GLOBAL"] = str(test_global).replace("\\", "/")
        eff = module.read_effective(git, overrides or None)
        if not eff.get("ok"):
            doc["reason"] = eff.get("reason", "git config could not be read")
            doc["stderr"] = eff.get("stderr")
            return doc
        doc["entries"] = eff.get("entries", [])
        doc["raw"] = eff.get("raw")
        decision = module.classify(eff.get("entries", []))
    except BaseException as exc:  # noqa: BLE001 - a detector fault is INCONCLUSIVE
        doc["reason"] = f"detector fault ({type(exc).__name__}): {exc}"
        return doc

    verdict = decision.get("verdict")
    doc["verdict"] = verdict
    doc["reason"] = decision.get("reason")
    if verdict == PASS:
        doc["decision"] = CONTINUE
        doc["typed_code"] = None
    elif verdict == FAIL:
        doc["decision"] = BLOCK
        doc["typed_code"] = ERR_PROMPTABLE
        doc["helper"] = decision.get("prompt_capable_helper")
        doc["origin"] = decision.get("origin")
    else:  # INCONCLUSIVE or any unexpected value stays INCONCLUSIVE
        doc["verdict"] = INCONCLUSIVE
        doc["decision"] = WARN_CONTINUE
        doc["typed_code"] = WARN_INCONCLUSIVE
    return doc


def render_decision(doc: dict) -> int:
    """Emit the operator-facing message and return the process exit code."""
    decision = doc.get("decision")
    if decision == CONTINUE:
        return 0
    if decision == BLOCK:
        helper = doc.get("helper") or "<unknown>"
        origin = doc.get("origin") or "<unknown origin>"
        print(
            f"{ERR_PROMPTABLE}: the effective credential resolution still reaches "
            f"a prompt-capable interactive helper '{helper}' from origin "
            f"'{origin}'; lane NOT run (0 attempts); credential posture gate "
            f"BLOCKED (fail-closed on the danger).",
            file=sys.stderr,
        )
        return EXIT_BLOCK
    print(
        f"{WARN_INCONCLUSIVE}: the credential-posture detector could not reach a "
        f"verdict ({doc.get('reason')}); continuing -- the user-scope git default "
        f"(L1) remains the structural control and this gate is the second layer. "
        f"Inconclusive is NOT a pass.",
        file=sys.stderr,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="GCM lane credential-posture gate")
    ap.add_argument("--json", action="store_true", help="emit the decision document")
    ap.add_argument("--git", default=None, help="git executable (default: PATH)")
    ap.add_argument("--test-global", default=None, dest="test_global",
                    help="TEST-ONLY: point git's global scope at a scratch file")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress the human message (still returns the exit code)")
    args = ap.parse_args(argv)

    doc = evaluate(git=args.git, test_global=args.test_global)
    code = 0 if args.quiet else render_decision(doc)
    if args.json:
        print(json.dumps(doc, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
