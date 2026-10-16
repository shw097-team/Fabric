# FAR-20261019 — single-action items for the owner

Everything in this file is **prepared, not executed**. Each row says what is needed, what has already been
measured and filled in for you, and precisely why an agent cannot complete it. Agent-executable work from
the same ruling was executed in this round and carries its own receipts; this file exists because the
remaining items are not engineering tasks.

Claim ceiling: `LOCAL`. Nothing here has been accepted, released or promoted.

## 1. Items where the only missing act is your signature — the evidence is already gathered

| # | Item | What is already prepared | The single act | Why it cannot be delegated |
|---|---|---|---|---|
| S1 | `R7-04-FRESH-G1` — fresh runtime certificate | Measured this round: **binary** `C:\Users\user\AppData\Local\OpenAI\Codex\bin\e78bad9887fa50cf\codex.exe`, version `0.163.0-alpha.10.2`, 341,312,816 bytes, sha256 `9ecb9df2ecafcc00542ef0966c6f1737a81397dc9531b0a4b178238e2bf4a46d`; **route epoch** revision 22; **arms served this round**: EXECUTE `opencode-go/deepseek-v4.1-flash` (pinned rank 1), VERIFY `openai-codex/gpt-6.1-sol` (pinned rank 2, arm B — arm A is the writer's own model by owner order SOD006-C3) | Sign one certificate binding those five values | It attests that *you* observed the effective runtime. An agent can measure; only the owner can attest |
| S2 | `CANONICAL-AO-RELEASE` | The round's adjudication, limitations and readback are on disk | Issue the external acceptance/release record | Self-issued acceptance is the failure mode the entire protocol exists to prevent |
| S3 | `A1-A3-AUTHORITY-BINDING` | The register records exactly which bytes are missing | Attach your original signed A1/A3 bytes to a detached package | The agent does not hold your signed originals |
| S4 | `KP-R04-POLARITY` | The twenty conflicting clauses and their counterexamples are located and recorded in the register | Sign the textual polarity reconciliation | Repairing MUST-NOT polarity **changes normative meaning**; the signature is the act, not the edit |
| S5 | `SOURCE6-AUTHORITY` | The active-vs-historical question is recorded with the unrecoverable-bytes qualification | Sign the disposition for source #6 | Only the source's owner can declare what is still normative |
| S6 | `K-08` / `K-09` | Both are scoped in the register with their evidence limits | Designate a read-capable independent verifier; choose a pre-dispatch commitment mechanism that is not mtime | Both are choices about *who checks* and *what counts as proof* — owner decisions by construction |
| S7 | `PROMOTION-RETAIN-DEFAULT` | The canonical-only and epoch-19 classes are enumerated | Record retain-by-default (no deletion) | Retention vs deletion of canonical-only material is an authority act |

## 2. Items needing your disposition on a *candidate* an agent produced

| # | Item | Candidate state | Your act |
|---|---|---|---|
| C1 | Guard predicate precision (`FAR018-GUARD-FALSE-POSITIVE`, P1) | A candidate patch plus a falsifying test is delivered in `writer/` by the EXECUTE lane; the guard itself is **untouched** | Review the diff and decide whether to install. Loosening a security control must not be self-approved |
| C2 | Checker engine mismatch (`CHECKER-ENGINE-MISMATCH`, P1) | Measured: the canonical registry (revision 22) declares VERIFY_SECURITY **arm A = `opencode-go/deepseek-v4.1-flash`** as default — the same model the EXECUTE writer holds — with `openai-codex/gpt-6.1-sol` as non-default arm B. Declarative surfaces disagree about the engine label | Decide the authoritative engine label and let the declarative surfaces be aligned **without** moving the serving arm |
| C3 | Stale canonical pin (`CANONICAL-CODEX-PIN`, P0) | **Executed this round** under your authorisation: the pin now resolves to the live binary; backup, one-line diff and readback are in `TIER_A_EXECUTION.json` | Nothing, unless you object to the repair — the backup is retained |

## 3. Items that need a second actor, not a signature

| # | Item | Measured reality | What would close it |
|---|---|---|---|
| X1 | `R7-03-ISOLATE` — a checker boundary the checker cannot lift | Only **one** interactive OS identity exists on this host, and the same identity can remove its own deny ACE. What was proven is an *ordinary* denial, not an immutable boundary | A second, distinct OS identity for the checker (local account or container), or accept the recorded limitation |
| X2 | `R7-02-CODE-PROMOTE` / `DOC05-EFFECT-ADMISSION` | Different repositories and different owners | The owning teams' acts; outside this control plane |
| X3 | `FAR018-SPINE-LINEAGE` (P1) | All five FAR-018 work orders carry VERIFIED results; the lifecycle sits at `EVOLUTION_REVIEW` and delivery is refused because the remaining states encode release authority | The lifecycle authority records an evidence-only terminal disposition without crossing unsigned release states |

## 4. Explicitly not claimed

No production promotion. No external acceptance. No convergence claimed beyond `TEMP_CLOSED_CHALLENGE`.
The 31 register rows belonging to other rounds' scope are re-scoped, not closed.
