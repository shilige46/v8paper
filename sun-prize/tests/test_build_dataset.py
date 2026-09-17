from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.problem_bank import parse_catalog
from scripts.build_dataset import (
    primary_candidates,
    validate_expected_ids,
    write_outputs,
)

FIXTURE = Path(__file__).parent / "fixtures" / "catalog-mini.md"
COMMIT = "f" * 40


class BuildDatasetTests(unittest.TestCase):
    def setUp(self):
        self.records, errors = parse_catalog(
            FIXTURE.read_text(encoding="utf-8"), "catalog-mini.md", COMMIT
        )
        self.assertEqual([], errors)

    def test_primary_candidates_are_solved_without_lean(self):
        self.assertEqual(
            ["JSP-000002"],
            [record.jsp_id for record in primary_candidates(self.records)],
        )

    def test_validate_expected_ids_accepts_consecutive_unique_ids(self):
        validate_expected_ids(self.records, 3)

    def test_validate_expected_ids_rejects_missing_id(self):
        with self.assertRaises(ValueError):
            validate_expected_ids([self.records[0], self.records[2]], 3)

    def test_validate_expected_ids_rejects_duplicate_id(self):
        duplicate = [self.records[0], self.records[0], self.records[2]]
        with self.assertRaises(ValueError):
            validate_expected_ids(duplicate, 3)

    def test_outputs_are_deterministic(self):
        reversed_records = list(reversed(self.records))
        with TemporaryDirectory() as left_tmp, TemporaryDirectory() as right_tmp:
            left = Path(left_tmp)
            right = Path(right_tmp)
            write_outputs(
                reversed_records,
                left / "problems.jsonl",
                left / "candidates.csv",
            )
            write_outputs(
                self.records,
                right / "problems.jsonl",
                right / "candidates.csv",
            )
            self.assertEqual(
                (left / "problems.jsonl").read_bytes(),
                (right / "problems.jsonl").read_bytes(),
            )
            self.assertEqual(
                (left / "candidates.csv").read_bytes(),
                (right / "candidates.csv").read_bytes(),
            )

    def test_validate_expected_ids_rejects_out_of_range_id(self):
        bad = list(self.records)
        bad[2] = replace(bad[2], jsp_id="JSP-000004")
        with self.assertRaises(ValueError):
            validate_expected_ids(bad, 3)


if __name__ == "__main__":
    unittest.main()
