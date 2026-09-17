import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.make_triage import extract_links, classify_row, generate_triage


class MakeTriageTests(unittest.TestCase):
    def test_extract_links_finds_markdown_and_autolinks(self):
        text = "[Proof](https://example.com/proof) and <https://example.com/exposition>"
        self.assertEqual(
            ["https://example.com/proof", "https://example.com/exposition"],
            extract_links(text),
        )

    def test_classifies_discrete_public_proof_as_inspect_first(self):
        row = {
            "jsp_id": "JSP-000001",
            "mathematical_area": "Number theory / Combinatorics",
            "publication_details": "[Proof](https://example.com/proof)",
            "public_review": "Unverified.",
        }
        triage = classify_row(row)
        self.assertEqual("inspect-first", triage["engineering_band"])
        self.assertEqual("True", triage["has_public_proof_link"])
        self.assertEqual("1", triage["proof_link_count"])
        self.assertEqual("False", triage["advanced_analysis_flag"])
        self.assertEqual("False", triage["geometry_topology_flag"])

    def test_classifies_analysis_proof_as_inspect(self):
        row = {
            "jsp_id": "JSP-000002",
            "mathematical_area": "Analysis / Measure theory",
            "publication_details": "[Paper](https://example.com/paper)",
            "public_review": "",
        }
        triage = classify_row(row)
        self.assertEqual("inspect", triage["engineering_band"])
        self.assertEqual("True", triage["advanced_analysis_flag"])

    def test_classifies_missing_source_as_source_needed(self):
        row = {
            "jsp_id": "JSP-000003",
            "mathematical_area": "Graph theory",
            "publication_details": "",
            "public_review": "",
        }
        triage = classify_row(row)
        self.assertEqual("source-needed", triage["engineering_band"])
        self.assertEqual("0", triage["proof_link_count"])

    def test_generate_triage_writes_card_with_explicit_unreviewed_state(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "candidates.csv"
            output = root / "triage.csv"
            research = root / "research"
            with source.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "jsp_id",
                        "title",
                        "mathematical_area",
                        "current_status",
                        "lean_proof",
                        "eligible_to_claim",
                        "publication_details",
                        "public_review",
                        "source_file",
                        "source_commit",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "jsp_id": "JSP-000002",
                        "title": "Solved without Lean",
                        "mathematical_area": "Combinatorics",
                        "current_status": "Solved",
                        "lean_proof": "False",
                        "eligible_to_claim": "No",
                        "publication_details": "[Proof](https://example.com/proof)",
                        "public_review": "Unverified.",
                        "source_file": "catalog.md",
                        "source_commit": "f" * 40,
                    }
                )
            rows = generate_triage(source, output, research)
            self.assertEqual(1, len(rows))
            card = (research / "JSP-000002.md").read_text(encoding="utf-8")
            self.assertIn("Not reviewed yet.", card)
            self.assertIn("no award entitlement inferred", card)


if __name__ == "__main__":
    unittest.main()
