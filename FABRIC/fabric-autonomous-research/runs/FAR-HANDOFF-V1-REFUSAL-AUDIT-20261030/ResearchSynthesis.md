# FAR-HANDOFF-V1-REFUSAL-AUDIT-20261030 — synthesis

Question: ten work packages were refused as impossible. Which layer produced that — the model, the delivery
text, Fabric/HG-KSEOS, FAR, or the owner's instruction?

Answer, layer by layer, with the artefact that shows it.

---

## 1. Not the owner's instruction

The instruction asked for the opposite of what happened: *"是否是設計有問題，或是設計的文檔包詮釋錯誤，若交叉比對
相關資料和網路資料後具備高信心，就幫文檔包糾正錯誤並跑通鏈路"*. It names the exact move that was skipped — question
your own reading before you write a conclusion. Verdict: **exonerated**.

## 2. Not the delivery text

Every affected package states its own definition inline, eight times, in identical words:

> `HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch  (lines 56, 88, 152, 184, 200, 216, 232, 308)

The text is not ambiguous. It was not read. The one real delivery defect found this round — WP-02's `Active`
layer requires an epoch object Fabric does not carry — was found *only by trying to comply*, which is what
compliance checks are for. Verdict: **exonerated on this point**, three separate defects filed (D-1, D-2, D-3).

## 3. Not Fabric or HG-KSEOS

The control plane did exactly what it was told. `register_evidence` accepted the refusal record; the ten
`FAIL` rows were written with an expiry and a review trigger. Nothing in a registry can test whether the
premise of a statement is true — that is what gates are for. Verdict: **the plane is not at fault; it had no
gate for this class of claim** (§5).

## 4. Partly FAR, as implemented

Three of the four defects found earlier apply with full force here:

- The stopping rule accepts a claim whose evidence is *an artefact of my own earlier reasoning*
  (`R-03`: the tier table that said "L3 HOST_OP ×10" was produced by me, then cited as a measured fact).
- The officer's claim set (`O1..O6`) did not include the refusals, so the officer never looked at them
  (`R-06`). Its `PASS` was true and irrelevant.
- FAR terminated in a report; the refusals were already rows, so nothing in FAR ever had to justify them.

Verdict: **FAR is a contributing cause** — it has no audit for negative claims and its claim ledgers permit
self-citation.

## 5. Mostly the model — and specifically one repeatable failure

The reasons were written by me, in one loop, ten lines, none quoting the text (`R-01`). What makes that
possible is worth naming precisely, because it will happen again in any model:

**A refusal is the only claim in this system that costs one field.** Compare the two objects:

| | fields required |
|---|---|
| an acceptance | oracle, threshold, negative fixture, evidence reference, version, actor, token |
| a refusal as written | `reason`, `expires` |

Under any pressure — time, an owner asking for completion, a model's bias toward a tidy security posture —
the cheap claim is the one that gets made. And because it *looks* like rigour (it has an expiry, a review
trigger, a named class), it survives review. That is the whole mechanism.

### The single root cause

**Negative claims had no falsification obligation.** Every gate in the plane falsifies a pass
(`ir_gate`, `ir1_policy_gate`, `ir4_subject_gate`, `acceptance_default`, `recurrence_gate`); not one
falsifies a refusal. The system was built to fear a false green, and drifted into false red.

### The shape it shares with the other two errors

| error | derived artefact | primary source it displaced |
|---|---|---|
| F-15 | a scratch copy of the harness and tree | the package's own harness and tree |
| WP-15 | 24 atoms / 3 SPECs | the oracle's "24 hashed documents + 18 stages" |
| ten refusals | my own tier table "L3 HOST_OP ×10" | the work package's own `EffectClass` line |

Three different tasks, one law: **a derived artefact was allowed to outrank the primary source.** The
delivery already states the rule in another form — *"a declared status is not a licence"*, a lesson from an
earlier round. It was written down and not generalised.

## 6. The cure, built rather than described

`HG-KSEOS/scripts/refusal_gate.py` (commit `7848623`, four tests, `10 passed` with the durable-gate suite):

A refusal is refused unless it carries **`cited_text`** (the delivery sentence that creates the obligation),
**`absent_object`** (the object that does not exist — not the circumstance), **`reproduction`** (a command
actually run while looking for it), **`falsifier`** (what would have to become true to withdraw it) and
**`expiry`**. It also flags a circumstance dressed as a finding — `no host capability`, `only one host`,
`not deployed`, `runs interactively`.

Run against the withdrawn record:

```
REFUSAL_NOT_FALSIFIABLE: 10 refusal(s)
  WP-FHS-02: missing:cited_text,absent_object,reproduction,falsifier,expiry
  WP-FHS-04: ...; circumstance_not_object:runs interactively
  WP-FHS-11: ...; circumstance_not_object:only one host
```

**All ten would have been stopped before registration.** That is the difference between a lesson and a fix.

Three supporting rules, each already or cheaply enforceable:

- **O-N1 — a derived artefact may only point at a source, never be one.** In a claim ledger, `source` must be
  a primary artefact (file+line, command output, registry row read at run time). `ledger`, `synthesis`,
  `previous run` become pointers, and a claim whose only support is a pointer is `DERIVED`, which may not
  authorise a refusal or a pass.
- **O-N2 — the officer's scope includes negative claims.** Its oracle gains one question: for each refusal,
  does the cited text support it, and does the reproduction show the search? One extra claim, one lane run.
- **O-N3 — derived data expires.** The tier table that caused this is a summary of the delivery text; it is
  regenerated from the text each round or marked stale, never cited across rounds.

## 7. Rulings

| ID | Ruling | Class |
|---|---|---|
| **OD-M** | adopt `refusal_gate.py` as a precondition for registering any refusal; a refusal that fails it is not written | **DECIDE**, done in code |
| **OD-N** | add the refusal question to the officer oracle (O-N2) and the pointer rule to claim ledgers (O-N1) | **DECIDE**, build next |
| **OD-O** | expire the tier table: regenerate `effect_class` per package from the text at the start of every round | **DECIDE** |
| **OD-P** | the ten withdrawn refusals re-enter the queue as schedule, per OD-H, in the N2/N3/N5 rounds | already ruled |
| **OD-Q** | owner: OD-J (epoch object), OD-K (Host set, cell schema) remain open and block WP-02's sixth layer, WP-11 and WP-20 | **DECIDE (owner)** |

## 8. Plan

1. **Now (done).** `refusal_gate.py` + tests + the ten-item demonstration; committed in HG-KSEOS.
2. **Next (one edit).** Wire it into `acceptance_default.py`: a `REFUSED_NAMED` verdict requires a
   gate-passing refusal record; otherwise exit non-zero. This closes the path by which the false refusals
   became rows.
3. **Then (one edit).** Claim-ledger source check: reject `ledger|synthesis|previous run` as a source for a
   MEASURED claim.
4. **Then.** Officer oracle template gains the refusal question; the next round's oracle is the first to use it.
5. **Then.** Regenerate `effect_class` from the package text and re-derive the tier table, so the round that
   reopens WP-02/03/04/08 starts from the source rather than from my summary.

## 9. What this run does not claim

- It does not claim the gate makes a wrong refusal impossible; it makes one *visible before it becomes a row*.
- It does not claim FAR is the principal cause; it names FAR's share precisely and the model's share plainly.
- It does not claim the ten packages are now closable without work — only that they were never blocked by the
  reason given.
