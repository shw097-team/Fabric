# FAR-LANE-REMEDIATION-20261021 — session closure and handover

**Control plane:** HG-KSEOS (sole). **Runtime/Orchestration:** the canonical Hermes profile.
**Rounds:** `FAR-REMEDIATION-20261021` (epoch 23) → `FAR-CLOSURE-20261021` (epoch 24) →
`FAR-CLOSURE-20261021-R2` (transport vocabulary + checker tooling) →
`FAR-CLOSURE-20261021-R3` (land the untracked runtime so a clean checkout can rebuild the contract).
**HG-KSEOS commits:** `c442f07` → `5d63e00` → `248eda9` → `051d574`.
**Fabric branch:** `pub/far-lane-remediation-20261021` at `cf93dab` (published, not merged).

## The one-paragraph version

The declared route was correct on paper and un-runnable in practice. The pool carries **two**
identities per entry — the **governance identity** (`provider`/`model`, what `check_drift()` and the
receipt gate compare) and the **transport vocabulary** (`transport_model`, the string actually handed
to the Codex-CLI transport) — and the transport vocabulary is **per-provider**. The openai arm
requires the **bare** id; the pool carried the qualified `openai-codex/gpt-6.1-sol`, which the relay
routes to the *default* provider and answers `HTTP 400 Model is unavailable`. Measured on the live
relay: bare → 200, `openai/gpt-6.1-sol` → 200, qualified → 400. That is the whole mechanism behind
"gpt-6.1-sol sometimes works": it worked whenever the id reached the backend bare and failed whenever
a provider-qualified spelling was used. Three other defects sat alongside it (a cross-field
contradiction `check_drift()` structurally cannot see, registry internal residue describing revision
17/22, and a PROBE arm sitting where a dispatch could read it as a policy default). All four are
closed at epoch 24, and the independent AO lane re-derived 10/10 claims → `VERDICT: PASS` with the
digest guard reporting 520/520 governed files unchanged.

## What is closed (and by what evidence)

| # | Defect | Closed by | Evidence |
|---|---|---|---|
| F1 | `sod.verify_security_arm_A` restated a superseded deepseek arm while `lane_chains.VERIFY_SECURITY[0]` was gpt-6.1-sol — invisible to `check_drift()`, which compares each binding only against its own pointer target | field realigned; new named gate `C15_crossfield_arm_A` | `var/FAR-CLOSURE-20261021/apply_receipt.json` |
| F2/F3/F4 | registry internal residue: `authorization_basis` said revision 17, `selected_arm_identity` named deepseek-v4.1-flash, the projection note described revision 22 / PLAN=glm | all three restated at epoch 24 | same receipt |
| F5 | a measured PROBE arm (minimax) sat where an unpinned dispatch could pick it and read it as a policy default | labelled `PROBE/探測`, `automatic_selection: false`; gate `C16_probe_not_auto` | same receipt |
| F6 | the change checklist did not reflect the receipts that exist | reconciled; the AO item was recorded as NOT OBTAINED rather than silently ticked | `openspec/.../tasks.md` |
| F7 | `AGENTS.md` pointed at the superseded SoD conflict (C2) and source revision 18 | now C4 and revision 24 | `AGENTS.md` |
| G8 | the openai arm's transport vocabulary was qualified, not bare → the declared GPT 6.1 SOL-MEDIUM arm was structurally un-runnable | bare transport id for PLAN#1, VERIFY_SECURITY#1, EXECUTE#2; a conformance test fails if any `openai-codex` entry is qualified | `var/FAR-CLOSURE-20261021-R2/apply_receipt.json`; `pool.transport_vocabulary` |
| G9 | a checker lane could not re-derive a test-suite result: the host shell exports `TMPDIR=/tmp` (an MSYS virtual path a native Windows child cannot use), so `tempfile.mkdtemp` failed | the dispatcher hands the child a Windows-usable scratch root as `TMPDIR`/`TEMP`/`TMP`, plus `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` | `scripts/hgk-lane-dispatch.py`; `lane_receipts/VERIFY_acceptance.json` |
| G10 | the published contract was **not reproducible from the repository**: this round committed the tests and the dispatcher while the modules they import (`hg_kseos.lane_policy`, `lane_admission`, `lane_route_resolver`, `role_binding`) were untracked — a clean worktree at HEAD raised `ImportError` and the suite aborted during collection | the measured closure landed in commit `051d574`; the closure was re-derived against `git ls-files`, so nothing pulls in an untracked dependency | `evidence/apply_receipt_r3.json`; `lane_receipts/AO_landing2.json` (AO extracted the tree with `git archive HEAD` and got `IMPORTS_OK` + `5 passed, 90 subtests passed` from the committed bytes alone) |

## Verification actually performed (and by whom)

- `check_drift(registry=load_registry())` → `[]`
- `pytest tests/test_lane_policy.py -q` → **5 passed, 90 subtests passed**
- `openspec validate far-lane-remediation-20261021 --strict` → valid
- self-check harness → **GATE_PASS 20/20**
- **Independent AO lane** (`openai-codex/gpt-6.1-sol`, Codex CLI, escalated `read-only` →
  `workspace-write` under explicit authorisation with a digest guard over `config/`, `tests/`,
  `src/`, `openspec/`, `AGENTS.md`, `README.md`) → **VERDICT: PASS, 10/10 claims**, guard verdict
  **CLEAN** (520/520 governed files unchanged). Receipt:
  `lane_receipts/VERIFY_acceptance.json`.
- **External-acceptor simulation** (fresh clone of the published branch, every blob read from the
  remote commit object store and its sha256 recomputed) → **36/36 files match**, 0 mismatches,
  0 absent, 0 secret findings.

## What is NOT closed — do not read this round as "done"

1. **Model-axis independence between PLAN and VERIFY_SECURITY is ABSENT.** Both are
   `openai-codex/gpt-6.1-sol` **by owner order** (2026-10-21), declared as
   `SOD006-C4 OPEN_OWNER_ORDERED`. Only *process* separation is claimed. EXECUTE
   (`deepseek-v4.1-flash`) and VERIFY (`gpt-6.1-sol`) remain model-distinct. Closing the PLAN/VERIFY
   gap is an **owner decision**, not an engineering task. Ledger row `K-26 OWNER`.
2. **The relay's model catalogue is a stale snapshot.** The ChatGPT OAuth backend listed 9 models
   including `gpt-6.1-sol` and `gpt-6-sol`; the relay catalogue holds 92 entries with no 6.x, and its
   `models_cache.json` records `fetched_at = 2000-01-01`, `client_version = 0.0.0`. The lane works
   because the bare id is forwarded verbatim — **not** because the catalogue is current. A catalogue
   refresh is an open item outside the epoch-24 contract change. Ledger row `K-25 PARTIAL`.
3. **The openai-codex upstream's availability is not under local control.** Its quota showed 31%
   weekly used with an unexpired credential while requests still failed with
   `Model is unavailable`; the transport-vocabulary repair is what made the arm usable, but upstream
   catalogue drift and availability remain outside the local contract.
4. **No acceptance, no release, no promotion.** The AO's own receipt states that a pass "is not an
   acceptance of any subject". The Fabric packet is `CANDIDATE_ONLY`; the branch is published for
   external acceptance and is **not merged**.
5. **The COMMITTED `config/hermes.json` is stale.** It still names the `var/hermes-v020` isolated
   home and `deepseek-v4-flash`, so the committed tree carries three `PROJECTION_DEBT` warnings
   that the working tree does not. The corrected binding exists only as an **uncommitted** edit
   from an earlier session; it was deliberately NOT landed because it is an out-of-scope rewrite
   that also repoints `executable` at the `hermes.exe` trampoline. Ledger row `K-27`/`K-28`.
6. **300+ untracked candidate entries remain** in the HG-KSEOS working tree; the nine files this
   round's tests and dispatcher actually depend on are landed, the rest needs a per-item
   disposition. Ledger row `K-29`.
7. **The Hermes *session* model and the *lane* models are two different planes and were kept
   separate throughout.** The interactive session's provider pin says nothing about what the PLAN
   lane is bound to; every lane model claim in this packet comes from the pool's governance
   identity and was exercised through `scripts/hgk-lane-dispatch.py`.

## Handover — how to pick this up

- **To re-verify the route contract:** `python scripts/hgk-lane-dispatch.py --lane VERIFY_SECURITY
  --require-arm openai-codex/gpt-6.1-sol --codex-executable <pinned codex.exe> --pool
  config/lane-route-slots.candidate.json` and read the receipt's `served_arm`, `used_transport_model`,
  `usage_receipt_ok` and `subject_mutation.verdict`.
- **To re-run the local gate:** `./.venv/Scripts/python.exe var/FAR-REMEDIATION-20261021/selfcheck.py`
  and `./.venv/Scripts/python.exe -m pytest tests/test_lane_policy.py -q`.
- **To check for drift:** `./.venv/Scripts/python.exe -c "import sys;sys.path.insert(0,'src');from
  hg_kseos import lane_policy as lp;print(lp.check_drift(registry=lp.load_registry()))"`.
- **To change a route:** edit `config/model-lane-assignment.json` + `config/lane-routing-registry.yaml`
  **together** and advance the epoch; `check_drift` compares the registry's projection expectations
  against the assignment, so bumping one without the other produces `DRIFT_VALUE` rows.
- **To change a lane's transport spelling:** read `config/lane-route-slots.candidate.json`'s
  `transport_vocabulary` block first. The rule is per-provider and it is enforced by a test.
- **Kanban board:** `far-remediation-20261021` — 16/16 cards `done`, each carrying the receipt that
  closed it. **OpenSpec change:** `far-lane-remediation-20261021` (epoch 23 → 24).
- **Fabric ledger:** `INTEGRATION/KNOWN-FINDINGS.md` rows K-21 … K-26.
