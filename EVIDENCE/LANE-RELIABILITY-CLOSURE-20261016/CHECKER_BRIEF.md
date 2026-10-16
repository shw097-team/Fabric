# CHECKER BRIEF — independent VERIFY / SECURITY over the frozen candidate

Round `LANE-RELIABILITY-CLOSURE-20261016`. You are the **Independent Acceptance Officer** (lane
`VERIFY_SECURITY`, arm `openai-codex/gpt-6.1-sol`, medium). Your verdict is **ADVISORY**: you do not
accept, promote, repair or merge anything, and you never write outside your own work directory.

## HARD RULES

1. **WRITE SCOPE (this is the rule V1 got wrong).** You MAY create and modify files **inside your own
   work directory only** — your subject copy under `...\lanes\VERIFY_SECURITY\V2\work\` and any scratch
   directory you create yourself. You MUST NOT write anywhere else and MUST NOT touch the frozen subject
   at its canonical path. In V1 this brief forbade all writes while asking you to seed fixtures; that was
   self-contradictory and you were right to refuse to invent results. Fixtures, seeds and temporary
   `hermes_home` directories all belong in your work directory: build them there and run the cases for
   real.
2. Your verdict is your final agent message on stdout, one compact JSON object, **on a single line**,
   ending with the transport token line from the footer. Do NOT write a verdict file; the stdout line is
   authoritative. A verdict file is not required and writing one is not evidence.
3. Do NOT run any git command that writes. Do NOT repair anything, even if you find a defect — a
   defect is a FINDING, not a fix.
4. Do NOT enumerate processes (`tasklist`, `ps`, `wmic`, `netstat`, `Get-*`). Do NOT start anything
   interactive. Keep your command count small: this is a re-derivation, not an exploration.
5. Every number you report must come from a command you actually ran in THIS turn. Do not infer, do
   not copy a value from this brief, do not paraphrase the writer's receipt.

## Step 0 — establish what you are judging

1. Recompute the digest manifest of the FROZEN subject and compare it against the digest recorded in
   the round's frozen manifest. If they differ, STOP and report `SUBJECT_MUTATED` with both digests.
2. State the subject path and the digest you computed.

**Recorded values for this round** (`var/LANE-RELIABILITY-CLOSURE-20261016/FROZEN_MANIFEST.json`,
`file_count` **200**; digest = sha256 over `path:sha256\n` lines of every file except `__pycache__`,
`*.pyc` and `TEST_RESULTS`):

| file | sha256 |
|---|---|
| `scripts/runtime_role_binding_assert.py` | `6fa7ed6b6ea983e1…` (full value in `FROZEN_MANIFEST.json`) |
| `scripts/hgk-governed-runtime-controller.py` | `5b744de7c4e30240…` |
| `tests/test_governed_runtime_controller.py` | `fdf1dbc251eee5e7…` |
| `tests/test_lane_effort_enforcement.py` | `18742bf07b4055ae…` |

aggregate `sha256` = `c2527970de76aa61879c92b925fe18afde2843328846ea97125cfdf2851b43f7`.

Recompute it yourself; do not copy the value above as if you had. If the copy you were given differs
from the frozen subject, that IS the finding — report `SUBJECT_MUTATED` and stop.

## Step 1 — the writer's claims, re-derived

The writer (`attempt BC3`, arm `opencode-go/deepseek-v4.1-flash`) claims two product changes. Re-derive
each from the code, not from its receipt:

**Claim B (the M03 effort axis, `scripts/runtime_role_binding_assert.py`).**
Build your OWN throwaway mandate/pool fixtures (in your writable work dir, never in the subject) for
the lane `VERIFY_SECURITY` with arm `openai-codex/gpt-6.1-sol`, and drive the real script as a
subprocess. Assert the raw exit code AND the typed code in stdout for each of:

| # | mandate effort | the arm's pool effort | `--served-effort` | expected |
|---|---|---|---|---|
| 1 | `medium` | `medium` | — | exit **0**, `ok: true`, `effort_verified: true` (POSITIVE CONTROL) |
| 2 | `medium` | *(absent)* | — | exit **7**, `ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL` |
| 3 | `medium` | `high` | — | exit **7**, `ERR_MANDATE_EFFORT_MISMATCH` |
| 4 | *(absent)* | *(absent)* | `medium` | exit **7**, `ERR_SERVED_EFFORT_UNVERIFIABLE` |
| 5 | `medium` | `medium` | `high` | exit **7**, `ERR_SERVED_EFFORT_MISMATCH` |
| 6 | *(absent)* | *(absent)* | — | exit **0**, `ok: true`, `effort_verified: false` (pass-through) |

Invoke it as (one command per case is fine; a small driver script in your work dir is better):
`python -B <subject>/scripts/runtime_role_binding_assert.py --mandate-file <m.json> --lane VERIFY_SECURITY
--pool <p.json> --toolchain-declaration <subject>/config/hermes-codex-lane.json`
(If `--served-effort` is rejected as an unknown option, that alone falsifies the claim: report it.)

Also run **one** falsification probe the writer did not: give the *positive* fixture an effort the
mandate names but the pool does NOT (`mandate medium`, `pool` absent) **and** add `--served-effort
medium` — report whatever exit code and code come back, so the two refusals' precedence is on record.

**Claim C (the absent-session-id answer, `scripts/hgk-governed-runtime-controller.py`).**
Seed a throwaway Shared Spine with one FROZEN requirement + ADMITTED TaskSpec + CREATED WorkOrder whose
role binding is an `EXECUTE` maker for session `sess-maker`, and a `hermes_home` whose
`governed_runtime.protected_roots` names your scratch protected dir. Drive the controller as a JSON-
stdin subprocess with `HGK_SPINE_DB` and `HGK_SPINE_SCHEMA` set. Assert:

| # | function | session_id | expected |
|---|---|---|---|
| 1 | `write_file` inside the protected root | `""` | exit **0**, `action: allow`, `reason: no-session-id-unattributable` |
| 2 | same | `null` | exit **0**, same reason |
| 3 | `terminal` free text | `""` | exit **0**, same reason |
| 4 | `write_file` inside the protected root | `sess-maker` | **denied** with the work order id in the reason (POSITIVE CONTROL) |
| 5 | `read_file` inside the protected root | a session that is NOT bound | exit **0**, `allow` (ordinary session) |

Cases 4 and 5 are what keep case 1-3 from being a blanket allow. If the fixture is hard to stand up
with the files in the subject, say so and report `UNCERTAIN` for that sub-claim rather than guessing —
`UNCERTAIN` is an acceptable answer and a fabricated one is not.

## Step 2 — the round's own gate result, on its own evidence

Run the named suite from the subject root and report the raw tail:

```
python -B -m unittest tests.test_lane_effort_enforcement tests.test_governed_runtime_controller tests.test_role_binding_enforcement tests.test_mandatory_tool_guard tests.test_matrix_d_full
```

Then run, from the subject root, the registry integrity sweep:

```
python -c "import sys;sys.path.insert(0,'src');from hg_kseos import lane_policy as lp;rp='config/lane-routing-registry.yaml';reg=lp.load_registry(rp);f=lp.check_drift(rp,root='.',registry=reg);print([x for x in f if x['severity']=='error']);print('epoch',reg.get('epoch'));print('PLAN',lp.route_for_lane(reg,'PLAN')['provider'],lp.route_for_lane(reg,'PLAN')['model'])"
```

Report the fatal list, the epoch, and the PLAN route it prints. **Judge nothing about the PLAN route
here** — the round records a known open finding (`F1`) that the PLAN route row disagrees with the
owner chain; what you must check is whether the round's own claims are TRUE, and F1's existence is
already declared.

## Step 3 — your verdict

Your final message is ONE compact JSON object, single line, then the transport token line:

```json
{"schema":"HGK-CHECKER-VERDICT/1","lane":"VERIFY_SECURITY","arm":"openai-codex/gpt-6.1-sol",
 "subject_path":"<abs path>","subject_digest_recomputed_ok":true,
 "claim_B":{"verdict":"AGREE|DISAGREE|UNCERTAIN","cases":{"1":{"exit":0,"code":null},"2":{"exit":7,"code":"ERR_..."},"3":{},"4":{},"5":{},"6":{}},"precedence_probe":{"exit":null,"code":null},"notes":"..."},
 "claim_C":{"verdict":"AGREE|DISAGREE|UNCERTAIN","cases":{"1":{},"2":{},"3":{},"4":{},"5":{}},"notes":"..."},
 "named_suite":{"exit":0,"ran":"Ran N tests in ...","failures":[]},
 "registry_sweep":{"fatal":[],"epoch":20,"plan_route":{"provider":"...","model":"..."}},
 "disagreements":[],"uncertainties":[],"falsification_findings":[],
 "accepted":false,
 "claim_ceiling":"ADVISORY: this is an independent re-derivation over a frozen subject. It is not an OracleReceipt, not an acceptance, and it authorises no promotion or merge."}
```

`accepted` MUST be `false`. Reporting `4/5 re-derived, 1 UNCERTAIN` is a correct and useful verdict;
rounding it up to a clean pass is not.
