#!/usr/bin/env sh
# T3 - lane launcher wiring.
#
# Usage: lane_launcher.sh <lane-name> <model> <effort> <brief> <log>
#
# Fixed, fail-closed order:
#   1. resolve + verify the DECLARED toolchain identity via
#      scripts/hgk-lane-toolchain.py (T1). No find / command -v discovery.
#   2. run the bounded pre-lane identity preflight via
#      scripts/hgk-lane-preflight.py (T2).
#   2.5 run the GCM credential-posture gate via
#      scripts/gcm-containment/lane_credential_posture.py and apply the
#      asymmetric posture policy below. TEST-ONLY scratch posture via
#      HGK_LANE_POSTURE_TEST_GLOBAL / HGK_LANE_POSTURE_GIT (see that section).
#   3. only then run the real lane, and only when T2 returned LANE_OK.
#
# Substitution gate:
#   * LANE_TOOLCHAIN_MISMATCH -> REFUSE to substitute; exit non-zero and NAME the
#     offending build. No deviation record is written.
#   * LANE_MODEL_REFUSED      -> write a declared-model-deviation record that
#     carries the T2 receipt fields; do NOT substitute inline; exit non-zero for
#     an owner decision.
#
# Safety:
#   * the canonical containment guard (scripts/hgk-lane-preflight.py's
#     check_containment, reused via --check-containment) is the ONLY containment
#     predicate; there is no second, weaker inline check.
#   * NO directory is created (no mkdir) until containment is PROVEN for the
#     scratch base, the lane scratch, the caller log and the receipt.
#   * cleanup deletes ONLY the lane's own scratch, only after re-proving
#     containment; a failed deletion changes the exit status and is recorded
#     AFTER it is attempted. No `|| true` swallows a delete failure.
#
# T7 identity assertion:
#   * after the long lane returns, the served model is extracted ONLY from the
#     CLI's anchored startup banner in $LOG and compared with the declared model.
#   * a mismatch, or an absent/unreadable banner on an otherwise-successful lane,
#     writes ${LOG}.identity.receipt.json and exits 98
#     (ERR_LANE_MODEL_IDENTITY_MISMATCH). 98 is deliberately outside the existing
#     90/91/92/93/94/95/99 launcher/preflight codes.
#
# Credential-posture gate (step 2.5) -- the L3 consumer of
# scripts/gcm-containment/credential_preflight.py:
#   * the preflight can only be a CONTROL if something acts on its verdict; this
#     launcher is that consumer. It runs BEFORE the real lane starts and applies
#     an ASYMMETRIC, three-valued policy:
#       FAIL         -> BLOCK: exit 89 (ERR_LANE_CREDENTIAL_POSTURE_PROMPTABLE),
#                       naming the offending prompt-capable helper AND its origin
#                       file. Fail-closed on the DANGER.
#       INCONCLUSIVE -> WARN loudly on stderr with a typed code
#                       (WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE) and CONTINUE.
#                       Deliberately NOT fail-closed on the DETECTOR.
#       PASS         -> continue silently.
#   * the second prompt surface is closed separately: GIT_TERMINAL_PROMPT=0 is
#     exported into the LANE environment (step 3) so git fails immediately
#     instead of waiting on a terminal that an unattended lane has nobody to
#     watch. The preflight/reset only covers the HELPER list; this covers git's
#     OWN askpass/terminal fallback (rounded seam S2).
#   * the posture actually in force is auditable: ${LOG}.identity.receipt.json
#     gains an additive `credential_posture` object recording at minimum
#     `git_terminal_prompt`, read back from the lane's own receipt.
#
# TRADE-OFF (recorded, not hidden): L1 (the user-scope git config default -- an
# empty-string helper reset plus `manager --no-ui`) is the STRUCTURAL control and
# holds whether or not this gate works. This gate is the SECOND layer. Making a
# detector malfunction block every lane would turn a detector bug into a lane
# outage, which is the opposite of the low-resistance criterion the owner set.
# So we are fail-closed on a positive violation of the invariant, and not
# fail-closed on the detector's inability to reach a verdict. The gate is
# deterministic and model-free; it never issues a credential request.
#
# POSIX sh (git-bash on Windows). Prefer stdlib; no new dependencies.

set -u

if [ "$#" -ne 5 ]; then
  echo "usage: $0 <lane-name> <model> <effort> <brief> <log>" >&2
  exit 64
fi

LANE_NAME="$1"
MODEL="$2"
EFFORT="$3"
BRIEF="$4"
LOG="$5"

SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
RESOLVER="$SELF_DIR/hgk-lane-toolchain.py"
PREFLIGHT="$SELF_DIR/hgk-lane-preflight.py"
SUBJECT_ROOT="$(cd "$SELF_DIR/.." && pwd)"

# Windows<->POSIX path conversion when a native interpreter is used on git-bash.
WIN() {
  if command -v cygpath >/dev/null 2>&1; then cygpath -w "$1"; else printf '%s' "$1"; fi
}

# Interpreter override; otherwise pick a working one. This is NOT binary
# discovery of the lane toolchain (that is T1's job) - it only chooses a Python
# to run the two helper scripts.
PYTHON="${HGK_LANE_PYTHON:-}"
if [ -z "$PYTHON" ]; then
  for cand in python3 python; do
    if command -v "$cand" >/dev/null 2>&1 && "$cand" -c '' >/dev/null 2>&1; then
      PYTHON="$cand"; break
    fi
  done
  if [ -z "$PYTHON" ]; then
    echo "ERR_LANE_TOOLCHAIN_NO_PYTHON" >&2
    exit 92
  fi
fi

if "$PYTHON" -c 'import os,sys; sys.exit(0 if os.name=="nt" else 1)' 2>/dev/null; then
  WINPATHS=1
else
  WINPATHS=0
fi
P() { if [ "$WINPATHS" = 1 ]; then WIN "$1"; else printf '%s' "$1"; fi; }

SCRATCH_BASE="${HGK_LANE_SCRATCH:-${TMPDIR:-/tmp}/hgk-lane-preflight}"
SCRATCH="${SCRATCH_BASE}/${LANE_NAME}"
PREFLIGHT_RECEIPT="${LOG}.preflight.receipt.json"
CONTAINMENT_RECEIPT="${LOG}.containment.receipt.json"
DEVIATION_RECORD="${LOG}.model-deviation-required.json"
IDENTITY_RECEIPT="${LOG}.identity.receipt.json"
POSTURE_RECEIPT="${LOG}.credential-posture.receipt.json"

# ---- The L3 credential-posture gate (step 2.5) ------------------------------
# Reuses the canonical classifier in gcm-containment/credential_preflight.py.
# The two HGK_LANE_POSTURE_* knobs are TEST-ONLY deterministic seams that let
# the posture path be exercised against a scratch git scope (or a nonexistent
# git) WITHOUT ever provoking a live credential request or a credential window.
POSTURE_GATE="${HGK_LANE_POSTURE_GATE:-${SELF_DIR}/gcm-containment/lane_credential_posture.py}"
POSTURE_ARGS=""
if [ -n "${HGK_LANE_POSTURE_GIT:-}" ]; then
  POSTURE_ARGS="${POSTURE_ARGS} --git ${HGK_LANE_POSTURE_GIT}"
fi
if [ -n "${HGK_LANE_POSTURE_TEST_GLOBAL:-}" ]; then
  POSTURE_ARGS="${POSTURE_ARGS} --test-global ${HGK_LANE_POSTURE_TEST_GLOBAL}"
fi

# ---- The ONE containment guard, reused from T2 (never a second check) --------
# Calls the canonical check_containment in hgk-lane-preflight.py. Exit 0 when
# containment is proven, non-zero otherwise.
containment_ok() {
  "$PYTHON" "$(P "$PREFLIGHT")" --check-containment "$(P "$1")" "$(P "$2")" "$(P "$3")" >/dev/null 2>&1
}

# ---- Containment decisions BEFORE any mkdir --------------------------------
CONTAINMENT_OK=0
if containment_ok "$SCRATCH_BASE" "$SCRATCH" "$SUBJECT_ROOT"; then
  CONTAINMENT_OK=1
fi

LOG_PARENT="$(dirname "$LOG")"
LOG_CONTAINMENT_OK=0
if containment_ok "$LOG_PARENT" "$LOG" "$SUBJECT_ROOT" \
   && containment_ok "$LOG_PARENT" "$PREFLIGHT_RECEIPT" "$SUBJECT_ROOT" \
   && containment_ok "$LOG_PARENT" "$CONTAINMENT_RECEIPT" "$SUBJECT_ROOT" \
   && containment_ok "$LOG_PARENT" "$DEVIATION_RECORD" "$SUBJECT_ROOT" \
   && containment_ok "$LOG_PARENT" "$POSTURE_RECEIPT" "$SUBJECT_ROOT" \
   && containment_ok "$LOG_PARENT" "$IDENTITY_RECEIPT" "$SUBJECT_ROOT"; then
  LOG_CONTAINMENT_OK=1
fi

if [ "$LOG_CONTAINMENT_OK" != 1 ]; then
  echo "ERR_LANE_LOG_PATH_INSIDE_SUBJECT: caller log path '${LOG:-}' (or a sibling output path) is not proven outside subject root '${SUBJECT_ROOT}'; refused before creating any directory (0 attempts)." >&2
  exit 94
fi

if [ "$CONTAINMENT_OK" != 1 ]; then
  echo "ERR_LANE_SCRATCH_CONTAINMENT_UNPROVEN: scratch_base='${SCRATCH_BASE}' scratch='${SCRATCH}' is not proven contained and outside subject root '${SUBJECT_ROOT}'; refused before creating any directory (0 attempts)." >&2
  exit 95
fi

# ---- Cleanup: delete ONLY the proven scratch, AFTER re-proving --------------
CLEANUP_DONE=0
CLEANUP_FAILED=0
cleanup() {
  if [ "$CLEANUP_DONE" = 1 ]; then
    return 0
  fi
  CLEANUP_DONE=1
  if [ "$CONTAINMENT_OK" != 1 ]; then
    echo "CLEANUP_SKIPPED: containment not proven; deleted nothing." >&2
    return 0
  fi
  # Re-prove immediately before deleting (defense in depth); on doubt, delete
  # nothing. Every failure is surfaced and reflected in the exit status.
  if ! containment_ok "$SCRATCH_BASE" "$SCRATCH" "$SUBJECT_ROOT"; then
    echo "CLEANUP_SKIPPED: containment lost at delete time; deleted nothing." >&2
    return 0
  fi
  if rm -f "$(P "${SCRATCH}/binaryhome/auth.json")" 2>/dev/null || [ ! -e "$SCRATCH/binaryhome/auth.json" ]; then
    :
  else
    echo "CLEANUP_FAILED: could not remove the seeded credential under '${SCRATCH}'." >&2
    CLEANUP_FAILED=1
  fi
  if rm -rf "$(P "$SCRATCH")" 2>/dev/null; then
    if [ -e "$SCRATCH" ]; then
      echo "CLEANUP_FAILED: scratch '${SCRATCH}' still exists after rm -rf." >&2
      CLEANUP_FAILED=1
    fi
  else
    echo "CLEANUP_FAILED: rm -rf '${SCRATCH}' failed." >&2
    CLEANUP_FAILED=1
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# ---- 1. Toolchain identity: resolve + verify FIRST (fail closed) ------------
DECL_ARGS=""
if [ -n "${HGK_LANE_DECLARATION:-}" ]; then
  DECL_ARGS="--declaration $(P "${HGK_LANE_DECLARATION}")"
fi
RESOLVE_JSON="$("$PYTHON" "$(P "$RESOLVER")" --verify $DECL_ARGS 2>/dev/null)"
RESOLVE_RC=$?
if [ "$RESOLVE_RC" != 0 ]; then
  DETAIL="$(printf '%s' "$RESOLVE_JSON" | "$PYTHON" -c 'import json,sys
try:
    d=json.load(sys.stdin)
    print("{}: {}".format(d.get("error"), d.get("detail")))
except Exception:
    print("ERR_LANE_TOOLCHAIN: unparsable resolver output")' 2>/dev/null)"
  echo "ERR_LANE_TOOLCHAIN: declared toolchain did not verify; lane NOT run; substitution REFUSED." >&2
  echo "${DETAIL}" >&2
  exit 90
fi
CODEX_EXE="$(printf '%s' "$RESOLVE_JSON" | "$PYTHON" -c 'import json,sys;print(json.load(sys.stdin)["path"])')"
CODEX_VERSION="$(printf '%s' "$RESOLVE_JSON" | "$PYTHON" -c 'import json,sys;print(json.load(sys.stdin)["version"])')"

# ---- Caller log directory: created ONLY NOW (containment + identity proven) --
if [ ! -d "$LOG_PARENT" ]; then
  mkdir -p "$(P "$LOG_PARENT")"
fi

# ---- 2. Pre-lane identity preflight (one trivial prompt, <=120 s) -----------
SEED_ARGS=""
if [ -n "${HGK_LANE_PREFLIGHT_SEED_AUTH:-}" ]; then
  SEED_ARGS="--seed-auth $(P "${HGK_LANE_PREFLIGHT_SEED_AUTH}")"
fi
"$PYTHON" "$(P "$PREFLIGHT")" --model "$MODEL" --effort "$EFFORT" $DECL_ARGS \
  $SEED_ARGS --scratch "$(P "$SCRATCH")" --log "$(P "${LOG}.preflight.log")" \
  --subject-root "$(P "$SUBJECT_ROOT")" --receipt "$(P "$PREFLIGHT_RECEIPT")"
PREFLIGHT_RC=$?

CLASS="$("$PYTHON" -c 'import json,sys
try:
    print(json.load(open(sys.argv[1], encoding="utf-8")).get("error_class") or "LANE_INCONCLUSIVE")
except Exception:
    print("LANE_INCONCLUSIVE")' "$(P "$PREFLIGHT_RECEIPT")" 2>/dev/null)"

case "$CLASS" in
  LANE_OK)
    : # fall through to the real lane
    ;;
  LANE_TOOLCHAIN_MISMATCH)
    echo "LANE_TOOLCHAIN_MISMATCH: harness fault; offending build path=${CODEX_EXE} version=${CODEX_VERSION}; lane NOT run; substitution REFUSED." >&2
    exit 91
    ;;
  LANE_MODEL_REFUSED)
    "$PYTHON" - "$(P "$DEVIATION_RECORD")" "$LANE_NAME" "$(P "$PREFLIGHT_RECEIPT")" <<'PY'
import json, sys
dest, lane, receipt_path = sys.argv[1:4]
r = json.load(open(receipt_path, encoding="utf-8"))
doc = {
    "schema": "HGK-LANE-MODEL-DEVIATION-REQUIRED/1",
    "required": True,
    "class": "LANE_MODEL_REFUSED",
    "lane": lane,
    # the deviation record CARRIES the T2 receipt fields:
    "codex_cli": r.get("codex_cli"),
    "codex_cli_version": r.get("codex_cli_version"),
    "declared_model": r.get("declared_model"),
    "served_model": r.get("served_model"),
    "error_class": r.get("error_class"),
    "preflight_raw": r.get("preflight_raw"),
    "evidence_receipt": receipt_path,
    "note": ("genuine provider refusal on the declared model; a human/owner "
             "decides the declared model deviation. The launcher does NOT "
             "substitute inline."),
}
json.dump(doc, open(dest, "w", encoding="utf-8"), indent=2)
PY
    echo "LANE_MODEL_REFUSED: wrote ${DEVIATION_RECORD}; lane NOT run; substitution permitted only via a declared owner decision." >&2
    exit 92
    ;;
  *)
    echo "LANE_INCONCLUSIVE: preflight produced no usable verdict; lane NOT run; substitution REFUSED." >&2
    exit 93
    ;;
esac

# ---- 2.5 GCM credential-posture gate (asymmetric; deterministic; no window) --
# The L3 consumer of gcm-containment/credential_preflight.py. Reuses the
# canonical classifier through the gate wrapper; never a second inline check.
# Asymmetric policy (documented in the header):
#   FAIL         -> BLOCK, exit 89, naming the helper + origin (fail-closed on
#                   the danger).
#   INCONCLUSIVE -> warn loudly with a typed code and CONTINUE (not fail-closed
#                   on the detector).
#   PASS         -> continue silently.
set +e
"$PYTHON" "$(P "$POSTURE_GATE")" $POSTURE_ARGS --json > "$(P "$POSTURE_RECEIPT")" 2> "$(P "${LOG}.credential-posture.stderr.txt")"
POSTURE_RC=$?
set -e
POSTURE_VERDICT="$("$PYTHON" -c 'import json,sys
try:
    print(json.load(open(sys.argv[1], encoding="utf-8")).get("verdict") or "INCONCLUSIVE")
except Exception:
    print("INCONCLUSIVE")' "$(P "$POSTURE_RECEIPT")" 2>/dev/null)"
if [ "$POSTURE_VERDICT" = "FAIL" ]; then
  # Re-emit the typed message (named helper + origin) from the gate's own doc.
  "$PYTHON" - "$(P "$POSTURE_RECEIPT")" <<'PY' >&2
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    d = {}
print("{}: the effective credential resolution still reaches a prompt-capable "
      "interactive helper '{}' from origin '{}'; lane NOT run (0 attempts); "
      "credential posture gate BLOCKED (fail-closed on the danger).".format(
          "ERR_LANE_CREDENTIAL_POSTURE_PROMPTABLE",
          d.get("helper") or "<unknown>", d.get("origin") or "<unknown origin>"))
PY
  exit 89
fi
if [ "$POSTURE_VERDICT" = "PASS" ]; then
  : # continue silently
elif [ "${POSTURE_VERDICT:-}" = "INCONCLUSIVE" ]; then
  echo "WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE: the credential-posture detector could not reach a verdict; continuing (see ${LOG}.credential-posture.receipt.json). INCONCLUSIVE is NOT a pass; the L1 user-scope default remains the structural control." >&2
else
  echo "WARN_LANE_CREDENTIAL_POSTURE_INCONCLUSIVE: the posture gate produced no usable verdict (rc=${POSTURE_RC}); continuing. INCONCLUSIVE is NOT a pass." >&2
fi

# ---- 3. Real lane ----------------------------------------------------------
CODEX_HOME_DIR="${HGK_LANE_CODEX_HOME:-${SCRATCH}/binaryhome}"
mkdir -p "$(P "$CODEX_HOME_DIR")"
export CODEX_HOME="$(P "$CODEX_HOME_DIR")"

# Close git's OWN prompt surface (second seam S2) for the real lane: git fails
# immediately instead of waiting on a terminal nobody is watching. It applies to
# the lane invocation below and is read back into the identity receipt.
export GIT_TERMINAL_PROMPT=0

echo "=== ${LANE_NAME} lane -> ${LOG} (codex=${CODEX_EXE} version=${CODEX_VERSION} model=${MODEL}) ===" >&2
set +e
timeout "${HGK_LANE_TIMEOUT:-2400}" "$CODEX_EXE" exec --cd "$(P "$LOG_PARENT")" --skip-git-repo-check \
  -s read-only -m "$MODEL" -c "model_reasoning_effort=\"${EFFORT}\"" - \
  < "$BRIEF" > "$LOG" 2>&1
LANE_RC=$?
set -e
echo "EXIT=${LANE_RC}" >> "$LOG"

IDENTITY_OUT=""
IDENTITY_RC=0
set +e
IDENTITY_OUT="$("$PYTHON" - "$(P "$LOG")" "$MODEL" "$(P "$PREFLIGHT")" "$(P "$IDENTITY_RECEIPT")" "$LANE_RC" "${GIT_TERMINAL_PROMPT:-}" "$(P "$POSTURE_RECEIPT")" "${POSTURE_VERDICT:-INCONCLUSIVE}" <<'PY'
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

log_path, declared_model, preflight_path, receipt_path, lane_rc = sys.argv[1:6]
git_terminal_prompt = sys.argv[6]
posture_receipt_path = sys.argv[7]
posture_verdict = sys.argv[8]
try:
    lane_rc_int = int(lane_rc)
except ValueError:
    lane_rc_int = -1

spec = importlib.util.spec_from_file_location(
    "hgk_lane_preflight_identity", preflight_path
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

raw = Path(log_path).read_text(encoding="utf-8", errors="replace")
lines = raw.splitlines()
served_model, served_version = module.served_from_header(lines)

if served_model is None:
    status = "IDENTITY_UNREADABLE"
    error_class = "ERR_LANE_MODEL_IDENTITY_MISMATCH"
elif served_model == declared_model:
    status = "IDENTITY_OK"
    error_class = None
else:
    status = "IDENTITY_MISMATCH"
    error_class = "ERR_LANE_MODEL_IDENTITY_MISMATCH"

# The credential posture the LANE actually ran under, read back for audit. The
# git_terminal_prompt value is the one exported into the lane environment (not a
# note about it); helper/origin come from the posture gate's own receipt.
try:
    posture_doc = json.loads(Path(posture_receipt_path).read_text(encoding="utf-8"))
except Exception:
    posture_doc = {}

doc = {
    "schema": "HGK-LANE-IDENTITY-RECEIPT/1",
    "identity_ok": status == "IDENTITY_OK",
    "status": status,
    "error_class": error_class,
    "declared_model": declared_model,
    "served_model": served_model,
    "served_version": served_version,
    "lane_exit_code": lane_rc_int,
    "assertion_enforced": lane_rc_int == 0,
    "raw_log_path": log_path,
    "extraction": "anchored_startup_banner_only",
    "credential_posture": {
        "git_terminal_prompt": git_terminal_prompt,
        "posture_verdict": posture_verdict,
        "prompt_capable_helper": posture_doc.get("helper"),
        "origin": posture_doc.get("origin"),
        "posture_receipt_path": posture_receipt_path,
    },
}
Path(receipt_path).write_text(json.dumps(doc, indent=2), encoding="utf-8")
print(status + " " + (served_model if served_model is not None else "UNREADABLE"))
PY
)"
IDENTITY_RC=$?
set -e
if [ "$IDENTITY_RC" != 0 ] || [ -z "$IDENTITY_OUT" ]; then
  echo "ERR_LANE_MODEL_IDENTITY_MISMATCH declared=${MODEL} served=UNREADABLE" >&2
  cleanup
  if [ "$CLEANUP_FAILED" = 1 ]; then
    exit 99
  fi
  exit 98
fi

set -- $IDENTITY_OUT
IDENTITY_STATUS="${1:-IDENTITY_UNREADABLE}"
IDENTITY_SERVED="${2:-UNREADABLE}"
if [ "$LANE_RC" = 0 ] && [ "$IDENTITY_STATUS" != "IDENTITY_OK" ]; then
  echo "ERR_LANE_MODEL_IDENTITY_MISMATCH declared=${MODEL} served=${IDENTITY_SERVED}" >&2
  cleanup
  if [ "$CLEANUP_FAILED" = 1 ]; then
    exit 99
  fi
  exit 98
fi

EXIT_REASON="LANE_COMPLETE"
cleanup
if [ "$CLEANUP_FAILED" = 1 ] && [ "$LANE_RC" = 0 ]; then
  # A cleanup failure must change the return code.
  exit 99
fi
exit "$LANE_RC"
