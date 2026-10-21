# lane-routing — MiniMax mandate (epoch 25)

## ADDED Requirements

### Requirement: All three governed lanes serve the owner-mandated MiniMax arm

The control plane SHALL bind the PLAN, EXECUTE and VERIFY_SECURITY lanes to the arm
`opencode-go/minimax-m3.1-flash-free` as their rank-1, default and automatically-selected arm,
by owner order 2026-10-21.

The pool artifact (`config/lane-route-slots.candidate.json`) SHALL remain the single selection
authority: the registry routes, the assignment's lane chains, the assignment rows and the
VERIFY supply selector SHALL be **derived** from the pool rather than independently declared,
so that the three cannot drift apart silently.

The binding SHALL NOT delete any previously declared arm. Every former rank-1 arm SHALL remain
reachable as an operator-selectable fallback, so that a later owner order can restore a prior
binding without re-deriving the pool.

#### Scenario: The three lanes are bound to the mandated arm

- **WHEN** the pool is read for PLAN, EXECUTE and VERIFY_SECURITY
- **THEN** each pool's first entry has `provider = opencode-go`, `model = minimax-m3.1-flash-free`
- **AND** each pool's first entry has `default = true` and `automatic_selection = true`
- **AND** each pool's ranks are contiguous `1..N` with no gap
- **AND** the registry's three routes and the assignment's three lane chains all name the same
  provider and model as that pool entry

#### Scenario: A former default arm stays reachable

- **WHEN** a lane's pool is inspected after the binding
- **THEN** every arm that was present before the binding is still present
- **AND** it carries `default = false`
- **AND** it is addressable by its rank for an operator-selectable dispatch

### Requirement: The model-axis collision is declared, not hidden

When the same model serves a maker lane and a checker lane by owner order, the registry SHALL
declare the collision in `sod_invariants.declared_conflicts` with an explicit
`OPEN_OWNER_ORDERED` status, and the corresponding `sod_invariants.pairs` entry SHALL carry
`distinct_required: false` **together with the reason**.

The registry SHALL NOT claim model-axis independence in that state, and SHALL NOT claim that
correlated blind spots inside the shared model family are absent.

#### Scenario: A writer and a checker share one model by owner order

- **WHEN** the EXECUTE arm and the VERIFY_SECURITY arm resolve to the same model
- **THEN** `sod_invariants.declared_conflicts` contains an entry with status `OPEN_OWNER_ORDERED`
  naming that pair and the model
- **AND** the `EXECUTE → VERIFY_SECURITY` pair has `distinct_required: false`
- **AND** the pair's note states the owner order that caused it

#### Scenario: The residual separation is stated accurately

- **WHEN** the assignment's `sod` block is read
- **THEN** the model-separation statements say that model-axis separation is absent by owner order
- **AND** they name the remaining separations: process, lane, evidence-path, and the
  no-self-acceptance rule

### Requirement: The mandate is proved by serving, not by declaration

A lane SHALL be reported as serving the mandated arm only when a real dispatch produced a
receipt whose `required_arm` and `served_arm` are both the mandated arm, whose exit status is
zero, and in which the model actually invoked a tool. A direct completion against the relay
SHALL NOT by itself upgrade a lane to admitted.

The HGK admission receipt SHALL report `ADMITTED` only when the exercise records at least one
completed model call AND at least one completed tool, and the served provider and model match
the requested arm.

#### Scenario: A lane that answers but never runs a tool is not admitted

- **WHEN** a lane exercise records one model call but zero completed tools
- **THEN** the admission status is not `ADMITTED`
- **AND** the refusal is recorded rather than upgraded

#### Scenario: A lane that runs a tool at the mandated arm is admitted

- **WHEN** a dispatch to the mandated arm exits zero, its receipt reports
  `required_arm == served_arm == opencode-go/minimax-m3.1-flash-free`, and the lane exercise
  records at least one completed tool
- **THEN** the admission status is `ADMITTED`
- **AND** the receipt names the transport id that was actually sent
