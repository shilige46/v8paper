from __future__ import annotations

from dataclasses import asdict, dataclass
import html
import re


HEADING_RE = re.compile(r"^##\s+(JSP-\d{6})\s+·\s+(.+?)\s*$", re.MULTILINE)
ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$")
BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)


@dataclass(frozen=True)
class ProblemRecord:
    jsp_id: str
    title: str
    date_proposed: str
    mathematical_area: str
    problem_description: str
    current_status: str
    proof_contributors: list[str]
    lean_proof: bool | None
    lean_proof_raw: str
    eligible_to_claim: str
    historical_bounty: str
    publication_details: str
    public_review: str
    attribution_basis: str
    source_file: str
    source_commit: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _normalize_cell(value: str) -> str:
    value = BR_RE.sub("\n", value)
    return html.unescape(value).strip()


def _parse_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in block.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        key = match.group(1).strip()
        value = _normalize_cell(match.group(2))
        if key in {"Field", "---"} or set(key) == {"-"}:
            continue
        fields[key] = value
    return fields


def _parse_contributors(status_raw: str) -> list[str]:
    for line in status_raw.splitlines()[1:]:
        if line.startswith("Proof contributors:"):
            raw = line.removeprefix("Proof contributors:").strip()
            return [part.strip().rstrip(".") for part in raw.split(";") if part.strip()]
    return []


def _parse_lean(raw: str) -> bool | None:
    first = raw.splitlines()[0].strip() if raw.strip() else ""
    if first == "No" or first.startswith("No ") or first.startswith("No—") or first.startswith("No —"):
        return False
    if first == "Yes" or first.startswith("Yes ") or first.startswith("Yes—") or first.startswith("Yes —"):
        return True
    return None


def parse_catalog(
    text: str, source_file: str, source_commit: str
) -> tuple[list[ProblemRecord], list[str]]:
    records: list[ProblemRecord] = []
    errors: list[str] = []
    matches = list(HEADING_RE.finditer(text))

    for index, match in enumerate(matches):
        jsp_id, title = match.group(1), match.group(2).strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        fields = _parse_fields(block)
        required = (
            "Date proposed",
            "Mathematical area",
            "Problem description",
            "Current status",
            "Lean proof",
            "Eligible to claim",
        )
        missing = [name for name in required if name not in fields]
        if missing:
            errors.append(f"{source_file}: {jsp_id}: missing fields: {', '.join(missing)}")
            continue

        status_raw = fields["Current status"]
        current_status = status_raw.splitlines()[0].strip()
        lean_raw = fields["Lean proof"]
        records.append(
            ProblemRecord(
                jsp_id=jsp_id,
                title=title,
                date_proposed=fields["Date proposed"],
                mathematical_area=fields["Mathematical area"],
                problem_description=fields["Problem description"],
                current_status=current_status,
                proof_contributors=_parse_contributors(status_raw),
                lean_proof=_parse_lean(lean_raw),
                lean_proof_raw=lean_raw,
                eligible_to_claim=fields["Eligible to claim"],
                historical_bounty=fields.get("Historical bounty", ""),
                publication_details=fields.get("Publication details", ""),
                public_review=fields.get("Public review", ""),
                attribution_basis=fields.get("Attribution basis", ""),
                source_file=source_file,
                source_commit=source_commit,
            )
        )

    return records, errors
