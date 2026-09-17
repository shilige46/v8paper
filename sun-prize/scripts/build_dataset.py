from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.problem_bank import ProblemRecord, parse_catalog
from scripts.sync_official import CATALOG_FILES


CSV_FIELDS = (
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
)


def _jsp_number(record: ProblemRecord) -> int:
    return int(record.jsp_id.removeprefix("JSP-"))


def load_snapshot(
    raw_dir: Path, source_commit: str
) -> tuple[list[ProblemRecord], list[str]]:
    records: list[ProblemRecord] = []
    errors: list[str] = []
    for filename in CATALOG_FILES:
        path = raw_dir / filename
        if not path.is_file():
            errors.append(f"{filename}: snapshot file missing")
            continue
        parsed, parse_errors = parse_catalog(
            path.read_text(encoding="utf-8"), filename, source_commit
        )
        records.extend(parsed)
        errors.extend(parse_errors)
    return records, errors


def primary_candidates(records: list[ProblemRecord]) -> list[ProblemRecord]:
    return sorted(
        [
            record
            for record in records
            if record.current_status == "Solved" and record.lean_proof is False
        ],
        key=_jsp_number,
    )


def validate_expected_ids(records: list[ProblemRecord], expected_count: int) -> None:
    ids = [record.jsp_id for record in records]
    if len(ids) != expected_count:
        raise ValueError(f"expected {expected_count} records, found {len(ids)}")
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate JSP ids found")
    expected = [f"JSP-{index:06d}" for index in range(1, expected_count + 1)]
    if sorted(ids) != expected:
        missing = sorted(set(expected) - set(ids))
        extra = sorted(set(ids) - set(expected))
        raise ValueError(f"JSP ids are not consecutive; missing={missing[:5]} extra={extra[:5]}")


def write_outputs(
    records: list[ProblemRecord], jsonl_path: Path, candidates_path: Path
) -> None:
    ordered = sorted(records, key=_jsp_number)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    candidates_path.parent.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in ordered:
            handle.write(
                json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True) + "\n"
            )

    with candidates_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in primary_candidates(ordered):
            data = record.to_dict()
            writer.writerow({field: data[field] for field in CSV_FIELDS})


def _write_failures(path: Path, errors: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for error in errors:
            handle.write(json.dumps({"error": error}, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build normalized Sun Prize datasets")
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--jsonl", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--failures", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=1022)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    source_commit = manifest.get("source_commit", "")
    records, errors = load_snapshot(args.raw_dir, source_commit)

    try:
        validate_expected_ids(records, args.expected_count)
    except ValueError as exc:
        errors.append(str(exc))

    _write_failures(args.failures, errors)
    if errors:
        return 1

    write_outputs(records, args.jsonl, args.candidates)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
