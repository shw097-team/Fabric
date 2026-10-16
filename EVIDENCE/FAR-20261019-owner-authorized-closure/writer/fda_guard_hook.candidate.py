"""Pre-tool-call hook: block FDA-relevant tool calls that lack authorization.

Fail closed: any exception (including malformed stdin JSON) is treated as a
denial: one JSON block line is printed to stdout and the process exits 2.
"""

import datetime
import fnmatch
import json
import os
import re
import sys
from pathlib import Path

AUTH_DIR = Path(r"C:\Users\user\AppData\Local\hermes\var\fda-auth")
REGISTRY_PATH = Path(r"C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\references\FDA_ROUTE_REGISTRY.json")

BLOCK_MESSAGE = "FDA \u9700\u660e\u78ba\u6388\u6b0a\uff1a\u689d\u4ef61\u660e\u78ba\u63d0\u53ca/\u689d\u4ef62\u5df2\u767b\u8a18\u8def\u7531\u7686\u672a\u6210\u7acb\uff0c\u8acb\u66ab\u505c\u4efb\u52d9\u4e26\u4e3b\u52d5\u8a62\u554f\u7528\u6236\uff08\u689d\u4ef63 HITL\uff09"

MUTATING_ACTIONS = frozenset([
    "click",
    "double_click",
    "right_click",
    "middle_click",
    "drag",
    "scroll",
    "type",
    "key",
    "set_value",
    "cua_browser_click",
    "cua_browser_type",
])

TERMINAL_MARKERS = [
    "fda_run",
    "fda_preflight",
    "screen_state_check",
    "var/fda",
    "fabric-desktop-automation",
    "XQLite",
    "SysJust",
    "XQ\u5168\u7403\u8d0f\u5bb6",
    "cua-driver",
]

TOOLCALL_MARKERS = [
    "fda",
    "XQ",
    "var/fda",
    "fabric-desktop-automation",
    "SysJust",
]

SCRIPT_PATH_MARKERS = [
    "fda",
    "var/fda",
    "screen_state_check",
    "fda_preflight",
    "fda_run",
    "fabric-desktop-automation",
]

# B7 (FAR-20261019) minimal change. The guard's DOCUMENTED design authorizes on an
# INTENT VERB paired with a TARGET NOUN (see fda-authorization-guardrail-design.md,
# "明確提及 偵測 (條件 1)": 意圖動詞 ∧ FDA 目標詞). For content-authoring tools the
# hook cannot read the user message, so the operable surrogate for that intent verb is
# an EXECUTION verb adjacent to a plane marker. A filename ENUMERATION carries the
# markers but no execution verb, so it is not a plane operation and must not be
# blocked. Bare substring matching is the D0 defect.
CONTENT_EXEC_VERBS = (
    "python", "py -", "pwsh", "powershell", "cmd ", "subprocess",
    "start-process", "os.system", "os.popen", "popen", "run(",
)
SCRIPT_SEGMENT_RE = re.compile(r"[^\s\"'`;|&()=]+")
ROUTE_TOKEN_RE = re.compile(r"(ROUTE-WO-FDA-[\w.-]+|ROUTE-SQS-[\w.-]+)", re.IGNORECASE)
DOUBLE_DASH_ROUTE_RE = re.compile(r"--route-id(?:=|\s+)([^\s,;]+)", re.IGNORECASE)
SINGLE_DASH_ROUTE_RE = re.compile(r"(?<![\w-])-route-id(?:=|\s+)([^\s,;]+)", re.IGNORECASE)


def _args_text(args):
    """Return a JSON-string representation of the args value."""
    if args is None:
        return ""
    if isinstance(args, str):
        return args
    return json.dumps(args)


def _command_text(args):
    """Extract the command string from terminal args (dict or JSON string)."""
    if isinstance(args, dict):
        command = args.get("command")
        if isinstance(command, str):
            return command
        return json.dumps(args)
    if isinstance(args, str):
        try:
            parsed = json.loads(args)
        except Exception:
            return args
        if isinstance(parsed, dict):
            command = parsed.get("command")
            if isinstance(command, str):
                return command
            return json.dumps(parsed)
        return args
    return ""


def _action_from_args(args):
    """Extract the action value from computer_use args."""
    if isinstance(args, dict):
        action = args.get("action")
        return action if isinstance(action, str) else ""
    if isinstance(args, str):
        try:
            parsed = json.loads(args)
        except Exception:
            return ""
        if isinstance(parsed, dict):
            action = parsed.get("action")
            return action if isinstance(action, str) else ""
    return ""


def _target_path(args):
    """Extract the destination path from write_file/patch args."""
    parsed = args
    if isinstance(args, str):
        try:
            parsed = json.loads(args)
        except Exception:
            return None
    if not isinstance(parsed, dict):
        return None
    for key in ("path", "file_path", "filepath", "target", "destination"):
        value = parsed.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _is_fda_path(target):
    """True when the target is the registry file or lives under fda-auth."""
    try:
        target_abs = os.path.normcase(os.path.abspath(str(target)))
    except Exception:
        return False
    auth_abs = os.path.normcase(os.path.abspath(str(AUTH_DIR)))
    registry_abs = os.path.normcase(os.path.abspath(str(REGISTRY_PATH)))
    if target_abs == registry_abs:
        return True
    if target_abs == auth_abs or target_abs.startswith(auth_abs + os.sep):
        return True
    if fnmatch.fnmatch(os.path.basename(target_abs), "FDA_ROUTE_REGISTRY.json"):
        return True
    if fnmatch.fnmatch(target_abs, auth_abs + os.sep + "*"):
        return True
    return False


def extract_script_paths(command):
    """Extract FDA-related script path segments from a terminal command."""
    paths = []
    for segment in SCRIPT_SEGMENT_RE.findall(command):
        lowered = segment.lower()
        if any(marker.lower() in lowered for marker in SCRIPT_PATH_MARKERS):
            paths.append(segment)
        elif "fabric-desktop-automation" in lowered and lowered.endswith(".py"):
            paths.append(segment)
    return paths


def _content_is_execution(lowered):
    """B7: True when the text carries an EXECUTION verb, i.e. it would RUN a plane
    script -- the operable surrogate for the documented intent verb. Pure filename
    enumeration carries the markers but no execution verb, so it is not a plane
    operation."""
    return any(verb in lowered for verb in CONTENT_EXEC_VERBS)


def classify_fda_relevant(tool_name, args, extra_text=""):
    """Return True when the tool call is FDA-relevant and must be gated."""
    if tool_name == "terminal":
        command = _command_text(args)
        normalized = command.replace("\\", "/").lower()
        return any(marker.lower() in normalized for marker in TERMINAL_MARKERS)

    if tool_name == "computer_use":
        action = _action_from_args(args).lower()
        if action == "capture":
            sys.stderr.write(
                "fda_guard_hook: computer_use 'capture' is read-only; not blocked.\n"
            )
            return False
        if action in MUTATING_ACTIONS:
            lowered = (_args_text(args) + " " + extra_text).lower()
            return any(token.lower() in lowered for token in ("XQ", "SysJust", "XQLite"))
        return False

    if tool_name in ("execute_code", "delegate_task", "write_file", "patch"):
        lowered = _args_text(args).lower()
        marker_present = any(marker.lower() in lowered for marker in TOOLCALL_MARKERS)
        # B7: a write INTO the gate's own protected surface is always gated, markers
        # or not (that path check is class-level, not content-level).
        if tool_name in ("write_file", "patch"):
            target = _target_path(args)
            if target is not None and _is_fda_path(target):
                return True
        # B7: a marker only gates when the content would EXECUTE a plane script. An
        # artifact that merely ENUMERATES filename markers is not a plane operation
        # (the D0 false positive): no execution verb, so not blocked.
        return marker_present and _content_is_execution(lowered)

    return False


def _token_authorizes(session_id):
    """Condition 1: a live session token for this session exists."""
    if not session_id:
        return False
    token_path = AUTH_DIR / ("%s.json" % session_id)
    if not token_path.exists():
        return False
    try:
        token = json.loads(token_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if not isinstance(token, dict):
        return False
    if token.get("session_id") != session_id:
        return False
    expires_raw = token.get("expires_at_utc")
    if not isinstance(expires_raw, str) or not expires_raw:
        return False
    try:
        expires = datetime.datetime.fromisoformat(expires_raw.replace("Z", "+00:00"))
    except Exception:
        return False
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=datetime.timezone.utc)
    return expires > datetime.datetime.now(datetime.timezone.utc)


def _load_registry():
    """Load the route registry; missing/unreadable yields no routes."""
    try:
        if not REGISTRY_PATH.exists():
            return {}
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, (dict, list)) else {}
    except Exception:
        return {}


def _iter_routes(registry):
    """Yield route entry dicts from a dict- or list-shaped registry."""
    if isinstance(registry, dict):
        if "routes" in registry:
            for entry in _iter_routes(registry["routes"]):
                yield entry
            return
        for key, value in registry.items():
            if isinstance(value, dict):
                entry = dict(value)
                entry.setdefault("id", key)
                yield entry
            elif isinstance(value, str):
                yield {"id": key, "status": value}
    elif isinstance(registry, list):
        for item in registry:
            if isinstance(item, dict):
                yield item


def _registry_authorizes(registry, route_ids):
    """Condition 2: any candidate route id is ACTIVE and unexpired."""
    if not route_ids:
        return False
    today = datetime.datetime.now(datetime.timezone.utc).date()
    wanted = {str(route_id).lower() for route_id in route_ids}
    for entry in _iter_routes(registry):
        entry_id = entry.get("id") or entry.get("route_id")
        if entry_id is None or str(entry_id).lower() not in wanted:
            continue
        if str(entry.get("status", "")).upper() != "ACTIVE":
            continue
        expires_raw = (
            entry.get("expires")
            or entry.get("expires_at")
            or entry.get("expires_at_utc")
            or entry.get("expires_on")
        )
        if expires_raw is None:
            continue
        try:
            expires_date = datetime.date.fromisoformat(str(expires_raw)[:10])
        except Exception:
            continue
        if expires_date >= today:
            return True
    return False


def _route_ids_from_text(text):
    """Collect candidate route ids from ROUTE-* tokens in a text blob."""
    ids = []
    for match in ROUTE_TOKEN_RE.finditer(text):
        token = match.group(1)
        ids.append(token)
        for prefix in ("ROUTE-WO-FDA-", "ROUTE-SQS-"):
            if token[: len(prefix)].upper() == prefix:
                suffix = token[len(prefix):]
                if suffix:
                    ids.append(suffix)
                break
    return ids


def _deny():
    """Print the single JSON block line used for every denial."""
    payload = json.dumps({"action": "block", "message": BLOCK_MESSAGE})
    sys.stdout.write(payload + "\n")


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("empty stdin")
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("stdin is not a JSON object")
        # real wire format: args arrive as tool_input; extra carries non-top-level keys
        extra = data.get("extra")
        if isinstance(extra, dict):
            for k, v in extra.items():
                data.setdefault(k, v)
        if data.get("tool_input") is not None and data.get("args") is None:
            data["args"] = data["tool_input"]

        tool_name = data.get("tool_name")
        args = data.get("args")
        session_id = data.get("session_id")

        extra_text = ""
        extra = data.get("extra")
        if isinstance(extra, dict):
            extra_text = json.dumps(extra)
        if not classify_fda_relevant(tool_name, args, extra_text):
            return 0

        if _token_authorizes(session_id):
            return 0

        registry = _load_registry()
        route_ids = []
        if tool_name == "terminal":
            command = _command_text(args)
            extract_script_paths(command)  # identify FDA script paths per spec
            route_ids.extend(_route_ids_from_text(command))
            match = DOUBLE_DASH_ROUTE_RE.search(command)
            if match is None:
                match = SINGLE_DASH_ROUTE_RE.search(command)
            if match is not None:
                route_ids.append(match.group(1).strip('"\'`'))
        route_ids.extend(_route_ids_from_text(_args_text(args)))
        if route_ids and _registry_authorizes(registry, route_ids):
            return 0

        _deny()
        return 2
    except Exception:
        _deny()
        return 2


try:
    sys.stdin.reconfigure(encoding="utf-8")
except Exception:
    pass


if __name__ == "__main__":
    sys.exit(main())