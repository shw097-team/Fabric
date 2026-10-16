# Amendment 03 — the sub-agent batch: the second triage, the skill dispositions, and one disagreement

Adds to the pack after `AMENDMENT_02`. Nothing published earlier is rewritten. All three leaves ran
`opencode-go/deepseek-v4.1-flash` read-only; the raw transcripts are published beside this file.

## 1. A second, independent triage of the same 28 items (corroboration)

The order asked for every owner-decision and blocked item, and this round's own EXECUTE lane produced one table.
A leaf produced another from the same source, keyed instead on **who holds the primary unblocking authority**:

| bucket | count | meaning |
|---|--:|---|
| `preparable_now` | 2 | the closing candidate already exists; only an owner disposition on it remains |
| `needs_signature` | 15 | closure is a signature or normative disposition only the owner can make |
| `external_actor` | 11 | closure needs a party outside this control plane (another repo/team, a vendor, an external AO, a second OS identity, a peer checkout owner) |

Both triages agree that all 28 are "prepared, not executed" and that no item was signed. Two items are
actionable on the owner's desk now, and both touch this round directly:

- **`CHECKER-ENGINE-MISMATCH`** (P1, preparable_now). The canonical registry (revision 22) declares
  VERIFY_SECURITY arm A = `opencode-go/deepseek-v4.1-flash` as the *default*, with `openai-codex/gpt-6.1-sol` as
  a **non-default** arm B; the dispatch slots carry a Codex-CLI label. This is exactly the mechanism this round
  measured and then worked around: with arm B unpinned the pool's rank-1 serves it, and with the rank pinned the
  mandated GPT model serves. The owner chooses the authoritative label; the declarative files are untouched.
- **`CANONICAL-CODEX-PIN`** (P0, preparable_now). The pin refresh was executed under authorization in an earlier
  round; what remains is the owner's ratification or objection, with the backup retained.

## 2. SKILL / candidate landability — the question the order actually asked

| disposition | items |
|---|---|
| **landable now** | the atomic lane-rebind change-set (registry epoch 22, model assignment rev 22, dispatch slots rev 10, and the policy fixture moved **together** — moving the route row alone is the named failure); the staged `scripts/gcm-containment/*` repair set with its README; the source-repoint capability (`knowledge.py::repoint_source` + spine change + its test), which fills a documented gap because an INSERT-OR-IGNORE ingest can never re-point |
| **needs an owner signature** | merging the publication PRs (#6/#8/#10) and branch cleanup; R11 (build an admission-receipt producer or remove the ADMITTED branch from the guard); NF-05 (promote the dispatch pool out of `CANDIDATE`, or keep reading a candidate pool by explicit decision); the SoD-exemption trust boundary; F-IND-3; the stale binary pin in `config/hermes-codex-lane.json` |
| **not recommended** | committing the rollback clutter (`config/*.bak-*`, 30+ files, plus `*.tmp-*` across scripts/tests/src); root scratch artifacts with no evidence; bulk-landing unclassified `evidence/review/**` and `openspec/**` dumps; and, above all, treating the round's own packet as accepted without an independent checker verdict |

That last row is the same rule this round's own merges were held under, so the guidance and the behaviour agree.

## 3. One disagreement, recorded rather than smoothed

The leaf's merge-readiness read reports PR #16 as `changed_files 21 / additions 3749 / deletions 72` at head
`6362d70c`. This round's two later live reads say otherwise: `PR_FACTS2.json` binds PR #16's `head_sha` to the
branch tip (`09b11bd235…`, match true) and the self-check read live `deletions == 0` for both candidates — the
repaired, purely additive homepage diff. The leaf's numbers are the pre-repair state, consistent with its own
caveat that GitHub recomputes and caches these fields between calls. **The later reads govern**; the leaf's
`GO` verdict on the mechanics (mergeable, clean, behind_by 0, no CI, no branch protection) is not in dispute.

Its findings that do stand and matter: neither candidate is gated by anything automated — no workflows, no
branch protection, no reviews — so merge-readiness rests **entirely** on the owner's acceptance decision, which
is the same conclusion this round reached by a different route.

## 4. What changes in the pack's conclusions

Nothing is withdrawn. The owner's action list gains one named item (`CHECKER-ENGINE-MISMATCH`, which is the
declarative counterpart of this round's routing finding) and the skill/candidate question the order asked is now
answered with three dispositions instead of none.
