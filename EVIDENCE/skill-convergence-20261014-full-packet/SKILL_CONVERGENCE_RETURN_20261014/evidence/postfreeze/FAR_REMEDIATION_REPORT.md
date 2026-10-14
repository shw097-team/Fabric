# FAR — remediation and reinforcement ruling for the SKILL-CONVERGENCE round

Method: Facts, then Assessment against the six criteria the order names (low friction, high feasibility,
high engineering necessity, low regression risk, no over-engineering, alignment with the core goal), then
Recommendation. Written as the PLAN/orchestrator artifact of this round, in Hermes.

Route disclosure, stated up front because it is an audit fact: this session's runtime metadata reports
`deepseek-v4.1-flash` via `opencode-go`, not the `GLM-5.3-Flash` the order assigns to PLAN. I did not modify
any global model default, and the assigned routes are the ones the lanes actually ran on: the EXECUTE lanes
ran `opencode-go/deepseek-v4.1-flash` and the VERIFY/SECURITY lanes ran `opencode-go/glm-5.3-flash`, each
proven by its own dispatch receipt (required arm equals served arm). The PLAN artifact is therefore authored
in this session and independently checked by the GLM lanes, so the separation of duties is preserved at the
lane and evidence level even though the PLAN authoring model differs from the order's assignment.

## 1. Facts (measured this round, reproducible from the named artifacts)

Entry size, the primary goal:

| Entry | baseline chars | candidate chars | change | share of the 100,000 hard cap |
|---|---|---|---|---|
| adversarial-verification-rounds | 99,999 | 21,759 | -78,240 (-78.2%) | 21.8% |
| hgk-governed-execution | 99,996 | 19,658 | -80,338 (-80.3%) | 19.7% |

Both entries had been at 99,996 and 99,999 of a 100,000 cap; both now sit near one fifth of it.

Losslessness, re-derived independently by the harness and by two separate GLM checker lanes:
AVR reconstructs from 10 mapped slices to 101,488 bytes sha256 `4be690a4feaee5ba…` equal to the baseline;
HGK reconstructs from 6 mapped slices to 105,116 bytes sha256 `174df0185026de09…` equal to the baseline;
drop, order-swap and single-byte mutations are all detected. The frozen subject is 374 files at digest
`9b68418bcbfd230d43d6525752a09d156b37b31fb214eacaf3b5c77b616936cb`.

Reference population, which is where the round did not deliver what its headline implies:

| Entry | reference files | vs the linter's 60-file sprawl warning | unreachable files | unreachable bytes |
|---|---|---|---|---|
| adversarial-verification-rounds | 25 -> 28 | 28, under the cap | 10 | 62,201 |
| hgk-governed-execution | 105 -> 108 | 108, **48 over the cap** | 37 | 230,407 |

"Unreachable" is measured, not asserted: the file's path appears in no other file of the skill, main
document included. The live linter's own calibration for that rule reads "a deliberately curated large
workflow skill sits near 50 topical files; the hoarding shape this catches was 443 one-per-session files",
and the rule fires as a warning (`references-sprawl`), not as a hard failure.

## 2. Assessment, item by item

| Candidate item | Necessity | Friction | Feasibility | Regression risk | Over-engineering risk | Aligned with core | Ruling |
|---|---|---|---|---|---|---|---|
| Entry extraction (already done) | met | - | verified twice | none | none | yes | **keep as accepted candidate basis** |
| Finish consolidating all remaining theme groups of both entries | low now | high | high | low | medium | partial | **defer**: the entries are at ~20% of the cap, so further consolidation buys no limit relief, only tidiness |
| Merge the 48-over-cap sprawl in HGK references | high | medium | high | low | low | yes, this *is* 治理收斂 | **do, bounded pilot** |
| Harness false signal: `stub_points_at_topic` reports false for every row on Windows | medium-high (it is a false-signal source inside the evidence chain) | very low | high | negligible | none | yes | **do** |
| Dispatcher drops partial stdout/stderr on timeout (reproduced; it destroyed the diagnostics of eleven failed lanes) | high | medium | high | medium if landed | low if kept candidate | yes, it is the mechanism that hid eleven failures | **do as a candidate patch, do not land** |
| Guarded apply has only ever run against fixtures | medium | medium | medium | low | medium | partial | **defer with reason**: real-write evidence belongs to the apply work order, not to this remediation, and it cannot be validated without writing to a target |
| Live rollback drill and canonical apply/promotion | - | high | - | high | - | out of authority | **refuse to self-grant**; promotion needs an authority that is not the agent |

## 3. Recommendation

R1. Freeze the extraction result as the accepted candidate basis. It is the one part of the core goal that is
    complete, byte-exactly verified, and independently checked.

R2. Remediate the measured sprawl breach in the HGK candidate, bounded: merge the fourteen smallest
    unreachable reference files (42,985 bytes total) into one new topic file, with headings that preserve each
    original file name so the names stay greppable, and with **no stubs**, precisely because measurement shows
    nothing references them. Expected count change: 108 -> 95. This does **not** reach the 60 cap; reaching it
    needs roughly 34 further merges and is declared as follow-up, not as done.

R3. Repair the harness false signal, then re-freeze the subject as generation 2 and have the checker lanes
    bind the new digest. A verification chain that reports a false negative on every row is worse than no
    check, because it teaches the next round to ignore the field.

R4. Reproduce and prepare the dispatcher timeout-capture fix as a **candidate patch with reproduction
    evidence**, not a landing. Editing the control plane's own lane mechanism is a canonical change: it needs
    its own admission, bounded authority and governed landing, and the agent must not self-promote it.

R5. Write down what is refused and why: canonical apply, promotion, and any claim that the whole goal is
    "converged". Two advisory verdicts over a frozen generation are not acceptance.

## 4. Execution plan for R2, R3, R4, then independent re-verification

E1 (EXECUTE lane, HGK work order, `deepseek-v4.1-flash`): implement R2 inside `candidates/hgk` only.
E2 (EXECUTE lane, APPLY work order, `deepseek-v4.1-flash`): implement R4 inside `candidates/apply` only.
E3 (parent, harness maintenance): implement R3, then re-freeze generation 2 and re-measure.
E4 (VERIFY lane and SECURITY lane, `glm-5.3-flash`, forced arm, read-only, guard-subject baseline+candidates):
    independently re-derive the generation-2 numbers and the two made edits.

Claim ceiling for all of it: candidate-only changes to a non-canonical tree, independently re-derived, with no
acceptance, no promotion, no canonical write, and no repair of the eleven timed-out lanes already on the record.
