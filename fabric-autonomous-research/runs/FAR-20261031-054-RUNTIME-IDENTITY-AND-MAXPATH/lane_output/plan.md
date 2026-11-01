我會先讀取這份 brief，確認它要求的工作與治理邊界。
這個 run 已有 `--lane PLAN` 的啟動紀錄，但尚未看到完成 receipt。我會把 brief 中的量測視為待核實證據，並區分「修正 CLI 入口」與「修復受管理環境」兩個問題。
NONCE-ECHO: FAR-PLAN-3428C405

**Recommend (b) as the durable repair: rebuild the lease-managed environment under a shorter, governed path. Treat (a) as a separate entry-point cleanup, conditional on preserving the runtime controls. Reject (c) as the permanent design.** This recommendation is provisional until a controlled reproduction establishes causality.

The brief reports two distinct defects: `hermes` resolves to a recovery forwarder with a different `HERMES_HOME`, and the failing environment contains exceptionally long dependency paths. Making one invocation work does not establish that both defects are repaired.

I independently read [config/hermes.json](C:/Projects/Agent_Workspace/HG-KSEOS/config/hermes.json). It records unresolved runtime-tree ambiguity and several interpreter, installation, and profile identities. That supports requiring explicit runtime binding. I could not inspect the recovery forwarder because access was denied; the path lengths, import failure, and nine-second successful turn remain **brief-supplied observations**, not measurements reproduced here.

| Candidate | What must be true | Decision |
|---|---|---|
| **(a) Retire the recovery forwarder; use the product CLI** | The product entry must support the required profile, isolation, dependency provenance, lease lifecycle, receipts, and rollback. Governed consumers must resolve to that same approved identity. | Appropriate entry cleanup once equivalence is demonstrated. Desktop inference alone does not establish suitability for governed execution. |
| **(b) Shorten the managed environment** | The failure must follow path length with interpreter, dependency payload, and launch conditions held constant. The environment manager must support creation and renewal at the shorter location. | Preferred durable repair because it addresses the suspected defect while retaining environment management. |
| **(c) Shadow OpenAI with a short-path vendor copy** | A complete, pinned SDK must load deterministically, without mixing package trees or introducing uncontrolled search paths. | Reject as the normal repair. It adds another dependency authority and can conceal the broken environment. Any emergency exception needs a bounded lifetime and independent verification. |

The reported 260-character boundary is a strong lead, **not yet a causal proof**. Windows path behavior depends on the API and process configuration. The desktop and managed environments may also differ in Python version, SDK version, package completeness, or import resolution.

EXECUTE should establish causality before changing routing:

1. **Capture runtime identity.** Record command resolution, launcher target, interpreter and version, effective `HERMES_HOME`, environment-manager identity, SDK version, import search order, and actual loaded package origins. Exclude credentials.
2. **Run a controlled path experiment.** Recreate the same pinned dependency payload using the same interpreter at short and long roots. In fresh processes, import the reported module and initialize the same client without sending a model request. Capture complete exceptions and module origins. Exercise the suspected boundary on both sides.
3. **Separate length from missing content.** Compare the installed payload with its admitted package artifact. Determine whether extraction omitted or damaged files, or whether existing files are inaccessible through the runtime’s import path.

**What EXECUTE should build**

Use separate, single-package WorkOrders:

- **Diagnostic reproduction:** produce the controlled experiment and raw evidence. If shortening alone does not resolve the failure, report the path hypothesis as unconfirmed and stop that repair.
- **Managed environment repair:** rebuild through the supported manager at an admitted short root. Avoid moving an existing virtual environment. Add a preflight that checks the complete resolved installation layout against the experimentally supported path budget and reserves documented headroom for generated files and upgrades.
- **Entry-point reconciliation:** bind governed consumers to an explicit interpreter, entry module, profile, and environment identity. Retire recovery routing from normal invocation only after the replacement passes qualification. Preserve recovery as an explicitly identified recovery capability.

Acceptance must include successful imports and client initialization, rejection of an over-budget environment for the intended reason, rejection of conflicting runtime identities, and successful environment recreation or renewal. A permitted model smoke test can then verify the bound profile and provider route; elapsed time alone is not acceptance evidence.

An independent checker must rederive the decisive results from raw artifacts, using a preregistered oracle. Canonical binding changes must use the Shared Spine transition path. Rollback must retain the prior binding and environment references; if the prior environment is already known broken, rollback should leave execution disabled rather than silently restore it as healthy.

**The recommendation is falsified if** the identical payload fails at a short path, the missing module is absent from the admitted SDK artifact, import shadowing explains the failure, or shortening requires abandoning required lifecycle controls. Conversely, if the supported product CLI demonstrably provides those controls and the lease environment is obsolete, **(a) becomes the preferred repair**, with managed-environment retirement included explicitly.

Planning only: no code or runtime configuration was changed. The run contains a PLAN dispatch-start log, but I did not observe a completed lane receipt or independent acceptance result.