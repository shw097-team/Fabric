#!/usr/bin/env python3
"""P2b governed-runtime controller: a THIN JSON-stdin adapter.

This is the controller the Hermes ``mandatory_tool_guard.check_tool_call`` contract invokes (see
``hermes/agent/mandatory_tool_guard.py``). The guard writes a JSON payload on stdin and allows the
tool call ONLY on exit 0 with stdout JSON ``{"action":"allow"}``; every other outcome refuses. The
controller therefore answers exactly that contract and prints exactly one JSON object.

It introduces NO new subsystem. It reuses:
  * ``hg_kseos.role_binding.find_session_binding`` (P2a) for the session -> governed-binding lookup,
    after the dispatcher's spine-open pattern (import ``SharedSpine`` from the repo tree; accept the
    ``HGK_SPINE_DB``/``HGK_SPINE_SCHEMA`` overrides, else the canonical Shared Spine);
  * the profile ``governed_runtime.protected_roots`` list the guard itself read.

Governance rule: inside a governed round a MAKER (EXECUTE) must not write to a protected root
out-of-band; a CHECKER (VERIFY/SECURITY) may inspect. Ordinary sessions and calls that touch no
protected root are allowed unchanged. A call carrying NO session id cannot be attributed to a
governed round at all (a binding requires a non-empty session), so it is answered as
``no-session-id-unattributable`` rather than turned into an exit-3 outage that would refuse every
mutating call of an agent whose session id is absent.
"""
from __future__ import annotations

import json
import os
import posixpath
import sys
from pathlib import Path

# A mutating tool call is the only kind a governed round has to police.
MUTATING = {"write_file", "patch", "execute_code", "terminal"}
# Free-text args: a shell command or inline code whose destination cannot be path-resolved at all.
FREE_TEXT = {"execute_code", "terminal"}
# The role whose ad-hoc writes a governed round must refuse, and the roles that may still inspect.
MAKER_ROLES = {"EXECUTE"}
CHECKER_ROLES = {"VERIFY", "VERIFY_SECURITY", "SECURITY"}

ROOT = Path(__file__).resolve().parents[1]
SPINE_DB = ROOT / "var" / "shared-spine" / "hg-kseos.db"
SPINE_SCHEMA = ROOT / "src" / "hg_kseos" / "schema.sql"
# The single canonical root a governed round must protect when the profile names none.
CANONICAL_PROTECTED_ROOT = "C:/Projects/Agent_Workspace/HG-KSEOS"


def _emit(body: dict, code: int = 0) -> int:
    sys.stdout.write(json.dumps(body))
    sys.stdout.flush()
    return code


def _norm_seps(text: str) -> str:
    """One separator flavour; Windows drops trailing dots/spaces on each NORMAL component.

    '.' and '..' are left intact -- they are segments, not filenames, and must survive to be
    resolved by ``posixpath.normpath``.
    """
    parts = []
    for seg in text.replace("\\", "/").strip().split("/"):
        parts.append(seg if seg in (".", "..") else seg.rstrip(" ."))
    return "/".join(parts)


def _is_abs(posixish: str) -> bool:
    """Absolute in the POSIX or Windows ('C:/..', '//host/share') sense."""
    return posixish.startswith("/") or (len(posixish) >= 2 and posixish[1] == ":")


def _canon(text: str, base: str = "") -> str:
    """Canonicalize a possibly-RELATIVE path for comparison.

    A mutating call may name its target relative to the session cwd and may fold '.'/'..' segments
    into it, so folding separators and case alone is NOT enough: `x.py` from a protected cwd and
    `outside/../protected/x.py` would both read as "outside the protected roots". Absolutize against
    ``base`` (the session cwd the guard sent), resolve dot segments lexically, drop Windows-trailing
    dots/spaces, then casefold.
    """
    folded = _norm_seps(text)
    if not folded:
        return ""
    if base and not _is_abs(folded):
        folded = _norm_seps(base).rstrip("/") + "/" + folded
    return posixpath.normpath(folded).casefold()


def _ensure_src_on_path() -> None:
    """Make the repo tree importable without requiring ``hg_kseos`` to be installed."""
    src = str(ROOT / "src")
    if src not in sys.path:
        sys.path.insert(0, src)


def _load_spine():
    _ensure_src_on_path()
    from hg_kseos.spine import SharedSpine  # noqa: E402

    db = Path(os.environ.get("HGK_SPINE_DB") or SPINE_DB)
    schema = Path(os.environ.get("HGK_SPINE_SCHEMA") or SPINE_SCHEMA)
    return SharedSpine(db, schema)


def _protected_roots(hermes_home: str) -> list[str]:
    """Read ``governed_runtime.protected_roots`` from the profile the guard used.

    Unreadable/empty -> the single canonical root. This is the same source of authority the guard
    consulted, so the controller and the guard agree on what "protected" means.
    """
    try:
        import yaml  # noqa: PLC0415
    except Exception:  # noqa: BLE001 - a missing parser must fall back, never crash
        return [CANONICAL_PROTECTED_ROOT]
    if not hermes_home:
        return [CANONICAL_PROTECTED_ROOT]
    config_path = Path(hermes_home) / "config.yaml"
    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - unreadable config is the documented fallback case
        return [CANONICAL_PROTECTED_ROOT]
    if not isinstance(raw, dict):
        return [CANONICAL_PROTECTED_ROOT]
    binding = raw.get("governed_runtime")
    if not isinstance(binding, dict):
        return [CANONICAL_PROTECTED_ROOT]
    roots = binding.get("protected_roots")
    if not isinstance(roots, list):
        return [CANONICAL_PROTECTED_ROOT]
    clean = [r for r in roots if isinstance(r, str) and r.strip()]
    return clean or [CANONICAL_PROTECTED_ROOT]


def _path_targets(function_name: str, args) -> list[str]:
    """Extract the candidate target path(s) a call would touch, ignoring non-string args safely."""
    if not isinstance(args, dict):
        return []
    if function_name in ("write_file", "patch"):
        value = args.get("path")
        return [value] if isinstance(value, str) and value else []
    if function_name == "terminal":
        command = args.get("command")
        return [command] if isinstance(command, str) and command else []
    if function_name == "execute_code":
        code = args.get("code")
        return [code] if isinstance(code, str) and code else []
    return []


def _hits_protected(function_name: str, targets: list[str], roots: list[str], base: str = "") -> bool:
    """True when a call reaches any protected root.

    A path-shaped arg is absolutized against the session cwd and normalized, then checked by
    containment; a free-text arg (a terminal command or inline code) is checked by scanning for any
    protected-root substring, since it can name a root anywhere. When the session cwd itself sits
    inside a protected root, a path-shaped target that is STILL relative can only land inside that
    root, so it counts as a hit.
    """
    canon_roots = [_canon(r) for r in roots]
    base_canon = _canon(base) if base else ""
    cwd_in_root = bool(base_canon) and any(base_canon == r or base_canon.startswith(r + "/") for r in canon_roots)
    if not targets:
        # A mutating call whose target we could not attribute, issued from inside a protected root.
        return cwd_in_root
    for target in targets:
        is_path = function_name in ("write_file", "patch")
        cand = _canon(target, base if is_path else "")
        for root in canon_roots:
            if is_path:
                if cand == root or cand.startswith(root + "/"):
                    return True
            else:
                if root in cand:
                    return True
        if not is_path:
            # Free text is only scanned for a literal root mention here; whether it can REACH a root
            # is decided in main(), which refuses it outright for a governed MAKER (see FREE_TEXT).
            continue
        if cwd_in_root and not _is_abs(_norm_seps(target)):
            return True
        # A link/junction can still point INTO a protected root when the literal path does not.
        literal = target if _is_abs(_norm_seps(target)) else f"{_norm_seps(base).rstrip('/')}/{_norm_seps(target)}"
        try:
            resolved = _canon(os.path.realpath(literal))
        except Exception:  # noqa: BLE001 - an unresolvable path must never widen the allow
            resolved = ""
        if resolved and resolved != cand:
            for root in canon_roots:
                if resolved == root or resolved.startswith(root + "/"):
                    return True
    return False


def _role_of(binding: dict) -> str:
    """Classify a governed-round binding by the maker/checker roles it declares."""
    roles = binding.get("roles")
    declared = {str(k).upper() for k in roles} if isinstance(roles, dict) else set()
    if declared & MAKER_ROLES:
        return "maker"
    if declared & CHECKER_ROLES:
        return "checker"
    return "other"


def main() -> int:
    raw = sys.stdin.buffer.read()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:  # noqa: BLE001 - malformed/empty stdin is a controller failure
        return 2
    if not isinstance(payload, dict):
        return 2

    function_name = payload.get("function_name")
    if function_name not in MUTATING:
        return _emit({"action": "allow", "reason": "non-mutating"}, 0)

    roots = _protected_roots(payload.get("hermes_home") or "")
    targets = _path_targets(function_name, payload.get("function_args"))
    hits = _hits_protected(function_name, targets, roots, payload.get("session_cwd") or "")
    # A free-text arg (a shell command or inline code) names its destination in a way we cannot
    # resolve: a relative path reaches a protected root from ANY cwd, including the root's parent,
    # and carries no root string to scan for. Such a call is therefore NOT "outside the protected
    # roots" by default -- it falls through to the binding lookup, where a governed MAKER is refused.
    if not hits and function_name not in FREE_TEXT:
        return _emit({"action": "allow", "reason": "outside-protected-roots"}, 0)

    # From here on a mutating call either reaches a protected root or (free text) cannot be shown
    # not to; it may only be allowed by a genuine non-maker session. Everything below is fail-closed.
    #
    # ABSENT/BLANK session id (finding CONTROLLER-ABSENT-SESSION-ID-FAILCLOSED, closed by round
    # LANE-RELIABILITY-CLOSURE-20261016). A governed binding REQUIRES a non-empty session:
    # ``validate_binding`` refuses a blank one and ``find_session_binding`` raises
    # ERR_ROLE_BINDING_SESSION_REQUIRED for it. So a call carrying no session id cannot belong to a
    # governed round -- there is no binding keyed by "" to protect. Mapping its typed refusal to
    # exit 3 was an OUTAGE, not a control: the guard sends ``getattr(agent,"session_id","") or ""``,
    # so ANY agent without a session id had EVERY mutating call refused. It was also inconsistent
    # with the already-allowed unknown-id case (a valid-but-unknown id returns None => allow).
    # Answer the contract instead, with a reason a reader can tell apart from "no governed round".
    session_id = payload.get("session_id")
    if not (isinstance(session_id, str) and session_id.strip()):
        return _emit({"action": "allow", "reason": "no-session-id-unattributable"}, 0)

    try:
        _ensure_src_on_path()
        from hg_kseos import role_binding as _role_binding  # noqa: PLC0415

        spine = _load_spine()
        found = _role_binding.find_session_binding(spine, session_id)
    except Exception:  # noqa: BLE001 - an unacquirable boundary is a refusal, never a pass
        return 3

    if found is None:
        return _emit({"action": "allow", "reason": "no-governed-round"}, 0)

    try:
        wo = str(found.get("workorder"))
        role = _role_of(found.get("binding") or {})
        if role == "maker":
            reason = (f"maker-write-in-governed-round:{wo}" if hits
                      else f"maker-free-text-unresolvable:{wo}")
            return _emit({"action": "deny", "reason": reason}, 0)
        return _emit({"action": "allow", "reason": "checker-may-inspect"}, 0)
    except Exception:  # noqa: BLE001 - any unexpected failure AFTER the binding is known refuses
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
