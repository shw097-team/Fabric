# Fabric External Independent Challenge Reviewer — Install / Mount

## Package identity

- Plugin: `fabric-external-independent-challenge-reviewer`
- Skill: `fabric-external-independent-challenge-reviewer`
- Version: `1.0.0`
- Default invocation policy: explicit only (`allow_implicit_invocation: false`)
- Candidate permission posture: read-only

## A. Codex / ChatGPT desktop — direct Skill mount

Copy or link this directory:

```text
skills/fabric-external-independent-challenge-reviewer/
```

into one supported Codex local skill location, preferably:

```text
$REPO_ROOT/.agents/skills/fabric-external-independent-challenge-reviewer/
```

for repo-scoped use, or:

```text
$HOME/.agents/skills/fabric-external-independent-challenge-reviewer/
```

for user-scoped use.

Then restart Codex only if discovery does not refresh automatically. Invoke explicitly with the skill selector / `$fabric-external-independent-challenge-reviewer` where supported.

For RP-002, launch Codex from the frozen candidate/review workspace, not from a maker session that has been modifying the candidate.

## B. ChatGPT Work — plugin form

This package already includes:

```text
.codex-plugin/plugin.json
skills/fabric-external-independent-challenge-reviewer/
```

Use it as a local/private plugin package or feed it to the current `@plugin-creator` / plugin installation flow in Work. The plugin contains no MCP server and requests only the review workflow; attach or expose the frozen review files separately according to your workspace permissions.

After installation, select the bundled skill explicitly in a fresh Work session for high-value acceptance review.

## C. Recommended RP-002 invocation

Provide only the clean-room review bundle, not the whole maker conversation:

```text
Use fabric-external-independent-challenge-reviewer.
Review RP-002 gate R1 as an external clean-room challenger.
Do not trust Hermes/HGK/Internal Oracle PASS statements.
Do not modify the candidate.
Re-derive the verdict from frozen r3/A0 authority, exact candidate identity,
canonical Evidence Manifest, raw diffs/tests/traces/receipts, rollback/replay,
and package readback. Search for disconfirming evidence and correlated blind spots.
Return EXTERNAL_CHALLENGE_REPORT.md and recommend only CONTINUE,
RESUME_SMALLEST_REPAIR, META_ORACLE, DOMAIN_OWNER, HITL, or TERMINAL.
```

## D. Local package self-test

From the skill directory:

```text
python scripts/verify_review_bundle.py --self-test
python -m unittest tests/test_verify_review_bundle.py
```

These tests validate the Skill package shape and report/intake contracts only. They do not prove RP-002 runtime acceptance.
