我會先讀取這份 brief，確認它要求的工作與適用規範。
Brief 將路徑長度故障與 Python ABI 不相容列為兩個待處理問題。我也找到了本輪的 PLAN dispatch 啟動紀錄，但尚未看到完成 receipt；因此目前不能宣稱 PLAN lane 已通過證據閘門。我會繼續查閱本機原始證據，並清楚標示決策依據與未驗證部分。
目前可讀到的兩個 `hermes.cmd`，包括位於產品 `venv\Scripts` 下的那個，都會轉送到 recovery runtime，並覆寫 `HERMES_HOME`。這表示驗證不能只看 PATH 指向哪個檔案，還要檢查 launcher 內容與最終啟動的 interpreter。尚未重跑 brief 所述的匯入邊界與模型回合測試。
NONCE-ECHO: FAR-PLAN-81FACD98

**Recommend (b): rebuild the lease-managed environment at a governed short root, using dependencies compatible with its bound interpreter.** This is a conditional recommendation. Shortening the existing environment alone does not address ABI incompatibility.

The dispatched planning agent inspected the existing [controlled reproduction](C:/Projects/Agent_Workspace/HG-KSEOS/ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-12/MAXPATH_CONTROLLED_REPRO.json) and [reproduction script](C:/Projects/Agent_Workspace/HG-KSEOS/scripts/wp12_maxpath_controlled_repro.py). The artifact records the same Python-source payload importing at target-path lengths 125 and 259, then failing at 260 on the named screenshot module. It also records an installed-environment import failure involving `pydantic_core._pydantic_core`.

Those are recorded observations, not experiments rerun this turn. Their limits are material:

- The short-path reproduction still obtains other dependencies from the product venv; it does not qualify a complete replacement environment.
- The digest covers `.py` files, not complete distributions.
- The ABI scanner reports ten matches, exposes eight names, and does not test their imports. Their complete inventory and runtime necessity remain unverified.
- The artifact’s maker-produced `PASS` is not independent acceptance.

Current read-only launcher inspection adds an important finding: the first PATH-resolved `hermes.cmd` sits under the product’s `venv\Scripts`, but its contents forward to recovery and overwrite `HERMES_HOME`. Executable identity must therefore include launcher contents and the final interpreter.

| Repair | Assessment |
|---|---|
| **(a) Product CLI only** | Potentially preferable if the product runtime already supplies every required lifecycle, isolation, profile, and evidence control. The reported nine-second turn establishes functional viability for that invocation, not those controls. |
| **(b) Short managed rebuild** | Preferred provisionally. It can address both path length and ABI compatibility while retaining an explicit provisioning and rollback owner. Recreate through the supported manager rather than copying the existing environment. |
| **(c) Shadow-vendored `openai`** | Reject as the permanent repair. It leaves native dependency incompatibilities unresolved and introduces package-precedence, provenance, and update obligations. |

For **(b)** to be adopted, the environment manager must support the short root, recreate compatible dependencies, preserve the intended profile, and maintain these properties after renewal and restart. If those conditions cannot be demonstrated, the decision remains `INCONCLUSIVE`.

EXECUTE should receive exactly one work package: **“Rebuild and qualify the bound lease-managed runtime at a short root.”** It should provision a candidate environment, enforce an explicit path budget, bind interpreter and package provenance, and prepare a reversible binding change. Retirement of recovery entry points is a separate authority change.

Preregister the following checks before implementation:

- **Positive:** fresh-process target import, offline client construction with stub transport, required native-extension imports, correct package origins, and successful environment recreation. Then test the same agent turn under the intended profile when provider access is authorized.
- **Negative:** wrong interpreter, foreign package origin, stale evidence, and ambiguous home must fail for the intended reason. Missing inputs must yield `INCONCLUSIVE`.
- **Boundary:** reproduce the observed 259/260 behavior and test immediately below, at, and above the selected path-budget threshold. Inspect semantic results; the reproduction catches exceptions, so exit zero alone is insufficient.
- **Lifecycle and rollback:** repeat qualification after restart and lease recreation; rehearse restoring exact prior bindings and launcher bytes. A restored known-broken environment must remain disabled.

An independent checker must rederive the decisive claims from frozen raw evidence. Canonical changes require the typed Shared Spine event, evidence, and rollback references.

The recommendation would be overturned if a compatible short rebuild still fails, lifecycle operations reintroduce either defect, or required profile state changes. **Candidate (a) becomes preferable if the product runtime demonstrably satisfies all required controls and the separate managed environment is obsolete.** Equivalent boundary counterexamples would invalidate a categorical 260-character explanation.

This remains **delegated candidate advice**: the lane gate returned `RECEIPT_MISSING`. No passing governed PLAN receipt, implemented repair, or acceptance is claimed.