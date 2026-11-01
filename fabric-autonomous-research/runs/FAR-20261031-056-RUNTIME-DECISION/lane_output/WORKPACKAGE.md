NONCE-ECHO: FAR-EXECUTE-1DF97172

# Runtime decision: retire the recovery forwarder

## Decision

The governed control plane must adopt repair **(a): retire the recovery forwarder and make the product CLI the only supported entry point**.

The canonical launch identity should be the already observed product entry:

```text
<hermes-root>\hermes-agent\.hermes-runtime\python\cpython-3.11.17-windows-x86_64-none\python.exe -m hermes_cli.main
```

with `HERMES_HOME` resolved to the approved product profile. The `hermes` command exposed to agents should ultimately resolve to that entry, or an inspected wrapper that preserves the same interpreter, module, and explicit profile. It must not resolve to `D:\Hermes-Recovery\live22\bin\hermes` or to another wrapper that overwrites `HERMES_HOME`.

This is an entry-point decision, not a claim that the recovery environment has been repaired. Any use of the recovery runtime remains non-canonical until it is rebuilt with dependencies compatible with its interpreter.

## Evidence and application to each candidate

The deciding evidence is:

1. The recovery-forwarded command fails on every attempted agent turn with the exact `openai.types.responses.response_computer_tool_call_output_screenshot_param` initialization error.
2. The product interpreter command, with `HERMES_HOME` pointed at the profile, completes a model turn in about nine seconds.
3. Copying the same openai package bytes imports at module-path lengths 125 and 259 and fails with the production error at length 260. This establishes path length as a triggering condition.
4. The installed failing environment also contains ten extension modules built for a different CPython release, so it cannot be imported intact by the 3.11 runtime even at a short path.
5. Launcher inspection is part of executable identity: at least one `hermes.cmd` under the product `venv\Scripts` forwards to the recovery runtime and overwrites `HERMES_HOME`. Changing `PATH` alone would therefore be incomplete; every forwarding wrapper that reaches agents must be replaced, disabled, or quarantined as part of adoption.

Candidate comparison:

| Candidate | Evidence-based result | Decision |
|---|---|---|
| (a) Retire the recovery forwarder; use the product CLI | Directly removes the observed failing launch path. The product interpreter has a successful end-to-end model turn. Residual work is launcher replacement and migration of any unique recovery configuration. | **Adopt** |
| (b) Relocate or shorten the lease-managed environment | The boundary experiment supports shortening as a fix for the path-length trigger. It does not fix the recorded incompatible extension modules. Relocation alone would yield a shorter but still ABI-incomplete environment. A future rebuild with wheels compiled for the bound interpreter could be viable, but that is a broader repair than candidate (b) as stated. | **Reject as the adopting repair** |
| (c) Vendor a short-path openai package to shadow the broken one | The import result makes shadowing plausible for openai, but it leaves the rest of the environment ABI-incomplete and creates a second dependency authority through precedence-based shadowing. A successful openai import would not establish a coherent runtime. | **Reject** |

Candidate (a) wins because it is the only proposed repair supported by a successful complete model turn while avoiding dependence on the packaging path that produced the failure. Candidates (b) and (c) each address one symptom while leaving the interpreter/dependency mismatch unresolved.

## Required interpretation of the decision

Adoption of (a) means the product runtime is authoritative and the recovery runtime is excluded from normal dispatch. It does not mean the merely installed copy of openai should be copied into the product runtime, and it does not justify silently falling back to the recovery runtime when the product entry fails. A failure at the canonical entry must fail closed with a named launcher or runtime error.

If use of a lease-managed recovery environment is an independently required product capability, it must later pass a separate rebuild acceptance: a short, managed root; an interpreter-compatible lock or wheel set; full extension-module imports; the same agent-turn matrix; provenance and digests; and rollback. That future repair does not change the decision needed now: retire the forwarding path and use the product CLI.

## Concrete acceptance checks for (a)

The following checks distinguish adoption from a superficial `PATH` edit:

1. Resolve the public `hermes` command from the same shell and environment used by an agent, then inspect the resolved launcher contents. The launcher must contain no recovery-runtime or recovery-`HERMES_HOME` indirection.
2. Start a fresh process and record the final executable, Python version, `hermes_cli` module origin, and effective `HERMES_HOME`. Repeat a representative model turn through every supported launch surface.
3. Exercise the intended profile and required integrations, not only `--version` or a help command. A help response is not evidence that authentication, model initialization, or profile loading works.
4. Scan the product runtime for extension modules whose ABI filename or import result is incompatible with the bound interpreter. The product path must have a coherent dependency set, independent of the ten incompatible modules recorded for the failing environment.
5. Verify that no supported agent, service, alias, scheduled task, or desktop integration still invokes either the recovery launcher or a wrapper that forwards to it.
6. Record the replacement/quarantine operation, raw before/after launcher contents, final resolution results, hashes of the product runtime artifacts used for the test, and a rollback procedure that restores the prior launch state if adoption fails.
7. Require an independent checker to reproduce the final command identity and model turn from raw evidence. The maker's nine-second observation and a file-presence check are not final acceptance.

## Falsifiers

The choice of (a) must be withdrawn or amended if any of the following is observed:

- A fresh process launched directly through the documented product interpreter and intended profile fails to complete the representative agent turn, and the failure is in the product runtime rather than an unrelated provider outage.
- The product runtime itself imports incompatible extension modules, cannot load the approved profile, or otherwise cannot carry the required agent workload after forwarding is removed.
- A required workflow depends on recovery-only capabilities that cannot be reproduced through the product CLI and that workflow cannot reasonably be migrated or separately rebuilt.
- The recovery forwarder cannot be retired without violating the applicable lease ownership or rollback contract. In that case candidate (a) is operationally unavailable; candidate (b), in its full dependency-compatible rebuild form, must be selected and proved.
- Independent checking shows that the reported successful product turn used the recovery interpreter, a different profile, a stale process, or another path than the one proposed as canonical. The observation would no longer support an agent-turn success through (a).
- A comprehensive execution test shows the recovery environment can be rebuilt at a short path with interpreter-compatible extension modules and all required workloads, while the product CLI cannot provide those workloads. That would make the unqualified choice of (a) incomplete and favor the rebuilt environment under (b).
- A vendored openai package would not by itself falsify (a); it would still need a complete, tested interpretation for all ten incompatible extensions and a provenance model that removes shadowing ambiguity.

## Claim boundary

This document makes a repair-selection decision from the supplied runtime observations. It does not claim that launchers have already been retired, that the recovery environment is repaired, or that final governed acceptance has occurred. Independent reproduction in a fresh process remains required.
