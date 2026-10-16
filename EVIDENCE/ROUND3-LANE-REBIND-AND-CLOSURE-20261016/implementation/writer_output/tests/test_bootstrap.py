from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.bootstrap import configured_workspace_bindings
from hg_kseos.spine import SharedSpine


class BootstrapWorkspaceBindingTests(unittest.TestCase):
    def test_canonical_layout_uses_one_path_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bindings = configured_workspace_bindings(root, root)
            self.assertEqual(len(bindings), 1)
            self.assertEqual(bindings[0][0], "WS-CANONICAL")
            self.assertEqual(bindings[0][2], root.resolve())
            self.assertEqual(bindings[0][3], "WRITABLE_CANONICAL_WITH_FROZEN_INPUT_SUBTREES")

    def test_companion_layout_preserves_source_and_maker_roles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            maker = root / "maker"
            source.mkdir()
            maker.mkdir()
            bindings = configured_workspace_bindings(maker, source)
            self.assertEqual([binding[0] for binding in bindings], ["WS-SOURCE", "WS-MAKER"])
            self.assertEqual([binding[3] for binding in bindings], ["READ_ONLY_SOURCE", "WRITABLE_MAKER"])

    def test_canonical_mode_is_admitted_by_shared_spine_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spine = SharedSpine(root / "spine.db")
            spine.initialize()
            spine.create_project()
            binding = configured_workspace_bindings(root, root)[0]
            spine.bind_workspace(*binding)
            with spine.connect() as connection:
                row = connection.execute(
                    "SELECT workspace_id,path,mode FROM workspaces WHERE workspace_id='WS-CANONICAL'"
                ).fetchone()
            self.assertEqual(row["path"], str(root.resolve()))
            self.assertEqual(row["mode"], "WRITABLE_CANONICAL_WITH_FROZEN_INPUT_SUBTREES")


if __name__ == "__main__":
    unittest.main()
