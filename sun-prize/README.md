# Sun Prize Research Workspace

Independent research workspace for screening the Justin Sun Prize mathematical problem bank and selecting Lean formalization targets.

This directory is intentionally isolated from the existing `v8paper` site. Work for this project lives only under `sun-prize/` on branch `sun-prize-research` during milestone 1.

## Current status

Milestone 1 implementation is in place:

- catalog parser with explicit parse-failure reporting;
- pinned official snapshot synchronizer;
- deterministic 1,022-record dataset builder with contiguous-ID validation;
- exact `Solved + Lean proof = No` candidate filter;
- transparent triage generator;
- first-pass inspection log covering more than 30 candidate problems;
- evidence-backed top-10 research shortlist in [`CANDIDATES.md`](CANDIDATES.md);
- individual research cards for the top 10.

The current first feasibility target is **JSP-000897**, because it is a short finite Turán/neighborhood theorem with unusually strong existing Mathlib support and no obvious dedicated public JSP repository found during the 2026-09-18 race check.

## Source provenance

Approved pinned official source:

```text
TheJustinSunPrize/awards
commit ff33abd13163e789790eb1014e55f57c05f94432
```

Expected official catalog volumes:

```text
catalog-0001-0100.md
catalog-0101-0200.md
catalog-0201-0300.md
catalog-0301-0400.md
catalog-0401-0500.md
catalog-0501-0600.md
catalog-0601-0700.md
catalog-0701-0800.md
catalog-0801-0900.md
catalog-0901-1000.md
catalog-1001-1022.md
```

The pinned snapshot is used for reproducible screening. Live GitHub searches are a separate overlay used for race/duplication checks because formalization activity can change after the pinned commit.

## Reproduce the pipeline

Use Python 3.11+ from the `sun-prize/` directory.

### 1. Run tests

```bash
python -m unittest discover -s tests -v
```

### 2. Download the pinned official snapshot

```bash
python scripts/sync_official.py \
  --commit ff33abd13163e789790eb1014e55f57c05f94432 \
  --output data/raw \
  --manifest data/snapshot.json
```

### 3. Build normalized data and the primary candidate pool

```bash
python scripts/build_dataset.py \
  --raw-dir data/raw \
  --manifest data/snapshot.json \
  --jsonl data/problems.jsonl \
  --candidates data/candidates.csv \
  --failures data/parse_failures.jsonl \
  --expected-count 1022
```

The builder exits nonzero if parsing fails, ids are duplicated/missing, or the normalized problem count is not exactly 1,022.

### 4. Generate transparent triage metadata

```bash
python scripts/make_triage.py \
  --candidates data/candidates.csv \
  --output data/triage.csv \
  --research-dir research
```

The triage stage deliberately avoids a hidden numerical “difficulty score.” It exposes source availability, broad infrastructure flags and research state so a human can challenge the queue.

## Runtime limitation recorded for this session

The ChatGPT code-execution sandbox used to develop milestone 1 could run Python tests but could not resolve/access GitHub over the network. The GitHub connector could inspect and edit repositories, but it cannot be passed directly into the local Python process as a network transport. Therefore the code and shortlist were completed, but this session did **not** fabricate `data/problems.jsonl`, `data/candidates.csv`, `data/triage.csv` or a fake `data/snapshot.json`.

See [`data/SNAPSHOT-LIMITATION.md`](data/SNAPSHOT-LIMITATION.md). The full offline artifacts should be generated only after `sync_official.py` succeeds in a network-capable environment.

## Research artifacts

- [`CANDIDATES.md`](CANDIDATES.md) — exactly 10 current targets and next experiments.
- [`research/INSPECTION.md`](research/INSPECTION.md) — first-pass screening / exclusions / race findings.
- `research/JSP-*.md` — evidence cards for the shortlist.
- [`lean/README.md`](lean/README.md) — boundary and next-phase expectations.
- `docs/superpowers/specs/` — approved design.
- `docs/superpowers/plans/` — milestone-1 implementation plan.

## Prize / eligibility boundary

This repository is independent research, not an official award record. A catalog row saying `Solved` does not establish that a new Lean file will be accepted, and `Lean proof = No` does not guarantee nobody else is working on it. Official submission rules, theorem scope, attribution, dates, Lean verification and committee review remain controlling.

No file in this workspace should describe a Lean proof as complete unless it has been built with the pinned Lean/Mathlib environment, contains no `sorry`/`admit`/unproved substitute assumptions, and matches the complete original problem statement.
