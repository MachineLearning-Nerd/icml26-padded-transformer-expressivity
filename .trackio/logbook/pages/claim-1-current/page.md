# Claim 1 — exact current audit

## Contract and verdict

Theorem 4.2 asserts two language-class equalities for every admissible width
function under sufficient volume, polynomial padding, and polynomial maximum
width. **Verdict: BLOCKED. Confidence: LOW.**

The previous Lean theorem is not the current verifier: it takes the four hard
source inclusions as hypotheses and proves their set-equality composition.

## Four completed routes

| Route | Method | Result |
| --- | --- | --- |
| 1 | Eight-edge source inclusion reconstruction | Dependency graph closes only if hard inclusions are accepted |
| 2 | Lean signature, kernel, and axiom inspection | 11 reports pass; semantic inclusions remain hypotheses |
| 3 | London–Kanade primary-scope comparison | Supports log-width endpoints, not the new arbitrary-width theorem |
| 4 | Assumption-aware falsification | Printed routing contradicted; admissible repair works; no theorem counterexample |

Raw ledger:
[`routes.json`](../../../../.openresearch/artifacts/claim1/routes.json).
Current checker: `repro/run_claim_routes.py`. Fixed command:

```bash
uv run --locked python repro/run_campaign.py
```

The validator requires all four distinct routes and rejects unsupported
promotion to VERIFIED. Finite tables are regressions only.

## Remaining blockers

A complete certificate must define transformer and circuit semantics and prove
all AC0/TC0 lower and upper inclusions, repaired routing, and uniformity. No
such certificate exists in the candidate.
