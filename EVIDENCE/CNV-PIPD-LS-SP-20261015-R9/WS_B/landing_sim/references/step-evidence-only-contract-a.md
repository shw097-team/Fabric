## External-challenge evidence closure (EVIDENCE_ONLY Contract A — learned 2026-08-12)

External reviewers fail blocking findings on **missing digests and missing raw
receipts**, not on substance. A `PARTIAL_CHALLENGE` with `EVIDENCE_GAP`
findings is a resume-smallest-repair, NOT a rebuild:

- Compile a **SEPARATE `EVIDENCE_ONLY` compiler contract** — never merge it into
  the next stage's UPGRADE contract. Same lint/activation/acceptance PASS
  requirement. Terminal = `PENDING_STAGE1_EXTERNAL_META_ACCEPTANCE`; do NOT
  seal; do NOT enter the next stage; do NOT rerun full gates unless fresh
  invalidation proves a specific edge stale.
- Close each finding with a `CLOSURE_<FINDING_ID>.json`: finding id,
  classification, status CLOSED, smallest_repair, focused_retest predicates
  (parse / row counts / unique IDs / required fields / **SHA-256 from final
  bytes**), bound_into list, verdict.
- Every blocking evidence artifact must carry a SHA-256 in the review MD raw
  index. Missing digest == external FAIL.
- Raw receipts must be delivered as **BODIES** (checker identity, subject
  binding, predicates, denominator, pass/fail counts, every pass:false item +
  note, isolation/no-write), not hash+summary. Hash-only is itself a finding.
- **FREEZE ORDER (the drift bug):** re-running any generator/checker AFTER the review
  MD was generated silently desyncs the embedded hash from the artifact bytes
  (observed: review MD embedded `fab4b137…` while the file was
  `e4401149…`). Order: freeze ALL mutable artifacts → regenerate review MD LAST
  → mirror → hash → freeze. Re-generate once more after the final checkpoint write.
- **MANIFEST-BEFORE-SUBJECT (inverse freeze bug, verified PCIV-F01 2026-08-13):** a
  package/receipt manifest generated BEFORE a subject artifact's final bytes causes a
  stale internal cross-reference: `FINAL_PACKAGE_MANIFEST.yaml` (01:29) embedded
  `E2_BEHAVIOR_SUBJECT_SELECTION.yaml` = `fe824e17…` while the file's final bytes
  (01:36) were `d4f93610…`; the accepted final review MD (02:11, generated after)
  correctly recorded `d4f93610…`. Detection predicate: re-verify every manifest
  internal entry hash against current bytes (12/13 matched, 1 stale). Classification:
  current package-manifest internal staleness — historical accepted manifest/review MD
  PRESERVED, only the current edge invalidated; smallest repair = regenerate manifest
  entry to current bytes as a NEW superseding manifest, never rewrite 68867e08-style
  accepted hashes.
- **SINGLE-DIRECTION hash binding:** the outer index (review MD) hashes every
  inner artifact; inner artifacts (RESUME_CHECKPOINT) reference the MD by PATH
  ONLY. Two artifacts embedding each other's hashes = self-referential loop
  that breaks on any edit.
- Preserve pointer-file semantics: a `*_REF.yaml` pointer file's own hash and
  the referenced artifact's content digest are distinct fields by design — a
  checker predicate requiring them to match is wrong (MASTER_REF case).

Full recipe + observed drift case: `references/external-evidence-closure.md`.

**FDA-round extensions (verified 2026-08-13, EXT-FDA-001..008 closure):** external
reviewers fail on (1) no exact frozen subject root, (2) pointer-rich MD without raw
bytes, (3) checker-denominator conflicts, (4) self-contradictory DoD pass-lists,
(5) runtime gates left BLOCKED when a no-key path existed. Closures:
- **Subject root = git commit.** `git add <all FDA artifacts> && git commit` →
  `git rev-parse HEAD` is the recomputable identity; two-commit model (artifacts →
  EvidenceManifest+bundle) avoids the MD-embeds-own-HEAD loop.
- **Raw review bundle + EvidenceManifest:** byte-copy every artifact into
  `evidence/review/FDA_RAW_REVIEW_BUNDLE/`; manifest binds path+sha256+size +
  subject_root + fresh checker/tests runs + DoD-36 matrix, generated LAST.
- **Checker denominator:** one current fresh-run value everywhere (126→144→146 as
  receipts grew); never reuse a stale freeze number.
- **DoD-36 machine matrix:** full 36 rows, no omitted IDs (21/22/25 were dropped in
  one pass), PASS/PARTIAL/BLOCKED mutually consistent (a "1–16 PASS" line alongside
  "UFO2 BLOCKED" is a confirmed defect).
- **UFO² effective-load does NOT require an external API key** (over-conservative
  BLOCKED_HITL corrected): Ollama local (`API_KEY:"ollama"` placeholder), custom
  `BaseService`, or `PlaceHolderService` all work keyless; verified 7/7 via
  opencode-go backend (Hermes dotenv credential, in-memory only). urllib to
  opencode.ai → HTTP 403 code 1010 (Cloudflare block); the OpenAI SDK works.

Full recipe + generator pitfalls: `references/external-challenge-review-closure.md`.

**Focused RE-REVIEW repair (verified 2026-08-14):** FAIL = deterministic CONTRADICTIONS inside
submitted evidence. Track A (normalization): rewrite evidence MD fresh (write_file not patch), ONE
current value per truth, label old counts SUPERSEDED_PRE_<PATCH>, grep stale tokens → 0.
Track B (rebind order): freeze HEAD → receipts → tests → fresh checker → SubjectManifest →
EvidenceManifest (rehash bundle bytes) → render final MD LAST → mirror → readback → submit.
HARD: never append ChangeSet after manifest regeneration. Identity trap: claimed file+hash MUST
equal received bytes. Full: `references/external-rereview-normalization-rebind.md`.
