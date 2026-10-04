# -*- coding: utf-8 -*-
"""
RP-002 C1 — Coding Factory second acceptance: materialize 4 HGK Profile Distributions
+ HGK/TEAM.md + HGK_STACK_MANIFEST.yaml + RP002/TEAM.md (FIT-GAP -> REUSE -> BIND -> ADAPT -> TEST).

Reuse-first:
  - Hermes profile distribution format (pinned v0.20.0) — no new package manager.
  - HGK control/skills as inherited capability references — no duplicate skills.
  - config.yaml mirrors the certified opencode-go/deepseek-v4-flash route — no new provider.
No duplicate OSS implementation; fake named-method = 0; silent fallback = 0.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sys
from pathlib import Path

FAB = Path(r"C:\Projects\Agent_Workspace\Fabric")
PROFILES = FAB / "profiles"

DIST_TEMPLATE = """name: {name}
version: 0.1.0
description: "{description}"
hermes_requires: ">=0.12.0"
author: "RP-002 HGK"
license: "MIT"
env_requires:
  - name: OPENCODE_GO_API_KEY
    description: "OpenCode Go API key (provider route for this profile)"
    required: true
"""

SOUL_TEMPLATE = """# {title}

You are the **{name}** Hermes profile, part of the RP-002 HGK Profile Team
(HGK-REFERENCE-PROJECT-002, Fabric-Governed / Profile-Distributed / Kanban-Coordinated).

## Identity & boundaries
- Stack: HGK_ENGINEERING (governance/normative plane owner: HG-KSEOS)
- Profile = identity/state/role boundary, NOT a security sandbox (Hermes upstream; RP-002 r3 §4.4).
- You are an executor role inside frozen governance; you never self-approve final candidates.

## Role
{role}

## Invariants (fail-closed)
- FILES_FIRST / NO_SOURCE_NO_NORM: every claim must trace to an admitted source locator.
- WorkOrder is the normative executor contract; Kanban is runtime pointer only.
- Maker != final checker; your own summary is never acceptance evidence.
- Production autonomy NOT_CLAIMED; live broker write FORBIDDEN.
- Silent provider/model fallback FORBIDDEN (preserve opencode-go/deepseek-v4-flash route).
- Critical writes: write -> raw readback -> truncation sentinel scan -> SHA-256 -> parse/lint -> focused test.

## Inputs / Outputs
{io}
"""

CONFIG_TEMPLATE = """# {name} — RP-002 profile config (inherits certified HGK route; no silent downgrade)
model:
  provider: opencode-go
  default: deepseek-v4-flash
  base_url: https://opencode.ai/zen/go/v1
  api_mode: chat_completions
approvals:
  mode: manual
agent:
  max_turns: 300
  verify_on_stop: false
skills:
  external_dirs: []
"""

GITIGNORE = """auth.json
.env
.env.EXAMPLE
state.db*
hermes_state.db
response_store.db*
gateway.pid
gateway_state.json
processes.json
auth.lock
active_profile
.update_check
memories/
sessions/
logs/
plans/
workspace/
home/
image_cache/
audio_cache/
document_cache/
browser_screenshots/
cache/
hermes-agent/
.worktrees/
profiles/
bin/
node_modules/
local/
checkpoints/
sandboxes/
backups/
errors.log
.hermes_history
"""

PROFILE_SPECS = [
    {
        "name": "hgk-orchestrator",
        "title": "HGK Orchestrator",
        "description": "HGK lifecycle/orchestration; consumes Fabric policy; WorkOrder admission; Hermes/Kanban pointer ABI",
        "role": ("Own the HGK engineering lifecycle: WorkOrder admission, gate sequencing, factory handoffs, "
                 "policy consumption (Fabric governance contracts via HGK APL hooks), checkpoint/resume, "
                 "and BreakGlass escalation. Kanban is runtime pointer, never second task truth."),
        "io": ("IN: WorkOrder contracts, gate evidence, policy events. OUT: bounded orders, checkpoints, "
               "orchestration evidence, TT/CR updates."),
    },
    {
        "name": "hgk-knowledge-factory",
        "title": "HGK Knowledge Factory",
        "description": "Source-bound knowledge distillation; source inventory, authority router, retrieval/crosswalk",
        "role": ("Distill admitted corpora (教程字幕, RP-002 corpus, HGK/SQS controls) into source-bound engineering "
                 "norms: provenance, dedup, CURRENT/SUPERSEDED/CONDITIONAL/REJECTED/DEFERRED, requirements/decisions/"
                 "OSS/risk/acceptance crosswalk. Never invent norms; unsupported norm = 0."),
        "io": "IN: source inventory + admitted corpora. OUT: distillation ledgers, crosswalks, evidence candidates.",
    },
    {
        "name": "hgk-document-factory",
        "title": "HGK Document Factory",
        "description": "ADR/SDD/TaskSpec docs; current doc factory rules, requirement/evidence/rollback crosswalk",
        "role": ("Close Requirement -> ADR/SDD -> TaskSpec -> WorkOrder -> Acceptance -> Evidence -> Rollback with "
                 "required_requirement_orphan = 0. Consumes only K1-sealed current contract."),
        "io": "IN: sealed requirement ledger + design inputs. OUT: design contract, task specs, work orders, acceptance bindings.",
    },
    {
        "name": "hgk-coding-factory",
        "title": "HGK Coding Factory",
        "description": "Bounded implementation; Codex/OpenCodex route, OpenSpec/gstack/Spec Kit router, tests",
        "role": ("Execute FIT-GAP -> REUSE -> INSTALL/QUALIFY only if needed -> BIND/ADAPT -> TEST. Codex CLI is the "
                 "bounded writer for tracked code changes (OpenCodex proxy route). OpenSpec = active brownfield; "
                 "gstack = selected advisory slices; Spec Kit = standby XOR. Fake invocation/silent fallback = 0."),
        "io": "IN: admitted TaskSpec + frozen requirement. OUT: bounded code changes, tests, maker evidence, rollback proof.",
    },
]

TEAM_MD = """# HGK TEAM — RP-002 Profile Team Topology

stack_id: HGK_ENGINEERING
stack_manifest: HGK_STACK_MANIFEST.yaml
oracle_profile: construction-acceptance-oracle (internalized at O1; external frozen oracle before)
coordination: Hermes Kanban (board RP002-FABRIC-BOOTSTRAP, project-scoped)

## Roles
| Profile | Primary role | Handoff out | Handoff in |
|---|---|---|---|
| hgk-orchestrator | lifecycle/orchestration; WorkOrder admission; policy consumption | bounded order -> factories | gate evidence, policy events |
| hgk-knowledge-factory | source-bound distillation | K1-sealed current contract -> document factory | admitted corpora + source inventory |
| hgk-document-factory | ADR/SDD/TaskSpec/WO/acceptance chain | sealed engineering contract -> coding factory | K1-sealed contract |
| hgk-coding-factory | bounded implementation (Codex writer) | code + tests + maker evidence -> oracle checker | admitted TaskSpec |

## Handoff rules
1. WorkOrder is the executor contract; Kanban keeps runtime pointer/status only.
2. A downstream factory consumes only the SEALED output of the upstream factory.
3. Maker != checker: coding factory output is verified by the oracle CHECKER in a fresh read-only context.
4. Any divergence between WorkOrder and Kanban state -> BLOCK + reconcile from WorkOrder.

## Boundaries
- HGK/TEAM.md is not an Authority Matrix; powers come from Fabric/HGK/SQS controls.
- Profile != security sandbox (least privilege + separate credentials where required).
- No live broker write; production autonomy NOT_CLAIMED.
"""

STACK_MANIFEST = """schema: RP002-STACK-MANIFEST/1
stack_id: HGK_ENGINEERING
profiles:
  - hgk-orchestrator
  - hgk-knowledge-factory
  - hgk-document-factory
  - hgk-coding-factory
authority_domain: [SOFTWARE_ENGINEERING, AGENTIC_ENGINEERING_GOVERNANCE]
services: [source_ledger, evidence_store, knowledge_fts]
knowledge_namespace:
  read: ["hgk.*", "shared.*"]
  write: ["hgk.*"]
  promote: ["hgk.*"]
runtime: {engine: hermes, coordination: kanban, board_policy: project_scoped}
acceptance: {oracle_profile: construction-acceptance-oracle}
inherited_capabilities:
  codex: {owner_profile: hgk-coding-factory, rule: PRESERVE_CURRENT_CERTIFIED_ROUTE_OR_REQUALIFY}
  opencodex_opencode_provider: {owner_profile: hgk-coding-factory, rule: NO_SILENT_FALLBACK}
  openspec: {state: CERTIFIED_ACTIVE_BROWNFIELD, owner_profile: hgk-coding-factory, rule: NO_SILENT_FALLBACK}
  gstack: {state: CERTIFIED_SELECTED_SLICES, authority: ADVISORY_NOT_REDUCER}
  spec_kit: {state: INHERITED_STANDBY_XOR, rule: NO_DUAL_SPEC_OWNER}
  governed_evolution: {state: INHERITED_REQUIRED}
  independent_checker_reducers: {state: INHERITED_REQUIRED_FINAL_AUTHORITY}
"""

RP002_TEAM_MD = """# RP002 TEAM — Project Composition

team_id: RP002_FABRIC_BOOTSTRAP
project_id: HGK-REFERENCE-PROJECT-002
execution_graph: rp002/RP002_EXECUTION_GRAPH.yaml
gate_catalog: rp002/RP002_GATE_CATALOG.yaml

## Members
- bootstrap_executor: CURRENT_CERTIFIED_HGK_RUNTIME (G0~C1)
- post_h1_profiles: [hgk-orchestrator, hgk-knowledge-factory, hgk-document-factory, hgk-coding-factory, construction-acceptance-oracle]
- post_sqp1_profiles: [sqs-orchestrator, sqs-data-analysis, sqs-risk]

## Constraints
- self_hosting_required_after: F1
- live_broker_write: false
- fabric_authority_matrix_is_external_to_team_md: true
- G0~C1 executed by current certified HGK runtime; profile team not assumed before H1
- internal Oracle candidate null until O1 (external frozen bootstrap oracle before)
"""


def main() -> int:
    created = []
    for spec in PROFILE_SPECS:
        d = PROFILES / spec["name"]
        (d / "skills").mkdir(parents=True, exist_ok=True)
        (d / "distribution.yaml").write_text(DIST_TEMPLATE.format(**spec), encoding="utf-8")
        (d / "SOUL.md").write_text(SOUL_TEMPLATE.format(**spec), encoding="utf-8")
        (d / "config.yaml").write_text(CONFIG_TEMPLATE.format(name=spec["name"]), encoding="utf-8")
        (d / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
        (d / "README.runtime-contract.md").write_text(
            f"# {spec['name']} runtime contract\n\nSee HGK/TEAM.md + HGK_STACK_MANIFEST.yaml for role/boundaries.\n"
            f"Install: `hermes profile install {d} --name {spec['name']}`\n",
            encoding="utf-8")
        created.append(spec["name"])

    (FAB / "HGK" / "TEAM.md").parent.mkdir(parents=True, exist_ok=True)
    (FAB / "HGK" / "TEAM.md").write_text(TEAM_MD, encoding="utf-8")
    (FAB / "HGK_STACK_MANIFEST.yaml").write_text(STACK_MANIFEST, encoding="utf-8")
    (FAB / "RP002" / "TEAM.md").parent.mkdir(parents=True, exist_ok=True)
    (FAB / "RP002" / "TEAM.md").write_text(RP002_TEAM_MD, encoding="utf-8")

    manifest = {
        "artifact_id": "RP002_C1_MATERIALIZATION",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "profiles_created": created,
        "team_files": ["HGK/TEAM.md", "RP002/TEAM.md"],
        "stack_manifest": "HGK_STACK_MANIFEST.yaml",
        "reuse_notes": [
            "Hermes profile distribution format (pinned v0.20.0) — no new package manager",
            "HGK control/skills referenced as inherited capabilities — no duplicated skills",
            "config.yaml mirrors certified opencode-go/deepseek-v4-flash route — no new provider",
        ],
    }
    out = FAB / "rp002" / "C1" / "RP002_C1_MATERIALIZATION.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
