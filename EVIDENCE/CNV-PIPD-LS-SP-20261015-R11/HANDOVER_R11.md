# HANDOVER R11 — SESSION closure & handover for mission `CNV-PIPD-LS-SP-20261015`

**Read this file top to bottom before doing anything else.** It is written for a NEW session that has no memory
of the conversation that produced it. Claim ceiling: **`LOCAL / candidate-only`** — nothing here is an
acceptance, a Gate PASS, an AO verdict or a release.

Generated: 2026-10-16 (UTC+8 host) by round **R11-0** (`ChangeSet R11-0-SESSION-HANDOVER`, HGK project
`CNV-R11-HANDOVER`). Predecessor handover: `../CNV-PIPD-LS-SP-20261015-R10/HANDOVER_R10.md`.

---

## 0. The 60-second orientation

You are inside the **HG-KSEOS / Fabric convergence mission**. `HG-KSEOS` is the control plane; the canonical
Hermes runtime is bound to it as the governed Runtime/Orchestration Plane; `Fabric` is the repo where each round
publishes a candidate-evidence packet for an **external** acceptance officer. Ten rounds (R6..R10) have been
executed and published. This round (R11) does **not** build product: it closes the session so you can continue.

**What "continue" means in practice**: pick an item from §5 (each has ONE next action), run it, keep the claim
ceiling, publish the evidence. Nothing is blocked on missing information — the blockers are human decisions and
external gates, and they are listed as such.

---

## 1. Anchors (authority) — do not re-derive, do not supersede

| Role | Path | Measure |
|---|---|---|
| **SOLE AUTHORITY**: the package | `<HERMES_HOME>/attachments/Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG.md` | v2.0.0, 2,689,181 bytes, sha256 `96d9d564…cff9c3f` |
| Independent acceptance report | `<HERMES_HOME>/attachments/Fabric_Convergence_External_Independent_Acceptance_Report_20261015.md` | `scope_verdict: PARTIAL_CHALLENGE`, `production_decision: FAIL_CLOSED`, `merge_decision: CONDITIONAL_APPROVE_AFTER_MINIMAL_METADATA_AND_SCOPE_CHECKS` |
| Governing rules | `C:/Projects/Agent_Workspace/HG-KSEOS/AGENTS.md` | control-plane rules |
| Claim ceiling | — | `LOCAL / candidate-only`, in every round |

`<HERMES_HOME>` = `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes`
(**MSIX path** — the plain `.../Local/hermes` path is a different, wrong place).

Six older blueprints were demoted to `STATE_EVIDENCE`-only by owner decision; the package above is the only
authority. Do not resurrect them as requirements.

---

## 2. Where everything lives

- **Round roots (all artefacts, evidence, briefs, ledgers)**
  `C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015` (R6/R7) and `…-R8`, `…-R9`, `…-R10`, `…-R11`.
- **GUARD SUBJECT — hands off, byte-verbatim**: `…/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/`
  (300 files). No round writes there; checkers never write there.
- **Control plane**: `C:/Projects/Agent_Workspace/HG-KSEOS/`
  - shared spine DB `var/shared-spine/hg-kseos.db`
  - lane routing **registry** `config/lane-routing-registry.yaml` — **UNTRACKED local state, not versioned**
  - lane **slots** `config/lane-route-slots.candidate.json` — UNTRACKED
  - openspec change records `openspec/changes/<change>/{proposal.md,tasks.md,specs/<capability>/spec.md}`
- **Fabric repo**: `C:/Projects/Agent_Workspace/Fabric` — **it may be sitting on a peer round's in-flight branch**;
  treat its working tree and untracked dirs as read-only, and publish from a NEW worktree off `origin/main`.
- **Credential (PATH only, never a value)**: `C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt`
  (fine-grained PAT: Contents read+write, PR create/merge). It must never appear in argv, a URL, a log or an artefact.
  On Windows git, `GIT_ASKPASS` alone is ignored — pass
  `-c credential.helper= -c credential.interactive=always -c core.askPass=<wrapper.cmd>` per invocation.
- **Skills to load first** (in this order): `hgk-lifecycle-admission`, `hgk-kanban-and-lane-routing`,
  `hgk-governed-execution`, `governed-write-admission`, `remote-repo-publication`.

---

## 3. Standing owner rules that still apply

1. **Lane chain**: PLAN/Orchestrator in Hermes; EXECUTE = Codex CLI; VERIFY/SECURITY = Codex CLI. The current
   owner order binds PLAN to `GLM-5.3-Flash` (opencode-go) and **both** EXECUTE and VERIFY/SECURITY to
   `DeepSeek V4.1 Flash` (opencode-go) — i.e. **the writer and the checker share one arm**, so a round's
   verification has **no model-axis independence**. Record that, never paper over it.
2. **Lane pools are a separate surface from the registry.** A mandated arm can be declared, reachable
   provider-direct, and still **absent from the lane's pool** → the dispatch fail-closes
   `ERR_LANE_REQUIRED_ARM_ABSENT` (exit 4). Do **not** edit the registry to make your dispatch succeed: run the
   mandated model provider-direct through the same relay with the model pinned on argv, smoke-probe it first
   (`-z "Reply with exactly: PROBE_OK"`), and disclose the deviation.
3. **On 429/quota**: switch immediately to the declared fallback and continue — do not pause; record every switch
   and state that a fallback verdict comes from a different checker.
4. **Candidate-only**: no self-acceptance, no self-promotion of an approval, no Gate PASS, no release claim.
5. **Evidence discipline**: name the tested revision (bytes + sha256) whenever you report a test result; label
   carried-over facts as carried-over; say `NOT RE-MEASURABLE` instead of supplying a plausible mechanism.

---

## 4. What is already done and published (verified)

| Round | ChangeSet | Fabric branch / PR | Head |
|---|---|---|---|
| R6/R7 | evidence + docs | `evidence/cnv-pipd-ls-sp-20261015-r6` (PR #3, closed) / `…-r7` (PR #4, draft) | `a10f7bea` / `04a1e118` |
| R8 | EIA closure + skill slim | `evidence/cnv-pipd-ls-sp-20261015-r8` (PR #5, draft) | `3af41480` |
| R9 | FAR residual closure | `evidence/cnv-pipd-ls-sp-20261015-r9` (PR #7, draft) | `5cd47cea` |
| R10 | session closure/candidates | `evidence/cnv-pipd-ls-sp-20261015-r10` (PR #9, draft) | `34d57124` |
| peer | lane reliability / FAR remediation+closure | `pub/lane-reliability-closure-20261016` (PR #6) / `pub/far-remediation-and-closure-20261016` (PR #8) | `0cb59d90` / `5ae6f37d` |

`main` = `b8ff8104`. All the above prefixes were re-read during R10 and reported **unchanged**.
R9 repaired two real defects (a `validate.py` guard pair, a skill main-file slim to 21,026 bytes with 113 refs and
0 lost). R10 repaired this session's own lane tooling (per-turn immutable receipts + a nonce attestation; 8 tests)
and adjudicated 36 change-record rows.

**Guard subject status**: `R6_DELIVERY/` = 300 files, byte-verbatim, 0 drift (last checked this mission).

---

## 5. OPEN ITEMS — measured, owner-tagged, one action each

### 5.1 Owner decisions (a human must choose; no agent may)

| id | item | one action |
|---|---|---|
| OD-1 | **Registry vs order conflict**: the live registry has `PLAN = openai-codex/gpt-6.1-sol` (epoch 21, applied 12:36:30 by an act outside the rounds, `check_drift == []`), while the standing order binds PLAN to `GLM-5.3-Flash`. | Decide which stands, then run one registry re-declaration (or accept the registry value). Record as an OPEN `declared_conflicts` entry either way. |
| OD-2 | **`SOD_VIOLATION` in the registry itself**: `check_sod(PLAN, VERIFY_SECURITY)` is a violation because both resolve to `openai-codex/gpt-6.1-sol`. | Decide the intended PLAN/VERIFY split; the registry must then satisfy `check_sod`, not merely `check_drift`. |
| OD-3 | **Writer/checker same arm** in the standing order (EXECUTE and VERIFY both `DeepSeek V4.1 Flash`). | Accept as a declared residual, or name a different checker arm. |
| OD-4 | **221 cases / 8 Gates / Fresh G1 / source #6** were never run; the package marks source #6 `FAIL_CLOSED`. | Authorise an acceptance window, or explicitly defer them out of scope. |
| OD-5 | **Skill support-files index gap**: 73 of 112 reference files are unlisted in `hgk-governed-execution`'s index. | Approve the index pass (an owner-authored record, not an agent rewrite). |

### 5.2 Work remaining (an agent can do these; nothing needs a decision)

| id | item | one action | locator |
|---|---|---|---|
| WR-1 | The **canonical dispatcher** still lacks the two repairs the round proved: per-turn receipt paths and a nonce gate that reads its own recorded stdout. R10's repair lives in a *successor* file only. | Port `R10/tooling/dispatch_r10.py`'s two changes into the canonical `scripts/hgk-lane-dispatch.py` (owner-authorized control-plane round). | `C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py` |
| WR-2 | **Dangling load path** in the governed skill: it names `entry_map.json` (lines 66, 71) and the file does not exist. | Write the missing `entry_map.json` or amend the skill to a resolvable pointer. | `<HERMES_HOME>/skills/software-development/hgk-governed-execution/SKILL.md` |
| WR-3 | `hgk-far-remediation-20261016` reads **0/25** while ~20 of its rows are measurably live. | Tick the rows that R10's adjudication scored `DONE_MEASURED`, keeping the row text and citing the measurement. | `C:/Projects/Agent_Workspace/HG-KSEOS/openspec/changes/hgk-far-remediation-20261016/tasks.md` + `R10/R10_CHANGE_RECORD_ADJUDICATION.json` |
| WR-4 | `skill-mainfile-cap-remediation` (11 rows) is **SUPERSEDED** — its premise (a 100,000-byte cap breach) was already false (measured 99,996/100,000 LF-normalised characters; the file is now 21,026 bytes). | Close the record as superseded with the measurement cited. | `…/openspec/changes/skill-mainfile-cap-remediation/tasks.md` |
| WR-5 | `lifecycle.plan()` spec-id collision (`TS-<segment>-NN` uniqueness) was worked around, not fixed. | Fix the id derivation in the lifecycle controller, or document the constraint. | `C:/Projects/Agent_Workspace/HG-KSEOS/src/hg_kseos/lifecycle.py` (~line 277) |
| WR-6 | Hermes source reports `0.21.5` while `config/hermes.json` declares `0.20.0`. | Reconcile the declared version. | `<HERMES_HOME>/config/hermes.json` |

### 5.3 Open governance records (openspec)

**Every one of the 24 change records under `HG-KSEOS/openspec/changes/` carries unchecked rows** (371 open rows
in total, measured by this round). Most of them are older than this mission and are **not** this mission's work.
Per-record dispositions, measurements and one-action paths: `OPEN_RECORDS_INVENTORY.tsv` (this root) and
`R11/FAR/ws1/open_records_inventory.tsv`.

### 5.4 Blockers

| id | blocker | why it cannot be closed by an agent |
|---|---|---|
| BL-1 | Human gates: Fresh G1 re-certification, DOC-05 effect admission, owner/AO/release authorisation | requires a human signature |
| BL-2 | The external acceptance officer has not accepted any packet (`scope_verdict: PARTIAL_CHALLENGE`) | external party |
| BL-3 | Source #6 is `FAIL_CLOSED` in the package | owner/authority decision |
| BL-4 | A peer round holds the local Fabric checkout on an in-flight branch | coordination, not a defect |

---

## 6. Resume recipe (copy-paste)

```bash
# 0. anchors
HERMES_HOME="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes"
HGK="C:/Projects/Agent_Workspace/HG-KSEOS"

# 1. HGK typed admission (copy the previous harness, change PROJECT_ID + paths)
cd "$HGK" && ./.venv/Scripts/python.exe C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015-R11/hgk_admission_r11.py

# 2. an openspec change record needs proposal.md + specs/<capability>/spec.md + tasks.md
cd "$HGK/openspec" && openspec validate <change> --strict

# 3. KANBAN/SWARM graph in one call
hermes kanban boards create <slug> && hermes kanban boards switch <slug>
hermes kanban swarm "<goal>" --worker "<profile>:<title>" --verifier acceptance-officer --synthesizer hgk-orchestrator --json

# 4. a governed lane turn — PRE-FLIGHT THE POOL FIRST (see §3.2)
cd "$HGK" && ./.venv/Scripts/python.exe <ROUND>/tooling/dispatch_r10.py VERIFY_SECURITY <BRIEF> 1 2400 --artifacts <dir>

# 5. publication (successor of publish_r10.py; worktree off origin/main, credential helper only)
cd <ROUND> && python publish_r1x.py prepare && python publish_r1x.py m2 && python publish_r1x.py push && python publish_r1x.py readback && python publish_r1x.py pr
```

---

## 7. Honesty notes for the next session

- R10's independent check returned **PARTIALLY_VERIFIED** (7 confirmed / 1 refuted / 1 unverifiable) and forced
  four corrections that are applied in R10's artefacts. Read `R10/R10_VERIFY/R10_VERDICT_ADJUDICATION.json`
  before quoting R10: it lists exactly what was **withdrawn** (a 0-byte-probe mechanism, a blanket side-effect
  claim, an understated collision count, an imprecise nonce-mechanism description).
- **No round has model-axis independence** under the current order (writer = checker arm).
- A child agent's output is a **claim**; re-derive decisive values yourself before acting.
- The local Fabric checkout diverged from `origin/main` at some point (not caused by these rounds); always cut
  publication branches from `origin/main`, never from the local checkout.

---

## 8. This round's own artefacts

`HANDOVER_R11.md` (this file) · `RESUME_MANIFEST.json` · `OPEN_RECORDS_INVENTORY.tsv` ·
`R11_SESSION_CLOSURE_LEDGER.json` · `HGK_TYPED_ADMISSION_R11.json` · `R11_BOARD_EVIDENCE.json` ·
`FAR/ws1|ws2|ws3/` (three read-only research products) · `SELF_EVOLUTION_R11.md/.json` ·
`R11_VERIFY/` (checker verdict + adjudication) · `publish_r11.py` (publication successor).
