# Parallel sub-agent batch — verified inputs for this round

Three sub-agents ran in parallel and independently of each other and of this round's own measurement. Their
results were used as verification input, and each was checked by this round before being relied on.

| task | role | duration | api calls | outcome |
|---|---|---|---|---|
| 1 | verify every remote branch against its pull request's merged flag | 100.72 s | 11 | 14 branches deletion candidates, 3 kept |
| 2 | build the machine-checkable fact set for the homepage | 200.88 s | 20 | 13 pull requests and the root surface, all read live |
| 3 | session closure, handover and owner-gated hygiene candidates | 166.17 s | 9 | closure part, handover pointer, candidate table |

Findings that changed this round's own ruling, rather than confirming it:

- The homepage is NOT as thin as the round's audit assumed. It already carries the governance-contract role
  table, the layout table and contributor ground rules; what is stale is its dated status section, and what is
  missing is the evidence-prefix map and the merged-pull-request index. The ruling was narrowed from "rewrite the
  front page" to "refresh the status line and add an appendix", which is the smaller and more honest change.
- The branch count to remove is 14, not the 11 that a prefix-only scan suggests: the two `docs/skill-*` branches
  and the three `pub/*` branches are merged too. Conversely, `evidence/skill-convergence-20261014-full-packet`
  has no pull request at all and must be kept, so "old" is not the test; "merged" is.
- PR #15's `merge_commit_sha` field is a test-merge preview, not a merge. Any report that reads that field as a
  merge would claim a merge that did not happen.
