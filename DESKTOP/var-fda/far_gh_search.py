# -*- coding: utf-8 -*-
"""FAR R2: XQ official GitHub + repo discovery via GitHub API."""
import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# GitHub org/user search for XQ / XS / 嘉實 (XQ maker)
for q in ("XQ org:xq", "user:xqinfo", "org:xqinfo", "嘉實 XQ", "XScript XQ"):
    t = fetch("https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + "&per_page=8")
    if t.startswith("ERR"):
        print(q, "->", t[:60])
        continue
    try:
        d = json.loads(t)
        print(f"=== {q} ({d.get('total_count', 0)} hits) ===")
        for r in d.get("items", [])[:8]:
            print(f"  {r['full_name']} | {r.get('language')} | {(r.get('description') or '')[:70]}")
    except Exception as e:
        print(q, "-> parse err", str(e)[:50])
    print()
