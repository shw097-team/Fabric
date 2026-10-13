# Approved upgrade scope

## In scope for a planned upgrade (what an external engineer may plan against)
- the governance contract and its binding statement (which plane owns what);
- the four subjects' public contracts, schemas, manifests and document sets;
- the control-plane spine schema and typed lifecycle vocabulary;
- the desktop-effect plane's documented procedures, guards and skills;
- the publication contract of this mirror (manifest, projection rules, non-claims).

## Out of scope (must not be planned against, and is not published here)
- credential values, `API KEY/`, `.env`, auth stores — never published, never planned against;
- machine-local runtime state, quarantined artifacts, bytecode and shortcuts;
- frozen source roots that a subject has sealed;
- licence choice, bulk-binary disposition, and whether a local repo is linked to a remote.

## Who decides what
| decision | authority |
|---|---|
| publish scope of this mirror | repository owner, recorded in `MANIFEST.json` |
| subject baseline and re-certification | Human Policy Owner + fresh G1 |
| acceptance of any subject | Acceptance Officer through the HG-KSEOS gates; never this repo |
| licence, bulk binaries, remote linkage | repository owner |

## The capability test an upgrade plan must satisfy
An external engineer must be able to produce, **from this repository alone**: the upgrade scope, the
dependency and contract map, the validation plan, the rollback plan and the non-claim list —
without reading any private workspace path. The readiness set in this folder exists to make that test
passable; it is the closure criterion an earlier independent review found missing.
