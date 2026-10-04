# -*- coding: utf-8 -*-
"""Fetch cua.ai background delivery doc — the key page for user-mouse conflict."""
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

t = fetch("https://cua.ai/docs/concepts/browser-targeting-and-background-delivery")
clean = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
text = re.sub(r"<[^>]+>", " ", clean)
text = html.unescape(re.sub(r"\s+", " ", text))
print(text[:4000])
