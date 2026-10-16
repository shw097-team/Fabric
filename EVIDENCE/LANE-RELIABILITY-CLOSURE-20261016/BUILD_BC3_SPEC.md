# BUILD brief — B + C, EDIT-ONLY attempt (round LANE-RELIABILITY-CLOSURE-20261016, lane EXECUTE, BC3)

Attempts `BC1` and `BC2` both died after writing their first file and then STARTING COMMANDS. BC2's
saved evidence: the model wrote `tests/test_lane_effort_enforcement.py` (11:30:24, 5161 bytes, correct),
then made no further write for six minutes while its `codex.exe` burned no CPU and held no socket.

So this brief removes that whole risk surface: **you are an EDIT-ONLY turn.** You apply patches and
write files. You do NOT run anything. The orchestrator owns the test oracle and runs every suite
itself, outside your turn.

## HARD RULES (violating any one wastes the turn)

1. **Do NOT run any shell command other than `apply_patch`.** No `python`, no `unittest`, no
   `grep`, no `dir`, no `tasklist`/`ps`/`netstat`/`Get-*`. Nothing that enumerates processes.
2. Never start an interactive program or a pager.
3. Do not read any file except the three you will patch.
4. When the four patches below are applied, STOP. Print the transport token from the footer as your
   final message. That token is not a verdict.

## WRITE SET

1. `scripts/runtime_role_binding_assert.py`            (patch — hunks B-1a, B-1b, B-1c, B-1d)
2. `scripts/hgk-governed-runtime-controller.py`        (patch — hunks C-1a, C-1b)
3. `tests/test_governed_runtime_controller.py`         (patch — append 3 cases, hunk C-2)
4. `tests/test_lane_effort_enforcement.py`             **ALREADY CORRECT — DO NOT TOUCH IT**

Nothing else. Do not create any other file, do not touch `config/**`, `src/**` or any other test.

If a hunk's "find" text is not present VERBATIM, do not invent a nearby variant: apply the rest and
report the mismatch in your final message.

---

## ChangeSet B — enforce the EFFORT axis in the pre-dispatch role-mandate gate

### Hunk B-1a — new CLI option

FIND:

```python
    ap.add_argument("--session", default=None)
    ap.add_argument("--round", default=None)
    ap.add_argument("--subject", default=None)
    args = ap.parse_args()
```

REPLACE WITH:

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

### Hunk B-1b — the enforcement block

FIND:

```python
        if chain_missing:
            print(json.dumps({"ok": False, "code": ERR_CODES["unresolved"],
                              "detail": {"stage": "chain", "why": f"chains arms absent from pool: {chain_missing}",
                                         "chain": chain}}, ensure_ascii=False))
            return 6

    result = {
```

REPLACE WITH:

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

### Hunk B-1c — report the axis in the success payload

FIND:

```python
        "binding_checked": bool(bound.get("binding_checked")),
        "binding_digest": bound.get("binding_digest"),
        "claim_ceiling": CLAIM_CEILING,
    }
```

REPLACE WITH:

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

### Hunk B-1d — extend the claim ceiling

FIND:

```python
CLAIM_CEILING = ("DECLARATION_ONLY: this asserts the per-round role declaration is present and "
                 "internally consistent with the persisted binding/pool/toolchain. It does NOT prove "
                 "any role executed, and it does NOT prove a model was served. The legacy selector "
                 "path below (no --binding) proves even less: it checks the mandate selector only.")
```

REPLACE WITH:

```python
CLAIM_CEILING = ("DECLARATION_ONLY: this asserts the per-round role declaration is present and "
                 "internally consistent with the persisted binding/pool/toolchain, INCLUDING the "
                 "reasoning-effort axis (mandate effort vs the declared arm's pool effort, and an "
                 "explicitly supplied --served-effort when given). It does NOT prove any role "
                 "executed, and it does NOT prove a model was served. The legacy selector path "
                 "below (no --binding) proves even less: it checks the mandate selector only.")
```

---

## ChangeSet C — the controller's absent-session-id OUTAGE

Measured basis (the previous round's own receipt, `R3_ACTIVATION_RECEIPT.json::new_finding`):
`mandatory_tool_guard.check_tool_call` sends `session_id = getattr(agent,"session_id","") or ""` and
allows ONLY on exit 0. `role_binding.find_session_binding` RAISES on a blank id by design, and the
controller maps ANY exception to exit 3 — so an agent with no session id has EVERY mutating call
refused.

### Hunk C-1a — the answer

FIND:

```python
    # From here on a mutating call either reaches a protected root or (free text) cannot be shown
    # not to; it may only be allowed by a genuine non-maker session. Everything below is fail-closed.
    try:
        _ensure_src_on_path()
        from hg_kseos import role_binding as _role_binding  # noqa: PLC0415

        spine = _load_spine()
        found = _role_binding.find_session_binding(spine, payload.get("session_id"))
    except Exception:  # noqa: BLE001 - an unacquirable boundary is a refusal, never a pass
        return 3
```

REPLACE WITH:

```python
    # From here on a mutating call either reaches a protected root or (free text) cannot be shown
    # not to; it may only be allowed by a genuine non-maker session. Everything below is fail-closed.
    #
    # ABSENT/BLANK session id (finding CONTROLLER-ABSENT-SESSION-ID-FAILCLOSED, closed by round
    # LANE-RELIABILITY-CLOSURE-20261016). A governed binding REQUIRES a non-empty session:
    # ``validate_binding`` refuses a blank one and ``find_session_binding`` raises
    # ERR_ROLE_BINDING_SESSION_REQUIRED for it. So a call carrying no session id cannot belong to a
    # governed round -- there is no binding keyed by "" to protect. Mapping its typed refusal to
    # exit 3 was an OUTAGE, not a control: the guard sends ``getattr(agent,"session_id","") or ""``,
    # so ANY agent without a session id had EVERY mutating call refused. It was also inconsistent
    # with the already-allowed unknown-id case (a valid-but-unknown id returns None => allow).
    # Answer the contract instead, with a reason a reader can tell apart from "no governed round".
    session_id = payload.get("session_id")
    if not (isinstance(session_id, str) and session_id.strip()):
        return _emit({"action": "allow", "reason": "no-session-id-unattributable"}, 0)

    try:
        _ensure_src_on_path()
        from hg_kseos import role_binding as _role_binding  # noqa: PLC0415

        spine = _load_spine()
        found = _role_binding.find_session_binding(spine, session_id)
    except Exception:  # noqa: BLE001 - an unacquirable boundary is a refusal, never a pass
        return 3
```

(If `_emit` is not the module's emit helper, find the name it uses to print its answer object and use
that instead — one helper call, same payload, exit 0.)

### Hunk C-1b — the module docstring's governance rule

FIND:

```python
Governance rule: inside a governed round a MAKER (EXECUTE) must not write to a protected root
out-of-band; a CHECKER (VERIFY/SECURITY) may inspect. Ordinary sessions and calls that touch no
protected root are allowed unchanged.
```

REPLACE WITH:

```python
Governance rule: inside a governed round a MAKER (EXECUTE) must not write to a protected root
out-of-band; a CHECKER (VERIFY/SECURITY) may inspect. Ordinary sessions and calls that touch no
protected root are allowed unchanged. A call carrying NO session id cannot be attributed to a
governed round at all (a binding requires a non-empty session), so it is answered as
``no-session-id-unattributable`` rather than turned into an exit-3 outage that would refuse every
mutating call of an agent whose session id is absent.
```

### Hunk C-2 — append 3 cases to `tests/test_governed_runtime_controller.py`

Insert these three methods immediately BEFORE the trailing block

```python
if __name__ == "__main__":
    unittest.main()
```

keeping that block exactly as it is, at the same indentation as the file's other `test_*` methods:

```python
    def test_pos_absent_session_id_is_answered_not_an_outage(self):
        """CONTROLLER-ABSENT-SESSION-ID-FAILCLOSED: a blank session id must be ANSWERED.

        The guard sends ``getattr(agent,"session_id","") or ""``; ``find_session_binding`` refuses a
        blank id by design, and mapping that to exit 3 made the guard refuse EVERY mutating call for
        any agent without a session id. This case asserts the ANSWER and its OWN reason string.
        POSITIVE CONTROL on the SAME fixture: ``test_neg_maker_write_inside_protected_denied``
        presents a REAL session id and must still deny.
        """
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m",
                                                  "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")}, "", home),
                         db, home)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        body = self._json(proc)
        self.assertEqual(body["action"], "allow")
        self.assertEqual(body["reason"], "no-session-id-unattributable")

    def test_pos_null_session_id_is_answered_not_an_outage(self):
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m",
                                                  "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("write_file", {"path": str(protected / "x.py")}, None, home),
                         db, home)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        body = self._json(proc)
        self.assertEqual(body["action"], "allow")
        self.assertEqual(body["reason"], "no-session-id-unattributable")

    def test_pos_absent_session_id_free_text_is_answered_not_an_outage(self):
        """The unresolvable free-text class is answered the same way, not turned into a refusal."""
        tmp, protected, home = self._workspace()
        db = self._seed_spine(tmp, [("TS-M", WO, "sess-maker",
                                     {"EXECUTE": {"provider": "p", "model": "m",
                                                  "surface": "s", "rank": 1}})])
        proc = self._run(self._payload("terminal", {"command": "echo x > x.py"}, "", home), db, home)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        body = self._json(proc)
        self.assertEqual(body["action"], "allow")
        self.assertEqual(body["reason"], "no-session-id-unattributable")
```

---

## YOUR FINAL MESSAGE

Report, in plain text: the three file paths you patched, whether every hunk's FIND text was present
verbatim, and any hunk you could not apply. Then print the standalone transport token from the footer
on its own line. Do not run the suites — the orchestrator does that next.
