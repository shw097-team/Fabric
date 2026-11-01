# Work Package: Governed Hermes Runtime Repair Decision

## Scope gate

This is exactly one work package. The executor must complete only the Hermes Windows runtime repair decision described below. Do not broaden the package into a general runtime redesign, dependency upgrade, provider migration, or production/release action. This package contains all task context needed to start; repository exploration is unnecessary and must not delay execution.

## Objective

Determine and document which of three candidate repairs a governed control plane should adopt for the Hermes runtime failure on this Windows host:

- Candidate A: retire the recovery forwarder and make the desktop product CLI the only entry point.
- Candidate B: relocate or shorten the lease-managed environment so no module path reaches 260 characters.
- Candidate C: vendor a short-path `openai` package that shadows the broken package.

The output must be an evidence-based decision with explicit falsification conditions. It must distinguish a proven repair from a workaround and must not claim governed acceptance unless independent evidence verifies the complete runtime path.

## Observed evidence

The following facts are inputs to this package and must be treated as candidate evidence until reproduced during execution:

1. On the affected Windows host, `hermes` on PATH resolves to `D:\Hermes-Recovery\live22\bin\hermes`.
2. That entry is a recovery forwarder whose `hermes.cmd` sets `HERMES_HOME=D:\Hermes-Recovery\live22`.
3. An agent turn started through that forwarder fails with:

   `RuntimeError: Failed to initialize OpenAI client: No module named 'openai.types.responses.response_computer_tool_call_output_screenshot_param'`

4. The desktop product’s own entry, `<hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main`, with `HERMES_HOME` pointing at the profile directory, answers a model turn in about 9 seconds.
5. A controlled reproduction copied the same installed `openai` package (1,048 `.py` files and one package digest) to three roots:
   - at a 125-character module path, it imports;
   - at a 259-character module path, the same bytes import;
   - at a 260-character module path, the same bytes fail with exactly the production error.
6. The installed environment also contains 10 extension modules built for another CPython; those modules cannot be imported by the Python 3.11 runtime even at a short path.

Record exact commands, exit codes, elapsed times, sanitized paths where needed, and hashes for newly collected raw evidence. Do not treat file existence, a merely successful import at a shorter path, or an LLM opinion as proof that the named repair solves the full agent-turn failure.

## Required analysis

Evaluate all three candidates against the same criteria:

1. **Mechanism:** Does the candidate remove the actual failing condition rather than only its symptom? Explain how it interacts with the 260-character evidence.
2. **Primary behavior:** Does the candidate make the same failing agent-turn path succeed, including OpenAI client initialization and a model response?
3. **Entry-point integrity:** Which executable is resolved, which `HERMES_HOME` is effective, and does the product profile remain the intended profile?
4. **Lease lifecycle:** Does the candidate remain valid after lease renewal, relocation, rollback, re-provisioning, or environment recreation?
5. **Shadowing and supply chain:** Does the candidate rely on package shadowing or byte-identical vendoring? Identify precedence, provenance, update, rollback, and digest-control consequences.
6. **Native extension compatibility:** How does the candidate handle or isolate the 10 CPython-incompatible extension modules? A solution that masks them without proving they are unnecessary for the exercised path is incomplete.
7. **Governability:** Can the entry point, environment root, package provenance, configuration, and intended `HERMES_HOME` be declared, verified, audited, and rolled back through controlled artifacts?
8. **Operational simplicity and blast radius:** Compare maintenance cost, number of moving parts, failure modes, and reversibility.
9. **Security and trust boundary:** Do not let `PATH`, user config, cwd, or a spawned process silently redirect to a different environment or credential set. Fail closed on ambiguity.
10. **Sustainability:** Explain whether the repair survives normal upgrades and lease-managed provisioning without recurring manual repair.

## Decision rule

Adopt the candidate that provides the strongest root-cause repair under the evidence while preserving explicit environment identity and rollback. A successful short-path import alone proves only a path-length mechanism. A direct product-CLI success proves that entry can serve the tested turn, but does not by itself prove that all required entry points and lease transitions are governed.

The final decision must:

- state the chosen repair in one unambiguous sentence;
- map each observed fact to the conclusion it supports and the limits of that support;
- explain why each rejected candidate is insufficient, riskier, or less governable;
- name the file/config/version references that define the effective entry point and `HERMES_HOME`;
- define the rollback to the exact pre-change executable resolution and `HERMES_HOME`;
- separate `PASS`, `FAIL`, and `INCONCLUSIVE`, treating `INCONCLUSIVE` as unaccepted;
- state explicitly that production, release, or remote deployment is not authorized by this package.

## Falsification conditions

The decision must name observable conditions that would overturn or materially weaken it. At minimum address all of the following:

1. The selected repair fails to answer the same model turn that succeeds through the desktop product CLI.
2. The failure persists despite every relevant module path being at 259 characters or fewer, proving path length was not the sole cause.
3. The failure recurs at a path below 260 characters, or a longer path succeeds under equivalent conditions, invalidating a categorical 260-character rule.
4. The successful entry uses another `HERMES_HOME`, profile, credential context, model, or provider than the intended one.
5. The recovery forwarder’s environment is found to be the authoritative product profile and the proposed replacement loses required state.
6. Lease renewal, re-provisioning, rollback, or a clean restart changes the resolved executable or environment root and reintroduces the failure.
7. The short-path vendored `openai` package differs in bytes, exports, metadata, or provenance from the intended package, or package shadowing resolves an unintended copy.
8. The 10 incompatible native extensions are required for the exercised runtime path, or shadowing/relocation merely hides a second readiness failure.
9. The proposed repair requires manual, untracked edits to a lease-managed directory that the next lease can overwrite.
10. Independent verification produces a digest mismatch, a non-zero exit, a missing usage receipt, a vacuous pass caused by missing inputs, or any `INCONCLUSIVE` result.

## Required verification

Use deterministic, observed checks where possible. The final evidence pack must include:

- pre-change resolution of `hermes` and the effective `HERMES_HOME`;
- direct product-CLI import and model-turn probe with elapsed time and exit status;
- the controlled 259/260-character import boundary reproduced from input paths, with raw output and the package digest;
- a complete agent-turn probe through the selected entry, including model response evidence and the effective profile/environment identity;
- an inventory of the 10 incompatible extension modules and their import behavior, with an explanation of their role in the selected path;
- checks for package resolution provenance and precedence when Candidate C is evaluated;
- a negative probe where an unresolved or wrong environment identity fails closed;
- an absent-input probe returning `INCONCLUSIVE`, never `PASS`;
- a stale or foreign digest probe returning `FAIL`;
- rollback rehearsal evidence;
- an independent checker result derived from raw artifacts under a separate evidence path, not from the maker’s summary.

Do not run SQP1, Stage-3, production, live-trading, deployment, merge, push, or secret-access actions.

## Deliverables and completion criteria

Produce one evidence directory for this work package containing:

1. `DECISION.md` — the chosen repair, evidence-to-claim mapping, rejected alternatives, risks, rollback, and falsifiers.
2. `EVIDENCE_MANIFEST.yaml` — raw artifact paths, command lines, exit codes, timestamps, subject/candidate digests, classifications, and checker references.
3. Raw positive, negative, boundary, lease, and rollback evidence.
4. `INDEPENDENT_CHECKER_RESULT.yaml` — a `PASS`, `FAIL`, or `INCONCLUSIVE` verdict with checker identity, input digests, checks performed, and limitations.
5. Any minimal implementation/config change required by the selected repair, limited to this single package and with an exact rollback patch or command.

Completion requires implementation for the selected repair (where applicable), positive and negative evidence, the boundary check, rollback proof, and an independent checker verdict of `PASS`. A maker summary, unchanged file hash, or successful one-off command is insufficient. If any decisive input is absent or conflicting, report `INCONCLUSIVE` and leave governed acceptance unclaimed.