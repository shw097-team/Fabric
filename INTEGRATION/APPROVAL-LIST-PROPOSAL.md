# Mirror publication approval list — PROPOSAL (not frozen)

`STATUS: PROPOSAL — awaiting owner freeze.` Until it is frozen, a refresh is performed as an explicit,
reviewed change-set like the one that produced the current publication. This document is the input the
owner needs in order to freeze the rules that a builder would then encode.

## Include (governance, contracts and planning evidence only)
- the four subjects' `AGENTS.md`, `README`/index documents, contracts, schemas, manifests;
- typed lifecycle definitions and requirement/workorder receipts;
- the `INTEGRATION/` readiness set and this proposal;
- `EVIDENCE/` records of assessments, hygiene and independent checks.

## Exclude
- credential values, `API KEY/`, `.env`, auth stores — never published;
- `worktrees/`, `.venv/`, raw evidence stores, generated files (`*.pyc`, `*.lnk`, `*.tmp`), OS metadata.

## Named exceptions (carried, not silently resolved)
- `DESKTOP/var-fda/**` — desktop-effect plane runtime state and documentation. Published as a **named, bounded
  exception**; it is documentation for planners, not an approved payload. Whether to narrow it further is
  an owner decision.

## Rules a builder must enforce
1. An approval list is authoritative: a path absent from it must never enter a commit.
2. Removals are explicit by path; a removal touching a non-generated path fails the change.
3. The manifest's declared set must equal the tree that was actually published.
4. No credential-shaped path may be committed, and any such attempt fails the run.
5. Every refresh publishes its own scope, its before/after counts and its open owner decisions.

## What freezing this proposal would unblock
The in-repo mirror builder (open item O-02). Until then, the builder is **not** authorised work.
