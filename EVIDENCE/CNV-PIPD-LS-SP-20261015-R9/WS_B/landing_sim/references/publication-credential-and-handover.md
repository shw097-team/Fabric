# Publishing a governed candidate: credential facts and hand-off

## Where the GitHub credential lives (this workstation, 2026-10-11)

The operator's push credential is a file named `Fine-grained personal access tokens.txt`:

- **Primary copy: `C:\Projects\Agent_Workspace\PIPD\Fine-grained personal access tokens.txt`** — i.e. **inside the
  PIPD git working tree**. An older copy may still exist at `C:\Projects\Agent_Workspace\API KEY\`.
- **It is NOT a bare token.** The file is several labelled lines. Measured shape: a `NAME` label line, the token
  *name* line (`HGK-SWOF-ACCEPTANCE-BRIDGE`, 26 chars), a `personal access token` label line, then the value
  (`github_pat_…`, 93 chars) on its own line. Taking `head -c N` of the whole file, or grepping a pattern that
  excludes `-`, silently yields the wrong bytes and a 401 that looks like a dead credential but is really a parsing
  bug. Extract with `github_pat_[A-Za-z0-9_-]+` and never print the result.
- **Extraction and use rules:** read it into a temp file OUTSIDE any repo, use it only via an `Authorization`
  header or a credential helper, never in a remote URL that lands in a log, never in argv, and delete the temp file
  after. Compare a supplied value against the file copy by **sha256** — that proves identity without transcribing a
  secret.

### Status of the supplied values (measured)

Every value supplied so far, including one pasted into chat by the operator on 2026-10-11 (verified byte-identical to
 the file copy by sha256), returns **`401 Bad credentials`** on `GET /user`, `/orgs/shw097-team`,
`/repos/shw097-team/PIPD-LS-SP` and `/repos/shw097-team/Fabric`, with **no `X-OAuth-Scopes` response header** — i.e.
the token is not recognised at all, not merely under-scoped. Both `Authorization: Bearer` and `Authorization: token`
behave identically. The repo itself answers **200 anonymously**, so the endpoint and name are correct and the fault is
the credential.

**Resolved 2026-10-11 — publication succeeded, and the cause was NOT the secret.** Three tokens were tried;
the third pushed the branch (verified by a fresh anonymous clone). The lesson reverses the earlier
conclusion: **check the permission set before asking the operator for a new secret.** Two facts each cost a
cycle:

- **Two of the tokens were VALID yet read-only.** `GET /user` → 200, the repo → 200,
  `x-accepted-github-permissions: contents=read` on a Contents read, and every write → `403 Resource not
  accessible by personal access token`. A `200` on any *read* says **nothing** about write ability.
- **Repository access set to "Public repositories" is read-only by design** for fine-grained PATs — it cannot
  be upgraded to write. It must be **"All repositories"** or **"Only select repositories"** with
  **Contents: Read and write**. A brand-new PAT defaults to Metadata-only, so Contents is usually `Read`
  unless deliberately changed.

The earlier diagnosis ("revoked/expired/never-activated", above) was correct for the specific value it was
measured on, but it was wrong as a **rule**, and it caused two unnecessary re-issues. A `401` that is genuinely
about the value looks like a missing/invalid credential; a **`403` with that particular message is a
permission problem on a VALID token** — read the difference.
A push needs a fine-grained PAT with **Contents: read and write** on the target repo (and org approval if the
repo is org-owned), a deploy key, or a GitHub App.

### A VALID token can still be read-only — and the obvious check lies

Measured 2026-10-11 on a freshly issued fine-grained PAT: `GET /user` → **200** (login resolves), the target repo
→ **200**, and yet every write is refused. Do not conclude "the token works" from a 200 on a read.

Three measurements, in increasing order of authority:

1. **`x-accepted-github-permissions` on a Contents read** — `200` with `contents=read` means *read* is granted. It
   tells you what the read *required*; it is not an enumeration of the grant.
2. **The `permissions` block in `GET /repos/{owner}/{repo}` is a TRAP.** It reported
   `{'admin': True, 'maintain': True, 'push': True, ...}` for this read-only token. That block describes **the
   user's** permission on the repo, not the fine-grained PAT's grant. Never cite it as evidence that a token can
   write.
3. **A reversible write probe is the only proof.** Create a branch ref pointing at a commit the remote already
   has, then verify and delete it:

   ```bash
   curl -s -o /tmp/p.json -w "http=%{http_code}\n" -X POST \
     https://api.github.com/repos/<owner>/<repo>/git/refs \
     -H "Authorization: Bearer $T" -H "Accept: application/vnd.github+json" \
     -d '{"ref":"refs/heads/__perm_probe__","sha":"<sha-already-on-the-remote>"}'
   ```

   `403` with `"Resource not accessible by personal access token"` = the token lacks the write permission (this is
   the fine-grained signature; a classic PAT with missing scope says something else). Using an
   already-present commit means a successful probe costs nothing to undo, and a denied probe creates nothing — check
   with `GET .../git/ref/heads/__perm_probe__`; `404` confirms nothing was created.

`git push` with such a token fails as `403 ... Permission to <owner>/<repo>.git denied to <user>` — note it blames
the **user**, which invites a wrong fix (checking org membership) when the real defect is the token's own permission
set. Fix is owner-side: edit the PAT → Repository permissions → **Contents: Read and write** (the value does not
change, so the retry needs no new secret), and clear any pending org approval.

### A token file inside the repo is a live hazard

An untracked credential file in a repo working tree is one `git add -A` away from being committed and pushed. Keep the
ignore rules in place (`Fine-grained personal access tokens*.txt`, `API KEY/`) and verify with `git check-ignore -v`.
On rotation, record the **reasoning** rather than asserting a rule. The owner's standing position (2026-10-11) is
that rotating a credential which GitHub does not recognise at all (`401`, no scope header) is unwarranted, because
an unrecognised value confers no capability and its disclosure removes none — so it was recorded as
`rotation: NOT_REQUIRED`, not as an open item. That reasoning does **not** transfer to a credential that *is*
valid: a recognised token carries real capability, and the case for rotating one that has appeared in a transcript
is correspondingly stronger. Judge by capability conferred, not by the fact of exposure.

## Hand-off shape for a blocked publication

When publication is credential-blocked, the round is not "unfinished" — it is **`NOT_EXECUTED` with a named cause**,
and that is a complete, verifiable outcome. Hand over, in one place: the frozen candidate commit and tree, the exact
probe commands and their HTTP codes, the anonymous control that proves the endpoint works, and the specific decision or
asset the operator must supply. State plainly whether the block is *external only* (local evidence still stands) or
*whether it also invalidates an internal claim*. A blocked push does not invalidate local acceptance evidence, but it
does mean an external verifier sampling only the remote sees the pre-repair state — say both.
