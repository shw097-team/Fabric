# -*- coding: utf-8 -*-
"""FAR R1k: decode ALL astro-island props correctly (urllib.unquote + utf-8)."""
import base64
import json
import re
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/125.0"
t = urllib.request.urlopen(urllib.request.Request("https://www.xq.com.tw/module", headers={"User-Agent": UA}), timeout=25).read().decode("utf-8", errors="replace")

found = []
for m in re.finditer(r'<astro-island[^>]*props="([^"]+)"', t):
    raw = m.group(1)
    try:
        # astro props are URL-encoded base64; try quote-unquote first
        decoded = urllib.parse.unquote(raw)
        # then base64
        padded = decoded + "=" * (-len(decoded) % 4)
        data = base64.b64decode(padded).decode("utf-8", errors="replace")
        found.append(data)
    except Exception as e:
        try:
            data = base64.b64decode(raw).decode("utf-8", errors="replace")
            found.append(data)
        except Exception:
            pass

print(f"decoded {len(found)} islands")
for i, d in enumerate(found):
    print(f"=== island {i} (len {len(d)}) ===")
    print(d[:2500])
