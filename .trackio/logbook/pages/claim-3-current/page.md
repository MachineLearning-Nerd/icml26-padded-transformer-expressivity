# Claim 3 — exact current audit

## Contract and verdict

For every `d>=1`, Theorem 5.1 asserts exact FO-uniform AC^d/TC^d
characterizations for the stated precision/width regimes with
`Theta(log^d N)` looping. **Verdict: BLOCKED. Confidence: LOW.**

## Four completed routes

| Route | Method | Result |
| --- | --- | --- |
| 1 | Lemmas 5.1–5.4 proof decomposition | Coherent plan, but semantic reductions/uniformity not mechanized |
| 2 | Deterministic/exhaustive bounded composition | 54 maps and 3,024 cases pass; finite only |
| 3 | Merrill–Sabharwal primary-scope comparison | Supports growing-precision AHAT endpoint, not both new extensions |
| 4 | Assumption-aware falsification | No valid language-class counterexample found |

Raw ledger:
[`routes.json`](../../../../.openresearch/artifacts/claim3/routes.json).
The checker fails closed if a fourth falsification route is absent or ignores
the theorem assumptions. The historical truth tables remain regression
evidence, not a universal proof.
