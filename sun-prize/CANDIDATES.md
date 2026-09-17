# Sun Prize opportunity board

Snapshot date: 2026-09-18  
Pinned catalog source: `TheJustinSunPrize/awards@ff33abd13163e789790eb1014e55f57c05f94432`

> **Status:** the original Top-10 formalization shortlist is retired. A deeper race audit showed that catalog field `Lean proof = No` is not a reliable indicator that a problem is unoccupied. Many problems already have complete public Lean developments, official PRs, or evidence-registration issues that have not yet propagated into the pinned catalog.

This file is now a **race-first opportunity board**. We do not start proof work until a candidate passes the competition gates below.

## Hard gate before any work

For every candidate, check all of the following immediately before investing engineering time:

1. exact JSP id in official `TheJustinSunPrize/awards` pull requests;
2. exact JSP id and original Erdős number in official issues/evidence batches;
3. dedicated public GitHub repositories;
4. global GitHub code search using JSP id, Erdős number, title and source-paper phrases;
5. `plby/lean-proofs` / Formal Conjectures directly by original Erdős number and theorem title;
6. very recent public work (new repositories, papers, SAT searches, proof ports and verification packages).

Any confirmed complete prior formalization moves the target to **NO-GO**, even if the official catalog still says `Lean proof = No`.

## NO-GO — do not spend proof time

The previous shortlist is no longer actionable.

| JSP | Why retired |
| --- | --- |
| JSP-000897 | Multiple official submissions (`#155`, `#439`, `#736`) plus an earlier complete public `plby/lean-proofs` development (`Erdos1079.lean`). |
| JSP-000698 | Official Lean submissions/evidence already exist. |
| JSP-000657 | Existing public Lean source has been registered in the official evidence flow. |
| JSP-000845 | Existing `plby` proof/evidence registration found. |
| JSP-000896 | Official PR / complete proof evidence found. |
| JSP-000842 | Multiple official formalization submissions found. |
| JSP-000641 | Public Lean evidence already exists. |
| JSP-000661 | Official issue records a complete public Lean proof and replay evidence. |
| JSP-000672 | Official PR / `plby` proof found. |
| JSP-000838 | Existing public Lean proof is in official evidence batches. |

Additional examples eliminated during the deep audit include JSP-000760 (`plby` Erdős 916), JSP-000916 (`plby` Erdős 1105), JSP-000632 (`plby` Erdős 771), JSP-000601 (`plby` Erdős 733), JSP-000622/623 (`plby` Erdős 758/759), JSP-000837 (`plby` Erdős 1005), JSP-000907 (official PR `#274` plus stronger `plby` proof), JSP-000314 (`plby` Erdős 380 plus official PR), JSP-000653, JSP-000958, JSP-000455, JSP-000428, JSP-000475, JSP-000476, JSP-000521, JSP-000588, JSP-000514, JSP-000511, JSP-000725, JSP-000728, JSP-000733, JSP-000640, JSP-000619, JSP-000637, JSP-000673, JSP-000689, JSP-000690, JSP-000839, JSP-000840, JSP-000945, JSP-001018, JSP-001021 and most of the obvious solved/Lean-No tail entries.

## Public formalization gaps found, but not worth first attack

These passed the public-race checks performed so far, but fail our time-value test because the mathematical proof stack is too heavy.

| JSP | Visible race | Why deferred |
| --- | --- | --- |
| JSP-000503 | No exact official PR/issue or dedicated Lean repository located in the audit | 2025 solution *Cyclic subsets in regular Dirac graphs* uses dense Hamiltonian graph machinery, stability, probability/regularity and asymptotics. A genuine gap, but expensive to formalize. |
| JSP-000814 | No exact official PR and no matching `plby` proof located | Character sums / analytic number theory / asymptotics. High infrastructure cost. |
| JSP-000966 | No exact official PR and no matching `plby` proof located | The 2025 solution on the most probable order of a random permutation uses local limit/probabilistic number theory machinery. High formalization cost. |
| JSP-000589 | No strong race signal located in the first audit | Finite-looking statement, but the underlying asymmetric van der Waerden/additive-Ramsey proof is deep enough that it is not a cheap formalization arbitrage. |
| JSP-000747 | No exact race signal found | Upper-bound side relies on deep multiplicative-number-theory results; poor first target. |

These are **reserve research gaps**, not active targets.

## Falsifiable/open-problem track

We also screened open problems for a different strategy: find a finite counterexample by SAT/MILP/enumeration, then formalize a small certificate. This could capture mathematical-solver value rather than merely duplicating an old proof.

Several apparently attractive targets are already crowded:

- JSP-000826 / Erdős 993 (tree independence-polynomial unimodality): multi-billion-tree exhaustive searches and active public projects;
- JSP-000500 / Erdős 617: public SAT/certificate work and official `r = 7` Lean submission;
- JSP-000134 / Erdős 128: multiple AI/SAT research campaigns;
- JSP-000082 / Erdős–Gyárfás power-of-two cycle conjecture: active SAT and structural work in 2026;
- JSP-000244 / Erdős 287: exact search and arithmetic pruning already force any counterexample to astronomically large parameters;
- JSP-000395 / Erdős 488: multiple agentic/Lean research projects;
- related classic finite-graph targets such as Gallai path decomposition are also under active computational study.

We will not duplicate these searches unless new evidence shows an exploitable gap.

## Low-cost background probe — JSP-000639 / Erdős 612

**Status:** low visible competition, but not a main green-light target.

Question: for `P = p₁⋯pₙ`, the product of the first `n` primes, must there always be a prime `p` with `pₙ < p < P` for which `P + p` is also prime?

Race audit on 2026-09-18:

- no exact official JSP-000639 PR located;
- no exact official JSP-000639 issue located;
- no dedicated repository located by JSP/Erdős-number search;
- no clear public computational campaign surfaced in the first global code search.

A preliminary disposable runtime probe checked `n = 2..100` and found a witness for every tested `n`, usually after only a modest number of candidate primes. This is **not a proof and is not a persisted verification artifact**. It suggests small-`n` counterexamples are unlikely and that the conjectured witness may be abundant.

Decision: keep this as a cheap/background computational probe only. Stop immediately if witness search cost grows without structural evidence of a counterexample.

## Current decision

**There is no main target with a green light yet.**

That is preferable to spending days reproducing work that already exists or formalizing a theorem whose infrastructure cost dominates any realistic opportunity. The next target must simultaneously satisfy:

- no complete public formalization / official submission found after the full hard-gate search;
- no heavily active computational race if it is an open/falsifiable problem;
- proof or counterexample search has a bounded first experiment that can fail cheaply;
- the result would address the full original JSP problem, not just a scoped lemma or a special case;
- a successful result can be verified reproducibly and converted into a clean public submission quickly.

## Next screening direction

Prioritize two pools:

1. **recently solved 2025–2026 problems** whose solution is short enough to formalize but has not yet reached `plby` / official PRs;
2. **open, finitely falsifiable problems** with low visible competition and a genuinely cheap SAT/enumeration search space.

Do not return to the retired shortlist without rerunning the complete race audit.

## Data caveat

The parser/synchronizer/dataset/triage code is implemented and unit-tested, but this ChatGPT execution runtime could not materialize the full offline 1,022-entry raw snapshot through the local network path. Therefore the race audit combines the pinned official records with live GitHub/official-PR/issue/code searches. `data/problems.jsonl`, `data/candidates.csv`, and `data/triage.csv` must not be represented as generated until the synchronizer runs successfully in a network-capable environment.
