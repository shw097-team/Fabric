#!/usr/bin/env python
"""FAR-CLOSURE-20261021 / R2 — repair the openai arm's transport vocabulary (G8).

Root cause (measured, not inferred):
  The pool carries TWO identities per entry:
    provider/model      -> the GOVERNANCE identity (what the lane is declared to be)
    transport_model     -> the string handed to the Codex-CLI transport
  The transport vocabulary is per-provider, and the openai arm REQUIRES the BARE id
  ("gpt-6.1-sol"). A qualified "openai-codex/gpt-6.1-sol" is routed by the relay to the
  DEFAULT provider, which does not serve it and answers
      HTTP 400  Provider error 400: Upstream request failed: Model is unavailable.
  scripts/hgk-lane-dispatch.py documents this in its own design notes (lines 12-14):
      "the openai arm REQUIRES the bare id, because 'openai-codex/<model>' is routed to the
       default provider and answers HTTP 400"
  Measured on 2026-10-21 against the live relay on 127.0.0.1:10101:
      "gpt-6.1-sol"                        -> 200  "OK_gpt-6.1-sol"
      "openai/gpt-6.1-sol"                 -> 200  "OK"
      "openai-codex/gpt-6.1-sol"           -> 400  Model is unavailable
      "openai-codex/gpt-5.6-sol"           -> 400  Model is unavailable
      "gpt-6.1-sol-high"                   -> 400  not supported when using Codex with a ChatGPT account
  The pool's PLAN rank-1 and VERIFY_SECURITY rank-1 both carried the qualified form, so the
  declared GPT 6.1 SOL-MEDIUM arm could not be served at all -- the lane was structurally
  un-runnable while looking correctly declared.

Repair:
  PLAN rank-1            transport_model: openai-codex/gpt-6.1-sol -> gpt-6.1-sol
  VERIFY_SECURITY rank-1 transport_model: openai-codex/gpt-6.1-sol -> gpt-6.1-sol
  The governance identity (provider=openai-codex, model=gpt-6.1-sol) is UNCHANGED, so the
  receipt gate still compares against the declared identity, and the lane's declared contract
  is unchanged.

Also records the measured transport vocabulary as a first-class, checkable fact:
  config/lane-route-slots.candidate.json gains a "transport_vocabulary" block, and the
  conformance test gains a check that every openai-codex entry uses a BARE transport_model.

Properties: dry-run default; per-file pre-image sha256; exactly-once anchors; idempotent;
post-write assertions; check_drift; conformance suite; receipt. No git write verbs.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROUND = "FAR-CLOSURE-20261021-R2"
OUT = ROOT / "var" / ROUND
POOL = ROOT / "config" / "lane-route-slots.candidate.json"
ASG = ROOT / "config" / "model-lane-assignment.json"
REG = ROOT / "config" / "lane-routing-registry.yaml"
TEST = ROOT / "tests" / "test_lane_policy.py"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    pre = {str(p): sha(p) for p in (POOL, ASG, REG, TEST)}
    changes = []

    pool = json.loads(POOL.read_text(encoding="utf-8"))
    fixed = []
    for lane in pool["lanes"]:
        for c in lane["ordered_pool"]:
            if c.get("provider") == "openai-codex" and c.get("transport_model", "").startswith("openai-codex/"):
                bare = c["transport_model"].split("/", 1)[1]
                fixed.append({"lane": lane["lane"], "rank": c.get("rank"),
                              "from": c["transport_model"], "to": bare})
                c["transport_model"] = bare
                c["transport_vocabulary_note"] = (
                    "the openai arm requires the BARE id: a qualified 'openai-codex/<model>' is routed "
                    "by the relay to the default provider and answers HTTP 400 'Model is unavailable' "
                    "(measured 2026-10-21 on 127.0.0.1:10101; bare id -> 200). The governance identity "
                    "provider=openai-codex / model=<id> is unchanged.")
    if not fixed:
        print(json.dumps({"applied": False, "note": "already applied (no qualified openai transport_model present)"},
                         ensure_ascii=False))
    pool["transport_vocabulary"] = {
        "measured_at": "2026-10-21",
        "relay": "http://127.0.0.1:10101",
        "rule": "the transport id is per-provider: openai-codex REQUIRES the bare id; "
                "nvidia REQUIRES '<provider>/<model>'; opencode-go accepts bare or qualified.",
        "openai_codex_bare_only": True,
        "evidence": {
            "gpt-6.1-sol": 200, "openai/gpt-6.1-sol": 200,
            "openai-codex/gpt-6.1-sol": 400, "openai-codex/gpt-5.6-sol": 400,
            "gpt-6.1-sol-high": 400,
        },
    }
    pool["rev"] = "far-closure-20261021-r2"
    if args.apply and fixed:
        POOL.write_text(json.dumps(pool, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes.append({"finding": "G8", "file": str(POOL), "change": "openai-codex transport_model -> bare id", "fixed": fixed})

    # conformance check: every openai-codex entry must use a bare transport_model
    check = '''

class TestOpenaiTransportVocabulary(unittest.TestCase):
    """G8 (round FAR-CLOSURE-20261021-R2): the openai arm REQUIRES the BARE transport id.

    A qualified 'openai-codex/<model>' is routed by the relay to the default provider, which
    does not serve it and answers HTTP 400 'Model is unavailable'. The governance identity is
    unchanged; only the transport vocabulary is corrected. Measured 2026-10-21 on the live
    relay: bare id -> 200, qualified id -> 400.
    """

    POOL = Path(__file__).resolve().parents[1] / "config" / "lane-route-slots.candidate.json"

    def test_openai_codex_transport_models_are_bare(self):
        pool = json.loads(self.POOL.read_text(encoding="utf-8"))
        offenders = []
        for lane in pool["lanes"]:
            for c in lane["ordered_pool"]:
                if c.get("provider") == "openai-codex":
                    tm = str(c.get("transport_model", ""))
                    if "/" in tm:
                        offenders.append(f"{lane['lane']}#{c.get('rank')}:{tm}")
        self.assertEqual([], offenders, f"openai-codex entries must use a bare transport_model: {offenders}")

    def test_transport_vocabulary_is_recorded(self):
        pool = json.loads(self.POOL.read_text(encoding="utf-8"))
        tv = pool.get("transport_vocabulary") or {}
        self.assertTrue(tv.get("openai_codex_bare_only"), "transport_vocabulary must record the bare-only rule")
        self.assertIn("gpt-6.1-sol", (tv.get("evidence") or {}), "the measured evidence must name gpt-6.1-sol")
'''
    t = TEST.read_text(encoding="utf-8")
    if "class TestOpenaiTransportVocabulary" not in t:
        t = t.rstrip("\n") + "\n" + check
        if args.apply:
            TEST.write_text(t, encoding="utf-8")
            changes.append({"finding": "G8", "file": str(TEST), "change": "added transport-vocabulary conformance tests"})

    receipt = {"round": ROUND, "utc": stamp, "applied": bool(args.apply), "changes": changes,
               "fixed": fixed, "pre_sha256": pre}
    if args.apply:
        sys.path.insert(0, str(ROOT / "src"))
        from hg_kseos import lane_policy as lp
        drift = lp.check_drift(registry=lp.load_registry())
        receipt["check_drift"] = drift
        pool2 = json.loads(POOL.read_text(encoding="utf-8"))
        bad = [f"{l['lane']}#{c.get('rank')}" for l in pool2["lanes"] for c in l["ordered_pool"]
               if c.get("provider") == "openai-codex" and "/" in str(c.get("transport_model", ""))]
        receipt["openai_transport_offenders"] = bad
        rc = subprocess.run([str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "pytest", "tests/test_lane_policy.py", "-q"],
                            cwd=str(ROOT), capture_output=True, text=True, timeout=900)
        receipt["pytest_rc"] = rc.returncode
        receipt["pytest_tail"] = (rc.stdout or "").strip().splitlines()[-2:]
        receipt["post_sha256"] = {str(p): sha(p) for p in (POOL, ASG, REG, TEST)}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / ("apply_receipt.json" if args.apply else "apply_dryrun.json")).write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"applied": bool(args.apply), "fixed": fixed, "check_drift": receipt.get("check_drift"),
                      "offenders": receipt.get("openai_transport_offenders"), "pytest_rc": receipt.get("pytest_rc"),
                      "pytest_tail": receipt.get("pytest_tail")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
