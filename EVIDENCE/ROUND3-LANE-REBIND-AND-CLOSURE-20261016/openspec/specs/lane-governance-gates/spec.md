# lane-governance-gates — delta for hgk-round3-lane-rebind-20261016

## ADDED Requirements

### Requirement: The declaring surface and the enforcing surface SHALL agree on a demoted SoD pair

Where the registry declares a maker/checker pair as `distinct_required: false` together with a
`declared_conflicts` entry, the pre-dispatch guard SHALL reach the same conclusion as the registry: the pair
is dispatchable. Where a pair is same-model and NO such declaration exists, the guard SHALL refuse. A guard
stricter than the declaration it serves makes an owner-ordered configuration undispatchable; a guard looser
than the declaration permits silent self-verification. Neither is acceptable.

#### Scenario: An owner-ordered pair reaches the guard

- **WHEN** the checker's model equals the maker's model and the registry declares that exact pair with
  `distinct_required: false` and a `declared_conflicts` entry whose status is `OWNER_ORDERED_IN_FORCE`
- **THEN** the guard SHALL pass the distinctness check AND the verdict SHALL carry the conflict id, so the
  exemption is visible in every receipt and never silent

#### Scenario: An undeclared collision reaches the guard

- **WHEN** the checker's model equals the maker's model and no matching declaration exists, or the
  declaration's status is anything other than `OWNER_ORDERED_IN_FORCE`, or the pair is still declared
  `distinct_required: true`
- **THEN** the guard SHALL refuse with the distinctness violation code, unchanged from its prior behaviour

#### Scenario: The maker lane cannot be determined

- **WHEN** the caller does not name the maker lane and the maker model matches the default arm of more than
  one route, or of no route
- **THEN** the guard SHALL NOT apply any exemption (fail closed)

### Requirement: A SoD declaration SHALL be superseded, never deleted

When a collision recorded in `declared_conflicts` ceases to hold because the owner order changed, its entry
SHALL move to a superseded status carrying a reference to the superseding order, and SHALL remain readable in
the registry.

#### Scenario: The collision's premise changes

- **WHEN** the owner order re-points one of the two lanes so that the recorded collision no longer exists
- **THEN** the historical entry SHALL remain, marked superseded, with the superseding order named — and a new
  entry SHALL declare the collision the new order creates, if any

### Requirement: The conformance fixture SHALL move with the owner order in the same change

The fixture that asserts each lane's rank-1 default and fallback order SHALL be updated in the same change as
the order it encodes, because the fixture's invariant IS the current owner order; a change that moves the
registry without moving the fixture is incomplete and SHALL fail its own suite.

#### Scenario: A rebind lands without the fixture

- **WHEN** a route row's default arm or fallback order changes and the fixture still asserts the previous
  order
- **THEN** the conformance suite SHALL fail, and the rebind SHALL be treated as not landed
