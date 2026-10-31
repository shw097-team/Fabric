# FAR-HANDOFF-V1-ALLPASS-GAP-20261030 — second-order synthesis

Subject: `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`
Predecessor: `FAR-HANDOFF-V1-RESIDUAL-20261030` (which produced the rulings this round executed)
Channels: R2-A control plane (sqlite) · R2-B repository (git, files, digests) · R2-C run records (dispatch receipts, officer verdicts)
Every number below is a command output in this run.

---

## 1. What is still not complete (GQ-1)

| # | Item | Measured | Grade |
|---|---|---|---|
| 1 | 22 work-package acceptances | **12 PASS · 10 FAIL(refused) · 0 NOT_RUN** | settled |
| 2 | receipt quality behind the 12 grants | **5 grade A · 7 grade B** | not uniform |
| 3 | F-15 first-work harness | repository copy **35/0**; shipped package **34/1** | repaired in one artefact, not both |
| 4 | OD-E closure declaration `{00,15}` | ruled, **no artefact exists** | unrecorded |
| 5 | native checker | **0/22** — no checker with its own principal exists | capability boundary |
| 6 | ten host-level packages | refused by name, expiry 2026-12-31 | not done, and not doable here |
| 7 | delivery on `main` | **yes**, `d3c2eec16c` | done |
| 8 | branches | `#5` open (185 files, base `candidate/r18`); `#1`,`#2` draft with **empty merge-base** | two blocked, one waiting |
| 9 | HG-KSEOS worktree | **9 dirty entries**, `scripts/` = 1 modified + 2 untracked | blocks any `scripts/` subject |
| 10 | the other 909 acceptances | `NOT_RUN` | outside this delivery's denominator |

**Grade A** means the artefact is backed by a clean producer receipt or by a recomputation that does not depend on the producer. **Grade B** means the artefact is correct only because an officer re-derived it from sources — the producing dispatch either timed out (`A`, `C`: exit 124, no receipt written) or was **served by a different model than the one requested** (`B`: asked `deepseek-v4.1-flash`, attempt reports `mimo-v2.6-flash`, `ok: true`).

Grade A: `00`, `06`, `14`, `18`, `19`. Grade B: `01`, `05`, `07`, `09`, `15`, `16`, `21`.

## 2. Why ALL PASS was not reached — and whether FAR is at fault (GQ-2)

Two separate answers, because conflating them is what produced the previous round's optimism.

### 2.1 ALL PASS is not reachable on this host, and that is not a research failure

Ten of the twenty-two packages require host capability that does not exist on this machine: a policy-consumption trace from a running consumer, an issuer principal separate from the agent, a scheduler-managed wake lease, a worker with a journal cursor, three independent officers, a second host, a fresh process tree, a runtime capability broker, occupant slots, an executable 192-cell matrix. A research run cannot manufacture a host. Writing PASS rows for those ten would reproduce exactly the defect the delivery was opened to remove: a green manifest over a ten-per-cent walk.

The reachable criterion is **every claim carries a lawful verdict**, and that is what was reached: 22/22, none `NOT_RUN`.

### 2.2 FAR is defective in one specific, reproducible way

The predecessor's claim `C-04` said *"WP-FHS-15 is promotable today"* and cited: three SPEC files, 24 functional atoms, 24 unique `req_id`s, 48 fixtures, `KnownAnswer.ask=false`. Every one of those numbers was true. And the claim was still wrong, because the acceptance row's own oracle reads:

> 24 base docs 真 hash Reader 與 18 Stage 三 SPEC 具來源

The oracle asks for **24 hashed documents** and an **18-stage plan**. The delivered SPECs carry three DAG nodes (`00`,`01`,`15`) and no 18-stage plan at all. The atoms were 24; the documents were 6 distinct sources. Counting the atoms looked like counting the oracle and was not.

**Defect F-A — the stopping rule measures measurability, not satisfaction.** `ResearchPlan.stopping_rule` reads "every question has a claim whose evidence is a command output". A claim can meet that rule while being bound to the wrong oracle. The rule needs one more clause: *a claim that asserts promotability must quote the acceptance oracle it claims to satisfy and show each clause discharged.*

**Defect F-B — FAR terminates in a handover, not in a row.** The predecessor ended with `ResearchHandoff.yaml` listing `OD-B..OD-E` as `decisions_required`. The control plane has no trace of them. The grants that exist were written afterwards, by hand, in a script. A decision that changes no row can be reported as done, and was.

**Defect F-C — the officer's claim set was written by the maker.** I wrote the oracle for the officer's pass. Claim `O5` asked it to check that each entry's cited source exists. It did that faithfully, and the wrong-oracle conclusion sailed through, because the question being asked was "are the citations real", not "does the artefact satisfy the oracle".

**Defect F-D — the lane receipt does not compare requested against served.** `wpB.json` carries `used_transport_model: opencode-go/deepseek-v4.1-flash`, `ok: true`, `usage_receipt_ok: true`, and `attempts[0].model: opencode-go/mimo-v2.6-flash`. Nothing in the dispatcher treats that difference as a fault. A lane binding is currently a request, not a guarantee.

### 2.3 Root cause, stated once

**The research pipeline ends in a document; the control plane ends in rows; nothing binds one to the other.** Every symptom above is that one structural gap wearing a different hat: a claim that satisfies the stopping rule but not the oracle, a decision that changes no row, an officer asked the wrong question, a receipt that records a request and calls it a binding.

That is why a round can be told to use FAR, use FAR, and still leave residuals — the residuals live in the layer FAR does not write to.

## 3. How each residual closes (GQ-3)

Six mechanisms cover everything still open. Each has an owner class and a row that changes.

| Mechanism | Items | Who | What changes |
|---|---|---|---|
| **R — record** | OD-E closure `{00,15}`; receipt grades A/B; the 10 refusal rows already written | agent | an artefact + a registry row |
| **M — repair and re-measure** | F-15 in the shipped package; `scripts/` three files; dispatcher requested≠served | agent | a file whose digest changes, plus a before/after |
| **C — obtain capability** | the 10 host-level packages; the native checker | **owner** | either a host binding exists, or the refusal stands |
| **P — re-publish from main** | `#1`, `#2` (orphan history) | branch owners | a new branch cut from `main` |
| **W — wait then merge** | `#5` (base `candidate/r18`, 185 files) | agent after `#6` | a merge commit |
| **S — supersede** | the three older `FAIL` rows | agent | a successor requirement naming what closed them |

Nothing in that table is blocked on research. Three of the six are blocked on **decisions**, not on knowledge — which is the point of §4.

## 4. Owner / issuer decisions (GQ-5)

| ID | Decision | Class | Recommendation |
|---|---|---|---|
| **OD-A** | delivery merged to `main` | already exercised (envelope `WIN-12cb9b954e99`) | closed |
| **OD-B** | promote the 12, refuse the 10 | `RECORD` | done, keep |
| **OD-C** | accept grade-B receipts (7 packages) or demand a re-run | **DECIDE** | accept, and fix the dispatcher so grade B cannot recur silently |
| **OD-D** | patch the shipped package for F-15, or leave the package read-only and ship the patched tool beside it | **DECIDE** | ship beside it; a delivery that mutates itself cannot be re-verified |
| **OD-E** | declare closure `{00,15}` | `RECORD` | do now — it has been "ruled" for a round without a row |
| **OD-F** | the ten host packages: build the host bindings, or make the refusal permanent | **DECIDE (owner, product)** | the only decision here that costs real money; everything else is bookkeeping |
| **OD-G** | change the delivery's success criterion from ALL PASS to 0 UNKNOWN | **DECIDE (owner)** | recommended — see §6 |

Only **OD-F** and **OD-G** are genuinely the owner's: one spends money, one changes what "done" means. OD-C, OD-D, OD-E are engineering choices that were previously mislabelled as signatures; that mislabelling is itself part of the backlog.

## 5. Promotion and merge rulings

| Candidate | State | Ruling |
|---|---|---|
| WP-FHS-00/01/05/06/07/09/14/15/16/18/19/21 | granted, 5 grade A + 7 grade B | **stay granted**; grade is recorded per claim |
| WP-FHS-02/03/04/08/10/11/12/13/17/20 | refused, expiry 2026-12-31 | **stay refused** unless OD-F says otherwise |
| B1 / SKELETON / HANDOFF archives | `-V2 PASS`, digests re-verified | no action |
| `#7` (this delivery) | merged `1e98abf7` | done |
| `#4` openspec-only | merged `91f47a50` | done |
| `#6` publish/r20 subset | merged `da1d033b` | done |
| `#5` R20 skeleton+spine r2-revision3 | open, 185 files, base `candidate/r18` | **merge after rebasing onto `main`**; it is the last of the six |
| `#1`, `#2` | draft, **empty merge-base with `main`** | **do not merge**; re-publish their 12 files from a branch cut off `main` |

## 6. A different frame (the part that is not in the delivery)

The delivery defines success as ALL PASS over 22 work packages. Measured against that, it can never succeed here, and a run that keeps trying is optimising the wrong number.

Flip it: **the unit is not the package, it is the claim, and the failure mode is not FAIL — it is UNKNOWN.**

- `PASS` says a claim was checked and held.
- `FAIL` says it was checked and did not hold.
- `UNKNOWN` says nobody looked.

Under that frame the delivery's real target is **0 UNKNOWN**, which this round reached for all 22 packages, and which is a stronger guarantee than a pass count: it means every claim carries a verdict, an evidence reference, and — where it is a refusal — an expiry and a review trigger. A delivery with 12 PASS and 10 dated refusals is *finished*. A delivery with 22 PASS and no host binding would be *lying*.

This is the one recommendation that changes the definition rather than the work, and it is why OD-G exists.

## 7. Execution plan

**P1 — close the bookkeeping (agent, ~10 min, no owner input).**
1. Write `deliveries/CLOSURE_DECLARATION.json`: closure `{00,15}`, with the typed-edge argument and the rejected alternative recorded.
2. Write `receipts/P20_RECEIPT_GRADES.json`: grade A/B per package, with the dispatch exit codes and the requested-vs-served models.
3. Commit, push, merge to `main`.

**P2 — make the two defects unable to recur (agent, ~1 h).**
4. `hgk-lane-dispatch`: refuse when `attempts[i].model != used_transport_model` (F-D). Ten lines plus a negative test.
5. `acceptance_default.py`: a claim that asserts promotability must carry `oracle_quote` and `clauses_discharged`; refuse the claim otherwise (F-A).
6. `recurrence_gate` ledger: add the four defect classes F-A..F-D with this run as occurrence 1 and the P2 tests as their regression tests (F-B is covered by the row-binding rule below).
7. A rule, written where decisions are made: **a decision is not made until a row changed.** The `*_ALLPASS_CLOSURE.json` receipts already carry the row counts; make that field mandatory.

**P3 — finish the branches (agent, ~30 min).**
8. Rebase `#5` onto `main`, verify its file set, merge; then close it.
9. Report `#1`/`#2` to their owners with the empty-merge-base evidence and the re-publish recipe.

**P4 — the owner's two decisions.**
10. OD-F: build the ten host bindings, or make the refusals permanent. If built, each becomes its own round with a host-capability demonstration, not a document.
11. OD-G: adopt 0 UNKNOWN as the delivery's success criterion.

**P5 — hygiene (agent, ~15 min).**
12. Dispose of the three `scripts/` leftovers in one commit (the projections rederive script is an abandoned predecessor of `lane_policy_reconcile.py` — compare, then delete).
13. Supersede `R7-FARCLO-2`, `R9-CTRLPKG`, `R10-HANDOVER` with successor requirements that name what closed them; keep the FAIL rows.

## 8. What this run does not claim

- It does not claim the ten host packages can be closed here.
- It does not claim the grade-B artefacts are as well-evidenced as the grade-A ones.
- It does not claim FAR is broadly broken; it names four specific defects and their tests.
- It does not claim the delivery is wrong to target ALL PASS — it argues the target should be 0 UNKNOWN, and leaves that to the owner.
