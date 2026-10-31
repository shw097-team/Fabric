# FAR-HANDOFF-V1-RESIDUAL-20261030 — research synthesis

Subject: `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`
Channels: R2-A filesystem · R2-B HG-KSEOS registry · R2-C GitHub API
Every number below is a command output in this run; nothing is carried from an earlier round's prose.

## 1. What is not actually PASS

| # | Item | Measured state | Why it is not PASS | Class of cure |
|---|---|---|---|---|
| 1 | 22 work-package acceptances `ACC-WP-FHS-00..21` | 22 rows, **all `NOT_RUN`** | the requirements exist (`R18-WP-FHS-00..21`) but no verdict was ever resolved for any of them | `EXECUTE` for 12, `REFUSED_NAMED` for 10 |
| 2 | first-work harness (F-15) | shipped **34/1**, repaired 35/0 | the shipped runner fails `EXISTING_5_AFFECTED_TESTS`; the repair only worked in one environment because `jsonschema` resolution is unisolated | `DECIDE` — pin the interpreter |
| 3 | "native" checker | **0/22**, nothing to run | `grep CheckerReceipt\|PublisherReceipt\|NativeChecker` over `src tools scripts config` returns nothing; the checkers are lanes, not natives | `RECORD` — relabel, stop claiming native |
| 4 | 22-WP closure declaration | declared `{00,01,15}`, typed edges give `{00,15}` | `01` is a *dependency* of `15`, not a closure member; the DAG file carries 0 top-level edges and 36 `depends_on` edges | `DECIDE+RECORD` |
| 5 | delivery not on `main` | PR #7 open, 119 files, `+61,519/−0`, mergeable clean | nothing merged; the control plane's `main` does not contain the delivery | `SIGN` (one operation) |
| 6 | five registry `FAIL` rows | `R7-FARCLO-2`, `R9-CTRLPKG`, `R10-HANDOVER`, `ACC-DURABILITY-SKELETON`, `ACC-DURABILITY-HANDOFF` | the first three are lineage rounds closed as FAIL; the last two were recorded before publication and now carry `-V2 PASS` | `RECORD` (supersede, keep history) |
| 7 | `scripts/` subject | 1 modified + 2 untracked files | `IR-4` refuses a round whose subject is uncommitted — observed twice (`exit 4`) | `DECIDE` — dispose of the three files |

The registry denominator is the real headline: **931 `NOT_RUN` against 8 `PASS`**. Item 1 is only the part of that which belongs to this delivery.

## 2. How each becomes PASS

**Item 1 — 12 of 22 are closable from a lane.** The DAG ranks them by effect class:

| tier | count | WPs | closable by a lane? |
|---|---|---|---|
| `L0` LOCAL_DRAFT_WRITE | 4 | 05, 07, 15, 16 | yes — artifacts are files |
| `L1` SOURCE_READ | 5 | 00, 01, 09, 19, 21 | yes — ledgers and manifests |
| `L2` REPO_WRITE | 2 | 06, 18 | yes — with a reversible diff |
| `L3` HOST_OP | 10 | 02, 03, 04, 08, 10, 11, 12, 13, 17, 20 | **no** — needs host capability that does not exist here |
| `L4` RELEASE | 1 | 14 | only after 06 |

The 10 `L3` packages are not a scheduling problem, they are a capability boundary: wake-lease binding, issuer/receiver binding, worker journal cursor, hot-swap parity. Writing PASS rows for them from a lane would be the same defect as a green manifest over a 10 % walk.

**Item 2** — pin the interpreter (`python 3.11.17`, the one that imports `jsonschema 4.26.0`) and add a preflight `import jsonschema` to the harness entry so a missing dependency fails loudly instead of degrading into `ValidationFail`. Then re-run as-shipped; only that run counts as 35/35.

**Item 3** — the honest sentence is "every acceptance in this delivery is a lane acceptance". A native claim needs ① a checker with its own principal and key ② a claim-schema recomputation service ③ a publisher/registry sink ④ a refusal path. None of the four exists. Relabel, and record the four-piece requirement as the precondition for ever claiming native.

**Item 4** — declare `{00,15}`. `01` produces `AuthorityConflictLedger` and is a dependency of `15`; it is not in the closure. Alternatively keep `{00,01,15}` and add the typed edge `00→01` and `01→15`; the first is cleaner because it does not invent structure to justify a number.

**Item 5** — merge (order in §4). The delivery becomes part of `main`, which is the only thing that makes the manifests citable by an external team.

**Item 6** — supersede, never rewrite. `R7-FARCLO-2`, `R9-CTRLPKG`, `R10-HANDOVER` get a successor requirement that names what closed them; the FAIL rows stay in the table.

**Item 7** — `scripts/lane_projections_rederive.py` is almost certainly an abandoned predecessor of `scripts/lane_policy_reconcile.py`. Compare, then delete or fold it in a single commit, together with the two other leftovers.

## 3. Promotion rulings (already-checked candidates)

| Candidate | Evidence in hand | Ruling |
|---|---|---|
| **WP-FHS-15** TPM corpus & SPEC 18-stage | 3 SPEC files, 24 functional atoms, 24 unique `req_id`, 48 POS/NEG fixtures, `KnownAnswer.ask=false`, `ExecutionHandoff` present | **promote to PASS** — the claims are machine-countable |
| WP-FHS-05 / 07 / 16 | draft artifacts exist in the package | promote **after** a count check identical to WP-15's; no new work |
| WP-FHS-00 / 01 / 09 / 19 / 21 | nothing produced yet | not promotions, they are work: five read-lane runs |
| WP-FHS-06 / 18 | need a reversible diff | work, and only counts once merged |
| WP-FHS-02,03,04,08,10..13,17,20,14 | host / release | **refused by name**, expiry 2026-12-31, reason: no host capability |
| B1 / SKELETON / HANDOFF archives | `ACC-DURABILITY-*-V2` PASS, digests re-downloaded | already promoted, no action |

## 4. Merge order (measured, not guessed)

`#7` (119 files, `+61,519/−0`) ∩ every other PR = **0 files**. `#5` sits on `candidate/r18` and shares **79** files with `#6`; `#2` is stacked on `#1` (1 shared file).

```
#7 → #4 → #6 → #1 → #2 → #5 (rebase onto the new main, then open)
```

`#7` first because it is additive-only and conflicts with nothing; `#4` next (openspec-only, 81 files); `#6` is the large one and must land before `#5` can rebase; `#1→#2` is a stacked pair and must land in that order.

## 5. Owner / issuer decisions — five, one of them a signature

| ID | Decision | Kind | Unblocks | Recommendation |
|---|---|---|---|---|
| OD-A | merge batch to protected `main` in the order above | **SIGN** | item 5; the delivery becomes citable | grant, one operation |
| OD-B | promote WP-15 (then 05/07/16 after count check) | `DECIDE+RECORD` | item 1 partially | grant |
| OD-C | named refusal for the 10 `L3` WPs + WP-14, expiry 2026-12-31 | `RECORD` | stops them reading as "pending work" | issue |
| OD-D | pin interpreter + harness preflight import | `DECIDE` | item 2, F-15 | pin, do not vendor |
| OD-E | closure declared `{00,15}` | `DECIDE+RECORD` | item 4 | declare `{00,15}` |

That is the whole authorisation surface. Everything else in this round is a lane run or a registry row — the failure mode to avoid is turning `OD-B..E` into signatures, which is how the previous rounds produced "待裁決" that nobody could ever close.

## 6. Execution plan

| Phase | Lane | Work | Acceptance |
|---|---|---|---|
| P1 | EXECUTE (deepseek) | five `L1` packages: SourceManifest, AuthorityConflictLedger, ProtectedCheckerRequest, SBOM, 96-cell coverage skeleton | one AO run over the five artifacts |
| P2 | EXECUTE | WP-15 promotion + count check on 05/07/16 | mechanical: counts must equal the declared numbers |
| P3 | EXECUTE | WP-06 minimal reversible diff, WP-18 bounded repair | diff must be revertible by `git revert` alone |
| P4 | VERIFY (gpt-6.1-sol) | three AO runs, oracle registered before each | `acceptance_default` must return GRANTED, not NOT_RUN |
| P5 | owner | OD-A merge batch | remote readback: `main` contains #7's tree |
| P6 | PLAN | relabel native→lane, refusals recorded, closure repaired | registry counts show 0 unexplained `NOT_RUN` for this delivery |

Cost estimate: ~3 AO runs (7–12 min each, 1 M tokens each), 12 acceptance writes, one merge batch. No new tooling is required — `acceptance_default.py`, `ir_gate.py`, `register_durable_deliveries.py` already exist and were exercised this week.

## 7. What this round refuses to do

- It will not write PASS for the 10 `L3` packages. The capability is absent, and a PASS row with no host effect reproduces exactly the defect this run was chartered to kill.
- It will not call any of the 22 acceptance objects "native".
- It will not add dependencies to the DAG so that a previously declared closure number becomes true.
- It will not merge on the owner's behalf: the merge batch is one signature and it is the owner's.

## 8. One-line answer

Twelve of the twenty-two work packages can be closed by lane work this week, one of them (WP-FHS-15) is already promotable on measured artifacts; ten are beyond the current host and must be refused by name rather than deferred; the delivery itself is one signature away from `main` because PR #7 conflicts with nothing.
