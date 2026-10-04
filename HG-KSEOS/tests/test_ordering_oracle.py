"""test_ordering_oracle.py — C7 regression guard for the FAR-derived ordering-oracle control.

The named defect class is ORDERING_ORACLE_WALL_CLOCK_ONLY: an ordering decision taken on wall-clock
`created_at` (second granularity) instead of a monotonic insertion order. Two rows sharing a timestamp
make such a choice arbitrary. The fix uses SQLite's implicit `rowid`, matching the existing convention
in evidence_graph.py.

Two halves, per the validator-authoring discipline:
  * a SOURCE guard  - no wall-clock ordering site may reappear in the control plane
  * a BEHAVIOURAL assertion - with colliding created_at values the rowid order is deterministic and the
    wall-clock order is genuinely ambiguous (i.e. the guard is not vacuous)
"""
import re, sqlite3, unittest
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src" / "hg_kseos"
# matches BOTH the unqualified form and the table-alias form (ORDER BY v.created_at).
# The earlier literal pattern was alias-blind and missed a real site at evidence_graph.py:224.
WALL_CLOCK_RE = re.compile(r"ORDER\s+BY\s+(?:\w+\.)?created_at", re.IGNORECASE)


class TestNoWallClockOrderingSites(unittest.TestCase):
    """SOURCE guard: an ordering decision must not be taken on wall-clock created_at."""

    def test_no_order_by_created_at_in_control_plane(self):
        offenders = []
        for f in sorted(SRC.glob("*.py")):
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if WALL_CLOCK_RE.search(line):
                    offenders.append(f"{f.name}:{i}: {line.strip()[:90]}")
        self.assertEqual(offenders, [], "wall-clock ordering site(s) reintroduced:\n" + "\n".join(offenders))

    def test_guard_is_not_alias_blind(self):
        """Regression: the guard must flag a QUALIFIED wall-clock ordering site (ORDER BY v.created_at),
        which a literal 'ORDER BY created_at' pattern silently misses."""
        self.assertTrue(WALL_CLOCK_RE.search("WHERE x=? ORDER BY v.created_at"),
                        "guard is alias-blind - it would miss a real defect site")

    def test_rowid_convention_is_present(self):
        """The guard is only meaningful if the codebase actually uses rowid for ordering."""
        hits = [f.name for f in SRC.glob("*.py")
                if "ORDER BY rowid" in f.read_text(encoding="utf-8")]
        self.assertTrue(hits, "no ORDER BY rowid site found - the ordering convention is gone")


class TestRowidOrderIsDeterministicAndWallClockIsNot(unittest.TestCase):
    """BEHAVIOURAL: proves the control is non-vacuous - rowid is total, created_at is not."""

    def _conn(self):
        c = sqlite3.connect(":memory:")
        c.execute("CREATE TABLE workorders(workorder_id TEXT, created_at TEXT, state TEXT)")
        # two admissions in the SAME second - the real-world collision case
        c.execute("INSERT INTO workorders VALUES('WO-A','2026-10-04T20:00:00','ADMITTED')")
        c.execute("INSERT INTO workorders VALUES('WO-B','2026-10-04T20:00:00','ADMITTED')")
        return c

    def test_rowid_order_is_total(self):
        c = self._conn()
        r1 = c.execute("SELECT workorder_id FROM workorders WHERE state='ADMITTED' ORDER BY rowid LIMIT 1").fetchone()
        r2 = c.execute("SELECT workorder_id FROM workorders WHERE state='ADMITTED' ORDER BY rowid LIMIT 1").fetchone()
        self.assertEqual(r1, ("WO-A",), "first-inserted admission must win")
        self.assertEqual(r1, r2, "rowid ordering must be deterministic across repeated reads")

    def test_ordering_keys_diverge_on_distinct_timestamps(self):
        """NON-TAUTOLOGICAL divergence proof (previous collision fixture was tautological - it only
        asserted its own timestamps were equal). Here INSERTION order deliberately OPPOSES wall-clock
        order, so the two keys select DIFFERENT admissions: this is what makes the change behaviourally
        real rather than a no-op."""
        c = sqlite3.connect(":memory:")
        c.execute("CREATE TABLE workorders(workorder_id TEXT, created_at TEXT, state TEXT)")
        c.execute("INSERT INTO workorders VALUES('WO-X','2026-10-04T20:00:05','ADMITTED')")  # inserted first
        c.execute("INSERT INTO workorders VALUES('WO-Y','2026-10-04T20:00:01','ADMITTED')")  # earlier clock, later insert
        by_rowid = c.execute("SELECT workorder_id FROM workorders WHERE state='ADMITTED' "
                             "ORDER BY rowid LIMIT 1").fetchone()[0]
        by_clock = c.execute("SELECT workorder_id FROM workorders WHERE state='ADMITTED' "
                             "ORDER BY created_at LIMIT 1").fetchone()[0]
        self.assertEqual(by_rowid, "WO-X", "admission order must be insertion order")
        self.assertEqual(by_clock, "WO-Y", "wall-clock order must be the earlier timestamp")
        self.assertNotEqual(by_rowid, by_clock, "the two oracles MUST disagree here - proves non-inertness")


if __name__ == "__main__":
    unittest.main(verbosity=2)
