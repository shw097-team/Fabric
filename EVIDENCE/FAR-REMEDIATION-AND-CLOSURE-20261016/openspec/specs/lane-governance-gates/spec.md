# lane-governance-gates — delta for hgk-far-remediation-20261016

## ADDED Requirements

### Requirement: A lane's route row SHALL agree with the surface that selects the lane's model

The registry's per-lane route row and the ordered pool that the dispatch path actually consumes SHALL
declare the same provider and model for a lane. Where they disagree, the disagreement SHALL be recorded
as a finding with a named authority, and SHALL NOT be left implicit.

#### Scenario: A route row retained from a superseded order

- **WHEN** a route row's `selection_authority` names an order whose stated premise has since been
  measured false
- **THEN** the row SHALL be rebound to the arm named by the order in force, and the superseded premise
  SHALL be retained as a dated note rather than deleted.

#### Scenario: The conformance gate reads the route row

- **WHEN** the conformance test compares a lane's default arm against the owner chain
- **THEN** it SHALL pass on the canonical tree after the rebind, and the registry `epoch` SHALL have
  advanced exactly once for that change.

### Requirement: A declared SoD conflict SHALL state whether it is open or ordered

A declared conflict between two roles SHALL carry a status that distinguishes "awaiting an owner
decision" from "ordered by the owner". An ordered overlap SHALL name the order it rests on and SHALL
state which form of independence remains.

#### Scenario: Two roles are deliberately given the same model

- **WHEN** the owner orders the same model for the planner and the acceptance officer
- **THEN** the conflict SHALL read as ordered, not open, and the surviving process / lane /
  evidence-path independence SHALL be written into the same record.

### Requirement: A verified change SHALL NOT remain permanently unpromoted without a stated reason

Where a change set has been verified over a frozen subject and the canonical product still carries the
pre-change behaviour, the round SHALL either promote it under an explicit authorisation or record the
authorisation that is missing.

#### Scenario: A verified candidate closes a live outage

- **WHEN** the same fixture returns the faulty behaviour on the canonical tree and the fixed behaviour on
  the verified candidate
- **THEN** the promotion SHALL be applied under a recorded authorisation, with per-file backups and
  before/after digests, and the applied product SHALL be re-derived rather than trusted.

## MODIFIED Requirements

### Requirement: A lane turn's shape SHALL be selectable and SHALL be recorded

The lane dispatch surface SHALL accept an optional turn-shape selection whose `edit_only` value
constrains the turn to writing files and forbids the behaviours measured to stall a lane, and the
receipt SHALL record the shape actually used. The default SHALL remain behaviourally unchanged, and no
existing flag's meaning SHALL change.

#### Scenario: A bounded writer turn that would otherwise run the oracle

- **WHEN** a change set needs a test suite to validate it
- **THEN** the writer's turn MAY be dispatched edit-only, with the orchestration side owning the
  re-derivation, and the receipt SHALL say so.

#### Scenario: An existing invocation

- **WHEN** no turn shape is requested
- **THEN** the dispatch SHALL behave exactly as before the flag existed.

## REMOVED Requirements

None.
