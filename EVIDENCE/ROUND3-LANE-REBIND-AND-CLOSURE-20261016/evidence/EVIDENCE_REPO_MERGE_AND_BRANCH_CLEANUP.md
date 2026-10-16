# EVIDENCE — Repository MERGE / BRANCH-CLEANUP / PUBLICATION surface audit
### Round: ROUND3-LANE-REBIND-AND-CLOSURE-20261016
### kind: read-only classification of every remote branch and pull request in shw097-team/Fabric
### generated_by: a read-only audit pass inside the Fabric clone at C:/Projects/Agent_Workspace/Fabric
### paired_json: EVIDENCE_REPO_MERGE_AND_BRANCH_CLEANUP.json (same directory)
---

## 0. Scope and non-claims

**What this IS:** a timestamped, command-anchored classification of the repository's merge,
branch-cleanup and publication surface as measured on 2026-10-16 (Asia/Taipei UTC+8).

**What this is NOT:** this is not a merge, not a branch deletion, not a push, not a PR
create/close/edit/comment, not a registry or governance mutation, and not an acceptance
verdict on any round's engineering deliverable. No branch was merged, deleted, pushed,
or created. No PR was created, mutated, closed, or commented on.

The carrying contract explicitly forbids the agent from performing merges, branch
deletions or PR mutations; this audit classifies the surface and prices the owner's
options. Option (c) — leave everything and publish this packet — is the only route an
autonomous agent is permitted to execute under the "no agent self-acceptance /
self-promotion" clause, and that is what has been done.

---

## 1. Measurement snapshot (exact commands)

Run in the local clone at C:/Projects/Agent_Workspace/Fabric (POSIX/MSYS bash):

```
cd "C:/Projects/Agent_Workspace/Fabric"
git rev-parse --abbrev-ref HEAD              # pub/far-remediation-and-closure-20261016
git rev-parse HEAD                           # 5ae6f37d305fa9da2da8e9a05b03ff65f02bd04f
git remote -v                                # origin = https://github.com/shw097-team/Fabric.git
git fetch origin --prune                     # prunes stale remote-tracking refs; no new branches appeared
git branch -r --sort=objectname --format='%(refname:short)|%(objectname)|%(committerdate:iso8601-strict)|%(subject)'
```

Remote branch inventory (excluding `HEAD`), tip SHA + last-commit timestamp:

```
main                                            b8ff810  2026-10-15T20:45:45+08:00
docs/skill-convergence-20261014                 3707448  2026-10-14T16:09:10+08:00
docs/skill-convergence-20261014-followup        4650444  2026-10-14T16:20:40+08:00
evidence/skill-convergence-20261014-full-packet df411fb  2026-10-14T16:19:28+08:00
evidence/cnv-pipd-ls-sp-20261015-r6             a10f7be  2026-10-15T20:39:38+08:00
evidence/cnv-pipd-ls-sp-20261015-r7             04a1e11  2026-10-16T01:00:08+08:00
evidence/cnv-pipd-ls-sp-20261015-r8             3af4148  2026-10-16T11:52:41+08:00
evidence/cnv-pipd-ls-sp-20261015-r9             5cd47ce  2026-10-16T13:00:11+08:00
pub/lane-reliability-closure-20261016           0cb59d9  2026-10-16T12:05:24+08:00
pub/far-remediation-and-closure-20261016        5ae6f37  2026-10-16T13:27:27+08:00
```

Cross-checked independently against the remote, credential-free:

```
git ls-remote https://github.com/shw097-team/Fabric.git
```
```
b8ff810... main (HEAD)
3707448... refs/heads/docs/skill-convergence-20261014
4650444... refs/heads/docs/skill-convergence-20261014-followup
a10f7be... refs/heads/evidence/cnv-pipd-ls-sp-20261015-r6
04a1e11... refs/heads/evidence/cnv-pipd-ls-sp-20261015-r7
3af4148... refs/heads/evidence/cnv-pipd-ls-sp-20261015-r8
5cd47ce... refs/heads/evidence/cnv-pipd-ls-sp-20261015-r9
df411fb... refs/heads/evidence/skill-convergence-20261014-full-packet
5ae6f37... refs/heads/pub/far-remediation-and-closure-20261016
0cb59d9... refs/heads/pub/lane-reliability-closure-20261016
3707448... refs/pull/1/head
4650444... refs/pull/2/head
a10f7be... refs/pull/3/head
04a1e11... refs/pull/4/head
3af4148... refs/pull/5/head
0cb59d9... refs/pull/6/head
5cd47ce... refs/pull/7/head
5ae6f37... refs/pull/8/head
```

 git ls-remote confirms every locally-tracked branch tip matches the remote, byte-for-byte.

---

## 2. Branch classification (exactly one class per branch)

### 2.1 LONG_LIVED_DO_NOT_TOUCH

| Branch | Why this class |
|---|---|
| `main` | The default branch — tip `b8ff810`, equal to `origin/HEAD`. Never touched by this audit. |
| `evidence/skill-convergence-20261014-full-packet` | Deliberate long-lived evidence branch. NOT merged, has NO open PR; `ahead=3 behind=14` vs main; its 641-file diff touches only `EVIDENCE/skill-convergence-20261014-full-packet/`. Several main-tree documents *explicitly designate this branch as the standing evidence home* and document a standalone clone workflow targeting this branch name. Treating it as deletable would break documented provenance. Read-back check: `mkdir /tmp/fp_ro && cd /tmp/fp_ro && git init -q . && git remote add origin https://github.com/shw097-team/Fabric.git && git fetch -q --depth 1 origin evidence/skill-convergence-20261014-full-packet && git config core.longpaths true && git checkout -qf FETCH_HEAD`; on the Windows host this needed `core.longpaths true` due to >260-char paths inside the packet; `git ls-files | wc -l` → **2548 files**. The byte-identical packet is retrievable with a documented command. |

Documentation anchors on `origin/main` pointing at the full-packet branch:

```
git grep -n "full-packet" origin/main -- '*.md' '*.json'
EVIDENCE/SKILL-CONVERGENCE-20261014/README.md:41: manifest,結案集…在 **本 repo 的分支** `evidence/skill-convergence-20261014-full-packet` 之
EVIDENCE/SKILL-CONVERGENCE-20261014/README.md:42: can be clone-ed and re-run
EVIDENCE/SKILL-CONVERGENCE-20261014/README.md:54: git clone --depth 1 --branch evidence/skill-convergence-20261014-full-packet …
EVIDENCE/SKILL-CONVERGENCE-20261014/PUBLICATION-RECORD.md:24: `evidence/skill-convergence-20261014-full-packet`（tip `df411fbd…"，641 檔在樹
EVIDENCE/SKILL-CONVERGENCE-20261014/PUBLICATION-RECORD.md:41: … the packet was republished byte-identically to this repository's branch …
FABRIC/README.md:51: 完整回傳包（638 檔）在本 repo 的分支 `evidence/skill-convergence-20261014-full-packet` …
INTEGRATION/KNOWN-FINDINGS.md K-20: the packet was republished byte-identically … the deleted tip is recoverable from this branch
```

### 2.2 MERGED_AND_DELETABLE

| Branch | Merged by | Tip ancestry vs main | ahead/behind |
|---|---|---|---|
| `docs/skill-convergence-20261014` | PR #1 (closed, `merged_at=2026-10-14T08:10:09Z`, `merge_commit_sha=f14724d`) | `git merge-base --is-ancestor origin/docs/skill-convergence-20261014 origin/main` → 0 | ahead=0 behind=15 |
| `docs/skill-convergence-20261014-followup` | PR #2 (closed, `merged_at=2026-10-14T08:21:06Z`, `merge_commit_sha=266f8d6`) | same ancestry test → 0 | ahead=0 behind=13 |
| `evidence/cnv-pipd-ls-sp-20261015-r6` | PR #3 (closed, `merged_at=2026-10-15T12:45:46Z`, `merge_commit_sha=b8ff810` — **that IS the current origin/main commit**) | same ancestry test → 0 | ahead=0 behind=1 |

These three are pure residue; each tip is reachable through its own merge commit forever.

### 2.3 OPEN_PR_AWAITING_OWNER

| Branch | Head of open PR | Draft? | Ahead/behind vs main | Last commit |
|---|---|---|---|---|
| `evidence/cnv-pipd-ls-sp-20261015-r7` | PR #4 | draft=true | ahead=7 behind=0 | 2026-10-16T01:00:08+08:00 |
| `evidence/cnv-pipd-ls-sp-20261015-r8` | PR #5 | draft=true | ahead=3 behind=0 | 2026-10-16T11:52:41+08:00 |
| `evidence/cnv-pipd-ls-sp-20261015-r9` | PR #7 | draft=true | ahead=4 behind=0 | 2026-10-16T13:00:11+08:00 |
| `pub/lane-reliability-closure-20261016` | PR #6 | draft=false | ahead=4 behind=0 | 2026-10-16T12:05:24+08:00 |
| `pub/far-remediation-and-closure-20261016` | PR #8 | draft=false | ahead=4 behind=0 | 2026-10-16T13:27:27+08:00 |

Per PR, `mergeable`/`mergeable_state`/`changed_files` are pulled from the dedicated
`GET /pulls/<n>` endpoint (chunked over the batch-list endpoint, which does not always populate
these populated merge fields):

```
GET https://api.github.com/repos/shw097-team/Fabric/pulls/<n>
→ PR 4: mergeable=true  clean  draft=true  306 files
→ PR 5: mergeable=true  clean  draft=true  359 files
→ PR 6: mergeable=true  clean  draft=false 74 files
→ PR 7: mergeable=true  clean  draft=true  120 files
→ PR 8: mergeable=true  clean  draft=false 131 files
```

All five merge cleanly into `main` right now. Their base SHA equals current `origin/main`
and none of them has a content conflict with any other open PR (see §3, zero overlap).

### 2.4 SUPERSEDED_AND_DELETABLE

No branch fits this class. Every diverging remote branch either faces an open PR (R7, R8,
R9, two pub/* lanes) or is deliberately long-lived (full-packet). Branches whose PR merged
are instead merged-and-deletable, not superseded.

### 2.5 Counts

```
LONG_LIVED_DO_NOT_TOUCH   : 2  (main, evidence/skill-convergence-20261014-full-packet)
MERGED_AND_DELETABLE      : 3  (docs/*, docs/*-followup, evidence/cnv-pipd-ls-sp-20261015-r6)
SUPERSEDED_AND_DELETABLE  : 0
OPEN_PR_AWAITING_OWNER    : 5  (evidence/r7, r8, r9; pub/lane-reliability…, pub/far-remediation…)
TOTAL                     : 10 remote branches (matches git ls-remote refs/heads count)
```

---

## 3. Open PR detail (per contract)

For each open PR the audit reports number, head, base, head-is-ancestor-of-main, GitHub
mergeability, changed-file count, and whether any of its content already exists on main
by another route.

Content-already-on-main-by-another-route test — shape:

```
git ls-tree -r --name-only origin/main | sort -u > /tmp/main_files.txt
for BR in evidence/cnv-pipd-ls-sp-20261015-r7 \
          evidence/cnv-pipd-ls-sp-20261015-r8 \
          evidence/cnv-pipd-ls-sp-20261015-r9 \
          pub/far-remediation-and-closure-20261016 \
          pub/lane-reliability-closure-20261016 ; do
    git diff --name-only origin/main...origin/$BR | sort -u > /tmp/branch_files.txt
    N_ON_MAIN=$(comm -12 /tmp/main_files.txt /tmp/branch_files.txt | wc -l)
    N_BRANCH=$(wc -l < /tmp/branch_files.txt)
    echo "$BR: branch_files=$N_BRANCH already_on_main=$N_ON_MAIN"
done
# results: r7 306/0, r8 359/0, r9 120/0, pub/far… 131/0, pub/lane… 74/0
```

Pairwise overlap between open PRs:

```
pub/far-remediation… vs r9 → 0 file overlap
pub/far-remediation… vs r8 → 0 file overlap
pub/far-remediation… vs r7 → 0 file overlap
evidence/r9 vs r8 → 0 file overlap
evidence/r9 vs r7 → 0 file overlap
evidence/r8 vs r7 → 0 file overlap
```

Directory-scope sanity (verifies each PR isolates to its own evidence dir):

```
evidence/cnv-pipd-ls-sp-20261015-r7 → EVIDENCE/CNV-PIPD-LS-SP-20261015-R7/
evidence/cnv-pipd-ls-sp-20261015-r8 → EVIDENCE/CNV-PIPD-LS-SP-20261015-R8/
evidence/cnv-pipd-ls-sp-20261015-r9 → EVIDENCE/CNV-PIPD-LS-SP-20261015-R9/
pub/far-remediation-and-closure-20261016 → EVIDENCE/FAR-REMEDIATION-AND-CLOSURE-20261016/
pub/lane-reliability-closure-20261016 → EVIDENCE/LANE-RELIABILITY-CLOSURE-20261016/
```

Content-already-on-main-by-another-route is therefore **false for each of the 5 open PRs** —
each PR's file set is metrologically disjoint from `origin/main` and from every other
open PR's file set. A merge of any of these five is a strict addition:
- the three `evidence/cnv-pipd-ls-sp-20261015-*` heads each add one new evidence packet dir;
- the two `pub/*` heads each add one new publication packet dir;
- none of them re-submits or duplicates work that is already on main.

### 3.1 PR #4 (open, draft) — head `evidence/cnv-pipd-ls-sp-20261015-r7`

```
GET /pulls/4  → mergeable=true, mergeable_state=clean, 306 changed_files, +A/-D deltas one-off
git merge-base --is-ancestor origin/evidence/cnv-pipd-ls-sp-20261015-r7 origin/main
    → branch tip IS NOT an ancestor of main (retcode 1)
```
No overlap with main by another route; no overlap with any other open PR.

### 3.2 PR #5 (open, draft) — head `evidence/cnv-pipd-ls-sp-20261015-r8`

```
GET /pulls/5  → mergeable=true, mergeable_state=clean, 359 changed_files
git merge-base --is-ancestor origin/evidence/cnv-pipd-ls-sp-20261015-r8 origin/main → retcode 1
```
No overlap with main by another route; no overlap with any other open PR.

### 3.3 PR #6 (open, ready) — head `pub/lane-reliability-closure-20261016`

```
GET /pulls/6  → mergeable=true, mergeable_state=clean, 74 changed_files
git merge-base --is-ancestor origin/pub/lane-reliability-closure-20261016 origin/main → retcode 1
```
No overlap with main by another route; no overlap with any other open PR.

### 3.4 PR #7 (open, draft) — head `evidence/cnv-pipd-ls-sp-20261015-r9`

```
GET /pulls/7  → mergeable=true, mergeable_state=clean, 120 changed_files
git merge-base --is-ancestor origin/evidence/cnv-pipd-ls-sp-20261015-r9 origin/main → retcode 1
```
No overlap with main by another route; no overlap with any other open PR.

### 3.5 PR #8 (open, ready) — head `pub/far-remediation-and-closure-20261016`

```
GET /pulls/8  → mergeable=true, mergeable_state=clean, 131 changed_files
git merge-base --is-ancestor origin/pub/far-remediation-and-closure-20261016 origin/main → retcode 1
```
No overlap with main by another route; no overlap with any other open PR.
This PR's head is the branch the local working copy has checked out; nothing was written there by the audit.

### 3.6 Closed-PRs inventory (background for the cleanup telemetry)

```
PR #1 (closed, merged) head docs/skill-convergence-20261014,         27 files
PR #2 (closed, merged) head docs/skill-convergence-20261014-followup, 5 files
PR #3 (closed, merged) head evidence/cnv-pipd-ls-sp-20261015-r6,    581 files
```
All three have `merged=true`, `merged_at` set, and their tips are the exact branch tips
currently live on the remote — confirming no branch drift happened between merge and now.

---

## 4. Option pricing under the governance contract

Under the carrying contract: agent may not self-accept, may not promote, and merges are
reserved to the repository owner. Pricing of each option:

| Option | Content | Risk | Whose call it is |
|---|---|---|---|
| **(a)** Merge an open PR into main | 5 candidates (PRs #4 #5 #6 #7 #8), all `mergeable_state=clean`, all non-conflicting, all zero content-overlap with main. Metrics and cleanliness don't decide ownership: merging *is* acceptance. | Medium — merges are irreversible once the branch is deleted; each PR is also evidence-bound to other rounds and would need its own acceptance pass; the two draft PRs (#4, #5, #7) are not formally opened for review yet. | **OWNER ONLY.** Agent must not execute. |
| **(b)** Delete specific branches | Only the 3 MERGED_AND_DELETABLE branches are safe now: `docs/skill-convergence-20261014`, `docs/skill-convergence-20261014-followup`, `evidence/cnv-pipd-ls-sp-20261015-r6`. Their tips and the full evidence of each round are reachable forever through the merge commits `f14724d`, `266f8d6`, `b8ff810`. Nothing else qualifies: the 5 open-PR branch heads carry pending owner review; full-packet is a documented standing branch. | Low (residue removal only). Names on the merged tips are preserved forever in the PR-object head.sha; deletion is reversible by re-pushing the same SHA. | **OWNER ONLY.** Deletion is a ref mutation, excludes agent. |
| **(c)** Leave everything as-is, publish a merge-readiness packet | Do nothing to the merge surface; publish this MD+JSON pair as the readiness artifact. | Low — zero writes, zero friction, no state change. | **ALLOWED TO AGENT.** Executed: this packet is the artifact. |
| **(d)** Other low-friction options found | None | n/a — nothing further qualifies without crossing the agent/no-write boundary | n/a |

**Explicit statement:** under a contract that reserves merges to the repository owner,
the autonomous agent may perform **only option (c)**. Options (a), (b) and the empty (d)
are reserved to the owner. Nothing in this round was executed against options (a) or (b).

---

## 5. Merge-readiness summary (packets available to the owner)

Five open PRs, all `mergeable_state=clean`, all with current-main base SHA (`b8ff810`),
all with zero conflict against any other open PR, all with zero content overlap with main:
#4, #5, #6, #7, #8. All five LACK content on main by any other route, so a merge is a
strict addition of either evidence packets (the three evidence/cnv-* branch rounds) or
evidence publications (the two pub/* closure branches), not a re-submission of already
merged work.

One PR (#8) is currently non-draft and ready for owner review at the local working copy;
the other PR other than #8 (#6) is also non-draft. Three are still draft (#4, #5, #7).

The three MERGED branch tips correspond one-to-one to closed-and-merged wire pulls #1,
#2, #3. No other branch is merge-cleaned out this round.

**Gaps the owner should be aware of:**
- Fine-grained PAT could not read branch protections (403), so required-review-count /
  required-check visibility is limited to what the surface `/pulls/<n>` already reports (`mergeable_state=clean`).
- The evidence/skill-convergence-20261014-full-packet branch is documented as the standing
  evidence home on several main-tree records; deleting it would break the documented
  provenance chain. Confirmed **DO NOT TOUCH** in this audit for now.

## 6. Provenance and method

- Local clone: C:/Projects/Agent_Workspace/Fabric, checked out on
  `pub/far-remediation-and-closure-20261016` (tip `5ae6f37`), which is the head of PR #8.
- All git calls were paid locally; API calls used only `GET`/`FETCH` (`HEAD`-method-free);
  all writes on the local clone were limited to
  `var/ROUND3-LANE-REBIND-AND-CLOSURE-20261016/evidence/EVIDENCE_REPO_MERGE_AND_BRANCH_CLEANUP.md`
  and its paired `.json` (untracked evidence files, git status shows these as untracked).
- The full evidence tree was not touched; the audit did not check HEAD against the working
  tree but instead read the tree via `origin/main`, `origin/<branch>`, and
  `refs/pull/<n>/head` remotely, which is the authoritative state.

## 7. STOP

Per the carrying contract: **no merges were executed; no branch was deleted, pushed or
mutated; no PR was created, edited, closed, commented on, or otherwise mutated.** This
audit is strictly classification + pricing. Ownership of (a) and (b) is reserved to the
repository owner.
