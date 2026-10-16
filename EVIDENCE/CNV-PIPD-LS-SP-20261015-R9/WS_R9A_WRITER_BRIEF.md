# WS-R9-A WRITER BRIEF — adapt the R7-0 validator hardening to main's newer contract

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R9-0` · HGK project `CNV-R9-FARCLOSURE` (WO-TS-FARCLOSURE-04)
Role: bounded writer (Codex CLI EXECUTE lane). Authority: PKG v2.0.0 + EIA-R6-04 + the R8-0 finding `BLK-R8-WS2-MAIN-DIVERGENCE`.
**Claim ceiling: LOCAL / candidate-only.** A green run here is not an acceptance and not a Gate PASS.

FIRST LINE OF YOUR FIRST MESSAGE and LAST LINE OF YOUR FINAL MESSAGE must both be exactly:
`R9A-WSRITER-NONCE-7f3c1d`

## 0. Answer this in one line before you touch anything

Does `r8-wt` still carry the R8-0 hardening (3 modified files) and do the two named tests still fail there? If they now pass, STOP and report that instead of editing.

## 1. Work root and write set (hard limits)

- Worktree: `C:/Projects/Agent_Workspace/PIPD/worktrees/r8-wt` (git branch state: base `dba4b19456777d3b597fdf71480f6423dd974243`, three files modified and uncommitted: `src/pipd_ls_sp/validate.py`, `src/pipd_ls_sp/pipeline.py`, `src/pipd_ls_sp/cli.py`).
- You may edit ONLY `src/pipd_ls_sp/validate.py` (and only the two regions named in §3).
- You may write your receipt and logs ONLY into `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R9/WS_A/` (create it).
- Interpreter (pin it absolutely, do not rely on `python` resolving): `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.
- Forbidden: any git write command (no add/commit/branch/checkout/stash/reset) and sending anything to any outside host; editing any other file anywhere; reading or printing any credential file; touching `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/**`; touching `C:/Projects/wt-r8-cleanmain`.
- Do not weaken any check to make a test pass. If the specified change cannot make both tests pass without weakening the hardening, STOP and report the conflict with evidence.

## 2. The two failures you must fix (measured, base = main)

1. `tests/test_s4ext_trace_closure.py::LegalTraceStillPassesTests::test_real_trace_link_is_legal_beside_its_endpoints`
   Cause: the test calls `validate_bundle(bundle, schemas_dir)` with **no** frozen context. The hardened `validate.py:224-235` sees `fc.get("trace_endpoint_hashes") is None` and emits `TraceLink: UNBOUND_FROZEN_CONTEXT` for both endpoints even though the bundle itself carries the atoms that give those endpoints their frozen digests.
2. `tests/test_tooling_executes.py::TestToolingExecutes::test_cli_smoke_runs`
   Cause: `cli.py:175-176` passes the `PI-PKG` **dict** into `derive_frozen_context()`, whose line 434 does `((atom.get("risk_guard") or {}).get("oracle") or {})`. In main's newer fixture `risk_guard` is a non-empty **string**, so `.get` raises `AttributeError: 'str' object has no attribute 'get'`.

## 3. The specified change (apply exactly these two hunks; do not redesign)

### Hunk 1 — `validate_bundle()`: derive the context from the bundle when none was supplied
Anchor: immediately AFTER the empty-bundle guard, i.e. after the `return {...}` block that reports `"empty bundle: zero records checked cannot be a PASS"` (currently lines 388-391) and BEFORE `for contract, record in bundle.items():` (currently line 392). Insert:

```python
    # R9-0 (BLK-R8-WS2): when the caller supplies no frozen context, discharge the endpoint /
    # oracle bindings against the bundle's OWN atoms instead of failing closed. Each atom's
    # frozen digest is its own content_hash, which the record-level self-digest check already
    # verifies, so this adds a resolvable binding without removing one: a caller-supplied
    # context is never overridden, and a supplied context that lacks an endpoint still fails
    # closed in semantic_invariants.
    if frozen_context is None:
        derived: dict[str, Any] = {}
        for _c, _rec in bundle.items():
            if not isinstance(_rec, dict):
                continue
            for _atom in ((_rec.get("stable_semantic_contract") or {}).get("atoms") or []):
                if isinstance(_atom, dict) and _atom.get("subject_id") and _atom.get("content_hash"):
                    derived.setdefault("trace_endpoint_hashes", {}).setdefault(
                        str(_atom["subject_id"]), str(_atom["content_hash"]))
                _rg = _atom.get("risk_guard") if isinstance(_atom, dict) else None
                _oracle = _rg.get("oracle") if isinstance(_rg, dict) else None
                if isinstance(_atom, dict) and _atom.get("req_id") and isinstance(_oracle, dict) \
                        and _oracle.get("expected") is not None:
                    derived.setdefault("oracle_expected", {}).setdefault(
                        str(_atom["req_id"]), _oracle["expected"])
            if isinstance(_rec, dict) and _rec.get("subject_id") and _rec.get("content_hash"):
                derived.setdefault("trace_endpoint_hashes", {}).setdefault(
                    str(_rec["subject_id"]), str(_rec["content_hash"]))
        frozen_context = derived or None
```
(`Any` is already imported in this module — verify before inserting; if it is not, add it to the existing `typing` import rather than using a new import line.)

### Hunk 2 — `derive_frozen_context()`: guard the string-vs-mapping case
Replace the single line currently at 434:
```python
            oracle = ((atom.get("risk_guard") or {}).get("oracle") or {})
```
with:
```python
            # R9-0 (BLK-R8-WS2): `risk_guard` may be a free-text string in a submitted PI, so the
            # mapping access is guarded: an unusable shape yields no oracle expectation rather than
            # an AttributeError, and the fail-closed branch for that binding still fires.
            rg = atom.get("risk_guard")
            oracle = (rg.get("oracle") if isinstance(rg, dict) else {}) or {}
```

## 4. Acceptance commands (run all of them; paste raw output into your receipt)

1. `python -m pytest tests -q -p no:cacheprovider -k "test_real_trace_link_is_legal_beside_its_endpoints or test_cli_smoke_runs"` → **expect `2 passed`**.
2. NEGATIVE CONTROL (must still refuse — proves the fix did not open the hole the R7-0 hardening closed): run the mutation probes for M04, M06 and M16 with the round's own runner in the worktree, e.g. `python <the worktree's mutation runner> m04` (find it; the R8-0 run produced MUTATIONS_18_ON_MAIN receipts under `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R8/WS_B/RAW/` — reuse those exact invocation shapes and keep their raw JSON out of the worktree). → **expect `observed=REJECT`, `validator_verdict=FAIL` for each of M04/M06/M16**.
3. `python -m pytest tests -q -p no:cacheprovider` (full suite; it took ~206 s in R8-0) → paste `N failed, M passed` verbatim.
4. `git -c core.pager=cat diff --stat` (READ-ONLY; this is not a write command) → expect `pipeline.py` unchanged by you and `validate.py` carrying exactly your two hunks.

## 5. Receipt (required, before you finish)

Write `WS_A/WS_R9A_RECEIPT.json` + `WS_A/WS_R9A_RAW.md` containing: the §0 answer; the two hunks as applied (with line numbers after the edit); the raw output of every §4 command; the mutation receipts; an explicit statement of what you did NOT run; and any blocker with its raw error. Then write `WS_A/WS_R9A_DONE` containing only your nonce.

Do not claim that the fix is correct beyond the commands above. If a command fails, record it as a failure rather than adjusting the command.
