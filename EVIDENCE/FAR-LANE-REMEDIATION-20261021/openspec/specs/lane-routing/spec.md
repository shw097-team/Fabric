## ADDED Requirements

### Requirement: Single declared rank-1 per lane, agreeing across surfaces

The lane declaration surfaces (`config/lane-routing-registry.yaml`, `config/model-lane-assignment.json`,
`config/lane-route-slots.candidate.json`, `AGENTS.md`, the in-Hermes PLAN-plane profile, and the owner-chain
conformance test) SHALL declare the same rank-1 provider/model and engine per lane for the current epoch.

#### Scenario: Registry and governing doc agree

- **WHEN** `lane_policy.route_for_lane(registry,'PLAN')` is read
- **THEN** it returns `openai-codex` / `gpt-6.1-sol` with `engine: hermes`, matching the `AGENTS.md` lane-chain contract
- **AND** `route_for_lane(registry,'VERIFY_SECURITY')` returns `openai-codex` / `gpt-6.1-sol` with `engine: codex-cli`

### Requirement: Declared collisions are recorded, never hidden

When the owner mandates the same model on PLAN and VERIFY_SECURITY, the registry SHALL carry a
`declared_conflicts` entry with status `OPEN_OWNER_ORDERED` and the SoD pair SHALL set `distinct_required: false`;
no surface may report model-axis independence for that pair.

#### Scenario: Divergent writer and checker stay distinct

- **WHEN** `lane_policy.check_sod(route_for_lane(reg,'EXECUTE'), route_for_lane(reg,'VERIFY_SECURITY'))` runs
- **THEN** it reports distinct models (`deepseek-v4.1-flash` vs `gpt-6.1-sol`)

### Requirement: Toolchain pin is executable and measured

`config/hermes-codex-lane.json::codex_executable` SHALL name an existing binary whose `--version` equals
`codex_version`, and `codex_sha256` SHALL equal the sha256 of those bytes.

#### Scenario: Drift gate is clean

- **WHEN** `lane_policy.check_drift(registry=reg)` runs after the change
- **THEN** it returns an empty list
- **AND** the pinned executable exists on disk

### Requirement: Pool rank order and role labels agree

`config/lane-route-slots.candidate.json::lanes[].ordered_pool` SHALL label the rank-1 entry `DEFAULT/首選`
and subsequent entries as fallbacks in the same order as the lane's declared fallback chain.
