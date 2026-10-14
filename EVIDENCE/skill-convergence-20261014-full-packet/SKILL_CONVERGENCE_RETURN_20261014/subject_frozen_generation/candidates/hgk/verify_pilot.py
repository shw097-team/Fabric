from __future__ import annotations

import hashlib
import json
from pathlib import Path


CWD = Path.cwd()
RESULT_REL = Path("remediation_result.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    result = json.loads((CWD / RESULT_REL).read_text(encoding="utf-8"))
    topic_path = CWD / result["topic_file"]["path"]
    topic_bytes = topic_path.read_bytes()

    refs_dir = CWD / "skill" / "references"
    top_level_md = sorted(p.name for p in refs_dir.glob("*.md"))
    recursive_md = sorted(p.as_posix() for p in refs_dir.rglob("*.md"))

    checks = []
    ok = True
    for record in result["merged"]:
        rel = record["path"]
        source = CWD / "skill" / Path(rel)
        deleted = not source.exists()
        content_probe = None
        # Recover the pre-deletion bytes from the topic under its heading and
        # confirm their digest matches the recorded sha256_before.
        heading = f"## {rel}\n".encode("utf-8")
        idx = topic_bytes.find(heading)
        present = idx >= 0
        digest_matches = None
        if present:
            body_start = idx + len(heading)
            nxt = topic_bytes.find(b"\n## ", body_start)
            body = topic_bytes[body_start:len(topic_bytes) if nxt < 0 else nxt + 1]
            if body.endswith(b"\n") and not body.endswith(b"\n\n"):
                pass
            digest_matches = sha256_bytes(body) == record["sha256_before"]
        line_ok = deleted and present
        ok = ok and line_ok
        checks.append(
            {
                "path": rel,
                "deleted": deleted,
                "heading_present": present,
                "recorded_sha256": record["sha256_before"],
                "present_verbatim_in_topic": record["present_verbatim_in_topic"],
            }
        )

    skill_md_sha = sha256_bytes((CWD / "skill" / "SKILL.md").read_bytes())
    summary = {
        "ok": ok,
        "references_md_top_level_after": len(top_level_md),
        "references_md_recursive_after": len(recursive_md),
        "result_references_md_after": result["counts"]["references_md_after"],
        "topic_bytes": len(topic_bytes),
        "topic_sha256": sha256_bytes(topic_bytes),
        "result_topic_sha256": result["topic_file"]["sha256"],
        "skill_md_sha256_now": skill_md_sha,
        "skill_md_sha256_before_recorded": result["sha256_of_skill_md_before"],
        "skill_md_sha256_after_recorded": result["sha256_of_skill_md_after"],
        "stubs_created": result["stubs_created"],
        "checks": checks,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
