#!/usr/bin/env python3
"""Tests for the repaired GCM containment preflight (round HGK-GCM-REPAIR-20261013).

Runnable with the host python + pytest:

    C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m pytest \
        scripts/gcm-containment/tests/test_credential_preflight.py -v

Every case runs against SCRATCH config files and PURE functions. No live
credential probe, no git fetch/pull/push, no cmdkey, no live host resolution used
as a fixture. The end-to-end case redirects git's global scope with
``--test-global`` (a temporary file) and never touches the real ~/.gitconfig.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GCM_DIR = HERE.parent

# Load the two modules as the preflight itself loads them (sibling import works
# because GCM_DIR is on sys.path).
sys.path.insert(0, str(GCM_DIR))
if str(GCM_DIR) not in sys.path:
    sys.path.append(str(GCM_DIR))

import assertions as A  # noqa: E402
import credential_preflight as CP  # noqa: E402

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
INCONCLUSIVE = "INCONCLUSIVE"


def child_env(**extra):
    """A scrubbed CHILD environment: no GIT_CONFIG_*, no askpass, prompt off."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_CONFIG_") and k not in ("GIT_ASKPASS", "SSH_ASKPASS")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.update(extra)
    return env


def whole_path(helpers, interactive=None, env=None, askpass_config=None,
               config_params=None):
    """Overall verdict for one context (uses the CHILD-attributed pure function)."""
    return CP.evaluate_context(
        env=env if env is not None else child_env(),
        cwd=None, helpers=helpers, interactive=interactive,
        askpass_config=askpass_config, config_params=config_params,
    )


def status_of(section, name):
    for a in section["assertions"]:
        if a["name"] == name:
            return a["status"]
    raise KeyError(name)


# --------------------------------------------------------------------------- #
# required cases 1-6 (pure)
# --------------------------------------------------------------------------- #

def test_01_reset_only_is_not_whole_path_pass():
    """Case 1: reset-only may NOT be a whole-path PASS."""
    section = whole_path([{"origin": "sys", "scope": "system", "value": ""}])
    assert section["verdict"] != PASS
    assert section["verdict"] == INCONCLUSIVE
    # the reset itself is present...
    assert status_of(section, "helper_resolution_reset") == PASS
    #...but nothing survives, so non-interactive cannot be proven.
    assert status_of(section, "helper_non_interactive") == UNKNOWN


def test_02_reset_plus_manager_no_ui_is_not_whole_path_pass():
    """Case 2: reset + 'manager --no-ui' only may NOT be a whole-path PASS."""
    section = whole_path([
        {"origin": "sys", "scope": "system", "value": ""},
        {"origin": "user", "scope": "global", "value": "manager --no-ui"},
    ])
    assert section["verdict"] != PASS
    assert section["verdict"] == FAIL
    assert status_of(section, "helper_resolution_reset") == PASS
    assert status_of(section, "helper_non_interactive") == FAIL


def test_03_unknown_helper_form_is_unknown_not_pass():
    """Case 3: an unknown helper form is UNKNOWN, never PASS."""
    section = whole_path([
        {"origin": "sys", "scope": "system", "value": ""},
        {"origin": "user", "scope": "global", "value": "my-custom-helper --xyzzy"},
    ])
    assert section["verdict"] != PASS
    assert section["verdict"] == INCONCLUSIVE
    assert status_of(section, "helper_non_interactive") == UNKNOWN


def test_04_unvetted_askpass_is_not_pass():
    """Case 4: an unvetted executable askpass is never a PASS."""
    section = whole_path(
        helpers=[{"origin": "sys", "scope": "system", "value": ""},
                 {"origin": "user", "scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "global", "value": "false"}],
        env=child_env(GIT_ASKPASS="C:/some/unvetted/askpass.exe"),
    )
    assert section["verdict"] != PASS
    assert status_of(section, "askpass_not_prompting") == UNKNOWN


def test_05_child_override_reinstating_manager_is_detected():
    """Case 5: a CHILD env override that reinstates the system manager FAILs."""
    env = child_env(GIT_CONFIG_SYSTEM="C:/scratch/etc/gitconfig")
    section = whole_path(helpers=[{"origin": "sys", "scope": "system", "value": ""}],
                         env=env)
    assert status_of(section, "no_config_override") == FAIL
    assert section["verdict"] != PASS


def test_06_regression_l1_shape_with_interaction_disabled_passes():
    """Case 6 (regression): reset + 'manager --no-ui' + interactive=false -> PASS.

    This must PASS WITHOUT weakening case 2: case 2 has NO interactive setting
    and stays FAIL; here the interaction is explicitly disabled.
    """
    section = whole_path(
        helpers=[{"origin": "sys", "scope": "system", "value": ""},
                 {"origin": "user", "scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "global", "value": "false"}],
    )
    assert section["verdict"] == PASS, [a for a in section["assertions"]]
    assert status_of(section, "helper_non_interactive") == PASS
    assert status_of(section, "helper_resolution_reset") == PASS
    assert status_of(section, "askpass_not_prompting") == PASS
    assert status_of(section, "terminal_prompt_disabled") == PASS
    assert status_of(section, "no_config_override") == PASS


def test_06b_case2_and_case6_do_not_conflict():
    """The frame of case 6: the ONLY difference from case 2 is the interactive setting."""
    common_helpers = [{"origin": "sys", "scope": "system", "value": ""},
                      {"origin": "user", "scope": "global", "value": "manager --no-ui"}]
    without = whole_path(common_helpers)
    with_disabled = whole_path(common_helpers, interactive=[{"scope": "global", "value": "false"}])
    assert without["verdict"] == FAIL
    assert with_disabled["verdict"] == PASS


# --------------------------------------------------------------------------- #
# assertion-level unit checks
# --------------------------------------------------------------------------- #

def test_helper_non_interactive_no_ui_alone_is_insufficient():
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager --no-ui"}])
    assert res["status"] == FAIL


def test_helper_non_interactive_accepts_interaction_disabled():
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "global", "value": "false"}])
    assert res["status"] == PASS


def test_helper_non_interactive_accepts_gcm_env_disabled():
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager"}],
        env={"GCM_INTERACTIVE": "never"})
    assert res["status"] == PASS


def test_helper_non_interactive_vacuous_empty_is_unknown_not_pass():
    res = A.assert_helper_non_interactive([{"scope": "system", "value": ""}])
    assert res["status"] == UNKNOWN


def test_no_reset_is_unknown_not_pass():
    res = A.assert_helper_resolution_reset(
        [{"scope": "system", "value": "manager"}])
    assert res["status"] == UNKNOWN


def test_roll_up_pass_only_if_every_assertion_passes():
    assert A.roll_up([{"status": PASS}, {"status": PASS}]) == PASS
    assert A.roll_up([{"status": PASS}, {"status": UNKNOWN}]) == INCONCLUSIVE
    assert A.roll_up([{"status": PASS}, {"status": FAIL}]) == FAIL
    assert A.roll_up([]) == INCONCLUSIVE


def test_terminal_prompt_assertion_reason_mentions_askpass():
    res = A.assert_terminal_prompt_disabled({"GIT_TERMINAL_PROMPT": "0"})
    assert res["status"] == PASS
    assert "askpass" in res["reason"].lower()


def test_empty_askpass_value_is_absent():
    res = A.assert_askpass_not_prompting({"GIT_ASKPASS": ""})
    assert res["status"] == PASS


# --------------------------------------------------------------------------- #
# case 7: scratch-config end-to-end via --test-global
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# round-2 (HGK-GCM-REPAIR2-20261013) counterexamples for D1 / D2 / D3 / D8
#
# Each counterexample asserts the FIXED (fail-closed) behaviour, so it fails on
# the old fail-open behaviour and passes on the new one. No-over-block controls
# assert the fix did not become a false FAIL.
# --------------------------------------------------------------------------- #

def _fake_which(mapping):
    """Deterministic PATH resolver for tests (never touches the live host)."""
    def which(name):
        return mapping.get(name)
    return which


def _scoped(value, scope="global"):
    return {"scope": scope, "value": value}


def test_D1_counterexample_higher_precedence_reenable_is_not_pass():
    """D1: a later/higher-precedence re-enable must NOT be ignored.

    Old behaviour: interaction_disabled_for returned True on the FIRST disabling
    entry, so this whole context wrongly PASSed. New: FAIL.
    """
    section = whole_path(
        helpers=[{"scope": "system", "value": ""},
                 {"scope": "command", "value": "manager --no-ui"}],
        interactive=[{"scope": "system", "value": "false"},
                     {"scope": "command", "value": "true"}],
        env=child_env(),
    )
    assert section["verdict"] != PASS
    assert section["verdict"] == FAIL
    assert status_of(section, "helper_non_interactive") == FAIL


def test_D1_counterexample_gcm_env_always_beside_false_is_not_pass():
    """D1: GCM_INTERACTIVE=always beside credential.interactive=false must FAIL."""
    section = whole_path(
        helpers=[{"scope": "system", "value": ""},
                 {"scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "global", "value": "false"}],
        env=child_env(GCM_INTERACTIVE="always"),
    )
    assert section["verdict"] == FAIL
    assert status_of(section, "helper_non_interactive") == FAIL


def test_D1_counterexample_unordered_scope_is_unknown_not_pass():
    """D1: contradictory/unordered inputs must not prove non-interaction."""
    # Two entries sharing the deciding scope with conflicting values.
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "command", "value": "false"},
                     {"scope": "command", "value": "true"}],
        which=_fake_which({"git-credential-manager": None}),
        allow={"paths": set(), "digests": set()},
    )
    assert res["status"] != PASS

    # An unrankable scope cannot be ordered, so it cannot prove non-interaction.
    res2 = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "mystery-scope", "value": "false"}],
        which=_fake_which({"git-credential-manager": None}),
        allow={"paths": set(), "digests": set()},
    )
    assert res2["status"] != PASS


def test_D1_control_single_disabling_at_helper_scope_still_passes():
    """D1 no-over-block: one disabling value at/above the helper scope still PASSes."""
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager"}],
        interactive=[{"scope": "global", "value": "false"}],
        allow={"paths": {"c:\\vetted\\git-credential-manager.exe"}, "digests": set()},
        which=_fake_which({"git-credential-manager": "C:\\vetted\\git-credential-manager.exe"}),
    )
    assert res["status"] == PASS


def test_D1_control_disable_at_or_above_helper_scope_governs():
    """D1 no-over-block: a disabling value at/above the helper scope governs it."""
    # Same scope governs.
    assert A.interaction_disabled_for("global", [{"scope": "global", "value": "false"}]) is True
    # Higher-precedence scope governs.
    assert A.interaction_disabled_for("global", [{"scope": "command", "value": "false"}]) is True
    # A value BELOW the helper scope does not govern it (no silent over- or under-block).
    assert A.interaction_disabled_for("global", [{"scope": "system", "value": "false"}]) is False


def test_D2_counterexample_unvetted_path_is_not_pass():
    """D2: a helper accepted on basename/family alone wrongly PASSed; now FAIL."""
    section = whole_path(
        helpers=[{"scope": "system", "value": ""},
                 {"scope": "global", "value": "C:/unvetted/manager.exe"}],
        interactive=[{"scope": "global", "value": "false"}],
        env=child_env(),
    )
    assert section["verdict"] != PASS
    assert section["verdict"] == FAIL
    assert status_of(section, "helper_non_interactive") == FAIL


def test_D2_counterexample_gh_family_does_not_inherit_gcm_coverage():
    """D2: 'gh auth git-credential' must NOT inherit GCM-style setting coverage."""
    section = whole_path(
        helpers=[{"scope": "system", "value": ""},
                 {"scope": "global", "value": "gh auth git-credential"}],
        interactive=[{"scope": "global", "value": "false"}],
        env=child_env(),
    )
    assert section["verdict"] == FAIL
    assert status_of(section, "helper_non_interactive") == FAIL


def test_D2_counterexample_unresolved_program_is_not_pass():
    """D2: a prompt-capable family name that resolves to nothing is FAIL, never PASS."""
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "global", "value": "false"}],
        which=_fake_which({}),
        allow={"paths": set(), "digests": set()},
    )
    assert res["status"] == FAIL


def test_D2_control_vetted_path_still_passes():
    """D2 no-over-block: the real installed executable still PASSes."""
    real = shutil.which("git-credential-manager")
    if not real:
        import pytest
        pytest.skip("git-credential-manager not installed on this host")
    section = whole_path(
        helpers=[{"scope": "system", "value": ""},
                 {"scope": "global", "value": '"%s" --no-ui' % real.replace("\\", "/")}],
        interactive=[{"scope": "global", "value": "false"}],
        env=child_env(),
    )
    assert section["verdict"] == PASS, [(a["name"], a["status"]) for a in section["assertions"]]
    assert status_of(section, "helper_non_interactive") == PASS


def test_D2_control_bare_family_name_resolves_on_host_still_passes():
    """D2 no-over-block: bare 'manager --no-ui' resolves via PATH by positive identity."""
    real = shutil.which("git-credential-manager")
    if not real:
        import pytest
        pytest.skip("git-credential-manager not installed on this host")
    section = whole_path(
        helpers=[{"scope": "system", "value": ""},
                 {"scope": "global", "value": "manager --no-ui"}],
        interactive=[{"scope": "global", "value": "false"}],
        env=child_env(),
    )
    assert section["verdict"] == PASS, [(a["name"], a["status"]) for a in section["assertions"]]


def test_D3_counterexample_failed_askpass_read_is_unknown_not_pass():
    """D3: a FAILED core.askPass read must be UNKNOWN, never a silent PASS.

    Old behaviour: read_context discarded the failed read, returned askpass=[],
    and the whole context PASSed. New: askpass_not_prompting is UNKNOWN and the
    whole context is INCONCLUSIVE.
    """
    orig = CP.read_config

    def fake(git, key, env):
        if key == "core.askPass":
            return {"ok": False, "reason": "simulated read failure", "entries": []}
        return orig(git, key, env)

    CP.read_config = fake
    try:
        ctx = CP.read_context("git", dict(os.environ))
    finally:
        CP.read_config = orig
    assert ctx["ok"] is True
    assert ctx["askpass_ok"] is False
    section = CP.evaluate_context(
        env=child_env(), cwd=None, helpers=ctx["helpers"],
        interactive=ctx["interactive"], askpass_config=ctx["askpass"],
        askpass_read_ok=ctx["askpass_ok"],
        interactive_read_ok=ctx["interactive_ok"])
    assert section["verdict"] == INCONCLUSIVE
    assert status_of(section, "askpass_not_prompting") == UNKNOWN


def test_D3_counterexample_failed_interactive_read_is_not_pass():
    """D3: a FAILED credential.interactive read is missing input, not absence."""
    res = A.assert_helper_non_interactive(
        [{"scope": "global", "value": "manager --no-ui"}],
        interactive=[],
        interactive_read_ok=False,
        which=_fake_which({"git-credential-manager": "C:\\vetted\\git-credential-manager.exe"}),
        allow={"paths": {"c:\\vetted\\git-credential-manager.exe"}, "digests": set()},
    )
    assert res["status"] == UNKNOWN


def test_D3_control_read_ok_still_passes():
    """D3 no-over-block: a successful read with the setting present still PASSes."""
    res = A.assert_askpass_not_prompting({"GIT_ASKPASS": ""}, askpass_config=[],
                                         askpass_read_ok=True)
    assert res["status"] == PASS


def test_D8_scalar_interactive_returns_typed_error_not_traceback():
    """D8: classify(entries, interactive="false") must return a typed error."""
    out = CP.classify([{"scope": "global", "value": "manager"}], interactive="false")
    assert out["verdict"] == INCONCLUSIVE
    assert out.get("error") == "ERR_CLASSIFY_BAD_ARGUMENT"
    assert "interactive" in out.get("reason", "")
    assert out.get("is_acceptance") is False


def test_D8_non_mapping_entries_return_typed_error():
    """D8: a scalar / non-mapping entry list must not raise a bare AttributeError."""
    out = CP.classify("not-a-list")
    assert out["verdict"] == INCONCLUSIVE
    assert out.get("error") == "ERR_CLASSIFY_BAD_ARGUMENT"


def test_D8_well_formed_call_still_works():
    """D8 no-over-block: a well-formed call is unaffected by the type guard."""
    out = CP.classify([{"scope": "system", "value": ""},
                       {"scope": "global", "value": "manager --no-ui"}],
                      interactive=[{"scope": "global", "value": "false"}])
    assert "verdict" in out


def _write_global(dirpath, body):
    p = Path(dirpath) / "scratch.gitconfig"
    p.write_text(body, encoding="ascii")
    return p


def _run_cli(global_file, child_env_dict):
    tmp = tempfile.mkdtemp()
    cef = Path(tmp) / "child.json"
    cef.write_text(json.dumps(child_env_dict), encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(GCM_DIR / "credential_preflight.py"), "--json",
         "--test-global", str(global_file), "--child-env-file", str(cef)],
        capture_output=True, text=True,
    )
    return proc


def test_07_end_to_end_contained_fixture_exit_0():
    with tempfile.TemporaryDirectory() as d:
        gf = _write_global(
            d,
            "[credential]\n\thelper =\n\thelper = manager --no-ui\n\tinteractive = false\n",
        )
        proc = _run_cli(gf, child_env())
    assert proc.returncode == 0, proc.stdout + proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["verdict"] == PASS
    assert doc["child"]["verdict"] == PASS
    # baseline is a separate section and is not what the verdict is taken from
    assert "baseline" in doc and "child" in doc


def test_07_end_to_end_prompting_fixture_exit_2():
    with tempfile.TemporaryDirectory() as d:
        gf = _write_global(d, "[credential]\n\thelper = manager\n")
        proc = _run_cli(gf, child_env())
    assert proc.returncode == 2, proc.stdout + proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["verdict"] != PASS


def test_07_child_override_fixture_exit_2():
    """A child env that redirects GIT_CONFIG_SYSTEM is a FAIL through the CLI."""
    with tempfile.TemporaryDirectory() as d:
        gf = _write_global(
            d,
            "[credential]\n\thelper =\n\thelper = manager --no-ui\n\tinteractive = false\n",
        )
        env = child_env(GIT_CONFIG_SYSTEM="C:/scratch/other-system-gitconfig")
        proc = _run_cli(gf, env)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    doc = json.loads(proc.stdout)
    assert any(a["name"] == "no_config_override" and a["status"] == FAIL
               for a in doc["assertions"])


if __name__ == "__main__":
    # Plain-python fallback if pytest is not used.
    import traceback
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
    raise SystemExit(1 if failed else 0)
