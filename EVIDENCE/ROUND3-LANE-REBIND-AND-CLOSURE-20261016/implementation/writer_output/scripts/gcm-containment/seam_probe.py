#!/usr/bin/env python3
"""Deterministic, model-free, network-free seam re-runner for round
``HGK-GCM-CONTAINMENT-20261013``.

Two seams are re-derived from scratch every run:

  S1 ``helper_list_reset``
      Build a scratch SYSTEM config whose ``credential.helper`` is a logging
      shell shim, and a scratch GLOBAL config whose helper is an EMPTY value
      followed by a DIFFERENT logging shim. Issue a credential request and
      report which shim was invoked. The CONTROL case (no empty reset) must
      show the SYSTEM shim being invoked; the RESET case must show ONLY the
      GLOBAL shim. The real config files are never touched -- the scratch
      configs are wired in through ``GIT_CONFIG_SYSTEM`` / ``GIT_CONFIG_GLOBAL``
      (native ``C:/...`` forward-slash paths; this host does not translate MSYS
      paths for native programs).

  S2 ``git_own_prompt_fallback``
      With a helper that returns nothing, show that git falls back to its OWN
      prompt path (it invokes the askpass program), and that a non-interactive
      process environment changes that outcome (``GIT_TERMINAL_PROMPT=0`` turns
      the terminal fallback into a typed immediate failure instead of a wait).

Three-valued discipline: every seam is ``PASS`` / ``FAIL`` / ``INCONCLUSIVE``.
``INCONCLUSIVE`` is never reported as a pass. Inputs are asserted non-empty
BEFORE any comparison. Exit 0 only when every seam is ``PASS``; exit 2 on any
``FAIL`` or ``INCONCLUSIVE``.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PASS = "PASS"
FAIL = "FAIL"
INCONCLUSIVE = "INCONCLUSIVE"

REQUEST_TEMPLATE = "protocol=https\nhost={host}\n\n"


# --------------------------------------------------------------------------- #
# environment / scratch helpers
# --------------------------------------------------------------------------- #

def base_env() -> dict:
    """The host environment minus every GIT_* knob, so the seam is deterministic."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    # Never let a caller's ASKPASS / terminal-prompt setting leak into a seam.
    for k in ("GIT_ASKPASS", "SSH_ASKPASS", "GCM_INTERACTIVE",
              "GIT_TERMINAL_PROMPT", "GIT_CONFIG_NOSYSTEM"):
        env.pop(k, None)
    return env


def fwd(p: Path | str) -> str:
    return str(p).replace("\\", "/")


def shim_helper(token: str, log_path: Path) -> str:
    """A git credential-helper value that logs ``token`` when git invokes it.

    No backslashes anywhere, so git's double-quote escape processing cannot
    turn the stored value into a multi-line blob (which would defeat the
    line-oriented reader downstream). ``echo`` puts each key on its own line.
    """
    inner = (f"echo {token} >> '{fwd(log_path)}'; "
             f"echo username={token.lower()}; echo password=pw-{token.lower()}")
    return f'"!f() {{ {inner}; }}; f"'


def write_config(path: Path, helpers: list[str]) -> None:
    body = "[credential]\n"
    for h in helpers:
        body += f"\thelper = {h}\n"
    path.write_text(body, encoding="ascii", newline="\n")


def run_git(git: str, args: list[str], env: dict, cwd: Path, stdin: str) -> dict:
    proc = subprocess.run([git, *args], input=stdin, capture_output=True,
                          text=True, env=env, cwd=str(cwd), timeout=60)
    return {"argv": [git, *args], "exit": proc.returncode,
            "stdout": proc.stdout, "stderr": proc.stderr}


def nonempty(*vals: str) -> bool:
    return all(isinstance(v, str) and v.strip() != "" for v in vals)


# --------------------------------------------------------------------------- #
# S1 -- helper list reset
# --------------------------------------------------------------------------- #

def seam_s1(git: str, scratch: Path) -> dict:
    sys_cfg = scratch / "s1.system.config"
    glob_cfg = scratch / "s1.global.config"
    sys_log = scratch / "s1.system.log"
    glob_log = scratch / "s1.global.log"
    token_sys = "SYS-HELPER-INVOKED"
    token_glob = "GLOBAL-HELPER-INVOKED"

    write_config(sys_cfg, [shim_helper(token_sys, sys_log)])
    host = "seam.invalid"
    request = REQUEST_TEMPLATE.format(host=host)

    env = base_env()
    env["GIT_CONFIG_SYSTEM"] = fwd(sys_cfg)
    env["GIT_CONFIG_GLOBAL"] = fwd(glob_cfg)

    obs: dict = {"control": {}, "reset": {}}

    def run_case(name: str, global_helpers: list[str]) -> dict:
        sys_log.unlink(missing_ok=True)
        glob_log.unlink(missing_ok=True)
        write_config(glob_cfg, global_helpers)
        env["GIT_CONFIG_GLOBAL"] = fwd(glob_cfg)
        res = run_git(git, ["credential", "fill"], env, scratch, request)
        sys_hit = sys_log.exists() and token_sys in sys_log.read_text(encoding="ascii")
        glob_hit = glob_log.exists() and token_glob in glob_log.read_text(encoding="ascii")
        return {"global_helpers": global_helpers,
                "system_shim_invoked": sys_hit,
                "global_shim_invoked": glob_hit,
                "system_log_content": sys_log.read_text(encoding="ascii") if sys_log.exists() else "",
                "global_log_content": glob_log.read_text(encoding="ascii") if glob_log.exists() else "",
                "run": res}

    # CONTROL: the global config rebinds WITHOUT an empty reset first, so the
    # accumulated helper list still contains the system shim and git reaches it.
    obs["control"] = run_case("control", [shim_helper(token_glob, glob_log)])
    # RESET: an empty value at the higher-priority scope resets the list, so the
    # system shim must NOT be reached and only the global shim answers.
    obs["reset"] = run_case("reset", ["", shim_helper(token_glob, glob_log)])

    command = (f"GIT_CONFIG_SYSTEM={fwd(sys_cfg)} GIT_CONFIG_GLOBAL={fwd(glob_cfg)} "
               f"{git} credential fill  (stdin: protocol=https / host={host})")

    control_ok = obs["control"]["system_shim_invoked"]
    reset_sys_clear = not obs["reset"]["system_shim_invoked"]
    reset_glob_hit = obs["reset"]["global_shim_invoked"]

    # Assert inputs are non-empty BEFORE comparing.
    if not nonempty(*[str(r["run"]["stdout"]) for r in (obs["control"], obs["reset"])]):
        status = INCONCLUSIVE
        reason = "credential-request stdout was empty; cannot compare which shim answered"
    elif not (control_ok or reset_glob_hit) and not reset_sys_clear:
        status = INCONCLUSIVE
        reason = "neither shim was observed on either case; the seam did not execute"
    elif control_ok and reset_sys_clear and reset_glob_hit:
        status = PASS
        reason = ("control reached the system shim; an empty higher-priority helper reset the "
                  "list so the system shim was NOT reached and only the rebinding shim answered")
    else:
        status = FAIL
        reason = (f"contrary observation: control_system_invoked={control_ok}, "
                  f"reset_system_invoked={obs['reset']['system_shim_invoked']}, "
                  f"reset_global_invoked={reset_glob_hit}")

    return {"id": "S1_helper_list_reset", "status": status, "reason": reason,
            "command": command,
            "scratch_system_config": fwd(sys_cfg),
            "scratch_global_config": fwd(glob_cfg),
            "real_config_untouched": True, "observations": obs}


# --------------------------------------------------------------------------- #
# S2 -- git's own prompt fallback
# --------------------------------------------------------------------------- #

def seam_s2(git: str, scratch: Path) -> dict:
    sys_cfg = scratch / "s2.system.config"
    glob_cfg = scratch / "s2.global.config"
    ask_log = scratch / "s2.askpass.log"
    ask_shim = scratch / "s2.askpass.cmd"

    # Helper returns nothing.
    noop = '"!f() { exit 0; }; f"'
    write_config(sys_cfg, [noop])
    write_config(glob_cfg, [""])

    # A native .cmd askpass program (git for Windows executes a native program,
    # and the prior round's MSYS .sh shim was measured broken for native git).
    ask_shim.write_text(
        "@echo off\r\n"
        f"echo ASKPASS-INVOKED>>\"{fwd(ask_log)}\"\r\n"
        "echo seam-askpass-user\r\n",
        encoding="ascii", newline="")

    host = "seam.invalid"
    request = REQUEST_TEMPLATE.format(host=host)
    env = base_env()
    env["GIT_CONFIG_SYSTEM"] = fwd(sys_cfg)
    env["GIT_CONFIG_GLOBAL"] = fwd(glob_cfg)

    def run_case(name: str, extra: dict) -> dict:
        ask_log.unlink(missing_ok=True)
        case_env = dict(env)
        case_env.update(extra)
        res = run_git(git, ["credential", "fill"], case_env, scratch, request)
        ask_hit = ask_log.exists() and "ASKPASS-INVOKED" in ask_log.read_text(encoding="ascii")
        return {"env_overrides": extra, "askpass_invoked": ask_hit,
                "askpass_log_content": ask_log.read_text(encoding="ascii") if ask_log.exists() else "",
                "run": res}

    # M1: git's OWN prompt path is reached -- it invokes the askpass program.
    obs_m1 = run_case("m1_askpass_path", {"GIT_ASKPASS": fwd(ask_shim)})
    # M2: with no askpass, the default environment falls through to the
    # controlling terminal (attempted, then it fails on this host).
    obs_m2 = run_case("m2_terminal_default", {})
    # M3: a non-interactive process environment changes that outcome.
    obs_m3 = run_case("m3_terminal_disabled", {"GIT_TERMINAL_PROMPT": "0"})

    command = (f"GIT_CONFIG_SYSTEM={fwd(sys_cfg)} GIT_CONFIG_GLOBAL={fwd(glob_cfg)} "
               f"{git} credential fill  (helper returns nothing; askpass/terminal observed)")

    m1_ok = obs_m1["askpass_invoked"]
    m3_stderr = obs_m3["run"]["stderr"].lower()
    m3_typed = ("terminal prompts disabled" in m3_stderr) and obs_m3["run"]["exit"] != 0
    m2_attempt = "/dev/tty" in obs_m2["run"]["stderr"].lower() or \
                 "prompt" in obs_m2["run"]["stderr"].lower()

    # Assert the observation INPUTS (the raw channels this seam reads) are
    # non-empty BEFORE any comparison. A successful askpass legitimately has no
    # stderr, so the input is the askpass log, not m1's stderr.
    if not nonempty(obs_m1["askpass_log_content"], obs_m2["run"]["stderr"],
                    obs_m3["run"]["stderr"]):
        status = INCONCLUSIVE
        reason = ("one of the observed channels (askpass log / default-terminal stderr / "
                  "non-interactive stderr) was empty; cannot assert the prompt path")
    elif m1_ok and m3_typed:
        status = PASS
        reason = ("with the helper returning nothing git reached its own askpass prompt path "
                  "(askpass program invoked), and GIT_TERMINAL_PROMPT=0 changed the outcome to a "
                  "typed immediate failure ('terminal prompts disabled')")
    else:
        status = FAIL
        reason = (f"askpass_path_reached={m1_ok}, noninteractive_typed_failure={m3_typed}, "
                  f"default_terminal_attempted={m2_attempt}")

    return {"id": "S2_git_own_prompt_fallback", "status": status, "reason": reason,
            "command": command, "real_config_untouched": True,
            "observations": {"m1_askpass_path": obs_m1,
                             "m2_terminal_default": obs_m2,
                             "m3_terminal_disabled": obs_m3},
            "two_observables": {
                "askpass_prompt_path_reached": m1_ok,
                "default_environment_attempted_terminal": m2_attempt,
                "noninteractive_env_changes_outcome": m3_typed}}


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="deterministic model-free seam re-runner")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    ap.add_argument("--git", default=None, help="git executable (default: PATH)")
    ap.add_argument("--keep-scratch", action="store_true")
    args = ap.parse_args(argv)

    git = args.git or shutil.which("git")
    scratch = Path(tempfile.mkdtemp(prefix="gcm-seam-"))
    seams: list[dict] = []
    try:
        if git is None:
            for sid in ("S1_helper_list_reset", "S2_git_own_prompt_fallback"):
                seams.append({"id": sid, "status": INCONCLUSIVE,
                              "reason": "git executable not found on PATH",
                              "command": "git credential fill"})
        else:
            seams.append(seam_s1(git, scratch))
            seams.append(seam_s2(git, scratch))
    finally:
        if not args.keep_scratch:
            shutil.rmtree(scratch, ignore_errors=True)

    all_pass = bool(seams) and all(s["status"] == PASS for s in seams)
    result = {
        "schema": "HGK-GCM-CONTAINMENT-SEAM-PROBE/1",
        "round": "HGK-GCM-CONTAINMENT-20261013",
        "git": git or "NOT_FOUND",
        "seams": {s["id"]: s for s in seams},
        "all_pass": all_pass,
        "claim_ceiling": ("deterministic seam re-run; no model, no network; this is a "
                          "mechanism proof, not acceptance"),
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for s in seams:
            print(f"[{s['status']:>12}] {s['id']}: {s['reason']}")
        print("ALL_PASS" if all_pass else "NOT_ALL_PASS")
    return 0 if all_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
