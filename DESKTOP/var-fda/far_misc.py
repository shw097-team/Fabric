# -*- coding: utf-8 -*-
"""FAR R3c: XQ official FB posts + Mobile01 for module list."""
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

def yt(q, n=10):
    t = fetch("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    if t.startswith("ERR"):
        return []
    vids = re.findall(r'"videoId":"([^"]+)"', t)
    titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"', t)
    return list(zip(vids, titles))[:n]

# Mobile01 search via YT is no good; try FB posts search via YT tags: search "XQ 模組 購買 訂閱 教學 影片"
for q in ("XQ 如何訂閱模組 教學", "XQ 模組 兌換 序號", "XQ 模組 免費 一個月"):
    print(f"=== {q} ===")
    for v, ti in yt(q, 8):
        print(f"  {ti[:65]} | https://youtu.be/{v}")
    print()
