# FAR-20261019 — ranked ruling over every still-open item

Round: `FAR-20261019-owner-authorized-closure` · project `FAR-019-OWNER-AUTH` (TS-AUTH-01..05)
Authority: the sole owner of Fabric & HG-KSEOS, in this session, authorising direct execution of this
round's ruling. Claim ceiling: `LOCAL` — locally re-derivable completion. External acceptance: NOT ISSUED.
`full_convergence_verdict` stays `TEMP_CLOSED_CHALLENGE`; `production_verdict` stays `FAIL_CLOSED`;
`canonical_AO_acceptance` stays `NOT_ISSUED`.

## What actually changed since FAR-20261016-018

Independent lane W1 re-checked all 118 items of the previous register against the filesystem: **6 are now
genuinely closed** (mutable-source metadata semantics, cross-index presence non-vacuity, the guard-root
first attempt, the premature task ticks, the pack-index self-hash, the guessed workorder-count probe) and
**10 are newly created by the previous round itself** — a round that closes items also manufactures them.
94 items remain open: 3 agent-executable now, 31 belonging to other rounds' scope, and 60 that need the
owner's signature because they assert a human-owned fact or release something.

## Tier A — execute now under the owner's authorisation (this round)

Ordered by necessity ÷ friction. Every one is reversible or accompanied by a backup.

| # | Action | Why necessary | Friction | Authority | Falsifier |
|---|---|---|---|---|---|
| A1 | Refresh the canonical Codex executable pin (`config/hermes-codex-lane.json`) to the measured live binary, with backup and hash readback | The declared path points at a **deleted** update directory; every governed lane dispatch fails closed on it (`ERR_LANE_TOOLCHAIN_BINARY_MISSING`). This is the P0 blocking the whole lane mechanism | one line + backup + readback | owner authorisation (the item's own text says "under owner authorization, refresh…") | after the edit, a lane preflight that resolves the binary fails, or any other config key changes |
| A2 | Close the previous round's own Kanban cards that carry evidence (8 cards left `running` after their outputs were produced) | A board that leaves finished gates `running` is a false trace; the round's own close-out is part of its evidence | CLI calls only | agent | a card is completed whose output artifact does not exist on disk |
| A3 | Publish a currentness erratum: the addendum prints `50/50` while the final readback receipt records `51/51` | Two numbers in the same pack disagree; the machine receipt is authoritative and the prose is stale | one additive file | agent | the erratum rewrites the historical receipt instead of adding to it |
| A4 | Merge the peer evidence chain PR #6 / #8 / #10 at their verified exact HEADs | Long-standing owner-deferred blocker; all three measured **`mergeable: true` / `mergeable_state: clean`** in the live repo, and their preflight passed in the previous round | merge only; no rebase, no force | owner authorisation (each item's own text: "under separate maintainer authorization, merge the verified exact HEAD") | a merge is attempted at a HEAD that moved since the frozen reference, or `main` is force-updated |
| A5 | Promote the previous round's evidence PR #13 out of draft | A draft pack is not sent to reviewers; the owner has now authorised executing the ruling, and this is the round's stated delivery path | one GraphQL call | owner authorisation | the promotion also merges or rewrites content |
| A6 | Repair the lane receipt so a retry cannot overwrite the original first-failure receipt (attempt-numbered receipts) | The previous round's retry destroyed the record of why the first dispatch was refused; a governance trail that a retry can erase is not a trail | bounded code change + test | agent | the change alters receipt *content* rather than its path, or an existing receipt is unreadable afterwards |
| A7 | Prove each repaired probe is non-vacuous: re-run the repaired harness against the original defect and require it to **fail** | Three of the previous round's repairs (live-source metadata, presence indicator, S8b success value) were vacuous for a round; a repair without a falsification run is a claim, not a proof | one script + injected mutations | agent | a repaired probe passes when its subject is deliberately corrupted |

## Tier B — prepared, owner signature required (not executed, and why)

These are **not** withheld out of caution; each needs a human act an agent cannot perform without
forging it, or changes normative meaning.

| # | Item | Why an agent must not execute it |
|---|---|---|
| B1 | `R7-04-FRESH-G1` — a fresh runtime certificate binding the effective binary hash, route and epoch | It is a signed attestation that the owner inspected the effective runtime. An agent can produce the measurement; attesting it is the owner's act |
| B2 | `CANONICAL-AO-RELEASE` — the canonical independent AO acceptance and release record | Self-issued acceptance is the one thing the whole protocol exists to prevent |
| B3 | `A1-A3-AUTHORITY-BINDING` — attach the owner-original A1/A3 bytes and signatures to a detached package | Requires the owner's original signed artifacts, which the agent does not hold |
| B4 | `KP-R04-POLARITY` — twenty clauses whose MUST-NOT polarity contradicts their text | Repairing polarity **changes normative meaning**; the policy owner's signed reconciliation is the act, not the edit |
| B5 | `R7-02-CODE-PROMOTE` / `DOC05-EFFECT-ADMISSION` / `SOURCE6-AUTHORITY` / `K-08` / `K-09` | Different repos and different owners; outside this control plane's authority and this session's goal |
| B6 | `R7-03-ISOLATE` — a checker boundary the checker cannot lift | Measured: only one interactive OS identity exists on this host, and the same identity can remove its own deny ACE. Reachable only with a second identity, which does not exist here |
| B7 | Guard predicate precision (a guard that refuses evidence merely *enumerating* reference filenames) | The guard is a security control; loosening it is a security-normative change. Prepared as a patch + a falsifying test, not installed |

## Tier C — explicitly out of this round

The 31 items belonging to other rounds' scope (R8 bounded proposal, historical OpenSpec retirement,
promotion-retain default, mandate rebinding, the remaining `other-round` rows). Re-opening them here would
be the over-engineering this ruling is required to avoid; they are re-scoped, not silently dropped.

## Non-goals (unchanged from the previous round)

Full 221-item convergence, production promotion, `.hgk/` migration, rewriting merged evidence, and
hand-slimming the two skills. The skill reference sprawl (109 files) is recorded as an advisory finding
with a plan, not executed: a 109-file rewrite is exactly the over-engineering the ruling must refuse.

## Defects this round found on its own

1. **`lifecycle.plan()` derives TaskSpec ids as `TS-{project_id last segment}-NN`.** Two projects whose ids
   end in the same token collide (`IntegrityError`, fail-closed, no corruption). This round's first two
   admission attempts died on it. Minimal repair: derive the id from the whole project id or a digest.
2. **A failed admission leaves the project and its frozen requirement behind permanently** — two orphans
   (`FAR-019-R7R11-RESIDUAL`, `FAR-019-OWNER-CLOSURE`) sit at `PLAN_READY` with no governed abandonment
   path. Recorded; not hand-deleted from the shared spine, because a direct DB write is itself ungoverned.
3. **The spine cannot tell two rounds apart by goal** — both projects carried an identical `goal_hash`,
   so the round identity lives only in `project_id`.

## Execution order

A1 → A2 → A3 → A6 → A7 (agent-executable, local, verifiable) → A4 → A5 (repository acts) → independent
VERIFY → publish + per-blob readback → HGK lineage + self-check + evolution.

**Amendment (owner order, mid-round):** the owner moved the PLAN & Orchestrator lane and the
VERIFY/SECURITY lane to `opencode-go/deepseek-v4.1-flash` because the GPT quota was about to run out.
The verbatim order and its consequences are in `OWNER_ORDER_MODEL_SWITCH.json`. The consequence that
matters: the writer and the checker now share one model, so **model-axis independence is absent and must
not be claimed** — this is declared conflict `SOD006-C3` (owner-ordered), which canonical revision 22
already anticipates as an accepted risk. The independence this round still has is process, lane and
evidence-path independence plus no-self-acceptance.

Every Tier A action that is executed is reported with its raw receipt; any that turns out to be
infeasible is reported as a blocker rather than rounded up.
