# -*- coding: utf-8 -*-
"""fda_preflight.py — FIXED GATE 0 for ANY FDA-class desktop automation (user-mandated
2026-08-14, UD-FDA-UPGRADE-HITL-2026-08-14-001 / UD-FAR-RESEARCH-GATE-2026-08-14-001).

READ-ONLY preflight gate: verify the qualified assets exist, load the routing truth
(matrix), compute the ROUTE + ALLOWED_INPUT_CHANNELS for a requested action, and exit
0 (PASS) or 2 (BLOCKED). ZERO write, ZERO install, ZERO mouse — this script itself
must never become the "乱装工具" it is guarding against.

Usage (any FDA/XQ desktop task, BEFORE any automation):
    python fda_preflight.py --app XQ --app-version 3.20.02-260811 --action-class XQ_LAUNCH_LOCATE --route-id ROUTE-WO-FDA-GUARD-IMPL-001
    python fda_preflight.py --app XQ --app-version 3.20.02-260811 --action-class XQ_LAUNCH_LOCATE --auth-token <TOKEN_FILE>
    python fda_preflight.py --list                        # dump all matrix action classes
    python fda_preflight.py --check-assets                # asset presence only

Flags:
    --route-id <ID>      registered governed route id (condition 2); e.g. ROUTE-WO-FDA-GUARD-IMPL-001
    --auth-token <FILE>  path to a session token file minted by fda_guard_mint.py (condition 1)

Exit codes: 0 = PASS (proceed with ALLOWED_INPUT_CHANNELS only)
            2 = BLOCKED (stop, report to user, record defect; NO install/retry attempts)
                --action-class is operation intent -> REQUIRES a valid --route-id or
                --auth-token; otherwise blocked_reasons contains no_authorization:<reason>
                and the route is NOT computed. --list / --check-assets are diagnostic
                and need no authorization.
"""
import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# --- qualified asset inventory (hardcoded, matches screen_state_check.py style) ---
ASSETS = {
    "cua_driver": r"C:\Users\user\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe",
    "pywinauto": r"C:\Projects\Agent_Workspace\HG-KSEOS\.venv\Lib\site-packages\pywinauto",
    "xq_adapter": r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\xq_native_adapter.py",
    "matrix": r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation\FDA_DESKTOP_CAPABILITY_MATRIX.yaml",
    "screen_state_check": r"C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\references\screen_state_check.py",
}
BLOCKED_REASONS = []  # filled during checks; non-empty => exit 2

# --- governed route registry (guardrail condition 2; read-only) ---
REGISTRY_PATH = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\references\FDA_ROUTE_REGISTRY.json")


def check_assets() -> dict:
    """Presence check only. Returns {name: {present, path}}; never installs."""
    out = {}
    for name, path in ASSETS.items():
        present = Path(path).exists()
        out[name] = {"present": present, "path": path}
        if not present:
            BLOCKED_REASONS.append(f"asset_missing:{name}")
    return out


def load_matrix() -> dict:
    """Load the routing truth (FDA_DESKTOP_CAPABILITY_MATRIX.yaml). Read-only."""
    import yaml
    p = Path(ASSETS["matrix"])
    if not p.exists():
        BLOCKED_REASONS.append("matrix_missing")
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def matrix_to_flat(matrix: dict) -> dict:
    """Conversion layer: nested matrix schema -> flat dict consumed by fda_router.route().

    matrix schema: action_classes.<name>.providers.<PROVIDER>.state (QUALIFIED/...)
    router expects: {(app, app_version, action_class): {provider.lower(): 'PASS'}}
    Mapping: state QUALIFIED (or QUALIFIED_SURFACE) -> 'PASS' for routing purposes;
    the raw state is kept in ALLOWED_INPUT_CHANNELS output for honesty.
    """
    flat = {}
    for cls_name, cls in (matrix.get("action_classes") or {}).items():
        app_id = (cls.get("application") or {}).get("id")
        ver = (cls.get("application") or {}).get("version")
        if not app_id or not ver:
            continue
        # matrix version strings carry a product prefix ('XQLite-3.20.02-260811');
        # fda_router keys on the bare version -> strip the prefix
        ver_bare = ver.split("-", 1)[-1] if "-" in ver else ver
        prov = {}
        for pname, pdata in (cls.get("providers") or {}).items():
            st = (pdata or {}).get("state")
            if st in ("QUALIFIED", "QUALIFIED_SURFACE"):
                prov[pname.lower()] = "PASS"
        flat[(app_id, ver_bare, cls_name)] = prov
    return flat


def compute_route(matrix: dict, app: str, app_version: str, action_class: str) -> dict:
    """Use the REAL fda_router.route() (imported, never rewritten)."""
    sys.path.insert(0, r"C:\Projects\Agent_Workspace\Fabric\fabric-desktop-automation")
    from fda_router import route, Request  # noqa: E402

    flat = matrix_to_flat(matrix)
    # resolve the certified entry for this exact (app, version, class); matrix version
    # string is like 'XQLite-3.20.02-260811' -> strip prefix for matching
    candidates = {k: v for k, v in flat.items() if k[2] == action_class}
    if not candidates:
        BLOCKED_REASONS.append(f"no_matrix_row:{action_class}")
        return {"route": "BLOCKED", "allowed_channels": [], "reason": "no matrix row"}
    # try exact app_version match first, then any row of the same action_class
    match = candidates.get((app, app_version, action_class)) or next(iter(candidates.values()))
    req = Request(app=app, app_version=app_version, action_class=action_class,
                  risk_class="LIVE" if "PAPER" in action_class else "BOUNDED",
                  requires_secret=False, financial_side_effect=False,
                  active_position_policy_mutation=False)
    try:
        # fda_router.route() looks up by (app, app_version, action_class) tuple key
        # inside the dict it receives -> wrap the provider map under the exact key
        key = (app, app_version, action_class)
        provider = route(req, {key: match})
    except Exception as e:  # route() raises on unknown state -> fail closed
        BLOCKED_REASONS.append(f"route_error:{str(e)[:50]}")
        provider = "BLOCKED"
    channels = []
    if provider == "CUA":
        channels = ["CUA_BACKGROUND_ONLY", "WIN32_MESSAGES_ONLY"]
    elif provider == "UFO2":
        channels = ["UFO2_UIA_BACKEND"]
    elif provider == "HITL":
        channels = ["HUMAN_ASSIST"]
    return {"route": provider, "allowed_channels": channels,
            "reason": "matrix routing truth", "matrix_state": match}


def verify_authorization(route_id, auth_token, action_class) -> dict:
    """Authorization gate (guardrail conditions 1/2), pure stdlib.

    route_id path: the route must exist in FDA_ROUTE_REGISTRY.json with status ACTIVE
    (case-insensitive) and expires (ISO date) >= today (UTC); when action_class is
    given, it must be listed in the entry's action_classes (case-insensitive) unless
    the entry has no action_classes key.
    auth_token path: the token file must be valid JSON whose expires_at_utc parses as
    ISO (Z allowed) and lies in the future.
    Returns {'authorized': bool, 'source': 'route'|'token'|None, 'route_id': id|None,
    'reason': str}. Read-only: never writes, never installs.
    """
    if route_id:
        try:
            with open(REGISTRY_PATH, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return {"authorized": False, "source": None, "route_id": None, "reason": "registry_unavailable"}
        entries = data.get("routes") if isinstance(data, dict) and isinstance(data.get("routes"), list) else [data]
        wanted = str(route_id).lower()
        entry = None
        for cand in entries:
            if not isinstance(cand, dict):
                continue
            rid = cand.get("route_id") or cand.get("id")
            if rid is not None and str(rid).lower() == wanted:
                entry = cand
                break
        if entry is None:
            return {"authorized": False, "source": None, "route_id": None, "reason": "route_not_found"}
        if str(entry.get("status") or "").upper() != "ACTIVE":
            return {"authorized": False, "source": None, "route_id": None, "reason": "route_inactive"}
        raw_expires = entry.get("expires")
        try:
            exp = date.fromisoformat(str(raw_expires)[:10]) if raw_expires else None
        except (ValueError, TypeError):
            exp = None
        if exp is None or exp < datetime.now(timezone.utc).date():
            return {"authorized": False, "source": None, "route_id": None, "reason": "route_expired"}
        if action_class is not None and "action_classes" in entry and entry.get("action_classes") is not None:
            allowed = {str(c).lower() for c in entry["action_classes"]}
            if str(action_class).lower() not in allowed:
                return {"authorized": False, "source": None, "route_id": None, "reason": "route_action_class_mismatch"}
        return {"authorized": True, "source": "route",
                "route_id": str(entry.get("route_id") or entry.get("id")), "reason": "ok"}
    elif auth_token:
        try:
            with open(auth_token, encoding="utf-8") as f:
                token_data = json.load(f)
        except Exception:
            return {"authorized": False, "source": None, "route_id": None, "reason": "token_expired"}
        raw_expires = token_data.get("expires_at_utc") if isinstance(token_data, dict) else None
        try:
            exp = datetime.fromisoformat(str(raw_expires).replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return {"authorized": False, "source": None, "route_id": None, "reason": "token_expired"}
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp <= datetime.now(timezone.utc):
            return {"authorized": False, "source": None, "route_id": None, "reason": "token_expired"}
        return {"authorized": True, "source": "token", "route_id": None, "reason": "ok"}
    return {"authorized": False, "source": None, "route_id": None, "reason": "no_authorization"}


def main() -> int:
    ap = argparse.ArgumentParser(description="FDA preflight gate (read-only)")
    ap.add_argument("--app", default="XQ")
    ap.add_argument("--app-version", default="3.20.02-260811")
    ap.add_argument("--action-class")
    ap.add_argument("--route-id",
                    help="registered governed route id (condition 2); e.g. ROUTE-WO-FDA-GUARD-IMPL-001")
    ap.add_argument("--auth-token",
                    help="path to a session token file minted by fda_guard_mint.py (condition 1)")
    ap.add_argument("--list", action="store_true", help="list matrix action classes")
    ap.add_argument("--check-assets", action="store_true", help="assets only")
    args = ap.parse_args()

    assets = check_assets()
    matrix = load_matrix() if not args.check_assets else {}

    # Authorization gate: --action-class means route computation = operation intent,
    # which REQUIRES a governed route id (condition 2) or a minted session token
    # (condition 1). --list / --check-assets are diagnostic-only and stay exempt.
    authz = None
    if args.action_class and not args.list and not args.check_assets:
        authz = verify_authorization(args.route_id, args.auth_token, args.action_class)
        if not authz["authorized"]:
            BLOCKED_REASONS.append(f"no_authorization:{authz['reason']}")
    elif args.list or args.check_assets:
        authz = {"authorized": True, "source": "diagnostic"}

    result = {
        "schema": "FDA-PREFLIGHT/1",
        "assets": assets,
        "blocked_reasons": list(BLOCKED_REASONS),
    }
    if authz is not None:
        result["authorization"] = authz

    if args.list and matrix:
        classes = list((matrix.get("action_classes") or {}).keys())
        result["action_classes"] = classes
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    if args.action_class and matrix and authz is not None and authz["authorized"]:
        result["route_result"] = compute_route(matrix, args.app, args.app_version, args.action_class)
        if result["route_result"]["route"] == "BLOCKED" and "no_matrix_row" not in BLOCKED_REASONS:
            pass  # route BLOCKED already recorded
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 2 if BLOCKED_REASONS else 0


if __name__ == "__main__":
    sys.exit(main())
