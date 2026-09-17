# First-pass candidate inspection

Date: 2026-09-18

Pinned official catalog commit: `ff33abd13163e789790eb1014e55f57c05f94432`.

This is a research triage log, not an official eligibility record. `No dedicated repo located` means that a GitHub repository-name search for the JSP id did not return an obvious formalization repository at the time of checking; it does **not** prove that no private, differently named, or unindexed work exists.

## Screening log

| JSP | Pinned state | First-pass disposition | Race / bottleneck note |
| --- | --- | --- | --- |
| JSP-000288 | Solved / Lean No | Exclude for now | Public `JSP000288.lean` already located in `aichiwuhuarou/jsp-lean-proofs`; high race risk. |
| JSP-000301 | Solved / Lean No | Exclude | Multiple public Lean efforts / official-repo issue activity already located; very high race risk. |
| JSP-000307 | Solved / Lean No | Exclude | At least five dedicated public formalization repositories located. |
| JSP-000313 | Solved / Lean No | Defer | Density of squarefree entries in Pascal rows; analytic/number-theoretic machinery dominates. |
| JSP-000314 | Solved / Lean No | Defer | Recent analytic number theory result on largest prime factors; likely substantial infrastructure. |
| JSP-000315 | Solved / Lean No | Defer | Asymptotics of highly composite numbers; analysis-heavy. |
| JSP-000640 | Solved / Lean No | Exclude for now | Dedicated public `jsp-000640-lean` repository located. |
| JSP-000641 | Solved / Lean No | **Shortlist** | Finite two-colouring / descending-wave theorem; no dedicated JSP repository located. Custom definitions likely main cost. |
| JSP-000643 | Solved / Lean No | Defer | Small-sieve / multiplicative-density machinery. |
| JSP-000644 | Solved / Lean No | Defer | Sieve and density estimates; infrastructure cost high. |
| JSP-000653 | Solved / Lean No | Watch | Direct modern source exists and no dedicated JSP repo located, but sharp multiplicative asymptotics appear substantial. |
| JSP-000655 | Solved / Lean No | Defer | Acyclic-colouring proof is probabilistic; probability infrastructure likely dominates. |
| JSP-000657 | Solved / Lean No | **Shortlist** | Five-page 1994 finite graph/Ramsey paper; no dedicated JSP repo located. |
| JSP-000658 | Solved / Lean No | Watch | Finite graph statement but proof is probabilistic/Ramsey-type. |
| JSP-000660 | Solved / Lean No | Defer | Regular-subgraph problem culminates in a modern extremal proof; larger theorem stack. |
| JSP-000661 | Solved / Lean No | **Shortlist** | Nine-page graph-independence paper; no dedicated JSP repo located, but logarithmic asymptotics increase Lean cost. |
| JSP-000663 | Solved / Lean No | Watch | Additive-combinatorial basis theorem; no obvious JSP repo located. |
| JSP-000671 | Solved / Lean No | Defer | Later proof is long and technically deep; poor first Lean target. |
| JSP-000672 | Solved / Lean No | **Shortlist** | Pure finite graph/cycle structure; no dedicated JSP repo located, but theorem-scope matching needs care. |
| JSP-000673 | Solved / Lean No | Exclude for now | Public `jsp-000673-formalization` repository exists (currently small/empty when inspected); active-work signal. |
| JSP-000688 | Solved / Lean No | Watch | Hypergraph chromatic-number theorem; finite but likely probabilistic. |
| JSP-000689 | Solved / Lean No | Exclude for now | Dedicated public Lean repository located. |
| JSP-000690 | Solved / Lean No | Exclude | Multiple dedicated public Lean repositories located. |
| JSP-000697 | Solved / Lean No | Defer | Solution uses arithmetic geometry / hyperelliptic curves. |
| JSP-000698 | Solved / Lean No | **Shortlist** | Cycle-plus-triangles 3-colouring; no dedicated JSP repo located. Mathlib already contains Combinatorial Nullstellensatz. |
| JSP-000699 | Solved / Lean No | Defer | Infinite/asymptotic subset-sum completeness theorem. |
| JSP-000838 | Solved / Lean No | **Shortlist / watch** | Short source but probabilistic method; no dedicated JSP repo located. |
| JSP-000839 | Solved / Lean No | Exclude for now | Dedicated public `jsp-000839-lean-proof` located. |
| JSP-000840 | Solved / Lean No | Exclude for now | Dedicated public `jsp-000840-lean-proof` located. |
| JSP-000842 | Solved / Lean No | **Shortlist** | Finite graph cycles; Mathlib has Hamiltonian/cycle infrastructure; no dedicated JSP repo located. |
| JSP-000845 | Solved / Lean No | **Shortlist** | Multiple-copy Ramsey / disjoint monochromatic cliques; finite and matching infrastructure exists. |
| JSP-000848 | Solved / Lean No | Defer | Nonplanarity/topological-minor formalization is a large infrastructure commitment. |
| JSP-000849 | Solved / Lean No | Defer | Planarity/maximal-planar vocabulary is not as mature in Mathlib as basic finite graph infrastructure. |
| JSP-000895 | Solved / Lean No | Defer | Modern locally sparse Steiner-system machinery; too deep for first target. |
| JSP-000896 | Solved / Lean No | **Shortlist** | Balanced multipartite transversal clique; Mathlib has complete multipartite/equipartite graph infrastructure; no dedicated JSP repo located. |
| JSP-000897 | Solved / Lean No | **Shortlist — first experiment** | Very short finite extremal graph theorem; Mathlib already contains Turán's theorem, neighborhoods, induced subgraphs, edge counts. No dedicated JSP repo located. |
| JSP-000945 | Solved / Lean No | Exclude | Several dedicated public Lean/formalization repositories located. |
| JSP-001016 | Solved / Lean No | Defer | Logarithmic-density Ramsey theorem; analytic/additive infrastructure cost. |
| JSP-001018 | Solved / Lean No | Exclude for now | At least two dedicated public formalization repositories located. |
| JSP-001021 | Solved / Lean No | Exclude for now | Dedicated public Lean proof repository located. |
| JSP-001022 | Solved / Lean No | Defer | Recent deep number-theory proof on primitive sets/divisibility chains. |

## Reusable Mathlib infrastructure located

- `Mathlib/Combinatorics/SimpleGraph/Extremal/Turan.lean` — formal Turán theorem and canonical Turán graphs.
- `Mathlib/Combinatorics/SimpleGraph/Finite.lean` — finite neighborhoods, induced subgraphs, edge-set/cardinality lemmas.
- `Mathlib/Combinatorics/SimpleGraph/Matching.lean` — graph matchings and support.
- `Mathlib/Combinatorics/SimpleGraph/Hamiltonian.lean` — Hamiltonian paths/cycles.
- `Mathlib/Combinatorics/Nullstellensatz.lean` — Noga Alon's Combinatorial Nullstellensatz.
- `Mathlib/Combinatorics/SimpleGraph/CompleteMultipartite.lean` — complete multipartite/equipartite graph infrastructure.

## Main conclusion of this pass

The low-hanging counterexample problems are already attracting substantial public formalization activity. Our better niche is the next layer: short or medium finite graph theorems whose core infrastructure already exists in Mathlib but whose JSP id does not yet have an obvious dedicated public formalization repository.
