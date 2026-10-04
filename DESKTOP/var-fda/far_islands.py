# -*- coding: utf-8 -*-
"""FAR R1j: extract astro island payloads from /module page (contains module list data)."""
import json
import re
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
t = urllib.request.urlopen(urllib.request.Request("https://www.xq.com.tw/module", headers={"User-Agent": UA}), timeout=25).read().decode("utf-8", errors="replace")

# astro islands embed JSON props: <script type="application/json">...</script> or astro-island props=
print("astro-island count:", t.count("astro-island"))
# find inline JSON props
for m in re.finditer(r'<astro-island[^>]*props="([^"]+)"', t):
    import base64
    try:
        raw = base64.b64decode(m.group(1)).decode("utf-8", errors="replace")
        print("=== island props ===")
        print(raw[:3000])
    except Exception as e:
        print("b64 err:", str(e)[:50])
# also look for any JSON arrays of Chinese strings
for m in re.finditer(r'\[([\u4e00-\u9fff]{2,12}(?:模組|進階|即時|EOD|選股|量化)[^\]]{0,200})\]', t):
    print("ARRAY:", m.group(0)[:200])
