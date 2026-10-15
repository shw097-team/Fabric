# R6 EXTERNAL ACCEPTANCE HANDOFF

producer: Codex CLI bounded writer EXECUTE lane (opencode-go/deepseek-v4.1-flash)
produced_utc: 2026-10-15T08:17:41.061258+00:00
verdict: PENDING_CHECKER
claim_level: LOCAL

This document tells an independent Acceptance Officer (different model family,
`opencode-go/glm-5.3-flash`, and/or the canonical AO) exactly what to re-run and what
evidence each re-run must produce. The AO must not trust any verdict in this lane.

## 0. Ground rules for the AO

- Read and hash, in order: `OWNER_TRUST_LOCK.json`, `HG-KSEOS/AGENTS.md`, `Fabric/AGENTS.md`,
  the Owner-approved PKG, the commander PROMPT, `C0_C9_CONTRACT_R5.json`,
  `compiler_native_output_R5/thin-prompt.md`.
- The compiled thin prompt (`thin-prompt.md`, sha256 `2f246796c3b927170a90ed7dd3f4307e913579db2efb56b307cbc2377a1cb77f`)
  is the authoritative job order; file 7 wins over the writer brief where they disagree.
- Re-run every command yourself; produce your own raw stdout/stderr/exit and your own hashes.

## 1. Capability qualification (22 ACTIVE_REQUIRED)

For each capability, re-run the recorded probe(s) and confirm positive/negative behavior on the
same subject. Raw evidence lives under `R6_DELIVERY/RAW/`.

- native-prompt-compiler: `python <compiler>/scripts/prompt_contract_compiler.py lint|activation|acceptance|render|hash|duplication <contract>`
  - required: exit 0 and `PROMPT_COMPILE_PASS`; evidence `RAW/cap01_compiler_*.stdout.txt`.
- approved-document-verifier: `python pipd_pkg_v2_check.py --doc <pkg> --check` and `--materialize`
  - required either way: exit 30 `FAIL_CLOSED MISSING_EXTERNAL_OWNER_APPROVED_LOCK` or `SOURCE_PHYSICAL_MISSING`.
  - unblock: supply the external Owner-approved lock and the missing physical source bytes.
- HGK-typed-spine-and-lifecycle: run `RUNNERS/probe_spine_lifecycle.py positive|negative|acceptance` and `RUNNERS/probe_spine_fk.py`
  - required: illegal transition refused; acceptance idempotency; FK refusal.
- Hermes-canonical-runtime: re-run `hermes --version`; compare to `HG-KSEOS/config/hermes.json`.
  - expected finding: served v0.21.5 (2026.9.24) vs declared 0.20.0/v2026.8.3. Owner certification needed.
- Codex-EXECUTE-DeepSeek: resolve the declared lane binary and run `runtime_role_binding_assert.py`.
  - expected: declared binary `.../Codex/bin/2e5e00daee91c61d/codex.exe` is absent (`ERR_LANE_TOOLCHAIN_BINARY_MISSING`).
- Codex-VERIFY-GLM: run `HG-KSEOS/tools/check_acceptance_independent.py`; independently confirm denominator/failures.
- Hermes-Kanban: `hermes kanban boards list`.
- Hermes-Swarm: `hermes kanban swarm --help`.
- gstack-advisory: `RUNNERS/probe_gstack_rolemap.py positive|negative`.
- OpenSpec-brownfield: `openspec --version` (full path `C:/Users/user/AppData/Roaming/npm/openspec.cmd`).
- AVR-HGK-Skill-loader: run the skill pack self-run (`--all`).
- FAR-SQLite-FTS5: `RUNNERS/probe_fts5.py positive|negative|teardown`.
- bounded-FS-API-Desktop: re-run the PIPD unsafe-destination guard (`project-unsafe`).
- approval-gated-GitHub: `python PIPD/tools/github_publish.py`; expected `GITHUB_AUTH_BLOCKED` unless a PAT is supplied.
- pipd-route-intake / pipd-authority-source / pipd-profile-tailor / pipd-pi-compile / pipd-pd-bind /
  pipd-execution-contract / pipd-assurance-tqaep / pipd-package-project:
  `RUNNERS/probe_pipd_chain.py <case>`; required: positive exit 0 and negative refusal with the recorded reason.

## 2. Requirement trace (221 planning cases)

- Re-run the 64 RQ parents, 129 children and 28 legacy T cases with a real bound runner.
- Required evidence per case: command, cwd, UTC, exit code, raw stdout/stderr, producer, independent checker.
- Current state: 0/221 executed; all BLOCKED_NOT_RUN (source physical missing / admission not run).

## 3. Hostile mutations (18)

- Re-run `RUNNERS/probe_mutations.py <m01..m18>` for each constructible case.
- Required evidence: `RAW/mut_<id>.stdout.txt` with observed outcome and validator verdict.
- The AO must specifically confirm the three gaps: M04, M06, M16 were NOT detected (validator PASS).

## 4. AUD findings (24)

- For each AUD close predicate, obtain the independent checker receipt or external authority condition.
- Required evidence: a same-subject receipt proving the stated close predicate, not a file-presence check.

## 5. Gates G-A..G-H

- Bind each gate runner, run positive/negative/first-fail, capture raw receipts, and pair with an
  independent checker. All eight are currently NOT_RUN.

## 6. Checkpoint / rollback

- Re-run `RUNNERS/checkpoint_drill.py` and verify: mutation detected by re-hash, rollback to exact
  original sha `1052061aeaae04784fb45ba2f2a5f4916f359875f54d03401c1fe0bb669f949d`.

## 7. Publication receipt

- Confirm no repository publication and no network egress occurred from this lane.

## 8. Exact evidence each re-run must produce

- command, cwd, UTC start, exit code
- raw stdout file and raw stderr file (sha256 recorded)
- producer identity and independent checker identity (different family)
- source hashes used and candidate package sha
- invalidation rule, rollback pointer, and residue readback
