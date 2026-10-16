# Spec delta — lane governance gates (round LANE-RELIABILITY-CLOSURE-20261016)

## ADDED Requirements

### Requirement: The reasoning-effort axis is enforced at the pre-dispatch gate

`scripts/runtime_role_binding_assert.py` SHALL compare the round mandate's declared per-lane
`reasoning_effort` against the declared arm's pool entry, and SHALL refuse on disagreement or on an
unverifiable comparison, using this axis's own typed codes and its own exit code 7 so the outcome
stays distinguishable from the mandate/pool/toolchain refusals (2/3/4/5/6). It SHALL also accept an
explicitly supplied served effort and refuse when it disagrees with the mandate.

Before this change the file contained ZERO occurrences of `effort` (measured:
`grep -c effort scripts/runtime_role_binding_assert.py` == 0), so a lane served at a different
reasoning effort than the mandate names was refused by nothing.

#### Scenario: The mandate's effort disagrees with the declared arm's pool entry

- **WHEN** the mandate declares `reasoning_effort: medium` and the declared arm's pool entry declares `high`
- **THEN** the gate exits 7 and prints `ERR_MANDATE_EFFORT_MISMATCH`

#### Scenario: The mandate names an effort the pool cannot verify

- **WHEN** the mandate declares `reasoning_effort: medium` and the declared arm's pool entry declares none
- **THEN** the gate exits 7 and prints `ERR_MANDATE_EFFORT_UNDECLARED_IN_POOL`

#### Scenario: A served effort is supplied with no mandate effort to compare it to

- **WHEN** `--served-effort medium` is supplied and the lane's mandate declares no `reasoning_effort`
- **THEN** the gate exits 7 and prints `ERR_SERVED_EFFORT_UNVERIFIABLE`

#### Scenario: A served effort disagrees with the mandate

- **WHEN** the mandate declares `medium` and `--served-effort high` is supplied
- **THEN** the gate exits 7 and prints `ERR_SERVED_EFFORT_MISMATCH`

#### Scenario: Lane with no declared effort stays a pass-through

- **WHEN** neither the mandate nor the pool entry declares an effort (the EXECUTE shape)
- **THEN** the gate exits 0 and reports `effort_verified: false`

### Requirement: A mutating call with no attributable session id is answered, not turned into an outage

`scripts/hgk-governed-runtime-controller.py` SHALL answer a mutating tool call that carries no
session id — absent, `null`, or blank — with a single JSON object on exit 0 and the reason
`no-session-id-unattributable`, because a governed role binding requires a non-empty session and so
such a call cannot belong to a governed round. It SHALL NOT map that case to exit 3.

The guard sends `getattr(agent, "session_id", "") or ""` and allows only on exit 0, so mapping this
case to exit 3 refused EVERY mutating call of any agent whose session id was absent — an outage, and
inconsistent with the already-allowed valid-but-unknown id case.

#### Scenario: Blank session id with a write inside a protected root

- **WHEN** the payload carries `session_id: ""` and a `write_file` whose target is inside a protected root
- **THEN** the controller exits 0 and prints `{"action": "allow", "reason": "no-session-id-unattributable"}`

#### Scenario: Null session id with a write inside a protected root

- **WHEN** the payload carries `session_id: null` and the same `write_file`
- **THEN** the controller exits 0 and prints the same answer and reason

#### Scenario: A real governed maker session still denies the same write

- **WHEN** the payload carries a session id that resolves to a live governed EXECUTE binding whose write order covers the protected root
- **THEN** the controller still denies, with the work order id in the reason (the positive control for the two scenarios above)

## MODIFIED Requirements

### Requirement: The lane-routing registry's publication epoch tracks its own content

`config/lane-routing-registry.yaml` SHALL advance its `epoch` whenever any committed byte that a
`projections[].bindings[]` pointer pins changes, SHALL re-pin `source_of_routes.revision` and
`source_of_routes.sha256` to the assignment file's final bytes, and SHALL keep every binding's
`expected` equal to the value the referenced site actually holds.

Measured before this round: the `hermes-codex-lane` binding `/codex_sha256` expected the PRE-repair
digest `D13914CE...DAEC` while the live config carried `e98c516f...b99e`, which made
`lane_policy.check_drift(registry=reg)` fatal (1 `DRIFT_VALUE` finding) even on a pristine tree.

#### Scenario: A pinned digest is corrected to the measured live value

- **WHEN** the corrected binding and the re-pinned `source_of_routes` digest are in place and the epoch is advanced
- **THEN** `check_drift` returns ZERO findings on the canonical root

#### Scenario: The integrity gate can no longer pass on a corrupted tree

- **WHEN** a projection site is altered after the registry was re-pinned
- **THEN** `tests/test_lane_policy.py::test_drift_injection_subcases` detects it (its pristine baseline must be clean for the injection sub-cases to mean anything)
