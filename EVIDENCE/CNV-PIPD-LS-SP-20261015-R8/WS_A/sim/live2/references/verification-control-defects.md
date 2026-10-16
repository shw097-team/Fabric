# Verification-control defects that pass a maker's own eye

A control can be green, recorded, and still be evidence about the WRONG tree. These four defects were all
raised by an independent third party on a candidate whose maker had already run the same checks.

## 1. Measure the control against the PUBLISHED subject, not against your working tree

A single worktree often carries more than the published branch: split-branch work, in-flight edits, files
the publication deliberately excluded. A PASS measured there says nothing about the subject a reviewer
clones.

- Materialise the subject without touching the worktree:
  `git archive --format=tar <subject-tip> | tar -x -C <tmp>` and run the control inside `<tmp>`.
- If the change is SPLIT across branches (a product branch and a harness branch), expect strict in-tree
  controls to fail on citations of the other branch's files. Either relabel those citations as prose
  ("the lane shell in the harness branch's `stage-b` directory") or scope the control to the documents that
  only cite in-tree paths. Do NOT round the result to PASS.
- Search roots matter as much as the subject: documents mix round-relative and repo-root-relative locators,
  so a control invoked from the round directory needs both roots, or should be invoked from the clone root
  with round-relative input paths. Run the documented command VERBATIM once to confirm it does what the
  expectation says.

## 2. Hash the COMMITTED blob, not the file in front of you

With `* text=auto eol=lf` in `.gitattributes`, a hash taken from a CRLF working copy cannot be reproduced
from a clone. Record both, labelled:

```bash
git cat-file -p <tip>:<path> | sha256sum     # the reproducible value
```

A reviewer who recomputes from the clone will get the blob hash; if the receipt carries only the EOL form,
it reads as a mismatch and the content agreement is lost behind it.

## 3. A documented command must be copy-pasteable from the CWD it names

A block that `cd`s to the clone root and then uses round-relative paths is broken for every reader, even
though each individual command worked for the author. Define the path once and use it:
`R=.hgk/rounds/<round>` then `cd "$R"` for round-relative steps. Also check tool availability in the
reader's environment: an anonymous clone has no `node_modules`, so `npx --no-install <tool>` cannot resolve
- point at the recorded raw output instead of a command the reader cannot run.

## 4. Prove non-mutation with a NAMED diff, never with a count

`git status --porcelain | wc -l` before/after conflates the program's side effects with whatever else was
happening in that tree at the same time (concurrent writes by the orchestrator are the usual confounder).
Capture the entry lists and diff them:

```bash
git status --porcelain > before.txt;  <run>;  git status --porcelain > after.txt
comm -13 <(sort before.txt) <(sort after.txt)          # new not-ignored entries
comm -13 <(sort bi.txt) <(sort ai.txt)                 # with --ignored appended
```

Report the counts AND the entry names, and if the answer is "NONE" say the earlier non-zero count was not
reproducible and name what it actually was.

## 5. Close a finding against the ARTIFACT, never against a console excerpt

A verdict reaches you twice: as a file and as a truncated tail in a process-completion notice. The excerpt is
cut mid-list, so a claim whose evidence text lists five stale statements can arrive showing three, and a maker
who closes on the excerpt publishes two unfixed items as done. Re-read the claim's OWN evidence field (and the
report section it points at) before marking it closed, enumerate every item inside the claim, and give each one
a disposition. A numbered list inside a single claim is several findings sharing an ID.

## 6. Scope every quantifier to the set you actually measured

"The guard is red on ANY base", "violations reached ZERO", "all N files are excluded" are claims about the
cases you did not run. Measure two bases and the honest sentence is "red on both tested bases (other bases
untested)"; measure zero violations in one dimension and the sentence must name that dimension ("frozen-path
writes reach zero; allowlist violations remain 5"). The direction of the conclusion can stay correct while the
quantifier is false, and a reviewer who recomputes will find the quantifier first. Prefer the largest set you
measured, stated as such, over the smallest set that sounds like success.

Also check the SCOPE of a relative claim: "five tool files are outside the allowlist" was true against `main`
and false against the declared stacked base, where those files are simply not in the changed set. A relative
fact carries its reference point in the sentence or it is wrong half the time.

## 7. A count your own writing changes must be published as an invariant

Extends §4 to document counts: "N files mention X" grows every time the round documents the finding, so a
number measured at one subject stops holding at the next — and a checker measuring the CURRENT subject will
report your earlier number as a disagreement. Publish the invariant ("zero product-side hits; every hit is a
record authored inside this round"), name the subject when a number must appear, and retire the bare count.

## 8. A third-party verdict is a work item, not a trophy

Treat each finding as a repair task in the same round: fix, re-measure, publish the MEASURED result (a
failure is a valid published result when it is explained), and record in the receipt what the independent
check could NOT verify from its position. One correction round per finding class is normal; two rounds on
the same class means the control itself is mis-specified and should be re-specified, not re-run.
