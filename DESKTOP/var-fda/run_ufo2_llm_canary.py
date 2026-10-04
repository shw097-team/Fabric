# -*- coding: utf-8 -*-
"""UFO2 LLM backend canary via Hermes dotenv credential (in-memory only).
Uses Hermes' own get_env_value_prefer_dotenv to read OPENCODE_GO_API_KEY —
never writes it anywhere. Sends ONE minimal chat_completion to prove the
opencode-go route works as a UFO2 LLM backend.
"""
import sys
from pathlib import Path

HERMES = Path(r"C:\Users\user\AppData\Local\hermes\hermes-agent")
sys.path.insert(0, str(HERMES))

from hermes_cli.config import get_env_value_prefer_dotenv

key = get_env_value_prefer_dotenv("OPENCODE_GO_API_KEY") or ""
print(f"key present: {len(key) > 0} | len: {len(key)}")
if not key:
    print("FAIL: no key")
    raise SystemExit(2)

# minimal OpenAI-compatible chat call against opencode-go
import json
import urllib.request

body = json.dumps({
    "model": "deepseek-v4-flash",
    "messages": [{"role": "user", "content": "Reply with exactly: UFO2_CANARY_OK"}],
    "max_tokens": 16,
}).encode("utf-8")

req = urllib.request.Request(
    "https://opencode.ai/zen/go/v1/chat/completions",
    data=body,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    },
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        content = (data.get("choices") or [{}])[0].get("message", {}).get("content", "")
        print(f"HTTP {resp.status} | model={data.get('model')} | content={content[:60]!r}")
        print("CANARY: PASS" if "UFO2_CANARY_OK" in content else "CANARY: PARTIAL")
except Exception as e:
    print(f"CANARY: FAIL — {type(e).__name__}: {str(e)[:200]}")
