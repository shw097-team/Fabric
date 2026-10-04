# -*- coding: utf-8 -*-
"""Verify opencode-go endpoint via Hermes' own chat_completions transport.
If this works, the same base_url+key can back UFO2.
"""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\user\AppData\Local\hermes\hermes-agent")

from hermes_cli.config import get_env_value_prefer_dotenv
import json
import urllib.request

key = get_env_value_prefer_dotenv("OPENCODE_GO_API_KEY") or ""

# replicate Hermes chat_completions minimal request (see transport code)
payload = {
    "model": "deepseek-v4-flash",
    "messages": [{"role": "user", "content": "Say exactly: OK"}],
    "max_tokens": 8,
    "stream": False,
}
for url in (
    "https://opencode.ai/zen/go/v1/chat/completions",
    "https://opencode.ai/zen/go/chat/completions",
):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode())
            print(f"{url} -> HTTP {resp.status} OK: {str(data)[:120]}")
            break
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:200]
        print(f"{url} -> HTTP {e.code}: {body}")
