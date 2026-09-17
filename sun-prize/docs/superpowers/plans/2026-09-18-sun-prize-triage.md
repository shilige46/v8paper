# Sun Prize Triage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible first-stage research pipeline that snapshots the 1,022-problem Justin Sun Prize bank, normalizes all entries, enumerates every `Solved + Lean proof = No` target, and produces an evidence-backed top-10 shortlist for later Lean formalization.

**Architecture:** Keep the project isolated under `sun-prize/`. A small Python standard-library pipeline downloads a pinned upstream snapshot, parses each catalog entry into a typed normalized record, writes deterministic JSONL/CSV outputs, and validates the expected 1,022-record count. Human research cards then add proof accessibility, likely Mathlib prerequisites, formalization bottlenecks, duplication risk, and a concrete next experiment before `CANDIDATES.md` is finalized.

**Tech Stack:** Python 3.11+ standard library (`argparse`, `csv`, `dataclasses`, `html`, `json`, `pathlib`, `re`, `urllib.request`, `unittest`), Markdown, CSV, JSONL. Lean is explicitly deferred to the next milestone.

**Spec:** `sun-prize/docs/superpowers/specs/2026-09-18-sun-prize-research-design.md`

## Global Constraints

- Work only on branch `sun-prize-research` for this milestone.
- Modify only paths under `sun-prize/`; do not modify repository-root `README.md` or `index.html`.
- Pin the official source snapshot to `TheJustinSunPrize/awards` commit `ff33abd13163e789790eb1014e55f57c05f94432`.
- Treat the official catalog as a screening source, not as independent verification or a guarantee of an award.
- Preserve unknown/blank official fields as unknown/blank; do not silently infer them.
- Primary automated target pool is exactly `Current status = Solved` and `Lean proof = No`.
- A complete Lean proof must eventually cover the full original problem and contain no `sorry`, `admit`, or substitute unproved assumptions; that proof work is outside this milestone.
- Generated reports must be reproducible from a saved raw snapshot without network access.

---

### Task 1: Create the parser core and fixed fixtures

**Files:**
- Create: `sun-prize/scripts/problem_bank.py`
- Create: `sun-prize/tests/test_problem_bank.py`
- Create: `sun-prize/tests/fixtures/catalog-mini.md`
- Create: `sun-prize/tests/__init__.py`

**Interfaces:**
- Produces: `ProblemRecord` dataclass.
- Produces: `parse_catalog(text: str, source_file: str, source_commit: str) -> tuple[list[ProblemRecord], list[str]]`.
- Produces: `ProblemRecord.to_dict() -> dict[str, object]`.
- Later tasks consume these exact names.

- [ ] **Step 1: Write the three-record fixture**

Create `catalog-mini.md` with exactly three entries:

```markdown
<a id="JSP-000001"></a>
## JSP-000001 · Open example
| Field | Content |
| --- | --- |
| Date proposed | 1900 |
| Mathematical area | Number theory |
| Problem description | An open example. |
| Current status | Open |
| Lean proof | No |
| Eligible to claim | No |
| Historical bounty |  |
| Publication details |  |
| Public review |  |

<a id="JSP-000002"></a>
## JSP-000002 · Solved without Lean
| Field | Content |
| --- | --- |
| Date proposed | 1950 |
| Mathematical area | Combinatorics |
| Problem description | A solved example. |
| Current status | Solved<br>Proof contributors: Alice Example; Bob Example. |
| Lean proof | No |
| Eligible to claim | No |
| Historical bounty |  |
| Publication details | [Proof](https://example.com/proof)<br>[Exposition](https://example.com/exposition) |
| Public review | Unverified. |

<a id="JSP-000003"></a>
## JSP-000003 · Solved with Lean
| Field | Content |
| --- | --- |
| Date proposed | 2000 |
| Mathematical area | Graph theory |
| Problem description | A formalized example. |
| Current status | Solved |
| Lean proof | Yes — [Lean source](https://example.com/proof.lean)<br>Formalization contributors: Carol Example. |
| Eligible to claim | Yes |
| Historical bounty | USD 100 |
| Publication details | [Paper](https://example.com/paper) |
| Public review | Reviewed. |
```

- [ ] **Step 2: Write parser tests before implementation**

`test_problem_bank.py` must assert:

```python
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
```

- [ ] **Step 3: Run tests and confirm they fail because the parser does not exist**

Run from `sun-prize/`:

```bash
python -m unittest discover -s tests -v
```

Expected: import failure for `scripts.problem_bank`.

- [ ] **Step 4: Implement the minimal parser**

`problem_bank.py` must:

```python
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
```

Parse problem blocks from `## JSP-...... · ...` headings, parse Markdown table rows, convert `<br>` to newlines, decode HTML entities, use only the first line of `Current status` as the status, and split a `Proof contributors:` suffix on semicolons while preserving `et al.` text. `Lean proof` maps exact leading `Yes` to `True`, exact leading `No` to `False`, and other forms such as `Reported; standalone source not located` to `None` while preserving `lean_proof_raw`.

Malformed problem blocks append a readable error string containing the source filename and JSP id when available; they must not vanish silently.

- [ ] **Step 5: Run the parser tests**

```bash
python -m unittest discover -s tests -v
```

Expected: all Task 1 tests pass.

- [ ] **Step 6: Commit Task 1**

```bash
git add sun-prize/scripts/problem_bank.py sun-prize/tests
 git commit -m "feat: add Sun Prize catalog parser"
```

---

### Task 2: Add pinned snapshot synchronization

**Files:**
- Create: `sun-prize/scripts/sync_official.py`
- Create: `sun-prize/tests/test_sync_official.py`
- Create: `sun-prize/data/raw/.gitkeep`
- Create: `sun-prize/data/snapshot.json` during the real run

**Interfaces:**
- Produces: `CATALOG_FILES: tuple[str, ...]` containing the 11 official catalog filenames.
- Produces: `download_snapshot(output_dir: Path, source_commit: str, opener=urlopen) -> dict[str, object]`.
- Writes the 11 catalog files under `data/raw/` and metadata to `data/snapshot.json`.

- [ ] **Step 1: Write synchronization tests**

The tests must use a fake opener and no live network. Assert that:

```python
self.assertEqual(11, len(CATALOG_FILES))
self.assertEqual("catalog-0001-0100.md", CATALOG_FILES[0])
self.assertEqual("catalog-1001-1022.md", CATALOG_FILES[-1])
```

Also assert every requested URL contains the supplied 40-character commit and that `snapshot.json` records repository `TheJustinSunPrize/awards`, the commit, and all 11 filenames.

- [ ] **Step 2: Run tests and confirm failure**

```bash
python -m unittest tests.test_sync_official -v
```

Expected: import failure until `sync_official.py` exists.

- [ ] **Step 3: Implement pinned download logic**

Use URLs of the exact form:

```text
https://raw.githubusercontent.com/TheJustinSunPrize/awards/{commit}/problems/{filename}
```

Reject a source commit unless it matches `[0-9a-f]{40}`. Download to temporary sibling files and replace final files only after a successful response, so a failed sync does not silently leave a half-written individual catalog file. Write a manifest containing source repository, commit, UTC fetch timestamp, filenames, and SHA-256 hash of each downloaded file.

- [ ] **Step 4: Run synchronization tests**

```bash
python -m unittest tests.test_sync_official -v
```

Expected: PASS.

- [ ] **Step 5: Run the real snapshot sync at the approved official commit**

```bash
python scripts/sync_official.py \
  --commit ff33abd13163e789790eb1014e55f57c05f94432 \
  --output data/raw \
  --manifest data/snapshot.json
```

Expected: 11 `.md` catalog files and a manifest whose commit is exactly `ff33abd13163e789790eb1014e55f57c05f94432`.

- [ ] **Step 6: Commit Task 2**

```bash
git add sun-prize/scripts/sync_official.py sun-prize/tests/test_sync_official.py sun-prize/data
 git commit -m "feat: snapshot official Sun Prize catalogs"
```

---

### Task 3: Build the normalized 1,022-record dataset and target pool

**Files:**
- Create: `sun-prize/scripts/build_dataset.py`
- Create: `sun-prize/tests/test_build_dataset.py`
- Generate: `sun-prize/data/problems.jsonl`
- Generate: `sun-prize/data/candidates.csv`
- Generate: `sun-prize/data/parse_failures.jsonl`

**Interfaces:**
- Produces: `load_snapshot(raw_dir: Path, source_commit: str) -> tuple[list[ProblemRecord], list[str]]`.
- Produces: `primary_candidates(records: list[ProblemRecord]) -> list[ProblemRecord]` where only `current_status == "Solved" and lean_proof is False` qualifies.
- Produces deterministic JSONL sorted numerically by JSP id.
- Produces CSV with at least: `jsp_id,title,mathematical_area,current_status,lean_proof,eligible_to_claim,publication_details,public_review,source_file,source_commit`.

- [ ] **Step 1: Write filtering and deterministic-output tests**

Use the mini fixture and assert:

```python
self.assertEqual(["JSP-000002"], [r.jsp_id for r in primary_candidates(records)])
```

Write the same dataset twice into separate temporary directories and assert byte-for-byte equality for JSONL and CSV outputs.

- [ ] **Step 2: Add a count-validation test**

Create a helper `validate_expected_ids(records, expected_count)` that checks unique ids are exactly consecutive from `JSP-000001` through `JSP-{expected_count:06d}`. Test duplicates and a missing id both raise `ValueError`.

- [ ] **Step 3: Run Task 3 tests and confirm failure**

```bash
python -m unittest tests.test_build_dataset -v
```

- [ ] **Step 4: Implement dataset building**

The CLI must accept:

```text
--raw-dir data/raw
--manifest data/snapshot.json
--jsonl data/problems.jsonl
--candidates data/candidates.csv
--failures data/parse_failures.jsonl
--expected-count 1022
```

If any parser error exists or the id validation fails, exit nonzero after writing `parse_failures.jsonl`; do not present the dataset as complete.

- [ ] **Step 5: Build the real dataset from the saved snapshot**

```bash
python scripts/build_dataset.py \
  --raw-dir data/raw \
  --manifest data/snapshot.json \
  --jsonl data/problems.jsonl \
  --candidates data/candidates.csv \
  --failures data/parse_failures.jsonl \
  --expected-count 1022
```

Expected: `1022` normalized unique records, zero parse failures, and a nonempty `Solved + Lean No` candidate CSV.

- [ ] **Step 6: Cross-check anchor cases**

Programmatically assert against the real JSONL:

```python
assert by_id["JSP-001007"]["current_status"] == "Solved"
assert by_id["JSP-001007"]["lean_proof"] is False
assert by_id["JSP-001010"]["current_status"] == "Solved"
assert by_id["JSP-001010"]["lean_proof"] is False
```

Also assert `JSP-001001` has `lean_proof is True`, proving the filter distinguishes already-formalized entries.

- [ ] **Step 7: Run the full unit suite**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 8: Commit Task 3**

```bash
git add sun-prize/scripts/build_dataset.py sun-prize/tests/test_build_dataset.py sun-prize/data
 git commit -m "feat: build Sun Prize candidate dataset"
```

---

### Task 4: Create transparent triage fields and research-card generation

**Files:**
- Create: `sun-prize/scripts/make_triage.py`
- Create: `sun-prize/tests/test_make_triage.py`
- Generate: `sun-prize/data/triage.csv`
- Generate: `sun-prize/research/` Markdown cards for the inspected shortlist pool

**Interfaces:**
- Produces: `extract_links(markdown_text: str) -> list[str]`.
- Produces transparent metadata columns, not a hidden mathematical-quality score.
- Required columns: `jsp_id`, `area`, `has_public_proof_link`, `proof_link_count`, `public_review_text`, `advanced_analysis_flag`, `geometry_topology_flag`, `finite_constructive_hint`, `race_search_needed`, `research_state`.

- [ ] **Step 1: Write tests for transparent feature extraction**

Test that a record with two Markdown links yields `proof_link_count == 2`; a blank publication field yields zero; areas containing `Analysis`, `Measure`, `Topology`, or `PDE` set the advanced-analysis/geometry-topology flags according to explicit keyword lists; keywords such as `finite`, `integer interval`, `coloring`, `subset`, `residue`, and `graph` are recorded only as hints, never as proof of easy formalizability.

- [ ] **Step 2: Run tests and confirm failure**

```bash
python -m unittest tests.test_make_triage -v
```

- [ ] **Step 3: Implement triage generation**

`make_triage.py` reads `candidates.csv` and writes `triage.csv`. It must not output a single unexplained numeric score. It may output a transparent `engineering_band` with only three values:

- `inspect-first`: public proof/exposition link exists and no advanced-analysis/geometry-topology keyword is present;
- `inspect`: public proof/exposition link exists but advanced infrastructure keywords are present;
- `source-needed`: no directly recorded publication/proof link exists.

This band is only a queueing device, not a claim that one mathematical problem is intrinsically easier.

- [ ] **Step 4: Generate research-card skeletons for the first inspection pool**

For every `inspect-first` row, create `research/JSP-xxxxxx.md` containing the exact normalized official fields plus empty human-review sections with explicit state markers:

```markdown
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
```

These phrases are deliberate research-state values, not implementation placeholders; generated cards must never imply review has occurred when it has not.

- [ ] **Step 5: Run Task 4 tests and generate `triage.csv`**

```bash
python -m unittest tests.test_make_triage -v
python scripts/make_triage.py --candidates data/candidates.csv --output data/triage.csv --research-dir research
```

Expected: deterministic triage rows for every primary candidate.

- [ ] **Step 6: Commit Task 4**

```bash
git add sun-prize/scripts/make_triage.py sun-prize/tests/test_make_triage.py sun-prize/data/triage.csv sun-prize/research
 git commit -m "feat: add transparent Sun Prize triage"
```

---

### Task 5: Perform evidence review and publish the top-10 shortlist

**Files:**
- Modify: exactly 10 selected files under `sun-prize/research/`
- Create: `sun-prize/CANDIDATES.md`
- Create: `sun-prize/README.md`
- Create: `sun-prize/lean/README.md`

**Interfaces:**
- `CANDIDATES.md` is the human decision artifact for the next milestone.
- Each chosen card must include source evidence, not only a title/status row.

- [ ] **Step 1: Build a 30-problem inspection queue**

From `triage.csv`, take all `inspect-first` candidates in stable JSP order and inspect at least the first 30. If fewer than 30 exist, append `inspect` candidates until 30 are reviewed. For each, read the cited complete-solution paper/exposition and current official entry.

- [ ] **Step 2: Check duplicate/race risk for all 30**

Search GitHub and the official awards repository for the JSP id, exact title, and obvious Lean formalization references. Record one of `no complete Lean source located`, `possible active work located`, or `complete Lean source located`. Any candidate with a complete qualifying Lean source located is removed from the top-10 queue even if the pinned catalog still says `No`, and the discrepancy is documented.

- [ ] **Step 3: Fill evidence sections for the best-supported candidates**

For each contender record:

- direct proof/exposition URLs;
- rough proof structure in 3–8 bullets;
- prerequisite mathematical objects;
- likely Mathlib namespaces/theorem families after repository search;
- expected nontrivial missing lemmas;
- whether the argument is finite/computational, elementary discrete, algebraic, analytic, geometric/topological, or set-theoretic;
- source ambiguity or theorem-scope risk;
- duplicate/race result;
- one concrete Lean feasibility experiment.

Do not invent absent information. Mark unverifiable claims explicitly as unverified.

- [ ] **Step 4: Select exactly 10 research targets**

Selection must be based on the recorded factual dimensions. `CANDIDATES.md` must show a comparison table with exactly 10 rows and columns for: JSP id, area, proof source, proof structure profile, likely Lean infrastructure, main bottleneck, race risk, current official eligibility flag, and next experiment.

The document may use `Primary`, `Secondary`, and `Watch` engineering work queues, but must not claim prize probability or guaranteed payment.

- [ ] **Step 5: Document reproducibility and project boundaries**

`README.md` must include commands:

```bash
python -m unittest discover -s tests -v
python scripts/build_dataset.py --raw-dir data/raw --manifest data/snapshot.json --jsonl data/problems.jsonl --candidates data/candidates.csv --failures data/parse_failures.jsonl --expected-count 1022
python scripts/make_triage.py --candidates data/candidates.csv --output data/triage.csv --research-dir research
```

It must state the pinned official commit and that the project is independent research, not an official award record.

`lean/README.md` must say no Lean proof work has been claimed complete in milestone 1 and that the selected target will receive its own proof plan.

- [ ] **Step 6: Run final verification**

Run:

```bash
python -m unittest discover -s tests -v
python - <<'PY'
import csv, json
from pathlib import Path
rows = [json.loads(line) for line in Path('data/problems.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
assert len(rows) == 1022
assert len({r['jsp_id'] for r in rows}) == 1022
with Path('data/candidates.csv').open(encoding='utf-8', newline='') as f:
    candidates = list(csv.DictReader(f))
assert candidates
assert all(r['current_status'] == 'Solved' for r in candidates)
assert all(r['lean_proof'] == 'False' for r in candidates)
print(f'validated problems={len(rows)} primary_candidates={len(candidates)}')
PY
```

Expected: tests pass; 1,022 unique normalized problems; every primary candidate is solved with no recorded Lean proof.

- [ ] **Step 7: Review repository scope**

Verify `git diff main...HEAD --name-only` contains no path outside `sun-prize/`.

- [ ] **Step 8: Commit milestone 1**

```bash
git add sun-prize
 git commit -m "docs: shortlist Sun Prize formalization targets"
```

---

## Plan self-review

- Spec coverage: snapshot provenance, all 1,022 records, parse failures, primary `Solved + Lean No` enumeration, top-10 evidence cards, race checks, reproducibility, and no premature proof/award claim are all assigned to tasks.
- Placeholder scan: implementation steps specify exact behavior and tests. Research cards intentionally use explicit `Not reviewed yet` state values only until Task 5 evidence review replaces them for contenders.
- Type consistency: `ProblemRecord`, `parse_catalog`, `primary_candidates`, JSONL/CSV field names, and the pinned source commit are consistent across tasks.
