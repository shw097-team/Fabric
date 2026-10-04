# -*- coding: utf-8 -*-
"""FAR R3d: fetch 台股進階訂閱教學 video desc — module list + pricing."""
import json
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
vid = "8ia4XAe180M"
t = urllib.request.urlopen(urllib.request.Request(f"https://www.youtube.com/watch?v={vid}", headers={"User-Agent": UA}), timeout=25).read().decode("utf-8", errors="replace")
m = re.search(r'"shortDescription":"(.*?)","isCrawlable', t, re.S)
if m:
    try:
        d = json.loads('"' + m.group(1) + '"')
    except Exception:
        d = m.group(1)
    print("=== 台股進階訂閱教學 desc ===")
    print(d[:3000])
else:
    print("no desc")
