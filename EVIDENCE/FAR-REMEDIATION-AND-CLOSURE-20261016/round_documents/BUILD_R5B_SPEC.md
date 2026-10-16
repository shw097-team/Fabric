# BUILD — R5b (EXECUTE lane, EDIT-ONLY turn) — re-dispatched with a CORRECTED brief

Round `FAR-REMEDIATION-AND-CLOSURE-20261016`, WorkOrder `WO-FAR-REMEDIATION-AND-CLOSURE-20261016-EXECUTE`.
Ruling item: **R5** of `FAR_RULING.md`. This replaces the R5 brief, which was ambiguous about where to
write and cost the previous attempt its whole window (see `lanes/EXECUTE/R5/TERMINATION.json`).

## Where you are, and where you write (read this first — the previous attempt failed here)

Your sandbox root **is** this directory:

```
C:/Projects/Agent_Workspace/HG-KSEOS/var/FAR-REMEDIATION-AND-CLOSURE-20261016/candidate
```

It is writable. **Do not test whether it is writable, do not probe for other writable locations, and do
not create scratch or probe files.** All paths you write are relative to the root above:

- write `scripts/hgk-lane-dispatch.py`  → i.e. the file at `<root>/scripts/hgk-lane-dispatch.py`
- write `tests/test_lane_turn_shape.py` → i.e. a NEW file at `<root>/tests/test_lane_turn_shape.py`

Do not write `candidate/...` inside the root: that would create `<root>/candidate/...`, which is wrong.
A copy of the current `scripts/hgk-lane-dispatch.py` is already there; edit it in place.

## Your role

You are the bounded writer on the EXECUTE lane. Your provider/model is fixed by the dispatch contract
(`opencode-go` / `deepseek-v4.1-flash`) and is asserted by the orchestrator, not by you.

## What this turn is

An **EDIT-ONLY** turn. You write files. You do **not** run the test suite, you do **not** run git, you do
**not** run any project command, and you do **not** try to prove your own work. The orchestrator owns the
oracle and re-derives your change independently. This is deliberate: bounded-writer turns on this lane have
stalled for 900 s each when the writer also tried to run the oracle.

## The change (additive only — no existing flag may change meaning)

In `scripts/hgk-lane-dispatch.py`:

1. In the argparse block of `main()`, the block that already defines `--prompt` (around line 1365), add:

   ```python
   ap.add_argument("--turn-shape", choices=("normal", "edit_only"), default="normal",
                   help="edit_only prepends a fixed HARD RULES block to the prompt and forbids the "
                        "behaviours measured to stall a bounded-writer turn; the shape used is recorded in "
                        "the attempt record. The default keeps the previous behaviour exactly.")
   ```

2. Add a module-level constant beside the other module constants holding a short, imperative block. It
   must say: write files only; do not run the test suite, git or any project command; do not attempt to
   prove your own work; state plainly what you could not do; emit one final JSON line. Name it
   `HARD_RULES_EDIT_ONLY`.

3. Where the prompt is handed to the codex process —
   `cmd += ["exec", "--skip-git-repo-check", "--ephemeral", "--json", args.prompt]` (about line 1089) —
   compute the effective prompt **once, in that same function**:

   ```python
   effective_prompt = (HARD_RULES_EDIT_ONLY + "\n\n" + args.prompt) if args.turn_shape == "edit_only" else args.prompt
   ```

   and use `effective_prompt` in that `cmd`. No other call site changes.

4. Record the shape in the attempt record (the dict the file already serialises, and the one written to
   `--json-out`): add `turn_shape` with the value actually used, and `turn_shape_prompt_chars` with the
   length of the prefix actually prepended (0 for `normal`). Do not remove or rename any existing key.

## Typed RED-first test

New file `tests/test_lane_turn_shape.py`, which must:

- assert that with `--turn-shape normal` — and when the flag is omitted — the effective prompt equals the
  prompt argument exactly, with `turn_shape == "normal"` and `turn_shape_prompt_chars == 0`;
- assert that with `edit_only` the effective prompt **starts with** the HARD RULES constant and still ends
  with the original prompt text;
- assert that argparse **rejects** a value outside `{normal, edit_only}` with a non-zero exit
  (`SystemExit` from argparse counts);
- be written so that it FAILS against the pre-change file and PASSES against yours. In your final message,
  state whether you actually observed the pre-change failure; if you did not run it, say so and say that
  the orchestrator will re-derive it.

## Hard rules for this turn

- Write only those two paths. No other file, no repository configuration, no new dependency.
- Do not run `python -m unittest`, `pytest`, `git`, or any project CLI. Do not spawn subprocesses.
- Do not edit `tests/fixtures/`, `src/`, or any config to make anything pass.
- Do not claim any verification you did not personally perform on the file contents alone.
- If something here is impossible or self-contradictory, say so plainly rather than inventing a workaround.
  An honest refusal is a valid outcome.

## Final message

End with exactly one JSON line:

`{"ok": bool, "files_written": [paths], "hard_rules_const": "<name>", "effective_prompt_computed_once": bool, "receipt_keys_added": [keys], "pre_change_failure_observed": "yes"|"no"|"not_run", "notes": "..."}`
