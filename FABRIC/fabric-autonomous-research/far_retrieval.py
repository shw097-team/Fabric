"""FAR automatic tri-source retrieval layer (deterministic, stdlib only).

Retrieves governed local corpus documents, HGK shared-spine memory rows, and
read-only arXiv web entries for a question, then emits a cross-reference
ledger. It never writes outside out_dir, never sends credentials, never
mutates remote state, and outputs stay candidates until verified.
"""

import datetime
import hashlib
import json
import os
import re
import sqlite3
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

KB_ROOTS = (
    r"C:/Projects/Agent_Workspace/知識庫/HG-KSEOS_SSOT",
    r"C:/Projects/Agent_Workspace/知識庫/實作相關DOC",
    r"C:/Projects/Agent_Workspace/知識庫/工程基座",
    r"C:/Projects/Agent_Workspace/知識庫/Obsidian投影",
    r"C:/Projects/Agent_Workspace/知識庫/專業技術文檔",
    r"C:/Projects/Agent_Workspace/知識庫/GENIE",
    r"C:/Projects/Agent_Workspace/知識庫/HG-KSEOS資料庫",
    r"C:/Projects/Agent_Workspace/知識庫/SQS-THC資料庫",
    r"C:/Projects/Agent_Workspace/知識庫/教程字幕",
)

DEFAULT_SPINE_DB = r"C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db"

SKIP_SEGMENTS = {".git", ".venv", ".venv-data", "node_modules", "__pycache__", ".cache"}
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".parquet", ".db", ".pyc", ".xlsx", ".docx", ".pptx"}
MAX_FILE_SIZE = 2 * 1024 * 1024
MAX_SCAN_FILES = 2000
SURFACE_READ_SIZE = 60 * 1024
BODY_SLICE = 1500
SNIPPET_LENGTH = 200

last_web_status = "NOT_RUN"

_CJK_RUN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
_ASCII_WORD = re.compile(r"[a-z0-9]+")


def tokenize(text):
    """Return unique lowercase alnum words and CJK bigrams from text."""
    tokens = []
    seen = set()

    def _add(token):
        if token and token not in seen:
            seen.add(token)
            tokens.append(token)

    for match in _CJK_RUN.finditer(text):
        run = match.group(0)
        for i in range(len(run) - 1):
            _add(run[i:i + 2])
    for match in _ASCII_WORD.finditer(text.lower()):
        _add(match.group(0))
    return tokens


def score_doc(text, question_tokens):
    """Return the count of question tokens present in the document surface."""
    haystack = text.lower()
    return sum(1 for token in question_tokens if token in haystack)


def _doc_surface(path, body):
    """Assemble filename words, first three heading lines, and body slice."""
    parts = [" ".join(tokenize(path.stem))]
    headings = []
    for line in body.splitlines():
        if line.lstrip().startswith("#"):
            headings.append(line)
            if len(headings) == 3:
                break
    parts.append("\n".join(headings))
    parts.append(body[:BODY_SLICE])
    return "\n".join(parts)


def _file_sha256(path):
    """Return the sha256 hex digest of the full file bytes."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def retrieve_knowledge_base(question, top_k=8, roots=KB_ROOTS, max_files=MAX_SCAN_FILES):
    """Walk governed KB roots and return the top scoring local documents (bounded, deterministic)."""
    tokens = tokenize(question)
    if not tokens or not roots:
        return []
    results = []
    examined = 0
    for root in roots:
        root_path = Path(root)
        if not root_path.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = sorted(name for name in dirnames if name not in SKIP_SEGMENTS)
            for filename in sorted(filenames):
                path = Path(dirpath) / filename
                if any(part in SKIP_SEGMENTS for part in path.parts):
                    continue
                if path.suffix.lower() in BINARY_EXTENSIONS:
                    continue
                examined += 1
                if examined >= max_files:
                    return sorted(results, key=lambda r: (-r["score"], r["source_id"]))[:top_k]
                try:
                    if path.stat().st_size > MAX_FILE_SIZE:
                        continue
                    with open(path, "rb") as handle:
                        head = handle.read(SURFACE_READ_SIZE)
                except OSError:
                    continue
                body = head.decode("utf-8", errors="replace")
                score = score_doc(_doc_surface(path, body), tokens)
                if score <= 0:
                    continue
                try:
                    sha256 = _file_sha256(path)
                except OSError:
                    continue
                results.append({
                    "source_id": str(path).replace("\\", "/"),
                    "path": str(path).replace("\\", "/"),
                    "sha256": sha256,
                    "score": score,
                    "role": "LOCAL_GOVERNED_CORPUS",
                    # FH-01 lineage
                    "origin_artifact_id": str(path).replace("\\", "/"),
                    "origin_artifact_digest": sha256,
                    "source_family": "FABRIC_HGK_KNOWLEDGE",
                    "derivation_kind": "CANONICAL",
                })
    results.sort(key=lambda row: (-row["score"], row["path"]))
    return results[:top_k]


def retrieve_memory(question, top_k=8, spine_db=None):
    """Query the HGK shared-spine knowledge FTS and memory tables."""
    if spine_db is None:
        spine_db = DEFAULT_SPINE_DB
    tokens = tokenize(question)
    if not tokens:
        return []
    results = []
    seen = set()
    status = "OK"
    try:
        spine_path = Path(spine_db)
        if not spine_path.exists():
            status = "SPINE_DB_MISSING"
            return results
        connection = sqlite3.connect("file:%s?mode=ro" % spine_path.as_posix(), uri=True)
        try:
            cursor = connection.cursor()
            match = " OR ".join('"%s"' % token for token in tokens)
            try:
                rows = cursor.execute(
                    "SELECT doc_id, title, body FROM knowledge_fts "
                    "WHERE knowledge_fts MATCH ? LIMIT 500",
                    (match,),
                ).fetchall()
            except sqlite3.Error:
                rows = []
            if not rows:
                like_rows = []
                for token in tokens[:3]:
                    like_rows.extend(cursor.execute(
                        "SELECT doc_id, title, body FROM knowledge_docs "
                        "WHERE title LIKE ? OR body LIKE ? LIMIT 200",
                        ("%" + token + "%", "%" + token + "%"),
                    ).fetchall())
                rows = like_rows
            for doc_id, title, body in rows:
                score = score_doc(title + " " + body[:BODY_SLICE], tokens)
                if score > 0 and doc_id not in seen:
                    seen.add(doc_id)
                    results.append({
                        "source_id": doc_id,
                        "title": title,
                        "snippet": body[:SNIPPET_LENGTH],
                        "score": score,
                        "role": "MEMORY",
                        # FH-01 lineage: FTS projection of knowledge_docs doc_id (same origin family)
                        "origin_artifact_id": doc_id,
                        "origin_artifact_digest": None,
                        "source_family": "FABRIC_HGK_KNOWLEDGE",
                        "derivation_kind": "FTS_INDEX",
                    })
            for token in tokens[:3]:
                for memory_id, scope, body in cursor.execute(
                    "SELECT memory_id, scope, body FROM memory_records "
                    "WHERE scope LIKE ? OR body LIKE ?",
                    ("%" + token + "%", "%" + token + "%"),
                ).fetchall():
                    score = score_doc(scope + " " + body[:BODY_SLICE], tokens)
                    if score > 0 and memory_id not in seen:
                        seen.add(memory_id)
                        results.append({
                            "source_id": memory_id,
                            "title": scope,
                            "snippet": body[:SNIPPET_LENGTH],
                            "score": score,
                            "role": "MEMORY",
                            # FH-01 lineage: memory summary (provenance text = origin pointer)
                            "origin_artifact_id": memory_id,
                            "origin_artifact_digest": None,
                            "source_family": "HGK_MEMORY",
                            "derivation_kind": "MEMORY_SUMMARY",
                        })
        finally:
            connection.close()
    except Exception as exc:
        status = "ERROR"
    if status == "ERROR" and not results:
        return []
    results.sort(key=lambda row: (-row["score"], row["source_id"]))
    return results[:top_k]


def _parse_atom(data):
    """Parse an Atom feed into entry dicts with title, summary, id, updated (DOCTYPE/entity-safe)."""
    if b"<!DOCTYPE" in data[:4096] or b"<!ENTITY" in data[:4096]:
        raise ValueError("feed declares DOCTYPE/ENTITY; rejected as untrusted")
    namespace = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)
    entries = []
    for node in root.findall("a:entry", namespace):
        title = (node.findtext("a:title", default="", namespaces=namespace) or "").strip()
        summary = (node.findtext("a:summary", default="", namespaces=namespace) or "").strip()
        entry_id = (node.findtext("a:id", default="", namespaces=namespace) or "").strip()
        updated = (node.findtext("a:updated", default="", namespaces=namespace) or "").strip()
        entries.append({
            "source_id": entry_id,
            "url": entry_id,
            "title": title,
            "snippet": summary[:SNIPPET_LENGTH],
            "updated": updated,
        })
    return entries


class _AllowedHostsRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler that only follows redirects to allowed hosts."""

    def __init__(self, allowed_roots):
        self.allowed_roots = [str(root).lower() for root in allowed_roots]
        urllib.request.HTTPRedirectHandler.__init__(self)

class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """FH-02 / EXT-FAR-TS-HARD-001: automatic redirects DISABLED (frozen-plan smallest path).

    Any redirect (same-host included) is denied -> strict allowlist + pre-connect IP
    validation + no redirect chain (no DNS-rebinding window via redirect hops).
    """
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("redirects disabled (EXT-FAR-TS-HARD-001): %s" % newurl[:120])


DENIED_SCHEMES = ("file", "ftp", "gopher", "data", "ws", "wss")


def _resolve_and_classify_ip(host):
    """Resolve host and classify IPs (FH-02 SSRF: deny loopback/private/link-local/metadata/etc)."""
    import ipaddress, socket
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except Exception:
        return None
    ips = []
    for info in infos:
        try:
            ips.append(ipaddress.ip_address(info[4][0]))
        except ValueError:
            continue
    if not ips:
        return None
    for ip in ips:
        embedded_non_global = False
        try:
            if ip.version == 6 and (ip.sixtofour or ip.teredo):
                # FAR-SEC-02: 6to4/Teredo may embed a non-global IPv4 (e.g. 2002:7f00:1::1 -> 127.0.0.1)
                v4 = ip.sixtofour if ip.sixtofour else (ip.teredo[0] if ip.teredo else None)
                embedded_non_global = bool(v4 and (v4.is_private or v4.is_loopback or v4.is_link_local))
        except Exception:
            pass
        if (ip.is_loopback or ip.is_private or ip.is_link_local or ip.is_unspecified
                or ip.is_multicast or ip.is_reserved or embedded_non_global
                or (ip.is_global is False and not ip.is_private and not ip.is_loopback)
                or str(ip) == "169.254.169.254"):  # cloud metadata endpoint
            return ("DENY", str(ip))
    return ("ALLOW", ",".join(str(ip) for ip in ips[:3]))


def _validate_url(url, allowed_roots):
    """FH-02 SSRF validator: scheme allowlist + exact-host + DNS/IP classification."""
    parts = urllib.parse.urlparse(url)
    scheme = (parts.scheme or "").lower()
    if scheme in DENIED_SCHEMES:
        return False
    if scheme != "https":
        return False
    if parts.port is not None and parts.port != 443:  # FAR-SEC-03: restrict to default HTTPS port
        return False
    host = (parts.hostname or "").lower()
    if not host or not any(host == root or host.endswith("." + root) for root in allowed_roots):
        return False
    verdict = _resolve_and_classify_ip(host)
    if verdict is None or verdict[0] != "ALLOW":
        return False
    return True


def _truncation_receipt(data, headers=None, cap=256 * 1024):
    """FH-03: content completeness/truncation semantics for a fetched body."""
    known = None
    if headers is not None:
        cl = headers.get("Content-Length")
        if cl and cl.isdigit():
            known = int(cl)
    received = len(data)
    if received > cap:
        return {"bytes_received_or_known": known, "bytes_read": received,
                "byte_cap": cap, "content_complete": False, "truncation_reason": "BYTE_CAP"}
    if known is not None and received < known:
        return {"bytes_received_or_known": known, "bytes_read": received,
                "byte_cap": cap, "content_complete": False, "truncation_reason": "SERVER_ABORT"}
    if known is None and received >= cap:
        return {"bytes_received_or_known": None, "bytes_read": received,
                "byte_cap": cap, "content_complete": False, "truncation_reason": "CONTENT_LENGTH_UNKNOWN"}
    return {"bytes_received_or_known": known, "bytes_read": received,
            "byte_cap": cap, "content_complete": True, "truncation_reason": "NONE"}


def _content_type_semantics(content_type):
    """FH-02: MIME-aware content decision. HTML doctype allowed for HTML; XML DTD rejected."""
    ct = (content_type or "").lower()
    if "text/html" in ct or "application/xhtml+xml" in ct:
        return "HTML", "normal HTML doctype allowed; parsed as inert content (no script execution)"
    if "application/xml" in ct or "text/xml" in ct or "application/atom+xml" in ct or "application/rss+xml" in ct:
        return "XML", "untrusted XML: DTD/external entities/XInclude disabled; rejected if unsafe"
    if "application/json" in ct:
        return "JSON", "parsed as inert data"
    if "text/plain" in ct:
        return "TEXT", "inert text"
    return "UNKNOWN", "no HTML parser guess for load-bearing evidence"


def retrieve_web(question, allowed_roots=None, top_k=5, fetch_fn=None):
    """Return governed read-only arXiv results for allowed roots only."""
    global last_web_status
    if not allowed_roots:
        last_web_status = "WEB_RETRIEVAL_SKIPPED_NO_ROOTS"
        return []
    words = [token for token in tokenize(question) if re.fullmatch(r"[a-z0-9]+", token)]
    cjk_tokens = [token for token in tokenize(question) if not re.fullmatch(r"[a-z0-9]+", token)]
    arxiv_roots = [root for root in allowed_roots if "arxiv.org" in str(root)]
    if not arxiv_roots or not (words or cjk_tokens):
        last_web_status = "SKIPPED"
        return []
    query_terms = (words + cjk_tokens)[:5]
    query = "+AND+".join(query_terms)
    url = ("https://export.arxiv.org/api/query?search_query=all:%s&max_results=%d"
           % (query, top_k))
    if not _validate_url(url, arxiv_roots):  # FH-02: validate initial URL before connect
        last_web_status = "BLOCKED_BY_AUTHORITY"
        return [{"source_id": "WEB-BLOCKED", "url": url, "title": "",
                 "snippet": "initial URL failed SSRF validation", "score": 0, "role": "WEB"}]
    entries = []
    failed = False
    seen_urls = set()
    for root in arxiv_roots:
        if url in seen_urls:
            continue
        seen_urls.add(url)
        try:
            if fetch_fn is not None:
                data = fetch_fn(url)
                content_type = "application/atom+xml"
                headers = None
            else:
                opener = urllib.request.build_opener(
                    _NoRedirectHandler())  # EXT-FAR-TS-HARD-001: redirects disabled
                with opener.open(url, timeout=30) as response:
                    content_type = response.headers.get("Content-Type") or ""
                    headers = response.headers
                    data = response.read(256 * 1024)
            parsed = _parse_atom(data)  # XML DTD/entity rejection applies (FH-02/05)
            ct_kind, ct_note = _content_type_semantics(content_type)
            trunc = _truncation_receipt(data, headers)
            if not parsed and cjk_tokens and words:
                # graceful degradation: CJK-only query returned nothing; retry ascii-only terms
                fallback_url = ("https://export.arxiv.org/api/query?search_query=all:%s&max_results=%d"
                                % ("+AND+".join(words[:3]), top_k))
                if not _validate_url(fallback_url, arxiv_roots):
                    raise RuntimeError("fallback URL failed SSRF validation")
                if fetch_fn is not None:
                    data = fetch_fn(fallback_url)
                else:
                    with opener.open(fallback_url, timeout=30) as response:
                        content_type = response.headers.get("Content-Type") or ""
                        headers = response.headers
                        data = response.read(256 * 1024)
                parsed = _parse_atom(data)
                trunc = _truncation_receipt(data, headers)
                url = fallback_url
        except Exception as exc:
            failed = True
            entries.append({
                "source_id": "WEB-FAIL",
                "url": url,
                "title": "",
                "snippet": str(exc)[:120],
                "score": 0,
                "role": "WEB",
            })
            continue
        for index, item in enumerate(parsed):
            item["score"] = max(1, 10 - index)
            item["role"] = "WEB"
            item["content_type_kind"] = ct_kind
            item["content_type_note"] = ct_note
            item["content_read"] = trunc
            item["origin_artifact_id"] = item.get("source_id")
            item["origin_artifact_digest"] = None
            item["source_family"] = "EXTERNAL_WEB"
            item["derivation_kind"] = "WEB_PRIMARY"
            entries.append(item)
    last_web_status = "PARTIAL_FAIL" if failed else "OK"
    return entries


def _channel_terms(rows):
    """Return a dict mapping each meaningful token to the number of rows containing it."""
    counts = {}
    for row in rows:
        surface = "%s %s" % (row.get("title", "") or "", row.get("snippet", "") or "")
        for token in set(tokenize(surface)):
            if len(token) < 2 or token.isdigit():
                continue
            counts[token] = counts.get(token, 0) + 1
    return counts


def build_cross_reference(kb_rows, mem_rows, web_rows):
    """Build deterministic agreement and disagreement rows across channels."""
    channels = (("KB", kb_rows), ("MEMORY", mem_rows), ("WEB", web_rows))
    rows = []
    for left_index in range(3):
        for right_index in range(left_index + 1, 3):
            left_name, left_rows = channels[left_index]
            right_name, right_rows = channels[right_index]
            left_terms = _channel_terms(left_rows)
            right_terms = _channel_terms(right_rows)
            for term in sorted(set(left_terms) & set(right_terms)):
                rows.append({
                    "channel_a": left_name,
                    "channel_b": right_name,
                    "term": term,
                    "count_a": left_terms[term],
                    "count_b": right_terms[term],
                    "agreement": True,
                    "disagreement": False,
                    "note": "",
                })
            left_token_sets = [
                set(tokenize(row.get("snippet", "") or ""))
                for row in left_rows if row.get("score", 0) > 0
            ]
            right_token_sets = [
                set(tokenize(row.get("snippet", "") or ""))
                for row in right_rows if row.get("score", 0) > 0
            ]
            for left_set in left_token_sets:
                for right_set in right_token_sets:
                    if not (left_set & right_set):
                        rows.append({
                            "channel_a": left_name,
                            "channel_b": right_name,
                            "term": "(none)",
                            "count_a": 0,
                            "count_b": 0,
                            "agreement": False,
                            "disagreement": True,
                            "note": "no-overlap flag for human review",
                        })
    rows.sort(key=lambda row: (row["channel_a"], row["channel_b"], row["term"]))
    return rows


def run_retrieval_stage(question, workorder_ref, out_dir, spine_db=None,
                        allowed_web_roots=None, top_k=8, roots=KB_ROOTS, max_files=MAX_SCAN_FILES):
    """Run the tri-source retrieval stage and write both ledger files."""
    kb_rows = retrieve_knowledge_base(question, top_k=top_k, roots=roots, max_files=max_files)
    mem_rows = retrieve_memory(question, top_k=top_k, spine_db=spine_db)
    web_rows = retrieve_web(question, allowed_roots=allowed_web_roots, top_k=top_k)
    cross_rows = build_cross_reference(kb_rows, mem_rows, web_rows)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    ledger_path = out_path / "RetrievalLedger.json"
    cross_path = out_path / "CrossReferenceLedger.tsv"
    ledger = {
        "schema": "FAR-RETRIEVAL-LEDGER/1",
        "workorder_ref": workorder_ref,
        "question": question,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "channels": {
            "knowledge_base": kb_rows,
            "memory": mem_rows,
            "web": web_rows,
        },
        "web_status": last_web_status,
        "cross_reference_count": len(cross_rows),
        "files": {
            "ledger": str(ledger_path),
            "cross_reference": str(cross_path),
        },
    }
    ledger_path.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(cross_path, "w", encoding="utf-8", newline="") as handle:
        handle.write("channel_a\tchannel_b\tterm\tcount_a\tcount_b\t"
                     "agreement\tdisagreement\tnote\n")
        for row in cross_rows:
            note = str(row["note"]).replace("\t", " ").replace("\r", " ").replace("\n", " ")
            handle.write("%s\t%s\t%s\t%d\t%d\t%s\t%s\t%s\n" % (
                row["channel_a"], row["channel_b"], row["term"],
                row["count_a"], row["count_b"],
                str(row["agreement"]), str(row["disagreement"]), note))
    return {
        "retrieval_count": len(kb_rows) + len(mem_rows) + len(web_rows),
        "cross_reference_count": len(cross_rows),
        "web_status": last_web_status,
        "files": {
            "ledger": str(ledger_path),
            "cross_reference": str(cross_path),
        },
    }
