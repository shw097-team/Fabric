# -*- coding: utf-8 -*-
"""Search XQ radar usage via Bing + XQ official site (newest)."""
import html
import re
import urllib.parse
import urllib.request
import time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

# Bing
t = fetch("https://www.bing.com/search?q=" + urllib.parse.quote(
    "XQ 策略雷達 啟動 執行 按鈕 功能列 教學"))
clean = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
text = re.sub(r"<[^>]+>", " ", clean)
text = html.unescape(re.sub(r"\s+", " ", text))
hits = re.findall(r"[^。；]{0,50}(?:啟動|執行|雷達)[^。；]{0,110}", text)
print("=== BING ===")
seen = set()
for h in hits:
    h = h.strip()
    if len(h) > 30 and h not in seen:
        seen.add(h)
        print("  ", h[:170])
    if len(seen) >= 6:
        break

# XQ official lesson list — find radar-related newer lessons
time.sleep(2)
t2 = fetch("https://www.xq.com.tw/lesson/sensor/")
links = re.findall(r'href="([^"]+)"[^>]*>([^<]{4,70})</a>', t2)
print("\n=== XQ SENSOR LESSONS ===")
for u, txt in links:
    txt = html.unescape(txt.strip())
    if txt and ('雷達' in txt or '警示' in txt):
        print("  ", txt[:60], "->", u[:90])
