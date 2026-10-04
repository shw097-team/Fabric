# -*- coding: utf-8 -*-
"""FAR R3b: fetch 台股進階 + 盤中量化交易 module video descriptions (decoded)."""
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

def yt_first(q):
    t = fetch("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    if t.startswith("ERR"):
        return None
    vids = re.findall(r'"videoId":"([^"]+)"', t)
    return vids[0] if vids else None

def desc(vid):
    t = fetch(f"https://www.youtube.com/watch?v={vid}")
    if t.startswith("ERR"):
        return "ERR"
    m = re.search(r'"shortDescription":"(.*?)","isCrawlable', t, re.S)
    if not m:
        return "(no desc)"
    # unescape JSON string
    try:
        import json
        d = json.loads('"' + m.group(1) + '"')
    except Exception:
        d = m.group(1)
    return d[:1800]

for q in ("XQ 台股進階 模組 功能", "XQ 盤中量化交易模組 介紹", "XQ 策略模組 福利頻道"):
    vid = yt_first(q)
    print(f"=== {q} -> {vid} ===")
    if vid:
        print(desc(vid))
    print()
