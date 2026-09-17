# Sun Prize Research Design

**Date:** 2026-09-18

## 1. Goal

Build an isolated research workspace inside `shilige46/v8paper` for systematically screening the Justin Sun Prize mathematical problem bank, ranking realistic targets, and later formalizing selected solutions in Lean without touching the repository's existing `README.md` or `index.html`.

The first milestone is **research triage only**: ingest the full 1,022-problem catalog, identify promising candidates, and produce a defensible top-10 shortlist. Proof development begins only after the shortlist is reviewed.

## 2. Repository isolation

All project files live under:

`sun-prize/`

Development occurs on branch:

`sun-prize-research`

No existing project file outside `sun-prize/` is modified during the first milestone.

## 3. Source of truth

Primary source:

- `TheJustinSunPrize/awards` official GitHub repository
- `problems/README.md`
- `problems/catalog-0001-0100.md` through `problems/catalog-1001-1022.md`
- official contribution, attribution, and eligibility documentation

The local workspace stores a dated snapshot plus normalized metadata so that later ranking results are reproducible even if the upstream catalog changes.

## 4. First-milestone architecture

### `sun-prize/data/`

Stores raw upstream snapshots and normalized structured data.

Planned outputs:

- `raw/` — downloaded catalog snapshots with source commit metadata
- `problems.jsonl` — one normalized problem record per line
- `candidates.csv` — human-readable filtered candidate table

Each normalized problem record should preserve, when available:

- JSP id
- title
- date proposed
- mathematical area
- problem description
- current status
- proof contributors
- Lean proof status
- eligibility status
- publication/proof links
- historical bounty text
- public-review status
- upstream source file
- upstream commit SHA

### `sun-prize/scripts/`

Contains small deterministic tools with separate responsibilities:

- catalog ingestion/parsing
- normalization
- candidate filtering
- ranking/report generation

Scripts must not silently infer missing official fields. Unknown values remain explicitly unknown.

### `sun-prize/research/`

Contains human-reviewed research cards for shortlisted problems.

One problem per Markdown file, including:

- exact official statement/status
- available public proof/exposition
- mathematical prerequisites
- likely Lean/Mathlib dependencies
- missing lemmas or formalization bottlenecks
- independent verification concerns
- duplicate-work / race risk
- next concrete experiment

### `sun-prize/lean/`

Reserved for the later proof phase. The first milestone may create only documentation/placeholders required by the plan; it will not claim a formal proof exists.

### `sun-prize/CANDIDATES.md`

The main decision document. It will contain the top-10 shortlist and the evidence behind each candidate.

### `sun-prize/README.md`

Explains the workflow, source provenance, reproducibility commands, and the boundary between research status and official prize eligibility.

## 5. Screening strategy

The scanner first separates the bank into broad buckets:

1. **Solved + Lean proof = No** — primary first-pass target pool.
2. **Open + computationally searchable / finite / constructive** — secondary pool for later experimentation.
3. **Solved + Lean proof = Yes** — excluded from primary formalization targets but useful as examples of accepted proof style and Mathlib infrastructure.
4. **Pinnacle / major long-standing open problems** — tracked for completeness but not prioritized for the first milestone.

The pipeline must not treat `Eligible to claim = No` as permanent impossibility. Instead it records why the problem is currently unavailable and whether completing a missing Lean formalization appears to be the blocking condition under the official rules.

## 6. Candidate evaluation dimensions

The shortlist will compare candidates on factual dimensions rather than a single opaque score. For each candidate record:

- public proof availability and accessibility
- proof length/structure
- theorem maturity / external verification
- Mathlib coverage of prerequisites
- expected number of nontrivial missing lemmas
- dependence on advanced analytic machinery
- dependence on geometry/topology/measure theory infrastructure
- finite/computational reduction potential
- statement ambiguity risk
- attribution/licensing/source clarity
- likelihood another formalization already exists or is actively being developed
- official eligibility blockers visible in the current catalog

A derived priority band may be produced for engineering triage, but the underlying facts must remain visible so the ranking can be challenged and revised.

## 7. Top-10 acceptance criteria

The first milestone is complete when:

1. all 1,022 catalog entries have been parsed or explicitly flagged as parse failures;
2. each record points back to its upstream catalog source and source commit;
3. all `Solved + Lean proof = No` entries are enumerable from structured data;
4. a shortlist of 10 candidates is documented with evidence, not just names;
5. each shortlist entry has at least one concrete next action;
6. the shortlist explicitly calls out race/duplication risk and official eligibility uncertainty;
7. no claim is made that a prize is guaranteed or that a proof is accepted before official validation.

## 8. Initial anchor candidates

`JSP-001007` and `JSP-001010` are useful seed cases because the current official catalog records them as solved while showing no Lean proof. They are not automatically the final top two; the full 1,022-problem scan determines the shortlist.

## 9. Testing and reproducibility

Parsing and filtering must be testable from fixed catalog fixtures.

Minimum test coverage for the first milestone:

- parse a solved problem with Lean proof
- parse a solved problem without Lean proof
- parse an open problem
- preserve multiline publication/proof links
- preserve unknown/blank fields
- reject/flag malformed entries rather than silently dropping them
- verify that the normalized record count matches the catalog count expected from the captured snapshot

The generated candidate report must be reproducible from the saved raw snapshot without network access.

## 10. Non-goals for the first milestone

Not included yet:

- attempting a Pinnacle proof
- claiming a prize
- submitting a PR to the official awards repository
- representing any Lean file as complete without local verification
- large-scale automated theorem proving before candidate selection
- modifying `v8paper` content outside `sun-prize/`

## 11. Later phase

After the top-10 review, select one primary target. Then create a separate implementation/proof plan for that problem covering theorem statement reconstruction, prerequisite lemmas, Mathlib imports, Lean build verification, and upstream submission readiness.
