# -*- coding: utf-8 -*-
"""FAR R2c: XQ official channel video list — extract ALL module names from titles."""
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

# XQ channel videos tab (handle @XQ--xq from official site footer)
for url in ("https://www.youtube.com/@XQ--xq/videos",):
    t = fetch(url)
    if t.startswith("ERR"):
        print("channel:", t[:60])
        continue
    titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', t)
    # also full-text search for 模組 titles
    mod_titles = [ti for ti in titles if "模組" in ti]
    print(f"=== channel videos with 模組 ({len(mod_titles)}) ===")
    for ti in sorted(set(mod_titles))[:40]:
        print("  ", ti[:70])
