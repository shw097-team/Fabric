import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_review_bundle.py"
spec = importlib.util.spec_from_file_location("vrb", SCRIPT)
vrb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vrb)


class VerifyReviewBundleTests(unittest.TestCase):
    def test_packaged_intake_template_valid(self):
        p = Path(__file__).resolve().parents[1] / "assets" / "EXTERNAL_CHALLENGE_INTAKE.template.json"
        self.assertEqual(vrb.validate_intake(p), [])

    def test_missing_intake_key_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"
            p.write_text(json.dumps({"review_id": "x"}), encoding="utf-8")
            self.assertTrue(vrb.validate_intake(p))

    def test_report_requires_headings_and_verdict(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.md"
            p.write_text("# report\n", encoding="utf-8")
            errors = vrb.validate_report(p)
            self.assertTrue(any(e.startswith("missing_heading") for e in errors))
            self.assertIn("missing_allowed_verdict", errors)

    def test_complete_report_structure_passes(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "good.md"
            body = "# EXTERNAL_CHALLENGE_REPORT\n\n" + "\n\n".join(vrb.REQUIRED_REPORT_HEADINGS) + "\n\nPASS_CHALLENGE\n"
            p.write_text(body, encoding="utf-8")
            self.assertEqual(vrb.validate_report(p), [])


if __name__ == "__main__":
    unittest.main()
