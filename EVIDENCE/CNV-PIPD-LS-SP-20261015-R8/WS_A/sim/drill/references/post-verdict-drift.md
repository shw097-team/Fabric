# Post-verdict drift: deciding what a frozen verdict still covers

A verdict binds **the bytes at freeze time**. Whatever happens after it is written — a correction
folded in, a mirror refreshed, the harness itself edited, a foreign round writing a shared path — the
question is never "did anything change?" but "does the verdict still bind what it claimed?". Answer it
with a scoped, re-runnable predicate; never with prose assurance.

## 1. Define the substantive predicate first

List what the verdict actually adjudicated: the artifact under review, the registry/spec/config it
binds, the pages it published. Then:

> **predicate** = did any SUBSTANTIVE deliverable change after the verdict's mtime?

Everything else is allowed to drift: the review mirror, the round's own `var/` evidence, the harness.
Without this split every edit looks like it invalidated the verdict, and "re-verify everything"
becomes the reflex.

## 2. Ship a re-runnable check, not a frozen digest table

A digest table over a set you are still editing goes stale by construction: the second row you touch
invalidates the first (a checker will catch exactly that and falsify the table). Record the check:

```python
def post_verdict_delta():
    """Re-run any time. Durable fact = the predicate; the path list is a timestamped snapshot."""
    vt = os.stat(VERDICT).st_mtime
    substantive = [ARTIFACT, REGISTRY, PUBLISHED_PAGE]      # what the verdict adjudicated
    roots = substantive + [MIRROR_DIR, EVIDENCE_DIR]        # allowed to drift
    delta = [p for r in roots for p in files_under(r) if os.stat(p).st_mtime > vt + 1]
    sub = [p for p in delta if p in substantive]
    return {"changed_after_verdict": sorted(delta), "substantive_changed": sub,
            "predicate_holds": not sub}
```

The `+1` second tolerance absorbs filesystem timestamp granularity. Print JSON so the result is
citable, and keep the function in the round's harness so a third party can re-derive it later.

## 3. Re-verification scope follows the predicate

| drift after the verdict | correct action |
|---|---|
| no substantive deliverable changed | **no re-run** — the verdict still binds them; record the delta |
| only the verdict's own object changed | targeted **item** re-check of the changed items only |
| a substantive deliverable changed | re-verify that artifact; the old verdict's claim over it is void |

Never dispatch a full independent pass over bytes that did not change: it burns a lane, proves nothing
new, and buries the one item that actually needs checking.

## 4. When the foreign writer is another governed round

Before treating a changed path as drift, look for the owning round: a round directory with
`admission/` + `plan|execute|verify|closure/`, a pre-image backup under `evidence/stray/`, and its own
verdict artifact. If found:

- **record the supersession, do not re-verify** — the foreign bytes belong to that round and its verdict
  is the only verdict on them; re-running your own checker would verify a change against no brief,
  imply your authorisation of it, and create a second competing verification of a change that already
  has an owner;
- **the owning round's write-set tells you the blast radius** — if it names none of your other
  artifacts, the overlap is the single shared path;
- **do not touch its git staging** — unstaging or committing another round's in-flight work is a write
  outside your mandate and interferes with a live round; the index is not canonical state;
- standing control (no new rule needed): *the later writer records the supersession, the earlier round
  does not re-verify, the owning round's verdict remains the only verdict on those bytes*.

## 5. Pitfalls

- **Never re-key a digest or a receipt so it matches the new bytes.** That destroys the evidence that
  the bytes moved. Add a line saying what moved and who owns it.
- **Fixes made after the verdict are not covered by it.** State that ceiling in the same file
  (`post_verdict_*_ceiling`), or the next reader assumes the verdict blessed the current bytes.
- **A self-check is not an acceptance.** A targeted re-check run by the round that authored the work is
  evidence, not a verdict; acceptance still needs the independent lane — and say plainly when it was
  offered but not taken.
- **When a checker falsifies your claim, audit the METRIC before accepting the falsification.** A
  metric scoped too broadly manufactures false falsifiers (counting every file that mentions a generic
  name as a consumer of the specific file under test). Narrow it to object-specific references,
  re-measure, and disclose the metric correction in place rather than quietly swapping the number.
- **A negative control is part of the check.** A predicate that has never been shown to fire on a
  synthetic violation is not a test; run it against one positive and two negative fixtures and record
  the result.
