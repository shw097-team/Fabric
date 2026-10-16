# Python Security Review — adversarial probe patterns (SSRF / XML / truncation)

Verified 2026-08-14 on WO-FAR-HARDENING-001 (focused hardening of the FAR tri-source
retrieval layer: far_retrieval.py / far_trisource.py). Class of task: independent
security-review lane of Python network/XML code inside a governed acceptance.
Read-only: run probes as in-memory heredoc python (`python -c "..."` / stdin), never
write probe files into the governed tree.

## Golden rule: probe empirically, don't assert

Static reading of a validator misses real gaps. The 6to4 gap below was found ONLY by
running the classifier against literal addresses. Always execute the adversarial
matrix against the live functions.

## SSRF validator probe matrix (scheme allowlist + host allowlist + resolved-IP class)

Probe every case; expected results verified 2026-08-14 (allowed root `arxiv.org`):

| case | result |
|---|---|
| `https://export.arxiv.org/api/query?x=1` | ALLOW |
| `http://…` (any http) | DENY (https-only) |
| `file:///etc/passwd`, `ftp://`, `gopher://`, `data:text/html,…`, `ws://`, `wss://` | DENY |
| `https://127.0.0.1/x`, `https://[::1]/x`, `https://10.0.0.5/x`, `https://169.254.169.254/…` | DENY (IP literals fail host allowlist AND/OR IP class) |
| `https://evil.com/x` | DENY |
| `https://arxiv.org.evil.com/x` (suffix trick) | DENY — correct `endswith("." + root)` pattern |
| `https://evilarxiv.org/x` (no dot) | DENY — the dot requirement blocks this |
| `https://export.arxiv.org@evil.com/x` (userinfo) | DENY — urlparse hostname = evil.com |
| `https://export.arxiv.org:8443/x` | ALLOW — port NOT restricted (INFO finding; host still allowlisted so not SSRF) |

IP classifier checks (deny list): loopback, private/RFC1918, link-local, unspecified,
multicast, reserved, `is_global is False` (catches CGNAT 100.64/10, benchmark 198.18/15,
doc ranges `2001:db8::`), explicit `169.254.169.254`. Multi-A fail-closed: ANY bad IP
in the resolution set → DENY (verify this — a permissive `any()` instead of `all()`
here is a critical finding).

### Known gap class: 6to4 / Teredo-embedded addresses (FAR-SEC-02, LOW)

`2002:7f00:1::1` (6to4-embedded 127.0.0.1) and `2001:0000::/32` Teredo variants return
ALLOW on Python 3.11 `ipaddress` — `is_private`/`is_global` don't cover the embedded
IPv4. Fix: also deny when `ip.version == 6 and (ip.sixtofour or ip.teredo)` unless the
embedded IPv4 itself is global. Exploitability gated by the strict host allowlist
(attacker would need DNS control over an allowlisted root) → LOW, not blocking.
Note `::ffff:127.0.0.1` (IPv4-mapped) IS correctly denied on 3.11.

### DNS-rebinding TOCTOU (FAR-SEC-01, LOW)

`_validate_url` resolves+classifies the host, then `urllib.request` re-resolves at
connect time — a resolver answering public-IP at validation and private-IP at connect
bypasses the check. Same TOCTOU applies per redirect hop (handler re-validates the
target URL, urllib re-resolves). Mitigation: resolve once and pin the connection
socket to the validated IP; otherwise document the host allowlist as the compensating
control. Always check the redirect handler: per-hop re-validation must re-run scheme +
host + resolved-IP on the NEW url (`redirect_request` override), not just on the
initial URL.

## XML DTD / entity / XInclude probes

ElementTree (`xml.etree.ElementTree`) is the safe baseline: it sets no external-entity
handlers (expat won't fetch), and it never processes XInclude unless `.XInclude()`
is explicitly invoked. Two probe shapes:

1. **Window-bypass smuggle:** a pre-reject scanning only the first N bytes
   (`if b"<!DOCTYPE" in data[:4096]`) is a FAST PATH, not the guarantee. Push the
   DOCTYPE past the window with a huge prolog comment:
   `b'<?xml version="1.0"?>' + b'<!--' + b'x'*5000 + b'-->' + b'<!DOCTYPE lolz [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>' + b'<feed …><entry><title>&xxe;</title>…`
   → ElementTree raises `ParseError: undefined entity &xxe;` — no fetch. Safe by
   parser defaults; the window check is defense-in-depth.
2. **Entity-bomb chain:** nested internal entities `a0="lol"`, `aN=&a(N-1);*10`, refs
   `&a9;&a9;` → expat ≥2.4 (bundled with Python 3.11) raises
   `ParseError: limit on input amplification factor (from DTD and entities) breached`
   in ~0.1 s. DO NOT test with a tiny chain (5×5 expands fine and "passes") — use a
   genuinely explosive chain (9-10 levels) or you'll falsely conclude the bomb
   protection is missing.

Also verify the positive case: HTML5 `<!DOCTYPE html>` must be ACCEPTED when the
content-type is `text/html`/`application/xhtml+xml` (content-type semantics: doctype
allowed for HTML-as-inert-text, rejected for XML) — and that HTML is never parsed/
executed downstream (entries only come from the Atom parser).

## Truncation / completeness semantics (256KB class)

- `response.read(256 * 1024)` caps the read; a receipt function must flag
  `content_complete: False` with a reason: `BYTE_CAP` (>cap), `SERVER_ABORT`
  (Content-Length > received), `CONTENT_LENGTH_UNKNOWN` (received == cap, no header —
  conservative fail-closed even if the body might be exactly complete).
- Edge verified: exactly-cap bytes WITH `Content-Length: 262144` → complete=True
  (correct); exactly-cap WITHOUT header → flagged incomplete (conservative).
- Truncation semantics gate negative inference: `content_complete=False` forbids a
  full-document-absence claim (test asserts reason ∈ the three codes). A truncated
  positive result may support only what was observed.

## Output shape (AO security lane)

Findings table (id, severity LOW/INFO/MED/CRIT, verbatim quote with line ref, concrete
fix) + AO item PASS/FAIL table + final two lines:
`SECURITY_VERDICT=…` and `ACCEPTANCE_OFFICER_VERDICT=PASS|FAIL`.
Verdicts used 2026-08-14: `SECURITY_VERDICT=PASS_WITH_LOW_INFO_FINDINGS`
(2 LOW / 3 INFO, non-blocking) → `ACCEPTANCE_OFFICER_VERDICT=PASS`.

## Hardening-round verification specifics (AO H-items, WO-FAR-HARDENING-001)

- **Test denominator recompute:** run `python -m unittest discover -s tests -t .`,
  then recompute the exact expected count via `unittest.TestLoader().discover(...)`
  walking nodeids; compare count AND `sha256("\n".join(sorted(nodeids)))` against the
  stored TEST_DENOMINATOR.json (`nodeids_digest`). A canary script may do this itself
  — re-running it is safe because the denominator is deterministic (digest stable
  across runs = recomputable evidence).
- **Canary re-run is read-only-safe:** canaries that regenerate their own output JSON
  in the canary dir are deterministic; verify on-disk content after re-run (digest
  unchanged) rather than trusting the pre-existing JSON.
- **Spine DB live read (read-only):**
  `sqlite3.connect('file:C:/…/hg-kseos.db?mode=ro', uri=True)` — never open the spine
  read-write from a verify lane. WO→rollback_pointer check:
  `SELECT rollback_pointer FROM workorders WHERE workorder_id='WO-…'`.
- **Mirror byte-identity:** sha256 every claimed mirror (Fabric/HGK/SQS evidence\review)
  and require equality; compare against the documented "canonical current" hash, and
  check the historical-baseline doc actually contains the historical hash
  (`grep 58de0815 FAR_R8_HISTORICAL_BASELINE.md` style) — a documented supersession
  chain (immutable verdict, additive updates) is legitimate; byte-exact r8 restoration
  is NOT expected.
- **"No new platform" grep semantics:** banned-lib grep (crawl4ai/firecrawl/neo4j/
  qdrant/playwright…) over the repo hits policy receipts (qdrant/neo4j
  `PRESERVE_DEFAULT_OFF` disposition docs) and pre-existing vendored skill trees —
  distinguish those from actual code imports; scope the claim to the hardening code
  (stdlib-only import check on the changed modules).
- **Mutation=0 evidence (SQS Financial Truth / live broker):** negative-side-effect
  receipt fields (`sqs_financial_truth_mutation: 0`, `live_broker_write: 0` with
  their check text), plus zero sqs/broker/trading tokens in the changed modules, plus
  a deny-guard (`BROKER_WRITE_DENIED`) — three independent layers.
