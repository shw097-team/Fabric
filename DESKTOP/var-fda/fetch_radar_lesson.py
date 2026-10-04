# -*- coding: utf-8 -*-
"""Fetch full XQ radar basic-operation lesson + image alt texts."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", errors="replace")

t = fetch("https://www.xq.com.tw/learn/sensor/basic/")
clean = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
clean = re.sub(r"<style[^>]*>.*?</style>", " ", clean, flags=re.S)
# keep image alts + text
alts = re.findall(r'<img[^>]*alt="([^"]+)"[^>]*>', t)
print("=== IMAGE ALTS ===")
for a in alts:
    if a.strip():
        print("  img:", a.strip()[:90])
# text blocks
text = re.sub(r"<[^>]+>", "\n", clean)
text = html.unescape(text)
lines = [l.strip() for l in text.splitlines() if l.strip()]
print("=== TEXT ===")
for l in lines:
    print(" ", l[:130])
