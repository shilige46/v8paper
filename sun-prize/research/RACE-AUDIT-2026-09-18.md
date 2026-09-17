# Deep race audit · 2026-09-18

## Purpose

Prevent wasted work. The official problem catalog can still say `Lean proof = No` while complete public Lean work is already present in a PR, issue/evidence batch, external repository, or `plby/lean-proofs`.

The audit therefore treats catalog status as **problem metadata**, not as proof that a target is unoccupied.

## Required race-clearance procedure

A candidate cannot enter active development until all six checks are performed:

1. official `TheJustinSunPrize/awards` PR search by JSP id;
2. official issue search by JSP id and original Erdős number;
3. GitHub repository-name search;
4. global GitHub code search by JSP id, Erdős number, title, distinctive source-paper terms;
5. direct `plby/lean-proofs` search by original Erdős number/title;
6. current/recent public activity check, including new papers and computational campaigns.

A single complete prior proof is enough to retire a formalization target unless our contribution is materially different and the official rules clearly make that difference valuable.

## Failure of the first shortlist

The original shortlist over-weighted `Solved + Lean proof = No` and repository-name search. JSP-000897 exposed the flaw: dedicated-repository search looked clean, but official PR search revealed several complete submissions and an older `plby` proof.

The following original Top-10 entries are now retired because prior public Lean work/evidence exists:

- JSP-000897
- JSP-000698
- JSP-000657
- JSP-000845
- JSP-000896
- JSP-000842
- JSP-000641
- JSP-000661
- JSP-000672
- JSP-000838

## Representative hidden prior work found

Examples showing why each search layer matters:

- JSP-000897: official PRs #155, #439, #736 and prior `plby` Erdős 1079;
- JSP-000760: no obvious JSP-named repository was required; direct original-number lookup found `plby` Erdős 916;
- JSP-000916: direct source/title lookup found `plby` Erdős 1105;
- JSP-000632: `plby` Erdős 771;
- JSP-000601: `plby` Erdős 733;
- JSP-000622/623: `plby` Erdős 758/759;
- JSP-000837: `plby` Erdős 1005;
- JSP-000907: official PR #274 explicitly states that a stronger prior `plby` proof already exists;
- JSP-000314: official PR activity plus a large existing `plby` Erdős 380 development;
- JSP-000958: official PR #144 carries full public formalization evidence despite the stale catalog snapshot;
- JSP-000653: official PR #732 and earlier scoped formal evidence;
- JSP-000500: official PR #80 covers the `r=7` case and public SAT/certificate work covers additional cases.

This is not an exhaustive blacklist. The race state changes daily.

## Formalization gaps that appear real but are expensive

### JSP-000503

Official status in the pinned snapshot: `Solved / Lean proof = No`.

No exact official PR/issue or matching public Lean repository was located during this audit. The 2025 solution paper, however, uses dense Hamiltonian graph machinery and substantial probabilistic/stability infrastructure. This is a real-looking gap but a poor first investment.

### JSP-000814

No matching public Lean proof or official PR located. The solution concerns average first-passage times for character sums and sits in analytic number theory. Formalization cost is expected to be high.

### JSP-000966

No matching public Lean proof or official PR located. The 2025 solution on the most probable order of a random permutation uses local-limit/probabilistic-number-theory machinery. Also high cost.

Conclusion: **empty does not imply attractive**.

## Falsifiable/open-problem track audited

We screened a second strategy: solve an open problem by finding a finite counterexample, then formalize the small certificate.

Targets rejected because the computational frontier is already crowded or far advanced:

- Erdős 993 / JSP-000826: exhaustive tree searches into billions of trees plus active public projects;
- Erdős 617 / JSP-000500: official formal work and public SAT/certificate research;
- Erdős 128 / JSP-000134: multiple public AI/SAT campaigns;
- Erdős–Gyárfás power-of-two cycle problem / JSP-000082: active SAT and structural research in 2026;
- Erdős 287 / JSP-000244: official verification work has already forced any counterexample to enormous parameters, making naive search worthless;
- Erdős 488 / JSP-000395: multiple agentic/Lean research projects;
- Gallai path decomposition and other classic finite-graph conjectures: active computational literature/frontiers.

## One low-visible-competition probe retained

### JSP-000639 / Erdős 612

Question: for the primorial-like product `P = p₁⋯pₙ`, is there always a prime `p` with `pₙ < p < P` such that `P + p` is prime?

Competition checks performed:

- no exact official JSP-000639 PR found;
- no exact official JSP-000639 issue found;
- no dedicated JSP/Erdős-612 repository found in the first repository search;
- no obvious public computational campaign surfaced in the first global code search.

A disposable runtime probe found witnesses for every `n = 2..100`, generally after few candidate primes. This makes small counterexamples look unlikely. The probe is not persisted proof evidence and must be reproduced before citing numerical bounds.

Use only as a cheap background experiment. Do not make it the main project without a new structural signal.

## Current conclusion

As of this audit, **no target has earned a full green light**.

This is a successful screening outcome: the purpose is to protect engineering time, not to force a candidate. We should invest only after finding an opportunity with both low visible competition and bounded proof/search cost.

The next search should concentrate on:

- 2025–2026 recently solved problems with short/elementary proofs that have not reached the existing Lean pipelines;
- open, finitely falsifiable problems that do not already have active SAT/agentic campaigns;
- newly added JSP entries where there has been less time for bulk formalization.
