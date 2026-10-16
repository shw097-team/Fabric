# Final Evidence Re-seal + Binding (subject/evidence separation, verified 2026-08-14, EXT-FAR-TS-RE-001/002)

External focused re-review returned PARTIAL_CHALLENGE with **zero product defects** and two
evidence-identity blockers. This reference is the maker-side recipe for the
RESUME_SMALLEST_REPAIR = EVIDENCE_ONLY re-seal round (user's minimal-processing directive:
"不准改產品 / 不改 Swarm default-on / 不需重跑 103 tests").

## The two blocking defects (what external reviewers actually fail on)

- **RE-001 CONFIRMED_DEFECT (stale subject binding):** the post-change subject manifest
  INCLUDED a mutable evidence receipt (`FAR_HARDENING_SECURITY_CLOSURE.json`). When the
  closure receipt was regenerated (timestamp/digest fix), the subject manifest went stale —
  manifest said `5b70f74f…`, final bytes were `67fed618…`. Subject manifests must never
  include receipts that legitimately change during the evidence round.
- **RE-002 EVIDENCE_GAP (stale global evidence manifest):** the embedded evidence manifest
  was generated BEFORE the hardening subject froze → it bound pre-hardening hashes for
  `far_retrieval.py` / `far_trisource.py` / contract yamls. Any manifest generated before
  the final evidence bytes exist is automatically stale.

## The re-seal structure (single-direction, no loops)

```text
1. FAR_<X>_FINAL_SUBJECT_MANIFEST.json   — code/config/runtime-contract ONLY
   (modules, tests, templates, contract yamls). NO AO/security/rollback/evidence receipts.
   Digest S. Freeze AFTER product bytes are final.
2. FAR_<X>_FINAL_EVIDENCE_MANIFEST.json  — binds S + ALL final evidence digests
   (security closure, AO receipt, rollback receipt, compile receipt, test denominator,
   nodeids digest, canaries). Excludes the evidence MD itself (pre-self-row rule).
   Digest E. Generate AFTER every evidence byte exists.
3. FAR_<X>_EVIDENCE.md                    — embeds manifests + all raw content. Hash Z.
   (The MD references the intake by PATH only — never embeds the intake's hash.)
4. FAR_<X>_FINAL_INTAKE.json              — generated LAST (after the MD): ONE structure
   binding S + E + Z + every receipt digest + test denominator + canaries + r8 baseline
   + side-effect zeros. This is the single "final focused review intake" the external
   reviewer reads. Digest I. Single-direction: intake binds MD; MD references intake by
   path → no self-loop, no regeneration cascade.
```

Loop-breaker rule (repeat of the freeze-loop lesson, now at the binding level): if the
evidence MD embeds the manifest AND the manifest binds the MD's own hash, every
regeneration desyncs — the intake is the terminating binding, generated last.

## Drift check justifies skipping the test rerun

User directive allowed skipping the 103-test rerun **only if code/config hashes are
byte-identical to the frozen subject**. Do the comparison first and record it:

```python
for f in code_files:  # modules, tests, templates, contract yamls
    cur = sha(FAR / f); frozen = subject['files'][f]['sha256']
    assert cur == frozen, f"DRIFT {f}"
# drift == 0 → "NO test rerun required (r2 directive)" recorded in evidence
```

If ANY code/config file drifted, the no-rerun exemption dies — rerun the focused suite.

## Timestamp integrity (maker-side; reviewer catches this as CONFIRMED_DEFECT)

- Every receipt timestamp must be **timezone-aware UTC** via
  `datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')`.
- NEVER hardcode placeholder timestamps in canary/receipt scripts
  (`"retrieved_at": "2026-08-14T00:00:00Z"` was a real blocker: the evidence MD's §0
  generation time was EARLIER than the embedded "retrieved_at" → impossible chronology).
- NEVER write local time (+08:00) with a `Z` suffix — reviewer proved the
  "generated at 16:43Z but embeds 00:40Z" contradiction.
- Check before shipping: all `*_at_utc` / `retrieved_at` / `frozen_at_utc` values
  <= the evidence MD §0 generation time (monotonic event ordering).

## Evidence fidelity with async worker output

When a swarm/fanout canary's subagent results arrive as an async batch AFTER the receipt
was written: update the receipt to the workers' **verbatim** claims (read the full
subagent-summary file — live .log lines are truncated), add `note: claims = worker
verbatim output (deleg_<id>)`, regenerate the evidence MD, mirror ×4, and register a
SUPERSEDING EVD (`...-R2`/`-R3` — `register_evidence` is UNIQUE on id; never re-register
the same id). Summarized claims in evidence = fidelity gap the next reviewer will flag.

## Swarm default-on as a governed change (not an acceptance defect)

- A USER directive ("把 FAR 改成默認開啟 Swarm/多子代理") = a policy change, frozen as
  `USER_DECISION_<TOPIC>_<date>_001.md` (authority=USER, status=FROZEN, bound_into
  contract yamls + docs).
- Contract surface: `fanout.default_on: true` + allowed_shapes kept + max_lanes still
  WorkOrder-budget-bound + `canonical_parallel_writers=0` + merge_collision=DISPUTE +
  cancel_on preserved; route-check yaml gets a DEFAULT_ON note; README table row.
- External reviewers ACCEPT the user decision and only check its safety invariants
  (read-only workers, no parallel canonical writers, no self-accept, budget bounded,
  no SQS/live authority expansion) — document those invariants in the canary receipt.
- Prove it with a REAL fanout canary: `delegate_task` two parallel leaf workers
  (SOURCE_FAMILY_SPLIT: one local-KB lane + one web lane), capture worker ids, durations,
  read_only flags, merge info (independent_families, collision=NONE), `fired_at_utc`.

## Checklist before handing to external focused re-read

- [ ] subject manifest = code/config only; every listed hash == current bytes (drift=0)
- [ ] final evidence manifest generated after ALL evidence bytes; digest recomputable
- [ ] final intake binds subject + EM + MD + receipts + denominator + canaries, generated LAST
- [ ] timestamps: all UTC, none in the future relative to MD §0
- [ ] evidence MD mirrored ×4 byte-identical; superseding EVDs registered for changed files
- [ ] worker-verbatim claims in canary receipts

## Master single-evidence-MD consolidation (user: "把全部驗收官所需的證據全部彙整成單一MD證據檔", verified 2026-08-14)

When the user asks for ONE MD holding everything the external reviewer needs, generate a
SUPERSEDING master MD (e.g. `FAR_FINAL_HARDENING_ACCEPTANCE_EVIDENCE.md`) instead of
pointing at scattered receipts. Master section layout that satisfied the r3 reviewer:

```text
§0 claim ceiling + supersession note (which focused MD/receipts it replaces)
§1 execution summary (C0-C8 + every external finding round + closure)
§2 final intake binding table (embedded intake MINUS self-binding fields — see below)
§3 spine readback (WO/RB/EVD rows)   §4 C0 change-input manifest full
§5 FIT-GAP full                      §6 compile gate receipt full
§7 user decision(s) full (e.g. swarm default-on) + contract diff
§8 D-decisions full                  §9 candidate subject manifest full
§10 final evidence manifest full     §11 security closure full
§12 AO receipt full                  §13 rollback receipt full
§14 ExecutionBinding full
§15 test evidence: denominator JSON + FULL nodeid list + real merged stdout + exit code
§16 canaries: every canary JSON full (incl. swarm fanout receipt with verbatim claims)
§17 historical baseline record full (r8)      §18 evidence identity (ALL SHA-256)
§19 verification guide (what the reviewer can independently recompute) → STOP
```

Key mechanics:
- **The master embeds the intake minus its self-binding fields.** The on-disk intake
  binds the master MD's hash; if the MD also embedded that binding, regeneration would
  loop. Embed `{k: v for k, v in intake.items() if k != 'frozen_at_utc'}` with
  `mutual_binding` stripped of `final_evidence_md`, and add a §2 note that the
  authoritative MD hash lives in the on-disk intake (single direction).
- **Rebind the intake AFTER creating the master**: the intake was generated for the
  earlier focused MD; regenerate it with `final_evidence_md = {sha256: <master sha>,
  bytes, file: <master name>}` + fresh `frozen_at_utc`, then mirror BOTH (master + intake)
  ×4 and register superseding EVDs (`...-V6`/`-R2` pattern). Only the intake's
  MD-binding changes; the embedded (stripped) copy in the MD stays valid.
- Generate the master with a generator script (read actual files via `body()`), verify
  `FFFD=0` + CJK counts + section presence, mirror, then hash from `read_bytes()`
  (write_text on Windows converts LF→CRLF, so `len(md.encode())` ≠ on-disk size).

## Accepted-MD immutability under NBOs (verified r3 acceptance, 2026-08-14)

After the external reviewer issues PASS_CHALLENGE on a master MD, their NBOs (e.g.
"§18 contains a stale intake-file SHA", "canary field naming imperfect") are
**archival/schema-quality only** — do NOT regenerate the accepted MD to fix them.
Regeneration changes the hash → breaks the intake binding → forces a re-seal + new
external round. The reviewer explicitly says "no re-seal required" for NBOs. Correct
handling: fix cheap wording in receipts/docs only if it doesn't touch the accepted MD
or the intake binding; otherwise note the NBO in the activation record / next ChangeSet.
Do not touch the signed identity.

## Activation close-out round (user: "驗收完成，正式啟用新版…更新使用手冊/AGENTS.md/TEAM.md/README…更新路由和設置…整理目錄樹")

After external acceptance, the user's activation directive has a fixed shape:

1. **Activation receipt** (`FAR_ACTIVATION_RECEIPT_v3.json` style): schema with
   event=FAR_V<n>_FORMAL_ACTIVATION, authority_basis (external report id + verdict +
   master evidence + intake + subject/EM digests + test denominator), activated list
   (each capability ACTIVE incl. new defaults), docs_updated list, claim ceiling
   (production/sqs/remote NOT + side-effect zeros + human gate preserved).
2. **Docs sweep**: README status header, TEAM.md Status section, AGENTS.md file map,
   User Guide execution section — all updated to the LATEST external verdict (include
   the new default posture, e.g. Swarm DEFAULT-ON with the USER_DECISION id).
3. **FABRIC routing update** (視情況): the router's canonical input
   (`FAR_CAPABILITY_MATRIX.yaml`) gets a new execution-class row for the changed
   posture (e.g. `hermes-swarm: state ACTIVE_DEFAULT, role DEFAULT_PARALLEL_RESEARCH_PATH,
   max_lanes=WO budget, canonical_parallel_writers=0, merge_collision=DISPUTE,
   single_thread_still_legal=true`) — the router must reflect the accepted change.
4. **Directory tree deliverable**: `FAR_DIRECTORY_TREE.txt` (245 lines; `find … |
   sort` or `tree`) + a subdir breakdown (canary/evidence-bundle/methods/
   research-product/tests/docs) in the final report.
5. Register EVD for the activation receipt; keep claim ceiling unchanged.
