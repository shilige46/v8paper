# Lean proof phase

Milestone 1 does **not** claim that any Justin Sun Prize problem has been formalized here.

The current first feasibility target is `JSP-000897`. Before a full proof is attempted, its paper statement and the official JSP scope must be reconstructed exactly and a separate proof implementation plan must be approved.

A future submission-ready proof must:

- formalize the complete original problem / accepted solved statement rather than a weaker special case;
- build under a pinned Lean + Mathlib toolchain;
- contain no `sorry`, `admit`, placeholder axiom, or substitute unproved assumption;
- include enough statement/source documentation for independent scope checking;
- pass local `lake build` / direct Lean compilation;
- be rechecked against live public formalization work immediately before any official submission.

## First planned feasibility spike: JSP-000897

Expected imports to investigate:

```lean
import Mathlib.Combinatorics.SimpleGraph.Extremal.Turan
import Mathlib.Combinatorics.SimpleGraph.Finite
```

The spike should only answer whether Bondy's dense-neighborhood theorem can be stated cleanly using existing `SimpleGraph.turanGraph`, degree, `neighborFinset`, induced-subgraph and edge-cardinality APIs. It is not a proof claim.
