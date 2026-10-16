#!/usr/bin/env python
"""T1 self-test: receipt loss on retry (FAR018-ER1).

The canonical `HG-KSEOS/scripts/hgk-lane-dispatch.py` persists every receipt to a
FIXED path (`emit_refusal` and the final receipt both write `args.json_out`), so a
retry overwrites the record of the first attempt's refusal. The previous round
lost exactly such a receipt and recovered it only by hand.

This test CREATES THE FAILURE the fix prevents and then demonstrates the fix:

  Phase A (defect)  - load the CANONICAL module, call `emit_refusal` twice against
                      the same `--json-out`, and assert attempt-1's bytes are GONE.
                      If the canonical file already preserved them, the test FAILS
                      (it cannot certify a defect that is not there).
  Phase B (fix)     - load the candidate module, repeat the two attempts, and assert
                      attempt-1's bytes are STILL readable in a numbered sibling.
  Phase C (no-mutate) - a third, byte-identical rewrite must NOT create a new archive
                      and must not alter the live receipt; and the archiving must not
                      rename or alter the ORIGINAL receipt content.

No hardcoded expected verdicts: every assertion is against bytes the real code
wrote on this run. Exit 0 only when A, B and C all hold; 3 otherwise.
"""

import argparse
import contextlib
import importlib.util
import io
import json
import tempfile
import types
from pathlib import Path

CANONICAL = Path("C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py")
FIXED = Path(__file__).resolve().parent / "hgk-lane-dispatch.candidate.py"


class _Args:
    """Minimal stand-in for the argparse namespace `emit_refusal` reads."""

    def __init__(self, json_out, codex_home):
        self.json_out = str(json_out)
        self.codex_home = str(codex_home)


def load_module(path, alias):
    spec = importlib.util.spec_from_file_location(alias, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def refusal(code):
    return {"schema": "test/refusal", "ok": False, "lane": "EXECUTE", "code": code,
            "detail": "attempt " + code}


def run_emits(mod, out_path, home, codes):
    """Drive the real `emit_refusal` for each code; return the printed payloads."""
    printed = []
    for code in codes:
        args = _Args(out_path, home)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = mod.emit_refusal(args, refusal(code))
        assert rc == 4, "emit_refusal must return the typed-refusal exit code 4"
        printed.append(json.loads(buf.getvalue()))
    return printed


def phase_a_defect(tmp):
    out = Path(tmp) / "a" / "receipt.json"
    mod = load_module(CANONICAL, "canonical_dispatch")
    run_emits(mod, out, tmp, ["ERR_ATTEMPT_ONE", "ERR_ATTEMPT_TWO"])
    live = json.loads(out.read_text(encoding="utf-8"))
    attempt_one_archived = any(Path(tmp).joinpath("a").glob("receipt.json.attempt-*"))
    lost_attempt_one = live.get("code") == "ERR_ATTEMPT_TWO" and not attempt_one_archived
    return {
        "phase": "A_defect_canonical",
        "live_code_after_retry": live.get("code"),
        "attempt_one_archived": attempt_one_archived,
        "attempt_one_record_lost": lost_attempt_one,
        "verdict": "PASS" if lost_attempt_one else "FAIL",
    }


def phase_b_fix(tmp):
    out = Path(tmp) / "b" / "receipt.json"
    mod = load_module(FIXED, "fixed_dispatch")
    run_emits(mod, out, tmp, ["ERR_ATTEMPT_ONE", "ERR_ATTEMPT_TWO"])
    archives = sorted(Path(tmp).joinpath("b").glob("receipt.json.attempt-*"))
    archived = [json.loads(p.read_text(encoding="utf-8")) for p in archives]
    live = json.loads(out.read_text(encoding="utf-8"))
    attempt_one_still_readable = any(r.get("code") == "ERR_ATTEMPT_ONE" for r in archived)
    live_is_attempt_two = live.get("code") == "ERR_ATTEMPT_TWO"
    ok = attempt_one_still_readable and live_is_attempt_two and len(archives) == 1
    return {
        "phase": "B_fixed_candidate",
        "archive_names": [p.name for p in archives],
        "archived_codes": [r.get("code") for r in archived],
        "live_code": live.get("code"),
        "attempt_one_still_readable": attempt_one_still_readable,
        "verdict": "PASS" if ok else "FAIL",
    }


def phase_c_no_mutate(tmp):
    out = Path(tmp) / "c" / "receipt.json"
    mod = load_module(FIXED, "fixed_dispatch_c")
    run_emits(mod, out, tmp, ["ERR_ATTEMPT_ONE", "ERR_ATTEMPT_TWO"])
    # snapshot the exact live bytes, then re-emit an IDENTICAL attempt-2 receipt.
    live_before = out.read_bytes()
    archives_before = sorted(Path(tmp).joinpath("c").glob("receipt.json.attempt-*"))
    run_emits(mod, out, tmp, ["ERR_ATTEMPT_TWO"])
    live_after = out.read_bytes()
    archives_after = sorted(Path(tmp).joinpath("c").glob("receipt.json.attempt-*"))
    identical_rewrite_no_new_archive = len(archives_before) == len(archives_after)
    live_bytes_unchanged = live_before == live_after
    # the archive must hold attempt-1's EXACT content (no rename/alter of original).
    archive_text = archives_after[0].read_text(encoding="utf-8")
    original_attempt_one = json.loads(archive_text)
    archive_preserves_original = original_attempt_one.get("code") == "ERR_ATTEMPT_ONE"
    ok = identical_rewrite_no_new_archive and live_bytes_unchanged and archive_preserves_original
    return {
        "phase": "C_no_mutate_on_identical_rewrite",
        "archives_before": len(archives_before),
        "archives_after": len(archives_after),
        "live_bytes_unchanged": live_bytes_unchanged,
        "archive_preserves_original_content": archive_preserves_original,
        "verdict": "PASS" if ok else "FAIL",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="T1 receipt-loss-on-retry self-test (FAR018-ER1).")
    ap.parse_args(argv)

    with tempfile.TemporaryDirectory() as tmp:
        results = [phase_a_defect(tmp), phase_b_fix(tmp), phase_c_no_mutate(tmp)]

    failed = [r["phase"] for r in results if r["verdict"] != "PASS"]
    for r in results:
        print(json.dumps(r, indent=2))
    print("T1_RESULT=" + ("PASS" if not failed else "FAIL:" + ",".join(failed)))
    return 0 if not failed else 3


if __name__ == "__main__":
    raise SystemExit(main())
