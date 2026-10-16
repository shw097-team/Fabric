"""Pre-LLM-call hook: mint a short-lived FDA session token when the user
explicitly authorizes FDA usage. This hook never blocks; it always exits 0.
"""

import datetime
import json
import os
import re
import sys
from pathlib import Path

AUTH_DIR = Path(r"C:\Users\user\AppData\Local\hermes\var\fda-auth")

# Intent verbs (unicode-escaped, verbatim per spec).
INTENT_VERBS = [
    "\u7528",
    "\u4f7f\u7528",
    "\u64cd\u4f5c",
    "\u64cd\u63a7",
    "\u57f7\u884c",
    "\u958b\u555f",
    "\u555f\u7528",
    "\u5141\u8a31",
    "\u6388\u6b0a",
    "\u53ef\u4ee5",
    "\u6279\u51c6",
    "approve",
    "use",
    "run",
    "operate",
    "authorize",
    "allow",
]

# FDA target tokens (unicode-escaped, verbatim per spec).
FDA_TARGETS = [
    "FDA",
    "fda_run",
    "fda_preflight",
    "screen_state_check",
    "XQ\u5168\u7403\u8d0f\u5bb6",
    "\u7b56\u7565\u96f7\u9054",
    "\u96f7\u9054",
    "XQLite",
    "PAPER",
]

INTENT_RE = re.compile("|".join(INTENT_VERBS), re.IGNORECASE)
TARGET_RE = re.compile("|".join(FDA_TARGETS), re.IGNORECASE)

TTL_SECONDS = 3600
MAX_MATCHED_TEXT = 200


def _iso_z(dt):
    """Format an aware datetime as ISO-8601 with a trailing Z."""
    return dt.isoformat().replace("+00:00", "Z")


def _collect_user_texts(data):
    """Return user_message plus the last four user history entries."""
    texts = []
    user_message = data.get("user_message")
    if isinstance(user_message, str) and user_message.strip():
        texts.append(user_message)

    history = data.get("conversation_history")
    if isinstance(history, list):
        user_entries = []
        for entry in history:
            if not isinstance(entry, dict) or entry.get("role") != "user":
                continue
            content = entry.get("content")
            if isinstance(content, str) and content.strip():
                user_entries.append(content)
            elif isinstance(content, list):
                parts = []
                for part in content:
                    if isinstance(part, dict) and isinstance(part.get("text"), str):
                        parts.append(part["text"])
                if parts:
                    user_entries.append("\n".join(parts))
        texts.extend(user_entries[-4:])
    return texts


def _mint_token(session_id, turn_id, matched_text):
    """Write (or refresh) the per-session FDA token file."""
    os.makedirs(AUTH_DIR, exist_ok=True)
    token_path = AUTH_DIR / ("%s.json" % session_id)
    now = datetime.datetime.now(datetime.timezone.utc)
    token = {
        "session_id": session_id,
        "turn_id": turn_id,
        "minted_at_utc": _iso_z(now),
        "ttl_seconds": TTL_SECONDS,
        "expires_at_utc": _iso_z(now + datetime.timedelta(seconds=TTL_SECONDS)),
        "matched_text": matched_text[:MAX_MATCHED_TEXT],
        "source": "pre_llm_call_mint",
    }
    if token_path.exists():
        try:
            existing = json.loads(token_path.read_text(encoding="utf-8"))
            existing_turn = existing.get("turn_id")
            if existing_turn is not None and str(existing_turn) >= str(turn_id):
                live = False
                try:
                    _e = datetime.datetime.fromisoformat(
                        str(existing.get("expires_at_utc", "")).replace("Z", "+00:00"))
                    live = _e > datetime.datetime.now(datetime.timezone.utc)
                except Exception:
                    live = False
                if live:
                    return
        except Exception:
            pass
    token_path.write_text(
        json.dumps(token, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        data = json.loads(raw)
        if not isinstance(data, dict):
            return 0
        # real wire format: user_message/conversation_history arrive inside extra
        extra = data.get("extra")
        if isinstance(extra, dict):
            for k, v in extra.items():
                data.setdefault(k, v)

        session_id = data.get("session_id")
        turn_id = data.get("turn_id")
        if not session_id:
            return 0

        combined = "\n".join(t for t in _collect_user_texts(data) if t)
        if not combined:
            return 0
        if INTENT_RE.search(combined) is None:
            return 0
        if TARGET_RE.search(combined) is None:
            return 0

        _mint_token(session_id, turn_id, combined)
    except Exception:
        pass
    return 0


try:
    sys.stdin.reconfigure(encoding="utf-8")
except Exception:
    pass


if __name__ == "__main__":
    sys.exit(main())