# Evidence-integrity, packaging-order and probe-design lessons

Ways a "closed" artifact lies about itself. Each was produced by a real governed submission, caught by an
external challenge, a fresh checker, or the author's own canonical-domain probes, and each is cheap to
prevent.

## L1 — a gate keyed to a NAME instead of a CLASSIFICATION

A HumanGate requirement derived from the operation string alone let a P3-classified request combined with
the operation name `read` execute with **no approval token**, contradicting the canonical risk-tier
invariant ("P3/P4/P5 without a valid exact token -> DENY").

Two compounding errors made it worse:

1. an in-repo test encoded the wrong semantics (operation = the gating authority), and
2. the fresh checker cited that test to downgrade the finding to `NON_BLOCKING`.

**Rule.** When a frozen authority keys a requirement to a *classification* (risk tier, permission
class), a *name* may only TIGHTEN it. A repo test is evidence, never authority. A checker that defers to
repo tests over the canonical source has an **oracle defect**, and that defect is itself blocking
regardless of how green the rest of the package is.

## L2 — a receipt that hardcodes one fact while deriving another

A closure receipt emitted a "checkpoint bound to source" claim from a claim function while its own detail
block — read from a stale pre-ChangeSet diagnosis file — still recorded `NOT_BOUND` and
`TEMP_CLOSED_STATE`. The submitted artifact contradicted itself.

**Rule.** Every field of a receipt that describes the same underlying fact must be derived from ONE live
source. Never mix a computed claim with a file-sourced detail block. Symptom to watch for: a claim and a
non-claim that negate each other inside one JSON object — grep your own receipts for that before shipping.

**Prose form of the same defect.** Narrative sections (dossier, report) get the same treatment: a generator
that hardcodes an obsolete blocker sentence emits it unconditionally, so the artifact presented as the
"current" summary contradicts the live closure state it sits beside. Branch the prose on the same boolean
the receipt uses (resolved / not resolved) instead of shipping one fixed paragraph.

## L3 — a descriptor register computed through a drifted path

After the evidence root moved to a new subdirectory, one loop still read the old prefix. Every blob read
returned empty, so the manifest recorded the **empty-file sha256** (`e3b0c442...`) with `bytes: 0` for five
genuinely non-empty descriptors. A second loop with the same bug made the secret scan report
`scanned_bytes: 40` for a 1.2 MB pack.

**Rule.** One constant for the evidence root, used by every reader and writer. ASSERT the blob is
non-empty before recording its hash, and assert a scan denominator is of the same order as the pack size.
An empty hash or a tiny scan denominator is always a harness bug, never a real artifact.

## L4 — a denominator that counts nothing because the rows carry the wrong scope key

`denominator(project)` joins `requirements.project_id`. The governed obligations had been registered under
a different project id than the governance project, so it reported a vacuous **0/0** while four real
WorkOrders were terminal. The closure claim then rested on rows the denominator could not see.

**Rule.** After any governed registration, READ BACK the denominator and require it **non-zero in the same
scope** as the closure claim. `0/0` is never a valid closure. Re-admitting the population under the
correct scope is honest as long as the historic mis-scoping is *disclosed* rather than rewritten.

## L5 — binding a checkpoint to an exact subject when the schema has no `repo_head`

The canonical `checkpoints` schema carries `state_digest`, `source_digest` and `repo_head`, but the typed
`ProjectLifecycleController.checkpoint()` sets `repo_head` to `""`. Claiming "checkpoint bound to source
SHA" from that field is false.

**What actually works, with typed APIs only:** pass the exact source SHA inside `evidence_refs`
(e.g. `"SRC:<40-hex>"`). The controller builds a payload that includes `evidence_refs`, computes
`state_digest == source_digest == sha256(canonical_json(payload))`, and stores the payload under
`project_lifecycles.intent_json["_checkpoint"]`. The binding is then **recomputable**: re-derive
`sha256(canonical_json(stored_payload))`, assert it equals the recorded `source_digest`, and assert the
payload literally names the source SHA. Report the canonical field (`source_digest`) as the binding
surface — never invent a schema field.

## L8 — a writer that dies fast is a dead relay, not a bad spec

The Codex writer invocation runs against a local relay on `http://127.0.0.1:10101` (websocket
`ws://127.0.0.1:10101/v1/responses`). If the relay is not running, the writer does NOT hang — it fails
**fast**, and the harness still reports `exit code 0` because the *harness* succeeded:

```text
codex_exit: 1          # the child failed
duration_s: ~108       # successful rounds take 13-45 min
candidate_changed: false
changed_paths: []
```

Diagnostic signature in the captured jsonl: `os error 10061` / "目標電腦拒絕連線" / "Reconnecting...
n/5 (stream disconnected before completion)" against `127.0.0.1:10101`.

**Rule.** Before dispatching any writer, check `curl -s -o /dev/null -w "%{http_code}" \
http://127.0.0.1:10101/healthz` and require `200`. If it is `000`, start the relay first
(`export OPENCODEX_HOME="$LOCALAPPDATA/HG-KSEOS/opencodex-hermes"; ocx start`) and poll healthz until it
returns 200. And when a writer reports exit 0 with `codex_exit != 0`:
`candidate_changed: false` and `changed_paths: []` in ~2 minutes, read the CODEX_*.jsonl **before**
touching the spec — do not "fix" a prompt that was never delivered to a model.

**Variant — relay up but the provider credential resolved empty.** The relay's provider entry can store
its key as an **env placeholder** (`apiKey: ${SOME_API_KEY}`). Starting the relay from a shell that lacks
that variable makes the credential resolve to nothing, and the writer then fails in ~2 s with
`openai-chat requires a non-empty credential (authMode: key)` (or the websocket equivalent,
`426 Upgrade Required`). This is a **setup** problem, not a spec problem.

Fix — load the environment BEFORE starting the relay:

```bash
set -a; . "$HOME/AppData/Local/hermes/.env"; set +a
export OPENCODEX_HOME="$LOCALAPPDATA/HG-KSEOS/opencodex-hermes"
ocx stop; ocx start        # then poll healthz until 200
```

Diagnose without printing the secret: read the provider's `apiKey` from the relay config and check whether
it matches `^\$\{?[A-Za-z_]\w*\}?$`, then check whether that variable name is set in the current shell.
Confirm the fix from the relay's own `usage.jsonl` — look for requests with `status: 200` for the
configured provider/model before assuming the writer is working. Never echo the credential into a log,
receipt, or reply.

## L9 — a published evidence tree must not carry unlabelled prior-round artefacts

Binding every file in an evidence directory to the current subject (`subject_reference = <current sha>`)
is wrong when that directory accumulates earlier repair rounds. An R1 closure receipt still asserting
"checkpoint NOT bound" and a published-evidence claim, sitting in the final-subject root and bound as
`DIRECT_FINAL_SUBJECT`, directly contradicts the final dossier — and bytes, not labels, are what a
verifier reads. Relocate prior-round artefacts under `historical/` with their own linkage mode and a
non-current subject reference, add a notice naming the superseded subjects, and **rebuild** the subject
root instead of merging into it (adding a relocated copy while leaving the originals reproduces the
bug). Fix every path class, not just the file names a report cites: prior-round checker logs under
`checker_live/` and `changeset_core/` are bound the same way.

**Classify by provenance FIRST, then by content — neither axis alone works.** Two wrong classifiers were
tried before the right one:

- a *prior-round name pattern* is whack-a-mole: it keeps leaking new families (`W2_R1_*`,
  `CODEX_WO-SWOF-W2-R001..R006`, prior-round compiler bundles that match on a substring), and each leak
  ships an artefact asserting a superseded subject while bound to the current one;
- an *allowlist of this round's artefacts, content-checked* over-relocates the current round's REAL
  artefacts whenever they legitimately do not name the current subject — a baseline adjudication that
  quotes only the baseline SHA, or a compiler receipt — so live evidence gets demoted to `historical/`,
  which is the same class of incoherence in the opposite direction.

The rule that held:

1. an explicitly retired artefact (basename containing `_SUPERSEDED`) is historical, whatever its prefix;
2. otherwise a prior-round NAME is decisive → historical: an earlier round's generator can stamp the
   current candidate into a legacy-named file, so content alone would wrongly promote it;
3. otherwise THIS round's name prefix (e.g. `R4_`) is decisive → current, independent of content;
4. otherwise current iff the bytes name the current subject;
5. raw `.log`/`.jsonl` are never current-bound (see the transcript paragraph below).

Then prove the classifier against the real directory listing AND against current-round negatives, and
**rebuild** the subject root from scratch each time — adding a relocated copy while leaving the originals
in place reproduces the bug.

Also fix identity at the source: an artefact copied with `cp` keeps the ORIGINAL `schema`/`repair_id`,
so a file named `R4_*` can assert `SWOF-W2-CLOSURE-R1` — regenerate it with the round's identity instead.
The same trap applies to harness-generated fields: when the writer/apply harness hardcodes a round id or
workorder in its output header, every receipt and raw log it emits self-labels a PRIOR round. Derive
those fields from the round's own constants, and grep the generated artefacts for stale round identifiers
before packing.

**Raw run transcripts are audit material, never current-subject evidence.** A `.log`/`.jsonl` carries
harness boilerplate, and that boilerplate has mislabelled a round (a current writer log whose embedded
header named a prior workorder) — binding one to the current subject re-introduces the very incoherence
this lesson is about. Classify transcripts as historical/raw at the SUFFIX level, not by name pattern.

**`historical/` must win over every other classification.** Run the relocation test FIRST in the linkage
function; a relocated artefact that inherits `WORKORDER_CHECKPOINT` from a name-suffix match is still a
current-labelled artefact to a reviewer, even though its subject reference is superseded.

**Hash-binding is not retrievability.** A receipt that names a transcript by path + sha256 satisfies
integrity only if that path exists in the PUBLISHED tree; pointing at an out-of-tree file means the single
independent transcript cannot be retrieved from the publication at all. Copy it into the evidence set (it
may live under `historical/`) and point the receipt at the committed path.

## L10 — after any structural edit, audit for deleted definitions before running

Replacing a region by index (`t[:start] + new + t[end:]`) silently deletes everything between the two
anchors — including module constants and helper functions you did not intend to touch. `ast.parse` still
passes (a missing `NAME` is a runtime `NameError`, not a syntax error), so the damage only shows when the
harness runs and returns a bare `None`/`None items`. After ANY structural edit, run an undefined-name
audit over the AST (collect Store/FunctionDef/ClassDef/import names plus builtins and parameters, then
diff against Load names) before invoking the script. Recovery: a stale `__pycache__/*.pyc` from before
the edit still holds module constants (`import` it and read the names) — but check its mtime, because it
may predate your later fixes, so restore the values while KEEPING the corrections you made since.

Also guard the anchor: an assertion like `"def foo(" not in t` before inserting catches the case where
a previous failed attempt already wrote the broken block (it wrote before its own parse check failed).
When a heredoc passes code containing escape sequences, prefer concatenating string pieces over
embedding `\n` inside a nested f-string — the escape can be materialised and produce an unterminated
string literal.

## L11 — finalize every artifact BEFORE running anything that binds its hash

A receipt/checkpoint payload that computes `EVIDENCE_SHA:{sha(path)}` at run time binds whatever revision
existed at that moment. Editing the receipt afterwards leaves the canonical checkpoint binding a blob
that is no longer in the published tree — a binding to a non-existent subject, which is a real
coherence defect, not cosmetic. It is invisible unless you hash the COMMITTED blob and compare, because
the receipt's own `independent_checker.sha256` may be correct while a mirror inside the checkpoint
payload is stale. Fix by re-running the chain in dependency order and re-verifying:
**finalize receipt → projection → closure → pack → readset → register**, then assert that every sha
declared as a BINDING resolves to a blob present in the published tree. When scanning for unresolvable
hashes, separate BINDING references (must match a committed blob) from CONTENT DIGESTS of non-file
inputs (the PI06 §15.5 golden vector, a checkpoint `source_digest` recomputable from the payload) and
COMMIT refs — a blanket "every 64-hex must match a blob" rule buries the real defect in false positives.

## L12 — the artifact-generation chain has a strict order, and it includes derived readbacks

Every artifact that READS live machine truth (a projection, a typed-lineage receipt, a checkpoint
summary) must be generated AFTER the thing it reads, and before the pack that commits it. Generating a
lineage receipt before the projection is what produced a receipt naming a checkpoint the very next
projection replaced. Fix the order once, in the harness, and make each such script assert its
precondition (e.g. `assert spine_last_checkpoint_id == projection.final_checkpoint_id`) so a stale
readback REFUSES instead of being published. Working order:
**finalize receipt → projection → closure → lineage readback → pack → readset → verification register**.

Also: not every artifact that verified a superseded tuple is safe to publish. If the EVIDENCE changed
but the SOURCE did not, a retired receipt still NAMES the current source, so publishing it inside the
tree makes a historical artefact reference the current subject — the contradiction you were trying to
avoid. Keep superseded receipts OUT of the tree as out-of-tree audit material and reference the current
round's equivalent BY ROLE from any in-tree summary (an in-tree prepublication pack cannot know a
post-publication receipt's hash anyway).

## L6 — two probe-harness traps that fabricate failures

- **Dual module identity.** Importing the product as `src.security.x` while the product's own tests import
  it as `security.x` creates two distinct classes, so `isinstance` fails and a valid object is rejected
  with a type-guard error. Import the product the same way its tests do, or lift the symbols from the
  already-loaded test module's namespace.
- **A fixture helper that re-signs.** A `valid_token(**overrides)` helper re-computes the signature, so it
  can never express "payload changed after signing". Use `dataclasses.replace` on an already-signed value
  instead. Related: such a helper is signed for the DEFAULT request, so mutating a request field leaves a
  token bound to a different subject — the resulting `DENY_EXACT_BINDING` is correct behaviour, not
  over-blocking, so do not "fix" the product to satisfy the probe.
- **Loading a shipped test by name out of context.** `unittest.TestLoader().loadTestsFromName(name, module)`
  errors on a `TestCase` method, which looks like a product failure. Run it through the real runner with
  the SAME top-level the suite uses (cwd = the tests directory) and assert `exit_code == 0`. Never embed an
  in-process invocation's error into evidence as if the product failed.
- **A harness edited by script, then run unverified.** Programmatic edits to a harness reliably break it in
  ways that look like findings: a replaced block swallows the variable definitions that came after it
  (`NameError`), or a substituted dict literal loses its closing brace (`SyntaxError: '{' was never
  closed`). Compile immediately after every programmatic edit — `python -c "import py_compile;
  py_compile.compile('<f>', doraise=True)"` (or `ast.parse`) — and only then run it in the pipeline. When a
  patch targets a multi-line block, re-read the surrounding lines afterwards to confirm what you deleted.
  A harness that breaks mid-pipeline can leave a partially-written artifact behind, so treat these as
  release-blocking, not cosmetic.

When a probe expectation fails, ask first whether the assertion encoded the wrong *precedence* (expecting
an integrity code on a field the earlier exact-binding stage already rejects) or the wrong *fixture*
(asserting a P3-only code against a P2 request). A probe is guilty until proven innocent.

## L7 — a probe battery that builds fixtures from the implementation's own attribute names

A 19/19-green probe battery for a HumanGate repair passed while the product still had a **fail-open on a
canonical RUIN effect** and a dead risk-tier gate. The battery never caught it because every fixture was
built with the code's own (invented) field name — so it could only ever confirm the implementation's own
vocabulary. The canonical contract carried ruin inside the canonical effect-risk enum
(`LOW|MEDIUM|HIGH|CRITICAL|RUIN|UNKNOWN_RUIN`); the code read ruin from a `ruin_class` attribute that
appears **zero times** in the canonical source.

**Rule.** Build the first-failing fixtures from the **canonical field domains and enum values**, taken by
direct read of the source, never from the implementation's attribute names or its own tests. Before
claiming a gate is closed, grep the canonical source for every identifier the code treats as
authoritative; an identifier the source does not contain is a fidelity gap, not a convention. A probe
battery whose fixtures are derived from the code is self-confirming and has near-zero evidential value.

**Corollary — the subject of a rule matters as much as its field.** The canonical text attached the ruin
veto to the proposed consequential **effect edge**, not to a subject-level ruin label — so a P0/P1 read
over a ruin-class subject is admissible. A gate that vetoes on the subject label instead of the effect
edge is wrong in the opposite direction (over-blocking) and must be caught by a positive control. Every
gate repair needs both a negative battery and a low-risk positive control, or it will overfit into "token
for everything".

**Corollary 2 — a checker that contradicts you is the most valuable output.** When a fresh checker returns
PARTIAL on a blocking finding, verify that finding against the canonical source before accepting OR
dismissing it. It may be right, and it may have *understated* the severity.

**Corollary 3 — supersede a bad battery, do not delete it.** When a probe battery is found to be
self-confirming, mark it superseded with the reason and keep it, so the failure mode stays visible.

**Corollary 4 — fix one axis at a time and re-probe ALL axes.** Repairing an enum/classification
defect on three domains (risk tier, permission class, autonomy) left a fourth (operation) fail-open,
because the fix was scoped to the axes named in the report. When a defect class is "an unclassifiable
value must fail closed", sweep EVERY domain of that class in the same repair, and re-run the whole probe
set — not just the axis you touched.

## L13 — a receipt packaged inside the commit it describes (circular dependency)

A closure receipt asserted publication-state tokens (`..._COMMIT_PUBLISHED`, `READY_FOR_..._RECHALLENGE`)
while being packaged INSIDE the evidence commit those tokens refer to. The published commit therefore
contained a receipt that said `NOT_PUBLISHED` and withhold the very tokens the source-side artifact
claimed — a self-contradiction baked into the immutable subject. A related form: an artifact cannot name
its own commit SHA, because writing the SHA changes the commit; each regeneration moves the commit it
names.

**Rule — separate closure state from publication state by LOCATION.**
- The packaged closure receipt asserts **closure state only** (locally closed, independent check pass,
  baseline preserved, checkpoint bound). It is then publication-independent, so packaging it is safe.
- Publication-state tokens live in an **out-of-tree** publication receipt, written once AFTER the push.
  Recording them there cannot move the commit they name.
- An in-tree artifact that must reference its own commit should name the **branch**, with an explicit
  resolution rule ("the evidence commit is the TIP of <branch>"), and leave the literal 40-hex to the
  out-of-tree receipt.
- **Gate every claim token on the artifact that establishes it.** Derive `..._PUBLISHED` from the actual
  publication receipt (and require its remote-match flags) rather than emitting it because a gate set
  passed; move unestablished tokens into `non_claims` and surface them as `withheld` so the withholding
  is auditable.

**Do not chase bit-idempotence.** A pack that embeds `generated_at_utc` mints a new commit on every run;
that is not a defect. Publish ONE pair, verify its remote bytes, record the literals out-of-tree, and
state in the receipt that regenerating again would mint a new commit and is therefore not performed. An
idempotence check that "fails" here is a hypothesis about the artifact, not a product failure.

## L15 — a packaged copy that went stale because it was regenerated after the pack

A receipt was regenerated after the evidence pack had already committed it, so the published subject
carried the OLD revision while the working tree held the new one. Byte-level checks against the working
file pass; only a comparison against the COMMITTED blob reveals it.

**Rule.** Order the pipeline so the pack runs LAST over final artifacts, and never regenerate a packaged
artifact afterwards. For every packaged artifact, assert the committed blob hash equals the local file
hash (`git show <rev>:<path> | sha256sum` vs the file) — not merely that the file "exists" in the tree.
Anything genuinely post-publication goes out of tree.

**Two traps that make that comparison lie (both hit in one session):**

- **Compare BYTES, not decoded text.** Reading a committed blob through a text-mode capture applies
  newline translation, so the hash of the decoded string can never equal the on-disk file hash and every
  artifact falsely reports DIFFER. Use `git cat-file blob <rev>:<path>` with binary capture and hash that.
- **Verify the path resolves before trusting an "empty" result.** A `git -C <bad-relative-path> show`
  fails silently; its empty stdout then hashes to the **empty-file SHA** and looks exactly like a
  stale/missing artifact. Any time a comparison reports the empty-file hash or all-entries-differ, first
  assert the command itself succeeded (`git -C <abs-path> cat-file -e <rev>:<path>`) — a wall of identical
  mismatches is a harness bug, not a finding.

## L16 — a manifest/index digest of a raw log that binds the LOGICAL string, not the on-disk bytes

A regression index recorded `roots[].sha256/bytes` for every `ROOT_*.log`. The digest was computed over the
in-memory string (`sha256(log.encode())`) and the file was then written in TEXT mode (`open(path, "w")`).
On Windows text mode translates `\n` -> `\r\n`, so the on-disk bytes (and their sha) differed from the
recorded value on every line-ending. Content and counts were authentic and reproduced, but the digest did
NOT bind the stored file, so the index failed as tamper-evidence — a fresh checker flagged it
`EVIDENCE_GAP` even though nothing was wrong with the run.

**Rule.** Any manifest/index/Return-Pack digest of a raw artifact must hash the LITERAL bytes that land on
disk. Either write the artifact with `open(path, "w", encoding="utf-8", newline="")` (no translation) or
hash the file back with `open(path, "rb").read()` AFTER writing. Never record a digest computed over a
pre-write string when the write path can transform newlines. This is the WRITE-side twin of L15's
READ-side "compare bytes, not decoded text": bind bytes at both ends. Verify by recomputing every recorded
digest with `open(...,"rb")` and asserting a 0-mismatch count before packing.

## L17 — a manifest/Return-Pack pair that hashes each other (mutual recursion is not a fixed point)

A pack that hashes the manifest while the manifest ALSO lists the pack (and itself) can never satisfy all
three references at once: the manifest's SELF row records whatever bytes existed when it was walked (a
pre-write or PREVIOUS revision, e.g. claimed `51c69e8e…`/8569 bytes while the committed file is
`3608f54b…`/9274), and the pack's manifest hash goes stale the instant the pack embeds it. Both shipped as
"final" and a fresh checker flagged the manifest's internal linkage as an `EVIDENCE_GAP`.

**Rule — a strictly ordered, non-recursive publication DAG.**

- The MANIFEST hashes CHILD artifacts only. It MUST NOT list **itself** (its own hash changes the moment
  it is written — a generator run twice lists the previous revision) and MUST NOT list the artifact that
  hashes it (the Return Pack).
- The PREPUBLICATION Return Pack hashes the manifest (+ selected children) and carries an explicit
  non-final publication state (`PREPUBLICATION / assigned by publication receipt`); it MUST NOT embed the
  SHA of the commit that contains it.
- The POSTPUBLICATION readset (out-of-tree support commit) records the source SHA, the evidence commit
  SHA, Git blob IDs, and the **recomputed** sha256/bytes of BOTH the manifest and the pack.
- No artifact may be required to contain the final sha256 of bytes that include that same hash value, and
  no two artifacts may require mutually recursive final hashes.

Verify before freezing: `pack.manifest_sha256 == sha256(open(manifest,'rb').read())`; the manifest's item
list excludes both the manifest and the pack; every recorded digest recomputes from `open(...,'rb')` with
0 mismatches. Prefer a manifest that simply lists no self/pack row over one that tries to back-fill them.

## L14 — a probe that exercises a dimension with only one value

A permutation-invariance probe ran against a fixture whose set-valued field held a **single** element, so
reversing it was a no-op and the probe passed without testing anything. It looked like positive evidence
and would have been reported as proof of canonicalization.

**Rule.** An invariance probe must vary the dimension it claims to test: use **at least three** elements
before asserting that permutations produce identical canonical bytes, and assert the inputs actually
differ (e.g. that the permuted tuple really is reversed). Apply this to every "X must not depend on Y"
claim — if Y has one possible value in the fixture, the probe proves nothing.

## L18 — a DERIVED build artifact published inside the evidence set leaks the historical tokens you excluded elsewhere

An evidence-only recertification established the invariant "the superseded intermediate SHA appears ONLY in the typed
historical supersession map". A fresh checker falsified it: the compiler's rendered prompt had been copied into the
published bundle as an active file, and its mission prose quoted the intermediate SHA as a reconcile-target. A second,
independent defect in the same pass: the supersession map's `replacement_or_readback` named a file that does not exist
(a typo'd basename), so a reader following the map hit a dead end.

**Rule.** A published evidence set holds EVIDENCE, not build outputs.

- Keep DERIVED artifacts (compiled prompts, rendered docs, caches, `*_COMPILED/`) OUT of the published bundle. Their
  receipt is the evidence; the rendered bytes are reproducible from the contract. If a derived artifact must ship,
  classify it explicitly (e.g. `DERIVED_NOT_SUBJECT`) so a whole-tree stale-token sweep does not read it as an active
  claim.
- State invariants against the exact class they cover. "Stale SHA confined to typed historical fields" is false the
  moment a raw verification transcript or a reused historical log quotes that SHA while REVIEWING it — those are
  records of the review, not claims. Enumerate the permitted carriers (`typed historical field`, `raw verification
  record`, `reused raw historical transcript`) and require the invariant to hold over ACTIVE CLAIMS only.
- Every `replacement_or_readback`/`replacement_ref` in a supersession or lineage map MUST be asserted to resolve to a
  real file in the published tree before freezing. A dangling replacement is an `EVIDENCE_GAP`, not a cosmetic.
- A re-dispatched checker must be told it is round 2 and what round 1 found; a checker whose own artifacts are
  produced AFTER it verifies (transcript/findings/receipt) must be told that absence at verification time is by-design
  ordering, or it will re-raise the same `EVIDENCE_GAP` every round.

**Ordering note.** The checker's own transcript/findings/receipt are appended after verification, which changes the
manifest, the Return Pack's `manifest_sha256`, and the sanitation inventory. Rebuild that tail (manifest -> pack ->
final sanitation) after appending them, then re-sync the worktree — otherwise the committed subject carries a manifest
that no longer matches its own children.

## Compiling the order through the canonical prompt-contract compiler

The compiler enforces a contract far stricter than its published JSON Schema — deep enums for execution
disposition, runtime lifecycle, acceptance depth, evidence rerun rule, checkpoint field set, and
cross-edges such as "every capability, requirement, deliverable and journey needs an acceptance edge",
"exactly one reviewed entry per source family", and "maker must not equal checker".

- **Mirror the shipped clean-linting reference contract** and replace only its CONTENT. Hand-authoring
  from the JSON Schema fails with a hundred-plus errors.
- Read the compiler's JSON error report and **group by message** before fixing; the count collapses fast
  once you see the patterns.
- Check each subcommand's real signature (`<verb> --help`) before scripting it: some take an out-directory
  rather than an out-file, and a duplication check takes a source FILE and a rendered prompt, not a
  directory.
- `PROMPT_COMPILE_BLOCKED` is a stop state, not something to work around.

## Dispatching a fresh independent checker

The checker is the highest-value control, and it is only as good as its oracle and its output contract.

- Put the **canonical source above repo tests in the prompt**, explicitly, and require the checker to
  report any identifier the code treats as authoritative that the canonical source lacks.
- Require the checker to build fixtures from canonical domains, and to state the base-relative truth:
  which fail-opens reproduced at the stated base commit and which were already fixed there. A finding
  that "did not reproduce" at base is not a refutation if it reproduced at an earlier candidate.
- **Require the final message to be exactly one JSON object and nothing else.** A child can end with a
  malformed tool fragment instead of its verdict; an absent or malformed verdict is NOT a pass and must
  be re-dispatched, never inferred from the transcript.
- Persist the RAW transcript plus a structured receipt, and hash the transcript into the receipt. A
  summary receipt without the raw trace is insufficient.
- Local independent PASS is not external acceptance. Never let either the maker or the checker promote it.
- **A post-publication verifier is a SEPARATE read-only role from both the maker and the publisher.**
  Give it the manifest as ONE coherent object (source/evidence/PR/readset/receipts/descriptors) and
  require it to verify against committed bytes and remote state (`git cat-file blob`, `git ls-remote`),
  never against a receipt's own assertions.
- **Expect PARTIAL for coherence defects that are not enumerated gate failures, and FIX them rather than
  shipping.** A manifest can pass every check and still not be self-coherent. Re-dispatch after each fix
  and state what the previous round found — a verifier told only "confirm the fix" misses the next
  residue in the same class.
- **Fix the failure CLASS, not the files a report cites.** Name-based patching leaks the next family
  every round; classify by provenance-then-content (L9) and re-verify against the real directory listing,
  because over-relocating the current round's own artefacts is the same defect in the opposite direction.
