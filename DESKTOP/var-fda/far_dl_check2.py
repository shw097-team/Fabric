# -*- coding: utf-8 -*-
"""FAR R2b: web search for XQ 3.19.03 installer / update server URL pattern."""
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# GitHub code/repo search for XQ update server patterns
for q in ("XQLite 3.19", "xq.com.tw update exe", "XQ 3.19.03", "xq 全球贏家 3.19"):
    t = fetch("https://api.github.com/search/repositories?q=" + urllib.parse.quote(q) + "&per_page=5")
    if t.startswith("ERR"):
        print(q, "->", t[:60])
        continue
    try:
        d = json.loads(t)
        print(f"=== {q} ({d.get('total_count', 0)}) ===")
        for r in d.get("items", [])[:5]:
            print(f"  {r['full_name']} | {(r.get('description') or '')[:60]}")
    except Exception as e:
        print(q, "-> parse err", str(e)[:40])

# try XQ update server pattern guesses
for url in ("https://update.xq.com.tw/", "https://www.xq.com.tw/api/version", "https://sysjust.com.tw/download"):
    t = fetch(url)
    if not t.startswith("ERR") and t:
        print(f"=== {url} ({len(t)} bytes) ===")
        for m in re.finditer(r"3\.\d{1,2}\.\d{1,2}", t):
            print("  version:", m.group(0))
    else:
        print(url, "->", t[:60])
