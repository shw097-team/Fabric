# FAR-018 — Method

## Shape

A decision study over an already-measured state. No new subject is created: the round's job is to
decide *what remains* and then execute it. The study therefore spends its budget on **adjudication and
verification**, not discovery.

## Inputs, frozen before the study

| Input | Locator |
|---|---|
| Product branch | `fix/s4r6-closeout-doc-identity-and-update-route-20261016` @ `127ec1c…` (tree `62eef9d8…`) |
| Evidence branch | `r6-closeout-evidence-20261016` @ `0b50d3e…` |
| Immutables | `main` @ `d3bd545…`; `v0.1.1-preview.4` → tag object `0618d73c…` → commit `cc6c193…`, 7 assets |
| Prior ruling | `FAR-20261016-017-s4r6-residual-closure/VERDICT.json` (ranked action set + owner gates) |
| Residual universe | `…/FAR-20261016-017…/RESIDUAL_UNIVERSE.tsv` (37 rows) |
| Governing documents | the thin-prompt and the external acceptance report in the Hermes attachments dir |
| Round plan | `r18/PLAN_CORE_GOAL_AND_SPEC.md`, `r18/TASK_CHECKLIST.md`, `r18/DETECTION_CHECKLIST.md` |

## Steps

1. **Freeze and inventory.** Record every subject by SHA and every governing-document requirement,
   before adjudicating any of them. (Done in the admission record and the input freeze.)
2. **Two independent read-only reconnaissance lanes, in parallel.**
   - Lane A audits **every requirement of the two governing documents against the artifacts**, row by
     row, with a status of `DONE` / `PARTIAL` / `NOT_DONE` / `NOT_APPLICABLE` / `OWNER_GATE` and a
     locator per row. It is forbidden to take a status from another document's self-claim.
   - Lane B collects the **repository facts** an outside engineer needs, each with the command or
     `path:line` that produced it. It is forbidden to invent a path or an output, and it may not write
     inside the repository.
   Both lanes are read-only by construction, so their findings cannot contaminate the subject.
3. **Adjudicate.** Rank candidate actions on the five axes the mandate names — friction, feasibility,
   engineering necessity, over-engineering, alignment with this round and with the upstream blueprint
   and acceptance report — and separate the execute set from the owner-gated set and the rejected set.
4. **Execute the execute set.** The substantive prose goes through the **bounded writer lane**
   (CODEX CLI, `deepseek-v4.1-flash`) against an explicit allowed-path list. Mechanical evidence
   generation that the writer need not do (status back-fill derived from this round's own record) is
   done by the orchestrator and **disclosed as such**, never presented as writer output.
5. **Verify independently.** A VERIFY lane pinned to a **different model axis** (`gpt-6.1-sol` at rank 2)
   re-runs the new document's commands and re-checks a sample of the back-filled rows against the named
   artifacts, and reports its own ceiling.
6. **Publish and read back.** Evidence branch only; LF normalisation applied to the packet directory
   alone; `SHA256SUMS` recomputed; a fresh clone must verify `N/N OK`; the product branch is left
   untouched and its hosted `verify` re-read.

## What this method deliberately does not do

- It does not re-open R17's finished work (the guard, the SSOT disclosure, the red-gate diagnosis, the
  amendment) — re-litigating a closed item is the failure mode the acceptance report names.
- It does not touch the HG-KSEOS control plane; the reason is recorded in the ruling, and the residue
  is carried as a ticket rather than silently dropped.
- It does not treat a green suite as acceptance. Every claim carries its own ceiling and its own
  reader.
