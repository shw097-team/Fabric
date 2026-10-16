## Pitfalls checklist

- **Router NATIVE ≠ skip orchestration.** `named_methods.route(flow)` returning
  `NATIVE`/DIRECT only selects the lane; Kanban/Swarm/Codex execution surfaces
  still apply. A governed task run without Kanban trace + independent lane +
  tracked writer is an execution-method gap, not a valid fast path.
- **Stale registry state = repair, not excuse.** `kanban_state: NOT_RESTORED…`
  with a working kanban.db is a defect to smallest-repair (backup → edit →
  readback → doctor regression), not a reason to skip Kanban.
- **Inherited execution surfaces are NOT current.** A new Stage needs its own
  canonical board, its own swarm lanes, and its own Codex WorkOrder execution;
  prior-Stage boards/lanes/writes are evidence for the prior Stage only.

- `PYTHONPATH=/c/...` fails for HGK repo python — use `C:\...` form; invoke the venv python
  as the quoted backslash path `".venv\Scripts\python.exe"` (gateway guard crash otherwise).
- **Native Windows Python (e.g. `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe`)
  rejects MSYS-style script paths** — `python /c/Users/.../x.py` → `can't open file
  'C:\c\Users\...'` (verified 2026-08-14 re-review; 3 consecutive failures until the
  `C:/Users/...` form was used). Always pass the Windows form `C:/Users/...` (forward
  slashes fine).
- **Heredoc python with backslashes gets mangled (verified 2026-08-14):** a `python -
  <<'EOF'` block containing `rel.replace('\\', '/')` died with `SyntaxError: unterminated
  string literal` — the backslashes were eaten before Python saw them. For any script
  containing backslash literals, write it with write_file and run the file instead of
  inlining in a heredoc.
- `git -C` with MSYS paths (`/c/Projects/...`) fails on native Windows git — use `C:/...`.
- `Start-Process -Redirect*` loses ExitCode in PowerShell 5.1 — see reference.
- PowerShell 5.1 `*>` redirect writes UTF-16LE — read back as Unicode, not UTF-8.
- Codex `--json` is an NDJSON event stream — the answer is the final `agent_message`.
- Kanban mutations blocked by `HERMES_DELEGATED_CHILD_CONTEXT=1` — unset it. NOTE: every
  subsequent `delegate_task` batch RE-SETS the var; unset again after EACH batch, even if
  it was empty minutes before.
- **Kanban active-board can be switched away mid-task by another session/task** (verified
  2026-08-13 WO-RP2-DAILY-001: heartbeat failed `cannot heartbeat <id> (not running?)` while
  `boards list` showed a foreign board `fda-implementation` as current). Fix: `hermes kanban
  boards switch <task-slug>` back, then heartbeat/complete. When a heartbeat/complete errors
  "not running", run `boards list` FIRST before assuming the claim TTL expired.
  EXTENSION (verified 2026-08-14 WO-HGK-MEM-RESEARCH-001): a card `create`d while a foreign
  board is active lands on THAT board — the returned id is valid but `assign`/`claim`/`complete`
  from your board fail with `unknown id or terminal state` / `no such task`. Fix: `boards list`
  to find which board actually owns the card (check the slug in the assign workspace path),
  `boards switch <owner-board>` → complete → `boards switch <your-board>` back. Never re-create
  the card (duplicate) — the original exists, just on the other board.
- PowerShell 5.1 `& $codexExe @args` with a prompt containing embedded `"` splits the
  prompt into multiple CLI args (`error: unexpected argument '...' found`) — sanitize the
  prompt file (replace `"` with `'`) before splatting.
- Codex `--approve-for-me` is mutually exclusive with `--sandbox` (it implies
  workspace-write); it did NOT unlock writes on the sealed lane anyway.
- **Never overwrite historical evidence files** (e.g. EVO004/EVO005 receipts) — new A2/A3-scoped
  evidence only. EXTENSION (verified 2026-08-13 FAR r8 violation): this includes the
  EXTERNALLY-SIGNED acceptance evidence MD — a post-acceptance round that regenerates the
  canonical file (docs/NBO/activation additions) breaks the documented immutable hash and
  fails AO A11. Fix = re-freeze (see
  `references/post-acceptance-subject-hygiene.md`): archive bytes → regenerate canonical →
  mirror ×4 → sweep ALL hash refs (short AND full 64-hex forms) → historical-baseline doc →
  superseding EVD. Do NOT attempt byte-exact restoration of the signed MD (dynamic generator
  timestamps + evolved embedded sources make it non-convergent).
- **Codex launcher hangs have two silent root causes (verified 2026-08-13 WO-FAR-RETRIEVAL-001):**
  (a) the launcher did NOT load `OPENCODE_GO_API_KEY` from `%LOCALAPPDATA%\hermes\.env` into
  the process env → codex exec hangs for 10+ min with an empty log (waiting on auth); the
  proven launcher reads the .env line-by-line and sets `$env:OPENCODE_GO_API_KEY` before
  splatting. (b) wrong isolated-home dir names: CODEX_HOME/OPENCODEX_HOME are
  `%LOCALAPPDATA%\HG-KSEOS\codex-hermes` / `opencodex-hermes` — the non-existent
  `codex-home` variant fails with "CODEX_HOME points to ... but that path does not exist".
  Also: arg order matters — `--model deepseek-v4-flash` FIRST, then `--cd <root>`, then
  `exec --skip-git-repo-check --ephemeral --json <prompt>` (single-quoted, `"`→`'` sanitized),
  capture with `& $codexExe @args *> log`. If a spawn hangs on the test step (pwsh
  WindowsApps invocation), the files are typically already written — kill the process,
  record FAR-CODEX-*-style defect, run tests with the standard Python311 directly.
- **Codex YAML/typo traps (verified 2026-08-13 PCIV-F01 repair):** (a) Codex writing YAML
  with an unquoted colon inside a value (`reason: PCIV-F01 closure: ...`) produces a file
  that fails `yaml.safe_load` — always run a fresh independent YAML parse after any Codex
  write; (b) Codex may silently write to a typo path (`evidence\rp02` instead of
  `evidence\rp002`) — always `find` the real output path after a Codex write and delete
  the typo dir; (c) a `mapping values are not allowed here` ScannerError on a Codex-written
  YAML is a maker defect, fix via a second WorkOrder-scoped Codex run (quote the value),
  never by Hermes-direct edit.
- **Codex long-path typo recurrence (verified 2026-08-13 ECL round, 2nd case):** the same
  class of typo recurred with a different missing char (`evidence\p002` — missing the `r`,
  vs earlier `rp02` — missing a `0`). Rule: after ANY Codex file write, (1) `find` the
  output path, (2) assert the EXACT expected directory exists, (3) grep for typo variants
  (`find . -name '*TYPO*'`), (4) have Codex move + delete the typo tree, (5) re-verify.
  Also: JSON receipts written by Codex parse fine; embed full 64-hex hashes in closure
  receipts and always re-hash from final bytes (a YAML-quote fix changes the file hash —
  `ac48014a…` became `999983fd…` after the fix; never copy a pre-fix hash into evidence).
- **Codex Chinese-content mojibake (verified 2026-08-13 docs upgrade, CODEX-MOJIBAKE-001):**
  the sealed lane (deepseek-v4-flash via opencodex) CORRUPTS Chinese UTF-8 on verbatim
  file rewrite (README 中文 1200→284 CJK chars, key strings lost; English-only AGENTS.md
  wrote fine). For doc edits with Chinese content: do NOT use Codex to write/rewrite —
  write correct UTF-8 via Hermes write_file with compensating controls (git diff review +
  independent checker + CJK/U+FFFD verification), record
  `CODEX_EXECUTOR_FALLBACK=MOJIBAKE_DEFECT` in evidence. English-only new files
  (AGENTS.md) are fine through Codex. Also: when setting AO check thresholds, use
  realistic values (compact operational docs have a few hundred CJK chars, not >1000) —
  an unrealistic maker-set threshold causes a false FAIL-as-specified that must be
  corrected with an AO_PREDICATE_CORRECTION record.
- Keep all task scripts under gitignored `var/a2/` / `var/a3/`; the tracked tree must show
  only the mandated evidence files as new.
- Evidence freeze: `cp` with `"...\$VAR"` inside double quotes does NOT expand the variable
  (creates a literal `review$EVID` file) — quote the path, not the var: use
  `"C:\...\evidence\review\\$EVID"` or build the path in a variable first.
- **Evidence-MD generator hygiene (verified 2026-08-13 FAR closure, 3 defects caught by
  external reviewer + internal gate):** (a) reading NESTED receipt fields with top-level
  `.get()` emits literal `None` into the generated evidence MD — always
  `grep -c 'None' <md>` before mirroring, and materialize the full post-repair chain
  (lane1 FAIL → finding → repair → lane2 PASS → final blockers=0), never a bare summary;
  (b) closure-receipt filenames are HYPHEN (`CLOSURE-EXT-FAR-001.json`) — an underscore
  in the generator silently produces a 0-row closure table, so verify table row count
  == expected denominator (`grep -c '^| EXT-FAR-'`); (c) `unittest` writes output to
  STDERR — capture test-stdout evidence with merged redirect
  (`python -m unittest discover -s tests -t . > out.txt 2>&1` + append EXIT), or the
  raw stdout evidence file is 0 bytes (AO-FINDING-FAR-002 class; a fresh AO lane WILL
  flag it). Full EVIDENCE_ONLY closure-round recipe (subject-root manifest with merkle
  digest, self-excluded evidence manifest, raw bundle, fresh-AO subject-binding, Q4
  real-invocation receipt, regression crosswalk, post-freeze separate-ChangeSet freeze,
  single zip review package):
  `references/external-challenge-evidence-closure-far.md`.
- **External-review freeze semantics:** the evidence MD references the mirror-receipt by
  PATH only; the receipt carries the MD hash (single direction, no self-loop). The MD
  must never embed its own hash.
- **Truncated-listing false absence (verified 2026-08-13 SQS data-plane cross-confirm):** an
  inventory piped through `head` (`find ... | head -N`) CANNOT support an ABSENCE claim — a
  head-truncated find made me misreport `data_plane/data/raw/` as unmaterialized while
  `raw/shioaji_kbars/` (637 parquet) actually existed; a fresh-context AO lane caught the
  error. Before declaring any layer/dir missing, run a dedicated unbounded check per expected
  item (`ls -d <path>`, `find <path> -type f | wc -l`), never a head-truncated listing.
- **DuckDB quirks (SQS data plane):** `asof`/`known_at` are DuckDB reserved words — quote them
  in SQL (`"asof"`); `fetchdf()` requires pandas (absent on system Python) — use `fetchall()`
  instead; import duckdb from the broken-base `.venv-data` via
  `sys.path.insert(0, r'...\SQS-THC\.venv-data\Lib\site-packages')` on system Python311.
- **Parallel fetch pipelines: never hold a lock across the network call (verified 2026-08-13,
  WO-RP2-DAILY-001).** First acquisition run produced 0 artifacts in 132 s: a global
  `threading.Lock` held across `sleep + urlopen + read` serialized all 8 workers AND the
  bursty contention stalled the source API. Fix pattern: `threading.Semaphore(N)` acquired
  ONLY around the fetch, polite `time.sleep` OUTSIDE any lock, plus per-item `PROGRESS`
  prints with `flush=True` so background runs are observable (repair record
  BACKFILL-CONCURRENCY-FIX-001). Debug recipe that isolates logic vs concurrency defects:
  import the module via `importlib.util.spec_from_file_location` and call the per-item
  function directly single-threaded — `__main__`-mode bugs can hide behind a silent
  background run. Also: git-bash background `pid` ≠ Windows python pid (`ps`/`tasklist`
  won't show it) — judge liveness by artifacts/receipts growth or `tasklist | grep python`.
- **Idempotent skip paths: index the receipts journal ONCE (verified 2026-08-13).** A
  `latest_receipt(symbol, source)` that re-iterates the whole journal per artifact is O(n²)
  because every SKIP_EXISTS append grows the journal — 26 s/symbol → 2 h+ for 263 symbols.
  Build `dict[(symbol, source)] = last_receipt` once from the loaded journal and look up in
  O(1). Layer-consistency checkers must sum by the SAME latest-per-(symbol,source) key so
  accumulated SKIP_EXISTS receipts don't inflate counts.
- **Transient 3xx from source CDNs needs code-aware retry with LONG backoff (verified
  2026-08-13).** TWSE's HiNetCDN intermittently answered `HTTP 308 Permanent Redirect`
  under concurrency; urllib raises `HTTPError 308` ("redirect error that would lead to an
  infinite loop") and the standard retry loop (3 × 0.4-0.8 s) never recovered — 20/263
  symbols failed with `TWSE_NETWORK_FAILURE` while the same request returned 200 when calm.
  Fix: catch `urllib.error.HTTPError` with `code == 308` → `time.sleep(8 + 4*attempt)` up to
  6 attempts, THEN fall through to the documented secondary source.
- **Surgical-repair pattern preserves writer=codex integrity (verified same round).** When a
  codex-written pipeline fails late and a plain rerun is too slow, do NOT edit the product
  script from Hermes. Kill the rerun; write orchestrator task tooling in gitignored
  `var/pciv/` that (1) imports the codex module via `sys.path.insert`,
  (2) monkeypatches the slow/brittle internals (dict-indexed latest_receipt, 308-aware
  http_get_json), (3) reprocesses ONLY the failed symbols, (4) runs the full deterministic
  rebuild (core → duckdb → manifest → catalog). Product code stays codex-authored; the
  helper is task tooling; queue the product-script hardening as a follow-up codex patch.
- **Month-level data defects are invisible to row-count checks — audit against a reference
  calendar (verified 2026-08-13, WO-RP2-DAILY-001).** (a) A `stat:OK` + empty month gets
  persisted as a 0-row artifact that then blocks refetch forever (SKIP_EXISTS sha match) —
  classify empties as pre-listing (keep) vs post-listing transient (delete+refetch).
  (b) A month can arrive partially (13/21 rows) and pass C5's >14-day gap rule while
  silently losing ~100 rows across many months — audit expected rows per symbol against a
  full-history symbol's date set (e.g. 1101), deficit >5 → delete ALL that symbol's raw
  artifacts and refetch every month. (c) DuckDB `read_parquet` infers polars-written
  String columns as BIGINT — `CAST(symbol AS VARCHAR)` in the table DDL or joins against
  legacy CSVs raise `int + str` TypeErrors.
- **Genuine suspension vs fetch defect: verify gap windows against the SOURCE's current
  data, then follow the user decision (verified 2026-08-13).** A C5-flagged gap where the
  source (TWSE) currently HAS the days = fetch defect → repair; where TWSE currently LACKS
  the days = genuine non-trading/suspension → user directive: REMOVE the symbol from the
  universe with a hash-bound `UNIVERSE_REMOVALS_<date>.md` evidence record (per-symbol
  TWSE-verified windows, names from the API `title`), delete its core, keep raw as history,
  and update checker constants (EXPECTED_SYMBOLS) via a Codex patch. Ad-hoc probe fetches
  during debugging pollute the governed raw layer and cause exactly-one-symbol
  receipts-vs-core mismatches — run probes in a scratch dir, and clean pollution
  (delete raw + strip receipts after a journal backup) when it happens.
- **Codex daemon death (`connection refused :10101`):** (a) `curl http://127.0.0.1:10101/healthz` confirm;
  (b) `ocx stop` may lie — find listener `netstat -ano | grep :10101 | grep LISTENING`, kill
  `powershell Stop-Process -Id <pid> -Force`; (c) RESTART MUST carry credential
  `export OPENCODE_GO_API_KEY=$(grep '^OPENCODE_GO_API_KEY=' "$LOCALAPPDATA/hermes/.env" | cut -d= -f2-)`
  + `export OPENCODEX_HOME="$LOCALAPPDATA/HG-KSEOS/opencodex-hermes"` BEFORE `opencodex start --port 10101`;
  (d) verify NEW pid + healthz. Daemon is NOT a service — record `OPENCODEX-DAEMON-RESTART-001` note.
- **Route recheck after Probe (2026-08-15 K6):** launcher `-Action Probe` kills the proxy in
  its finally block → recheck needs `-Action StartOpenCodex` + `& $codexExe @args` splatting
  canary; launcher `ERR_CODEX_ROUTE_EXIT_` = Start-Process-null-ExitCode false alarm (log
  nonce+turn.completed+usage = success); `Model metadata ... not found` benign. Recipe:
  `references/opencodex-human-home-hijack-restore.md`.

- **TWSE listing venue: NEVER infer from code prefix (verified 2026-08-13 WO-RP2-DAILY-003, external r3 caught it).** A scope doc built on "6xxx ⇒ 上櫃" claimed 38 TPEx symbols — factually WRONG: 6005 群益證, 6024 群益期, 6128 上福, 5538 東明-KY, 5471 松翰, 5515 建國, 5876 上海商銀 are ALL TWSE 上市; the whole 258-symbol universe is TWSE-listed, TPEx=0. The external acceptance officer flagged the resulting TWSE+TPEx scope claim as a dependency invalidation of the earlier "TPEx non-blocking (TWSE-only)" exemption. Authoritative master = TWSE ISIN `C_public.jsp` (strMode=2 上市 / strMode=4 上櫃; Big5 HTML, 市場別 column at cells[3]; reachable even when other TPEx endpoints 404). ALWAYS include a negative control — a code the master DOES classify TPEx (e.g. 6182 合晶) that is absent from the universe — to prove an all-TWSE result is a real property, not a parser artifact. Keep three fields separate in evidence: listing_venue (master) / provider (actual) / source_endpoint (actual API). Full recipe: `references/taiwan-isin-venue-master.md`.
- **Five-Clocks external closure needs semantic completeness, not non-null columns (verified 2026-08-13, DA-EXT-004 reopen).** The accepted conservative Daily-EOD model needs NO new columns: `event_time=asof; publication_time := availability_time := known_at := asof + 1 calendar day; ingest_time=retrieved_at; decision_time=consumer; bar visible iff availability_time <= decision_time`. Closure = (1) a clock-contract doc: mapping table + owner/source-backed equivalence statement + explicit conservative-consequence sentence + revision policy; (2) a causal-ordering checker (`known_at <= asof` count == 0, `retrieved_at date < asof` count == 0 — add as check_daily C11 via Codex); (3) same-day negative canary stays PASS. Materializing the semantic projection + checker closes the edge without rebuilding raw. Template in `references/taiwan-isin-venue-master.md`.
- **Scope-dependency invalidation guard (verified 2026-08-13 r3):** when new evidence CHANGES a scope claim (TWSE-only → TWSE+TPEx), re-check every previously-closed finding whose exemption was conditional on the OLD scope (DA-EXT-009's non-blocking was conditioned on TWSE-only). A0 scope authority decides the TARGET scope; it does NOT prove rows acquired, listing venue correct, or rights covering that provider — each needs its own exact evidence (receipts, master crosswalk, rights receipt scope field).
- **Terminal command hygiene (hardline blocklist, 3 blocks this session):** complex
  one-liners mixing `$()` subshells, embedded `"` quotes, and `sed` get rejected by the
  command parser. Prefer `search_files` for grep-style lookups, one simple command per
  check, and write multi-line logic to a script file instead of inline payloads.
- **Kanban duplicate-create (verified 2026-08-13 FAR):** `hermes kanban create --json | tail -3`
  truncates the id and re-running the create silently makes a SECOND task. If the id is
  not visible, run `kanban list` FIRST; archive the duplicate (`kanban archive <id>` —
  there is no delete).
- **Codex-written tests need `tests/__init__.py` (verified 2026-08-13 FAR):** without it,
  `unittest discover -s tests -t .` fails `Start directory is not importable` and
  `-m unittest tests/test_x.py` resolves to a non-importable dotted module. Smallest
  repair: Hermes adds an empty `tests/__init__.py` (record a defect id, e.g.
  FAR-CODEX-TESTPKG-001); do NOT rewrite the codex-authored test files.
- **`record_workorder_result` returns None (not a dict, verified 2026-08-13):** verify by
  re-SELECTing `workorders.state` (expect VERIFIED), never `.get()` on its return.
- **`register_evidence` is UNIQUE on evidence_id:** after regenerating a receipt, do NOT
  re-register the same id (IntegrityError) — register a NEW superseding id
  (`EVD-FAR-GATES-R2`), same pattern as PCIV-F01 manifests. Keep the old row.
- **`write_file` refuses SOUL.md (protected agent-instruction filename, verified 2026-08-13):**
  approval timeout = silence is not consent. Do NOT retry/bypass — record
  `NOT_WRITTEN_GUARDED` in evidence and ship the profile with the other files
  (config.yaml / distribution.yaml / README.runtime-contract.md).
- **write_file YAML validation rejects common patterns (verified 2026-08-13 FAR):**
  colon-in-scalar (`uses A2A (current: none)`), `#` starting a comment inside a flow
  sequence (`[#1288 ...]`), and plain text at column 0 under a `## heading` comment
  (parsed as a mapping key). Quote the value or indent under a real key.
- **Governed folder reorganization post-acceptance (verified 2026-08-14 FAR):** when the
  user asks to tidy a governed evidence folder ("檔案很雜亂"), (a) NEVER move frozen-identity
  files (externally-signed evidence MDs + final intake/subject/evidence manifests) or
  candidate-subject files (product code + subject-manifest configs) — their digests are
  externally accepted; verify with a hash check before/after (`sha256sum` identity set);
  (b) move only pure governance/evidence receipts into new `governance/` + `evidence/`
  subfolders (content unchanged → sha256 stable → evidence integrity preserved);
  (c) migrate spine EVD locators with a batch `UPDATE evidence_refs SET locator=? WHERE
  locator=?` — locators use WINDOWS BACKSLASH form (`C:\...\fabric-autonomous-research\FAR_x.json`);
  a posix-form (`C:/...`) match updates 0 rows; verify migrated count > 0;
  (d) update doc references (README/AGENTS/TEAM) with Python str.replace — sed `s|a|b|`
  breaks when the replacement text contains `|`; (e) record a
  `FAR_FOLDER_REORGANIZATION_RECEIPT.json` (moved counts, spine_locators_migrated,
  root_kept inventory) + EVD; (f) regenerate the directory tree (`tree -L 2 -I
  '__pycache__|aris-vendor'` or `find -maxdepth 2 | sort`) and deliver it as a file
  (`FAR_DIRECTORY_TREE.txt`) plus a summary in the reply. Root keeps only: entry docs +
  product code + frozen identity + candidate-subject configs; everything else moves.
- **Parallel-session skill-dir drift (verified 2026-08-13 FAR first-use):** other
  sessions on this machine share the Hermes skill dir + kanban DB + spine. Before
  creating a NEW reference/skill file, `ls -la` the skill references dir and grep
  SKILL.md — a concurrent session may already have documented the same recipe
  (observed: `shared-infra-team-implementation.md` appeared at 18:56 while this
  session planned a duplicate draft at 19:08; the challenge lane caught it). On
  redundancy: merge the unique delta into the existing file + delete the duplicate
  reuse-first; never ship a second parallel recipe). Also re-`skill_view`
  the SKILL.md before assuming prior content is still current. POST-CONSTRUCTION
  counterpart: if the overlap is discovered AFTER an upgrade landed, run
  `references/cross-session-integrity.md` (per-item survival verdicts + status-marker
  discipline) — this pitfall guards pre-build, that file guards post-build.
- **P0 tool registry row ≠ installed tool (verified 2026-08-13 MATT canary).**
  `INSTALLABLE_PROVIDER_TOOL` + `DEFAULT_ENABLED_AFTER_QUALIFICATION` + runtime
  `NOT_EXECUTED` = registered-but-not-enabled. "啟用 X" means running the TOOL-24-style
  pin→install→qualify route, not just confirming the row exists; keep the registry row
  honest until the formal qualification WO updates it.
- **CRLF patch-tool trap on Windows paths in skill/MD reference files (verified 2026-08-21,
  RBWI run, hit TWICE in rbwi-4plus1-pack-execution.md).** Editing a CRLF (Windows
  line-ending) .md/.mdx with the `patch` tool can split a Windows backslash path: a literal
  `evidence\rbwi-fullrun` gets consumed as `\r` = carriage return and written back as
  `evidence\r\nbwi-fullrun` (a 2-byte CRLF where only the `\rb` sub-path was intended) — the
  path then no longer resolves. This is exactly the documented class of "CRLF 斷行陷阱"
  (cross-session-integrity §6). Detection + fix, always bytes-level:
  ```python
  raw = open(p,'rb').read()
  print(raw.count(b'evidence\r\nbwi-fullrun'))            # >0 = broken
  raw = raw.replace(b'evidence\r\nbwi-fullrun', b'evidence\\rbwi-fullrun')
  open(p,'wb').write(raw)                                  # keep CRLF elsewhere intact
  ```
  Do NOT fix via `patch` again — new `\r` pairs can re-break. Verify by re-counting
  `raw.count(b'evidence\r\nbwi') == 0` after write. Applies to ANY Windows path
  (`evidence\rbwi`, `review\rbwi`, `docs\r…`) in a CRLF file.
- **`search_files` case-sensitive token hits can be substrings (`MATT` → `match`/`startswith`);**
  a claimed tool/skill requires a case-sensitive word-boundary check across HGK src +
  control/skills + Hermes skills dir + 知識庫 before declaring it absent, and the HGK
  registry CSV is the authoritative registration source.

- **A/B governed-vs-bare experiment confound (2026-08-24 MVLT-AB).** Comparing "pure Hermes" (ephemeral home, no skills, cold start) vs "governed Hermes" (canonical home, full skills, warm cache) means the manipulated variable IS NOT "governance on/off" — it is "governance + fresh/warm home + skills + cache" as a package. Must declare the confound upfront, use "observed under this confound structure" language, and NEVER attribute wall-clock/tool-call differences to governance alone. The ratio median and bootstrap CI (not just median) must be reported; N=3 ratios have extremely wide CIs (observed 0.245–1.524). Separate fixed_setup_sec from per_artifact_sec; report variable cost ratio as primary.

- **Kanban/Swarm execution surface creation ≠ closure (2026-08-24 MVLT-AB).** Creating a board + DAG + tasks does NOT satisfy the governed execution contract. Every run task must go through `assign → claim --ttl 1800 → heartbeat (with note) → complete --result "..."` with JSON receipts captured. Swarm lanes must be genuine `delegate_task` leaves (≥2 concurrent, overlap interval recorded, independent readback), NOT local checker calls. If Kanban tasks remain `ready`/`todo` and Swarm tasks `todo`, the governed round has an execution-method gap — report INCONCLUSIVE for traceability, do NOT claim PASS. The fresh-context AO lane MUST verify actual Kanban/Swarm receipts, not just artifact correctness.

- **OpenRouter free model rate limits in ephemeral homes (2026-08-24 MVLT-AB Mode A).** Ephemeral HERMES_HOME using OpenRouter `:free` models hit daily rate limits within 1-2 runs (HTTP 429 "free-models-per-day"). Mode A ephemeral homes MUST use the same valid canonical credentials (opencode-go API key + OpenRouter key from canonical `.env`) to ensure provider availability matches Mode B. Only the governance surface (skills/Kanban) should differ, not the credential path.

- **Evidence MD must reflect execution-method gaps honestly (2026-08-24 MVLT-AB).** When Kanban/Swarm surfaces were created but not closed, the evidence MD was updated to explicitly state: "WorkOrder and Kanban DAG were created; however, run and Swarm tasks remained ready/todo and were not claimed/completed... traceability lineage INCONCLUSIVE." This honest reporting is the correct evidence-only closure — never paper over gaps by claiming lineage=1.0. The three-root mirror (Fabric/HGK/SQS) must carry the same honest gap statement.

 - **Never write a number you did not measure in the same turn (verified SWOF W2 closure, twice).**
  A recorded regression/count that was hand-edited or copied from an earlier turn gets caught by the
  fresh checker and forces another round. Before any figure (test count, denominator, `Ran N tests`)
  goes into a receipt: run the exact quoted command THIS session and use ITS output. When the test set
  changes, re-measure — do not extrapolate "the same 4 + new" from memory.
- **`git commit -a` silently skips untracked files (verified SWOF W2).** A `git commit -am` on a
  worktree with new (untracked) source files commits nothing for them — HEAD stays at baseline while
  the apply-receipt claims a diff. Stage explicitly and assert staging is non-empty and in-scope
  before committing; the "tests moved but nothing changed in the diff" signal means the stage list is
  narrower than the admitted write-set.
- **The canonical HGK DB for governed records is `config/project.json -> canonical_database`
  (e.g. `var/shared-spine/hg-kseos.db`), NOT the project-scoped spine file you opened.**
  Registering TTs/issues/evidence in a project `.sqlite3` produces rows in the wrong volume; a
  read-only checker queries the canonical DB and reports the record absent. Resolve the canonical path
  from config FIRST, open exactly that DB read-only for verification, and re-read after write.
- **Request-controlled compatibility selector at a trust boundary is a fail-open blocker, not a
  convenience (verified SWOF R5 local_adapter).** A caller-settable field that substitutes an authn/
  privilege floor when the canonical field is missing is a downgrade: CRITICAL/AAC3 can receive AAC2.
  The fix is to DELETE the fallback so a missing canonical floor resolves None → DENY; a renamed
  `trusted_*` flag is the same bug. "No current in-repo caller" does NOT prove safety when the
  accepted public/API export surface exposes the downgrade-capable field.
- **Equal-rank external-review reports that disagree are QUARANTINED, then adjudicated by exact
  source repro — never picked by preference, majority, or date (verified SWOF R5).** When two
  same-rank challenge reports bind the same tuple, do NOT choose one. Run deterministic probes on the
  exact frozen bytes + frozen canonical authority, materialize an `_ADJUDICATION.json` with
  per-predicate evidence, then branch: blocker-confirmed (smallest repair) / nonblocking-current-scope
  (no product mutation) / unresolved (TEMP_CLOSED, no mutation). Full procedure:
  `references/equal-rank-external-conflict-adjudication.md`.
- **Two module identities for one import path break `isinstance` (verified SWOF R5 probe).** Loading
  a test file via `importlib.util.spec_from_file_location` while the same package is also on
  `sys.path` yields TWO distinct class objects, so `isinstance(token, ApprovalToken)` is False even
  for the "same" class. Source fixtures from the test module's own namespace, not a re-import.

- **Windows paths longer than 260 chars: `os.walk()` lists them, `open()` refuses them
 (verified on a 300+ char CJK-named corpus).** The inventory walk succeeds and then the read
 dies `FileNotFoundError: [Errno 2] No such file or directory` on exactly the long entries —
 listing and opening use different path-length rules, so the failure looks like a missing
 file rather than a path-length problem. Fix by opening through the extended-length marker:
 ```python
 def xopen(path, mode="rb"):
     p = os.path.abspath(path).replace("/", "\\")
     return open("\\\\?\\" + p, mode)        # literally: \\?\C:\...
 ```
 Apply it to EVERY corpus read (hash, line count, normalize), not just the file that failed —
 the same class of path recurs throughout the tree. The `\\?\` form needs a fully-qualified
 backslash path (no forward slashes); directory walks do not need it.


