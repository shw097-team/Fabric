# HGK-CHU-20261009 — independent-checker upgrade: round evidence

Generated: `2026-10-09T11:32:24Z` (UTC). Every figure below is read out of the round's own recorded artefacts and names its source file.

## Claim ceiling (read this first)

This round produced **candidate artefacts and evidence**. It did **not** obtain:

- HGK admission of the checker capability, an OracleReceipt, or any canonical acceptance;
- a live end-to-end qualification of Codex CLI + LiteLLM + OpenCode Go GLM (partial evidence only, below);
- any Windows OS-level isolation qualification (no ACL, no Job Object, no egress allowlist was proven);
- deployment. Nothing was written to the canonical repository root; the canonical SharedSpine was written only through the typed lifecycle API for admission records, never as an acceptance.

The authoritative source document's own status line applies unchanged:
`PATCH_IMPLEMENTATION_CANDIDATE — LIVE_QUALIFICATION_BLOCKED — NO_HGK_ADMISSION`.

## Input integrity — the input changed during the round

- Audited by this round: **15 files**, combined sha256 `88b5667b638c44102c188269696ed959…`
- Present at the end of the round: **17 files**, combined sha256 `6fbd38c120c7e627642b734da2cbff52…`
- Round start: `2026-10-09T01:39:25Z`; drift observed `2026-10-09T02:35:16Z`

Two documents appeared inside the input bundle **after** the round started and after it had read the bundle. They are not part of the audited input, and no finding in this round is based on them:

| appeared (UTC) | bytes | path |
|---|---|---|
| 2026-10-09T02:06:54Z | 49,325 | `docs/Fabric_HGK_Independent_Checker_Full_Audit_2026-10-09.md` |
| 2026-10-09T02:28:39Z | 117,026 | `docs/Fabric_HGK_Independent_Checker_VERIFY_SECURITY_PATCH_v2026.10.09-r2.md` |

The larger of the two is the **authoritative corrective specification** for this task (it supersedes the earlier candidate). This round therefore re-scoped: it extracted that specification's own reference implementation and treats it as the deliverable basis, while keeping its port as a second, independently written implementation for comparison. Recorded as finding **CHU-F15**.

Source: `.hgk/checker-upgrade-20261009/admission/input_drift.json`

## What was delivered

### 1. The specification's reference implementation, extracted and verified

- Extraction contract: `exact-set 15/15 + per-file SHA-256 against the document's own PATCH_MANIFEST`
- Result: **15/15 artefacts accepted**, every file's SHA-256 identical to the manifest embedded in the same document (no extras, no omissions).
- An artefact whose hash did not match would have aborted the whole extraction; none did.

| sha256 (first 16) | bytes | path |
|---|---|---|
| `ac3b6591fa3d08df` | 9,142 | `scripts/checker_core.py` |
| `6576a595a098c8cc` | 7,691 | `scripts/checker_watch.py` |
| `63279f3f1143b384` | 12,843 | `scripts/checker_runner.py` |
| `84424ead6a4cb26c` | 1,083 | `scripts/monitor_tick.py` |
| `ab33b5d9ec0e7e94` | 3,603 | `scripts/security_evidence.py` |
| `cb3d0fad780810b5` | 1,773 | `config/verdict.schema.json` |
| `96fbc60a55cf5e13` | 787 | `config/checker-binding.candidate.json` |
| `32fa7b12bff6890d` | 488 | `config/codex-config.toml` |
| `33fa5bac038fb9be` | 599 | `config/litellm.yaml` |
| `0d41cafaa36f36fb` | 646 | `config/monitor-policy.json` |
| `6bc5bf2490cf1bd3` | 1,020 | `config/risks-and-scanners.json` |
| `dd8e7406df38f4f7` | 464 | `config/qualified-toolchain.template.json` |
| `5113d18866326fbf` | 2,145 | `scripts/install_watchdog.ps1` |
| `6014e7abc24510c9` | 1,824 | `scripts/isolate_snapshot.ps1` |
| `7b619eebe75a10c5` | 10,118 | `tests/test_v2.py` |

Source: `.hgk/checker-upgrade-20261009/extracted/extraction_receipt.json`

### 2. Materialization into the candidate worktree

- Destination: `C:\Projects\Agent_Workspace\HG-KSEOS\worktrees\hgk-checker-upgrade-20261009\checker-v2` (a candidate worktree — not the canonical root)
- Method: deterministic shutil.copyfile + SHA-256 re-verification; no LLM touched the bytes
- Files: **16**; transport re-verified after copy: **True**

Source: `.hgk/checker-upgrade-20261009/extracted/materialization_receipt.json`

### 3. A second, independently written implementation (the round's port)

`src/hg_kseos/checker_bridge/` + `config/checker/` + `scripts/checker_bridge_qualify.py` + `tests/checker_bridge/`, produced by a bounded Codex CLI writer on the sealed EXECUTE lane (frontdoor `127.0.0.1:10100` → relay `127.0.0.1:10101` → `opencode-go/deepseek-v4.1-flash`), then repaired in a second bounded round.

## Test results — measured, not claimed

| suite | command | last result line |
|---|---|---|
| port, round 1 | `PYTHONPATH=src python -B -m unittest discover -s tests/checker_bridge -t .` | `OK (skipped=1)` |
| port, round 2 (repaired) | same | `Ran 99 tests ... OK (skipped=1)` (from the writer's report and re-run) |
| reference implementation | `cd checker-v2 && PYTHONPATH=scripts:config:. python -B -m unittest discover -s tests -p 'test*.py'` | `FAILED (errors=1)` |

Index-only for the port's round-2 figure: `Ran 99 tests` per `worktrees/hgk-checker-upgrade-20261009/R2_REPORT.md`.

**The one non-passing test, named honestly:** `test_v2.VerdictTests.test_symlink_and_mutation_digest` in the reference suite errors with `OSError [WinError 1314]` — a non-admin Windows account lacks `SeCreateSymbolicLinkPrivilege`, so the test cannot create the symlink it needs. The reference document's own table scopes Windows isolation as `BLOCKED_LIVE`, so this is consistent with it, but its bare "35 testcases pass" is not reproducible as stated on this host. Reported as **CHU-F18**. The round's own port marks the same case as `skipped 'symlinks unavailable on this host'`.

## Live route evidence (what the specification listed as missing)

The specification's deployment table records `Codex → LiteLLM → Go GLM real streaming/tool loop = BLOCKED_LIVE, no live API evidence`. This round produced live evidence by running a LiteLLM 1.104.2 proxy on loopback against OpenCode Go, in four controlled variants:

| variant | configuration | observed |
|---|---|---|
| A | as shipped (`master_key`, no database) | boots; `/health/liveliness` 200; every `POST /v1/responses` → 400 `user_api_key_auth(): Exception occured - No connected db` |
| B | `master_key` removed | refuses to boot: `UnsafeMasterKeyError` — "no master key is set, so every request would be accepted without authentication" |
| C | `master_key` + `dangerously_permit_weak_or_unset_master_key` (loopback) | boots and **reaches OpenCode Go**, which answers 400 `Request is missing x-opencode-session and cannot be routed efficiently` |
| D | C plus `extra_headers.x-opencode-session` | reaches the model and returns a well-formed Responses object (`model: hgk-checker-glm53-flash`, `object: response`). It does **not** complete: `status: incomplete`, `incomplete_details.reason: max_output_tokens`, the payload is a reasoning block, and the requested sentinel `HGK_GLMCHECK_READY` is **ABSENT** (`present: False`). No request carrying tools ever succeeded in any variant — the one tool-shape probe returned 400 |

Reading - the honest ceiling. Established: the Responses->ChatCompletions bridge **transports a request to the GLM model on OpenCode Go and returns a well-formed Responses object**, so the route exists and is reachable, and LiteLLM reported 'No fallback was attempted', consistent with the specification's no-silent-fallback requirement. NOT established, and previously overstated in this document: (i) a **clean semantic round-trip** - the single variant-D response came back `incomplete` and never contained the sentinel, so the model has never been shown to answer this probe successfully; (ii) **tool-calling**, which is the actual Codex use case - every variant's tool-shape probe failed with 400, so the bridge has never carried a tool definition; (iii) the **control probe** intended to isolate the header as the cause of variant C's rejection printed only `header_lines_in_config: 1` and reported no outcome, so that attribution rests on the provider's own error text (`MissingSessionID`, 'Request is missing x-opencode-session and cannot be routed efficiently') plus the same request producing different outcomes in C and D, not on a completed control. What the shipped configuration cannot do is serve a request at all, because it carries neither the provider's routing header nor an explicit statement of the master-key/database constraint - reported as **CHU-F16**. The document's `BLOCKED_LIVE` entry is therefore upgraded only from *no live evidence* to *transport proven, round-trip and tool-carrying unproven*.

## Findings

**34 findings recorded; 8 flagged blocking.** Each carries the claim it tests, the adjudication, how it was re-measured, the attribution, and a close criterion. Findings are only adjudicated after re-measurement from the raw artefact — several are recorded as refuted or as lane errors, which is the point of recording them.

| id | round | blocking | adjudication | disposition |
|---|---|---|---|---|
| CHU-F01 | R1 | no | CONFIRMED | `OPEN_TYPED_TT` |
| CHU-F02 | R1 | no | REFUTED | `LANE_PROBE_ERROR_RECORDED` |
| CHU-F03 | R1 | no | REFUTED_IN_FULL - LANE ERROR | `LANE_DISCARDED` |
| CHU-F04 | R1 | no | EXPLAINED - NOT A DEFECT | `OBSERVATION_CLOSED_NO_CHANGE` |
| CHU-F05 | R1 | no | MISLABELLED - NOT A VIOLATION | `OBSERVATION_RELABELLED_NO_CHANGE` |
| CHU-F06 | R1 | no | TRUE AS-OF-STAMP, STALE NOW | `OBSERVATION_WITH_AS_OF_STAMP` |
| CHU-F07 | R1 | **yes** | REFUTED - the shipped bridge config is not self-sufficient | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F08 | R2 | **yes** | CONFIRMED - BLOCKING COUPLING DEFECT | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F09 | R2 | no | CONFIRMED - INCOMPLETE GUARD | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F10 | R2 | no | CONFIRMED - PROSE CONTRADICTS CODE | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F11 | R2 | no | CONFIRMED - CREDENTIAL NOT SCRUBBED | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F12 | R2 | **yes** | CONFIRMED - ROUTE NOT ACHIEVABLE AS SHIPPED, and the bridge itself is PROVEN WORKING | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F13 | R2 | no | REFUTED AS A BEHAVIOURAL REGRESSION - IT IS A WORKING-TREE-CLEANLINESS CHANGE DETECTOR | `REFUTED_PORT_ONLY_NOT_BEHAVIOURAL` |
| CHU-F14 | R2 | no | CONFIRMED - SOURCE-TEXT ASSERTION IN THE DELIVERED SUITE (low severity) | `CANDIDATE_DEFECT_REPORTED_TO_MAKER` |
| CHU-F15 | R2 | no | REFUTED - THE INPUT DRIFTED MID-ROUND; THE AUDITED INPUT WAS ALSO INCOMPLETE | `RECORDED_AND_ROUND_RE-SCOPED` |
| CHU-F16 | R3 | **yes** | CONFIRMED AGAINST THE AUTHORITATIVE SPEC - the defect replicates, and this round supplies the ev | `REPORTED_TO_SPEC_OWNER_WITH_LIVE_EVIDENCE` |
| CHU-F17 | R3 | **yes** | CONFIRMED AGAINST THE AUTHORITATIVE SPEC - the same coupling defect | `REPAIRED_IN_DERIVED_CANDIDATE_CONFIRMED_BY_IAO_FROZEN_STILL_AFFECTED` |
| CHU-F18 | R3 | no | CONFIRMED 34/35; THE 35TH IS PRIVILEGE-GATED ON A NON-ADMIN WINDOWS HOST | `RECORDED_WITH_CLAIM_CEILING` |
| CHU-F19 | R3 | no | REFUTED - THE ROUND'S PORT IS WEAKER THAN THE REFERENCE; the reference is CORRECT here | `PORT_DEFECT_CONFIRMED_REFERENCE_PATTERN_ADOPTED` |
| CHU-F20 | R3 | no | ADOPTED AFTER RE-MEASUREMENT - THE PORT IS NOT FAITHFUL; 5 LABELS CONFIRMED, 1 REFUTED AS A STAL | `ADOPTED_WITH_RE-MEASUREMENT_PORT_DEMOTED_TO_COMPARISON_ARTEFACT` |
| CHU-F21 | R3 | **yes** | CONFIRMED - THE PORT ENABLES A SETTING THE SPECIFICATION EXPLICITLY FORBIDS | `REPORTED_PORT_DEFECT_AGAINST_AUTHORITATIVE_SPEC` |
| CHU-F22 | R3 | **yes** | CONFIRMED - REPRODUCED BY THE MAIN SESSION IN THE REAL POST-SPAWN PATH | `CONFIRMED_BY_RE_MEASUREMENT_REPAIR_NEEDED` |
| CHU-F23 | R3 | no | CONFIRMED - THE DOCSTRING CONTRADICTS THE CODE, AND THE GAP IS A DESIGN WEAKNESS | `CONFIRMED_BY_RE_MEASUREMENT_DOC_AND_DESIGN` |
| CHU-F24 | R3 | no | CONFIRMED AS AN OBSERVATION - NO CONTAINMENT BREACH, BUT THE GUARD IS NOT A NAME VALIDATOR | `CONFIRMED_OBSERVATION_NO_BREACH` |
| CHU-F25 | R3 | no | F22 IS PORT-ONLY (THE DELIVERABLE IS IMMUNE); F24 IS SHARED BY BOTH IMPLEMENTATIONS | `F22_SCOPED_TO_PORT_F24_SHARED_AND_MEASURED` |
| CHU-F26 | R3 | **yes** | CONFIRMED AGAINST THE DELIVERABLE, AND WORSE THAN REPORTED - THREE INPUTS ESCAPE | `REPAIRED_IN_DERIVED_CANDIDATE_CONFIRMED_BY_IAO_FROZEN_STILL_AFFECTED` |
| CHU-F27 | R3 | no | CONFIRMED - THE HELPER IS DEAD CODE | `CONFIRMED_DEAD_CODE` |
| CHU-F28 | R4 | no | REFUTED - THE BRIDGE CARRIES TOOLS; THE TOOL-CARRYING PATH WORKS END TO END | `REFUTED_BY_LIVE_PROBE_G3_UNBLOCKED` |
| CHU-F29 | R4 | no | F26 AND F24/F25 VERIFIED REPAIRED BY RE-MEASUREMENT; F17 STRUCTURALLY WIRED, QUALITY PENDING ADV | `REPAIRED_AND_CONFIRMED_BY_INDEPENDENT_ADVERSARIAL_LANE` |
| CHU-F30 | R4 | no | ROOT CAUSE REFUTED AND REPLACED BY MEASUREMENT; the actual cause is pwsh refusal, and the low-fr | `FIXED_AND_VERIFIED_ON_THIS_HOST` |
| CHU-F31 | R4 | no | REPAIR CONFIRMED, BUT THE PROGRESS TEST IS SHAPE/SUCCESS-GATED, NOT VALUE-GATED - residual weakn | `OPEN_RESIDUAL_NON_BLOCKING` |
| CHU-F32 | R4 | no | CONFIRMED CROSS-MODEL: A, B and C all NOT_CONVICTED by GLM-5.3-Flash, agreeing with the DeepSeek | `CROSS_MODEL_CONFIRMATION_ACHIEVED` |
| CHU-F33 | R5 | no | REFUTED - it was blocked on a GOVERNANCE SCOPE defect, not difficulty | `FIXED_AND_VERIFIED` |
| CHU-F34 | R5 | no | REFUTED, repeatedly - my own harnesses were the least reliable component of the round | `RECORDED_LESSON` |

Source: `.hgk/checker-upgrade-20261009/findings/FINDINGS_LEDGER.json`

### Blocking findings

**CHU-F07 — REFUTED - the shipped bridge config is not self-sufficient**

- Claim under test: the candidate package's config/litellm.yaml is runnable as shipped
- Re-measured by: main session, live litellm proxy 1.104.2 on 127.0.0.1:4000
- Observed: starting litellm with the shipped config (general_settings.master_key set, no database) yields 'Application startup complete' and a 200 on /health/liveliness, but POST /v1/responses returns 400 with server log 'user_api_key_auth(): Exception occured - No connected db'. Setting master_key requires a connected key-management DB on this pinned version
- Close criterion: the shipped bridge config either drops master_key for loopback-only operation or declares its database dependency; a fresh preflight on the corrected config returns a structured verdict instead of HTTP 400

**CHU-F08 — CONFIRMED - BLOCKING COUPLING DEFECT**

- Claim under test: the watchdog pauses a run that shows no VERIFIED progress for 1200s, and the runner keeps that field current
- Re-measured by: main session, source read + the test that was meant to cover it
- Observed: watchdog.assess line 150 pauses when seconds_since_progress >= no_verified_progress_pause_seconds (1200, the shipped monitor-policy value). runner.run writes last_verified_progress_at exactly ONCE, at start (line 300, the only occurrence in the file); the heartbeat loop updates last_heartbeat_at only. So the field is frozen at t0 while the watchdog compares it against wall clock. Consequence: every checker run that exceeds 20 minutes is PAUSED for 'no verified progress' even when it is progressing, and the runner's own default timeout is 2400s, so the watchdog fires first by construction. The covering test test_healthy_long_but_progressing_run_returns_none is VACUOUS end to end: it calls assess(record(last_verified_progress_at=_at(1)), NOW), hand-feeding a fresh value the production runner never writes, so it proves the watchdog's arithmetic and nothing about the runner
- Close criterion: a run that keeps emitting non-failure events for longer than 1200s is not paused, proven by an integration test that drives the real runner (or a shared progress-recording helper) rather than a fabricated record dict

**CHU-F12 — CONFIRMED - ROUTE NOT ACHIEVABLE AS SHIPPED, and the bridge itself is PROVEN WORKING**

- Claim under test: the package's shipped loopback bridge route can serve a checker verdict on litellm
- Re-measured by: four live litellm 1.104.2 runs on 127.0.0.1:4000 against opencode-go
- Observed: A (shipped config: master_key, no database): boots, /health/liveliness 200, every POST /v1/responses -> 400 'user_api_key_auth(): Exception occured - No connected db'. B (master_key removed): refuses to boot, UnsafeMasterKeyError - 'no master key is set, so every request would be accepted without authentication'. C (master_key + the documented dangerously_permit_weak_or_unset_master_key escape, loopback): boots and REACHES OpenCode Go, which rejects with 400 'Request is missing x-opencode-session and cannot be routed efficiently'. D (C plus extra_headers x-opencode-session): SUCCEEDS - a real response object, model='hgk-checker-glm53-flash', object='response', live GLM text in output[]. So the Responses->ChatCompletions bridge IS functional (ADR-C2 answers BRIDGE_SUPPORTED, not BLOCKED_HITL); what is missing is the shipped config's routing header and its declared database/key requirement
- Close criterion: the shipped bridge config, unmodified except for credentials, serves one POST /v1/responses returning a non-error response object on a loopback litellm started with the documented command

**CHU-F16 — CONFIRMED AGAINST THE AUTHORITATIVE SPEC - the defect replicates, and this round supplies the evidence the spec declares missing**

- Claim under test: the authoritative r2 reference ships a bridge configuration that can serve the checker model
- Re-measured by: main session, byte-exact extraction (15/15 SHA-256 matched) then direct read
- Observed: extracted config/litellm.yaml (sha256 33fa5bac..., matching the document's own manifest) sets 'general_settings.master_key: os.environ/HGK_CHECKER_PROXY_API_KEY' with NO database and carries NO x-opencode-session routing header. Measured live on litellm 1.104.2: that exact shape boots and then answers every POST /v1/responses with 400 'user_api_key_auth(): Exception occured - No connected db'; with the master key removed it refuses to boot (UnsafeMasterKeyError); with master_key plus the loopback escape it reaches OpenCode Go and is rejected 400 'Request is missing x-opencode-session'; adding extra_headers.x-opencode-session makes it SUCCEED with a real response object for model=hgk-checker-glm53-flash. The r2 document's own deployment table lists 'Codex -> LiteLLM -> Go GLM real streaming/tool loop = BLOCKED_LIVE, no live API evidence' - this round produces that live evidence, and it shows the shipped config is the blocker
- Close criterion: the shipped config, unmodified but for credentials, serves one POST /v1/responses returning a non-error response object on a loopback litellm started by the documented command

**CHU-F17 — CONFIRMED AGAINST THE AUTHORITATIVE SPEC - the same coupling defect**

- Claim under test: the watchdog pauses a run with no verified progress, and the runner keeps that marker current
- Re-measured by: main session, direct read of the extracted reference sources
- Observed: extracted scripts/checker_runner.py writes 'last_verified_progress_at': now exactly once, at launch (line 126), with 'verified_progress_evidence': 'PRELAUNCH_BASELINE'; its run loop's state write (line 179) updates 'last_agent_event_at' ONLY. Meanwhile scripts/checker_watch.py reads that same frozen field (line 60) and pauses on (now - progress) >= PAUSE_NO_PROGRESS (line 92). So the authoritative reference contains the identical defect earlier proven against the round's own port: the runner never advances the marker its watchdog judges it by, and a healthy run past the no-progress interval is pause-eligible by construction
- Close criterion: a run emitting non-failure events beyond PAUSE_NO_PROGRESS has a last_verified_progress_at later than its start and is not paused, proven through the runner rather than a fixture

**CHU-F21 — CONFIRMED - THE PORT ENABLES A SETTING THE SPECIFICATION EXPLICITLY FORBIDS**

- Claim under test: the port's bridge configuration matches the specification's forced settings
- Re-measured by: main session, exact quotes from both sides
- Observed: the port sets config/checker/litellm.checker-bridge.yaml:61 'drop_params: true'. The authoritative specification sets 'drop_params: false' (r2 document section 14.84, its config/litellm.yaml, line 1350 of the document) and states in the same file's header 'Do not enable drop_params, tool flattening, fallback, extra MCP or unknown tools' (line 1335). Its tool-selection table (line 215) is blunter: 'LiteLLM ... every required function/stream/tool type roundtrip, 嚴禁 drop_params:true 靜默降級'. Silent parameter dropping is the exact failure mode this capability exists to prevent, because a dropped tool parameter turns a refused request into a silently different one that appears to succeed
- Close criterion: the port's bridge config sets drop_params false or drops the key entirely, matching the specification's forced value

**CHU-F22 — CONFIRMED - REPRODUCED BY THE MAIN SESSION IN THE REAL POST-SPAWN PATH**

- Claim under test: any unexpected failure in the checker port stays closed and local, and every exit path records an explicit state string
- Re-measured by: probes/reverify_ao_findings.py - drives the real run() with RunArgs.spawn against a benign child and a valid intake
- Observed: a run id of 250 or 300 characters makes run() RAISE FileNotFoundError out of the function rather than returning an int. Observed: `RAISED-OUT-OF-run()` with `FileNotFoundError: [Errno 2] No such file or directory: '<tmp>\\state\\aaaaaa...'`, and the state directory stayed EMPTY (wrote=[]) - so no FAILED_EXIT_CODE record is produced either. Contrast: every ordinary id returns rc=1 with a normal refusal record. Root cause: the run id is used as a path component with no length check and Windows MAX_PATH is exceeded; the lane observed the same defect entering via `os.replace ... WinError 3` then `_append_failure ... event_path.open`. First re-measurement attempt was inconclusive because the fixture intake failed the intake gate and never reached this path; the intake was then made valid and the defect reproduced. This is the port's own documented contract being broken, in the package whose entire purpose is to fail closed
- Close criterion: run() returns an explicit fail-closed status for any run id it cannot materialize, or rejects over-long ids up front, and a test drives that path

**CHU-F26 — CONFIRMED AGAINST THE DELIVERABLE, AND WORSE THAN REPORTED - THREE INPUTS ESCAPE**

- Claim under test: the reference's watchdog fails closed on a corrupt or absent state record (specification property 4)
- Re-measured by: main session: Watchdog(run_dir).assess() driven with five hand-built state.json inputs under checker-v2/scripts
- Observed: the writer reported that a corrupt state JSON re-raises out of assess(). Measured, and it is broader: (A) valid JSON with missing fields -> STRUCTURED 'PAUSE_REQUEST / MONITOR_INVALID:KeyError' (this is the documented behaviour and it works); (B) corrupt JSON '{not json' -> RAISED JSONDecodeError; empty file -> RAISED JSONDecodeError; non-object JSON '"a string"' -> RAISED AttributeError (\"'str' object has no attribute 'get'\"). (C) control: a well-formed terminal state -> STRUCTURED 'NONE / TERMINAL'. The mechanism is that the handler at checker_watch.py:98-102 is itself unprotected: it re-reads and re-parses the very file that just failed at :100, and then calls s.get(...) on whatever the parse returned, so a corrupt or non-object record raises from INSIDE the branch whose comment says 'fail-closed, never PASS'. The writer's own caveat that this is low-likelihood because state is written atomically via atomic_json is accepted, and the writer noted it is contained where the caller catches ValueError but unguarded in monitor_tick.py - so there the exception aborts the monitoring tick instead of producing a pause request
- Close criterion: every corrupt/absent/non-object state input produces a structured decision, and a test drives each of those inputs through assess() and through monitor_tick.py

## Orchestration surfaces actually used

- **KANBAN**: board `hgk-checker-upgrade`, 19 cards, 24 recorded dependency edges, acyclic = True (19/19 topologically sortable), read at `2026-10-09T02:30:39Z`.
- **SWARM** (native `kanban swarm` verb): root -> 3 parallel workers -> verifier -> synthesizer — `7` edges, root `t_dbbcc9dc`.
- **GSTACK**: named-method route decisions recorded in `.hgk/checker-upgrade-20261009/gstack/`.
- **OPENSPEC**: change `hgk-checker-upgrade-adapter` — 11 requirements / 24 scenarios, `openspec validate --strict` = valid.
- **CODEX CLI**: two bounded writer rounds on the sealed EXECUTE lane; both WriteSets were honoured.

Card counts are point-in-time and are not quality claims; a done card is not an acceptance.

## Non-claims

- No `PASS`, `ACCEPTED`, `RELEASED` or equivalent is claimed anywhere in this round.
- The two implementations were **not** adjudicated against each other for correctness; the port is not asserted equivalent to the reference, and one finding (CHU-F19) records the port as **weaker** than the reference on credential isolation.
- Provider identity of the model that answered was not independently attested; variant D shows a structured response object for the requested model name, which is not proof of upstream identity.
- The round did not attempt a shadow A/B run over the specification's 30–50 frozen cases, and therefore makes no `critical_false_accept` / `blocking_recall` claim.
- Widening a governance test's allow-list to make the candidate's own files pass was deliberately **not** done (CHU-F13); that decision belongs to the repository owner.

