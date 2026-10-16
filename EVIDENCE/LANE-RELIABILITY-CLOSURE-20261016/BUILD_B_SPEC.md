# BUILD brief — ChangeSet B ONLY (round LANE-RELIABILITY-CLOSURE-20261016, lane EXECUTE, attempt BC2)

`BC1` timed out after 900 s without writing anything, and its saved stdout shows why: the turn spent its
budget enumerating processes (`tasklist`/PID listings) and then hit
`write_stdin failed: stdin is closed for this session; rerun exec_command with tty=true`. That is a
process failure, NOT a model failure — the receipt shows the mandated arm was served
(`usage_provider=opencode-go`, `usage_model=deepseek-v4.1-flash`, `usage_receipt_ok=true`). This brief
is the same change set, tightened, and it is now ONLY ChangeSet B.

## HARD RULES (a violation wastes the whole turn — read these first)

1. **This is a bounded patch job, not an investigation.** Do NOT enumerate processes
   (`tasklist`, `ps`, `wmic`, `netstat`, `Get-CimInstance`, `Get-Process`) — it is not part of this
   task and it is what killed BC1.
2. **Every command you run must terminate by itself.** NEVER start an interactive program or a
   pager (a bare `python` REPL, `less`/`more`, `git rebase -i`, an editor, anything that waits for
   input on stdin). If a command would wait for input, do not run it.
3. **Do not read files other than the two you will edit** (`scripts/runtime_role_binding_assert.py`,
   and — to match its existing test style — `tests/test_role_binding_enforcement.py`). No tree
   listings, no broad surveys.
4. **Do the writes FIRST, the long test runs LAST.** Target: all edits done within the first few
   minutes.
5. Use **native `apply_patch`** for every edit. One simple command per shell call.

## WRITE SET (the only files you may modify or create)

1. `tests/test_lane_effort_enforcement.py`   (CREATE — this is the RED fixture, write it first)
2. `scripts/runtime_role_binding_assert.py`  (MODIFY — the hunks below)
3. `TEST_RESULTS/**`                          (your own scratch: RED/GREEN logs, the receipt)

Nothing else. Do NOT touch `config/**`, `src/**`, `templates/`, `AGENTS.md`, or any other test file.
Do NOT run any git write command. No `pip install`. No network beyond the model transport already in
use.

Use exactly this interpreter for every Python command, by absolute path:
`C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`
(It carries the project's third-party deps, e.g. `jsonschema`. A bare `python` may resolve to an
interpreter without them and turn suite tests into FALSE failures.)

---

## ChangeSet B — enforce the EFFORT axis in the pre-dispatch role-mandate gate

Measured basis: `grep -c effort scripts/runtime_role_binding_assert.py` == 0. The round mandate
declares `reasoning_effort: medium` for PLAN and VERIFY/SECURITY and the pool entries for those arms
carry `reasoning_effort: "medium"`, but NOTHING compared the two, so a lane served at a different
effort was refused by nothing.

### Step 1 — CREATE `tests/test_lane_effort_enforcement.py` (write it byte-for-byte, then run it)

```python
"""M03 (round LANE-RELIABILITY-CLOSURE-20261016): the EFFORT axis of the pre-dispatch gate.

``scripts/runtime_role_binding_assert.py`` is the per-round role-mandate consumer: the owner order
names PLAN = ``gpt-6.1-sol`` MEDIUM and VERIFY/SECURITY = ``gpt-6.1-sol`` MEDIUM. Before this round
the script contained ZERO occurrences of ``effort``, so a lane served at a different reasoning effort
than the mandate declares was refused by NOTHING.

These tests drive the REAL script as a subprocess with synthetic mandate/pool fixtures -- the way the
dispatcher calls it -- and assert on the raw exit code and the typed code in stdout. They never import
the script and never assert on its source text.

Fixture shape: one lane (VERIFY_SECURITY) whose mandate declares ``medium`` and whose declared arm's
pool entry carries the effort under test. Every NEGATIVE asserts its OWN typed refusal code, and
``test_pos_matching_effort_passes`` is the POSITIVE CONTROL on the SAME fixture, so a refusal can
never pass for a reason other than the one the test names.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSERT = ROOT / "scripts" / "runtime_role_binding_assert.py"
TOOLCHAIN = ROOT / "config" / "hermes-codex-lane.json"
PY = sys.executable

PROVIDER = "openai-codex"
MODEL = "gpt-6.1-sol"


def _mandate(effort):
    role = {"provider": PROVIDER, "model": MODEL}
    if effort is not None:
        role["reasoning_effort"] = effort
    return {"schema": "HGK-ROLE-MANDATE/1", "round": "LANE-RELIABILITY-CLOSURE-20261016",
            "roles": {"VERIFY_SECURITY": role}}


def _pool(effort):
    entry = {"rank": 1, "provider": PROVIDER, "model": MODEL}
    if effort is not None:
        entry["reasoning_effort"] = effort
    return {"schema": "HGK-LANE-ROUTE-SLOTS/1",
            "lanes": [{"lane": "VERIFY_SECURITY", "ordered_pool": [entry]}]}


class LaneEffortEnforcement(unittest.TestCase):
    """One real assert-script subprocess per case; raw exit code + stdout are the oracle."""

    def _run(self, mandate_effort, pool_effort, served_effort=None):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="hgk-effort-", dir=str(ROOT.parent / "TEST_RESULTS")))
        mandate_file = tmp / "mandate.json"
        pool_file = tmp / "pool.json"
        mandate_file.write_text(json.dumps(_mandate(mandate_effort)), encoding="utf-8")
        pool_file.write_text(json.dumps(_pool(pool_effort)), encoding="utf-8")
        argv = [PY, "-B", str(ASSERT), "--mandate-file", str(mandate_file),
                "--lane", "VERIFY_SECURITY", "--pool", str(pool_file),
                "--toolchain-declaration", str(TOOLCHAIN)]
        if served_effort is not None:
            argv += ["--served-effort", served_effort]
        proc = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT),
                              timeout=300, check=False)
        try:
            body = json.loads(proc.stdout.strip().splitlines()[-1])
        except Exception:  # a non-JSON stdout is reported as-is, never masked
            body = {"raw_stdout_tail": proc.stdout[-400:]}
        return proc, body

    def test_pos_matching_effort_passes(self):
        """POSITIVE CONTROL: the same fixture the negatives use must SUCCEED."""
        proc, body = self._run("medium", "medium")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(body.get("ok"))
        self.assertEqual(body.get("declared_effort"), "medium")
        self.assertTrue(body.get("effort_verified"))

    def test_neg_mandate_effort_absent_from_pool_is_refused(self):
        proc, body = self._run("medium", None)
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL")

    def test_neg_effort_mismatch_is_refused(self):
        proc, body = self._run("medium", "high")
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_MANDATE_EFFORT_MISMATCH")

    def test_neg_served_effort_without_a_mandate_effort_is_unverifiable(self):
        proc, body = self._run(None, None, served_effort="medium")
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_SERVED_EFFORT_UNVERIFIABLE")

    def test_neg_served_effort_mismatch_is_refused(self):
        proc, body = self._run("medium", "medium", served_effort="high")
        self.assertEqual(proc.returncode, 7, proc.stdout + proc.stderr)
        self.assertEqual(body.get("code"), "ERR_SERVED_EFFORT_MISMATCH")

    def test_pos_lane_without_a_declared_effort_stays_a_pass_through(self):
        """The EXECUTE shape: a lane whose mandate names no effort is not silently failed."""
        proc, body = self._run(None, None)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue(body.get("ok"))
        self.assertFalse(body.get("effort_verified"))


if __name__ == "__main__":
    unittest.main()
```

Then run it and save the raw output to `TEST_RESULTS/RED.txt`:

```
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -B -m unittest tests.test_lane_effort_enforcement -v
```

Expected RED: real failures — the positives fail because `declared_effort`/`effort_verified` do not
exist yet, and the four negatives fail because the script exits 0 where the test demands exit 7. That
is the genuine absence of the behaviour. Record it, do not "fix" the tests.

### Step 2 — MODIFY `scripts/runtime_role_binding_assert.py` (four exact hunks)

**Hunk B-1a — new CLI option.** Find this exact block:

```python
    ap.add_argument("--session", default=None)
    ap.add_argument("--round", default=None)
    ap.add_argument("--subject", default=None)
    args = ap.parse_args()
```

Replace it with:

```python
    ap.add_argument("--session", default=None)
    ap.add_argument("--round", default=None)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--served-effort", default=None,
                    help="M03: the reasoning effort a receipt or startup header reported for this "
                         "lane's turn. When supplied it must equal the mandate's declared "
                         "reasoning_effort, else the run refuses.")
    args = ap.parse_args()
```

**Hunk B-1b — the enforcement block.** Find this exact block (the end of the chain check):

```python
        if chain_missing:
            print(json.dumps({"ok": False, "code": ERR_CODES["unresolved"],
                              "detail": {"stage": "chain", "why": f"chains arms absent from pool: {chain_missing}",
                                         "chain": chain}}, ensure_ascii=False))
            return 6

    result = {
```

Replace it with:

```python
        if chain_missing:
            print(json.dumps({"ok": False, "code": ERR_CODES["unresolved"],
                              "detail": {"stage": "chain", "why": f"chains arms absent from pool: {chain_missing}",
                                         "chain": chain}}, ensure_ascii=False))
            return 6

    # M03 (round LANE-RELIABILITY-CLOSURE-20261016): the EFFORT axis. The mandate declares a
    # per-lane `reasoning_effort` and the pool declares one on the arm; before this block NOTHING
    # compared them (measured: zero occurrences of "effort" in this file), so a lane served at a
    # different effort than the mandate names was refused by nothing. Fail closed on both ends
    # rather than assuming either side:
    #   ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL -- the mandate names an effort and the declared arm's
    #       pool entry carries none, so the declared effort cannot be checked at all;
    #   ERR_MANDATE_EFFORT_MISMATCH           -- mandate effort != the declared arm's pool effort;
    #   ERR_SERVED_EFFORT_UNVERIFIABLE        -- a served effort was supplied but the mandate names
    #       no effort to compare it against;
    #   ERR_SERVED_EFFORT_MISMATCH            -- a supplied served effort != the mandate's effort.
    # Exit code 7 is this axis's own, so the four outcomes stay distinguishable from the
    # mandate/pool/toolchain refusals above (2/3/4/5/6).
    declared_effort = declared.get("reasoning_effort")
    pool_effort = hit[0].get("reasoning_effort") if hit else None
    if declared_effort:
        if not pool_effort:
            print(json.dumps({"ok": False, "code": "ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL",
                              "detail": {"stage": "effort",
                                         "arm": f"{declared['provider']}/{declared['model']}",
                                         "mandate_effort": declared_effort,
                                         "why": "the declared arm's pool entry declares no reasoning_effort"}},
                             ensure_ascii=False))
            return 7
        if str(declared_effort) != str(pool_effort):
            print(json.dumps({"ok": False, "code": "ERR_MANDATE_EFFORT_MISMATCH",
                              "detail": {"stage": "effort",
                                         "arm": f"{declared['provider']}/{declared['model']}",
                                         "mandate_effort": declared_effort,
                                         "pool_effort": pool_effort}}, ensure_ascii=False))
            return 7
    if args.served_effort is not None:
        if not declared_effort:
            print(json.dumps({"ok": False, "code": "ERR_SERVED_EFFORT_UNVERIFIABLE",
                              "detail": {"stage": "effort", "served_effort": args.served_effort,
                                         "why": "the mandate declares no reasoning_effort for this lane"}},
                             ensure_ascii=False))
            return 7
        if str(args.served_effort) != str(declared_effort):
            print(json.dumps({"ok": False, "code": "ERR_SERVED_EFFORT_MISMATCH",
                              "detail": {"stage": "effort", "served_effort": args.served_effort,
                                         "mandate_effort": declared_effort}}, ensure_ascii=False))
            return 7

    result = {
```

**Hunk B-1c — report the axis in the success payload.** Find this exact block inside `result`:

```python
        "binding_checked": bool(bound.get("binding_checked")),
        "binding_digest": bound.get("binding_digest"),
        "claim_ceiling": CLAIM_CEILING,
    }
```

Replace it with:

```python
        "binding_checked": bool(bound.get("binding_checked")),
        "binding_digest": bound.get("binding_digest"),
        "declared_effort": declared_effort,
        "pool_effort": pool_effort,
        "effort_verified": bool(declared_effort and pool_effort
                                and str(declared_effort) == str(pool_effort)),
        "claim_ceiling": CLAIM_CEILING,
    }
```

**Hunk B-1d — extend the claim ceiling.** Find:

```python
CLAIM_CEILING = ("DECLARATION_ONLY: this asserts the per-round role declaration is present and "
                 "internally consistent with the persisted binding/pool/toolchain. It does NOT prove "
                 "any role executed, and it does NOT prove a model was served. The legacy selector "
                 "path below (no --binding) proves even less: it checks the mandate selector only.")
```

Replace with:

```python
CLAIM_CEILING = ("DECLARATION_ONLY: this asserts the per-round role declaration is present and "
                 "internally consistent with the persisted binding/pool/toolchain, INCLUDING the "
                 "reasoning-effort axis (mandate effort vs the declared arm's pool effort, and an "
                 "explicitly supplied --served-effort when given). It does NOT prove any role "
                 "executed, and it does NOT prove a model was served. The legacy selector path "
                 "below (no --binding) proves even less: it checks the mandate selector only.")
```

If a hunk's "find" text is not present VERBATIM, stop and report the mismatch in your receipt — do
not invent a nearby variant.

### Step 3 — run the focused tests GREEN, save to `TEST_RESULTS/GREEN.txt`

```
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -B -m unittest tests.test_lane_effort_enforcement tests.test_role_binding_enforcement -v
```

### Step 4 — emit the receipt EARLY, then run the named acceptance command

Write `TEST_RESULTS/BUILD_RECEIPT.json` as soon as step 3 is green, then run and append:

```
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -B -m unittest tests.test_lane_effort_enforcement tests.test_governed_runtime_controller tests.test_role_binding_enforcement tests.test_mandatory_tool_guard tests.test_matrix_d_full
```

Expected: **all green** (this attempt does NOT include ChangeSet C, so do not expect a new
controller case and do not add one). If a pre-existing test in those files goes red, do NOT edit it:
record the exact test name and refusal text, then STOP editing and report it in the receipt as a
finding.

Also record `grep -c effort scripts/runtime_role_binding_assert.py` (expected > 0 after the hunks).

## YOUR CLOSING RECEIPT (`TEST_RESULTS/BUILD_RECEIPT.json`)

```json
{
  "round": "LANE-RELIABILITY-CLOSURE-20261016",
  "lane": "EXECUTE",
  "attempt": "BC2",
  "changeset": ["B (M03 effort axis)"],
  "files_written": ["<path>:<sha256-12>"],
  "red_evidence": "TEST_RESULTS/RED.txt",
  "green_evidence": "TEST_RESULTS/GREEN.txt",
  "named_acceptance_command": "<the exact command>",
  "named_acceptance_result": "<verbatim tail, including the Ran N tests line>",
  "m03_probe": "grep -c effort scripts/runtime_role_binding_assert.py -> <number>",
  "unexpected_reds": [],
  "claim_ceiling": "A writer's own green run is a CLAIM. It is not verification and not acceptance; an independent checker lane re-derives every number in this receipt."
}
```

Your final answer MUST end with the standalone transport token given in the footer, on its own line.
