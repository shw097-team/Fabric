# Current-state audit: KANBAN / SWARM / GSTACK / OPENSPEC

## Scope, evidence and bottom line

Read-only audit on **2026-10-16 (UTC+08:00)**; the only requested write is this report. SQLite connections used `mode=ro`; SQL compatibility was exercised only in `:memory:`. No board/card/change was created, no dispatcher was run, and no canonical acceptance was performed by this audit. OpenSpec telemetry was disabled for the read-only CLI probes.

Path aliases below are exact, absolute prefixes (expand them when following any locator):

- **R** = `C:/Projects/Agent_Workspace/HG-KSEOS`
- **H** = `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes`
- **K** = `H/hermes-agent/hermes_cli`
- **O** = `C:/Users/user/AppData/Roaming/npm/node_modules/@fission-ai/openspec`
- **G** = `H/skills/software-development/hgk-kanban-and-lane-routing/references/gstack-named-method-readback.md`
- **E** = `R/var/LANE-RELIABILITY-CLOSURE-20261016`

| Mechanism | What a new large governed round must actually create/retain | What that does NOT prove |
|---|---|---|
| KANBAN | A real named board (`board.json` + board-specific `kanban.db`), real task/gate DAG, assignments and subsequent run/comment/result evidence | Normative WorkOrder authority or execution merely because cards exist |
| SWARM | Root + parallel worker cards + verifier + synthesizer; DB edges and root blackboard; round-local `KANBAN_SWARM_GRAPH.json` binding the actual returned IDs; evidence of genuinely parallel, independent lanes | A graph alone is not parallel execution or independent verification |
| GSTACK | Fresh named-method registry, flow-route and activation-invariant readback; declared-role reconciliation and lane/SoD/drift results, conventionally `GSTACK_READBACK.json` | A standalone GSTACK scheduler, actual role execution, or substantive lifecycle acceptance |
| OPENSPEC | Fresh brownfield route evidence and, for a change round, a named OpenSpec change with proposal/tasks/capability deltas (or explicitly valid no-spec metadata), conditional design, plus strict CLI validation output | Planning completeness, implementation, independent acceptance, release authority, or model selection |

Authority: `R/AGENTS.md:14-33` mandates these surfaces for **large governed execution tasks, not Q&A**; `R/AGENTS.md:92-110` makes WorkOrder normative and Kanban coordination-only; `R/AGENTS.md:128-147` reserves acceptance. The read-only restriction on THIS audit takes precedence over performing the setup being described. None of the creation recipes below was executed against a persistent target.

## 1. KANBAN: actual store, schema, and creation mechanics

### 1.1 Resolved paths and board record

Both of these databases exist and were opened read-only:

- Default/legacy-layout board: `H/kanban.db`.
- Concrete example board: `H/kanban/boards/lane-reliability-closure-20261016/kanban.db`.

The path contract is code, not inference: `K/kanban_db.py:399-413` shares the root board home across profiles, with `HERMES_KANBAN_HOME` override; `K/kanban_db.py:507-510` resolves `HERMES_KANBAN_DB` override and the default-versus-named-board paths. Merely setting a profile's `HERMES_HOME` is NOT sufficient to infer its board root. Explicit board selection avoids whichever board is currently selected.

`K/kanban_db.py:536-538,546-574` defines `board.json` as display metadata, with the directory slug as identity and a derived `db_path`. `K/kanban_db.py:577-624` writes metadata, including first `created_at`, and initializes the DB. There is no SQL `boards` table in either inspected store; boards are directories plus metadata and databases (live `sqlite_master` readback). The repo's older `R/config/hermes.json:66-68` instead cites `C:/Users/user/AppData/Local/hermes/kanban.db`; do not substitute that historical declaration for the inspected packaged-home store.

### 1.2 Live tasks/edges schema

Read using `PRAGMA table_info(tasks)`, `PRAGMA table_info(task_links)`/`sqlite_master` from the above stores. Both have the same inspected task schema. `tasks.id` is the primary key; nullable unless marked NOT NULL below. DDL source is `K/kanban_db.py:868-976`; the additional `completion_contract` migration is `K/kanban_db_connect.py:833`.

| Column | SQLite type | Constraint/default |
|---|---|---|
| id | TEXT | PRIMARY KEY |
| title | TEXT | NOT NULL |
| body | TEXT | nullable |
| assignee | TEXT | nullable |
| status | TEXT | NOT NULL |
| priority | INTEGER | DEFAULT 0 |
| created_by | TEXT | nullable |
| created_at | INTEGER | NOT NULL |
| started_at | INTEGER | nullable |
| completed_at | INTEGER | nullable |
| workspace_kind | TEXT | NOT NULL DEFAULT 'scratch' |
| workspace_path | TEXT | nullable |
| branch_name | TEXT | nullable |
| project_id | TEXT | nullable |
| claim_lock | TEXT | nullable |
| claim_expires | INTEGER | nullable |
| tenant | TEXT | nullable |
| result | TEXT | nullable |
| idempotency_key | TEXT | nullable |
| consecutive_failures | INTEGER | NOT NULL DEFAULT 0 |
| worker_pid | INTEGER | nullable |
| worker_started_at | INTEGER | nullable |
| last_failure_error | TEXT | nullable |
| max_runtime_seconds | INTEGER | nullable |
| last_heartbeat_at | INTEGER | nullable |
| current_run_id | INTEGER | nullable |
| workflow_template_id | TEXT | nullable |
| current_step_key | TEXT | nullable |
| skills | TEXT | nullable; JSON serialized by create_task |
| model_override | TEXT | nullable |
| provider_override | TEXT | nullable |
| reasoning_effort | TEXT | nullable |
| max_retries | INTEGER | nullable |
| goal_mode | INTEGER | NOT NULL DEFAULT 0 |
| goal_max_turns | INTEGER | nullable |
| session_id | TEXT | nullable |
| block_kind | TEXT | nullable |
| block_recurrences | INTEGER | NOT NULL DEFAULT 0 |
| completion_contract | TEXT | nullable; migrated column |

```sql
CREATE TABLE task_links (
    parent_id TEXT NOT NULL,
    child_id  TEXT NOT NULL,
    PRIMARY KEY (parent_id, child_id)
);
```

Edges mean **parent prerequisite -> dependent child**. The DDL has no foreign-key clauses; API checks/status gating are not replaceable with arbitrary SQL (`K/kanban_db.py:972-976,1343-1417`; dependency refusal readback at `K/kanban.py:933-940`). Other live tables are `task_comments`, `task_events`, `task_runs`, `task_attachments`, `kanban_notify_subs`, and SQLite's `sqlite_sequence` (live `sqlite_master`). Comments carry full text separately from events (`K/kanban_db.py:978-993`); runs carry attempt, heartbeat, summary and metadata (`K/kanban_db.py:995-1026`).

### 1.3 Agent-facing creation invocation

Use the installed Hermes venv, not the standalone Python used for SQLite inspection. Set the board home explicitly, retain the rest of the environment, and run from `H/hermes-agent`:

```bash
export HERMES_HOME='C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes'
export HERMES_KANBAN_HOME="$HERMES_HOME"
export PYTHONPATH="$HERMES_HOME/hermes-agent"
export PYTHONDONTWRITEBYTECODE=1
PY="$HERMES_HOME/hermes-agent/venv/Scripts/python.exe"
"$PY" -B -m hermes_cli.main kanban boards create ROUND-SLUG \
  --name 'ROUND DISPLAY NAME' --description 'Admitted round purpose' \
  --default-workdir 'C:/Projects/Agent_Workspace/HG-KSEOS'
"$PY" -B -m hermes_cli.main kanban --board ROUND-SLUG swarm 'ADMITTED GOAL' \
  --worker 'REGISTERED-WORKER-1:Worker one scope' \
  --worker 'REGISTERED-WORKER-2:Worker two scope' \
  --worker 'REGISTERED-WORKER-3:Worker three scope' \
  --verifier 'REGISTERED-VERIFIER' --synthesizer 'REGISTERED-SYNTHESIZER' \
  --created-by 'ORCHESTRATOR-PROFILE' --idempotency-key 'ROUND-UNIQUE-KEY' --json
```

These uppercase values are placeholders to replace with the admitted round/profile identities, not current assignments. `boards create` is unscoped; `--board` precedes `swarm`; goal is positional, workers accept `PROFILE:TITLE[:SKILLS]`, verifier/synthesizer take bare profile names. Source: `K/kanban_boards.py:74-90`; `K/kanban_parser.py:222-233,467-477`; `K/kanban.py:394-414`; `K/kanban_swarm.py:294-300`. The actual venv at `H/hermes-agent/venv/Scripts/python.exe` was checked present; `H/hermes-agent/.venv/Scripts/python.exe` was absent.

**Creation is not dispatch authorization.** Discover/verify profiles first (`R/AGENTS.md:112-117`). Native swarm immediately promotes worker cards to ready; its parser has no `--initial-status` option (`K/kanban_parser.py:222-233`; `K/kanban_swarm.py:123-161`). If the admitted round requires an AUTOMATIC_ROUTING_HOLD, do not blindly launch this builder into an active dispatcher: use an explicitly admitted held-card construction instead. The CLI creation recipe does not authorize product writes, model calls, or acceptance.

### 1.4 Exact INSERT and six-card binding

**This is the actual kernel INSERT to understand/use through the CLI/API, NOT permission to directly mutate a canonical board.** `R/AGENTS.md:8,92-100` requires typed governance; a raw `INSERT` omits events, readiness, blackboard, runs, hooks and API validation. The exact parameterized statement is `K/kanban_db.py:1353-1373`:

```sql
INSERT INTO tasks (
    id, title, body, assignee, status, priority,
    created_by, created_at, workspace_kind, workspace_path,
    branch_name, project_id, tenant, idempotency_key,
    max_runtime_seconds,
    skills, max_retries, model_override, provider_override,
    reasoning_effort,
    goal_mode, goal_max_turns, session_id, completion_contract
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
```

For a plain three-worker CLI swarm, the six executions have this exact binding shape. Let `g` be the nonempty stripped goal, `a` the creator, `v`/`s` the verifier/synthesizer profiles, `P` the integer priority, `k` the optional root idempotency key, and `now_i` each create call's epoch seconds. IDs `r,w1,w2,w3,v1,s1` below mean newly returned real task IDs, not literal strings to reuse. Bodies are exactly constructed in `K/kanban_swarm.py:61-67,188-254`.

The 24 parameters in statement order are:

```python
(id_i, title_i, body_i, assignee_i, status_i, P,
 a, now_i, 'scratch', None,
 None, None, tenant_i, key_i,
 None,
 skills_json_i, None, None, None,
 None,
 0, None, None, None)
```

This assumes an unprojected board, no tenant and workers without the optional skills suffix; thus `tenant_i=None`. A project-scoped board or explicit worker skills changes these values through the API (`K/kanban_db.py:1290-1335`; `K/kanban_swarm.py:184-187,213-223`). CLI swarm does not expose per-card model/provider/reasoning pins (`K/kanban.py:402-407`).

| Execution | id_i | title_i | assignee_i | status_i at INSERT | key_i | skills_json_i | parents |
|---|---|---|---|---|---|---|---|
| root | r | `Swarm: ` + `g.splitlines()[0][:80]` | a | blocked | k | NULL | none |
| worker 1 | w1 | worker 1 parsed title | worker 1 profile | todo | NULL | NULL | r |
| worker 2 | w2 | worker 2 parsed title | worker 2 profile | todo | NULL | NULL | r |
| worker 3 | w3 | worker 3 parsed title | worker 3 profile | todo | NULL | NULL | r |
| verifier | v1 | Verify swarm outputs | v | todo | NULL | `["requesting-code-review"]` | w1,w2,w3 |
| synthesizer | s1 | Synthesize swarm outputs | s | todo | NULL | `["humanizer"]` | v1 |

For CLI workers, `body_i` is their parsed title plus `_swarm_context(r,g)`; root/verifier/synthesizer bodies are the literal templates in the above source. The kernel's initial status calculation and validation precede INSERT (`K/kanban_db.py:1279-1289,1343-1344`). After graph construction the builder changes root blocked -> done with a completed run/summary/event, then recomputes readiness, so workers become ready and verifier/synthesizer remain todo. Root's done means **topology planned**, not goal achieved (`K/kanban_swarm.py:70-103,123-161`).

Exact edge INSERT (`K/kanban_db.py:1438-1442`), executed for seven parameter pairs:

```sql
INSERT OR IGNORE INTO task_links (parent_id, child_id) VALUES (?, ?);
```

```python
[(r,w1), (r,w2), (r,w3), (w1,v1), (w2,v1), (w3,v1), (v1,s1)]
```

Verification performed: extracted this INSERT from the current `create_task` AST, created `tasks`/`task_links` in `:memory:` from the live DB's DDL, inserted six fixture rows and seven edges. Result: `tasks=6`, `edges=7`, `all_edges_resolve=true`, `production_writes=0`. This verifies SQL/schema compatibility only, not runtime workflow or acceptance.

## 2. SWARM: execution graph artifact and DB binding

### 2.1 What is implemented versus conventional

Swarm is implemented as a thin topology/blackboard layer over Kanban, explicitly **no second scheduler** (`K/kanban_swarm.py:1-13`). Its returned data is exactly `root_id`, `worker_ids`, `verifier_id`, `synthesizer_id` (`K/kanban_swarm.py:41-51`). It also records a root comment with prefix `[swarm:blackboard] ` and JSON `{key:"topology", value:{root_id,worker_ids,verifier_id,synthesizer_id,goal}}` (`K/kanban_swarm.py:256-267`). This DB record is code-generated and recoverable on idempotent reuse (`K/kanban_swarm.py:201-209,270-291`).

The separate round artifact **`KANBAN_SWARM_GRAPH.json` with `schema: "HGK-KANBAN-SWARM-GRAPH/1"` is an evidence convention, not a formal JSON Schema enforced by the builder**. The builder does not write that file (`K/kanban.py:408-414` only prints the IDs). Evidence precedent is `E/KANBAN_SWARM_GRAPH.json:1-29`, fully inspected. A bounded text scan of `R/src`, `R/scripts`, `R/tools`, `R/tests`, `R/schemas`, `R/HGK`, `R/config` found no consumer/validator for that schema token; this is a bounded absence claim, not proof about every historical artifact or external component.

### 2.2 Exact observed schema/fields to reproduce

To follow the example faithfully, create a round-local JSON object with these keys/types. **“Required” here means required by this report's faithful example-based recipe, not validated by a located schema file.**

```text
schema: string = HGK-KANBAN-SWARM-GRAPH/1
round: string
at: string (example uses YYYY-MM-DD)
surface: string
board:
  slug: string
  name: string
  db: string (absolute resolved board DB path)
  default_workdir: string
  created_by: string (builder command identity)
swarm:
  builder: string
  goal: string
  root: string (actual SwarmCreated.root_id)
  workers: array[string] (actual SwarmCreated.worker_ids)
  verifier: string (actual SwarmCreated.verifier_id)
  synthesizer: string (actual SwarmCreated.synthesizer_id)
  assignee_profile: string (example-specific common-profile shorthand)
what_kanban_swarm_openspec_are_not: array[string]
dispatch_note: string
claim_ceiling: string
```

Source for every field: `E/KANBAN_SWARM_GRAPH.json:2-28`. With different role profiles, retain real per-card assignments in DB readback rather than falsely claiming a common `assignee_profile`. The example has no explicit `edges` array: binding depends on `board.db` + IDs and the live `task_links`/root blackboard. An additional edge readback is useful evidence, but is not an existing required field of this example.

The example IDs were rejoined against its named board DB, not trusted from prose:

| Role | DB task ID | Status at readback |
|---|---|---|
| root | t_d73fd9d5 | done |
| worker 1 | t_c81ed79f | ready |
| worker 2 | t_86dd7812 | ready |
| worker 3 | t_a64fc611 | ready |
| verifier | t_92f55a9e | todo |
| synthesizer | t_dbdc8541 | todo |

Observed at approximately **2026-10-16 12:16 +08:00**, through read-only SQL on `H/kanban/boards/lane-reliability-closure-20261016/kanban.db`; artifact locators are `E/KANBAN_SWARM_GRAPH.json:7-20`. All six IDs existed, all seven expected edges existed, and the root's topology comment agreed. Status is mutable; this is not a claim about later completion. New rounds must replace these IDs, never copy them.

A genuine governed SWARM round additionally needs raw lane execution/handoff and independent-checker evidence (`R/AGENTS.md:21-33,130-143`). The verifier card text asks for metadata `{"gate":"pass"}` and the synthesizer text says wait for verifier (`K/kanban_swarm.py:226-253`); those are **worker instructions**, not evidence that an independent checker ran. Kernel/CLI dependency and nonempty-completion checks exist (`K/kanban.py:900-940`; `K/kanban_db.py:2678-2686`), but card status cannot establish checker independence or canonical acceptance.

## 3. GSTACK: named-method readback, not a new control plane

### 3.1 Required names and sources

The readback recipe explicitly requires calls to:

```python
lane_policy.load_registry()
lane_policy.route_for_lane(reg, lane)
lane_policy.check_sod(maker, checker)
lane_policy.check_drift(registry=reg)
named_methods.registry_snapshot()
named_methods.route(flow)
named_methods.evaluate_activation_invariants()
```

Source: `G:6-29`. `route_for_lane` returns the matching top-level route, not a selected arm or served-model receipt (`R/src/hg_kseos/lane_policy.py:157-161`). The code uses the registry for declared lane policy; the recipe's “all-zero” activation check must not be promoted into substantive acceptance (`G:31,43-54`).

The seven currently selected GSTACK **method IDs** are:

| Method ID | Canonical flow keyword that selects it | Important literal-role caveat |
|---|---|---|
| gstack.office-hours | ambiguity | `route("office-hours")` is NATIVE |
| gstack.plan-eng-review | plan | Other plan role strings share this branch |
| gstack.review | review | `devex-review` shares this branch |
| gstack.qa | qa | `qa-only` shares this branch |
| gstack.cso | security | `route("cso")` is NATIVE |
| gstack.ship | release | `route("ship")` is NATIVE |
| gstack.retro | retro | Literal role matches |

Source/selection logic: `R/src/hg_kseos/named_methods.py:56-147,151-192`. Seven selected GSTACK methods are distinct from the eighth active method, `openspec` (`:39-55,146-147`). `registry_snapshot()` fields are `source_disposition`, `current_execution_scope`, `runtime_required_now`, `role`, `provider_state`, `fallback`, `final_authority`, `xor_with` (`:266-275`). `route()` returns `flow`, `provider`, `state`, `fallback`, `final_authority`, `route` (`:159-192`).

Declared role source: `R/HGK/HGK_GSTACK_ROLE_MAP.yaml:1-150` (JSON syntax despite `.yaml` extension); upstream snapshot: `R/HGK/HGK_GSTACK_UPSTREAM_CAPABILITY_SNAPSHOT.tsv:1-20`. Architecture adoption is not control-plane adoption; hard denials include GSTACK scheduler/spec/release/deploy authority (`role map:3-12`). Do not characterize the implemented `named_methods.py` registry/router as absent. Conversely, it is not evidence of a separate installed GSTACK execution service.

### 3.2 Fresh current readback and gaps

The actual `named_methods` module was loaded read-only with bytecode disabled. All seven canonical flow probes selected the expected GSTACK method. Paired negative probes using `selected_slices=set()` returned NATIVE with no provider, no fallback and no state. This is the current router behavior, **not** an executed certified native fallback (`R/src/hg_kseos/named_methods.py:157-192`).

Programmatic comparison against the role map produced:

- Declared roles: **19**; role-keyed selected methods: **7/19**.
- `DECLARED_NOT_SELECTED`: **12** — autoplan, benchmark, canary, codex, design-consultation, devex-review, document-*, investigate, plan-ceo-review, plan-design-review, plan-devex-review, qa-only. This class means no exact role-keyed selected method; some use a shared method and some remain native. It does NOT mean all twelve route NATIVE.
- `MAP_ROLE_ABSENT`: **9** literal role inputs route NATIVE — office-hours, design-consultation, investigate, cso, benchmark, document-*, ship, canary, codex. Some have a differently named canonical keyword mapping, as shown above.
- `SELECTED_NOT_IN_MAP`: **0**, explicit empty list `[]`.

The classes overlap; do not add their counts. These are fresh evaluations of `registry_snapshot()`/`ACTIVE_SELECTED` and `route(role)` against `R/HGK/HGK_GSTACK_ROLE_MAP.yaml:13-146`, following `G:33-41` with literal-role versus canonical-flow distinctions preserved.

All **14** activation-invariant counters were zero. This is narrowly explained by the code: `evaluate_activation_invariants()` checks lifecycle **file existence** and OpenSpec/Spec Kit XOR (`R/src/hg_kseos/named_methods.py:196-259`); it does not authenticate those files' contents, independently recertify providers, or execute the methods. Lifecycle paths are under `R/evidence/review`, from `:21,214-228`.

Fresh lane-policy readback at **2026-10-16T12:17:32.345959+08:00**: registry epoch **20**, status **CANDIDATE**; `check_drift(registry=reg)` returned `[]`. Top-level PLAN-vs-VERIFY and EXECUTE-vs-VERIFY comparisons both returned `SOD_OK`. These are declaration comparisons only (`R/src/hg_kseos/lane_policy.py:115-125,157-161,225-245,283-340`; inputs `R/config/lane-routing-registry.yaml`). They are not this audit's served-model attestation. The earlier example records epoch 19 (`E/GSTACK_READBACK.json:9-10`), so copying it would be stale.

### 3.3 What the new round must write

Conventionally write **`ROUND/GSTACK_READBACK.json`**, example schema label **`HGK-GSTACK-READBACK/1`** (`E/GSTACK_READBACK.json:1-84`). The prose recipe `G:1-54` specifies the readbacks and gap classes, but does **not** prescribe that filename or a machine-enforced JSON Schema. A bounded code scan of the seven R roots named in section 2 found no validator for this readback schema label.

Retain at least: round/as-of/source paths; fresh full registry snapshot and active-selected method list; lane registry epoch/status and actual top-level route results; per-declared-role and relevant canonical-flow route objects; activation counter object; all three gap classes with explicit lists/counts (including zero); selected/declared denominator; drift findings; maker/checker SoD result and any owner-declared deviation; paired positive/negative probe outputs and exit codes; honest claim ceiling. Fields beyond the old example are audit-recommended completeness fields derived from `G:15-54`, not falsely advertised as an existing enforced schema.

**Prior-artifact defect:** `E/GSTACK_READBACK.json:11` has `role_map_roles: []` despite the nineteen roles actually present; `:79-81` holds descriptive gap strings rather than measured lists/counts and omits `DECLARED_NOT_SELECTED`. The claimed explicit-empty-set task checkbox at `R/openspec/changes/hgk-lane-reliability-closure-20261016/tasks.md:34-35` is not equivalent to those missing structured results. Use it as a filename/shape precedent, not a complete verified readback. No historical artifact was repaired by this audit.

Additional claim caveat: registry entries have `final_authority=False`, but most route objects retain the default `final_authority=True`; only the release branch explicitly sets false (`R/src/hg_kseos/named_methods.py:34,159-161,185-188`). Preserve/report the actual objects; do not infer a grant of authority from that inconsistent output. Governance still reserves authority to HGK (`R/AGENTS.md:6-12,128-147`).

## 4. OPENSPEC: current CLI, files and strict validation

### 4.1 Installed executable and exact invocation

Installed CLI version is **1.8.0**, confirmed by `openspec --version`, matching `O/package.json:2-3`. Shell discovery resolved `C:/Users/user/AppData/Roaming/npm/openspec`; the Windows shim calls `O/bin/openspec.js` (`C:/Users/user/AppData/Roaming/npm/openspec.cmd:10-17`; package bin mapping `O/package.json:29-31`). No repo-local `node_modules/@fission-ai/openspec/package.json` or root `package.json` was present in the inspected HGK repo.

From cwd **`R`**, the exact installed CLI forms are:

```bash
OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 openspec new change ROUND-CHANGE --schema spec-driven
OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 openspec status --change ROUND-CHANGE --json
OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 openspec instructions proposal --change ROUND-CHANGE --json
# Repeat instructions for specs, design (if applicable), tasks; write their resolved paths.
OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 openspec validate ROUND-CHANGE --type change --strict
```

New-change syntax is implemented at `O/dist/cli/index.js:584-606`; creation resolves root/store before writing (`O/dist/commands/workflow/new-change.js:36-70`). Both `new change --help` and `validate --help` were executed. A prior local skill recommends `npx openspec validate ROUND-CHANGE --type change --strict` (`H/skills/software-development/hgk-kanban-and-lane-routing/SKILL.md`, automated self-check section), but the **direct installed `openspec` form above is what was actually exercised**; no `npx` install/download was performed. Telemetry opt-out behavior is code at `O/dist/telemetry/index.js:60-86`.

### 4.2 Config and on-disk layout

Project config is exactly **`R/openspec/config.yaml`**; its active content is `schema: spec-driven` (`:1`); the rest is commented guidance (`:3-32`). Current status resolved nearest root as `R`, `planningHome.kind=repo`, `changeRoot=R/openspec/changes/hgk-lane-reliability-closure-20261016` (actual `openspec status ... --json` output).

For a new change the layout is:

```text
R/openspec/
  config.yaml
  specs/                          # main capability specs, not the change's delta directory
  changes/
    ROUND-CHANGE/
      .openspec.yaml               # schema + created date, CLI scaffold
      proposal.md                 # why / what / capabilities / impact
      tasks.md                    # numbered - [ ] implementation checklist
      design.md                   # conditional design artifact
      specs/
        CAPABILITY-PATH/
          spec.md                 # change delta, not a second canonical source
    archive/
```

**Scaffolding alone does not generate all Markdown artifacts.** Code creates directories and `.openspec.yaml`, and only an optional description README (`O/dist/utils/change-utils.js:89-143`; `O/dist/commands/workflow/new-change.js:63-81`). The installed workflow defines proposal, specs, design and tasks output paths/dependencies (`O/schemas/spec-driven/schema.yaml:4-39,62-84,131-143,166-207`).

- A normal behavior-changing round writes `proposal.md`, `tasks.md`, and one `specs/<capability-path>/spec.md` for each new/modified capability. Delta headings use ADDED/MODIFIED/REMOVED/RENAMED Requirements; each requirement needs at least one `#### Scenario:` and normative SHALL/MUST text (`O/schemas/spec-driven/schema.yaml:62-84`). New capability Purpose guidance is `:86-94`.
- Pure documentation/tooling/refactor changes with no behavior delta may explicitly use `skip_specs: true` in valid `.openspec.yaml`; do NOT invent fake requirements or also carry spec files (`O/schemas/spec-driven/schema.yaml:24-30,68-71`; marker validation implementation at `O/dist/utils/change-metadata.js:149-162` and `O/dist/core/validation/validator.js:330-380`).
- `design.md` is conditional in workflow instructions for cross-cutting, dependency/data-model, security/performance/migration or ambiguity cases; it is not an unconditional prose demand for every tiny change (`O/schemas/spec-driven/schema.yaml:131-143`). Tasks depend on specs and design in the graph (`:201-207`), so inspect `status`/`instructions`; a tasks file's existence alone does not prove upstream artifacts are complete.

### 4.3 Actual strict validation versus completion

Executed against the existing example (not against an invented new change):

```text
$ openspec validate hgk-lane-reliability-closure-20261016 --type change --strict
Change 'hgk-lane-reliability-closure-20261016' is valid
exit: 0
```

Immediately following `openspec status --change hgk-lane-reliability-closure-20261016 --json` returned `proposal=done`, `specs=done`, `tasks=done`, **`design=ready`, `isPlanningComplete=false`, `isComplete=false`**. The files present were proposal, tasks and `specs/lane-governance-gates/spec.md`; no design or `.openspec.yaml` was present in this particular existing example. This legacy/example state does not change what the new-change scaffolder creates. Source files: `R/openspec/changes/hgk-lane-reliability-closure-20261016/{proposal.md,tasks.md,specs/lane-governance-gates/spec.md}`; runtime outputs were captured by this audit's terminal call.

Strict validation rejects warnings as well as errors (`O/dist/core/validation/validator.js:605-619`); **strict-valid does not equal planning-complete or implementation-accepted**. Preserve the real validator stdout/stderr and exit code for the new change, then retain status/instructions decisions separately.

The HGK OpenSpec named-method side also needs its own readback: `registry_snapshot()["openspec"]` and `route("brownfield")` (or migration flow) returned `OPENSPEC`, provider `openspec`, state `CERTIFIED_ACTIVE_BROWNFIELD`; deselecting all slices returned NATIVE/DEGRADED, while `greenfield` returned NATIVE/XOR_GREENFIELD. Registration and branch code: `R/src/hg_kseos/named_methods.py:39-55,151-169`. Do not silently replace this evidence with “we created a proposal.” Lifecycle existence checks use `R/evidence/review/HG-KSEOS_OPENSPEC_*` files (`:214-220,232-259`), not substantive current-round execution. Exact per-round route-readback filename is conventional, not enforced by that function.

### 4.4 Current change-directory inventory

Live filesystem listing of **`R/openspec/changes`**, as of **2026-10-16T12:18:50.182194+08:00**: **21 non-archive change directories**, **1 archived change directory**. The earlier read saw 20 non-archive directories; `hgk-far-remediation-20261016` appeared during the audit, showing concurrent work. This audit did not create it. Inventory is explicitly time-bounded, not a frozen global state.

1. `gcm-noninteractive-default-containment`
2. `hermes-incident-2026-10-05-repair`
3. `hgk-checker-upgrade-adapter`
4. `hgk-far-remediation-20261016`
5. `hgk-lane-brief-and-guard-hardening-20261015`
6. `hgk-lane-reliability-closure-20261016`
7. `hgk-plan-plane-rebind-20261015`
8. `hgk-r8-eia-closure-skill-slim-20261016`
9. `hgk-skill-convergence-20261014`
10. `lane-health-repair-20261011`
11. `lane-mandate-rebinding-and-d01-revocation`
12. `lane-model-chain-rebind-20261015`
13. `lane-sod-enforcement`
14. `lane-supervisor-windowless-convergence`
15. `lane-toolchain-identity-and-failure-classification`
16. `lane-verify-dual-routing-and-plan-high`
17. `lane-verify-routing-remediation`
18. `skill-mainfile-cap-remediation`
19. `sod-independent-verify-enforcement`
20. `strict-declaration-20261011`
21. `verification-artifact-contract`

## 5. Enforcement ceiling and handoff checklist

1. **Admission first:** the four coordination/method/spec surfaces do not replace Source -> frozen Requirement -> TaskSpec -> WorkOrder or Fabric policy consumption (`R/AGENTS.md:92-126`). They also do not independently choose or attest a serving model (`E/KANBAN_SWARM_GRAPH.json:22-28`).
2. **KANBAN:** create board metadata + DB, create actual cards/edges via the kernel, retain immutable ID binding and time-stamped mutable-state readbacks. A raw SQL skeleton without events/runs/blackboard is not the complete mechanism (`K/kanban_db.py:1353-1417`; `K/kanban_swarm.py:70-161,256-267`).
3. **SWARM:** retain the six-card/seven-edge graph for this requested topology and root blackboard; write the convention-based graph artifact; separately retain real parallel lane receipts/handoffs and independent verifier evidence (`R/AGENTS.md:21-33`; `K/kanban_swarm.py:188-267`). No graph artifact schema validator was located in the bounded source scan.
4. **GSTACK:** write fresh route/registry/invariant/gap evidence, including all nineteen roles rather than an empty role list, canonical-keyword caveats, current lane-policy checks and paired controls (`G:6-54`). The JSON artifact convention is documented/example-based; the actual registry/router and existence/XOR checks are code-backed but not proof of execution or acceptance (`R/src/hg_kseos/named_methods.py:146-259`).
5. **OPENSPEC:** create the named change through the installed CLI, author its resolved planning outputs, preserve strict validation and planning status, and separately record the brownfield route decision (`O/dist/utils/change-utils.js:89-143`; `O/schemas/spec-driven/schema.yaml:4-207`; `R/src/hg_kseos/named_methods.py:162-169`).
6. **No self-acceptance:** this is an evidence/mechanism audit, not independent product verification or acceptance (`R/AGENTS.md:12,130-147`). The default-on policy is prose authority; this audit did not establish a single mandatory code consumer that atomically enforces creation of all four artifacts on every round.

### Issues/limits encountered

- The documented sibling `C:/Projects/Agent_Workspace/Fabric/AGENTS.md` was not found at that exact path. No Fabric file was altered or inferred from a missing file; HGK's local projection is cited where applicable (`R/AGENTS.md:6,59-76,119-126`).
- Generic file search did not discover ignored `var` artifacts reliably; named paths were read directly and a bounded Python walk was used. No reusable `probe_gstack_rolemap.py` was found in that walk (candidate/subject/venv/vendor trees excluded); direct current-module positive/negative evaluations were run instead. This is not a claim that no historical copy exists anywhere.
- Two initial regular-expression search calls were rejected by the search tool; simpler searches/source reads succeeded. No failed lookup was treated as evidence of absence.
- Live board and OpenSpec inventory are mutable; readback times and the concurrent change-directory addition are disclosed rather than flattened into a frozen-state claim.

**Files created/modified by this audit:** only `R/var/FAR-REMEDIATION-AND-CLOSURE-20261016/evidence/EVIDENCE_MECHANISMS_AUDIT.md`. No governance store, profile, skill, repo source, prior evidence or OpenSpec change was intentionally written by this audit. No repair, dispatch, publication or acceptance was attempted.
