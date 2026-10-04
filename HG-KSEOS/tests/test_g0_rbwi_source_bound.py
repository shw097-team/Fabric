"""WAVE4 — rbwi_composite source-bound not-required semantics (G0 D4 extension).

A child adjudicated SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY (or
SOURCE_VALID_NOT_APPLICABLE) is a terminal state — the composite must not
FAIL_CLOSED on it.
"""
from __future__ import annotations

import unittest

from hg_kseos.lifecycle import rbwi_composite


class RbwiSourceBoundTests(unittest.TestCase):
    def test_source_valid_not_required_is_terminal(self):
        c = rbwi_composite({
            "local_paper": "PASS",
            "external_market": "SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY",
            "tool_coverage": "PASS",
            "user_journey": "PASS",
            "negative_degraded": "PASS",
            "replay": "PASS",
        })
        self.assertEqual(c["verdict"], "PASS")
        self.assertEqual(c["open_edges"], [])

    def test_source_valid_not_applicable_is_terminal(self):
        c = rbwi_composite({
            "local_paper": "PASS",
            "external_market": "SOURCE_VALID_NOT_APPLICABLE",
            "tool_coverage": "PASS",
            "user_journey": "PASS",
            "negative_degraded": "PASS",
            "replay": "PASS",
        })
        self.assertEqual(c["verdict"], "PASS")

    def test_temp_closed_still_blocks(self):
        c = rbwi_composite({
            "local_paper": "PASS",
            "external_market": "TEMP_CLOSED",
            "tool_coverage": "PASS",
            "user_journey": "PASS",
            "negative_degraded": "PASS",
            "replay": "PASS",
        })
        self.assertEqual(c["verdict"], "TEMP_CLOSED")


if __name__ == "__main__":
    unittest.main()
