#!/usr/bin/env python3
"""Validate current skills-only plugin trees and ZIP archives without extracting."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath


class DuplicateJsonKey(ValueError):
    pass


def strict_json_loads(text: str) -> object:
    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise DuplicateJsonKey(key)
            result[key] = value
        return result

    return json.loads(text, object_pairs_hook=unique_object)


def canonical_name(name: str) -> str | None:
    if "\\" in name or name.startswith("/") or re.match(r"^[A-Za-z]:", name):
        return None
    if name.endswith("//"):
        return None
    raw = name[:-1] if name.endswith("/") else name
    normalized = posixpath.normpath(raw)
    if not raw or normalized != raw:
        return None
    parts = PurePosixPath(normalized).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        return None
    return normalized


def safe_name(name: str) -> bool:
    return canonical_name(name) is not None


def source_map(root: Path, prefix: str = "") -> dict[str, str]:
    rows: dict[str, str] = {}
    for item in sorted(root.rglob("*")):
        if item.is_symlink():
            raise ValueError("source tree contains symlink")
        if item.is_file():
            rel = item.relative_to(root).as_posix()
            name = (PurePosixPath(prefix) / rel).as_posix() if prefix else rel
            digest = hashlib.sha256(item.read_bytes()).hexdigest()
            rows[name] = digest
    return rows


def validate_plugin_inside_archive(archive: zipfile.ZipFile, file_names: set[str]) -> list[str]:
    errors: list[str] = []
    manifests = [name for name in file_names if name.endswith(".codex-plugin/plugin.json")]
    if not manifests:
        return errors
    if len(manifests) != 1:
        return ["archive: expected exactly one plugin manifest"]
    manifest_name = manifests[0]
    plugin_root = manifest_name[: -len(".codex-plugin/plugin.json")]
    try:
        manifest = strict_json_loads(archive.read(manifest_name).decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError, DuplicateJsonKey):
        return ["archive: plugin manifest is invalid or duplicate-key JSON"]
    if not isinstance(manifest, dict):
        return ["archive: plugin manifest must be object"]
    for field in ("name", "version", "description", "skills"):
        if not isinstance(manifest.get(field), str) or not manifest[field]:
            errors.append(f"archive: plugin manifest {field} required")
    if manifest.get("skills") != "./skills/":
        errors.append("archive: plugin manifest skills must equal ./skills/")
    skills_root = plugin_root + "skills/"
    skill_files = [
        name
        for name in file_names
        if name.startswith(skills_root)
        and len(PurePosixPath(name[len(skills_root) :]).parts) == 2
        and PurePosixPath(name).name == "SKILL.md"
    ]
    if len(skill_files) != 1:
        errors.append(f"archive: plugin skills binding resolves to {len(skill_files)} active Skills")
    return errors


def validate_archive(path: Path, expected_root: Path | None = None, prefix: str = "") -> list[str]:
    errors: list[str] = []
    if prefix and (prefix.startswith("/") or "\\" in prefix or canonical_name(prefix) != prefix):
        errors.append("archive: expected prefix must be canonical")
    with zipfile.ZipFile(path) as archive:
        items = archive.infolist()
        file_items = [item for item in items if not item.is_dir()]
        names = [item.filename for item in items]
        if not file_items:
            errors.append("archive: no files")
        for name in names:
            if not safe_name(name):
                errors.append(f"archive: unsafe path {name}")
        for item in items:
            mode = (item.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                errors.append(f"archive: symlink entry {item.filename}")
            elif mode:
                file_type = stat.S_IFMT(mode)
                if item.is_dir() and file_type not in {0, stat.S_IFDIR}:
                    errors.append(f"archive: non-directory mode for directory entry {item.filename}")
                elif not item.is_dir() and file_type not in {0, stat.S_IFREG}:
                    errors.append(f"archive: special-file entry {item.filename}")
        canonical = [canonical_name(name) for name in names]
        valid_canonical = [name for name in canonical if name is not None]
        if len(valid_canonical) != len(set(valid_canonical)):
            errors.append("archive: duplicate path")
        lowered = [name.casefold() for name in valid_canonical]
        if len(lowered) != len(set(lowered)):
            errors.append("archive: case-colliding path")
        if any("__pycache__" in PurePosixPath(name).parts or name.endswith((".pyc", ".tmp", "~")) for name in names):
            errors.append("archive: stale/cache/temp file")
        actual: dict[str, str] = {}
        for item in file_items:
            canonical = canonical_name(item.filename)
            if canonical is None:
                continue
            if canonical in actual:
                continue
            actual[canonical] = hashlib.sha256(archive.read(item)).hexdigest()
        errors.extend(validate_plugin_inside_archive(archive, set(actual)))
        if expected_root is None:
            errors.append("archive: expected source root required for qualification")
        else:
            try:
                expected = source_map(expected_root, prefix)
            except (OSError, ValueError) as exc:
                errors.append(f"archive: invalid expected source ({exc})")
            else:
                if set(actual) != set(expected):
                    errors.append("archive: source/archive path set mismatch")
                for name in sorted(set(actual) & set(expected)):
                    if actual[name] != expected[name]:
                        errors.append(f"archive: source/archive content mismatch {name}")
        bad = archive.testzip()
        if bad:
            errors.append(f"archive: CRC failure {bad}")
    return errors


def read_name_from_skill(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return None
    raw = text[4:].split("\n---\n", 1)[0]
    for line in raw.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


def validate_tree(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        return ["plugin manifest missing"]
    try:
        manifest = strict_json_loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJsonKey):
        return ["plugin manifest invalid or duplicate-key JSON"]
    if not isinstance(manifest, dict):
        return ["plugin manifest must be object"]
    for field in ("name", "version", "description", "skills"):
        if not isinstance(manifest.get(field), str) or not manifest[field]:
            errors.append(f"manifest.{field}: required string")
    if manifest.get("skills") != "./skills/":
        errors.append("manifest.skills: must equal ./skills/")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest.get("name", "")):
        errors.append("manifest.name: must be kebab-case")
    skills_root = root / "skills"
    skill_files = sorted(skills_root.glob("*/SKILL.md")) if skills_root.is_dir() else []
    if len(skill_files) != 1:
        errors.append(f"skills: expected exactly one active Skill, found {len(skill_files)}")
    for skill_file in skill_files:
        skill_name = read_name_from_skill(skill_file)
        if not skill_name:
            errors.append(f"{skill_file}: missing frontmatter name")
        elif len(manifest["name"] + ":" + skill_name) > 64:
            errors.append("plugin:skill identity exceeds 64 characters")
        agent = skill_file.parent / "agents" / "openai.yaml"
        if not agent.is_file():
            errors.append("agents/openai.yaml: missing")
    all_files = [p for p in root.rglob("*") if p.is_file()]
    if any(path.is_symlink() for path in root.rglob("*")):
        errors.append("tree: symlink is not allowed")
    rels = [p.relative_to(root).as_posix() for p in all_files]
    if len(rels) != len(set(rels)) or len(rels) != len({r.casefold() for r in rels}):
        errors.append("tree: duplicate or case-colliding path")
    if any("__pycache__" in p.parts or p.suffix == ".pyc" or p.name.endswith((".tmp", "~")) for p in all_files):
        errors.append("tree: stale/cache/temp file")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-root", type=Path)
    parser.add_argument("--zip", dest="zip_path", type=Path)
    parser.add_argument("--expected-root", type=Path)
    parser.add_argument("--prefix", default="")
    args = parser.parse_args()
    errors: list[str] = []
    if args.plugin_root:
        errors.extend(validate_tree(args.plugin_root))
    if args.zip_path:
        errors.extend(validate_archive(args.zip_path, args.expected_root, args.prefix))
    if not args.plugin_root and not args.zip_path:
        parser.error("provide --plugin-root and/or --zip")
    print(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
