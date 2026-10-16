#!/usr/bin/env python
"""hgk-lane-guard.py — pre-dispatch conformance gate for the HG-KSEOS lane policy (CANDIDATE).

Given an intended lane, the maker engine+model, the target engine+model, and an admission status,
the guard refuses a dispatch unless:
  (a) the target (checker) model differs from the maker model            -> exit 2 (SoD)
  (b) the target arm is ADMITTED by a lane-shaped probe                  -> exit 3 (not admitted)
  (c) the policy epoch is current (not stale)                            -> exit 4 (stale epoch)

Precedence follows the enumeration (a) -> (b) -> (c). Exit 0 means ADMIT. A machine-readable
verdict is always printed; with --receipt PATH the same verdict is written to PATH.

EXECUTE-lane model allowlist enforcement (FAR-EXEC-IDENTITY-001, --enforce-model-allowlist)
refuses any model that is not exactly the single sanctioned id declared in
config/hermes-codex-lane.json. The sibling id `deepseek-flash` (bare or provider-prefixed) is an
explicit forbidden model. Typed exit codes, distinct per failure class, never a silent success:
  6  ERR_EXEC_MODEL_FORBIDDEN         the explicit forbidden sibling was requested
  7  ERR_EXEC_MODEL_NOT_SANCTIONED    a valid-but-unlisted model was requested
  8  ERR_EXEC_MODEL_MALFORMED         empty / whitespace / undecidable model token
  9  ERR_EXEC_MODEL_DECLARATION_INVALID  the lane declaration is unreadable or incomplete
 10  ERR_EXEC_MODEL_PROVIDER_MISMATCH a provider-prefixed model names a non-sanctioned provider

Everything is CANDIDATE. Read-only except the optional --receipt write.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_ROOT = _HERE.parent.parent


def _ensure_repo_src_on_path() -> Path:
    """Put the `hg_kseos` package's `src/` dir on sys.path.

    The module lives either at the repo root (`<root>/scripts/...`, so `<root>/src` is the package
    root) or inside a round subject (`<repo>/var/<round>/subject/scripts/...`, where no local `src`
    exists). Walk up from here to the nearest directory that actually contains `src/hg_kseos`, so the
    same file runs unchanged in both locations.
    """
    for base in (_ROOT, *_ROOT.parents):
        candidate = base / "src"
        if (candidate / "hg_kseos").is_dir():
            sys.path.insert(0, str(candidate))
            return candidate
    sys.path.insert(0, str(_ROOT / "src"))
    return _ROOT / "src"


_ensure_repo_src_on_path()

from hg_kseos import lane_policy as lp  # noqa: E402

EXIT_ADMIT = 0
EXIT_SOD = 2
EXIT_NOT_ADMITTED = 3
EXIT_STALE_EPOCH = 4
EXIT_USAGE = 5
# EXECUTE-lane model-allowlist failure classes (FAR-EXEC-IDENTITY-001), one per class.
EXIT_MODEL_FORBIDDEN = 6
EXIT_MODEL_NOT_SANCTIONED = 7
EXIT_MODEL_MALFORMED = 8
EXIT_MODEL_DECLARATION_INVALID = 9
EXIT_MODEL_PROVIDER_MISMATCH = 10

# The single global default for the lane declaration. The sanctioned (provider, model) is read
# from this file only; it is never hard-coded a second time.
_DEFAULT_DECLARATION = _ROOT / "config" / "hermes-codex-lane.json"
# The measured sibling: declared nowhere, enforced nowhere upstream, served by the relay anyway.
_FORBIDDEN_SIBLING = "deepseek-flash"


def _load_admission(path_or_status: str | None) -> tuple[str, dict | None]:
    """Return (status, record).

    A receipt FILE is the only admissible source of ADMITTED. A bare string is accepted only for
    UNPROVEN/REFUSED (fail-closed), because a self-declared ADMITTED with no probe evidence is
    exactly the trust-in-caller admission this gate exists to refuse (V3).
    """
    if not path_or_status:
        return "UNPROVEN", None
    candidate = Path(path_or_status)
    if candidate.exists() and candidate.is_file():
        data = json.loads(candidate.read_text(encoding="utf-8"))
        return str(data.get("status", "UNPROVEN")), data
    return path_or_status.strip().upper(), None


def _live_epoch(args, registry: dict) -> int | None:
    """Read the epoch from the live canonical source.

    V6: --expected-epoch is an assertion, never an override. The live value is always read from
    disk, so a caller who controls argv cannot force epoch_ok.
    """
    source = registry.get("source_of_routes", {}).get("path")
    if not source:
        return None
    source_path = (Path(args.root) / source) if args.root else (_ROOT / source)
    if not source_path.exists():
        return None
    try:
        doc = lp.load_site(source_path)
    except Exception:
        return None
    if isinstance(doc, dict) and "revision" in doc:
        return int(doc["revision"])
    return None


def _infer_maker_lane(registry: dict, maker_model: str | None) -> str | None:
    """Infer the maker lane from a model id, ONLY when exactly one route's default arm matches.

    The default arm is compared as `model` and as `provider/model` (both with and without the
    `provider/` prefix), exact case-insensitive string equality. An ambiguous match (more than one
    lane) or no match returns None, so the caller does NOT exempt — an unresolvable lane must fail
    closed, never widen the exemption.
    """
    if not maker_model:
        return None
    requested = str(maker_model).strip().lower()
    matches: set[str] = set()
    for route in registry.get("routes", []):
        provider = str(route.get("provider") or "").strip().lower()
        model = str(route.get("model") or "").strip().lower()
        forms = {model, f"{provider}/{model}" if provider else model}
        if requested in forms:
            matches.add(route.get("lane"))
    if len(matches) == 1:
        return next(iter(matches))
    return None


def evaluate(args) -> dict:
    registry_path = Path(args.registry) if args.registry else lp.DEFAULT_REGISTRY
    registry = lp.load_registry(registry_path)
    epoch = lp.registry_epoch(registry)

    checks: list[dict] = []
    errors: list[str] = []
    exit_code = EXIT_ADMIT
    status = "ADMIT"

    lane = args.lane
    known = lp.route_for_lane(registry, lane)
    if lane not in lp.LANE_ORDER:
        checks.append({"id": "lane_known", "ok": False, "code": "ERR_LANE_UNKNOWN_LANE",
                       "detail": f"lane {lane!r} is not in {list(lp.LANE_ORDER)}"})
        errors.append("ERR_LANE_UNKNOWN_LANE")
        exit_code = EXIT_NOT_ADMITTED
        status = "REFUSE"

    # (a) SoD: target/checker model must differ from the maker model.
    maker = {"engine": args.maker_engine, "model": args.maker_model}
    target = {"engine": args.target_engine, "model": args.target_model}
    sod_ok, sod_reason = lp.check_sod(maker["model"], target["model"])
    declared_conflict = None
    if not sod_ok:
        # A same-model pair may be EXEMPTED by an owner-ordered declaration in the registry. The
        # exemption is never silent: the resolved conflict id is carried on the verdict. The maker
        # lane comes from --maker-lane when given, else is inferred from --maker-model only when
        # exactly one route default arm matches; an unresolved lane fails closed (no exemption).
        maker_lane = args.maker_lane or _infer_maker_lane(registry, args.maker_model)
        checker_lane = args.lane if args.lane in lp.LANE_ORDER else None
        conflict_id, exempt_reason = lp.sod_declaration_exemption(registry, maker_lane, checker_lane)
        if conflict_id is not None:
            declared_conflict = conflict_id
            sod_ok = True
            sod_reason = f"{sod_reason}; EXEMPTED by declared conflict {conflict_id} (OWNER_ORDERED_IN_FORCE)"
        else:
            sod_reason = f"{sod_reason}; {exempt_reason}"
    sod_check = {"id": "sod_distinct_model", "ok": sod_ok,
                 "code": None if sod_ok else "ERR_LANE_SOD_VIOLATION", "detail": sod_reason}
    if declared_conflict is not None:
        sod_check["declared_conflict"] = declared_conflict
    checks.append(sod_check)
    if not sod_ok and exit_code == EXIT_ADMIT:
        errors.append("ERR_LANE_SOD_VIOLATION")
        exit_code = EXIT_SOD
        status = "REFUSE"

    # (c-pre) source digest binding: recorded registry source digest must match live bytes.
    recorded = registry.get("source_of_routes", {}).get("sha256")
    src_path = registry.get("source_of_routes", {}).get("path")
    if recorded and src_path:
        live_src = (Path(args.root) / src_path) if args.root else (_ROOT / src_path)
        if live_src.exists():
            live_digest = lp._sha256_file(live_src)
            digest_ok = (live_digest == recorded)
            checks.append({"id": "source_digest", "ok": digest_ok,
                           "code": None if digest_ok else "ERR_LANE_SOURCE_STALE",
                           "detail": f"recorded={recorded} live={live_digest}"})
            if not digest_ok and exit_code == EXIT_ADMIT:
                errors.append("ERR_LANE_SOURCE_STALE")
                exit_code = EXIT_STALE_EPOCH
                status = "REFUSE"
        else:
            # fail-closed: a pinned source that cannot be read on disk is stale, not exempt.
            checks.append({"id": "source_digest", "ok": False, "code": "ERR_LANE_SOURCE_STALE",
                           "detail": f"pinned source not readable: {live_src}"})
            if exit_code == EXIT_ADMIT:
                errors.append("ERR_LANE_SOURCE_STALE")
                exit_code = EXIT_STALE_EPOCH
                status = "REFUSE"

    # (b) admission: arm must be ADMITTED by a lane-shaped probe, and the probe must have served
    #     the same arm we are about to dispatch.
    admit_status, admit_record = _load_admission(args.admission)
    admission_ok = admit_status == "ADMITTED"
    admit_detail = f"status={admit_status}"
    if admission_ok and admit_record is None:
        admission_ok = False
        admit_detail += " evidence=ABSENT (a bare ADMITTED string is not admissible; pass a probe receipt)"
    if admission_ok and admit_record:
        served = admit_record.get("served", {}) or {}
        rec_arm = admit_record.get("arm", {}) or {}
        # V4: the provider dimension is reconciled unconditionally. Omission of --target-provider is
        # not a wildcard: if either side fails to declare a provider, admission fails closed.
        rec_provider = rec_arm.get("provider")
        provider_ok = bool(rec_provider) and (rec_provider == args.target_provider)
        arm_matches = (
            lp.normalize_model(rec_arm.get("model", "")) == lp.normalize_model(target["model"])
            and provider_ok
            and lp.normalize_model(served.get("model", "")) == lp.normalize_model(target["model"])
        )
        admission_ok = arm_matches
        admit_detail += (f" arm_match={arm_matches} requested={rec_arm.get('model')}"
                         f" requested_provider={rec_provider} served={served.get('model')}"
                         f" target_provider={args.target_provider}")
    checks.append({"id": "arm_admitted", "ok": admission_ok,
                   "code": None if admission_ok else "ERR_LANE_NOT_ADMITTED", "detail": admit_detail})
    if not admission_ok and exit_code == EXIT_ADMIT:
        errors.append("ERR_LANE_NOT_ADMITTED")
        exit_code = EXIT_NOT_ADMITTED
        status = "REFUSE"

    # (c) epoch current. --expected-epoch, when supplied, is an additional assertion and never a
    # replacement for the live read (V6).
    live_epoch = _live_epoch(args, registry)
    epoch_ok = (live_epoch is None) or (int(live_epoch) == int(epoch))
    if args.expected_epoch is not None:
        expect_ok = (live_epoch is not None) and int(live_epoch) == int(args.expected_epoch)
        checks.append({"id": "expected_epoch_assertion", "ok": expect_ok,
                       "code": None if expect_ok else "ERR_LANE_STALE_EPOCH",
                       "detail": f"--expected-epoch={args.expected_epoch} live_epoch={live_epoch}"})
        epoch_ok = epoch_ok and expect_ok
    checks.append({"id": "epoch_current", "ok": epoch_ok,
                   "code": None if epoch_ok else "ERR_LANE_STALE_EPOCH",
                   "detail": f"registry_epoch={epoch} live_epoch={live_epoch}"})
    if not epoch_ok and exit_code == EXIT_ADMIT:
        errors.append("ERR_LANE_STALE_EPOCH")
        exit_code = EXIT_STALE_EPOCH
        status = "REFUSE"

    if args.lane not in lp.LANE_ORDER and exit_code == EXIT_ADMIT:
        exit_code = EXIT_NOT_ADMITTED
        status = "REFUSE"

    verdict = {
        "schema": "HGK-LANE-GUARD/1",
        "claim_ceiling": "CANDIDATE_ONLY",
        "status": status,
        "exit_code": exit_code,
        "lane": lane,
        "epoch": epoch,
        "live_epoch": live_epoch,
        "maker": maker,
        "target": {**target, "provider": args.target_provider},
        "admission_status": admit_status,
        "checks": checks,
        "errors": errors,
        "decision": "ADMIT" if exit_code == EXIT_ADMIT else "REFUSE",
    }
    if declared_conflict is not None:
        verdict["declared_conflict"] = declared_conflict
    return verdict


def load_lane_declaration(path: "str | Path | None" = None) -> dict:
    """Read the sanctioned (provider, model) from the lane declaration.

    This is the sole source of the sanctioned id; nothing else in this file re-states it. A missing
    file, a non-object body, or an empty provider/model is a declaration-invalid condition (fail
    closed) rather than a wildcard.
    """
    declaration_path = Path(path) if path else _DEFAULT_DECLARATION
    try:
        doc = json.loads(declaration_path.read_text(encoding="utf-8"))
    except Exception as exc:  # missing, unreadable, or non-JSON
        raise ValueError(f"ERR_EXEC_MODEL_DECLARATION_INVALID: cannot read {declaration_path}: "
                         f"{type(exc).__name__}") from exc
    if not isinstance(doc, dict):
        raise ValueError("ERR_EXEC_MODEL_DECLARATION_INVALID: declaration is not a JSON object")
    provider = str(doc.get("provider") or "").strip()
    model = str(doc.get("model") or "").strip()
    if not provider or not model:
        raise ValueError("ERR_EXEC_MODEL_DECLARATION_INVALID: provider/model missing or empty")
    return {"provider": provider, "model": model, "path": str(declaration_path)}


def _sanctioned_token(model: str) -> str:
    """Comparison token for a model id: lowercase, whitespace collapsed, provider prefix dropped."""
    token = str(model).strip().lower()
    if "/" in token:
        token = token.rsplit("/", 1)[-1]
    return token.strip()


def evaluate_exec_model_allowlist(
    *,
    model: "str | None",
    declaration_path: "str | Path | None" = None,
    provider: "str | None" = None,
) -> dict:
    """Enforce the EXECUTE-lane single-model allowlist and return a typed verdict.

    Resolution rules:
      * `model` omitted/null -> resolve the sanctioned model from the declaration and report it.
      * a bare id (`deepseek-v4.1-flash`) and a provider-prefixed id (`opencode-go/deepseek-v4.1-flash`)
        are the same request and both normalise to the same token.
      * the forbidden sibling `deepseek-flash` is refused explicitly, bare or prefixed, in any case.
      * any empty / whitespace-only / otherwise undecidable token is refused as malformed.

    Never returns a silent success: the verdict always carries a typed `error_code` (None only on
    ADMIT) and a distinct `exit_code`.
    """
    try:
        declared = load_lane_declaration(declaration_path)
    except ValueError as exc:
        return {
            "schema": "HGK-EXEC-MODEL-ALLOWLIST/1",
            "claim_ceiling": "CANDIDATE_ONLY",
            "status": "REFUSE",
            "decision": "REFUSE",
            "exit_code": EXIT_MODEL_DECLARATION_INVALID,
            "error_code": "ERR_EXEC_MODEL_DECLARATION_INVALID",
            "requested_model": model,
            "resolved_model": None,
            "detail": str(exc),
        }

    sanctioned_provider = declared["provider"]
    sanctioned_model = declared["model"]
    sanctioned_token = _sanctioned_token(sanctioned_model)
    forbidden_token = _sanctioned_token(_FORBIDDEN_SIBLING)

    def verdict(status, exit_code, error_code, requested, resolved, detail):
        return {
            "schema": "HGK-EXEC-MODEL-ALLOWLIST/1",
            "claim_ceiling": "CANDIDATE_ONLY",
            "status": status,
            "decision": status,
            "exit_code": exit_code,
            "error_code": error_code,
            "lane": "EXECUTE",
            "sanctioned": {"provider": sanctioned_provider, "model": sanctioned_model},
            "declaration": declared["path"],
            "requested_model": requested,
            "resolved_model": resolved,
            "forbidden_sibling": _FORBIDDEN_SIBLING,
            "detail": detail,
        }

    # Resolution: --model omitted (None) -> resolve from the declaration. An explicitly supplied
    # empty/whitespace token is NOT "omitted": it is a malformed request and must be refused.
    resolved_from_declaration = model is None
    raw_model = sanctioned_model if resolved_from_declaration else str(model)

    token = _sanctioned_token(raw_model)
    if not token:
        return verdict("REFUSE", EXIT_MODEL_MALFORMED, "ERR_EXEC_MODEL_MALFORMED",
                       model, None, "empty/whitespace-only model token")

    # Explicit forbidden sibling, bare or provider-prefixed, any case.
    if token == forbidden_token:
        return verdict("REFUSE", EXIT_MODEL_FORBIDDEN, "ERR_EXEC_MODEL_FORBIDDEN",
                       model, raw_model,
                       f"forbidden sibling model {_FORBIDDEN_SIBLING!r} (bare or provider-prefixed)")

    # Provider dimension: a prefix, when present, must name the sanctioned provider.
    requested_provider = None
    if "/" in str(raw_model).strip():
        requested_provider = str(raw_model).strip().split("/", 1)[0].strip().lower()
    if requested_provider is not None and provider is None and requested_provider != sanctioned_provider.lower():
        return verdict("REFUSE", EXIT_MODEL_PROVIDER_MISMATCH, "ERR_EXEC_MODEL_PROVIDER_MISMATCH",
                       model, raw_model,
                       f"provider {requested_provider!r} != sanctioned provider {sanctioned_provider!r}")
    if provider is not None and str(provider).strip().lower() != sanctioned_provider.lower():
        return verdict("REFUSE", EXIT_MODEL_PROVIDER_MISMATCH, "ERR_EXEC_MODEL_PROVIDER_MISMATCH",
                       model, raw_model,
                       f"provider {provider!r} != sanctioned provider {sanctioned_provider!r}")

    # Prefix collision guard: `deepseek-v4.1-flash` must not be accepted as `deepseek-flash` and
    # vice-versa. Exact token equality is the only ADMIT path.
    if token != sanctioned_token:
        return verdict("REFUSE", EXIT_MODEL_NOT_SANCTIONED, "ERR_EXEC_MODEL_NOT_SANCTIONED",
                       model, raw_model,
                       f"model {token!r} != sanctioned {sanctioned_token!r}")

    return verdict("ADMIT", EXIT_ADMIT, None, model, raw_model,
                   f"model {token!r} is the single sanctioned EXECUTE-lane model")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hgk-lane-guard.py", description=__doc__)
    parser.add_argument("--lane", required=False,
                        help="intended lane: PLAN | EXECUTE | VERIFY_SECURITY")
    parser.add_argument("--maker-lane", default=None,
                        choices=list(lp.LANE_ORDER),
                        help="maker lane (PLAN|EXECUTE|VERIFY_SECURITY); lets the SoD check consult "
                             "the registry's declared owner-ordered exemption. Omit to infer from "
                             "--maker-model, which only resolves when exactly one lane matches.")
    parser.add_argument("--maker-engine", required=False)
    parser.add_argument("--maker-model", required=False)
    parser.add_argument("--target-engine", required=False)
    parser.add_argument("--target-model", required=False)
    parser.add_argument("--target-provider", default=None)
    parser.add_argument("--admission", default=None,
                        help="ADMITTED/REFUSED/UNPROVEN, or a path to an admission receipt")
    parser.add_argument("--expected-epoch", type=int, default=None,
                        help="live/admitted epoch; default: read from the canonical policy revision")
    parser.add_argument("--registry", default=None)
    parser.add_argument("--root", default=None)
    parser.add_argument("--receipt", default=None, help="write the verdict JSON to this path")
    # EXECUTE-lane model-allowlist mode (FAR-EXEC-IDENTITY-001).
    parser.add_argument("--enforce-model-allowlist", action="store_true",
                        help="enforce the single sanctioned EXECUTE-lane model allowlist")
    parser.add_argument("--model", default=None,
                        help="model to check; when omitted, resolve from the lane declaration")
    parser.add_argument("--provider", default=None,
                        help="optional provider assertion for the model under check")
    parser.add_argument("--declaration", default=None,
                        help="path to the lane declaration (default: config/hermes-codex-lane.json)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.enforce_model_allowlist:
        verdict = evaluate_exec_model_allowlist(
            model=args.model,
            declaration_path=args.declaration,
            provider=args.provider,
        )
    else:
        # Legacy pre-dispatch mode: the lane-SoD arguments are mandatory here.
        missing = [name for name in ("lane", "maker_engine", "maker_model",
                                     "target_engine", "target_model")
                   if not getattr(args, name)]
        if missing:
            parser = build_parser()
            parser.error("legacy mode requires: " + ", ".join("--" + m.replace("_", "-")
                                                              for m in missing))
        verdict = evaluate(args)
    text = json.dumps(verdict, ensure_ascii=False, indent=2, sort_keys=True)
    print(text)
    if args.receipt:
        target = Path(args.receipt)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text + "\n", encoding="utf-8", newline="\n")
    return verdict["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
