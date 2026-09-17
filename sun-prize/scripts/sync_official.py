from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.request import urlopen


SOURCE_REPOSITORY = "TheJustinSunPrize/awards"
RAW_BASE_URL = "https://raw.githubusercontent.com/TheJustinSunPrize/awards/{commit}/problems/{filename}"
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CATALOG_FILES = (
    "catalog-0001-0100.md",
    "catalog-0101-0200.md",
    "catalog-0201-0300.md",
    "catalog-0301-0400.md",
    "catalog-0401-0500.md",
    "catalog-0501-0600.md",
    "catalog-0601-0700.md",
    "catalog-0701-0800.md",
    "catalog-0801-0900.md",
    "catalog-0901-1000.md",
    "catalog-1001-1022.md",
)


def download_snapshot(
    output_dir: Path, source_commit: str, opener=urlopen
) -> dict[str, object]:
    if not COMMIT_RE.fullmatch(source_commit):
        raise ValueError("source_commit must be a lowercase 40-character Git commit SHA")

    output_dir.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}

    for filename in CATALOG_FILES:
        url = RAW_BASE_URL.format(commit=source_commit, filename=filename)
        final_path = output_dir / filename
        temp_path = output_dir / f".{filename}.tmp"
        try:
            with opener(url) as response:
                data = response.read()
            temp_path.write_bytes(data)
            temp_path.replace(final_path)
        finally:
            if temp_path.exists():
                temp_path.unlink()
        hashes[filename] = hashlib.sha256(data).hexdigest()

    return {
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": source_commit,
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": list(CATALOG_FILES),
        "sha256": hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Download a pinned Sun Prize problem-bank snapshot")
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    manifest = download_snapshot(args.output, args.commit)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
