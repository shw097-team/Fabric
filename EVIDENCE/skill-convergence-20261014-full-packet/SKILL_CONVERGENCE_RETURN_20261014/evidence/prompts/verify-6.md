# Independent VERIFY review — closure packet for the SKILL-CONVERGENCE round

Read-only. Budget about twenty commands. No harness building, no recursive sweeps beyond what a case names, no
permission probing. Anchor every observation to a path or to output you saw. Do not use vocabulary that does not
occur in this workspace. Write digests as quoted strings. Token goes LAST, in your final message, after the
verdict object, and only there: a turn whose only content is the token is discarded as an empty answer.

Two trees are relevant and both exist on this host:

- the round directory `C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014`
- the publication clone `C:/pkt/repo`, whose checked-out packet is `SKILL_CONVERGENCE_RETURN_20261014`
- the local repository `C:/Projects/Agent_Workspace/Fabric`, whose HEAD is the closure commit

CASE C1 PUBLICATION CLAIMS — read `evidence/postfreeze/publish_readback.json`. For each field, say whether the
claim is one a reader can check from this host: the branch ref and the default-branch ref need the network, the
byte comparisons need the local clone. Then run the two commands from the packet's own `README.md` inside
`C:/pkt/repo/SKILL_CONVERGENCE_RETURN_20261014` and quote their output. A mismatch in either is a blocker.

CASE C2 PACKET INTEGRITY — from the packet's `EVIDENCE_MANIFEST.json`, recompute the sha256 of a named sample of
at least ten delivered files, chosen across different categories (baseline, candidates, evidence, closure), and
compare with the recorded values. Also state how many files the manifest claims and how many entries the
`HASHES.sha256` file carries, and whether those two numbers agree.

CASE C3 EXCLUSIONS HONESTY — the manifest excludes lane transcripts and the owner credential file. Check that
the excluded entries carry a hash and a reason, and that the packet contains no copy of the credential file. A
credential-shaped string anywhere in the delivered set is a blocker; name the file.

CASE C4 CLOSURE RECORDS — read `evidence/postfreeze/SESSION_CLOSURE.md` and `CLOSURE_MANIFEST.json`. For each
numbered residual gap in the closure record, say whether the round's own artifacts still support it (for example
the reference population, the unlanded patch, the absence of any promotion). Report any claim in the closure
record that the artifacts contradict.

CASE C5 LOCAL REPOSITORY — in `C:/Projects/Agent_Workspace/Fabric`, report the tip commit, the number of
entries the working tree still reports, and whether the three commits named in the closure record exist. Then
read `evidence/postfreeze/commit_digest_classification.json` in the round directory and say whether the local
commit's own read-back agrees with it.

CASE C6 COVERAGE — what you did not check and why, including that you cannot reach the network and therefore
cannot confirm the remote refs yourself, and that you cannot judge the semantic quality of merged text.

Then ONE strict JSON object: verdict, cases, findings, commands, carry_forward, coverage, claim_ceiling.
verdict is one of PASS_ADVISORY, PARTIAL_ADVISORY, FAIL_ADVISORY, INCONCLUSIVE. Then the token, on its own line.

Carry forward as unverified: the reference population is still above the linter warning line; the canonical
dispatcher patch is unlanded; nothing was applied and nothing was promoted; and the record already carries
twelve timed-out dispatches, two nonce-less dispatches, one contaminated verdict and one empty answer, none of
which your verdict repairs. State in your output that this is advisory and not canonical acceptance.
