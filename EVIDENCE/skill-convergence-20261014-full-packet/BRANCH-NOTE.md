# Round raw store — side branch, not part of the published payload

> `NOT_EXTERNALLY_ACCEPTED · NOT_MERGED · NOT_RELEASED · NOT_PRODUCTION · NO_LIVE_WORLD_EFFECT`

## What this branch is

`EVIDENCE/skill-convergence-20261014-full-packet/SKILL_CONVERGENCE_RETURN_20261014/` is the round's **complete**
return packet — the raw store: every lane transcript and stdout capture, the briefs, the harness, the manifests,
the closure set. It is what the curated set on `main`
([`EVIDENCE/skill-convergence-20261014/`](../../EVIDENCE/skill-convergence-20261014) on `main`) rests on, so a reviewer
who wants to audit a claim in the curated set can read the bytes behind it.

## Why it is on a branch and not on `main`

`INTEGRATION/MANIFEST.json` on `main` declares `evidence/ raw stores` **excluded** from the published payload. That
declaration is not overridden here: this branch is not the publication. It exists so that the curated set's claims
are checkable, and it is referenced by name from the curated record on `main`.

## What was checked before it was pushed

- no file name in the packet collides with a rule in the mirror's root `.gitignore` (0 collisions), so nothing is
  silently dropped on the way in;
- the owner's credential **value does not appear anywhere** in the packet (compared in memory; only the boolean is
  recorded);
- no `Authorization` header, no `Bearer` value, no `github_pat_`/`ghp_`/`nvapi`/`sk-`/`oc_sk` shaped string, and no
  private-key block appears anywhere; the only credential-shaped matches are 40+ character hexadecimal strings,
  which are the packet's own sha256 digests.
- Audit output: `evidence/packet_content_audit.json` in the round directory, and the same result is stated in the
  curated record on `main`.

## Reproduce the packet's own acceptance command

```bash
git clone --depth 1 --branch evidence/skill-convergence-20261014-full-packet \
  https://github.com/shw097-team/Fabric.git
cd Fabric/EVIDENCE/skill-convergence-20261014-full-packet/SKILL_CONVERGENCE_RETURN_20261014
# run the command in this packet's README.md -> expect `files 638 mismatch []` and `scan NO_HITS`
```

**Windows note.** The packet carries one 188-character relative path (a deliberate deep-path fixture of the subject,
a zero-byte file). With this branch's nesting the whole path exceeds the Windows `MAX_PATH` limit for some clone
roots, and git then checks the tree out with that one file missing while reporting "Clone succeeded, but checkout
failed". Use a short clone root and long-path support:

```bash
git -c core.longpaths=true clone --depth 1 --branch evidence/skill-convergence-20261014-full-packet \
  https://github.com/shw097-team/Fabric.git C:/fx
cd C:/fx/EVIDENCE/skill-convergence-20261014-full-packet/SKILL_CONVERGENCE_RETURN_20261014
git -c core.longpaths=true restore --source=HEAD :/     # only if the checkout reported the fixture missing
```

On Linux and macOS the checkout is unaffected. The committed blob is the empty file the manifest records
(`bytes: 0`, sha256 `e3b0c442…`), so nothing is lost by the long path — it is an environment limit, not missing
content, and it is recorded here rather than discovered by a reader.

## Provenance of this branch

The packet was first pushed to `shw097-team/PIPD-LS-SP` (branch `feat/skill-convergence-return-20261014`,
`e8997254c369957fb8b3a137aacb3c84d9d458ee`). The owner had named the Fabric repository as the destination for this
round's material, so the packet was republished here and that branch was deleted, restoring the other repository to
its previous ref set. The deleted tip is recorded in the curated record on `main` and can be restored from this
branch, which carries the same bytes.
