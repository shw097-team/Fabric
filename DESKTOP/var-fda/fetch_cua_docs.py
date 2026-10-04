# -*- coding: utf-8 -*-
"""Fetch cua-driver official docs: background vs foreground input, user mouse conflict."""
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
    "https://raw.githubusercontent.com/trycua/cua/main/libs/cua-driver/README.md",
    "https://raw.githubusercontent.com/trycua/cua/main/README.md",
):
    t = fetch(url)
    print(f"=== {url.split('/')[-1]} len={len(t)} ===")
    if t.startswith("ERR"):
        print(" ", t[:80])
        continue
    # extract background/foreground related text
    clean = re.sub(r"<[^>]+>", " ", t)
    text = html.unescape(re.sub(r"\s+", " ", clean))
    for kw in ("background", "foreground", "focus", "cursor"):
        idxs = [m.start() for m in re.finditer(kw, text, re.I)]
        print(f"  [{kw}] {len(idxs)} hits")
    # print lines around 'background'
    for m in re.finditer(r"background", text, re.I):
        s = max(0, m.start() - 120)
        print("   ...", text[s:m.start() + 180][:300])
        break
    print()
