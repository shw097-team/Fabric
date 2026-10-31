# W3 — measured capability probes

Captured: 2026-10-22T10:19:31.004728+08:00

Scope: read-only repository audit. No repository edit, commit, board mutation, provider dispatch, fetch, install, or acceptance write was performed. Exactly one requested deliverable is written by this audit. Tool-runtime caches/spillover are not deliverables. Existing Codex probe receipts are historical observations, not new model turns.

HG-KSEOS HEAD: `3dfaebc5c1d2ffe7d1782f3027bd25b54a557f2b`; SBL HEAD: `2dde2d84a2a6d95ccc6acb9356570bed68ab2f05`.

## State table

| Surface | State | Measured boundary |
|---|---|---|
| KANBAN | PARTIAL | Board list/stats work; ls exits 1 under subagent guard; historical open backlog remains. |
| SWARM | PASS | Help works and linked root→workers→verifier→synthesizer DAGs exist; no new dispatch tested. |
| GSTACK | PARTIAL | Seven selected named slices; role-name routing has native gaps; lane CLI has no flow-route/selected_route/reason_code interface. |
| OPENSPEC | FAIL | HGK validate --all exits 1 (37 pass, 2 fail); SBL passes 1/1. |
| CODEX CLI | PASS | Both supplied receipts bind required=served, nonce, exit 0, usage receipt true; receipt scope only. |
| SUB-AGENTS | PARTIAL | Real archived worker outputs exist, but historical round persists 3/4; broad census has inaccessible paths. |
| SELF-DETECT / REPAIR / ACCEPT / EVOLVE | FAIL | Detection exists; repair is a planner; self-accept explicitly refused; evolution ledger is not a self-applying gate. |

PASS never implies product acceptance. PARTIAL denotes a measured working subset, not a downgrade of a known failed acceptance criterion. OpenSpec failures and autonomous self-accept failure remain FAIL.

## Invocation conventions

All subprocesses inherited the environment with `PYTHONDONTWRITEBYTECODE=1` and `HERMES_HOME=C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes`. Commands below are actual argv rendered by subprocess.list2cmdline. The broken hermes.exe trampoline was bypassed with the supplied venv entry point. No dispatch --dry-run was used (it is not read-only).

## 1. KANBAN — PARTIAL

### Probe `boards`
Working directory: `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent`
Exit code: `0`

```text
C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe -B -c "import sys; sys.argv=[\"hermes\"]+sys.argv[1:]; from hermes_cli.main import main; main()" kanban boards list
```

Verbatim output excerpt:
```text
    round-sbl-hgk-rca-20261022  ROUND-SBL-HGK-RCA-20261022 (SBL x HG-KSEOS degradation RCA)  done=1, ready=7
    sbl-pipdls-20261020       SBL SpecBuild Loop PIPD-LS v0.1  archived=1, blocked=4, done=28, ready=1, running=1
    sbl-r11-20261021          SBL R11 full-contract continuation  done=1, ready=1, todo=5
    sbl-r12-far               SBL R12 FAR                   done=1, ready=5, todo=2
    sbl-r13-native            SBL R13 native chain          done=1, ready=4, todo=2
    sbl-r14-full-product      SBL R14 full product          done=8, ready=23
```

### Probe `stats`
Working directory: `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent`
Exit code: `0`

```text
C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe -B -c "import sys; sys.argv=[\"hermes\"]+sys.argv[1:]; from hermes_cli.main import main; main()" kanban --board sbl-r14-full-product stats
```

Verbatim output excerpt:
```text
By status:
  triage    0
  todo      0
  scheduled  0
  ready     23
  running   0
  blocked   0
  done      8

By assignee:
  default               done=6
  hermes-r14            done=1

Oldest ready task age: 2088s
```

### Probe `ls`
Working directory: `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent`
Exit code: `1`

```text
C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe -B -c "import sys; sys.argv=[\"hermes\"]+sys.argv[1:]; from hermes_cli.main import main; main()" kanban --board sbl-r14-full-product ls
```

Verbatim output excerpt:
```text
kanban: delegate_task child contexts cannot mutate Kanban tasks or boards
```

Board-scoped SQLite readback used `sqlite3.connect(path.as_uri()+"?mode=ro", uri=True)`, `SELECT * FROM tasks`, and Python Counter over status. In-process extraction completed with exit code 0. Counts include all rows, including archived rows; omitted statuses below are zero. This avoids the `ls` guard without bypassing it or modifying anything.

| Board | Done | Ready | Todo | Other |
|---|---:|---:|---:|---|
| round-sbl-hgk-rca-20261022 | 1 | 7 | 0 | none |
| sbl-pipdls-20261020 | 28 | 1 | 0 | archived=1, blocked=4, running=1 |
| sbl-r11-20261021 | 1 | 1 | 5 | none |
| sbl-r12-far | 1 | 5 | 2 | none |
| sbl-r13-native | 1 | 4 | 2 | none |
| sbl-r14-full-product | 8 | 23 | 0 | none |

R12 and R13 each have only their auto-completed swarm root done; all workers remain ready and verifier/synthesizer remain todo. R14 has a completed seven-card swarm plus other work, yet 23 cards remain ready. This is a measured unresolved backlog, not proof that boards never drain over all time: a single snapshot cannot establish a temporal “never.” The root body explicitly states it is completed immediately so workers can start; root done is not work completion. `ls` is NOT_EXERCISED beyond the actual guard refusal; no attempt was made to unset the subagent guard.

## 2. SWARM — PASS (graph presence only)

### Probe `swarm_help`
Working directory: `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent`
Exit code: `0`

```text
C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/hermes-agent/venv/Scripts/python.exe -B -c "import sys; sys.argv=[\"hermes\"]+sys.argv[1:]; from hermes_cli.main import main; main()" kanban swarm --help
```

Verbatim output excerpt:
```text
usage: hermes kanban swarm [-h] [--worker PROFILE:TITLE[:SKILL,SKILL]]
                           --verifier VERIFIER --synthesizer SYNTHESIZER
                           [--tenant TENANT] [--priority PRIORITY]
                           [--created-by CREATED_BY]
                           [--idempotency-key IDEMPOTENCY_KEY] [--json]
                           goal

positional arguments:
  goal                  Swarm goal / final outcome

options:
  -h, --help            show this help message and exit
  --worker PROFILE:TITLE[:SKILL,SKILL]
                        Parallel worker card (repeatable)
  --verifier VERIFIER   Verifier profile
  --synthesizer SYNTHESIZER
                        Synthesizer/writer profile
  --tenant TENANT       Tenant namespace
  --priority PRIORITY   Priority tiebreaker
  --created-by CREATED_BY
                        Creator/anchor profile
  --idempotency-key IDEMPOTENCY_KEY
                        Dedup key for the root card
  --json                Emit JSON output
```

Read-only census: 96 board databases; 62 graph-shaped swarm roots satisfy root→worker, every worker→verifier, verifier→synthesizer. Exact SQL: `SELECT * FROM tasks`; `SELECT * FROM task_links`; schemas read using `SELECT name,sql FROM sqlite_master WHERE type='table'`. Extraction exit 0. Parent columns are not on tasks: edges live in `task_links(parent_id, child_id)`.

SBL graph excerpts (verbatim row identifiers/statuses serialized from DB):
```json
[
  {
    "board": "sbl-pipdls-20261020",
    "root": "t_bf8acd6d",
    "workers": [
      "t_543f8bf3",
      "t_88de4454",
      "t_30f8c302",
      "t_73364f50"
    ],
    "verifier": "t_38296605",
    "synthesizer": "t_b598a788",
    "status": {
      "t_bf8acd6d": "done",
      "t_543f8bf3": "done",
      "t_88de4454": "done",
      "t_30f8c302": "done",
      "t_73364f50": "done",
      "t_38296605": "done",
      "t_b598a788": "done"
    }
  },
  {
    "board": "sbl-r12-far",
    "root": "t_c1b4d403",
    "workers": [
      "t_dd0f5282",
      "t_0d384783",
      "t_aea902e3",
      "t_47017ac5",
      "t_c7c44c52"
    ],
    "verifier": "t_00d2062c",
    "synthesizer": "t_5f76be91",
    "status": {
      "t_c1b4d403": "done",
      "t_dd0f5282": "ready",
      "t_0d384783": "ready",
      "t_aea902e3": "ready",
      "t_47017ac5": "ready",
      "t_c7c44c52": "ready",
      "t_00d2062c": "todo",
      "t_5f76be91": "todo"
    }
  },
  {
    "board": "sbl-r13-native",
    "root": "t_13b3d15c",
    "workers": [
      "t_6409816f",
      "t_0a223bab",
      "t_60dc110f",
      "t_150ada09"
    ],
    "verifier": "t_6f1e7a98",
    "synthesizer": "t_ff48fd57",
    "status": {
      "t_13b3d15c": "done",
      "t_6409816f": "ready",
      "t_0a223bab": "ready",
      "t_60dc110f": "ready",
      "t_150ada09": "ready",
      "t_6f1e7a98": "todo",
      "t_ff48fd57": "todo"
    }
  },
  {
    "board": "sbl-r14-full-product",
    "root": "t_7a41e27f",
    "workers": [
      "t_730d602a",
      "t_63a5568a",
      "t_6b3ebf66",
      "t_0c6b581f"
    ],
    "verifier": "t_39825119",
    "synthesizer": "t_d23ffddf",
    "status": {
      "t_7a41e27f": "done",
      "t_730d602a": "done",
      "t_63a5568a": "done",
      "t_6b3ebf66": "done",
      "t_0c6b581f": "done",
      "t_39825119": "done",
      "t_d23ffddf": "done"
    }
  }
]
```

R14 witness: root `t_7a41e27f`, verifier `t_39825119`, synthesizer `t_d23ffddf`; all done, with four done workers. The current RCA board has no matching complete graph shape in this snapshot. New graph creation and actual concurrent scheduling are NOT_EXERCISED: they mutate board/runtime state. A done DAG is not evidence of distinct models or independent principals.

## 3. GSTACK — PARTIAL

Sources read: `C:/Projects/Agent_Workspace/HG-KSEOS/HGK/HGK_GSTACK_ROLE_MAP.yaml` and `C:/Projects/Agent_Workspace/HG-KSEOS/src/hg_kseos/named_methods.py`. Role-map declares `ADOPT_FULL_GSTACK_ROLE_ARCHITECTURE=true`, `ADOPT_FULL_GSTACK_CONTROL_PLANE=false`; ship is SUPPORT_ONLY. Registry has 7 selected gstack methods / 19 mapped role keys; 12 map keys lack their own method; selected-not-in-map=0. Missing role-keyed methods can adopt shared ones and are not automatically missing capabilities.

### Probe `named_search`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `1`

```text
rg -n named_methods C:/Projects/Agent_Workspace/HG-KSEOS/config C:/Projects/Agent_Workspace/HG-KSEOS/registries C:/Projects/Agent_Workspace/HG-KSEOS/HGK
```

Verbatim output excerpt:
```text

```

### Probe `route_help`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-route.py --help
```

Verbatim output excerpt:
```text
usage: hgk-lane-route.py [-h] [--lane LANE] [--pool POOL]
                         [--override OVERRIDE] [--mode {candidates,selfcheck}]

options:
  -h, --help            show this help message and exit
  --lane LANE
  --pool POOL
  --override OVERRIDE
  --mode {candidates,selfcheck}
```

### Probe `route_selfcheck`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-route.py --mode selfcheck
```

Verbatim output excerpt:
```text
{"lanes": {"EXECUTE": 4, "PLAN": 7, "VERIFY_SECURITY": 5}, "mode": "selfcheck", "ok": true, "pool": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\lane-route-slots.candidate.json", "pool_sha256": "0033b616bdf21433b048463b2ee38513773ba4ab2395cc4d1a34a1e4f6526e3e", "schema": "HGK-LANE-ROUTE-CANDIDATES/1"}
```

### Probe `route_execute`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-route.py --lane EXECUTE
```

Verbatim output excerpt:
```text
{"candidates": [{"engine": "codex-cli", "model": "minimax-m3.1-flash-free", "provider": "opencode-go", "rank": 1, "role": "DEFAULT/首選", "token": "opencode-go/minimax-m3.1-flash-free", "transport": "opencodex relay 10101 via the isolated lane home (codex -> 10100 front-door port -> 10101); the openai-codex entry additionally has a human-home transport"}, {"engine": "codex-cli", "model": "deepseek-v4.1-flash", "provider": "opencode-go", "rank": 2, "role": "FALLBACK1/備援1", "token": "opencode-go/deepseek-v4.1-flash", "transport": "opencodex relay 10101 via the isolated lane home (codex -> 10100 front-door port -> 10101); the openai-codex entry additionally has a human-home transport"}, {"engine": "codex-cli", "model": "gpt-6-luna", "provider": "openai-codex", "rank": 3, "role": "FALLBACK2/備援2", "token": "openai-codex/gpt-6-luna", "transport": "opencodex relay 10101 via the isolated lane home (codex -> 10100 front-door port -> 10101); the openai-codex entry additionally has a human-home transport"}, {"engine": "codex-cli", "model": "deepseek-ai/deepseek-v4.1-flash", "provider": "nvidia", "rank": 4, "role": "FALLBACK3/備援3", "token": "nvidia/deepseek-ai/deepseek-v4.1-flash", "transport": "opencodex relay 10101 via the isolated lane home (codex -> 10100 front-door port -> 10101); the openai-codex entry additionally has a human-home transport"}], "lane": "EXECUTE", "mode": "pool", "ok": true, "pool": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\lane-route-slots.candidate.json", "pool_sha256": "0033b616bdf21433b048463b2ee38513773ba4ab2395cc4d1a34a1e4f6526e3e", "schema": "HGK-LANE-ROUTE-CANDIDATES/1"}
```

### Probe `route_verify`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-route.py --lane VERIFY_SECURITY
```

Verbatim output excerpt:
```text
{"candidates": [{"engine": "codex-cli", "model": "gpt-6.1-sol", "provider": "openai-codex", "rank": 1, "role": "DEFAULT/首選", "token": "openai-codex/gpt-6.1-sol", "transport": "same as EXECUTE"}, {"engine": "codex-cli", "model": "minimax-m3.1-flash-free", "provider": "opencode-go", "rank": 2, "role": "FALLBACK1/備援1", "token": "opencode-go/minimax-m3.1-flash-free", "transport": "same as EXECUTE"}, {"engine": "codex-cli", "model": "glm-5.3-flash", "provider": "opencode-go", "rank": 3, "role": "FALLBACK2/備援2", "token": "opencode-go/glm-5.3-flash", "transport": "same as EXECUTE"}, {"engine": "codex-cli", "model": "deepseek-v4.1-flash", "provider": "opencode-go", "rank": 4, "role": "FALLBACK3/備援3", "token": "opencode-go/deepseek-v4.1-flash", "transport": "same as EXECUTE"}, {"engine": "codex-cli", "model": "deepseek-ai/deepseek-v4.1-flash", "provider": "nvidia", "rank": 5, "role": "FALLBACK4/備援4", "token": "nvidia/deepseek-ai/deepseek-v4.1-flash", "transport": "same as EXECUTE"}], "lane": "VERIFY_SECURITY", "mode": "pool", "ok": true, "pool": "C:\\Projects\\Agent_Workspace\\HG-KSEOS\\config\\lane-route-slots.candidate.json", "pool_sha256": "0033b616bdf21433b048463b2ee38513773ba4ab2395cc4d1a34a1e4f6526e3e", "schema": "HGK-LANE-ROUTE-CANDIDATES/1"}
```

### Probe `named_live`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B -c "import sys,json;sys.path.insert(0,'src');from hg_kseos import named_methods as n; m=json.load(open('HGK/HGK_GSTACK_ROLE_MAP.yaml')); print(json.dumps({'active_selected':sorted(n.ACTIVE_SELECTED),'routes':{r:n.route(r) for r in m['roles']},'semantic_routes':{f:n.route(f) for f in ['ambiguity','security','release','brownfield','retro']},'invariants':n.evaluate_activation_invariants()},sort_keys=True))"
```

Verbatim output excerpt:
```text
{"active_selected": ["gstack.cso", "gstack.office-hours", "gstack.plan-eng-review", "gstack.qa", "gstack.retro", "gstack.review", "gstack.ship", "openspec"], "invariants": {"active_named_method_missing_binding": 0, "active_named_method_missing_doctor": 0, "active_named_method_missing_identity": 0, "active_named_method_missing_independent_cert": 0, "active_named_method_missing_install": 0, "active_named_method_missing_pilot": 0, "active_named_method_missing_pin": 0, "active_named_method_silent_fallback": 0, "canonical_flow_named_method_without_runtime_or_certified_substitute": 0, "dual_spec_owner": 0, "named_method_fake_invocation": 0, "named_method_silent_fallback": 0, "release_authority_escape": 0, "second_orchestrator": 0}, "routes": {"autoplan": {"fallback": "hgk_native_plan_review", "final_authority": true, "flow": "autoplan", "provider": "gstack.plan-eng-review", "route": "GSTACK", "state": "CERTIFIED"}, "benchmark": {"fallback": null, "final_authority": true, "flow": "benchmark", "provider": null, "route": "NATIVE", "state": null}, "canary": {"fallback": null, "final_authority": true, "flow": "canary", "provider": null, "route": "NATIVE", "state": null}, "codex": {"fallback": null, "final_authority": true, "flow": "codex", "provider": null, "route": "NATIVE", "state": null}, "cso": {"fallback": null, "final_authority": true, "flow": "cso", "provider": null, "route": "NATIVE", "state": null}, "design-consultation": {"fallback": null, "final_authority": true, "flow": "design-consultation", "provider": null, "route": "NATIVE", "state": null}, "devex-review": {"fallback": "hgk_native_review", "final_authority": true, "flow": "devex-review", "provider": "gstack.review", "route": "GSTACK", "state": "CERTIFIED"}, "document-*": {"fallback": null, "final_authority": true, "flow": "document-*", "provider": null, "route": "NATIVE", "state": null}, "investigate": {"fallback": null, "final_authority": true, "flow": "investigate", "provider": null, "route": "NATIVE", "state": null}, "office-hours": {"fallback": null, "final_authority": true, "flow": "office-hours", "provider": null, "route": "NATIVE", "state": null}, "plan-ceo-review": {"fallback": "hgk_native_plan_review", "final_authority": true, "flow": "plan-ceo-review", "provider": "gstack.plan-eng-review", "route": "GSTACK", "state": "CERTIFIED"}, "plan-design-review": {"fallback": "hgk_native_plan_review", "final_authority": true, "flow": "plan-design-review", "provider": "gstack.plan-eng-review", "route": "GSTACK", "state": "CERTIFIED"}, "plan-devex-review": {"fallback": "hgk_native_plan_review", "final_authority": true, "flow": "plan-devex-review", "provider": "gstack.plan-eng-review", "route": "GSTACK", "state": "CERTIFIED"}, "plan-eng-review": {"fallback": "hgk_native_plan_review", "final_authority": true, "flow": "plan-eng-review", "provider": "gstack.plan-eng-review", "route": "GSTACK", "state": "CERTIFIED"}, "qa": {"fallback": "hgk_native_qa", "final_authority": true, "flow": "qa", "provider": "gstack.qa", "route": "GSTACK", "state": "CERTIFIED"}, "qa-only": {"fallback": "hgk_native_qa", "final_authority": true, "flow": "qa-only", "provider": "gstack.qa", "route": "GSTACK", "state": "CERTIFIED"}, "retro": {"fallback": "hgk_native_retro", "final_authority": true, "flow": "retro", "provider": "gstack.retro", "route": "GSTACK", "state": "CERTIFIED"}, "review": {"fallback": "hgk_native_review", "final_authority": true, "flow": "review", "provider": "gstack.review", "route": "GSTACK", "state": "CERTIFIED"}, "ship": {"fallback": null, "final_authority": true, "flow": "ship", "provider": null, "route": "NATIVE", "state": null}}, "semantic_routes": {"ambiguity": {"fallback": "hgk_native_prw", "final_authority": true, "flow": "ambiguity", "provider": "gstack.office-hours", "route": "GSTACK", "state": "CERTIFIED"}, "brownfield": {"fallback": "hgk_native_prw", "final_authority": true, "flow": "brownfield", "provider": "openspec", "route": "OPENSPEC", "state": "CERTIFIED_ACTIVE_BROWNFIELD"}, "release": {"fallback": "hgk_native_release_checklist", "final_authority": false, "flow": "release", "provider": "gstack.ship", "route": "GSTACK", "state": "CERTIFIED"}, "retro": {"fallback": "hgk_native_retro", "final_authority": true, "flow": "retro", "provider": "gstack.retro", "route": "GSTACK", "state": "CERTIFIED"}, "security": {"fallback": "hgk_native_security", "final_authority": true, "flow": "security", "provider": "gstack.cso", "route": "GSTACK", "state": "CERTIFIED"}}}
```

The requested `selected_route` and `reason_code` fields are NOT_EMITTED, not inferred: neither the lane CLI nor named_methods.route returns them. The lane CLI supports only `--mode candidates|selfcheck`, `--lane`, `--pool`, `--override`; no flow argument. Therefore a flow-route invocation of that script is NOT_EXERCISED because unsupported; the real supported flow API `named_methods.route(flow)` was run instead, with its actual `route`/`provider`/`state` above. No synthetic selected_route or reason_code is supplied.

Literal role keys route 9/19 to NATIVE, including office-hours, cso, ship, investigate. Semantic flows ambiguity/security/release correctly choose office-hours/cso/ship. Thus literal-map-name routing is not interchangeable with semantic-flow routing. Seven selected methods and all-zero activation counters prove registration/presence only, not actual gstack subprocess execution. Named method execution beyond routing is NOT_EXERCISED (would dispatch work).

## 4. OPENSPEC — FAIL

### Probe `openspec_hgk_list`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec list
```

Verbatim output excerpt:
```text
Changes:
  far-minimax-mandate-20261021                           25/30 tasks   18h ago
  far-lane-remediation-20261021                          ✓ Complete    21h ago
  hgk-cnv-owner-decision-main-landing                    ✓ Complete    5d ago
  pipd-unmerged-candidate-merge-20261016                 7/8 tasks     5d ago
  hgk-cnv-hygiene-readme-closure                         ✓ Complete    5d ago
  pipd-repo-hygiene-and-handover-20261016                0/21 tasks    5d ago
  s4-final-pr18-closeout-20261016                        22/23 tasks   5d ago
  hgk-cnv-far018-far019-archive                          10/15 tasks   5d ago
  hgk-far-019-owner-authorized-closure                   7/21 tasks    5d ago
  hgk-far-018-r7r11-residual-closure                     3/12 tasks    5d ago
  pipd-r17-install-doc-identity-guard                    0/21 tasks    5d ago
  pipd-s4r6-closeout-doc-identity-and-update-route       0/23 tasks    5d ago
  hgk-cnv-evidence-archive-r7r11-20261016                11/21 tasks   5d ago
  hgk-r11-session-handover-20261016                      26/27 tasks   5d ago
  hgk-round3-lane-rebind-20261016                        26/27 tasks   5d ago
  hgk-r10-session-closure-20261016                       25/30 tasks   5d ago
  hgk-r9-far-residual-closure-20261016                   20/25 tasks   5d ago
  hgk-far-remediation-20261016                           0/25 tasks    5d ago
  hgk-lane-reliability-closure-20261016                  5/21 tasks    5d ago
  hgk-r8-eia-closure-skill-slim-20261016                 0/22 tasks    5d ago
  hgk-lane-brief-and-guard-hardening-20261015            0/22 tasks    6d ago
  hgk-plan-plane-rebind-20261015                         3/8 tasks     6d ago
  lane-model-chain-rebind-20261015                       0/13 tasks    6d ago
  hgk-skill-convergence-20261014                         3/16 tasks    7d ago
  gcm-noninteractive-default-containment                 36/44 tasks   8d ago
  lane-mandate-rebinding-and-d01-revocation              11/38 tasks   8d ago
  lane-toolchain-identity-and-failure-classification     18/27 tasks   8d ago
  verification-artifact-contract                         7/33 tasks    9d ago
  strict-declaration-20261011                            5/22 tasks    10d ago
  lane-health-repair-20261011                            30/34 tasks   10d ago
  sod-independent-verify-enforcement                     3/5 tasks     12d ago
  hgk-checker-upgrade-adapter                            0/23 tasks    12d ago
  lane-supervisor-windowless-convergence                 12/13 tasks   13d ago
  lane-verify-dual-routing-and-plan-high                 5/28 tasks    14d ago
  lane-sod-enforcement                                   0/27 tasks    14d ago
  lane-verify-routing-remediation                        0/14 tasks    14d ago
  skill-mainfile-cap-remediation                         0/11 tasks    14d ago
  hermes-incident-2026-10-05-repair                      0/35 tasks    15d ago
```

### Probe `openspec_hgk_validate_--help`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec validate --help
```

Verbatim output excerpt:
```text
Usage: openspec validate [options] [item-name]

Validate changes and specs

Options:
  --all              Validate all changes and specs
  --changes          Validate all changes
  --specs            Validate all specs
  --type <type>      Specify item type when ambiguous: change|spec
  --strict           Enable strict validation mode
  --json             Output validation results as JSON
  --concurrency <n>  Max concurrent validations (defaults to env
                     OPENSPEC_CONCURRENCY or 6)
  --no-interactive   Disable interactive prompts
  --store <id>       Store id to use as the OpenSpec root (a store is a
                     standalone OpenSpec repo you've registered)
  -h, --help         display help for command
```

### Probe `openspec_hgk_validate_--all`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `1`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec validate --all
```

Verbatim output excerpt:
```text
- Validating...
✓ spec/ao-lane-independent-verify
✓ change/far-lane-remediation-20261021
✓ change/far-minimax-mandate-20261021
✓ change/gcm-noninteractive-default-containment
✓ change/hermes-incident-2026-10-05-repair
✓ change/hgk-checker-upgrade-adapter
✓ change/hgk-cnv-evidence-archive-r7r11-20261016
✓ change/hgk-cnv-far018-far019-archive
✓ change/hgk-cnv-hygiene-readme-closure
✓ change/hgk-cnv-owner-decision-main-landing
✓ change/hgk-far-018-r7r11-residual-closure
✓ change/hgk-far-019-owner-authorized-closure
✓ change/hgk-far-remediation-20261016
✓ change/hgk-lane-brief-and-guard-hardening-20261015
✓ change/hgk-lane-reliability-closure-20261016
✗ change/hgk-plan-plane-rebind-20261015
✓ change/hgk-r10-session-closure-20261016
✓ change/hgk-r11-session-handover-20261016
✓ change/hgk-r8-eia-closure-skill-slim-20261016
✓ change/hgk-r9-far-residual-closure-20261016
✓ change/hgk-round3-lane-rebind-20261016
✓ change/hgk-skill-convergence-20261014
✓ change/lane-health-repair-20261011
✓ change/lane-mandate-rebinding-and-d01-revocation
✓ change/lane-model-chain-rebind-20261015
✓ change/lane-sod-enforcement
✓ change/lane-supervisor-windowless-convergence
✓ change/lane-toolchain-identity-and-failure-classification
✓ change/lane-verify-dual-routing-and-plan-high
✓ change/lane-verify-routing-remediation
✓ change/pipd-r17-install-doc-identity-guard
✓ change/pipd-repo-hygiene-and-handover-20261016
✓ change/pipd-s4r6-closeout-doc-identity-and-update-route
✓ change/pipd-unmerged-candidate-merge-20261016
✓ change/s4-final-pr18-closeout-20261016
✓ change/skill-mainfile-cap-remediation
✗ change/sod-independent-verify-enforcement
✓ change/strict-declaration-20261011
✓ change/verification-artifact-contract
Totals: 37 passed, 2 failed (39 items)
Details: openspec validate hgk-plan-plane-rebind-20261015 --type change
```

### Probe `openspec_sbl_list`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `0`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec list
```

Verbatim output excerpt:
```text
Changes:
  sbl-v01-candidate-build     26/28 tasks   13h ago
```

### Probe `openspec_sbl_validate_--all`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `0`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec validate --all
```

Verbatim output excerpt:
```text
- Validating...
✓ change/sbl-v01-candidate-build
Totals: 1 passed, 0 failed (1 items)
```

### Probe `openspec_bad1`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `1`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec validate hgk-plan-plane-rebind-20261015 --type change
```

Verbatim output excerpt:
```text
Change 'hgk-plan-plane-rebind-20261015' has issues
✗ [ERROR] file: Change must have at least one delta. No deltas found. Ensure your change has a specs/ directory with capability folders (e.g. specs/http-server/spec.md) containing .md files that use delta headers (## ADDED/MODIFIED/REMOVED/RENAMED Requirements) and that each requirement includes at least one "#### Scenario:" block. If this change intentionally modifies no specs (pure refactor, tooling, docs), set "skip_specs: true" in the change's .openspec.yaml instead. Tip: run "openspec change show <change-id> --json --deltas-only" to inspect parsed deltas.
Next steps:
  - Ensure change has deltas in specs/: use headers ## ADDED/MODIFIED/REMOVED/RENAMED Requirements
  - Each requirement MUST include at least one #### Scenario: block
  - Debug parsed deltas: openspec show hgk-plan-plane-rebind-20261015 --json --deltas-only
```

### Probe `openspec_bad2`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `1`

```text
"C:/Program Files/Git/bin/bash.exe" C:/Users/user/AppData/Roaming/npm/openspec validate sod-independent-verify-enforcement --type change
```

Verbatim output excerpt:
```text
Change 'sod-independent-verify-enforcement' has issues
✗ [ERROR] file: Change must have at least one delta. No deltas found. Ensure your change has a specs/ directory with capability folders (e.g. specs/http-server/spec.md) containing .md files that use delta headers (## ADDED/MODIFIED/REMOVED/RENAMED Requirements) and that each requirement includes at least one "#### Scenario:" block. If this change intentionally modifies no specs (pure refactor, tooling, docs), set "skip_specs: true" in the change's .openspec.yaml instead. Tip: run "openspec change show <change-id> --json --deltas-only" to inspect parsed deltas.
Next steps:
  - Ensure change has deltas in specs/: use headers ## ADDED/MODIFIED/REMOVED/RENAMED Requirements
  - Each requirement MUST include at least one #### Scenario: block
  - Debug parsed deltas: openspec show sod-independent-verify-enforcement --json --deltas-only
```

HGK has a hard validation FAIL: both named failing changes contain no spec delta. SBL validates but its change still reports 26/28 tasks. Working CLI availability cannot turn the HGK failure into PARTIAL.

## 5. CODEX CLI — PASS within supplied receipt scope

Read commands: Python `Path(path).read_text(encoding="utf-8")` and `json.loads` for the two exact requested probe paths. In-process read exit 0. The two original receipt attempts both report child exit=0 and a matching usage row; no new Codex invocation was made because the assignment explicitly requests existing receipt readback.

### `C:/Projects/Agent_Workspace/HG-KSEOS/var/ROUND-SBL-HGK-RCA-20261022/probe/exec_receipt.json`
```json
{
  "required_arm": "opencode-go/minimax-m3.1-flash-free",
  "served_arm": "opencode-go/minimax-m3.1-flash-free",
  "used_rank": 1,
  "ok": true,
  "usage_receipt_ok": true,
  "generated_utc": "2026-10-22T02:10:53.109027+00:00"
}
```
Verbatim receipt attempt fields:
```json
{
  "exit": 0,
  "nonce_present": true,
  "usage_status": 200,
  "usage_receipt_ok": true,
  "credential_posture": {
    "verdict": "INCONCLUSIVE",
    "decision": "WARN_CONTINUE",
    "reason": "helper-only verdict (no child env asserted): helper_resolution_reset=PASS; helper_non_interactive=UNKNOWN",
    "prompt_capable_helper": null,
    "origin": null,
    "git_terminal_prompt": "0"
  },
  "stderr_tail": "Reading additional input from stdin...\n2026-10-22T02:10:49.498911Z ERROR codex_api::endpoint::responses_websocket: failed to connect to websocket: HTTP error: 426 Upgrade Required, url: ws://127.0.0.1:10101/v1/responses\n"
}
```

### `C:/Projects/Agent_Workspace/HG-KSEOS/var/ROUND-SBL-HGK-RCA-20261022/probe/verify_receipt.json`
```json
{
  "required_arm": "opencode-go/deepseek-v4.1-flash",
  "served_arm": "opencode-go/deepseek-v4.1-flash",
  "used_rank": 4,
  "ok": true,
  "usage_receipt_ok": true,
  "generated_utc": "2026-10-22T02:11:01.415549+00:00"
}
```
Verbatim receipt attempt fields:
```json
{
  "exit": 0,
  "nonce_present": true,
  "usage_status": 200,
  "usage_receipt_ok": true,
  "credential_posture": {
    "verdict": "INCONCLUSIVE",
    "decision": "WARN_CONTINUE",
    "reason": "helper-only verdict (no child env asserted): helper_resolution_reset=PASS; helper_non_interactive=UNKNOWN",
    "prompt_capable_helper": null,
    "origin": null,
    "git_terminal_prompt": "0"
  },
  "stderr_tail": "Reading additional input from stdin...\n2026-10-22T02:10:59.057850Z ERROR codex_api::endpoint::responses_websocket: failed to connect to websocket: HTTP error: 426 Upgrade Required, url: ws://127.0.0.1:10101/v1/responses\n"
}
```

EXECUTE is rank 1 MiniMax; VERIFY_SECURITY is forced rank 4 DeepSeek, not current pool rank 1. It is correct for this receipt’s explicit required_arm, not evidence that default checker selection serves DeepSeek. Both receipts contain websocket 426 diagnostics but actual completed agent messages and usage success; diagnostics alone are not failure. Authorization/completion checks are false, subject_mutation is not_guarded, credential posture is INCONCLUSIVE/WARN_CONTINUE. These are not acceptance receipts and prove neither native execution authority nor subject verification.

## 6. SUB-AGENTS — PARTIAL

### Probe `sub_sbl`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `1`

```text
rg -i -l delegate|subagent|swarm C:/Projects/Agent_Workspace/SBL/evidence
```

Verbatim output excerpt:
```text

```

Parsed unique matching paths: **0**. Error lines: **0**. These are mention-bearing files, not delegation/event counts.

### Probe `sub_hgk`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `2`

```text
rg -i -l delegate|subagent|swarm C:/Projects/Agent_Workspace/HG-KSEOS/var
```

Verbatim output excerpt:
```text
C:/Projects/Agent_Workspace/HG-KSEOS/var\FAR-CLOSURE-20261021-R2\probes\VERIFY_acceptance.json.logs\attempt-23244-1792558909-1-stdout.txt
C:/Projects/Agent_Workspace/HG-KSEOS/var\FAR-CLOSURE-20261021-R2\probes\VERIFY_after_fix.json.logs\attempt-21824-1792558428-1-stdout.txt
rg: C:/Projects/Agent_Workspace/HG-KSEOS/var\checker-scratch\round-20261022-r14\TEST_RESULTS\hgk-m06-e2e-6mg7axpd: 存取被拒。 (os error 5)
rg: C:/Projects/Agent_Workspace/HG-KSEOS/var\checker-scratch\round-20261022-r14\TEST_RESULTS\hgk-m07a-lsgcamw9: 存取被拒。 (os error 5)
```

Parsed unique matching paths: **8046**. Error lines: **965**. These are mention-bearing files, not delegation/event counts.

### Probe `sub_retry`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `2`

```text
rg -i -l delegate|subagent|swarm C:/Projects/Agent_Workspace/HG-KSEOS/var -g !checker-scratch/** -g !checker-runtime/** -g !**/scratch/**
```

Verbatim output excerpt:
```text
C:/Projects/Agent_Workspace/HG-KSEOS/var\FAR-CLOSURE-20261021-R2\probes\VERIFY_acceptance.json.logs\attempt-23244-1792558909-1-stdout.txt
C:/Projects/Agent_Workspace/HG-KSEOS/var\FAR-CLOSURE-20261021-R2\probes\VERIFY_after_fix.json.logs\attempt-21824-1792558428-1-stdout.txt
rg: C:/Projects/Agent_Workspace/HG-KSEOS/var\checker-scratch\round-20261022-r14\TEST_RESULTS\hgk-m06-e2e-6mg7axpd: 存取被拒。 (os error 5)
rg: C:/Projects/Agent_Workspace/HG-KSEOS/var\checker-scratch\round-20261022-r14\TEST_RESULTS\hgk-m07a-lsgcamw9: 存取被拒。 (os error 5)
```

Parsed unique matching paths: **7789**. Error lines: **924**. These are mention-bearing files, not delegation/event counts.

### Probe `sbl_gov_sub`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `0`

```text
rg -i -l delegate|subagent|swarm C:/Projects/Agent_Workspace/SBL/_governance
```

Verbatim output excerpt:
```text
C:/Projects/Agent_Workspace/SBL/_governance\round-20261020-r2\17_DONORS\DISPOSITION_TABLE.json
C:/Projects/Agent_Workspace/SBL/_governance\round-20261020-r2\51_RESUME_CHECKPOINT.json
```

Parsed unique matching paths: **26**. Error lines: **0**. These are mention-bearing files, not delegation/event counts.

The broad HGK scan found 8046 accessible matching files but exited 2 with 965 error lines; this is a lower bound, not a complete census. A second differently scoped scan still exited 2 (7789 accessible matches, 924 errors), so access failures remain disclosed. Copies of source and environments contribute mentions; do not reinterpret 8046 as 8046 delegates. SBL evidence/ has zero matching files (rg exit 1 means no match, not a broken scan); broader _governance has 26.

Strongest single prior-round example:
`C:/Projects/Agent_Workspace/SBL/_governance/round-20261021-r9/FAR-R9-RULING.json`, research section:
```json
{
  "workers": 4,
  "model": "gpt-6.1-sol",
  "provider": "openai-codex",
  "durations_s": [
    443.95,
    367.64,
    306.84,
    581.19
  ],
  "raw_outputs": [
    {
      "file": "subagent-summary-0-20261021_213940_898000.txt",
      "bytes": 56834,
      "sha256": "58f28dcb4c2bb7c32d567bf12ca73554de167fe8ecf9a6a9b611e0378d3a0f8d"
    },
    {
      "file": "subagent-summary-1-20261021_213940_900010.txt",
      "bytes": 25860,
      "sha256": "42a5df3663e07121fa66c41136ef27c3142e6d985729f2e7938fde5d9c4bda7e"
    },
    {
      "file": "subagent-summary-3-20261021_213940_901017.txt",
      "bytes": 28946,
      "sha256": "b195bdf3aad2de612e3b5605630867d7c46d6758b08730c855177244684a1437"
    }
  ],
  "raw_outputs_gap": "3 of 4 worker outputs are persisted here. The 4th (SP integration, task index 2) was delivered inline in the delegation completion message and the harness did not write a summary file for it, so it is not on disk. Its findings are carried in this ruling (section sp_integration) but the raw text is not archived; that is a gap, not a claim of completeness."
}
```

Readback verified the three archived raw summary sizes and SHA256 values against this ruling:
```json
[
  {
    "path": "C:\\Projects\\Agent_Workspace\\SBL\\_governance\\round-20261021-r9\\raw_worker_outputs\\subagent-summary-0-20261021_213940_898000.txt",
    "bytes": 56834,
    "sha256": "58f28dcb4c2bb7c32d567bf12ca73554de167fe8ecf9a6a9b611e0378d3a0f8d",
    "matches": true
  },
  {
    "path": "C:\\Projects\\Agent_Workspace\\SBL\\_governance\\round-20261021-r9\\raw_worker_outputs\\subagent-summary-1-20261021_213940_900010.txt",
    "bytes": 25860,
    "sha256": "42a5df3663e07121fa66c41136ef27c3142e6d985729f2e7938fde5d9c4bda7e",
    "matches": true
  },
  {
    "path": "C:\\Projects\\Agent_Workspace\\SBL\\_governance\\round-20261021-r9\\raw_worker_outputs\\subagent-summary-3-20261021_213940_901017.txt",
    "bytes": 28946,
    "sha256": "b195bdf3aad2de612e3b5605630867d7c46d6758b08730c855177244684a1437",
    "matches": true
  }
]
```

The first raw output independently states `INCONCLUSIVE - NOT ACCEPTED` and that maker self-checks do not supersede it. The fourth output is expressly missing. This is stronger evidence than a textual swarm mention, but does not establish complete persistence of all delegated work. New delegation is NOT_EXERCISED in this read-only audit.

## 7. SELF-DETECT / SELF-REPAIR / SELF-ACCEPT / SELF-EVOLVE — FAIL

### Probe `self_files`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `0`

```text
rg --files C:/Projects/Agent_Workspace/SBL -g *self_check*
```

Verbatim output excerpt:
```text
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r10\90_EVIDENCE\self_check_r10.py
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\90_EVIDENCE\self_check_r7.py
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r9\90_EVIDENCE\self_check_r9.py
```

### Probe `all_self_consumers`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `0`

```text
rg -n self_check_r|self.detect|self.repair|self.accept|self.evol C:/Projects/Agent_Workspace/SBL -g *.py -g *.yml -g *.yaml -g *.toml
```

Verbatim output excerpt:
```text
C:/Projects/Agent_Workspace/SBL\openspec\config.yaml:7:  Claims are candidate-only; no self-acceptance, no self-promotion, no release claim.
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r9\90_EVIDENCE\self_check_r9.py:14:    acceptance verdict recorded here would be a self-acceptance channel.
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r10\90_EVIDENCE\self_check_r10.py:11:      with a maker-authored acceptance is a self-acceptance channel in disguise.
C:/Projects/Agent_Workspace/SBL\sbl_core\core.py:35:        self.repair = BoundedRepair()
C:/Projects/Agent_Workspace/SBL\tools\build_prompt_contract.py:335:                "candidate-only; no self-acceptance, no RELEASED, no PRODUCTION claim",
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\40_VERIFY\lane_rebind_gpt61\preimage_registry-pre-pin-refresh-20261021T104612Z.yaml:182:    OPEN_OWNER_ORDERED. What remains is process, lane and evidence-path separation plus the no-self-acceptance
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\40_VERIFY\lane_rebind_gpt61\preimage_registry-pre-pin-refresh-20261021T104612Z.yaml:413:      claim from the artifacts and is forbidden from reading the writer''s summary), and the no-self-acceptance
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\40_VERIFY\lane_rebind_gpt61\preimage_registry-pre-pin-refresh-20261021T104612Z.yaml:439:      forbidden from reading the writer''s summary), and the no-self-acceptance rule (the dispatcher refuses
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\40_VERIFY\lane_rebind_gpt61\preimage_registry-pre-pin-refresh-20261021T104612Z.yaml:498:    retained: PROCESS, LANE and EVIDENCE-PATH separation plus the no-self-acceptance rule; model diversity
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\40_VERIFY\lane_rebind_gpt61\preimage_registry-pre-pin-refresh-20261021T104612Z.yaml:558:  - pointer: /sod/maker_self_acceptance
C:/Projects/Agent_Workspace/SBL\_governance\round-20261021-r7\20_FAR\far-20261021-023\ResearchHandoff.yaml:135:  - no self-acceptance: the independent re-check must come from the VERIFY_SECURITY lane, not the maker lane
```

### Probe `repair_consumers`
Working directory: `C:/Projects/Agent_Workspace/SBL`
Exit code: `0`

```text
rg -n STOP_ESCALATE|NARROW_REPAIR|\.repair\.plan|self_check_r[0-9] C:/Projects/Agent_Workspace/SBL/sbl_cli C:/Projects/Agent_Workspace/SBL/sbl_core C:/Projects/Agent_Workspace/SBL/sbl_sp C:/Projects/Agent_Workspace/SBL/tools C:/Projects/Agent_Workspace/SBL/.github
```

Verbatim output excerpt:
```text
C:/Projects/Agent_Workspace/SBL/tools\build_prompt_contract.py:411:            "non_terminal_pause": ["PAUSED_REMEDIABLE", "BLOCKED", "STOP_ESCALATE", "TEMP_CLOSED",
C:/Projects/Agent_Workspace/SBL/sbl_core\m06_repair.py:48:            action="STOP_ESCALATE" if exhausted else "NARROW_REPAIR",
```

### Probe `r10_readonly_functions`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B -c "from __future__ import annotations
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
HGK = Path('C:/Projects/Agent_Workspace/HG-KSEOS')
SBL = Path('C:/Projects/Agent_Workspace/SBL')
CAND = Path('C:/Projects/Agent_Workspace/_sbl_r9_candidate')
R10 = SBL / '_governance/round-20261021-r10'
HO = R10 / 'HANDOVER_SBL_R10_20261021.md'
STATE = R10 / 'HANDOVER_STATE_R10.json'
PY = str(HGK / '.venv/Scripts/python.exe')
MANDATE = {'PLAN': 'opencode-go/minimax-m3.1-flash-free', 'EXECUTE': 'opencode-go/deepseek-v4.1-flash', 'VERIFY_SECURITY': 'gpt-6.1-sol'}
results: list[tuple[str, bool, str]] = []

def check(label: str, fn) -> None:
    try:
        ok, detail = fn()
    except Exception as exc:
        ok, detail = (False, f'{type(exc).__name__}: {exc}')
    results.append((label, ok, detail))
    print(f\"[{('PASS' if ok else 'FAIL')}] {label}\n       {detail}\")

def c1_mandate_rank1():
    s = json.loads((HGK / 'var/R10-GATE/final_summary.json').read_text(encoding='utf-8'))
    bad = {}
    for lane, want in MANDATE.items():
        got = s.get(lane, {})
        if not got.get('ok') or got.get('rank') != 1 or got.get('transport') != want:
            bad[lane] = got
    if bad:
        return (False, f'lane mismatch: {bad}')
    return (True, 'all three lanes ok at rank 1: ' + ', '.join((f\"{k}={s[k]['transport']} {s[k]['s']}s\" for k in MANDATE)))

def c2_epoch_joint():
    a = json.loads((HGK / 'config/model-lane-assignment.json').read_text(encoding='utf-8'))
    import yaml
    r = yaml.safe_load((HGK / 'config/lane-routing-registry.yaml').read_text(encoding='utf-8'))
    if int(a['registry_epoch']) != int(r['epoch']):
        return (False, f\"assignment {a['registry_epoch']} != registry {r['epoch']}\")
    return (True, f\"epoch {r['epoch']} agrees on both sides\")

def c3_drift():
    code = \"import sys;sys.path.insert(0,'src');from hg_kseos import lane_policy as lp;f=lp.check_drift();print(len(f),lp.drift_is_fatal(f))\"
    r = subprocess.run([PY, '-c', code], capture_output=True, text=True, timeout=300, cwd=str(HGK))
    if r.returncode != 0:
        return (False, f'drift gate crashed: {r.stderr[-200:]}')
    n, fatal = r.stdout.split()[:2]
    if int(n) != 0 or fatal != 'False':
        return (False, f'findings={n} fatal={fatal}')
    return (True, '0 findings, fatal=False')

def c4_surfaces_agree():
    \"\"\"Compare the three runtime surfaces to EACH OTHER and to the pool.

    This is the check the drift gate does not perform. Under the mandate:
      PLAN plane (governed profile) must name the PLAN model
      EXECUTE lane declaration and the runtime provider_route must name the EXECUTE model
    \"\"\"
    import yaml
    pool = json.loads((HGK / 'config/lane-route-slots.candidate.json').read_text(encoding='utf-8'))
    rank1 = {l['lane']: f\"{l['ordered_pool'][0]['provider']}/{l['ordered_pool'][0]['model']}\" for l in pool['lanes']}
    gov = yaml.safe_load(Path('C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/profiles/hgk-governed/config.yaml').read_text(encoding='utf-8'))['model']
    lane = json.loads((HGK / 'config/hermes-codex-lane.json').read_text(encoding='utf-8'))
    hd = json.loads((HGK / 'config/hermes.json').read_text(encoding='utf-8'))
    gov_pair = f\"{gov['provider']}/{gov['default']}\"
    lane_pair = f\"{lane['provider']}/{lane['model']}\"
    rt_pair = f\"opencode-go/{hd['provider_route']['model']}\"
    problems = []
    if gov_pair != rank1['PLAN']:
        problems.append(f\"governed PLAN plane {gov_pair} != pool PLAN {rank1['PLAN']}\")
    if lane_pair != rank1['EXECUTE']:
        problems.append(f\"EXECUTE lane decl {lane_pair} != pool EXECUTE {rank1['EXECUTE']}\")
    if rt_pair != rank1['EXECUTE']:
        problems.append(f\"provider_route {rt_pair} != pool EXECUTE {rank1['EXECUTE']}\")
    if lane.get('codex_executable') is None or lane.get('codex_sha256') is None:
        problems.append('codex toolchain pin missing from the lane declaration')
    if problems:
        return (False, '; '.join(problems))
    return (True, f'PLAN surface={gov_pair} == pool; EXECUTE lane={lane_pair} and provider_route={rt_pair} == pool; codex pin intact')

def c5_handover_sections():
    t = HO.read_text(encoding='utf-8')
    need = ['30 秒定向', '模型 mandate', '硬約束', '已完成並驗證', '未關閉項目', '下一步', '已證實的陷阱', '關鍵路徑地圖', '宣稱天花板', '前 5 個指令']
    missing = [s for s in need if s not in t]
    if missing:
        return (False, f'handover missing sections: {missing}')
    for rid in ['R9-02', 'R9-04', 'R9-05', 'R9-06', 'SP-INT']:
        if rid not in t:
            return (False, f'handover omits open item {rid}')
    return (True, f'{len(t)} chars, all 10 sections, all 5 open items named')

def c6_state_json():
    s = json.loads(STATE.read_text(encoding='utf-8'))
    if s['claim_ceiling'].split('.')[0] != 'CANDIDATE_ONLY':
        return (False, f\"ceiling: {s['claim_ceiling'][:60]}\")
    if len(s['open']) < 5:
        return (False, f\"only {len(s['open'])} open items recorded\")
    if s['planes']['fabric']['state'] != 'NO_SBL_INSTALL_TARGET':
        return (False, 'fabric state must stay NO_SBL_INSTALL_TARGET; no target was manufactured')
    if s['hgk_r9']['acceptance']['verdict'] not in ('FAIL', 'NOT_RUN'):
        return (False, f\"R9 acceptance is {s['hgk_r9']['acceptance']['verdict']}, must stay unresolved\")
    return (True, f\"{len(s['open'])} open items, fabric NO_SBL_INSTALL_TARGET, R9 acceptance={s['hgk_r9']['acceptance']['verdict']}\")

def c7_hgk_no_fabricated_pass():
    \"\"\"Scope the assertion to THIS programme's subjects.

    An earlier draft asserted \"no PASS anywhere\" and failed on five rows
    (ACC-REF-001, ACC-REQ-FAR-EXEC-IDENTITY-002, ACC-REQ-FAR-LANE-SOD-010/011,
    ACC-AO-INDEP-012) that belong to other rounds and were legitimately earned there.
    A provenance claim must be scoped to the subjects it is about; the unscoped form was
    my defect, not a fabrication by anyone else. These five are recorded as context.
    \"\"\"
    db = HGK / 'var/shared-spine/hg-kseos.db'
    con = sqlite3.connect(f'file:{db.as_posix()}?mode=ro', uri=True)
    rows = con.execute('select acceptance_id,verdict from acceptances').fetchall()
    con.close()
    mine = ('SBL-PIPDLS', 'R7-FARCLO', 'R9-CTRLPKG', 'R10')
    scoped = [(a, v) for a, v in rows if any((k in a for k in mine))]
    bad = [r for r in scoped if r[1] == 'PASS']
    if bad:
        return (False, f'a PASS exists for an SBL subject that was not earned: {bad}')
    others = sorted((a for a, v in rows if v == 'PASS'))
    return (True, f'{len(scoped)} SBL-subject row(s), none PASS; {len(others)} pre-existing PASS row(s) belong to other rounds: {others}')

def c8_candidate_readback():

    def g(*a):
        r = subprocess.run(['git', '-C', str(CAND), *a], capture_output=True, text=True, timeout=300)
        return (r.stdout + r.stderr).strip()
    br = 'candidate/r9-20261021-ctrlpkg'
    local = g('rev-parse', 'HEAD')
    g('fetch', 'origin', br)
    remote = g('rev-parse', f'origin/{br}')
    if local != remote:
        return (False, f'local {local[:8]} != remote {remote[:8]}')
    return (True, f'{br} @ {local[:8]} matches origin')

def c9_control_package_still_pins():
    tool = CAND / 'tools/check_control_package.py'
    r = subprocess.run([sys.executable, str(tool), '--verify'], capture_output=True, text=True, cwd=str(CAND), timeout=900)
    if r.returncode != 0:
        return (False, f'control package no longer verifies: {(r.stdout + r.stderr)[:200]}')
    m = json.loads((CAND / 'contracts/CONTROL_PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    return (True, f\"14 docs verify, rollup {m['rollup_sha256'][:16]}\")

def main() -> int:
    check('C1  mandate: three lanes served at rank 1 with the ordered models', c1_mandate_rank1)
    check('C2  registry epoch is a joint invariant on both sides', c2_epoch_joint)
    check('C3  drift gate clean', c3_drift)
    check('C4  runtime surfaces agree WITH EACH OTHER and the pool', c4_surfaces_agree)
    check('C5  handover document carries every section and open item', c5_handover_sections)
    check('C6  handover state JSON is honest', c6_state_json)
    check('C7  no acceptance PASS was fabricated anywhere', c7_hgk_no_fabricated_pass)
    check('C8  candidate branch pushed and read back', c8_candidate_readback)
    check(\"C9  control package still pins after this round's changes\", c9_control_package_still_pins)
    passed = sum((1 for _, ok, _ in results if ok))
    total = len(results)
    verdict = 'R10_SELF_CHECK_PASS' if passed == total else 'R10_SELF_CHECK_FAIL'
    out = R10 / 'SELF_CHECK_R10.json'
    out.write_text(json.dumps({'schema': 'SBL-R10-SELF-CHECK/1', 'verdict': verdict, 'passed': passed, 'total': total, 'checks': [{'label': l, 'ok': ok, 'detail': d} for l, ok, d in results]}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    print(f'\n{verdict}: {passed}/{total}')
    print(f'written {out}')
    return 0 if passed == total else 1
for f in [c2_epoch_joint,c3_drift,c4_surfaces_agree,c7_hgk_no_fabricated_pass]:
 try: print(f.__name__,repr(f()))
 except Exception as e: print(f.__name__,type(e).__name__,str(e))
"
```

Verbatim output excerpt:
```text
c2_epoch_joint (False, 'assignment 29 != registry 30')
c3_drift (True, '0 findings, fatal=False')
c4_surfaces_agree (False, 'governed PLAN plane opencode-go/minimax-m3.1-flash-free != pool PLAN openai-codex/gpt-6.1-sol; provider_route opencode-go/deepseek-v4.1-flash != pool EXECUTE opencode-go/minimax-m3.1-flash-free')
c7_hgk_no_fabricated_pass (True, "13 SBL-subject row(s), none PASS; 5 pre-existing PASS row(s) belong to other rounds: ['ACC-AO-INDEP-012', 'ACC-REF-001', 'ACC-REQ-FAR-EXEC-IDENTITY-002', 'ACC-REQ-FAR-LANE-SOD-010-CONVERGE-PLAN', 'ACC-REQ-FAR-LANE-SOD-011-ROUTER-WINDOW-PLAN']")
```

### Probe `self_controls`
Working directory: `C:/Projects/Agent_Workspace/HG-KSEOS`
Exit code: `0`

```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B -c "import sys,dataclasses
sys.path[:0]=[r'C:/Projects/Agent_Workspace/SBL',r'C:/Projects/Agent_Workspace/HG-KSEOS/src']
from sbl_core.m06_repair import BoundedRepair
from sbl_core.m05_verify import EvidenceVerification
from hg_kseos.spine import SharedSpine
p=BoundedRepair()
for attempts in [1,3]: print('repair',attempts,dataclasses.asdict(p.plan('probe failure',['evidence/probe'],attempts=attempts)))
try:p.plan('probe failure',[])
except Exception as e:print('repair_negative',type(e).__name__,str(e))
v=EvidenceVerification();v.record('probe','read-only positive control',0,'control',1)
print('independent_verdict',dataclasses.asdict(v.verdict('probe','maker','checker','PASS','LOCAL','LOCAL')))
try:v.verdict('probe','maker','maker','PASS','LOCAL','LOCAL')
except Exception as e:print('sbl_self_accept_negative',type(e).__name__,str(e))
s=object.__new__(SharedSpine)
try:s.record_workorder_result('NO_DB_PROBE','same','same','PASS',['probe'])
except Exception as e:print('hgk_self_review_negative',type(e).__name__,str(e))
class TransactionBoundaryReached(Exception):pass
s.transaction=lambda:(_ for _ in ()).throw(TransactionBoundaryReached('distinct checker reaches transaction; no DB opened'))
try:s.record_workorder_result('NO_DB_PROBE','maker','checker','PASS',['probe'])
except TransactionBoundaryReached as e:print('hgk_distinct_checker_control',str(e))
"
```

Verbatim output excerpt:
```text
repair 1 {'plan_id': 'R-2126da379146', 'first_fail': 'probe failure', 'scope': 'NARROW', 'max_attempts': 3, 'rollback_pointer': 'evidence/probe', 'action': 'NARROW_REPAIR'}
repair 3 {'plan_id': 'R-eb3e617b92ff', 'first_fail': 'probe failure', 'scope': 'NARROW', 'max_attempts': 3, 'rollback_pointer': 'evidence/probe', 'action': 'STOP_ESCALATE'}
repair_negative SBLError SBL_E_REPAIR_WITHOUT_EVIDENCE: repair requires at least one evidence reference
independent_verdict {'gate_id': 'probe', 'maker': 'maker', 'checker': 'checker', 'status': 'PASS', 'claim_level': 'LOCAL'}
sbl_self_accept_negative SBLError SBL_E_SELF_CHECK_FORBIDDEN: a maker may not verify its own work
hgk_self_review_negative InvariantViolation ERR_WORKORDER_SELF_REVIEW
hgk_distinct_checker_control distinct checker reaches transaction; no DB opened
```

All three self_check scripts were read in full in memory. Full-script runs are **NOT_EXERCISED**: R9 writes SELF_CHECK_R9.json, creates scratch/tamper copies, rewrites/restores candidate CONTROL_PACKAGE_MANIFEST.json, and fetches; R10 writes SELF_CHECK_R10.json and fetches; R7 includes git fetch. Those effects violate the read-only/exactly-one-output constraint. Instead R10 definitions were AST-extracted in memory (no main, no write/fetch calls), and only c2_epoch_joint, c3_drift, c4_surfaces_agree, c7_hgk_no_fabricated_pass were executed. The exact subprocess code is recorded above. Harness exit 0 is not check success: c2 and c4 returned False.

| Capability | Exists? | Actual gate/consumer? | Measured state |
|---|---|---|---|
| Self-detect | Yes: R7/R9/R10 checks and M05 evidence verification | Scripts return nonzero on failed aggregate (R7 sys.exit(1), R9/R10 return 1); no mandatory production caller of self_check_r* found in runtime/tools/CI. Selected read-only checks detect current epoch/route disagreements. | PASS for detection; not a proven mandatory autonomous gate. |
| Self-repair | Yes: M06 BoundedRepair; SharedCore constructs it | Missing evidence raises; attempt cap returns STOP_ESCALATE. Search found no runtime consumer that executes NARROW_REPAIR or enforces STOP_ESCALATE; only producer plus contract vocabulary. | PARTIAL planner/refusal; autonomous execution NOT_EXERCISED and not demonstrated. |
| Self-accept | No permitted same-maker acceptance; independent-verdict API exists | SBL M05 refuses equal normalized maker/checker; HGK spine refuses writer==checker before opening transaction. | FAIL as an autonomous self-accept capability; refusal gate PASS. |
| Self-evolve | Yes as a recorded research delta/lesson artifact; no demonstrated self-applying runtime | R7 SELF_EVOLUTION_DELTA.json records seven adopted lessons, but no mandatory apply/validate/rollback consumer was established. | FAIL for autonomous governed evolution, not absence of the ledger. |

Live load-bearing refusal: `src/hg_kseos/spine.py:345-346`:
```python
if writer == checker:
    raise InvariantViolation("ERR_WORKORDER_SELF_REVIEW")
```

The negative control invoked the actual SharedSpine.record_workorder_result on an uninitialized object; equality is checked before any database access. The distinct-checker control deliberately stops at an overridden transaction sentinel, proving it crosses the equality gate but never opening/writing a DB. This is not a positive acceptance test. SBL M05 also had a genuine in-memory independent LOCAL verdict positive control and same-maker refusal negative control.

Therefore SBL **cannot self-accept as the same writer/checker** under HGK. An autonomous system may arrange a separate independent checker and host acceptance, but calling that “self-accept” must not erase principal separation. Neither a green self-check receipt, a locally returned Verdict, nor different arbitrary strings is independent host-issued acceptance. R9/R10 explicitly assert no maker-authored PASS; live R10 scoped readback finds 13 SBL-subject acceptance rows, none PASS.

Current defect detected while the generic drift gate remained green:
```text
c2_epoch_joint (False, 'assignment 29 != registry 30')
c3_drift (True, '0 findings, fatal=False')
c4_surfaces_agree (False, 'governed PLAN plane opencode-go/minimax-m3.1-flash-free != pool PLAN openai-codex/gpt-6.1-sol; provider_route opencode-go/deepseek-v4.1-flash != pool EXECUTE opencode-go/minimax-m3.1-flash-free')
c7_hgk_no_fabricated_pass (True, "13 SBL-subject row(s), none PASS; 5 pre-existing PASS row(s) belong to other rounds: ['ACC-AO-INDEP-012', 'ACC-REF-001', 'ACC-REQ-FAR-EXEC-IDENTITY-002', 'ACC-REQ-FAR-LANE-SOD-010-CONVERGE-PLAN', 'ACC-REQ-FAR-LANE-SOD-011-ROUTER-WINDOW-PLAN']")
```

R7 self-evolution ledger source:
`C:/Projects/Agent_Workspace/SBL/_governance/round-20261021-r7/20_FAR/far-20261021-023/SELF_EVOLUTION_DELTA.json`: schema LOGICAL_FAR_SELF_EVOLUTION_DELTA_V1, proposed_evolution EVO-1..EVO-7, adopted_now seven entries, not_yet_applied empty. This is a producer assertion, not independently verified activation.

## Repository preservation and limits

Before/after git status readbacks match. HG-KSEOS clean. SBL retains pre-existing untracked `contracts/SBL_C0_C9_CONTRACT-R9.json` and `contracts/compiled-r9/`; neither was touched. Initial and final HEADs are the supplied commits. No repairs attempted.

Probe issues are not product defects: the initial self-consumer search used absent SBL/src and SBL/scripts and exited 2; it was retried against actual sbl_core/sbl_sp/tools/.github and the whole repository. An additional pathlib traversal into HGK var hit a missing nested plugin reference; the required rg census and its error counts above remain authoritative. No missing/unreadable evidence was fabricated. Runtime tool spillover/cache files may be created by the tooling itself; this audit writes only the requested evidence deliverable.
