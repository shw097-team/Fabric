# -*- coding: utf-8 -*-
"""Fetch XQ lesson pages about 策略雷達."""
import html
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# XQ lesson search API / pages
for url in (
    "https://www.xq.com.tw/?s=" + urllib.parse.quote("策略雷達"),
    "https://www.xq.com.tw/lessons/",
):
    t = fetch(url)
    print(f"=== {url} len={len(t)} ===")
    links = re.findall(r'href="([^"]+)"[^>]*>([^<]{5,80})</a>', t)
    seen = set()
    for u, txt in links:
        txt = html.unescape(txt.strip())
        if ("雷達" in txt or "lesson" in u) and u not in seen and "xq.com" in u:
            seen.add(u)
            print(f"  {txt[:60]} -> {u[:100]}")
    if len(seen) == 0:
        # dump any anchor text around 策略
        m = re.findall(r"[^<>]{0,40}策略[^<>]{0,60}", re.sub(r"<[^>]+>", "|", t))
        for x in m[:5]:
            print("  text:", x.strip()[:120])
