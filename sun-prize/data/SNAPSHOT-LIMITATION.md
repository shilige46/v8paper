# Snapshot execution limitation

Date: 2026-09-18

## What is implemented

`scripts/sync_official.py` deterministically downloads the 11 official catalog volumes at an explicit 40-character commit SHA and writes a manifest containing source repository, commit, UTC fetch time and SHA-256 hashes.

`scripts/build_dataset.py` then requires those saved raw files and validates exactly 1,022 unique consecutive JSP ids before generating normalized JSONL and the `Solved + Lean proof = No` CSV.

Both paths are covered by local unit tests with fixed fixtures/fake network responses.

## What was not executed in this ChatGPT runtime

The local code-execution sandbox could not resolve GitHub/raw.githubusercontent.com over the network. A normal `git clone` / raw catalog download therefore failed before any repository authentication was involved.

The connected GitHub tool can read the official repository and write this research branch, but it does not expose its HTTP transport as a Python `urlopen` adapter. Git object SHAs also cannot be reused across unrelated repositories, so copying the upstream blob SHA directly into `v8paper` was correctly rejected by GitHub.

For that reason this session did **not** create fake or partial versions of:

- `data/snapshot.json`
- `data/problems.jsonl`
- `data/candidates.csv`
- `data/triage.csv`

## How to clear the limitation

Run from `sun-prize/` in any network-capable environment:

```bash
python scripts/sync_official.py \
  --commit ff33abd13163e789790eb1014e55f57c05f94432 \
  --output data/raw \
  --manifest data/snapshot.json

python scripts/build_dataset.py \
  --raw-dir data/raw \
  --manifest data/snapshot.json \
  --jsonl data/problems.jsonl \
  --candidates data/candidates.csv \
  --failures data/parse_failures.jsonl \
  --expected-count 1022

python scripts/make_triage.py \
  --candidates data/candidates.csv \
  --output data/triage.csv \
  --research-dir research
```

Do not consider the offline-data acceptance criterion satisfied until these commands complete successfully and the final count check reports 1,022 unique problems.
