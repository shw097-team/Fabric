# Auditing whether a governed order is actually COMPLETE

Trigger: the user asks "是否已經 100% 完成 <order>? / 是否已解決 <report A> & <report B> 提出的全部問題、
建議和要求?" — or any phrasing that asks for a completion verdict against a contract.

**The trap this file exists to prevent.** A verified blocker is not a completed order. After the
substantive findings were fixed and independently re-verified, it is natural to answer "yes" — but a
governed order *also* enumerates artifacts and procedures, and those are separate deliverables. Passing
verdicts on the findings says nothing about whether the order's own required outputs exist.

## Procedure

1. Load the ORDER text in full, plus every challenge report it cites. Do this even when the fixes are
   long done — the audit is against the order's letter, not against memory.
2. Enumerate every **named deliverable**: each gate's required artifacts, each section's "required"
   records, the final-report shape, and any explicitly listed hygiene item.
3. For each, establish three separate facts — never collapse them:
   - **exists** at the current exact subject (a path, not a claim in prose);
   - **internally coherent** (its declared fields agree with the real changed paths, the real tree, the
     real machine truth);
   - **recorded where the order says** (in-tree vs out-of-tree is a contract term, not a preference).
4. Distinguish a **satisfied requirement** from a **surfaced one**. A predicate can hold in machine truth
   while the evidence artifact never states it — that is a presentation gap in the deliverable, and a
   strict reviewer reads the artifact, not the database. Re-derive it into the artifact.
5. Answer in the user's three-state discipline — **implemented / locally + independently verified /
   externally accepted** — and give an explicit list of what is NOT done. Never let green verdicts
   self-promote to a completion claim.

## Deliverable classes a governed order tends to enumerate

Scan the order text for these; each has been a real gap:

| Class | Typical requirement |
|---|---|
| Reconciliation record | a named artifact recording task-time baseline readback, both reports' verdicts, the reconciliation rule, already-closed findings, the write-set, invalidated tests, deferred items, claim ceiling |
| TT/CR delta | blocking-open count, deferred register with owners, explicit "no hidden blocking edge" |
| Scan receipts | secret AND redaction AND path-traversal AND symlink scans — not just the first one you happen to implement |
| Typed lineage | TaskSpec/WorkOrder/ECP/ExecutionBinding/permit rows, read from the spine rather than asserted |
| Compiler receipt | not only stage exit codes: also changeset count, changeset kind, unresolved-orphan count, duplication flag |
| Machine-truth assertions | e.g. lifecycle `last_checkpoint_id` == the final checkpoint — verify by reading the spine, and surface it in the projection |
| Final report shape | a fixed number of named blocks, with a readback SHA-256 for EVERY receipt/manifest/dossier/readset named in them |
| Hygiene | e.g. host-side PR title/body refresh, listed as "do it during publication" |

## Recording gate predicates, not just exits

A validator that reports only `exit_code == 0` does not evidence a predicate like "exactly one
ChangeSet" or "no unresolved acceptance orphan". Emit the predicate fields explicitly in the receipt so
an external reviewer can check them without re-running the tool.

## Ordering reminder

Adding artifacts to the evidence set means re-running the dependent chain and re-publishing (see the
packaging-order lessons L11/L12 in `evidence-integrity-lessons.md`), then re-dispatching the independent
post-publication verifier with the newly added artifacts listed as explicit coherence checks — "exists"
is not "coherent".
