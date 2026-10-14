# Before recommending "apply this candidate", RUN the gates you name

A candidate can pass every pre-flight a planner thinks to run and still fail the corpus's own conformance
suite. Naming a gate in a plan is not running it.

## Rule

When a recommendation is "apply candidate X", execute **every** gate the plan names **against the candidate**
BEFORE issuing the recommendation. A gate written as a post-apply checkbox turns a cheap pre-flight check into
a live regression.

## Why gates the lanes never exercised are the ones that bite

Lanes verify the pair/route/path they were briefed on. A conformance suite asserts the **whole** declared
invariant set. In the W6 case the verification lanes only ever checked the *checker* pair
(`PLAN != VERIFY_SECURITY`) and passed; the suite also asserts the *executor* pair (`EXECUTE != PLAN`), which
the candidate broke by binding PLAN to the EXECUTE lane's model. Nothing in the lanes' evidence could reveal
it.

## Cheap procedure that catches it

1. Build a **mirror** tree (copy the config/source roots into scratch), write the candidate files over it
   there, and run the corpus suites from the mirror. The live tree is never touched.
2. Run, at minimum: the repo's own conformance suite for that area, the registry/publication drift checker,
   and the separation-of-duties checker over **every declared pair** (not just the one you have been working
   with).
3. Only if all of them are green does the recommendation say "apply".

## If it is already applied and a gate fails

Revert to the last conformant state when the tool supports it, then re-run the same gate on the restored tree
to prove the failure was introduced by the apply and not pre-existing. Disclose the apply+revert cycle
explicitly — a resting state that looks untouched does not tell the reader that a mutation happened and was
undone.

## Ordering lesson

An apply that is mechanically clean (dry-run OK, pre-image digests match, rollback tested) is not thereby
*safe to do now*. Separate mechanical readiness from conformance readiness; a candidate can be ready to write
and not ready to land.
