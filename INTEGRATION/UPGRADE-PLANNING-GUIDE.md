# Upgrade planning guide (external engineers)

Read `NON-CLAIMS.md` first: this repository is a projection for planning, not an authority to act.

## 1. Establish the scope you may plan against
Read `UPGRADE-SCOPE.md`. Anything listed out of scope must not appear in your plan.

## 2. Map your work onto the four subjects
Read `SOURCE-PROJECTION.md`, then `DEPENDENCY-AND-CONTRACT-MATRIX.md`. Each dependency edge names a
producer, a consumer, a contract artifact and the authority that may change it. If an edge you need
is missing, that is a gap to report, not a licence to invent one.

## 3. Reproduce the current state
Enumerate the tree (`git ls-tree -r --name-only HEAD`) and compare against `MANIFEST.json`. The
manifest states what is published, what is excluded, and the subject state it was taken at. A digest
you cannot recompute from this repository is not evidence.

## 4. Plan the change as a governed re-publication
The projection has no fast-forward relationship with any local tree. Plan a reviewed change-set:
additions and removals by explicit path, with the approval list, then commit on a branch and merge.

## 5. Define validation before you change anything
Use `VALIDATION-AND-ROLLBACK.md`. Every class of change has a positive test, a negative test and a
rollback; if you cannot state the negative test, the plan is not ready.

## 6. Record what you will not claim
Carry `NON-CLAIMS.md` into your own plan. Do not restate projection presence as acceptance,
release, production readiness or live effect.

## 7. Escalate every owner-class decision
Licence choice, bulk-binary disposition, remote linkage of a local tree, subject baseline
re-certification and acceptance are owner decisions. This repository records them as open; it never
resolves them for the owner.

Generated 2026-10-13T11:50:38.128148+00:00.
