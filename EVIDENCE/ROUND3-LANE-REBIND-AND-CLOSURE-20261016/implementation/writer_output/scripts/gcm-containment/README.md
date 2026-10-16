# GCM containment — operator / consumer contract

Round `HGK-GCM-CONTAINMENT-20261013`. Claim ceiling: **CANDIDATE_ONLY** — host-measured,
not externally accepted. This directory is the L1 applier plus its L3 consumer and the
deterministic seam/measurement tooling. Nothing here was applied to the live host during
the round; the live `~/.gitconfig` is delivered as an applier the owner runs as one step.

## What the default is right now

Git for Windows wrote the system-scope handler:

```
file:C:/Program Files/Git/etc/gitconfig    credential.helper = manager
```

`git-credential-manager.exe` 2.7.0 permits interaction by default, so when a git call
needs a credential and the store has no usable answer, GCM opens a GUI account-selection
window and waits. Unattended, that call blocks. The measured effective resolution today is
still that single system handler:

```
git config --show-origin --get-all credential.helper
file:C:/Program Files/Git/etc/gitconfig	manager
```

There are four partial mitigations on the host and zero defaults; the defect is the missing
default, not a missing tool.

## What the applier does

`apply_gitconfig_default.py` APPENDS exactly one block to the **user-scope** gitconfig:

```gitconfig
[credential]
	helper =
	helper = manager --no-ui
	interactive = false
```

The empty `helper =` resets the accumulated helper list so the system `manager` is no longer
reached (`gitcredentials(7)`); `manager --no-ui` still answers silently from the credential
store, so cached pushes keep working; `interactive = false` makes GCM return an error instead
of waiting. No admin, no system-file change.

Seven properties, each visible in the code:

1. **dry-run is the default** — writing requires an explicit `--apply`.
2. **full-digest preimage guard** — sha256 of the current target (or `ABSENT`) captured up
   front and re-checked immediately before the write; any change refuses (`ERR_PREIMAGE_CHANGED`).
3. **per-run timestamped backup** — `.bak-<change>-<UTC>` beside the target, plus a
   `.meta.json` recording the preimage digest.
4. **post-write verification by EFFECTIVE resolution** — `git config --show-origin --get-all
   credential.helper` plus a request-level `git credential fill` probe; never a read-back of
   the bytes just written.
5. **receipt JSON** — target, scope, before/after sha256, effective resolution before/after,
   and the exact undo command.
6. **`--rollback`** — restores the preimage byte-identically from the latest backup and prints
   before/after sha256.
7. **append-only** — only ADDS the block; refuses (`ERR_CONFLICTING_CREDENTIAL_KEY`) if the
   target already carries a conflicting `helper` / `interactive` value this tool did not write,
   and never deletes or rewrites an existing key.

Preview (this is also the host-tested acceptance run; it does not write):

```
python scripts/gcm-containment/apply_gitconfig_default.py --dry-run --json
```

Apply is the owner's one step:

```
python scripts/gcm-containment/apply_gitconfig_default.py --apply --json
```

## How to run the preflight as a gate

`credential_preflight.py` is the single, side-effect-free consumer. It reads ONLY the
effective resolution and is three-valued: `PASS` (the resolution provably does not reach a
prompt-capable helper — an empty-string reset is present and every rebound helper is provably
non-interactive), `FAIL` (it does), `INCONCLUSIVE` (git missing, empty or unparsable output).
Exit 0 on `PASS`, exit 2 otherwise; `INCONCLUSIVE` is never counted as verification.

```
python scripts/gcm-containment/credential_preflight.py --json
```

Gate in a script:

```
python scripts/gcm-containment/credential_preflight.py || exit 2
```

Before the fix is applied on this host it returns `FAIL` (exit 2) naming the prompt-capable
`manager` reached from `file:C:/Program Files/Git/etc/gitconfig`. A `PASS` before the fix
would be a checker defect.

## How to roll back

```
python scripts/gcm-containment/apply_gitconfig_default.py --rollback --json
```

This restores the latest preimage byte-identically and prints before/after sha256. The exact
undo command is also carried in the receipt's `undo_command` field. The system gitconfig is
never touched, so rollback is only the user-scope block removal.

## What this containment does NOT cover

- **User scope only.** It writes `~/.gitconfig`. Other Windows users, and machines where the
  system config differs, are not affected.
- **Explicit overrides escape it.** Any call that sets `-c credential.helper=manager`, or
  `GIT_CONFIG_SYSTEM` / `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_NOSYSTEM`, or `GIT_CONFIG_COUNT`
  bypasses the user-scope reset by design. Those are the L2/L3 gaps, and L2 is NOT activated.
- **The system file is untouched.** The system-scope `manager` remains as written by the
  Git for Windows installer.
- **git only.** Non-git credential managers are out of scope.
- **git's own prompt path.** After a helper returns nothing, git can still try an askpass
  program and then the controlling terminal (seam S2). Only the helper-list reset is fixed
  here; a lane that leaves the terminal available still has that second interaction surface.
- **L2 not activated.** `scripts/cred/cred_broker.py` remains STANDING / NON-ACTIVATED; this
  round does not wire it into any write lane (see `execute/artifacts/L2_ACTIVATION_SEAM.json`).

## Human opt-in for a deliberate interactive authentication

When you actually mean to authenticate by hand, defeat the default on that one command:

```
git -c credential.helper=manager -c credential.interactive=true credential fill
```

or run your git command with `GIT_TERMINAL_PROMPT=1` from an interactive terminal and the
system handler in play. This is the deliberate, opt-in path; the default is non-interactive
precisely so that an unattended call never opens a window by accident.

## Tooling in this directory

| file | role |
|---|---|
| `seam_probe.py` | deterministic, model-free, network-free re-runner for seams S1 (`helper_list_reset`) and S2 (`git_own_prompt_fallback`); exits 0 only when every seam is `PASS` |
| `apply_gitconfig_default.py` | the L1 applier (seven properties above) |
| `credential_preflight.py` | the L3 gate (three-valued, exit 0 on `PASS`, exit 2 otherwise) |
| `win_instrument.py` | host-measured window/process sampler; `--self-test` proves discrimination, `--kill-matching` tears down a bounded probe, `--seconds` is a hard deadline |
