# Amendment 02 — the spine closeout, a near-miss, and why the project is still open

Supersedes nothing; it adds to `ERRATA_2.md` and `SESSION_CLOSURE_2.md` without rewriting either.

## What was attempted

The round's admission created the project `CNV-OWNER-DECISION-LANDING` and reached
`WORKORDERS_ADMITTED`. A closeout script was written to record each of its workorders' results with
`writer = codex/opencode-go-deepseek-v4.1-flash` and `checker = codex-verify/openai-codex/gpt-6.1-sol` — a
genuinely different model on each side, which is the property the spine's rule asks for — and then to move the
project forward.

## The near-miss, stated plainly

The first version of that script filtered the `workorders` table by `project_id`. **That column does not exist.**
The filter silently matched nothing, the script selected all 587 workorders in the spine, and its loop would
have recorded a result for every one of them.

It did not run. The listing output was piped through `head`, and the closed pipe raised `BrokenPipeError`
partway through printing, before the loop; `SPINE_CLOSEOUT.json` was never written. A read of the database
afterwards confirms no damage: `CNV-OWNER-DECISION-LANDING` is still `WORKORDERS_ADMITTED`, the newest
`updated_at` in the table predates the attempt, and the state histogram is coherent.

Two things are worth keeping from this. The abort was an accident of output plumbing, not a safeguard, so the
same script without the pipe would have written. And the defect class — a filter that matches the wrong set and
a loop that then acts on it — is exactly what a sealed, printed write set is for; the second version seals the
set and refuses to write when it is empty, which is the version that ran.

## Why the project is still open

The second version resolved no workorders either: `taskspecs` has no `project_id` column, so the project →
requirement → taskspec → workorder chain needs the requirement link, which this round did not establish. It
therefore refused to write, recorded the refusal in `SPINE_CLOSEOUT.json`, and stopped.

Leaving the project at `WORKORDERS_ADMITTED` is also what this round's contract asks for. The claim ceiling is
candidate-only, the maker does not accept its own work, and the deliver transition is a maintainer step. The
gap is named rather than papered over: **no workorder result was recorded and no transition was made.**

## What a next round needs

One thing only: resolve the requirement that each taskspec belongs to, seal the write set from that, print it,
and record results against the two lane models. Nothing else in this round blocks it.

## Sealed write set as recorded

```json
{
 "project": "CNV-OWNER-DECISION-LANDING",
 "write_set_sealed": 0,
 "wrote": false,
 "reason": "sealed set empty or implausible; no write attempted"
}
```
