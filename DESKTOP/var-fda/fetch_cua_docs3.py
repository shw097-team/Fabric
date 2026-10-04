# -*- coding: utf-8 -*-
"""Fetch cua.ai docs: find the background delivery page + extract key text."""
import html
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERR: {e}"

t = fetch("https://cua.ai/docs/cua-driver")
# find links to background delivery docs
links = re.findall(r'href="([^"]*background[^"]*)"', t, re.I)
print("bg links:", links[:5])
links2 = re.findall(r'href="([^"]*delivery[^"]*)"', t, re.I)
print("delivery links:", links2[:5])
links3 = re.findall(r'href="([^"]*captur[^"]*)"', t, re.I)
print("capture links:", links3[:5])

# extract text around 背景 background delivery
clean = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
text = re.sub(r"<[^>]+>", " ", clean)
text = html.unescape(re.sub(r"\s+", " ", text))
for kw in ("Best-effort background", "Background Delivery", "steal", "without"):
    for m in list(re.finditer(re.escape(kw), text, re.I))[:2]:
        s = max(0, m.start() - 80)
        print(f"[{kw}] ...{text[s:m.start()+250][:320]}")
        print()
