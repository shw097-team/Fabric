# -*- coding: utf-8 -*-
"""Fetch cua.ai docs on cua-driver background input + delivery modes."""
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

for url in (
    "https://cua.ai/docs/cua-driver",
    "https://cua.ai/docs/cua-driver/input",
):
    t = fetch(url)
    print(f"=== {url} len={len(t)} ===")
    if t.startswith("ERR"):
        print(" ", t[:80])
        continue
    clean = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", clean)
    text = html.unescape(re.sub(r"\s+", " ", text))
    # find key sections
    for kw in ("background", "delivery_mode", "foreground", "steal", "focus", "SendInput", "postmessage"):
        for m in list(re.finditer(kw, text, re.I))[:2]:
            s = max(0, m.start() - 100)
            print(f"  [{kw}] ...{text[s:m.start()+200][:280]}")
            print()
            break
    print("---")
