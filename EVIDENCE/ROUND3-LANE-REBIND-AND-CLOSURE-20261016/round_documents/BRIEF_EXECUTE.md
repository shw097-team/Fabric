# BRIEF — EXECUTE lane, bounded writer turn (EDIT-ONLY)

You are the EXECUTE bounded writer for round ROUND3-LANE-REBIND-AND-CLOSURE-20261016 of HG-KSEOS.
Your model appointment is BY OWNER ORDER: `opencode-go/deepseek-v4.1-flash` (CODEX CLI, sealed lane home).
Your workspace is the round's `candidate/` tree (a byte-identical copy of the canonical
`scripts/ src/ tests/ config/` trees). Write ONLY inside that tree, and ONLY the files listed in WRITE SET.

## Why this change is necessary (measured, not theoretical)

The owner order of 2026-10-16 puts the VERIFY/SECURITY checker on `opencode-go/deepseek-v4.1-flash` — the
SAME model the EXECUTE writer holds. That collision is legitimate here (owner-ordered), and the registry
already declares it:

* `config/lane-routing-registry.yaml` → `sod_invariants.pairs`: the EXECUTE/VERIFY_SECURITY entry is demoted
  to `distinct_required: false`;
* the same file → `sod_invariants.declared_conflicts` carries `SOD006-C3` for that exact pair with
  `status: OWNER_ORDERED_IN_FORCE`;
* `tests/test_lane_policy.py` states the product's intended semantics in its own words: for a demoted pair
  "the sweep must then assert the DECLARATION exists instead of asserting separation".

But the pre-dispatch gate disagrees with its own product. `scripts/hgk-lane-guard.py` calls the pure
`lane_policy.check_sod(maker_model, target_model)` and refuses ANY pair whose normalized model tokens are
equal. Measured today against the live registry:

    exit 2, ERR_LANE_SOD_VIOLATION, "SOD_VIOLATION maker_model=deepseek-v4.1-flash == checker_model=deepseek-v4.1-flash"

So the owner's own mandate cannot be dispatched at all: the gate is stricter than the order it exists to
serve, and it silently ignores the declaration the registry and the conformance test both honour. Your turn
makes the two surfaces agree WITHOUT opening a hole for an undeclared collision.

## TASK (additive only — no existing flag may change meaning)

1. `src/hg_kseos/lane_policy.py` — add a small pure helper that answers, from the registry document alone,
   whether a same-model (maker lane, checker lane) pair is EXEMPTED BY AN OWNER-ORDERED DECLARATION.
   It must require BOTH of these, and nothing weaker:
   * `sod_invariants.pairs` contains an entry whose `maker`/`checker` match the pair (either orientation)
     AND whose `distinct_required` is false;
   * `sod_invariants.declared_conflicts` contains an entry listing that EXACT pair whose `status` is
     exactly `OWNER_ORDERED_IN_FORCE`.
   Return the conflict id when exempted, else None plus a short reason. Keep the existing
   `check_sod(maker, checker)` semantics untouched — it is a pure two-token comparison and other callers
   rely on that.

2. `scripts/hgk-lane-guard.py` — in the `sod_distinct_model` check ONLY:
   * add an OPTIONAL `--maker-lane` argument (`PLAN|EXECUTE|VERIFY_SECURITY`). Additive: omitting it must
     leave today's behaviour intact except where the exemption below legitimately applies.
   * when the maker lane is omitted, infer it ONLY IF exactly one route's default arm (`provider` + `model`,
     compared both with and without the `provider/` prefix) equals `--maker-model`; if the match is
     ambiguous or absent, do NOT exempt (fail closed).
   * when the pure check reports a collision, consult the helper: if the pair is exempted, the check passes
     and the verdict MUST carry the conflict id (e.g. `"declared_conflict": "SOD006-C3"`) with a detail that
     names it, so the exemption is VISIBLE in every receipt and never silent. Exit code stays 0 (ADMIT) in
     that case only.
   * an undeclared same-model pair must still fail exactly as today: exit 2, `ERR_LANE_SOD_VIOLATION`.
   * touch nothing else: `source_digest`, `epoch_current`, `expected_epoch_assertion` and `arm_admitted`
     keep their present behaviour byte for byte.

3. `tests/test_lane_guard.py` (extend it; do not weaken existing cases) — RED-FIRST, against real
   production behaviour, never a post-hoc stub. Cover at least:
   * undeclared same-model pair → exit 2 `ERR_LANE_SOD_VIOLATION` (the regression that must NOT move);
   * declared owner-ordered pair (build a registry fixture carrying the pair + `SOD006-C3`) → ADMIT, and the
     verdict contains the conflict id;
   * distinct pair → ADMIT, unchanged, with no `declared_conflict` field;
   * a pair that is NAMED by the declaration but whose `distinct_required` is still true, or whose status is
     not `OWNER_ORDERED_IN_FORCE` → still exit 2 (prove the exemption cannot be widened).

## RULES

* Show the RED run before the fix and the GREEN run after it, verbatim, in your report.
* Do NOT run the repository test suites (no `pytest`, no `unittest discover`, no full-tree sweep). The
  orchestrator owns the oracle.
* No new dependency, no network, no git write, no credential access, no change outside WRITE SET.
* Keep the diff minimal and literal. Match the existing code's style (typed exit codes, `checks[]` entries,
  `sort_keys=True` JSON emission).

## WRITE SET

    src/hg_kseos/lane_policy.py
    scripts/hgk-lane-guard.py
    tests/test_lane_guard.py

## REPORT (your final message, after the transport token line requirement below)

1. The exact commands you ran and their observed output (RED then GREEN).
2. `git diff --stat`-equivalent: the files you changed and the line counts.
3. Any part of the task you could not complete, stated plainly, with the measured reason.
