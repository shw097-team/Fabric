# SELF-RESEARCH / SELF-LEARNING / SELF-ITERATION / SELF-EVOLUTION

Round `FAR-REMEDIATION-AND-CLOSURE-20261016`, session `20261016_104922_d455e7`.
Governed by the Fabric contract: candidacy only, no self-acceptance, every claim carries its ceiling.

## 1. Self-research — what was found that was not being looked for

The round's mandate was to FAR the residuals. Four findings came out of MEASURING what had to change,
not out of auditing, and three of them were not on any previous ledger:

| # | Finding | How it surfaced | Ledger status before |
|---|---|---|---|
| R7a | `config/model-lane-assignment.json` declared VERIFY_SECURITY's default arm as `gpt-6.1-sol` in its lane chain and as `glm-5.3-flash` in three sibling prose fields — **and `check_drift` reported zero fatal findings in that state** | reading every PLAN/VERIFY declaration surface before editing, because one route row could not be changed safely without knowing what else named it | not on the ledger |
| R7b | the registry's `source_of_routes{revision, sha256}` pins the SITE's bytes and revision, and the registry `epoch` is coupled to the site `revision`; neither is drift-checked | the existing lane-guard test failed 4 ways after R1 — the gate that agreed with me was not the gate that covered me | not on the ledger |
| E11 | "5 E11 cases" is really **4 E11 guard cases plus 1 C2 case**, and the underlying first cause is an **uncaught `OSError` on relay/usage METADATA probes** at `scripts/hgk-lane-dispatch.py:862-873` and `:1134-1135` — the promised refusal receipt is replaced by a crash | an independent sub-agent investigation, scoped read-only | carried as "environment-limited", which was half true |
| F1-premise | `routes[].PLAN`'s `selection_authority` was an order whose stated premise (a 429 on the OpenAI OAuth arm) had already been measured false | reading the row's own provenance rather than its value | on the ledger as an outlier, not as a stale premise |

Method note: the highest-yield move of this round was to enumerate **every surface that names a lane's
default arm** before changing any of them. F1 was treated last round as one bad row; it is actually a member
of a class — surfaces that must move together and a gate that does not look at their mutual agreement.

## 2. Self-learning — what the round would tell the next one, and where it is written

These are recorded as skill content, not as prose in this directory, so they load when relevant:

1. **State the sandbox root and write cwd-RELATIVE paths in a bounded-writer brief.** The R5 wedge had a
   diagnosed orchestration cause: the brief named the output as `candidate/scripts/...` while the dispatch
   cwd WAS `candidate/`, so the writer spent 15 minutes probing directory names for a writable location.
   The signature is distinctive: continuous 2-7 byte writes into a sequence of NEW directory names, at
   15-60 s intervals, CPU held at 0 — the writer is not idle, it is searching.
2. **A declaration change must enumerate its coupled pins.** Editing `routes[]` or the site file requires
   re-pinning `source_of_routes{revision, sha256}` and moving the registry `epoch` with the site `revision`.
   `check_drift` is silent about this; the lane guard is not.
3. **Two pointer groups can contradict each other with drift at zero.** A per-pointer comparator cannot see
   it. Add a cross-field sweep before trusting a green drift gate.
4. **The gate that agrees with you is not the gate that covers you.** After R1, two gates said "done" while
   a third was red by four tests. Run the adjacent gate, not the one you already expect to pass.

## 3. Self-iteration — what the round changed in its own machinery, and why

| Iteration | Trigger | Change |
|---|---|---|
| Detector parser | its first version certified the defect as clean | `check_declaration_agreement.py` now selects the claimed default by POSITION, not by list order; the false-negative claim I made from the buggy run was withdrawn |
| Brief form | the R5 wedge's diagnosis | `BUILD_R5B_SPEC.md` states the sandbox root, marks paths cwd-relative, and forbids probing for writable locations |
| Apply-script ordering | attempt 1 needed a rollback | the R1/R3 script now backs up BEFORE writing, runs dry by default, and fails on a non-unique match instead of guessing |
| Spine ordering | R2 promoted before its WorkOrder existed | `remedy_spine_workorders.py` creates requirement → taskspec → workorder in the required order and reads the whole spine back |
| Regression isolation | an incomplete change and a 518-test whole tree made causality unclear | the round now runs the whole tree on BOTH config states and diffs the named failures — this is what turned "some unrelated failures" into a proof of "1 removed, 0 added" |

## 4. Self-evolution — what this round proposes to the stack (CANDIDATE ONLY, nothing applied)

Ordered by the round's own criteria — low friction, high necessity, no over-engineering:

1. **Cross-field declaration sweep in `lane_policy.check_drift`** (highest value per line of code). The rule
   is one comparison per single-lane prose field. It closes R7a permanently and is RED-first testable.
2. **Coupled-pin sweep** — site digest, site revision, registry epoch — in the same pass. It turns a
   half-applied declaration change from a guard failure at dispatch time into a gate failure at edit time.
3. **`--turn-shape edit_only` in the dispatcher** (the item this round tried and did not deliver). The
   measurement behind it is now stronger, not weaker: two rounds, four bounded-writer turns, two wedges,
   and the second wedge's cause is diagnosed rather than blamed on the arm.
4. **Hermetic lane-guard tests plus two typed metadata-refusal catches** in the dispatcher (from the E11
   investigation). The product defect is real: an unreadable credential-metadata path currently crashes
   instead of producing the refusal receipt the contract promises.
5. **Prose-revision sweep** for the remaining superseded narration (`sod_across_all_arms`, the retired
   deviation record). Documentation debt; last on purpose.

## Claim ceiling

Everything in sections 1-3 is evidenced by files on disk and by re-run commands recorded in this directory.
Section 4 is a PROPOSAL SET: none of it is product code in this round, none of it is accepted, and the
ordering reflects this round's judgment rather than a measured cost model. No external party has reviewed
any of it.
