#!/usr/bin/env python3
"""Named assertions for the GCM containment preflight.

Round ``HGK-GCM-REPAIR-20261013``. The old ``classify()`` produced a single
whole-path verdict, and two inputs wrongly came back ``PASS`` (see
``tests/test_credential_preflight.py`` and ``$R/execute/Y2_REPORT.md``). This
module replaces that with a set of NAMED assertions, each independently
reported as ``PASS`` / ``FAIL`` / ``UNKNOWN`` with its own reason and evidence.

Rules encoded here (from the repair brief):

* ``UNKNOWN`` is never a pass. It is a first-class outcome, and it rolls up to
  ``INCONCLUSIVE`` (exit 2), never to ``PASS``.
* A vacuous pass is a defect. An assertion whose input is missing or empty does
  NOT return ``PASS``; it returns ``UNKNOWN``.
* ``--no-ui`` disables the GUI only. On its own it is NOT "nothing can prompt"
  and may never make ``helper_non_interactive`` pass.
* ``GIT_TERMINAL_PROMPT=0`` closes git's terminal prompt only; git tries an
  askpass program BEFORE it honours that setting, so askpass is asserted
  separately and an unvetted executable askpass is never a pass.
* The EFFECTIVE ``credential.interactive`` / ``GCM_INTERACTIVE`` value is
  resolved with git's precedence (later / higher scope wins); a lower-precedence
  disabling value does NOT prove non-interaction when a higher-precedence value
  re-enables it, and contradictory or unordered inputs are never a proof.
* A prompt-capable helper is accepted only on POSITIVE identity of its resolved
  program (installed path / digest allow-list). A basename or family name alone
  is not identity, and GCM-style settings do not cover an unvetted program.
* A FAILED config read is never treated as proven absence; it makes the
  dependent assertion UNKNOWN, which rolls up to INCONCLUSIVE.

Every function here is PURE: it takes already-read configuration and an
environment mapping, and returns a small dict. No git process, no network, no
credential access, no writes.
"""
from __future__ import annotations

import hashlib
import os
import shutil

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"

#: Overall verdict values (kept identical to ``credential_preflight``).
INCONCLUSIVE = "INCONCLUSIVE"

#: Helper families known, from their own documentation, to be able to interact
#: with the user (GUI, device-code, console, or browser). Presence of one of
#: these WITHOUT a documented interaction-disabling setting is a FAIL.
#:
#: Source actually read on this host (2026-10-13):
#:   * ``git-credential-manager.exe --help`` -> ``--no-ui  Do not use graphical
#:     user interface prompts`` (GUI only, not all prompting).
#:   * ``gcmcore.dll`` string table contains ``GCM_INTERACTIVE`` /
#:     ``interactive`` / ``never`` and also ``GIT_TERMINAL_PROMPT``.
PROMPT_CAPABLE_FAMILIES = (
    "manager",
    "git-credential-manager",
    "git-credential-manager-core",
    "gh",
    "github",
    "osxkeychain",
)

#: Values that, as the WHOLE helper value, are provably non-interactive
#: (git's documented no-op helper).
NON_INTERACTIVE_HELPER_VALUES = ("-",)

#: Values of ``credential.interactive`` / ``GCM_INTERACTIVE`` that disable
#: interaction. ``--no-ui`` is deliberately ABSENT: it disables the GUI only.
#: ``never`` is the value read out of the GCM binary's option table; the boolean
#: forms are the ones git accepts for ``credential.interactive``.
INTERACTION_DISABLED_VALUES = ("false", "never", "0", "off", "no")

#: Values that positively (re-)ENABLE interaction. Used only to resolve the
#: EFFECTIVE value by precedence: a higher-precedence enabling value must not be
#: masked by a lower-precedence disabling value (round-2 defect D1).
INTERACTION_ENABLED_VALUES = ("true", "always", "1", "on", "yes", "auto", "prompt")

#: git scope precedence (increasing). ``git config --get-all`` prints low ->
#: high, so a reset clears everything printed before it.
SCOPE_RANK = {"system": 0, "global": 1, "local": 2, "worktree": 3, "command": 4}


def _r(name, status, reason, evidence=None):
    return {"name": name, "status": status, "reason": reason, "evidence": evidence or {}}


def _rank(scope):
    if scope is None:
        return None
    return SCOPE_RANK.get(str(scope).strip().lower())


def _split_helper_value(value):
    """Split a helper value into tokens, honouring a double-quoted first token.

    A program path that contains spaces must be quoted (gitcredentials(7)), e.g.
    ``"C:/Program Files/Git/git-credential-manager.exe" --no-ui``.
    """
    text = str(value).strip()
    if text.startswith('"'):
        end = text.find('"', 1)
        if end != -1:
            first = text[1:end]
            rest = text[end + 1:].split()
            return [first] + rest
    return text.split()


def _first_token_base(value):
    parts = _split_helper_value(value)
    if not parts:
        return ""
    first = parts[0]
    base = first.replace("\\", "/").rsplit("/", 1)[-1]
    if base.lower().endswith(".exe"):
        base = base[:-4]
    return base.lower()


def surviving_helpers(helpers):
    """Replay git's accumulate/reset rule and return the helpers consulted last.

    A non-empty value APPENDS a helper; an EMPTY value RESETS the accumulated
    list (``gitcredentials(7)``). Only the helpers that survive to the end are
    actually consulted.
    """
    accumulated = []
    for h in helpers or []:
        if str(h.get("value", "")).strip() == "":
            accumulated = []
        else:
            accumulated.append(h)
    return accumulated


def _interaction_kind(value):
    """Classify a single interaction value: ``disabled`` / ``enabled`` / ``None``."""
    v = str(value).strip().lower()
    if v in INTERACTION_DISABLED_VALUES:
        return "disabled"
    if v in INTERACTION_ENABLED_VALUES:
        return "enabled"
    return None


def resolve_interaction_effective(interactive):
    """Resolve the EFFECTIVE ``credential.interactive`` value by git precedence.

    Returns ``{"kind": "disabled"|"enabled"|"unknown", "rank": int|None,
    "reason": str}``. ``unknown`` covers a missing setting, an unrankable scope
    (precedence cannot be ordered), conflicting values that share the deciding
    scope, and a deciding value that is not a recognised interaction value. An
    ``unknown`` result is NEVER a proof of non-interaction (round-2 defect D1).
    """
    entries = []
    for item in interactive or []:
        entries.append((_rank(item.get("scope")), _interaction_kind(item.get("value", ""))))
    if not entries:
        return {"kind": "unknown", "rank": None,
                "reason": "no credential.interactive entries were read"}
    if any(rank is None for rank, _ in entries):
        return {"kind": "unknown", "rank": None,
                "reason": "an entry has an unrankable scope; precedence cannot be resolved"}
    top = max(rank for rank, _ in entries)
    top_kinds = {kind for rank, kind in entries if rank == top}
    if len(top_kinds) > 1:
        return {"kind": "unknown", "rank": top,
                "reason": "conflicting interaction values share the deciding scope"}
    kind = top_kinds.pop()
    if kind is None:
        return {"kind": "unknown", "rank": top,
                "reason": "the deciding interaction value is not a recognised value"}
    return {"kind": kind, "rank": top,
            "reason": "effective %s value at scope rank %d" % (kind, top)}


def interaction_disabled_for(helper_scope, interactive):
    """True if a documented interaction-disabling setting governs this helper.

    ``interactive`` is a list of ``{"scope","value","origin"}`` read from the
    EFFECTIVE config. GCM reads ``credential.interactive`` from its own
    effective config regardless of which scope declared the helper, so a setting
    at the helper's scope or a HIGHER-precedence scope governs it. When a scope
    cannot be determined the setting is accepted conservatively (a lower-
    precedence setting can only help, never hurt); the helper itself is still
    only a PASS when a prompt-capable family is positively covered.

    The EFFECTIVE value is first resolved with git's precedence (later / higher
    scope wins). Contradictory or unordered inputs, or a higher-precedence
    re-enabling value, are NEVER a proof of non-interaction (round-2 defect D1).
    """
    effective = resolve_interaction_effective(interactive)
    if effective["kind"] != "disabled":
        return False
    hrank = _rank(helper_scope)
    if hrank is None:
        return True
    if effective["rank"] is None or effective["rank"] >= hrank:
        return True
    return False


# --------------------------------------------------------------------------- #
# positive identity of the resolved helper program (round-2 defect D2)
# --------------------------------------------------------------------------- #

def _normpath(path):
    try:
        return os.path.normcase(os.path.realpath(str(path)))
    except OSError:
        return os.path.normcase(str(path))


def _sha256_file(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def host_helper_allowlist():
    """Paths + digests of the known non-prompting credential helpers on THIS host.

    Low-resistance and built from what is actually installed (round-2 defect D2):
    the digest is a second acceptance path so a relocated but unchanged binary is
    still positively identified, while a same-named binary elsewhere is not.
    """
    allow = {"paths": set(), "digests": set()}
    for name in ("git-credential-manager", "git-credential-manager.exe"):
        found = shutil.which(name)
        if found:
            allow["paths"].add(_normpath(found))
            digest = _sha256_file(found)
            if digest:
                allow["digests"].add(digest)
    return allow


def resolve_helper_program(value, which=shutil.which):
    """Resolve the program a helper value actually runs (or ``None``).

    Mirrors git's own rule (``gitcredentials(7)``): if the first token carries a
    path separator it is used as-is; otherwise git runs ``git-credential-<name>``
    from PATH. Shell helpers (``!cmd``) are not a fixed program and never resolve.
    """
    parts = _split_helper_value(value)
    if not parts:
        return None
    prog = parts[0]
    if prog.startswith("!"):
        return None
    if "/" in prog or "\\" in prog:
        return prog
    for candidate in ("git-credential-" + prog, prog):
        found = which(candidate)
        if found:
            return found
    return None


def program_allowlisted(resolved, allow):
    """True only when the resolved program is positively identified."""
    if not resolved:
        return False
    if _normpath(resolved) in (allow or {}).get("paths", set()):
        return True
    digest = _sha256_file(resolved)
    return bool(digest) and digest in (allow or {}).get("digests", set())


# --------------------------------------------------------------------------- #
# named assertions
# --------------------------------------------------------------------------- #

def assert_helper_resolution_reset(helpers):
    """An empty-string reset exists at or above the system helper."""
    name = "helper_resolution_reset"
    resets = [h for h in helpers or [] if str(h.get("value", "")).strip() == ""]
    if resets:
        origins = sorted({h.get("origin") or "?" for h in resets})
        return _r(
            name, PASS,
            "an empty-string helper reset is present in the effective resolution "
            "(gitcredentials(7): a reset discards every lower-precedence helper "
            "accumulated so far, including the system-scope handler)",
            {"reset_origins": origins, "reset_count": len(resets)},
        )
    return _r(
        name, UNKNOWN,
        "no empty-string helper reset is present; without a reset the "
        "lower-precedence helpers (e.g. a system-scope 'manager') cannot be "
        "proven cleared, so this is NOT a pass",
        {"reset_count": 0},
    )


def assert_helper_non_interactive(helpers, interactive=None, env=None, allow=None,
                                  which=None, interactive_read_ok=True):
    """Every SURVIVING helper is provably non-interactive.

    A helper is provably non-interactive only when it is git's documented no-op
    helper, or its RESOLVED executable is positively identified (installed path
    / digest allow-list) as a known non-prompting program AND a documented
    interaction-disabling setting (``credential.interactive`` /
    ``GCM_INTERACTIVE``) governs it. ``--no-ui`` alone is insufficient, and a
    basename / family name alone is NOT identity: an unvetted executable is
    FAIL (round-2 defect D2). Any helper form that cannot be positively
    classified is ``UNKNOWN``.

    The interaction setting is resolved with git's precedence (later / higher
    scope wins); a higher-precedence re-enable, contradictory values, or an
    unordered scope are NEVER a proof of non-interaction (round-2 defect D1).
    """
    name = "helper_non_interactive"
    survivors = surviving_helpers(helpers)
    if not survivors:
        # Vacuous-pass ban: the reset left nothing to consult. That is not a
        # proof that nothing can prompt (git's own askpass/terminal paths are
        # separate), so the assertion is UNKNOWN, never PASS.
        return _r(
            name, UNKNOWN,
            "after replaying git's accumulate/reset rule no helper survives; "
            "there is no evidence to make this assertion pass (an empty helper "
            "list is not a proof that nothing can prompt)",
            {"surviving_helpers": []},
        )

    which = which or shutil.which
    allow = allow if allow is not None else host_helper_allowlist()
    env = env or {}
    gcm_env_kind = _interaction_kind(env.get("GCM_INTERACTIVE", ""))

    if not interactive_read_ok and gcm_env_kind is None:
        # The credential.interactive read FAILED, so its content is missing
        # input, not proven absence. We cannot positively classify a
        # prompt-capable helper as non-interactive; that is UNKNOWN, never PASS.
        return _r(
            name, UNKNOWN,
            "the credential.interactive config read FAILED, so the effective "
            "interaction setting is NOT proven (missing / unreadable input is "
            "never absence)",
            {"interactive_read_ok": False,
             "surviving_helpers": [str(h.get("value", "")).strip() for h in survivors]},
        )

    per_helper = []
    for h in survivors:
        value = str(h.get("value", "")).strip()
        base = _first_token_base(value)
        annotated = h.get("interaction_disabled") is True
        if gcm_env_kind == "enabled":
            # A positive env re-enable wins over any config disabling value.
            setting_disabled = False
        elif gcm_env_kind == "disabled":
            setting_disabled = True
        else:
            setting_disabled = interaction_disabled_for(h.get("scope"), interactive)
        if annotated and gcm_env_kind != "enabled":
            # An annotation from an earlier effective read may only help when it
            # does not contradict a positive env re-enable.
            setting_disabled = True

        if value in NON_INTERACTIVE_HELPER_VALUES:
            per_helper.append((PASS, value, "git's documented no-op helper"))
            continue

        resolved = resolve_helper_program(value, which=which)
        identity_ok = program_allowlisted(resolved, allow)

        if base in PROMPT_CAPABLE_FAMILIES:
            if not identity_ok:
                per_helper.append(
                    (FAIL, value,
                     "prompt-capable family whose resolved executable is NOT "
                     "positively identified (basename / family alone is not "
                     "identity); an unvetted executable is never provably "
                     "non-interactive, and GCM-style settings do not cover it")
                )
            elif setting_disabled:
                per_helper.append(
                    (PASS, value,
                     "positively-identified non-prompting program with interaction "
                     "disabled by a documented credential.interactive / "
                     "GCM_INTERACTIVE setting")
                )
            else:
                per_helper.append(
                    (FAIL, value,
                     "prompt-capable family with NO documented interaction-disabling "
                     "setting; '--no-ui' disables the GUI only and does NOT disable all "
                     "prompting (device-code / console remain)")
                )
        else:
            per_helper.append(
                (UNKNOWN, value,
                 "not a helper form this checker can positively classify as "
                 "non-interactive (or prompt-capable)")
            )

    statuses = [s for s, _, _ in per_helper]
    if FAIL in statuses:
        worst = FAIL
    elif UNKNOWN in statuses:
        worst = UNKNOWN
    else:
        worst = PASS

    detail = "; ".join("%r: %s" % (v, why) for _, v, why in per_helper)
    return _r(
        name, worst,
        "surviving helpers and their classification -> " + detail,
        {"per_helper": [{"value": v, "status": s, "why": why}
                        for s, v, why in per_helper]},
    )


def assert_askpass_not_prompting(env=None, askpass_config=None, askpass_read_ok=True):
    """GIT_ASKPASS, core.askPass, SSH_ASKPASS are absent or provably safe.

    An unvetted executable askpass is NEVER a pass: git invokes the askpass
    program before it honours ``GIT_TERMINAL_PROMPT``.

    A FAILED ``core.askPass`` read is NOT proven absence: when
    ``askpass_read_ok`` is false, missing config is missing input, so the
    assertion is UNKNOWN (round-2 defect D3). Missing input is never absence.
    """
    name = "askpass_not_prompting"
    env = env or {}
    hits = []
    for key in ("GIT_ASKPASS", "SSH_ASKPASS"):
        value = env.get(key)
        if value is not None and str(value).strip() != "":
            hits.append((key, str(value)))
    for item in askpass_config or []:
        value = str(item.get("value", "")).strip()
        if value != "":
            hits.append(("core.askPass", value))
    if not askpass_read_ok:
        return _r(
            name, UNKNOWN,
            "the core.askPass config read FAILED, so the absence of an askpass "
            "program is NOT proven (missing / unreadable input is never absence); "
            "env askpass hits seen: " + (", ".join(k for k, _ in hits) or "none"),
            {"askpass_read_ok": False,
             "askpass": [{"key": k, "value": v} for k, v in hits]},
        )
    if not hits:
        return _r(
            name, PASS,
            "GIT_ASKPASS, SSH_ASKPASS and core.askPass are all absent or empty in "
            "the evaluated context",
        )
    names = ", ".join(k for k, _ in hits)
    return _r(
        name, UNKNOWN,
        "an askpass program is configured (" + names + "); an unvetted executable "
        "askpass is never provably non-interactive, and git tries askpass before "
        "honouring GIT_TERMINAL_PROMPT, so this is NOT a pass",
        {"askpass": [{"key": k, "value": v} for k, v in hits]},
    )


def assert_terminal_prompt_disabled(env=None):
    """The intended CHILD environment sets GIT_TERMINAL_PROMPT=0.

    This alone does NOT cover askpass (git tries askpass first).
    """
    name = "terminal_prompt_disabled"
    value = str((env or {}).get("GIT_TERMINAL_PROMPT", "")).strip()
    if value == "0":
        return _r(
            name, PASS,
            "the intended CHILD environment sets GIT_TERMINAL_PROMPT=0. This closes "
            "git's own TERMINAL prompt only; it does NOT cover askpass, which git "
            "tries before honouring this setting",
            {"GIT_TERMINAL_PROMPT": "0"},
        )
    return _r(
        name, FAIL,
        "GIT_TERMINAL_PROMPT is %r, not '0'; git may fall back to a terminal prompt"
        % value,
        {"GIT_TERMINAL_PROMPT": value},
    )


def assert_no_config_override(env=None, config_params=None):
    """No CHILD-context override silently reinstates a prompt-capable helper."""
    name = "no_config_override"
    env = env or {}
    hits = []
    for key in ("GIT_CONFIG_SYSTEM", "GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM",
                "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"):
        if key in env:
            hits.append((key, str(env[key])))
    for key in env:
        if key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_"):
            hits.append((key, str(env[key])))
    for param in config_params or []:
        low = str(param).strip().lower()
        if "credential.helper" in low:
            hits.append(("-c", str(param)))
    if not hits:
        return _r(
            name, PASS,
            "no GIT_CONFIG_* environment override and no '-c credential.helper' "
            "config parameter is present in the child context",
        )
    return _r(
        name, FAIL,
        "the child context carries configuration overrides that can silently "
        "reinstate a prompt-capable helper: " + ", ".join(k for k, _ in hits),
        {"overrides": [{"key": k, "value": v} for k, v in hits]},
    )


def roll_up(assertions):
    """Overall verdict from named assertions: PASS only if every one is PASS."""
    statuses = [a.get("status") for a in assertions or []]
    if not statuses:
        return INCONCLUSIVE
    if all(s == PASS for s in statuses):
        return PASS
    if any(s == FAIL for s in statuses):
        return FAIL
    return INCONCLUSIVE


def run_assertions(helpers, interactive=None, env=None, askpass_config=None,
                   config_params=None, askpass_read_ok=True, interactive_read_ok=True,
                   allow=None, which=None):
    """Run every named assertion and roll them up into one verdict."""
    items = [
        assert_helper_resolution_reset(helpers),
        assert_helper_non_interactive(helpers, interactive, env, allow=allow,
                                      which=which, interactive_read_ok=interactive_read_ok),
        assert_askpass_not_prompting(env, askpass_config, askpass_read_ok=askpass_read_ok),
        assert_terminal_prompt_disabled(env),
        assert_no_config_override(env, config_params),
    ]
    return {"assertions": items, "verdict": roll_up(items)}


def run_helper_assertions(helpers, interactive=None, env=None, allow=None, which=None,
                          interactive_read_ok=True):
    """Run only the helper-resolution assertions (backward-compatible path).

    Used by the legacy ``classify(entries)`` contract, which has no environment
    to assert askpass / terminal / override against.
    """
    items = [
        assert_helper_resolution_reset(helpers),
        assert_helper_non_interactive(helpers, interactive, env, allow=allow,
                                      which=which, interactive_read_ok=interactive_read_ok),
    ]
    return {"assertions": items, "verdict": roll_up(items)}

