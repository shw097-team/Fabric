# Publishing a governed workspace mirror to an external repo

When the user asks to "integrate subject A + B + C and mirror them to a new public repo so an
external acceptance officer can verify all at once". The deliverable is a *curated* mirror plus
a verified remote tip — not an rsync of the working tree.

## 1. Sequence (order is the safety mechanism)

```
1. create the repo PRIVATE          -- never public-first: a public repo is indexed immediately
2. stage a CURATED tree
3. VERIFY the staged tree (per-subject file counts -- see pitfall below)
4. secret scan + adjudicate every hit
5. commit locally, then push
6. read back the remote tip (git ls-remote) and the remote tree (API recursive listing)
7. flip to public ONLY after 3-6 pass
```

Flipping visibility: `PATCH /repos/<owner>/<repo>` with `{"private": false}`; read back
`visibility` from the response rather than assuming.

## 2. Curation: what a mirror excludes

Include: source, tests, schemas, scripts, config (de-secreted), docs, and the acceptance
deliverables themselves.

Exclude (and say so in the mirror's README, because an acceptance officer must know what is
*not* being asserted): working-data directories, SQLite databases, git worktrees, raw evidence
stores, virtualenvs, build staging dirs, and any secret directory.

A single working-data directory can dwarf the whole repository — measure before deciding
(`du -sm <dir>/*  | sort -rn | head`), because an unmeasured copy can be tens of times the
size of the governance artifacts you actually meant to publish.

## 3. Pitfall: a stderr-suppressed copy loses a whole subject silently

`cp -r "$SRC"/* "$DST/" 2>/dev/null` that fails produces **no error and no files**, while the
surrounding script still prints its success line. An entire subject was missing from a first
push this way, and the remote read-back is what caught it.

Rule: after staging each subject, **assert its file count** before committing, and re-derive the
expected count from the source:

```bash
find "$DST/SUBJECT" -type f | wc -l        # must be > 0 and must match the source minus exclusions
```

Prefer `tar cf - --exclude=... . | (cd "$DST" && tar xf -)` over a globbed `cp -r`: it keeps
hidden files, handles names with spaces, and fails loudly.

## 4. Secret-scan adjudication (do not blanket-exclude, do not blanket-publish)

Scan the staged tree, then classify every hit into exactly one of:

| Class | Example | Action |
|---|---|---|
| Real credential | a live token/private key | exclude, report |
| Test placeholder | `sk-ABCDEFG...` in a test fixture | benign, publish |
| A bare variable NAME | `"OPENROUTER_API_KEY",` in a list | benign, publish — it is a name, not a value |

Report the adjudication explicitly (which file, which class, why). Publishing a live credential
is irreversible; silently dropping a test fixture weakens the mirror. Neither default is right.

Read credentials into an env var and never echo them; pass them inline to the push URL rather
than writing them into `.git/config`.

## 5. Host mechanics that matter

- Create: `POST /orgs/<org>/repos` with `{"name","private":true,"auto_init":true}`.
- Push form: `https://x-access-token:<PAT>@host/<owner>/<repo>.git`. The
  `git -c http.extraheader="Authorization: Bearer <PAT>"` form can fail with
  `invalid credentials` even when the same PAT reads the repo fine over the REST API.
- `auto_init:true` puts an initial commit on the remote, so the first push must be forced.
- **A force-push is a destructive action and needs explicit user consent.** If the runtime
  blocks it, stop and ask in plain text — do not retry, do not rephrase the command.
- Verify with ground truth, not the push exit code: `git ls-remote <url> refs/heads/main` for
the tip, and `GET /repos/<o>/<r>/git/trees/<branch>?recursive=1` for the file list.

## 6. Hygiene

Never let a scratch file captured with `curl -o` (an API response) get committed — check
`git status` for strays before the first commit, and if one lands, remove it in a follow-up
commit rather than leaving it in the mirror.

## 8. Publishing governed evidence to an EXISTING mirror (dual-branch, exact-SHA subjects)

When the remote repo already exists (it is an acceptance mirror you reuse, not create): do not
touch repo creation and do not change visibility — repo-settings mutation is not part of
candidate publication. Probe first, then push your own branches:

```bash
# 1. find the credential the user keeps for this (often a fine-grained github_pat_ in a file)
PAT=$(grep -oE 'github_pat_[A-Za-z0-9_]+' "$TOKFILE" | head -1)
# 2. probe BEFORE mutating: /user + /repos/<owner>/<repo> both HTTP 200 == token valid AND repo exists
curl -s -H "Authorization: Bearer $PAT" https://api.github.com/repos/<owner>/<repo> -o "$TMP/evb.json"
# 3. credential file OUTSIDE the repo; token-free origin URL in .git/config
printf 'https://<user>:%s@github.com\n' "$PAT" > "$LOCALAPPDATA/hgk-git-credentials"; chmod 600 "$LOCALAPPDATA/hgk-git-credentials"
git config credential.helper "store --file=$LOCALAPPDATA/hgk-git-credentials"
git remote add origin https://github.com/<owner>/<repo>.git   # never embed the token in the URL
# 4. push TWO separate branches: source candidate (PR head) and evidence;
git push -u origin <source-branch> <evidence-branch>
# 5. read back remote refs with ls-remote and assert each equals the local exact SHA
# 6. after done: rm the credential file and git config --unset credential.helper
```

Governed acceptance binds two immutable subjects that MUST differ: `source_candidate_sha`
(PR head) and `evidence_commit_sha` (the exact commit that contains the sanitized
EVIDENCE_RETURN_PACK). Push each on its own branch; open one PR whose `head.sha ==
source_candidate_sha` and verify it via API. `git -c http.extraheader=...` may fail with
`invalid credentials` — the credential-helper store form above is the reliable one.

### 8.1 Pitfall: the readset evidence_commit_sha self-reference loop

If the readset/manifest records `evidence_commit_sha` pointing at the branch tip that *contains
the readset itself*, every correction re-writes the readset, which changes the tip, which
invalidates the recorded SHA — an unbounded chase. Break it by making the acceptance subject an
immutable commit that is NOT the self-describing manifest:

- `evidence_commit_sha` = the exact commit that carries EVIDENCE_RETURN_PACK (e.g.
  `a6ee9b5...`), which by rule is **different** from the readset commit.
- The branch tip (which does move as you add pointer commits like the compiler receipt and the
  readset itself) is a **non-subject pointer** — record it in the PR description, never in the
  frozen readset. Branch tip is never an acceptance subject anyway.

This mirrors the source side: `source_candidate_sha` is the frozen PR-head commit, and later
commits to the branch do not change the subject the acceptance officer is bound to verify.

### 8.2 Secret hygiene for this flow

Fine-grained PATs read from a file and piped straight into the credential store never appear in
`.git/config`, shell history, or the repo. `/tmp` is unreliable for `curl -o` on MSYS — write the
probe to `$LOCALAPPDATA/Temp`. Token file paths may be given by the user rather than pasted —
read the token from disk, never ask for it in chat. Remove the credential file and unset the
helper once publication is done.

The mirror's README must state, in this order: the governance binding in one line; a table of
subject -> role -> what it may NOT do; the directory map; the **exclusion list**; what an
external officer can concretely verify (with file paths); and the claim ceiling plus non-claims.
A mirror without an exclusion list and a claim ceiling invites an over-claim.
