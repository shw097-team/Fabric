# FAR-HANDOFF-V1-CAPABILITY-MISREAD-20261030 — synthesis

Challenged claim: *"ten work packages cannot PASS on this host because the capability does not exist."*
Verdict of this run: **the claim was wrong, and the delivery's own words show why.**

---

## 1. What HOST_OP actually says

Every refused package carries the same line. Quoted from `11_WORKPACKAGES_AND_DAG.md`, WP-FHS-02 line 56:

> **EffectClass / Admission**：`HOST_OP`；OPS ECP + Host Owner/Issuer + nonce/TTL/epoch。

and WP-FHS-04 line 88, WP-FHS-08 line 152, WP-FHS-10 line 184, WP-FHS-11 line 200, WP-FHS-12 line 216,
WP-FHS-13 line 232, WP-FHS-17 line 308 — identical.

`HOST_OP` is defined by **authority**: an OPS execution-control plan, the host owner/issuer, and a
nonce/TTL/epoch triple. It does not say "another machine". The named `原 Consumer` / `原 Receiver` /
`原 Host Loader` are *software services in this workspace*, and the delivery elsewhere states plainly that
they were exercised: `04_FABRIC_HGK_CONTROL.md` says the Fabric consumer's `route_event` "已用靜態 fixture
實際接收本首工作的欄位映射" and the HGK `native_admission.py` request constructors were fed this delivery's
field mapping.

I read "host" as "hardware". The document means "the owning service, acting under the owner's authority".

## 2. The services exist — and one of them ran in this session

| Service the delivery names | Where it is | State |
|---|---|---|
| `FABRIC/fabric/consumers/hgk_policy_consumer.py` (WP-02 producer/consumer) | `C:\Projects\Agent_Workspace\Fabric\FABRIC` @ `fffcb98b` | **executed**: 9 router rows loaded, `route_event` returned `ROUTE_OK` for `RUNTIME_TRANSIENT`, `CONFIG_PREAPPROVED`, `PROFILE_CHANGE`, `SKILL_CHANGE`, `PIPELINE_CHANGE` |
| `src/hg_kseos/native_admission.py` (WP-03 issuer path) | `C:\Projects\Agent_Workspace\HG-KSEOS` | present, 32,007 B |
| `src/hg_kseos/spine.py` (WP-04 journal/lease, WP-08 cursor) | same | present, 32,194 B |
| `src/hg_kseos/providers.py` (WP-13/17 qualification) | same | present, 6,884 B |
| the three GWO domains (WP-10) | Fabric, HG-KSEOS, **SBL** — all three local repos with `.git` | present |
| Hermes itself (WP-12 normal entry) | this process | present |
| Codex CLI + `ocx` relay (WP-08 worker, WP-13 hot swap) | `%LOCALAPPDATA%\OpenAI\Codex\bin\...\codex.exe`, relay on 10101 | present and exercised this round |

The owner key is a **different principal** from the agent (`owner_window.py`, fingerprint
`412b351937be72a1`), which is exactly what WP-03's `IssuerReceiverBinding` and WP-09's "different principal"
require. It is not a missing capability; it is an unused one.

## 3. Corrected classification of the ten

| WP | what the text asks for | what exists | corrected ruling |
|---|---|---|---|
| **02** Fabric Policy Consumer | six layers hashed in one scope, read back by the original consumer | consumer runs; **5 of 6 layers demonstrated this run**; Fabric has no epoch object | **closable now** except the epoch ambiguity |
| **03** HGK Registry/Issuer | original receiver/issuer registry, same epoch and scope | `native_admission.py` + owner key = a second principal | closable: one signed WorkOrder/Permit round trip |
| **04** Hermes Durable Runtime | journal/wake/lease schema and checkpoint readable | `spine.py` has leases and a journal; this process is the runtime | closable: one lease lifecycle with a checkpoint |
| **08** FHS Execute Worker | one admitted WorkID, single lease, real PID, world readback | dispatcher + Codex worker + spine, all exercised | closable: one WorkOrder → worker → cursor → EffectRaw |
| **10** B1 three GWOs | three effects with three receivers | three local repos | closable, heavy: three independent effects and three readbacks |
| **11** Portable Host Dogfood | every SP, every Host: install/load/invoke/nontrigger/remove | hosts on this machine: Hermes desktop, Codex CLI, (Claude Code CLI if installed) | closable **if "each Host" means installed CLIs**; the delivery does not say |
| **12** W18 Normal Mode | fresh PID, ordinary Goal, live profile, real served | any new process is a fresh PID | closable |
| **13** CAP On-Demand + HotSwap | old/new occupant parity POS and NEG | lane arms can be swapped; this round accidentally demonstrated a substitution | closable: build the parity test, which is also the cure for the substitution defect |
| **17** CAP-BOOT Occupants | installer creates the occupant, then LoadedSHA | pip/ocx install and hash | closable |
| **20** CLI/Agent/Host Kind Matrix | the 192 cells are executable | no runner named | closable, compute-bound; needs a cell executor |

**None of the ten was refused for lack of hardware.** Four (02, 03, 04, 08) are same-day work. Six are
multi-hour. That is a scheduling fact, not a capability boundary, and the previous run dressed a scheduling
fact as a law of nature.

## 4. Where the delivery, not the agent, is wrong

Three defects found by trying to satisfy the text literally:

- **D-1 — WP-02's Active layer has no object.** The Done line demands `Source/Stage/Approve/Active/Loaded/
  Consumer 各自 hash 同 scope`. Fabric carries no policy epoch; the nearest object in force is
  `HGK_STACK_MANIFEST.yaml`. Either Fabric gains an epoch object, or WP-02's Active layer is defined as that
  manifest. This run records the interpretation and files the gap rather than inventing an epoch.
- **D-2 — "各 Host" is never enumerated.** WP-11 requires every SP on every Host; the delivery does not list
  the hosts. A matrix over an undefined set cannot be complete or incomplete, only arguable.
- **D-3 — WP-20's "executable" has no runner.** The Done says the 192 cells are executable; no cell
  executor, no schema per cell, no expected output. It is currently a table, not a test.

None of the three is fatal. All three make an ALL-PASS claim unfalsifiable, which is worse than being blocked.

## 5. What this does to the two earlier structural findings

The previous run named four FAR defects and a single root cause ("the pipeline ends in a document, the plane
ends in rows"). This run adds the reason those defects survive: **a refusal is also a claim, and it was the
one claim nobody re-derived.** Every package I refused went out with a reason, an expiry and a review
trigger — the form of rigour — while the substance was a misread word.

The cure is therefore not a better report. It is to make a refusal auditable the same way a pass is:

- **O-1 — every refusal names the absent object, not the missing circumstance.** "No host capability" is not
  a finding; "Fabric has no epoch object" is. A refusal whose reason contains no object name is rejected.
- **O-2 — a refusal carries a reproduction attempt.** The refuser must show the command it ran before
  concluding the service is absent. This run's WP-02 evidence is what that looks like.
- **O-3 — obligations become rows.** Give the spine an `obligations` table: one row per unclosed item, with
  `owner`, `due`, `state`, and the `acceptance_id` it will change. A round cannot close while any obligation
  row it opened is `OPEN`. That is the mechanical answer to "the round was green and the rows were not".
- **O-4 — a promotability claim quotes its oracle and discharges each clause.** Already written into the
  skill; it belongs in `acceptance_default.py` as a hard check.
- **O-5 — the officer derives its own claims from the oracle file.** The maker supplies subject and oracle
  only. This round's misread would have been caught by an officer asked "does 02's Done line name six
  layers that exist" instead of "does the citation resolve".

## 6. Rulings

| ID | Ruling | Class |
|---|---|---|
| **OD-H** | withdraw the blanket refusal of the ten; re-classify as schedule, and grant WP-02 subject to the epoch interpretation | **DECIDE** (agent, recorded) |
| **OD-I** | open four packages now (02, 03, 04, 08) as one round with one owner envelope; the other six as a second round | **DECIDE** |
| **OD-J** | Fabric: add a policy epoch object, or amend WP-02's Done to name the stack manifest | **DECIDE (Fabric owner)** |
| **OD-K** | define the Host set for WP-11 and the cell schema for WP-20 | **DECIDE (delivery owner)** |
| **OD-L** | install the `obligations` table and the round-closure gate (O-3) | **DECIDE**, then build |

## 7. Plan

**N1 (now, agent).** WP-02 evidence is written and measures five of six layers. Run the sixth as soon as
OD-J picks the object; until then it is recorded as interpreted, not as PASS.

**N2 (agent, one round).** WP-03 + WP-04 + WP-08: one owner envelope, one signed WorkOrder through
`native_admission`, one lease lifecycle with a checkpoint, one bounded worker with a real PID and a journal
cursor, each read back by its own consumer. These three share the same objects, so they close together.

**N3 (agent, one round).** WP-10 three GWOs: one effect per domain, each read back by its own receiver.

**N4 (agent, after OD-K).** WP-11 matrix and WP-20 cell executor.

**N5 (agent, one round).** WP-12 fresh-PID normal mode; WP-13 parity test (which doubles as the cure for the
served-vs-requested defect); WP-17 occupant install with LoadedSHA.

**N6 (agent).** O-3 and O-4 built into the plane, then re-run the delivery's denominator so the rows and the
report cannot disagree again.

## 8. What this run does not claim

- It does not claim the ten are closed. One of them is measurably closer; nine are re-classified, not done.
- It does not claim the delivery is correct. It names three places where it is not.
- It does not withdraw the four FAR defects found earlier; it explains why they survived this long.
