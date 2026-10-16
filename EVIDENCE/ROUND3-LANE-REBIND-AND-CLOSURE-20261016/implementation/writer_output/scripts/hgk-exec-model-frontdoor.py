#!/usr/bin/env python
"""hgk-exec-model-frontdoor.py — loopback-only EXECUTE-lane protocol proxy (CANDIDATE).

FAR-EXEC-IDENTITY-002. The shared relay on 127.0.0.1:10101 declares one model but serves the
sibling `deepseek-flash` anyway (measured by FAR-EXEC-IDENTITY-001). That relay is a SHARED
resource that PLAN / VERIFY roles also use, so this front door is a *dedicated* boundary for the
sealed EXECUTE lane only, listening on 127.0.0.1:10100 and forwarding to the shared relay.

This is a MODEL-ROUTING POLICY, not content censorship. A request whose `model` field is the
single sanctioned id is forwarded verbatim — its strings, paths, query and body are NOT scanned.
`message.content` that merely *mentions* `deepseek-flash` is ordinary text and MUST be allowed
(regression-tested). What is refused is a request that makes a non-sanctioned model the model
that will actually be routed.

Design summary (see docs/EXEC_IDENTITY_ENFORCEMENT.md for the full semantics):
  * `GET  /healthz`             -> local semantic health; sanctioned provider/model + upstream URL,
                                   no secrets. Harmless on any query string.
  * `GET  /v1/models`           -> only the single sanctioned entry.
  * `GET  /v1/responses` (WS upgrade) -> per-frame model validation before any upstream connect.
  * `POST /v1/chat/completions`, `/v1/responses`, `/v1/responses/compact` -> streaming proxy.
  * any other method/path, or any nonempty query on a POST route, including percent-encoded
    alias tricks -> typed 403. (verdicted BEFORE reading the body: no upstream quota is spent.)
  * JSON bodies are parsed with `object_pairs_hook` so a duplicate key at ANY nesting level is a
    hard 403, in either order. The top-level `model` is authoritative; a nested envelope
    `request.model` / `response.model` must not override it.
  * The sanctioned model token is canonicalised to `<provider>/<id>`. No model-less bypass.
  * Responses are streamed incrementally (SSE / chunked are never buffered) with event data and
    status preserved; hop-by-hop headers filtered; redirects disabled; disconnects handled.
  * One JSON-lines ledger row per HTTP request / WS client frame: timestamp, generated
    correlation id, decision, error class, models, upstream status. No secrets, bodies or query.
    The ledger is appended BEFORE forwarding; if it cannot be appended, the request FAILS CLOSED.
  * Non-loopback bind AND a non-loopback upstream override are refused at startup. The sanctioned
    pair is re-checked at start: anything other than opencode-go/deepseek-v4.1-flash fails start.

This is a RUNTIME control, not an OS security boundary: raw 127.0.0.1:10101 remains reachable and
is explicitly out of scope. Everything here is CANDIDATE.

Interpreter: aiohttp is required. On this host both the repo `.venv` (Python 3.12) and the system
Python (3.11) provide it; discover the interpreter before declaring the dependency (see
docs/RELEASE_NOTES_EXEC_IDENTITY.md).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import time
import uuid
from pathlib import Path

try:
    from aiohttp import ClientSession, ClientTimeout, TCPConnector, WSMsgType, web
except ImportError as exc:  # pragma: no cover - surfaced as a typed start failure
    sys.stderr.write(json.dumps({
        "schema": "HGK-EXEC-FRONTDOOR-START/1",
        "decision": "REFUSE",
        "error_code": "ERR_EXEC_FRONTDOOR_DEPENDENCY_MISSING",
        "detail": f"aiohttp is required but not importable: {exc}",
    }) + "\n")
    raise SystemExit(11)

_HERE = Path(__file__).resolve()
_SUBJECT = _HERE.parent.parent
_ROUND = _SUBJECT.parent
_DEFAULT_DECLARATION = _SUBJECT / "config" / "hermes-codex-lane.json"
_DEFAULT_LEDGER = _ROUND / "_control" / "maker" / "frontdoor-ledger.jsonl"
_DEFAULT_UPSTREAM = "http://127.0.0.1:10101"
_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 10100

_LOOPBACK = {"127.0.0.1", "::1", "localhost"}

_SANCTIONED_PROVIDER = "opencode-go"
_SANCTIONED_MODEL = "deepseek-v4.1-flash"
_SANCTIONED_PAIR = f"{_SANCTIONED_PROVIDER}/{_SANCTIONED_MODEL}"
_FORBIDDEN_SIBLING = "deepseek-flash"

# Exact allowlist: POST targets and the WS-upgrade target. Method/path are matched as exact
# strings, so no percent-decoding of the raw path happens before comparison (which is what makes a
# percent-encoded alias like /v1/chat%2Fcompletions a non-match -> 403).
_POST_ROUTES = frozenset({
    "/v1/chat/completions",
    "/v1/responses",
    "/v1/responses/compact",
})
_WS_ROUTES = frozenset({"/v1/responses"})
_MODELS_ROUTES = frozenset({"/v1/models"})
_HEALTH_ROUTES = frozenset({"/healthz", "/healthz/"})

# A model token is a "bare-ish" id when it carries no scheme, no whitespace and no path-y prefix
# beyond a single `provider/`. Anything else (percent-encoding, scheme, `../`, non-ascii) is
# malformed -> 403 rather than silently normalised.
_SAFE_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)?$")

# -------------------------------------------------------------------------------------------------
# Pool mode (additive, opt-in via --pool). In the LEGACY mode the allow-set holds exactly the
# sanctioned id and every allowed request is rewritten to `_SANCTIONED_PAIR`, so behaviour is
# byte-identical to the single-pair front door. In POOL mode the allow-set is the union of every
# EXECUTE/VERIFY_SECURITY entry's declared id, qualified id and transport_model, and an allowed
# request is forwarded with the MATCHED ENTRY'S TRANSPORT TOKEN verbatim (the relay routes on it:
# opencode-go wants the bare id, the nvidia arm the qualified one, the openai arm the bare one).
_ALLOWED_TOKENS: dict = {
    _SANCTIONED_MODEL: _SANCTIONED_PAIR,
    _SANCTIONED_PAIR: _SANCTIONED_PAIR,
}
_POOL_PATH: "str | None" = None
_POOL_LANES = ("EXECUTE", "VERIFY_SECURITY")

def load_pool_allowlist(path, lanes=None) -> dict:
    """Build the pool allow-set from the lane-route pool artifact. Fail-closed on any defect.

    `lanes` scopes the allow-set to named lanes. Scoping matters: the union of EXECUTE and
    VERIFY_SECURITY is WIDER than the sealed EXECUTE contract (the AO's X5 finding: a union door
    forwards a VERIFY-only arm for an EXECUTE dispatch), so each instance is started for exactly one
    lane and the transport for that lane points at its own door.
    """
    scope = tuple(lanes) if lanes else _POOL_LANES
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"ERR_EXEC_FRONTDOOR_POOL_UNREADABLE: {exc}") from exc
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"ERR_EXEC_FRONTDOOR_POOL_MALFORMED: {exc}") from exc
    lanes_doc = doc.get("lanes")
    if not isinstance(lanes_doc, list):
        raise ValueError("ERR_EXEC_FRONTDOOR_POOL_MALFORMED: no 'lanes' array")
    allow: dict = {}
    for body in lanes_doc:
        if not isinstance(body, dict) or body.get("lane") not in scope:
            continue
        entries = body.get("ordered_pool")
        if not isinstance(entries, list) or not entries:
            raise ValueError(f"ERR_EXEC_FRONTDOOR_POOL_MALFORMED: lane {body.get('lane')!r} has no ordered_pool")
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(f"ERR_EXEC_FRONTDOOR_POOL_MALFORMED: non-object entry in {body.get('lane')!r}")
            provider = entry.get("provider")
            declared = entry.get("model")
            transport = entry.get("transport_model")
            if not isinstance(transport, str) or not transport.strip():
                transport = declared
            if (not isinstance(provider, str) or not provider.strip()
                    or not isinstance(declared, str) or not declared.strip()
                    or not isinstance(transport, str) or not transport.strip()):
                raise ValueError(
                    f"ERR_EXEC_FRONTDOOR_POOL_MALFORMED: entry in {body.get('lane')!r} needs "
                    f"provider/model/transport_model")
            provider, declared, transport = provider.strip(), declared.strip(), transport.strip()
            for key in {declared, f"{provider}/{declared}", transport}:
                seen = allow.get(key)
                if seen is not None and seen != transport:
                    raise ValueError(
                        f"ERR_EXEC_FRONTDOOR_POOL_AMBIGUOUS: {key!r} maps to both {seen!r} and {transport!r}")
                allow[key] = transport
    if not allow:
        raise ValueError("ERR_EXEC_FRONTDOOR_POOL_EMPTY: no EXECUTE/VERIFY_SECURITY entries in the pool")
    return allow

# Envelope keys whose `model` is a nested routing envelope, checked in addition to the authoritative
# top-level model. The top-level model can never be overridden by these.
_ENVELOPE_MODEL_KEYS = ("request", "response")

# Reasonable body limit: relax, but never unbounded.
_MAX_BODY_BYTES = 32 * 1024 * 1024


def _raw_request_target(request: web.Request) -> str:
    """The undecoded request-target from the raw request line, e.g. '/v1/chat%2Fcompletions?x'.

    We classify on the RAW target so a percent-encoded alias can never be decoded into an allowlist
    match. aiohttp raises if the raw line is unavailable; we fall back to the joined path/query.
    """
    try:
        return request.raw_path
    except Exception:
        return request.path + (("?" + request.query_string) if request.query_string else "")

EXIT_OK = 0
EXIT_DEPENDENCY = 11
EXIT_BAD_CONFIG = 9
EXIT_NON_LOOPBACK_REFUSED = 12
EXIT_DECLARATION_DRIFT = 13


# -------------------------------------------------------------------------------------------------
# Sanctioned-pair resolution (declaration-only; re-validated against the exact pair at start).
# -------------------------------------------------------------------------------------------------
def _load_guard_module():
    spec = importlib.util.spec_from_file_location(
        "hgk_lane_guard_for_frontdoor", _HERE.parent / "hgk-lane-guard.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_guard = _load_guard_module()


def load_sanctioned(declaration_path: "str | Path | None" = None) -> dict:
    """Read the sanctioned {provider, model} from the lane declaration."""
    declared = _guard.load_lane_declaration(declaration_path or _DEFAULT_DECLARATION)
    return {
        "provider": declared["provider"],
        "model": declared["model"],
        "path": declared["path"],
    }


def _fail_start(error_code: str, detail: str) -> int:
    sys.stderr.write(json.dumps({
        "schema": "HGK-EXEC-FRONTDOOR-START/1",
        "decision": "REFUSE",
        "error_code": error_code,
        "detail": detail,
    }) + "\n")
    sys.stderr.flush()
    if error_code == "ERR_EXEC_FRONTDOOR_SANCTIONED_DRIFT":
        return EXIT_DECLARATION_DRIFT
    if error_code.startswith("ERR_EXEC_FRONTDOOR_NON_LOOPBACK"):
        return EXIT_NON_LOOPBACK_REFUSED
    if error_code == "ERR_EXEC_FRONTDOOR_DEPENDENCY_MISSING":
        return EXIT_DEPENDENCY
    return EXIT_BAD_CONFIG


def validate_sanctioned_pair(sanctioned: dict) -> tuple[str, str]:
    """Return the canonical (provider, model) or raise ValueError with a typed code."""
    provider = str(sanctioned.get("provider", "")).strip().lower()
    model = str(sanctioned.get("model", "")).strip().lower()
    if _POOL_PATH is None:
        if (provider, model) != (_SANCTIONED_PROVIDER, _SANCTIONED_MODEL):
            raise ValueError(
                f"ERR_EXEC_FRONTDOOR_SANCTIONED_DRIFT: declaration resolves to "
                f"{provider}/{model!r}; this front door is only for "
                f"{_SANCTIONED_PROVIDER}/{_SANCTIONED_MODEL!r}")
        return _SANCTIONED_PROVIDER, _SANCTIONED_MODEL
    if f"{provider}/{model}" not in _ALLOWED_TOKENS:
        raise ValueError(
            f"ERR_EXEC_FRONTDOOR_SANCTIONED_DRIFT: declaration resolves to {provider}/{model!r}, "
            f"which is not a member of the pool allow-list loaded from {_POOL_PATH!r}")
    return provider, model


# -------------------------------------------------------------------------------------------------
# Model-field extraction with strict duplicate-key rejection.
# -------------------------------------------------------------------------------------------------
class DuplicateKeyError(ValueError):
    def __init__(self, key: str):
        super().__init__(f"duplicate JSON key {key!r}")
        self.key = key


def _no_duplicates(pairs):
    seen: dict = {}
    for key, value in pairs:
        if key in seen:
            raise DuplicateKeyError(key)
        seen[key] = value
    return seen


def parse_json_strict(raw: bytes):
    """Parse JSON, rejecting duplicate keys at every level. Raises DuplicateKeyError or ValueError."""
    text = raw.decode("utf-8")
    return json.loads(text, object_pairs_hook=_no_duplicates)


def _canonical_token(model) -> "str | None":
    """Canonical comparison token, or None if the value is not a decidable string model."""
    if not isinstance(model, str):
        return None
    stripped = model.strip()
    token = stripped.lower()
    if not token:
        return None
    if not _SAFE_MODEL_RE.match(stripped):
        return None
    if "/" in token:
        # A provider prefix is only ever legal on an allow-listed id.
        if token not in _ALLOWED_TOKENS:
            return None
    return token


def top_level_models(obj) -> list:
    """The authoritative model value: the top-level `model` if present, else None."""
    if isinstance(obj, dict) and "model" in obj:
        return [obj["model"]]
    return []


def envelope_models(obj) -> list:
    """Nested routing-envelope models (request.model / response.model) that must ALSO be sanctioned.

    These never override the top-level model; they are additional model fields a client may set and
    which must not name the sibling. We deliberately do NOT recurse into arbitrary content objects
    (messages / input / tools), because those legitimately contain user text and structured data
    with a `model` key that is not a routing decision — refusing them would break valid payloads.
    """
    found = []
    if not isinstance(obj, dict):
        return found
    for key in _ENVELOPE_MODEL_KEYS:
        value = obj.get(key)
        if isinstance(value, dict) and "model" in value:
            found.append(value["model"])
    return found


def decide_model(models: list) -> "tuple[str, str | None, str]":
    """Return (decision, error_code, detail) for the collected model fields. Fail-closed."""
    if not models:
        return "REFUSE", "ERR_EXEC_FRONTDOOR_MODEL_ABSENT", "no top-level model field in request body"
    for value in models:
        token = _canonical_token(value)
        if token is None:
            return "REFUSE", "ERR_EXEC_FRONTDOOR_MODEL_MALFORMED", f"undecidable model value {value!r}"
        if token == _FORBIDDEN_SIBLING:
            return "REFUSE", "ERR_EXEC_FRONTDOOR_MODEL_FORBIDDEN", f"forbidden sibling model {value!r}"
        if token not in _ALLOWED_TOKENS:
            return "REFUSE", "ERR_EXEC_FRONTDOOR_MODEL_NOT_SANCTIONED", f"model {value!r} is not sanctioned"
    return "FORWARD", None, f"all {len(models)} model field(s) sanctioned"


def canonicalise_body(obj: dict) -> dict:
    """Rewrite the top-level model to the canonical `<provider>/<id>` without touching content."""
    obj = dict(obj)
    obj["model"] = _ALLOWED_TOKENS.get(_canonical_token(obj.get("model")), _SANCTIONED_PAIR)
    return obj


# -------------------------------------------------------------------------------------------------
# Ledger (fail-closed append).
# -------------------------------------------------------------------------------------------------
class Ledger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, row: dict) -> None:
        line = json.dumps(row, ensure_ascii=False, sort_keys=True)
        # A single line write on a flushed handle. Raises on failure -> caller fails closed.
        with self.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
            handle.flush()


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _new_correlation_id() -> str:
    return uuid.uuid4().hex


# -------------------------------------------------------------------------------------------------
# aiohttp application.
# -------------------------------------------------------------------------------------------------
_HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers",
    "transfer-encoding", "upgrade", "host", "content-length",
}


# -- C6 correlation --------------------------------------------------------------------------------
# The relay persists sha256(<session header>)[:32] as `conversationId` in its usage.jsonl row, and
# documents that field as a log/usage correlation id only (opencodex src/server/request-log-conversation.ts:
# "Best-effort chat/session correlation for Logs / usage.jsonl ... always hashes so client-controlled
# headers cannot land emails or short secrets in usage.jsonl", priority parent-thread > session_id >
# session-id > thread-id). Planting a door-owned derived value turns "which upstream spend row belongs
# to this decision?" from a guess into an equality check, and it cannot be spoofed because the client's
# own session/thread headers are stripped before the value is set.
_SESSION_HEADER_NAMES = ("session_id", "session-id", "x-session-id", "thread-id")


def correlation_session_value(correlation_id: str) -> str:
    """The stable, door-owned value planted in the upstream session header."""
    return f"hgkfd-{correlation_id}"


def correlation_conversation_id(correlation_id: str) -> str:
    """The exact `conversationId` the relay will persist for this request (sha256[:32] of the header)."""
    return hashlib.sha256(correlation_session_value(correlation_id).encode("utf-8")).hexdigest()[:32]


def client_session_digest(request) -> "str | None":
    """sha256[:32] of the client's own session/thread header if present - digest only, never the value.

    Recorded as the second join key: on responses-shaped turns the relay prefers a parent thread id
    over our session header, so the ledger carries both the per-request expectation and the
    per-conversation key.
    """
    for name in _SESSION_HEADER_NAMES:
        raw = request.headers.get(name)
        if raw and raw.strip():
            return hashlib.sha256(raw.strip().encode("utf-8")).hexdigest()[:32]
    return None


class FrontDoor:
    def __init__(self, *, upstream: str, ledger: Ledger, sanctioned_pair: str = _SANCTIONED_PAIR):
        self.upstream = upstream.rstrip("/")
        self.ledger = ledger
        self.sanctioned_pair = sanctioned_pair
        self.upstream_url = self.upstream
        self._session: ClientSession | None = None

    async def _ensure_session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(total=None, sock_connect=30, sock_read=None),
                connector=TCPConnector(limit=64, ssl=False),
                # Redirects disabled: a user-controlled header can never steer the upstream.
                auto_decompress=False,
            )
        return self._session

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    # -- ledger helpers -------------------------------------------------------------------
    def _log(self, *, correlation_id: str, method: str, path: str, decision: str,
             error_class, models: list, upstream_status, transport: str, note: str = "",
             expected_preflight: bool = False, upstream_conversation_id: "str | None" = None,
             upstream_session_id: "str | None" = None, client_session_sha256: "str | None" = None) -> None:
        row = {
            "schema": "HGK-EXEC-FRONTDOOR-LEDGER/2",
            "ts": _now_iso(),
            "correlation_id": correlation_id,
            "method": method,
            "path": path,
            "transport": transport,
            "decision": decision,
            "error_class": error_class,
            # Policy-relevant metadata only: requested model strings, never bodies/headers/secrets.
            "models": [str(m) for m in models],
            "upstream_status": upstream_status,
            # True only for refusals that are a by-design part of a healthy turn (the websocket
            # pre-flight). Explicit on EVERY row so a reader can separate a routing decision from
            # expected noise without parsing the note.
            "expected_preflight": bool(expected_preflight),
            # C6 join keys. upstream_conversation_id is the value the relay will write to its own
            # usage.jsonl `conversationId` for THIS request; client_session_sha256 is the digest of
            # whatever session/thread header the client sent (the relay prefers a parent thread on
            # responses-shaped turns, so this is the fallback key). A decision row can therefore be
            # joined to exactly one spend row by equality, not by guessing.
            "upstream_conversation_id": upstream_conversation_id,
            "upstream_session_id": upstream_session_id,
            "client_session_sha256": client_session_sha256,
            "join_rule": "usage.jsonl.conversationId == upstream_conversation_id (per request) "
                         "or == client_session_sha256 (per conversation); correlated by correlation_id",
        }
        if note:
            row["note"] = note
        self.ledger.append(row)

    def ledger_append_safe(self, row: dict) -> bool:
        """Best-effort append for pre-forward diagnostics; never raises."""
        try:
            self.ledger.append(row)
            return True
        except Exception:
            return False

    # -- local endpoints ------------------------------------------------------------------
    async def healthz(self, request: web.Request) -> web.Response:
        # Harmless regardless of query string; no secrets.
        return web.json_response({
            "schema": "HGK-EXEC-FRONTDOOR-HEALTH/1",
            "status": "ok",
            "claim_ceiling": "CANDIDATE_ONLY",
            "scope": "sealed EXECUTE lane only",
            "sanctioned_provider": _SANCTIONED_PROVIDER,
            "sanctioned_model": _SANCTIONED_MODEL,
            "sanctioned_pair": self.sanctioned_pair,
            "pool_path": _POOL_PATH,
            "pool_lanes": list(_POOL_LANES) if _POOL_PATH else None,
            "allowlist_size": len(_ALLOWED_TOKENS),
            "upstream": self.upstream_url,
            "raw_upstream_out_of_scope": f"{self.upstream_url} (127.0.0.1:10101) remains reachable",
        })

    async def models(self, request: web.Request) -> web.Response:
        if _POOL_PATH is None:
            data = [{
                "id": self.sanctioned_pair,
                "object": "model",
                "owned_by": _SANCTIONED_PROVIDER,
            }]
        else:
            data = [{
                "id": token,
                "object": "model",
                "owned_by": token.partition("/")[0] or _SANCTIONED_PROVIDER,
            } for token in sorted(set(_ALLOWED_TOKENS.values()))]
        return web.json_response({"object": "list", "data": data})

    # -- request routing ------------------------------------------------------------------
    def _refuse(self, request: web.Request, correlation_id: str, error_code: str,
                detail: str, models: "list | None" = None, http: int = 403) -> web.Response:
        self._log(correlation_id=correlation_id, method=request.method, path=request.path,
                  decision="REFUSE", error_class=error_code, models=models or [],
                  upstream_status=None, transport="http")
        return web.json_response({
            "schema": "HGK-EXEC-FRONTDOOR-DECISION/2",
            "claim_ceiling": "CANDIDATE_ONLY",
            "decision": "REFUSE",
            "error_code": error_code,
            "detail": detail,
            "correlation_id": correlation_id,
        }, status=http)

    def _classify_route(self, request: web.Request) -> "tuple[str, str | None]":
        """Return (kind, error_code). kind is 'post' | 'ws' | 'models' | 'health' | 'refuse'."""
        method = request.method
        raw_target = _raw_request_target(request)
        raw_path, _, raw_query = raw_target.partition("?")
        upgrade = request.headers.get("Upgrade", "").strip().lower()

        if method == "GET":
            if raw_path in _HEALTH_ROUTES:
                return "health", None
            if raw_path in _MODELS_ROUTES and not raw_query:
                return "models", None
            if raw_path in _WS_ROUTES and upgrade == "websocket" and not raw_query:
                return "ws", None
            return "refuse", "ERR_EXEC_FRONTDOOR_ROUTE_REFUSED"
        if method == "POST":
            if raw_path in _POST_ROUTES:
                if raw_query:
                    return "refuse", "ERR_EXEC_FRONTDOOR_QUERY_REFUSED"
                return "post", None
            return "refuse", "ERR_EXEC_FRONTDOOR_ROUTE_REFUSED"
        return "refuse", "ERR_EXEC_FRONTDOOR_METHOD_REFUSED"

    async def _read_body(self, request: web.Request) -> bytes:
        if request.content_length is not None and request.content_length > _MAX_BODY_BYTES:
            raise web.HTTPRequestEntityTooLarge(max_size=_MAX_BODY_BYTES, actual_size=request.content_length)
        return await request.read()

    def _forward_headers(self, request: web.Request) -> "dict[str, str]":
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP_BY_HOP}
        # Never let a client header select an arbitrary upstream.
        headers.pop("Host", None)
        headers.pop("host", None)
        return headers

    async def handle(self, request: web.Request) -> web.StreamResponse:
        correlation_id = _new_correlation_id()
        kind, error_code = self._classify_route(request)

        if kind == "health":
            return await self.healthz(request)
        if kind == "models":
            return await self.models(request)
        if kind == "refuse":
            # Verdict before reading the body: a refused route never spends upstream quota.
            return self._refuse(request, correlation_id, error_code or "ERR_EXEC_FRONTDOOR_ROUTE_REFUSED",
                                f"method={request.method} path={request.path} query={request.query_string!r}")
        if kind == "ws":
            return await self.websocket(request)

        # kind == "post"
        try:
            raw = await self._read_body(request)
        except web.HTTPException:
            raise
        except Exception as exc:
            return self._refuse(request, correlation_id, "ERR_EXEC_FRONTDOOR_BODY_READ",
                                f"{type(exc).__name__}: {exc}")

        if not raw:
            return self._refuse(request, correlation_id, "ERR_EXEC_FRONTDOOR_MODEL_ABSENT",
                                "empty body")

        try:
            parsed = parse_json_strict(raw)
        except DuplicateKeyError as exc:
            return self._refuse(request, correlation_id, "ERR_EXEC_FRONTDOOR_DUPLICATE_KEY",
                                f"duplicate JSON key {exc.key!r}", models=[])
        except RecursionError:
            return self._refuse(request, correlation_id, "ERR_EXEC_FRONTDOOR_BODY_MALFORMED",
                                "body nesting too deep")
        except ValueError as exc:
            return self._refuse(request, correlation_id, "ERR_EXEC_FRONTDOOR_BODY_NOT_JSON",
                                f"body is not valid JSON: {exc}")

        if not isinstance(parsed, dict):
            return self._refuse(request, correlation_id, "ERR_EXEC_FRONTDOOR_BODY_NOT_OBJECT",
                                "top-level JSON value is not an object")

        models = top_level_models(parsed) + envelope_models(parsed)
        decision, err, detail = decide_model(models)
        if decision != "FORWARD":
            return self._refuse(request, correlation_id, err or "ERR_EXEC_FRONTDOOR_MODEL_FORBIDDEN",
                                detail, models=models)

        # Canonicalise the top-level model, preserve every other byte of semantics.
        body_obj = canonicalise_body(parsed)
        forward_body = json.dumps(body_obj, ensure_ascii=False).encode("utf-8")
        headers = self._forward_headers(request)
        headers["Content-Length"] = str(len(forward_body))
        headers["Content-Type"] = "application/json"
        # C6: strip any client-supplied session/thread header, then plant this door's own derived id.
        # A caller must never be able to choose or collide with the correlation label.
        for name in [k for k in list(headers) if k.lower() in _SESSION_HEADER_NAMES]:
            headers.pop(name, None)
        headers["session_id"] = correlation_session_value(correlation_id)
        corr = {"upstream_conversation_id": correlation_conversation_id(correlation_id),
                "upstream_session_id": correlation_session_value(correlation_id),
                "client_session_sha256": client_session_digest(request)}

        # FAIL CLOSED: the FORWARD ledger row must land before we touch upstream.
        try:
            self._log(correlation_id=correlation_id, method=request.method, path=request.path,
                      decision="FORWARD", error_class=None, models=models,
                      upstream_status=None, transport="http", **corr)
        except Exception as exc:
            # Do NOT call _refuse: that would try to append to the same broken ledger and recurse.
            return web.json_response({
                "schema": "HGK-EXEC-FRONTDOOR-DECISION/2",
                "claim_ceiling": "CANDIDATE_ONLY",
                "decision": "REFUSE",
                "error_code": "ERR_EXEC_FRONTDOOR_LEDGER_FAILED",
                "detail": f"ledger append failed: {type(exc).__name__}: {exc}",
                "correlation_id": correlation_id,
            }, status=403)

        return await self._stream_upstream(request, correlation_id, forward_body, headers, models, corr)

    async def _stream_upstream(self, request: web.Request, correlation_id: str, body: bytes,
                               headers: dict, models: list, corr: dict) -> web.StreamResponse:
        session = await self._ensure_session()
        target = self.upstream + request.path
        try:
            upstream_resp = await session.request(
                request.method, target, data=body, headers=headers, allow_redirects=False)
        except Exception as exc:
            self._log(correlation_id=correlation_id, method=request.method, path=request.path,
                      decision="REFUSE", error_class="ERR_EXEC_FRONTDOOR_UPSTREAM_UNREACHABLE",
                      models=models, upstream_status=None, transport="http", **corr)
            return web.json_response({
                "schema": "HGK-EXEC-FRONTDOOR-DECISION/2",
                "decision": "REFUSE",
                "error_code": "ERR_EXEC_FRONTDOOR_UPSTREAM_UNREACHABLE",
                "detail": f"{type(exc).__name__}: {exc}",
                "correlation_id": correlation_id,
            }, status=502)

        status = upstream_resp.status
        self._log(correlation_id=correlation_id, method=request.method, path=request.path,
                  decision="FORWARD", error_class=None, models=models,
                  upstream_status=status, transport="http", **corr)

        resp = web.StreamResponse(status=status)
        ctype = upstream_resp.headers.get("Content-Type")
        if ctype:
            resp.headers["Content-Type"] = ctype
        for key, value in upstream_resp.headers.items():
            if key.lower() in _HOP_BY_HOP or key.lower() in ("content-type", "content-length"):
                continue
            resp.headers[key] = value
        try:
            await resp.prepare(request)
        except Exception:
            upstream_resp.release()
            return resp

        try:
            async for chunk in upstream_resp.content.iter_any():
                if not chunk:
                    continue
                try:
                    await resp.write(chunk)
                except (ConnectionResetError, RuntimeError):
                    # Client disconnected mid-stream; drop the upstream body and stop.
                    break
            try:
                await resp.write_eof()
            except Exception:
                pass
        finally:
            upstream_resp.release()
        return resp

    # -- websocket ------------------------------------------------------------------------
    async def websocket(self, request: web.Request) -> web.WebSocketResponse:
        correlation_id = _new_correlation_id()
        # /v1/responses GET+Upgrade is the only WS route. Query must be empty (classified already).
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # Upstream WS is opened lazily, only AFTER a valid model frame.
        upstream_ws = None
        upstream_session = None
        pump_task = None

        async def close_policy(reason: str, error_code: str) -> None:
            try:
                await ws.send_json({
                    "type": "error",
                    "schema": "HGK-EXEC-FRONTDOOR-WS-DECISION/1",
                    "decision": "REFUSE",
                    "error_code": error_code,
                    "detail": reason,
                    "correlation_id": correlation_id,
                })
            except Exception:
                pass
            await ws.close(code=1008, message=error_code.encode("utf-8")[:120])

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    frame = msg.data
                    # Validate EVERY client text frame before any upstream forwarding.
                    try:
                        parsed = parse_json_strict(frame.encode("utf-8"))
                    except DuplicateKeyError as exc:
                        self._log(correlation_id=correlation_id, method="WS", path=request.path,
                                  decision="REFUSE", error_class="ERR_EXEC_FRONTDOOR_DUPLICATE_KEY",
                                  models=[], upstream_status=None, transport="ws",
                                  note="client frame")
                        await close_policy(f"duplicate JSON key {exc.key!r}",
                                           "ERR_EXEC_FRONTDOOR_DUPLICATE_KEY")
                        return ws
                    except (ValueError, RecursionError) as exc:
                        self._log(correlation_id=correlation_id, method="WS", path=request.path,
                                  decision="REFUSE", error_class="ERR_EXEC_FRONTDOOR_BODY_NOT_JSON",
                                  models=[], upstream_status=None, transport="ws",
                                  note="client frame")
                        await close_policy(f"frame is not valid JSON: {exc}",
                                           "ERR_EXEC_FRONTDOOR_BODY_NOT_JSON")
                        return ws

                    if not isinstance(parsed, dict):
                        self._log(correlation_id=correlation_id, method="WS", path=request.path,
                                  decision="REFUSE", error_class="ERR_EXEC_FRONTDOOR_BODY_NOT_OBJECT",
                                  models=[], upstream_status=None, transport="ws",
                                  note="client frame")
                        await close_policy("frame is not a JSON object",
                                           "ERR_EXEC_FRONTDOOR_BODY_NOT_OBJECT")
                        return ws

                    models = top_level_models(parsed) + envelope_models(parsed)
                    decision, err, detail = decide_model(models)
                    if decision != "FORWARD":
                        self._log(correlation_id=correlation_id, method="WS", path=request.path,
                                  decision="REFUSE", error_class=err, models=models,
                                  upstream_status=None, transport="ws", note="client frame")
                        await close_policy(detail, err or "ERR_EXEC_FRONTDOOR_MODEL_FORBIDDEN")
                        return ws

                    # Valid model frame: connect the upstream lazily (no quota on rejected traffic).
                    if upstream_ws is None:
                        upstream_session = await self._ensure_session()
                        try:
                            upstream_ws = await upstream_session.ws_connect(
                                self.upstream + request.path)
                        except Exception as exc:
                            self._log(correlation_id=correlation_id, method="WS", path=request.path,
                                      decision="REFUSE",
                                      error_class="ERR_EXEC_FRONTDOOR_UPSTREAM_UNREACHABLE",
                                      models=models, upstream_status=None, transport="ws",
                                      expected_preflight=True,
                                      note="client websocket pre-flight: the upstream relay serves these "
                                           "lanes over HTTP only, so this refusal is expected; the same "
                                           "turn then FORWARDs over http and the upstream answers 200 "
                                           "(measured 4-7 such rows per turn, ~3-8 s before the fallback). "
                                           "NOT a block and NOT a routing decision. The WS path stays "
                                           "served because per-frame model validation is a certified "
                                           "control of this door.")
                            await close_policy(f"upstream WS unreachable: {exc}",
                                               "ERR_EXEC_FRONTDOOR_UPSTREAM_UNREACHABLE")
                            return ws
                        # Relay upstream -> client.
                        async def pump() -> None:
                            try:
                                async for up in upstream_ws:
                                    if up.type == WSMsgType.TEXT:
                                        await ws.send_str(up.data)
                                    elif up.type == WSMsgType.BINARY:
                                        await ws.send_bytes(up.data)
                                    elif up.type in (WSMsgType.CLOSE, WSMsgType.CLOSED,
                                                     WSMsgType.CLOSING):
                                        break
                                    elif up.type == WSMsgType.ERROR:
                                        break
                            except Exception:
                                pass
                        import asyncio
                        pump_task = asyncio.ensure_future(pump())

                    # Forward the validated (canonicalised) frame.
                    forward = json.dumps(canonicalise_body(parsed), ensure_ascii=False)
                    self._log(correlation_id=correlation_id, method="WS", path=request.path,
                              decision="FORWARD", error_class=None, models=models,
                              upstream_status=None, transport="ws", note="client frame")
                    try:
                        await upstream_ws.send_str(forward)
                    except Exception as exc:
                        await close_policy(f"upstream send failed: {exc}",
                                           "ERR_EXEC_FRONTDOOR_UPSTREAM_UNREACHABLE")
                        return ws

                elif msg.type == WSMsgType.BINARY:
                    self._log(correlation_id=correlation_id, method="WS", path=request.path,
                              decision="REFUSE", error_class="ERR_EXEC_FRONTDOOR_WS_BINARY",
                              models=[], upstream_status=None, transport="ws", note="client frame")
                    await close_policy("binary frames are not accepted",
                                       "ERR_EXEC_FRONTDOOR_WS_BINARY")
                    return ws
                elif msg.type == WSMsgType.ERROR:
                    break
                # PING/PONG/CLOSE handled by aiohttp.
        finally:
            if pump_task is not None and not pump_task.done():
                pump_task.cancel()
            if upstream_ws is not None and not upstream_ws.closed:
                await upstream_ws.close()
            if not ws.closed:
                await ws.close()
        return ws


@web.middleware
async def _encoding_guard(request: web.Request, handler):
    """Reject compressed request bodies explicitly, BEFORE the default decompressing reader runs.

    The launcher disables request compression (`features.enable_request_compression=false`), so any
    Content-Encoding here is unexpected and refused with a typed 415 rather than being auto-decoded
    or silently forwarded.
    """
    if request.method == "POST":
        encoding = (request.headers.get("Content-Encoding") or "").strip().lower()
        if encoding and encoding != "identity":
            cid = _new_correlation_id()
            request.app["front"].ledger_append_safe({
                "schema": "HGK-EXEC-FRONTDOOR-LEDGER/2", "ts": _now_iso(),
                "correlation_id": cid, "method": request.method,
                "path": _raw_request_target(request).split("?", 1)[0], "transport": "http",
                "decision": "REFUSE", "error_class": "ERR_EXEC_FRONTDOOR_CONTENT_ENCODING",
                "models": [], "upstream_status": None,
            })
            return web.json_response({
                "schema": "HGK-EXEC-FRONTDOOR-DECISION/2",
                "claim_ceiling": "CANDIDATE_ONLY",
                "decision": "REFUSE",
                "error_code": "ERR_EXEC_FRONTDOOR_CONTENT_ENCODING",
                "detail": f"content-encoding {encoding!r} is not accepted",
                "correlation_id": cid,
            }, status=415)
    return await handler(request)


def build_app(*, upstream: str, ledger: Ledger) -> web.Application:
    front = FrontDoor(upstream=upstream, ledger=ledger)
    app = web.Application(client_max_size=_MAX_BODY_BYTES, middlewares=[_encoding_guard],
                          # Disable aiohttp's own request decompression so a compressed body is a
                          # header check WE make (typed 415) rather than an opaque parser 400.
                          handler_args={"auto_decompress": False})
    app["front"] = front
    app.router.add_route("GET", "/healthz", front.healthz)
    app.router.add_route("GET", "/healthz/", front.healthz)
    app.router.add_route("*", "/{tail:.*}", front.handle)

    async def _on_cleanup(app_: web.Application) -> None:
        await front.close()
    app.on_cleanup.append(_on_cleanup)
    return app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hgk-exec-model-frontdoor.py", description=__doc__)
    parser.add_argument("--host", default=_DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=_DEFAULT_PORT)
    parser.add_argument("--upstream", default=_DEFAULT_UPSTREAM,
                        help="fixed loopback relay base URL; requests go to <upstream><path>")
    parser.add_argument("--declaration", default=None,
                        help="lane declaration (default: subject/config/hermes-codex-lane.json)")
    parser.add_argument("--pool", default=None,
                        help="lane-route pool artifact; when given, the allow-set is the union of the "
                             "selected lanes' declared, qualified and transport ids")
    parser.add_argument("--pool-lanes", default=None,
                        help="comma-separated lane scope for --pool (default: EXECUTE,VERIFY_SECURITY). "
                             "Scope one lane per instance so a door never forwards a sibling lane's arm")
    parser.add_argument("--ledger", default=None,
                        help="JSON-lines ledger (default: round _control/maker/frontdoor-ledger.jsonl)")
    return parser


def _is_loopback_host(host: str) -> bool:
    if host in _LOOPBACK:
        return True
    try:
        import ipaddress
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _is_loopback_url(url: str) -> bool:
    from urllib.parse import urlsplit
    parts = urlsplit(url)
    if parts.scheme not in ("http", "ws"):
        return False
    host = parts.hostname or ""
    return _is_loopback_host(host)


def serve(args: argparse.Namespace) -> int:
    host = str(args.host).strip()
    if not _is_loopback_host(host):
        return _fail_start("ERR_EXEC_FRONTDOOR_NON_LOOPBACK",
                           f"refusing to bind non-loopback host {host!r}")
    if not _is_loopback_url(str(args.upstream)):
        return _fail_start("ERR_EXEC_FRONTDOOR_NON_LOOPBACK_UPSTREAM",
                           f"refusing non-loopback upstream {args.upstream!r}")

    try:
        if args.pool:
            global _POOL_PATH, _ALLOWED_TOKENS, _POOL_LANES
            if args.pool_lanes:
                _POOL_LANES = tuple(x.strip() for x in str(args.pool_lanes).split(",") if x.strip())
                if not _POOL_LANES:
                    raise ValueError("ERR_EXEC_FRONTDOOR_POOL_MALFORMED: --pool-lanes resolved to nothing")
            _ALLOWED_TOKENS = load_pool_allowlist(args.pool, _POOL_LANES)
            _POOL_PATH = str(args.pool)
        sanctioned = load_sanctioned(args.declaration)
        validate_sanctioned_pair(sanctioned)
    except ValueError as exc:
        text = str(exc)
        if "SANCTIONED_DRIFT" in text:
            return _fail_start("ERR_EXEC_FRONTDOOR_SANCTIONED_DRIFT", text)
        if "POOL" in text:
            return _fail_start(text.partition(":")[0].strip(), text)
        return _fail_start("ERR_EXEC_FRONTDOOR_DECLARATION_INVALID", text)

    ledger = Ledger(Path(args.ledger) if args.ledger else _DEFAULT_LEDGER)
    app = build_app(upstream=str(args.upstream), ledger=ledger)
    sys.stderr.write(json.dumps({
        "schema": "HGK-EXEC-FRONTDOOR-START/1",
        "claim_ceiling": "CANDIDATE_ONLY",
        "listen": f"http://{host}:{args.port}",
        "upstream": str(args.upstream),
        "sanctioned_pair": _SANCTIONED_PAIR,
        "pool_path": _POOL_PATH,
        "allowlist_size": len(_ALLOWED_TOKENS),
        "declaration_sha256": hashlib.sha256(Path(sanctioned["path"]).read_bytes()).hexdigest(),
        "ledger": str(ledger.path),
    }) + "\n")
    sys.stderr.flush()
    web.run_app(app, host=host, port=args.port, print=None, handle_signals=True)
    return EXIT_OK


def main(argv: "list[str] | None" = None) -> int:
    return serve(build_parser().parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
