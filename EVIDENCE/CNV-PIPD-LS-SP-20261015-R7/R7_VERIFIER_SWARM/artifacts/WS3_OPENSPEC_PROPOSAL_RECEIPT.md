# WS3 OPENSPEC PROPOSAL RECEIPT — R7 tooling findings TF-01..TF-09

Change: `hgk-lane-brief-and-guard-hardening-20261015`
Absolute path: `C:\Projects\Agent_Workspace\HG-KSEOS\openspec\changes\hgk-lane-brief-and-guard-hardening-20261015\`
Created: 2026-10-15 23:59–2026-10-16 00:01 local (UTC+8). Claim ceiling: IDENTICAL to the findings
file — LOCAL observation / candidate proposal; not an acceptance, not an implementation.

## Files created (exact list, byte sizes measured on disk)

| File | Bytes |
|---|---|
| `.openspec.yaml` | 40 |
| `proposal.md` | 11,361 |
| `tasks.md` | 9,437 |
| `design.md` | 5,958 |
| `specs/lane-brief-and-guard-hardening/spec.md` | 7,148 |

Nothing else was written anywhere. No git command was executed; no file outside the change
directory was modified; no network host was contacted except the local `npx openspec` CLI resolution.

## Validation (raw CLI output)

Environment: openspec CLI 1.8.0 via `npx openspec` (CLI exists in the repo; nothing installed).

Command 1:
```
cd C:/Projects/Agent_Workspace/HG-KSEOS && npx openspec validate hgk-lane-brief-and-guard-hardening-20261015 --type change --strict
```
Raw output:
```
Change 'hgk-lane-brief-and-guard-hardening-20261015' is valid
EXIT:0
```

Command 2 (registration + task parse):
```
npx openspec list
```
Raw output (head):
```
Changes:
  hgk-lane-brief-and-guard-hardening-20261015            0/22 tasks    just now
  ...
```

Command 3 (delta parse):
```
npx openspec show hgk-lane-brief-and-guard-hardening-20261015 --json --deltas-only
```
Raw output (head): `deltaCount: 7`, all operations ADDED, each requirement with 2–4 parsed
`#### Scenario:` blocks (verified in the JSON before truncation).

Cross-check: `npx openspec validate --changes --strict` over the whole repo passes this change;
the two pre-existing failures (`hgk-plan-plane-rebind-20261015`,
`sod-independent-verify-enforcement`) are NOT touched by this work and failed before it (their
defect: no parseable delta — one has no specs/ dir with delta headers, the other names its spec file
`specs/authority.md` without a capability folder; both pre-date this session).

## Why the format matches the existing changes

- Read first: `HG-KSEOS/AGENTS.md`, `openspec/config.yaml` (`schema: spec-driven`), and three
  complete changes in full (`lane-model-chain-rebind-20261015`, `skill-mainfile-cap-remediation`,
  `lane-toolchain-identity-and-failure-classification`) plus the delta style of
  `lane-health-repair-20261011` (`## ADDED Requirements` + `### Requirement:` + `#### Scenario:` with
  `**WHEN**/**THEN**/**AND**` bullets) and the strict-declaration receipt shape
  (`lane-dispatch-honest-declarations`).
- `.openspec.yaml` mirrors the existing 2-line form exactly (`schema: spec-driven` /
  `created: 2026-10-15`) — identical bytes to `lane-model-chain-rebind-20261015/.openspec.yaml`.
- `proposal.md` uses the established `## Why / ## What Changes / ## Capabilities / ## Impact` +
  `Out of scope / Non-goals` sections; `design.md` follows the D1..Dn chosen/rejected pattern of
  `lane-toolchain-identity-and-failure-classification/design.md` including its Non-claims tail;
  `tasks.md` uses `##` groups with `- [ ]` items and inline `— evidence:` pointers (the
  lane-toolchain convention), extended with a per-task `[TF-nn|NOW|BLOCKED-owner]` applicability tag
  as the task required (each task names finding id, exact file/surface, acceptance evidence,
  applicability).
- The delta spec lands under `specs/<capability-folder>/spec.md` (the fix for the exact defect that
  makes two pre-existing changes fail strict validation), capability
  `lane-brief-and-guard-hardening`, 7 requirements, all scenarios WHEN/THEN-parsable.
- Task count 22 (tasks.md) is what `openspec list` parses; the proposal's NON-CLAIMS section states
  the proposal-is-not-acceptance rule explicitly, plus the inherited LOCAL claim ceiling.

## Findings coverage map

| Finding | Where | Applicability |
|---|---|---|
| TF-01 (prose false-positive guard) | proposal Surface A, tasks 1.1–1.2, spec «command context» req | NOW |
| TF-02 (taskspec collision + cwd HEAD) | proposal Surface B, tasks 4.1–4.4 | BLOCKED-owner (control plane) |
| TF-03 (non-VCS provenance) | proposal Surface C, task 6.1 (WriteSet+diff standing convention; git-init is the owner-gated alternative) | NOW |
| TF-04 (display redaction misleads edits) | proposal Surface D, task 7.1 (operating guidance only) | NOW |
| TF-05 (suite depends on absent git ref) | task 6.2–6.3 | NOW |
| TF-06 (nonce carrier) | task 3.1 additive attribution record NOW; task 3.2 root-cause BLOCKED-owner | split |
| TF-07 (driver writes into subject; brief fix) | tasks 2.4, 5.1, 5.2 | NOW |
| TF-08 (ignored byproducts void verdicts) | tasks 2.1–2.2, spec «guarded subject» req | NOW |
| TF-09 (end-state-only guard + driver defaults) | tasks 2.3, 5.1, spec «intra-turn sampling» + «output destination» reqs | NOW |

## Honest list of what was NOT done or could not be verified

- **Nothing implemented**: this session produced the proposal only. No guard, dispatcher, driver,
  admission path, or test was changed; every task is unexecuted (`0/22`).
- **The proposal's cited paths were verified read-only to existence level only**:
  `HG-KSEOS/scripts/hgk-lane-dispatch.py` and `runtime_role_binding_assert.py` exist;
  `probe_mutations.py` exists at
  `_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RUNNERS/probe_mutations.py` (read-only, plain reads
  only; the frozen tree was not modified). The PIPD product tree contains no `probe_mutations.py` —
  tasks 5.x target the RUNNERS copy/driver surface as the findings describe; the exact final resting
  place for a hardened driver copy is an implementation decision left to the executing round.
- **`R7_BLOCKERS_AND_TASKS.json` / `HGK_TYPED_ADMISSION_R6R7.json` (TF-02 inputs) were not read**;
  TF-02's evidence pointers are taken from the findings file verbatim. The tasks declare those
  records as the acceptance-evidence fixtures to use when the owner-gated work executes.
- **No acceptance check of any kind**: per NON-CLAIMS, an adopted proposal changes no runtime
  behaviour; the checker-lane verdicts that would close the findings do not exist yet, and none are
  claimed here.
- **Hermes-desktop rendering (TF-04) fix**: explicitly out of this repo's authority; recorded as
  operating guidance only.
- Two pre-existing strict-validation failures in other changes were observed and left untouched
  (out of scope; a write outside the new change directory was prohibited).
