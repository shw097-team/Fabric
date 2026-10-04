# -*- coding: utf-8 -*-
"""FAR R2b: YouTube search for XQ module intro (channel @XQ--xq)."""
import html
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# youtube search
for q in ("XQ 全球贏家 模組 介紹", "XQ 模組比較 訂閱"):
    t = fetch("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    if t.startswith("ERR"):
        print(q, "->", t[:50])
        continue
    vids = re.findall(r'"videoId":"([^"]+)"', t)
    titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', t)
    print(f"=== {q} ({len(vids)} vids) ===")
    for v, ti in list(zip(vids, titles))[:8]:
        print(f"  {ti[:60]} | https://youtu.be/{v}")
