# -*- coding: utf-8 -*-
"""FAR R2d: targeted YT searches for the FULL module list."""
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

for q in ("XQ 模組 有哪幾種", "XQ 全球贏家 全部模組", "XQ 模組 比較 台股進階 盤中量化", "XQ 盤中量化交易模組", "XQ 個人版 模組 訂閱 教學"):
    print(f"=== {q} ===")
    for v, ti in yt(q):
        print(f"  {ti[:65]} | https://youtu.be/{v}")
    print()
