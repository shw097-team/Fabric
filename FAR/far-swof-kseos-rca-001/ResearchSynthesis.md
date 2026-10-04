# FAR Research Synthesis — SWOF programme → HG-KSEOS acceptance-integrity proposal

run: `FAR-SWOF-KSEOS-RCA-001` v2 · route: HGK Step 10A Gate 1 (FAR research first)
corpus: `知識庫/實作相關DOC/SWOF` — 14 PROMPT, 16 external challenge reports, 160 evidence artifacts
lanes: A (W1 era) · B (W2 era) · C (evidence corpus) · D (root cause) · E (fresh-context challenge)

## 1. Decision-relevant answer

> The SWOF programme did not fail because its product code was bad. It failed because **the local
> acceptance oracle was the candidate's own artifact rather than the frozen canonical contract**, and
> because **evidence metadata was carried forward by identity rather than recomputed** — so rounds
> closed the counterexample in front of them and shipped next-round defects that the same contract
> already forbade.

Two families, both mechanically checkable, account for the overwhelming majority of the recurring
blockers.

## 2. What three independent lanes found (they did not see each other)

| Lane | Slice | Convergent result |
|---|---|---|
| A | 7 W1-era challenge reports | product passed every round; blockers were EVIDENCE-coherence + PROCESS-ordering; the same classes recur across 3+ rounds |
| B | 5 W2-era reports + 3 orders | checker IDENTITY separation held throughout; the gap is checker **ORACLE AUTHORITY**; 6 named blind spots incl. a correlated maker/test helper |
| C | 160 evidence artifacts | **round-identity drift** is the most machine-detectable class: frozen schema literal, frozen `order_id`, filename-vs-content round mismatch, carried byte-identical receipts |

Independent agreement across A/B/C — reached without a shared prompt — is what elevates these from
"one reviewer's opinion" to a research finding.

## 3. The two mechanisms in evidence

**Mechanism 1 — counterexample repair instead of contract proof.**
The loop accepts "a first-failing invariant" and never enumerates the invariant's declared domain, so
each repair closes one tuple and a sibling cell of the same frozen contract surfaces next round. The
HumanGate repair sequence is the clean illustration: a syntactic non-empty string → a shape-correct but
non-canonical token → a wrong basis byte recipe with unnormalised sets and an unconsumed
`required_authority` — four dimensions of ONE PI06 contract, removed across four rounds.

**Mechanism 2 — identity carried, not recomputed.**
`schema`, `order_id`, `repair_id`, nested `publication_state` and declared hashes were copied forward.
Because byte-hashes were correct, hash-checking passed while the *declaration* was false — e.g. an
empty-file SHA (`e3b0c442…`) used to describe non-empty artifacts, with **zero physically empty files**
in the corpus. A declaration defect is invisible to a hash-equality check by construction.

## 4. Corrections forced by the challenge lane (recorded, not hidden)

The fresh-context challenger returned `PASS_CHALLENGE_CONDITIONAL` and falsified real items:

| Item | v1 | Corrected in v2 |
|---|---|---|
| byte-identical W2R4 carried receipts | 5 | **8** (independently counted) |
| `order_id` frozen set | 4 files | **≥6** (incl. W2R1/R2 and W2R2/R2) |
| lane B "exact-commit lookup 404s" | asserted | **WITHDRAWN** — not verifiable in corpus |
| lane C counts 13 / 19 / 7 | stated as fact | **PROVISIONAL** — scan method not published |
| ROW3 cross-round predicate | blanket | **rescoped** — would have failed closed on by-design cumulative `W2R1` and the `historical/` immutable tree |
| ROW2 coverage | full cartesian | **rescoped** to the contract's declared minimum matrix |
| ROW1 provenance | touched-candidate-tree | **narrowed** to unattributable provenance (canonical constants whitelisted) |
| ROW5 empty-SHA branch | non-firing | **fixed** to key on descriptor path + recomputed bytes |
| W2R4 "defective" | flat | **qualified** — its newest Return Pack already dropped the postpublication token |

The ROW3 catch is the single most valuable output of the whole run: an over-broad predicate would have
been rejected as scope inflation and would also have **condemned legitimate immutable history**.

## 5. The proposal (8 controls, additive, no new subsystem)

`ProposedEvolution.yaml` v2. Chain stages and controls:

| Stage | Control | Blast radius | Prereq |
|---|---|---|---|
| ORACLE_CALIBRATION | C1 assertion must be attributable to a canonical locator | SMALL | U1 |
| FIRST_FAILING_INVARIANT | C2 declared-minimum-matrix coverage | SMALL | — |
| CROSS_ROUND_IDENTITY | C3 four-part identity predicate, historical/ exempt | SMALL | U4 |
| HANDOFF_READSET | C4 top-level == receipt subject (self-referential allowed) | SMALL | — |
| EVIDENCE_REGENERATION | C5 descriptor resolvability by path + bytes | SMALL | — |
| PUBLICATION_PREFLIGHT | C6 claim-token vs null-SHA + IndependentReceipt PASS | SMALL | — |
| ADMISSION | C7 materialized binding + event-order (not wall-clock) | MEDIUM | U2 |
| PD04_TASKSPEC_COMPILE | C8 obligation-closure + compiler identity | MEDIUM | U3 |

Four controls (C2, C4, C5, C6) are implementable immediately; the other four are gated on four
declared UNKNOWN inventories — this run **will not invent a field name** to make a predicate look
complete.

## 6. Non-claims

- lane C's 13 / 19 / 7 counts are **provisional** (scan method not published).
- lane B's 404 claim is **withdrawn**.
- The proposal does **not** claim product defects never occurred — product-conformance defects did
  occur; the narrower claim is that they were not the recurring *blocker* pattern in the W1 era.
- No claim that these controls would have produced an external PASS — only that they are deterministic
  predicates that would have caught **named** historical findings.
- **NO production, release, W3 dispatch, live-effect, or external-acceptance claim.**
- HG-KSEOS source mutation remains FORBIDDEN until separately proven and authorized.

## 7. Self-application

The author of this research is the same maker whose rounds produced several of the defects lane C
counted (`cp`-carried artifacts retaining an old `schema`/`repair_id`, filename-based classification,
and an out-of-order binding). The research and the maker's own failure record converge on the same two
mechanisms without sharing a prompt — which is why the proposal targets the *chain*, not the incident.
