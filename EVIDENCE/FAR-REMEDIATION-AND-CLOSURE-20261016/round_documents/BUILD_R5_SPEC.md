# BUILD — R5 (EXECUTE lane, EDIT-ONLY turn)

Round `FAR-REMEDIATION-AND-CLOSURE-20261016`, WorkOrder `WO-FAR-REMEDIATION-AND-CLOSURE-20261016-EXECUTE`.
Ruling item: **R5** of `FAR_RULING.md`.

## Your role

You are the bounded writer on the EXECUTE lane. Your provider/model is fixed by the dispatch contract
(`opencode-go` / `deepseek-v4.1-flash`) and is asserted by the orchestrator, not by you.

## What this turn is

An **EDIT-ONLY** turn. You write files. You do **not** run the test suite, you do **not** run git, you do
**not** run any project command, and you do **not** try to prove your own work. The orchestrator owns the
oracle and re-derives your change independently. This is deliberate: two earlier attempts on this lane
stalled for 900 s each when the writer turn also tried to run the oracle.

## The change (additive only — no existing flag may change meaning)

File: `scripts/hgk-lane-dispatch.py` (write the result to `candidate/scripts/hgk-lane-dispatch.py`).

1. In the argparse block of `main()` — the block that already defines `--prompt` (near line 1365) — add:

   ```python
   ap.add_argument("--turn-shape", choices=("normal", "edit_only"), default="normal",
                   help="edit_only prepends a fixed HARD RULES block to the prompt and forbids the "
                        "behaviours measured to stall a bounded-writer turn; the shape used is recorded "
                        "in the attempt record. Default keeps the previous behaviour exactly.")
   ```

2. Add a module-level constant next to the other module constants, holding the fixed block. It must say,
   at minimum: write files only; do not run the test suite, git or any project command; do not attempt to
   prove your own work; state plainly what you could not do; emit one final JSON line. Keep it short and
   imperative. Name it `HARD_RULES_EDIT_ONLY`.

3. At the point where the prompt is handed to the codex process — `cmd += ["exec", "--skip-git-repo-check",
   "--ephemeral", "--json", args.prompt]` (line 1089) — compute the effective prompt **once**:

   ```python
   effective_prompt = (HARD_RULES_EDIT_ONLY + "\n\n" + args.prompt) if args.turn_shape == "edit_only" else args.prompt
   ```

   and use `effective_prompt` in that `cmd` instead of `args.prompt`. `effective_prompt` must be defined in
   the same function that builds that `cmd`, so no other call site changes.

4. Record the shape in the attempt record (the dict the file already serialises, and the same dict written
   to `--json-out`): add the key `turn_shape` with the value actually used, and `turn_shape_prompt_chars`
   with the length of the prefix actually prepended (0 for `normal`). Do not remove or rename any existing
   key.

## Typed RED-first test

New file `candidate/tests/test_lane_turn_shape.py`. It must:

- assert that with `--turn-shape normal` (and when the flag is omitted) the effective prompt equals the
  prompt argument exactly, and `turn_shape == "normal"`, `turn_shape_prompt_chars == 0`;
- assert that with `edit_only` the effective prompt **starts with** the HARD RULES constant and still ends
  with the original prompt text;
- assert that argparse **rejects** any value outside `{normal, edit_only}` with a non-zero exit
  (`SystemExit` from argparse counts);
- be written so it fails against the pre-change file, and pass against yours. State in your final message
  whether you actually observed the pre-change failure — if you did not run it, say so, and say that the
  orchestrator will re-derive it.

## Hard rules for this turn

- Write only these two paths. No other file, no repository configuration, no new dependency.
- Do not run `python -m unittest`, `pytest`, `git`, or any project CLI. Do not spawn subprocesses.
- Do not edit `tests/`, `src/`, or any config to make anything pass.
- Do not claim any verification you did not personally perform on the file contents alone.
- If something in this brief is impossible or self-contradictory, say so plainly rather than inventing a
  workaround; an honest refusal is a valid outcome.

## Final message

End with exactly one JSON line:

`{"ok": bool, "files_written": [paths], "hard_rules_const": "<the exact constant name>", "effective_prompt_computed_once": bool, "receipt_keys_added": [keys], "pre_change_failure_observed": "yes"|"no"|"not_run", "notes": "..."}`
