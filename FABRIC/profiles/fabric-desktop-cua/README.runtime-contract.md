# fabric-desktop-cua — RP-002 Profile Runtime Contract instance
schema: RP002-PROFILE-RUNTIME-CONTRACT/1
profile_id: fabric-desktop-cua
team_id: fabric-desktop-automation
provider: CUA_DRIVER
state: MATERIALIZED_PENDING_QUALIFICATION

## Distribution
distribution_ref: Fabric/profiles/fabric-desktop-cua/distribution.yaml
version: 0.1.0
hermes_requires: ">=0.12.0"
commit_digest: BOUND_AT_DISTRIBUTION_FREEZE

## Config / SOUL / skills / MCP
config: Fabric/profiles/fabric-desktop-cua/config.yaml
soul: Fabric/profiles/fabric-desktop-cua/SOUL.md
skills: [] (inherits Hermes computer_use toolset; cua-driver install pending qualification)
mcp: stdio/in-process local preferred; no network listener

## Runtime identity / permissions
runtime_identity: HERMES_PROFILE (on-demand)
permissions:
  inspect_target_app: ALLOW
  capture_target_app_only: ALLOW
  click_type_within_admitted_target: ALLOW_BOUNDED
  unrelated_desktop_app: DENY
  password_mfa: DENY (HumanGate)
  fabric_policy_mutation: DENY
  workorder_creation: DENY
  self_promotion: DENY
  self_acceptance: DENY
  live_broker_write: DENY (NOT_AUTHORIZED)

## I/O
inputs: WorkOrder + ExecutionBinding + deterministic route + target identity
outputs: action receipts + readback refs + evidence candidates (candidate-only knowledge write)

## Fixtures / rollback
positive_fixtures: FDA-XQ-PAPER-V1 classes CUA-eligible (launch/locate, compile pass/fail readback, PAPER config, log/export readback)
negative_fixtures: credential entry, live write, second-writer, unknown-state retry, network listener
rollback: disable profile / unpin driver / revert to alternate provider (fabric-desktop-ufo2) per capability matrix

## Qualification status
effective_load: PENDING (cua-driver NOT installed on current host at C0 readback)
qualification_gate: FDA-C2
