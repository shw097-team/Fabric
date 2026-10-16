# WS1 — measured inventory of every open openspec change record (HG-KSEOS)

Measured **2026-10-16 14:27–14:55 (+08:00)** by the R11 FAR ws1 read-only worker.
Claim ceiling: **`LOCAL / candidate-only`** — nothing in this report is an acceptance,
a Gate PASS, a release, or a claim about product behaviour.

- Subject set: every record under `C:/Projects/Agent_Workspace/HG-KSEOS/openspec/changes/**`
  except `archive/` → **25 records** (a 25th, `hgk-round3-lane-rebind-20261016`, was created
  mid-session by a peer round at ~14:30 and is included).
- Toolchain: **available** — `npx --no-install openspec --version` → `1.8.0` (exit 0).
  Every record was validated with the real CLI; there are **no** `NOT_MEASURED` rows.
- Delivered files: `raw_measurements.json` (commands + raw output incl. verbatim
  `validate_raw.txt` content), `open_records_inventory.tsv` (25 rows), this report.
- Nothing under `openspec/` was modified; all writes stayed inside `.../R11/FAR/ws1/`.

## Method (one line per measurement)

| Measurement | How |
|---|---|
| (a) checked vs unchecked rows | `grep -cE '^- \\[ |^- \\[[xX]\\]' tasks.md` per record |
| (b) spec.md exists | filesystem walk for any `spec.md` in the record |
| (c) newest mtime | `find <record> -type f` sorted by mtime, head -1 |
| (d) strict validation | `cd ...openspec && npx --no-install openspec validate <name> --strict`, raw output kept (`validate_raw.txt`); exit-codes 0/1, plus a positive/negative control re-run |
| (e) live-execution evidence | read-only inspection of `HG-KSEOS/var/*`, `_handover/CNV-PIPD-LS-SP-20261015{,-R7..R11}/*`, the Hermes skills tree, and the Shared Spine `projects` table |

## Headline counts

- Rows: **25** · tasks rows: 223 checked / 364 unchecked.
- `spec.md` present: **23/25** (absent: `hgk-plan-plane-rebind-20261015`,
  `sod-independent-verify-enforcement` — both fail `--strict` for no deltas).
- `openspec validate --strict`: **23 PASS / 2 FAIL** (the two records above; raw error
  text is in `validate_raw.txt`).
- Live-execution evidence exists elsewhere on disk for the mission-referenced records:
  YES for every R6..R11 peer record (see TSV `live_evidence` column with exact roots);
  the two `20261015` lane-change records' work is live via `var/FAR-LANE-ROUTE-REBIND-20261015/`
  and the canonical registry (epoch 22), even though their own records were never ticked.

## Dispositions

| disposition | count | records |
|---|---|---|
| CLOSE_CANDIDATE | **7** | hgk-far-remediation-20261016, hgk-lane-brief-and-guard-hardening-20261015, hgk-r9-far-residual-closure-20261016, hgk-round3-lane-rebind-20261016, hgk-skill-convergence-20261014, lane-health-repair-20261011, lane-model-chain-rebind-20261015 |
| CONTINUE | **9** | gcm-noninteractive-default-containment, hgk-checker-upgrade-adapter, hgk-lane-reliability-closure-20261016, hgk-r10-session-closure-20261016, hgk-r11-session-handover-20261016, lane-supervisor-windowless-convergence, lane-toolchain-identity-and-failure-classification, strict-declaration-20261011, verification-artifact-contract |
| OWNER_DECISION | **5** | hgk-plan-plane-rebind-20261015, hgk-r8-eia-closure-skill-slim-20261016, lane-mandate-rebinding-and-d01-revocation, sod-independent-verify-enforcement, skill-mainfile-cap-remediation |
| HISTORICAL | **4** | hermes-incident-2026-10-05-repair, lane-sod-enforcement, lane-verify-dual-routing-and-plan-high, lane-verify-routing-remediation |

## The 5 most important facts a new session must know

1. **Stale records are the norm, not the exception — measure, never trust a checkbox.**
   Seven records are CLOSE_CANDIDATE: their work exists measurably on disk
   (`HG-KSEOS/var/<round>/`, `_handover/...R8/R9`, the live registry at epoch 22) while the
   record itself stays unticked. The worst single miss: `lane-model-chain-rebind-20261015`
   (13 open rows, every row executed at epoch 18 with receipts) and
   `hgk-far-remediation-20261016` (25 open rows executed by the peer round that produced
   `var/FAR-REMEDIATION-AND-CLOSURE-20261016/`, Gate G1–G7 all ok, Fabric PR #8 open).
   One action per row is already in the TSV `one_action` column — the close path is a
   tick-with-citation, not new work.

2. **The registry is at epoch 22 and the SoD picture has moved: PLAN/VERIFY are now distinct
   (required) while EXECUTE and VERIFY/SECURITY are deliberately the same model
   (`opencode-go/deepseek-v4.1-flash`), declared as `SOD006-C3 = OWNER_ORDERED_IN_FORCE`.**
   Any new record that still talks about PLAN=`gpt-6.1-sol` or "checker must differ from
   writer" without the C3 declaration is referring to a registry state that no longer
   exists (three records are in exactly that state — see TSV notes for
   `lane-mandate-rebinding-and-d01-revocation`, `lane-verify-dual-routing-and-plan-high`,
   `hgk-plan-plane-rebind-20261015`).

3. **Two records fail `--strict` and both are the same trivial cause**: no `specs/<capability>/spec.md`
   with delta headers (`hgk-plan-plane-rebind-20261015`, `sod-independent-verify-enforcement`).
   Neither is a product defect; `sod-independent-verify-enforcement`'s two open rows are
   explicit owner gates (canonical S1* apply, subject_digest migration) and should be
   OWNER_DECISION'd, not built. Fix by setting `skip_specs: true` or authoring deltas in a
   successor record — do not edit these records' proposal text.

4. **Record scope vs mission scope must be separated before closing anything.**
   `hgk-r10-session-closure-20261016` is CONTINUE, not historical: its row 5.2/5.3
   (push + Draft PR, prepared via `publish_r10.py`) is the *newest deliverable the external
   acceptance officer has never seen*, and its row 6.1a VERIFY lane fail-closed with
   `ERR_LANE_REQUIRED_ARM_ABSENT` (recorded, not bypassed). Conversely the four HISTORICAL
   records predate the convergence mission and their subjects are already covered by newer
   rounds — archive them without executing any row.

5. **The R11 record (`hgk-r11-session-handover-20261016`) is the live spine of this session**
   — rows 2.1/2.3/3.3 are the WS inventory that produced this very deliverable, and its
   remaining rows are (4.2) an independent VERIFY lane on the mandate's arm, (4.3) close/
   continue classification, and (5.1–5.4) publication with a byte-by-byte remote readback.
   The mandate's arm per owner order 2026-10-16 is VERIFY = `opencode-go/deepseek-v4.1-flash`
   (same model as the writer, disclosed as `SOD006-C3`); a dispatch on the R10-era rank-1
   `gpt-6.1-sol` pin would be a record defect, not a registry truth.
