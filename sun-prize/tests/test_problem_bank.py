from pathlib import Path
import unittest

from scripts.problem_bank import parse_catalog

FIXTURE = Path(__file__).parent / "fixtures" / "catalog-mini.md"
COMMIT = "f" * 40


class ProblemBankTests(unittest.TestCase):
    def setUp(self):
        self.records, self.errors = parse_catalog(
            FIXTURE.read_text(encoding="utf-8"),
            "catalog-mini.md",
            COMMIT,
        )

    def test_parses_all_fixture_records(self):
        self.assertEqual(3, len(self.records))
        self.assertEqual([], self.errors)

    def test_preserves_status_and_lean_state(self):
        by_id = {r.jsp_id: r for r in self.records}
        self.assertEqual("Open", by_id["JSP-000001"].current_status)
        self.assertFalse(by_id["JSP-000002"].lean_proof)
        self.assertTrue(by_id["JSP-000003"].lean_proof)

    def test_extracts_proof_contributors(self):
        record = {r.jsp_id: r for r in self.records}["JSP-000002"]
        self.assertEqual(["Alice Example", "Bob Example"], record.proof_contributors)

    def test_preserves_multiline_publication_links(self):
        record = {r.jsp_id: r for r in self.records}["JSP-000002"]
        self.assertIn("https://example.com/proof", record.publication_details)
        self.assertIn("https://example.com/exposition", record.publication_details)

    def test_preserves_blank_fields(self):
        record = {r.jsp_id: r for r in self.records}["JSP-000001"]
        self.assertEqual("", record.historical_bounty)
        self.assertEqual("", record.publication_details)


if __name__ == "__main__":
    unittest.main()
