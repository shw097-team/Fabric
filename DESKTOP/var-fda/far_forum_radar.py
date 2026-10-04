# -*- coding: utf-8 -*-
"""FAR R2d: fetch XQ forum threads about radar + XQ official blog on radar automation."""
import html
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

def ddg_urls(q, maxn=6):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    t = fetch(url)
    if t.startswith("ERR"):
        return []
    out = []
    for m in re.finditer(r'result__a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t, re.S):
        href = m.group(1)
        out.append(href)
        if len(out) >= maxn:
            break
    return out

# forum threads on radar usage problems
for q in ("site:forum.xq.com.tw 策略雷達 啟動", "site:forum.xq.com.tw 策略雷達 無法啟動"):
    urls = ddg_urls(q, 5)
    print(f"=== {q} ===")
    for u in urls:
        print("  ", u[:110])
    print()
