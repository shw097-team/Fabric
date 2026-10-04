# fabric-desktop-ufo2 — RP-002 Profile Runtime Contract instance
schema: RP002-PROFILE-RUNTIME-CONTRACT/1
profile_id: fabric-desktop-ufo2
team_id: fabric-desktop-automation
provider: MICROSOFT_UFO2
state: MATERIALIZED_PENDING_QUALIFICATION

## Distribution
distribution_ref: Fabric/profiles/fabric-desktop-ufo2/distribution.yaml
version: 0.1.0
hermes_requires: ">=0.12.0"
commit_digest: BOUND_AT_DISTRIBUTION_FREEZE

## Config / SOUL / skills / MCP
config: Fabric/profiles/fabric-desktop-ufo2/config.yaml
soul: Fabric/profiles/fabric-desktop-ufo2/SOUL.md
skills: [] (UFO2 runtime install pending qualification)
mcp: local/in-process or current admitted transport; no network listener by default

## Runtime identity / permissions
runtime_identity: HERMES_PROFILE (on-demand)
permissions:
  inspect_target_app: ALLOW
  capture_target_app_only: ALLOW
  uia_win32_visual_observation: ALLOW (provider-supported)
  click_type_within_admitted_target: ALLOW_BOUNDED
  unrelated_desktop_app: DENY
  password_mfa: DENY (HumanGate)
  external_web_search_for_xq_execution: DENY (default)
  fabric_policy_mutation: DENY
  workorder_creation: DENY
  self_promotion: DENY
  self_acceptance: DENY
  live_broker_write: DENY (NOT_AUTHORIZED)

## I/O
inputs: WorkOrder + ExecutionBinding + deterministic route + target identity
outputs: action receipts + readback refs + evidence candidates (candidate-only knowledge write)

## Fixtures / rollback
positive_fixtures: FDA-XQ-PAPER-V1 classes UFO2-eligible (complex/custom control, hybrid GUI-API) when certified
negative_fixtures: credential entry, live write, second-writer, unknown-state retry, network listener, web-search escape
rollback: disable profile / unpin driver / revert to alternate provider (fabric-desktop-cua) per capability matrix

## Qualification status
effective_load: PENDING (UFO2 runtime NOT installed on current host at C0 readback)
qualification_gate: FDA-C3
