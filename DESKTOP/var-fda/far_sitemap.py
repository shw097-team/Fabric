# -*- coding: utf-8 -*-
"""FAR R1l: XQ sitemap + YouTube search for module intro videos."""
import html
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

# sitemap
for s in ("https://www.xq.com.tw/sitemap.xml", "https://www.xq.com.tw/sitemap-index.xml", "https://www.xq.com.tw/sitemap-0.xml"):
    t = fetch(s)
    if not t.startswith("ERR") and "<url>" in t:
        print(f"=== {s} ===")
        urls = re.findall(r"<loc>([^<]+)</loc>", t)
        for u in urls:
            if any(k in u for k in ("module", "price", "pricing", "plan", "subscribe", "feature")):
                print("  ", u)
        break
