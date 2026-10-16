# WS-F RECEIPT — OpenSpec change proposal `hgk-r8-eia-closure-skill-slim-20261016`

Round `CNV-PIPD-LS-SP-20261015` / ChangeSet `R8-0` · HGK project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`
Producer: PLAN-plane sub-agent (`gpt-6.1-sol`, delegation `deleg_c746bb64` task 0)
Final write performed by the in-Hermes orchestrator after the owner's explicit authorization
(2026-10-16: *"授權我以既有治理機制（fda_guard_mint.py，USER 範圍、TTL 3600s）開一次受限授權"* + *"用戶追加授權你FDA的權限(若需要)"*).
The sub-agent's own write of this receipt was refused by the pre-tool guard; the evidence below is byte-verified
by the orchestrator, not copied from a summary.

## 1. Artifacts (bytes + sha256, measured on disk by the orchestrator)
| path | bytes | sha256 |
|---|---|---|
| `.openspec.yaml` | 40 | `9cfa2ab963a8c9b5…` |
| `proposal.md` | 5,382 | `a6b06b68a69a171b…` |
| `tasks.md` | 9,623 | `088aadcae9527962…` |
| `design.md` | 14,363 | `5ac85548f4f10137…` |
| `specs/r8-eia-closure-and-skill-slim-regression/spec.md` | 12,342 | `7bcee9f48b0310e1…` |
| `WS_F/OPENSPEC_STATUS.json` (CLI resolution evidence) | 3,327 | `279d7425e4bca714…` |
| `WS_F/OPENSPEC_VALIDATE_STRICT.log` | 57 | `858f1e7382b9c587…` |

Change root: `C:/Projects/Agent_Workspace/HG-KSEOS/openspec/changes/hgk-r8-eia-closure-skill-slim-20261016/`

## 2. Validation
```
$ npx openspec validate hgk-r8-eia-closure-skill-slim-20261016 --type change --strict
Change 'hgk-r8-eia-closure-skill-slim-20261016' is valid
```
Exit 0. Raw log: `WS_F/OPENSPEC_VALIDATE_STRICT.log`.

## 3. Content verified by the orchestrator (not taken from the summary)
- 5 capability groups: A skill-slim gate + guarded apply · B validator rebase on `main` + 18-mutation re-measurement ·
  C checker isolation evidence + owner-gated deployment · D nine-finding reconciliation + versioned publication errata ·
  E claim ceilings and owner gates.
- Counts by direct parse: **7 requirements · 20 scenarios · 22 unchecked tasks (0 checked)** → proposal only, zero implementation.
- The spec's A-group encodes the two rules this round actually relies on: the 60-reference threshold stays a **WARNING**
  (never a hard gate), and a >60 or over-cap condition may not be "fixed" by raising the cap or by shipping cache files to
  manufacture equality.
- Group C records the structural finding that a single shared Windows identity cannot separate maker from checker.
- Group E names the owner/authority prerequisites instead of inventing substitute authority.

## 4. Observations carried forward from this turn
1. The R8 regression/verification receipts written this round bind `subject_live` inconsistently between the
   orchestrator's post-apply re-run and the maker's own runs; the openspec proposal records the inconsistency rather
   than smoothing it. (Resolved for the applied skill by `WS_A/WS_A_INDEPENDENT_RECHECK.json`, which states its
   subject/live pair explicitly.)
2. The scratch deny-ACE proof (WS-C) demonstrates the mechanism on a scratch directory only; it does **not** show the
   guarded root is protected. The proposal keeps the ACL change proposal-only and owner-gated, which matches that limit.

## 5. Non-claims
This is a **proposal**. No product code, no control-plane/spine/config change, no ACL applied, no Gate PASS, no
acceptance, no approval. Claim ceiling **LOCAL / candidate-only**.
