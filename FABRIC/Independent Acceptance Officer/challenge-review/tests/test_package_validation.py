import importlib.util
import json
import shutil
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = SKILL_ROOT.parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "validate_package.py"
SPEC = importlib.util.spec_from_file_location("validate_package", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class PackageValidationTests(unittest.TestCase):
    def require_plugin_wrapper(self):
        if not (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").is_file():
            self.skipTest("Plugin-wrapper-only validation in a direct Skill install")

    def test_plugin_tree_passes(self):
        self.require_plugin_wrapper()
        with tempfile.TemporaryDirectory(dir=PLUGIN_ROOT.parent) as directory:
            copy = Path(directory) / "plugin"
            shutil.copytree(
                PLUGIN_ROOT,
                copy,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            self.assertEqual(MODULE.validate_tree(copy), [])

    def test_manifest_binds_current_skills_root(self):
        self.require_plugin_wrapper()
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["version"], "2.0.0")

    def test_combined_identity_is_within_limit(self):
        self.require_plugin_wrapper()
        manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertLessEqual(len(manifest["name"] + ":challenge-review"), 64)

    def test_safe_archive_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "safe.zip"
            source = Path(directory) / "source"
            (source / "skills" / "x").mkdir(parents=True)
            (source / "skills" / "x" / "SKILL.md").write_text("ok")
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("skills/x/SKILL.md", "ok")
            self.assertEqual(MODULE.validate_archive(path, source), [])

    def test_traversal_archive_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("../escape", "bad")
            self.assertTrue(MODULE.validate_archive(path))

    def test_case_collision_archive_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("A.txt", "one")
                archive.writestr("a.txt", "two")
            self.assertTrue(MODULE.validate_archive(path))

    def test_normalized_duplicate_archive_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("a/b.txt", "one")
                archive.writestr("a//b.txt", "two")
            self.assertTrue(MODULE.validate_archive(path))

    def test_symlink_archive_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                info = zipfile.ZipInfo("link")
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, "../../escape")
            self.assertTrue(MODULE.validate_archive(path))

    def test_dot_segment_archive_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("a/./b.txt", "bad")
            self.assertTrue(MODULE.validate_archive(path))

    def test_traversal_directory_entry_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("safe.txt", "ok")
                archive.writestr("../escape/", "")
            self.assertTrue(MODULE.validate_archive(path))

    def test_symlink_directory_entry_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("safe.txt", "ok")
                info = zipfile.ZipInfo("link/")
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, "")
            self.assertTrue(MODULE.validate_archive(path))

    def test_case_colliding_directory_entries_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("safe.txt", "ok")
                archive.writestr("A/", "")
                archive.writestr("a/", "")
            self.assertTrue(MODULE.validate_archive(path))

    def test_safe_directory_entry_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "safe.zip"
            source = Path(directory) / "source"
            (source / "skills" / "x").mkdir(parents=True)
            (source / "skills" / "x" / "SKILL.md").write_text("ok")
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("skills/", "")
                archive.writestr("skills/x/SKILL.md", "ok")
            self.assertEqual(MODULE.validate_archive(path, source), [])

    def test_repeated_trailing_separator_directory_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            source = Path(directory) / "source"
            source.mkdir()
            (source / "safe.txt").write_text("ok")
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("safe.txt", "ok")
                archive.writestr("a//", "")
            self.assertTrue(MODULE.validate_archive(path, source))

    def test_special_type_rejected_even_with_create_system_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            source = Path(directory) / "source"
            source.mkdir()
            (source / "safe.txt").write_text("ok")
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("safe.txt", "ok")
                info = zipfile.ZipInfo("device")
                info.create_system = 0
                info.external_attr = (stat.S_IFCHR | 0o600) << 16
                archive.writestr(info, "")
            self.assertTrue(MODULE.validate_archive(path, source))

    def test_plugin_archive_missing_bound_skills_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            source = Path(directory) / "source"
            (source / ".codex-plugin").mkdir(parents=True)
            manifest = '{"name":"x","version":"1.0.0","description":"x","skills":"./missing/"}'
            (source / ".codex-plugin" / "plugin.json").write_text(manifest)
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(".codex-plugin/plugin.json", manifest)
            self.assertTrue(MODULE.validate_archive(path, source))

    def test_duplicate_plugin_manifest_key_rejected_in_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            source = Path(directory) / "source"
            (source / ".codex-plugin").mkdir(parents=True)
            (source / "skills" / "x").mkdir(parents=True)
            manifest = (
                '{"name":"x","version":"1.0.0","description":"x",'
                '"skills":"./missing/","skills":"./skills/"}'
            )
            (source / ".codex-plugin" / "plugin.json").write_text(manifest)
            (source / "skills" / "x" / "SKILL.md").write_text("---\nname: x\ndescription: x\n---\nbody\n")
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr(".codex-plugin/plugin.json", manifest)
                archive.writestr("skills/x/SKILL.md", (source / "skills" / "x" / "SKILL.md").read_text())
            self.assertTrue(MODULE.validate_archive(path, source))

    def test_duplicate_plugin_manifest_key_rejected_in_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".codex-plugin").mkdir(parents=True)
            (root / "skills" / "x" / "agents").mkdir(parents=True)
            (root / ".codex-plugin" / "plugin.json").write_text(
                '{"name":"x","version":"1.0.0","description":"x",'
                '"skills":"./missing/","skills":"./skills/"}'
            )
            (root / "skills" / "x" / "SKILL.md").write_text("---\nname: x\ndescription: x\n---\nbody\n")
            (root / "skills" / "x" / "agents" / "openai.yaml").write_text("interface: {}\n")
            self.assertTrue(MODULE.validate_tree(root))

    def test_archive_content_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.zip"
            source = Path(directory) / "source"
            source.mkdir()
            (source / "file.txt").write_text("expected")
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("file.txt", "different")
            self.assertTrue(MODULE.validate_archive(path, source))

    def test_archive_without_source_binding_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "safe-looking.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("file.txt", "content")
            self.assertTrue(MODULE.validate_archive(path))


if __name__ == "__main__":
    unittest.main()
