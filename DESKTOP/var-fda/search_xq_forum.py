# -*- coding: utf-8 -*-
"""Search XQ forum internal search + fetch thread."""
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

# try forum search endpoints
for url in (
    "https://forum.xq.com.tw/?s=" + urllib.parse.quote("策略雷達 啟動"),
    "https://forum.xq.com.tw/search/" + urllib.parse.quote("策略雷達 啟動"),
):
    t = fetch(url)
    print(f"=== {url[:60]} len={len(t)} ===")
    if t.startswith("ERR"):
        print(" ", t[:80])
        continue
    clean = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", clean)
    text = html.unescape(re.sub(r"\s+", " ", text))
    # find sentences about 啟動/按鈕
    hits = re.findall(r"[^。；]{0,40}(?:啟動|執行|按鈕)[^。；]{0,90}", text)
    seen = set()
    for h in hits:
        h = h.strip()
        if len(h) > 25 and h not in seen and "策略" in h or "雷達" in h:
            seen.add(h)
            print("  ", h[:150])
    if not seen:
        print("  (no hits; title:", text[:100], ")")
    print()
