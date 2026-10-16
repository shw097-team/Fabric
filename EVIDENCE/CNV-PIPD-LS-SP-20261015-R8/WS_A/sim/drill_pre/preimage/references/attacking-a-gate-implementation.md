# Attacking a gate implementation (a checklist for the checker)

A "gate" is any code or config whose job is to assert a property before an action is allowed: a
credential-posture preflight, a permission check, a write-set guard, a pre-spawn precondition, a
policy assertion. They fail the same ways. Point the checker at this list -- every item is a defect
class that has been reproduced in a governed round, not a hypothetical.

## The single shape to hunt

**The gate reports PASS exactly when it could not establish the property.** Restate the gate's own
claim as "this proves X", then try to satisfy the gate WITHOUT X holding. If you can, the gate is
fail-open and every verdict downstream of it is void for that property.

## The ways

1. **Any-value scan instead of effective-value resolution.** "Is there an entry that disables it?"
   returns on the first hit, so a later, higher-precedence re-enable is ignored. If the underlying
   semantics are "the last value wins", the gate must resolve ORDER, not existence. Test mixed scopes
   in both orders.
2. **Identity by name.** A helper, plugin or binary accepted on basename/family alone, so an arbitrary
   executable at an unexpected path is treated as the known-safe one. Require the resolved path plus a
   digest, then try a copy, a symlink/hardlink, and the same basename at another path.
3. **Missing input read as proven absence.** A lookup that failed is recorded as "not set" and the
   assertion over the empty result passes. A failed READ and an absent VALUE are different facts.
4. **Vacuous pass.** An empty input set satisfies both sides of a comparison. Assert non-empty before
   comparing, and make "I could not find it" fail closed.
5. **A "single-use" claim that nothing consumes.** The primitive refuses a second CONCURRENT holder
   and looks correct, yet nothing marks the resource used and the consumer merely imports the wrapper.
   Test three directions separately -- sequential distinct holders, the same holder twice, and genuine
   concurrency -- and require a wiring proof that the spawning code acquires before it spawns.
   Passing the concurrency case proves nothing about reuse.
6. **A precondition satisfied by the marker, not the condition it names.** "Prior process is gone"
   accepted from a terminal log marker, an absent directory, or a directory without the marker. A
   marker proves a run ENDED, not that its process exited. Require the real check, make "cannot
   establish it" a refusal, and exercise the insufficient variants rather than only the positive
   control.
7. **Relaxed assertion.** A test that caught a real defect is edited (equality -> containment) so the
   suite goes green while the defect stays. Compare the test file's byte size and mtime against the run
   that reported the failure, and call the function under test directly with the failing input.
8. **A derivation skipped because it seemed redundant**, then cited as if performed. Look for a claim
   with no command and no digest behind it.
9. **An unenforced property described as enforced.** A sandbox, role or policy asserted in prose that
   the run's own header contradicts. Check every "enforced" claim against the mechanism that would
   enforce it; where the bound is evidence rather than mechanism, say exactly that.

## How to test so the result is usable

- Run the DIRECT call -- the pure function, or the CLI against a scratch fixture -- and say which you
  ran. An end-to-end journey can succeed for unrelated reasons.
- For every "must refuse" case, state the OTHER conditions the probe satisfied, so the refusal is
  attributable to the single condition under test.
- Report what the gate DOES bind to after a fix, not merely that the old input now refuses. A fix that
  narrows a claim without saying how far it now reaches is half the finding.
- Prefer a stub or a CLI seam over a model whenever a negative must be shown end to end.
- Check the production consumer, not just the library: a repair that makes a fail-closed gate refuse
  the configuration actually in use on the host is itself a defect.

## Reporting

Each finding needs the id, the severity, the reproduction as an executable call, what was observed,
and what the correct behaviour is. Local verification is not acceptance: keep `is_acceptance` false and
state the claim ceiling.
