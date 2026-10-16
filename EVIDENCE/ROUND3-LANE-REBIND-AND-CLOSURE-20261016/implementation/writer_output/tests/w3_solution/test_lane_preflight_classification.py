"""T4.2 - classifier positive/negative/boundary on the recorded samples.

Every fixture literal is labelled with the exact source file + line it came from
(see SOURCE_LINE below and SOLUTION_NOTES.md). Deterministic: no network, no real
model, no relay, no developer Codex home.
"""

import json

import pytest

from conftest import fixture_lines, line_at, preflight


DECLARED_MODEL = "gpt-6.1-sol"

# Source of the recorded samples, byte-identical copies of:
#   C:/Projects/Agent_Workspace/HG-KSEOS/var/far-iao-lane-skip-20261012/probes/MATRIX_2_binary_ab.txt
#   C:/Projects/Agent_Workspace/HG-KSEOS/var/far-iao-lane-skip-20261012/verify/VERIFY_AO3.exec-20261012T050346Z.log
MATRIX = "probes_MATRIX_2_binary_ab.txt"
VERIFY = "verify_VERIFY_AO3_literal_provenance.txt"


def _classify(text, exit_code=1):
    return preflight.classify(text.splitlines(), exit_code, DECLARED_MODEL)


# ---- Positive: each literal harness signature -> LANE_TOOLCHAIN_MISMATCH ----

def test_models_cache_schema_error_is_harness_fault():
    # MATRIX_2_binary_ab.txt line 4 (E1, the 0.147 build).
    line = line_at(MATRIX, 4)
    assert "failed to load models cache: missing field" in line
    assert _classify(line) == preflight.LANE_TOOLCHAIN_MISMATCH


def test_model_metadata_not_found_is_harness_fault():
    # MATRIX_2_binary_ab.txt line 18.
    line = line_at(MATRIX, 18)
    assert "Model metadata for" in line and "not found" in line
    assert _classify(line) == preflight.LANE_TOOLCHAIN_MISMATCH


def test_unexpected_argument_stdin_form_is_harness_fault():
    # The literal from the brief. It is NOT present in the supplied VERIFY logs
    # (verify ... line 2098 records "unexpected argument line present in supplied
    # log=False"); it appears only inside checker scripts. See SOLUTION_NOTES.md.
    line = "error: unexpected argument '-' found"
    assert _classify(line) == preflight.LANE_TOOLCHAIN_MISMATCH


def test_unknown_subcommand_and_unknown_flag_are_harness_faults():
    assert _classify("error: unrecognized subcommand 'exec2'") == preflight.LANE_TOOLCHAIN_MISMATCH
    assert _classify("error: unknown flag '--nope'") == preflight.LANE_TOOLCHAIN_MISMATCH


def test_combined_real_failing_log_is_harness_fault_no_substitution():
    """The real 0.147 log carries a provider-looking 400 AND toolchain symptoms.
    The harness symptom must dominate; substitution must be refused."""
    text = "\n".join([
        line_at(MATRIX, 4),
        line_at(MATRIX, 5),
        line_at(MATRIX, 18),
        line_at(MATRIX, 19),
    ])
    cls = _classify(text, exit_code=1)
    assert cls == preflight.LANE_TOOLCHAIN_MISMATCH
    assert cls != preflight.LANE_MODEL_REFUSED


# ---- Positive: a genuine refusal -> LANE_MODEL_REFUSED ----------------------

def test_genuine_provider_refusal_maps_to_model_refused():
    # MATRIX_2_binary_ab.txt lines 22/24/27 + a clean refusal body.
    text = "\n".join([
        line_at(MATRIX, 24),   # OpenAI Codex v0.162.0-alpha.17.2
        line_at(MATRIX, 27),   # model: gpt-6.1-sol
        'ERROR: {"type":"error","status":403,"error":{"type":"invalid_request_error",'
        '"message":"The \'gpt-6.1-sol\' model is not supported when using Codex with a ChatGPT account."}}',
    ])
    assert _classify(text, exit_code=1) == preflight.LANE_MODEL_REFUSED


# ---- Boundary / negative ---------------------------------------------------

def test_clean_success_header_maps_to_lane_ok():
    text = "\n".join([line_at(MATRIX, 24), line_at(MATRIX, 27), "codex", "OK"])
    assert _classify(text, exit_code=0) == preflight.LANE_OK


def test_empty_output_is_inconclusive():
    assert _classify("", exit_code=0) == preflight.LANE_INCONCLUSIVE
    assert _classify("", exit_code=1) == preflight.LANE_INCONCLUSIVE


def test_provider_error_without_account_language_is_not_a_deviation():
    text = 'ERROR: {"type":"error","status":400,"message":"bad request for gpt-6.1-sol"}'
    assert _classify(text, exit_code=1) != preflight.LANE_MODEL_REFUSED
    assert _classify(text, exit_code=1) == preflight.LANE_INCONCLUSIVE


def test_status_code_alone_is_not_enough():
    """A 400 that does not name the declared model is not a refusal of it."""
    text = 'ERROR: {"type":"error","status":400,"message":"bad request"}'
    assert _classify(text, exit_code=1) == preflight.LANE_INCONCLUSIVE


# ---- The provenance gap is recorded honestly -------------------------------

def test_unexpected_argument_signature_is_absent_from_the_recorded_supplied_log():
    """The brief's literal-3 signature is not in the supplied VERIFY_AO/Matrix
    logs; the VERIFY log itself records that. We assert the recorded fact rather
    than fabricate a fixture line."""
    # fixture line 1 == source VERIFY log line 2097 ("STEP 3: literal log provenance")
    # fixture line 2 == source VERIFY log line 2098
    provenance = line_at(VERIFY, 2)
    assert provenance == "unexpected argument line present in supplied log=False"

