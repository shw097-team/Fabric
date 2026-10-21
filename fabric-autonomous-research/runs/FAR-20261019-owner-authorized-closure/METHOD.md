# FAR-20261019 method — reuse-first, then execute under owner authority

## Shape of the round

This round is a **closure round over a closure round**. It does not re-derive FAR-018's method; it
re-uses the round scaffolding that already passed this project's compiler and lane gates, and spends its
effort on the part that was NOT finished last time: deciding and then *executing* what is still open.

## Steps

1. **Recon, three sources, no shared context.**
   - `far019_recon.py` — mechanical local recon: main tip, open pull-request states and Live mergeability,
     the declared-vs-live lane binary, the guard asset inventory, the reference-file count.
   - two independent leaf lanes (delegated, fresh context) — W1 rebuilds the *current* open-item
     universe with locators and an explicit still-open check per item; W2 writes the owner-decision
     dossier and *measures* whether each item is achievable on this host rather than asserting it.
   - Deliberately no shared scratch between the two lanes: a dossier that inherits the register's
     framing can only agree with it.
2. **Reuse the compiler-clean scaffolding, regenerate from the previous round, never from this round's
   own output.** `far019_contract.py` substitutes the round identity and the authority sources into
   FAR-018's contract, then the CAPC gates run in order (lint → activation → acceptance → hash →
   compile → duplication). Loading one's own output as a base carries forward any key the schema has
   since rejected; regenerating from the previous round cannot.
3. **Admission is a separate act from execution** (invariant 10a). The project, its requirement, its
   TaskSpecs and its WorkOrders are created through the Shared Spine lifecycle; no durable mutation of
   this round rides anything else.
4. **Ruling.** One ranked action set. Every action carries friction, feasibility, necessity,
   over-engineering test, session/blueprint alignment, the authority it rests on, and its falsifier.
5. **Execute under the authority the ruling cites** — the sole owner's authorisation given in this
   session. Actions that assert a fact only the owner can attest, or that change normative meaning, are
   prepared as single-action items and named as such.
6. **Independent verification** on a different model axis, pinned to a rank that is not the writer's
   own model, with an explicit instruction that an un-runnable check must return UNVERIFIABLE rather
   than a soft agreement.
7. **Close out**: single evidence MD, per-blob remote readback, HGK lineage, self-check with injected
   mutations, and the self-evolution record.

## Known limits of this method

- The compiler's duplication gate compares this round's thin prompt against FAR-018's and reports a
  non-trivial ratio, because the round deliberately re-uses the previous round's scaffold. The ratio is
  disclosed in the receipts as a measured value; deliberate structural re-use is judged to outrank
  shingle similarity here, and the briefs handed to the execution lanes are newly written.
- The two lanes run with `gpt-6.1-sol`, the same model family as the VERIFY lane; they are *recon*, not
  acceptance. Acceptance comes only from the pinned checker, and even that is `LOCAL` claim ceiling.
