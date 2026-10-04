# -*- coding: utf-8 -*-
"""FAR R1f: try XQ module data JSON/API paths + Google cache via other engines."""
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

# 1. XQ module page — fetch the module-compare page's astro chunks for module names
t = fetch("https://www.xq.com.tw/module-compare")
if not t.startswith("ERR"):
    # find astro js chunks
    for m in re.finditer(r'<script type="module"[^>]*src="([^"]+)"', t):
        src = m.group(1)
        if not src.startswith("http"):
            src = "https://www.xq.com.tw" + src
        js = fetch(src)
        if not js.startswith("ERR"):
            # module names in js
            names = set(re.findall(r'[\u4e00-\u9fff]{2,10}(?:進階|模組|即時|EOD|選股|量化|盤中|盤後|期權|海外|雲端|盯盤|下單)', js))
            if names:
                print(f"chunk {src[-40:]}: {sorted(names)[:20]}")
            # price-ish
            prices = re.findall(r'(\d{3,4})\s*元', js)
            if prices:
                print(f"  prices: {prices[:10]}")
