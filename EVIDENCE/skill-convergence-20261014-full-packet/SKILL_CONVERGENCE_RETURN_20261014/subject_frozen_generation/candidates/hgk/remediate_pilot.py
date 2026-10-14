from __future__ import annotations

import datetime as _dt
import hashlib
import json
from pathlib import Path


CWD = Path.cwd()
INPUT_JSON = Path(
    "C:/Projects/Agent_Workspace/HG-KSEOS/var/SKILL-CONVERGENCE-20261014/"
    "evidence/postfreeze/hgk_unreachable.json"
)
TOPIC_REL = Path("skill/references/topics/lane-bootstrap-and-guard-notes.md")
SKILL_MD_REL = Path("skill/SKILL.md")
RESULT_REL = Path("remediation_result.json")
PYTHON = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    with INPUT_JSON.open("r", encoding="utf-8") as handle:
        entries = json.load(handle)
    if not isinstance(entries, list) or len(entries) < 14:
        raise SystemExit("input JSON must be a list with at least 14 entries")
    selected = entries[:14]

    topic_path = CWD / TOPIC_REL
    skill_md_path = CWD / SKILL_MD_REL
    result_path = CWD / RESULT_REL

    if topic_path.exists():
        raise SystemExit(f"refusing to overwrite existing topic file: {topic_path}")
    if result_path.exists():
        raise SystemExit(f"refusing to overwrite existing result file: {result_path}")
    if not skill_md_path.is_file():
        raise SystemExit(f"missing SKILL.md: {skill_md_path}")

    sha_skill_before = sha256_bytes(skill_md_path.read_bytes())

    merged: list[dict[str, object]] = []
    deleted: list[str] = []
    source_bytes_by_rel: dict[str, bytes] = {}
    source_paths: list[Path] = []
    topic_parts: list[bytes] = []

    for raw in selected:
        if not isinstance(raw, list) or len(raw) != 2:
            raise SystemExit(f"unexpected entry shape: {raw!r}")
        rel_str, input_bytes = raw
        if not isinstance(rel_str, str) or not isinstance(input_bytes, int):
            raise SystemExit(f"unexpected entry types: {raw!r}")

        source_path = CWD / "skill" / Path(rel_str)
        if not source_path.is_file():
            raise SystemExit(f"missing source file: {source_path}")
        content = source_path.read_bytes()
        if len(content) != input_bytes:
            raise SystemExit(
                f"byte-size mismatch for {rel_str}: input={input_bytes} actual={len(content)}"
            )

        source_bytes_by_rel[rel_str] = content
        source_paths.append(source_path)
        deleted.append(rel_str)
        merged.append(
            {
                "path": rel_str,
                "bytes_before": len(content),
                "sha256_before": sha256_bytes(content),
                "present_verbatim_in_topic": False,
            }
        )

        topic_parts.append(f"## {rel_str}\n".encode("utf-8"))
        topic_parts.append(content)
        if not content.endswith(b"\n"):
            topic_parts.append(b"\n")

    topic_bytes = b"".join(topic_parts)
    topic_path.parent.mkdir(parents=True, exist_ok=True)
    topic_path.write_bytes(topic_bytes)

    for source_path in source_paths:
        source_path.unlink()

    topic_bytes_after = topic_path.read_bytes()

    for record in merged:
        rel_str = str(record["path"])
        source_path = CWD / "skill" / Path(rel_str)
        if source_path.exists():
            raise SystemExit(f"source still exists after deletion: {source_path}")
        present = source_bytes_by_rel[rel_str] in topic_bytes_after
        record["present_verbatim_in_topic"] = bool(present)
        if not present:
            raise SystemExit(f"content not present verbatim in topic: {rel_str}")

    sha_skill_after = sha256_bytes(skill_md_path.read_bytes())
    if sha_skill_after != sha_skill_before:
        raise SystemExit("SKILL.md changed during lane")

    references_before = 108
    references_after = references_before - len(deleted) + 1

    result = {
        "schema": "hgk.skill-reference-sprawl-remediation.pilot-result/v1",
        "lane": "EXECUTE",
        "observed_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "merged": merged,
        "topic_file": {
            "path": TOPIC_REL.as_posix(),
            "bytes": len(topic_bytes_after),
            "sha256": sha256_bytes(topic_bytes_after),
        },
        "counts": {
            "references_md_before": references_before,
            "references_md_after": references_after,
        },
        "deleted": deleted,
        "stubs_created": [],
        "sha256_of_skill_md_before": sha_skill_before,
        "sha256_of_skill_md_after": sha_skill_after,
        "exact_commands": [
            f"Get-Content -LiteralPath {INPUT_JSON.as_posix()} -Raw",
            f"{PYTHON} remediate_pilot.py",
        ],
        "coverage": {
            "input_json": INPUT_JSON.as_posix(),
            "entries_available": len(entries),
            "entries_used": len(deleted),
            "selection": "exactly the first 14 entries, preserving input order",
            "all_before_sizes_match_input": True,
            "all_sha256_before_recorded": True,
            "all_content_found_verbatim_in_topic_after_deletion": all(
                bool(record["present_verbatim_in_topic"]) for record in merged
            ),
            "original_paths_removed": True,
        },
        "claim_ceiling": (
            "Candidate-only edit whose byte-level checks were recomputed in this lane "
            "from the bytes on disk. This is not acceptance and creates no canonical "
            "acceptance status. The merge reduces the references markdown file count by "
            "13 net (14 removed, 1 added). The result is still above the 60-file "
            "references-sprawl warning cap, so that cap is still not met."
        ),
    }

    result_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "result": str(result_path),
                "topic_file": str(topic_path),
                "merged_count": len(deleted),
                "references_md_after": references_after,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
