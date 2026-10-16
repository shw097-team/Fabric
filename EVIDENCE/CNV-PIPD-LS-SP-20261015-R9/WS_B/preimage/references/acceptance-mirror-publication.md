# Publishing a local governed workspace as an external acceptance mirror

For the request "open a public repo and mirror these subjects so an external acceptance officer can
verify them all at once". The workspace is large, contains secrets and runtime state, and the repo
has no remote yet — the order of operations is what keeps this safe and honest.

## Procedure

1. **Recon before creating anything.** Locate each subject, measure it (`du -sm`), and find the
   secrets directories. A governed workspace root is routinely enormous because of `var/`
   (SQLite DBs, working data), `worktrees/`, `evidence/`, `.venv/`, and build staging. Never
   mirror it wholesale; decide the curated set deliberately.
2. **Create the remote repo PRIVATE first.** Stage, scan, and push while private; flip to public
   only after the secret scan is clean. Creating it public first publishes before you can scan —
   the one irreversible mistake in this workflow.
3. **Curate.** Include source / tests / docs / contracts / schemas / config and each subject's
   deliverables. Exclude `var/`, `worktrees/`, `evidence/` raw stores, `.venv/`, build `stage/`,
   and third-party vendored blobs (a downloaded distribution archive plus its extraction is not a
   governance artifact). Record the exclusion list in the mirror README so the acceptance surface
   is explicit.
4. **Secret-scan, then JUDGE the hits.** Grep for `github_pat_[A-Za-z0-9_]{20,}`,
   `-----BEGIN ... PRIVATE KEY-----`, `nvapi-`, `xox[baprs]-`, and key-file names (`.env`,
   `*_API.txt`). Do not stop at the match: a `sk-...` value inside a test fixture with an obviously
   synthetic body is a placeholder, and a bare variable NAME (`"OPENROUTER_API_KEY",`) is not a
   value. Never publish a live credential — exclude the file and say so.
5. **Write the integration framing.** Top-level README stating the governance binding (which
   component is the sole control plane, what is bound as the runtime/orchestration plane), a
   per-subject directory map, the excluded paths, the claim ceiling, and the concrete entry points
   an external officer can independently re-check. Keep the binding statement verbatim.
6. **Commit and push.** The repo may have no user config; pass `-c user.name=... -c user.email=...`
   per commit. For push auth use the credential-in-URL form
   `https://x-access-token:<TOK>@github.com/<owner>/<repo>.git`, passed inline so it never lands in
   `.git/config`. A fine-grained PAT sent as `-c http.extraheader="Authorization: Bearer <tok>"`
   fails with `invalid credentials` for git push — do not debug that path.
7. **Flip visibility** with `PATCH /repos/{owner}/{repo}` `{"private": false}`.
8. **Verify by reading back**, never by trusting the push output: `git ls-remote` for the tip, and
   the git trees API `GET /repos/{owner}/{repo}/git/trees/<branch>?recursive=1` for the file list.
   Compare the set of top-level directories against the intended subject list and print
   `truncated`. A 200 for one file does not prove a whole subject landed.

## Pitfalls

- **`cp -r <src>/* <dst>/ 2>/dev/null` hides a failure and leaves an EMPTY subject directory.** A
  whole subject went missing from a first push this way. After any bulk copy, count files
  (`find <dst> -type f | wc -l`) and never suppress stderr on a staging copy.
- **A nested `.git` inside a copied tree is captured only as a gitlink.** Git warns "adding
  embedded git repository" and the nested files are ABSENT from the mirror. Delete the nested
  `.git` before committing so the content becomes part of the repo. Silent subtree loss is worse
  than a loud failure.
- **`git add -A` sweeps in staging scratch** (API response dumps, probe outputs). Keep scratch out
  of the staging tree and re-check `git ls-files` for entries that should not be there.
- **`curl ... -w "..."` can exit non-zero and abort an `&&` chain mid-way**, silently skipping the
  verification steps that follow. Run verification as separate statements.
- **Committing into a repo that already carries unrelated uncommitted work.** `git add` only your
  own paths, never `-a`. Check `git diff --stat <path>` per file. If a file you edited was ALREADY
  modified before you touched it, your commit sweeps in those pre-existing edits — disclose which
  portion is yours rather than letting the diff imply you authored all of it.
