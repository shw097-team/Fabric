# Binding the checker, and the two ways its signal lies

Two failure families on the checker side of a round: the checker is not actually independent, or its
findings are not actually true. Both are cheap to prevent and expensive to discover late.

## 1. Bind the checker to a different model ONLY by stripping the default route's environment

A sealed CLI lane usually defaults to an internal relay. To put the checker on another provider over
native OAuth:

- Strip the relay environment around the invocation (`env -u OPENAI_BASE_URL -u OPENAI_API_KEY ...`).
  With the relay base URL present, a `<vendor>/<model>` request is routed to the default provider and
  answers HTTP 400 — the lane never reaches the OAuth backend, and you will misread that as "the
  provider is unsupported".
- Point the CLI's home directory at the one holding that provider's auth, and pin model AND reasoning
  effort on the command line. Pinning the model alone can silently come back with a different effort.
- Take the binding from the run's OWN stdout header (`model:`, `provider:`, `sandbox:`, effort). A
  registry or config declaration is a claim; the run's header is evidence.
- Ignore a declared route status in either direction. A registry can carry `UNPROVEN` or a stale
  failure string from a sibling model while your route works, and vice versa. Probe, then believe.

### Guard the interactive-login fallback before probing

Read the auth file's `last_refresh` first. A stale access token refreshes silently, but a revoked
refresh token falls back to an INTERACTIVE login — which opens a browser window on the user's desktop.
So probe with stdin from a file (never a tty), a hard timeout, and a visible-window sample taken
immediately before and after. Record both samples; "0 new windows" is only meaningful as a comparison.

### If the mandate forces the checker onto the maker's model

Record the axis as NOT_SATISFIED in the verdict, state that isolation now rests on process
separation + fresh context + read-only discipline alone, and state explicitly that this verdict does
NOT supersede an earlier different-model verdict on the same subject. A same-model round may still be
worth running — it just cannot carry the independence claim.

Why the axis is worth insisting on: in one measured pair, a different-model checker falsified five
HIGH-severity defects in a deliverable the same-model round had accepted, including a false statement
in a writer's self-report and an over-claim in the orchestrator's own ledger. The axis is necessary
but not sufficient — process and context separation are the rest of it.

## 2. False RED: your hand-built input is not the producer's shape

When you test a classifier, checker or guard by calling it directly, you must use the shape its REAL
producer emits. A hand-built dict that is missing a key the code now requires can produce a whole
category of bogus failures.

Measured case: probing a credential-helper classifier with `{"origin": ...}` entries returned
"unclassifiable" for the real, installed program, which looked like an over-blocking defect. The code
expected a `scope` key (as the real config reader emits); with the real shape every realistic input
passed. The "defect" was entirely constructed by the probe.

Rules:

- Before reporting a defect, get one REAL sample: call the production entry point (the gate/CLI the
  pipeline actually uses) and read what it passes, or read the producer function. Compare shapes.
- Exercise the production entry point end to end as the no-over-block control. If the production gate
  still says continue, an alarm raised from a hand-built input is probably yours.
- Retract a false alarm explicitly and say it was your probe. An unretracted false defect is worse than
  a missed one: it sends the next round chasing a non-existent bug.

## 3. Never let an in-place edit destroy its own verifiability

A rule for whoever writes the deliverable, enforced from the verifier side:

- Every in-place edit of a pre-existing file must leave a timestamped preimage copy, and the lane
  report must quote that path and its digest. Without it, "revertible" is unprovable, and a bad edit
  is unrecoverable in practice.
- An untracked file has NO git-verifiable preimage. A git index blob is a usable preimage only if the
  file was staged before the edit; say which of the two you relied on.
- Put the preimage requirement in the lane brief, not in the post-mortem. A round whose headline change
  has no preimage tends to be the round that also has a defect in that same change.

## 4. Mirrored evidence documents are immutable — corrections go in a NEW file

When an evidence artifact is mirrored byte-identically into several review roots, editing the
original silently diverges the copies while every hash in the transcript still looks correct. Write
superseding information into a NEW addendum file that quotes the sentence it supersedes, and re-mirror.

Related, same reasoning: do not mutate a shared version-control index while another session may be
writing the same repository. Establish that no foreign writer is active (recent mtimes under other
work areas, other running workers) before any staging decision, and treat "an unnamed actor already
staged files" as a reason to record state rather than to stage more.
