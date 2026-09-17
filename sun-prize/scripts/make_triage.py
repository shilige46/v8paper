from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re


MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)]+)\)")
AUTOLINK_RE = re.compile(r"<(https?://[^>]+)>")
ADVANCED_ANALYSIS_KEYWORDS = (
    "analysis",
    "measure",
    "pde",
    "harmonic",
    "analytic",
    "probability",
    "random",
)
GEOMETRY_TOPOLOGY_KEYWORDS = (
    "geometry",
    "geometric",
    "topology",
    "topological",
    "manifold",
)
FINITE_CONSTRUCTIVE_KEYWORDS = (
    "finite",
    "integer interval",
    "coloring",
    "subset",
    "residue",
    "graph",
    "combinatorics",
)
TRIAGE_FIELDS = (
    "jsp_id",
    "area",
    "has_public_proof_link",
    "proof_link_count",
    "public_review_text",
    "advanced_analysis_flag",
    "geometry_topology_flag",
    "finite_constructive_hint",
    "race_search_needed",
    "research_state",
    "engineering_band",
)


def extract_links(markdown_text: str) -> list[str]:
    found: list[tuple[int, str]] = []
    for pattern in (MARKDOWN_LINK_RE, AUTOLINK_RE):
        for match in pattern.finditer(markdown_text or ""):
            found.append((match.start(), match.group(1)))
    found.sort(key=lambda item: item[0])
    seen: set[str] = set()
    links: list[str] = []
    for _, url in found:
        if url not in seen:
            seen.add(url)
            links.append(url)
    return links


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.casefold()
    return any(keyword in lowered for keyword in keywords)


def classify_row(row: dict[str, str]) -> dict[str, str]:
    publication = row.get("publication_details", "")
    area = row.get("mathematical_area", "")
    title = row.get("title", "")
    links = extract_links(publication)
    advanced = _contains_any(area, ADVANCED_ANALYSIS_KEYWORDS)
    geometry = _contains_any(area, GEOMETRY_TOPOLOGY_KEYWORDS)
    finite_hint = _contains_any(
        f"{area} {title}", FINITE_CONSTRUCTIVE_KEYWORDS
    )

    if not links:
        band = "source-needed"
    elif advanced or geometry:
        band = "inspect"
    else:
        band = "inspect-first"

    return {
        "jsp_id": row.get("jsp_id", ""),
        "area": area,
        "has_public_proof_link": str(bool(links)),
        "proof_link_count": str(len(links)),
        "public_review_text": row.get("public_review", ""),
        "advanced_analysis_flag": str(advanced),
        "geometry_topology_flag": str(geometry),
        "finite_constructive_hint": str(finite_hint),
        "race_search_needed": "True",
        "research_state": "not-reviewed",
        "engineering_band": band,
    }


def _research_card(row: dict[str, str], triage: dict[str, str]) -> str:
    return f"""# {row.get('jsp_id', '')} · {row.get('title', '')}

## Official snapshot fields

- Mathematical area: {row.get('mathematical_area', '')}
- Current status: {row.get('current_status', '')}
- Lean proof: {row.get('lean_proof', '')}
- Eligible to claim: {row.get('eligible_to_claim', '')}
- Source file: {row.get('source_file', '')}
- Source commit: {row.get('source_commit', '')}
- Publication details: {row.get('publication_details', '')}
- Public review: {row.get('public_review', '')}
- Engineering band: {triage['engineering_band']}

## Proof accessibility
Not reviewed yet.

## Likely Lean / Mathlib prerequisites
Not reviewed yet.

## Formalization bottlenecks
Not reviewed yet.

## Duplicate / race check
Not checked yet.

## Eligibility uncertainty
Current official flag copied from snapshot; no award entitlement inferred.

## Next experiment
Read the cited complete-solution source and map its main theorem/lemmas to Mathlib.
"""


def generate_triage(
    candidates_path: Path, output_path: Path, research_dir: Path
) -> list[dict[str, str]]:
    with candidates_path.open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle))

    rows = [classify_row(row) for row in candidates]
    rows.sort(key=lambda row: row["jsp_id"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRIAGE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    research_dir.mkdir(parents=True, exist_ok=True)
    candidate_by_id = {row["jsp_id"]: row for row in candidates}
    for triage in rows:
        if triage["engineering_band"] != "inspect-first":
            continue
        row = candidate_by_id[triage["jsp_id"]]
        (research_dir / f"{triage['jsp_id']}.md").write_text(
            _research_card(row, triage), encoding="utf-8"
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Create transparent Sun Prize triage")
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--research-dir", type=Path, required=True)
    args = parser.parse_args()
    generate_triage(args.candidates, args.output, args.research_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
